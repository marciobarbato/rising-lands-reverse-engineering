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
