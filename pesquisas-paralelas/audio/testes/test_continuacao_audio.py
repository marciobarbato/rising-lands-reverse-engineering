"""Replay original-first buffer reuse/promotion cases without native execution."""
import json
from pathlib import Path
import sys
import unittest
OWNED=Path(__file__).resolve().parents[1];sys.path.insert(0,str(OWNED))
from audio_queue_fixtures import QueueFixtureMemory,COM_DUPLICATE,TABLE
from reproduzir_fila_audio import compare,replay


class AudioContinuationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capture=json.loads((OWNED/'evidencias/captura-continuacao-audio-original-v1.json').read_text())
        cls.cases={c['name']:c for c in cls.capture['cases']}

    def test_all_118_original_cases(self):
        self.assertFalse(self.capture['translation_executed']);self.assertEqual(self.capture['native_calls'],118)
        for case in self.capture['cases']:
            with self.subTest(case=case['name']):self.assertEqual(compare(case)[0],[])

    def test_duplicate_position_error_does_not_replace_output(self):
        result=replay(self.cases['duplicate-0-7101100-80004005'])
        self.assertEqual(result['value'],COM_DUPLICATE)
        self.assertEqual([c['method'] for c in result['com']],['DuplicateSoundBuffer','SetPosition'])

    def test_duplicate_error_keeps_reservation_and_no_record_pointer_store(self):
        case=self.cases['create-logical--1-80004005-7101100-0'];result=replay(case)
        before=QueueFixtureMemory.restore(case['input']['memory']);after=QueueFixtureMemory.restore(result['output'])
        self.assertEqual(result['value'],0);self.assertEqual(after.u32(0x498f64),0)
        self.assertEqual(after.u32(0x522170),before.u32(0x522170))
        self.assertEqual(after.u32(0x52216c),0)

    def test_physical_promotion_transfers_inherited_duplicate_identity(self):
        result=replay(self.cases['destroy-promote-0-1']);m=QueueFixtureMemory.restore(result['output'])
        self.assertEqual(m.u32(0x52211c),COM_DUPLICATE)
        self.assertEqual(m.u32(TABLE+10*44+32),0x52211c)
        self.assertEqual(m.u32(TABLE+10*44+36),0)
        self.assertEqual(m.u32(0x498f64),0xffffffff)

    def test_clear_list_error_hresult_uses_explicit_stopped_mask(self):
        for logical in (0,1):
            results=[replay(self.cases[f'clear-list-{logical}-{status}']) for status in (0,1,5)]
            self.assertEqual([len(r['com']) for r in results],[4,1,1])
            self.assertEqual(QueueFixtureMemory.restore(results[0]['output']).u8(TABLE+8),0)


class AudioConcurrentDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capture=json.loads((OWNED/'evidencias/captura-continuacao-audio-original-v3.json').read_text())
        cls.cases={c['name']:c for c in cls.capture['cases']}

    def test_all_139_native_calls_and_132_scenarios(self):
        self.assertFalse(self.capture['translation_executed'])
        self.assertEqual((self.capture['native_calls'],self.capture['scenarios']),(139,132))
        for case in self.capture['cases']:
            with self.subTest(case=case['name']):self.assertEqual(compare(case)[0],[])

    def test_concurrent_same_bank_reuses_physical_identity_and_duplicates(self):
        for count in (2,3):
            result=replay(self.cases[f'manage-concurrent-{count}-1']);m=QueueFixtureMemory.restore(result['output'])
            self.assertEqual(m.u32(0x498f60),0);self.assertEqual(m.u32(0x498f64),count-2)
            self.assertEqual(m.u32(0x498f68),19)
            self.assertEqual(sum(c['method']=='CreateSoundBuffer' for c in result['com']),1)
            self.assertEqual(sum(c['method']=='DuplicateSoundBuffer' for c in result['com']),count-1)

    def test_matching_ids_with_distinct_banks_do_not_share_buffers(self):
        result=replay(self.cases['manage-concurrent-3-0']);m=QueueFixtureMemory.restore(result['output'])
        self.assertEqual(m.u32(0x498f60),2);self.assertEqual(m.u32(0x498f64),0xffffffff)
        self.assertEqual(sum(c['method']=='CreateSoundBuffer' for c in result['com']),3)
        self.assertFalse(any(c['method']=='DuplicateSoundBuffer' for c in result['com']))

    def test_resident_compressed_reuses_stage1_original_extent_quirk(self):
        result=replay(self.cases['manage-data-1-1']);m=QueueFixtureMemory.restore(result['output'])
        before=QueueFixtureMemory.restore(self.cases['manage-data-1-1']['input']['memory'])
        self.assertFalse(any(c['method'] in ('_llseek','_hread') for c in result['com']))
        create=next(c for c in result['com'] if c['method']=='CreateSoundBuffer')
        self.assertEqual(int.from_bytes(bytes.fromhex(create['args'][0])[8:12],'little'),256)
        lock=next(c for c in result['com'] if c['method']=='Lock');self.assertEqual(lock['args'],[0,64,0])
        self.assertNotEqual(m.read(0x7004040,176),before.read(0x7004040,176))
        self.assertEqual(m.read(0x7004100,16),before.read(0x7004100,16))

    def test_persistent_sequence_preserves_each_original_state_and_live_refs(self):
        result=replay(self.cases['post-manage-promotion-repost-cancel-sequence'])
        self.assertEqual(len(result['steps']),8)
        self.assertEqual(result['steps'],self.cases['post-manage-promotion-repost-cancel-sequence']['steps'])
        m=QueueFixtureMemory.restore(result['output'])
        self.assertEqual(m.u32(0x7000100+72*4),0xffffffff)
        self.assertEqual(m.u32(0x52211c),COM_DUPLICATE)
        self.assertEqual(m.u32(0x498f64),0xffffffff)
