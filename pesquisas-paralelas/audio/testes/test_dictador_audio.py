"""Original-first entry-word256 lifecycle and explicit platform-boundary tests."""
import json
from pathlib import Path
import sys
import unittest
OWNED=Path(__file__).resolve().parents[1];sys.path.insert(0,str(OWNED))
from audio_queue_fixtures import QueueFixtureMemory,ScriptedCOM,REFS
from fila_audio import AudioQueue
from bancos_som import DependenciaSom
from reproduzir_fila_audio import compare,replay


class DictatorAudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=json.loads((OWNED/'evidencias/captura-dictador-audio-original-v3.json').read_text())
        cls.cases={c['name']:c for c in cls.original['cases']}

    def test_all_140_actual_entries_and_35_scenarios(self):
        self.assertEqual((self.original['native_calls'],self.original['planned_calls'],self.original['scenarios']),(140,140,35))
        self.assertFalse(self.original['translation_executed'])
        for case in self.original['cases']:
            with self.subTest(case=case['name']):self.assertEqual(compare(case)[0],[])

    def test_init_preserves_uninitialized_slot_word_and_allocation_counter(self):
        case=self.cases['init-7009000'];before=QueueFixtureMemory.restore(case['input']['memory'])
        after=QueueFixtureMemory.restore(replay(case)['output'])
        self.assertEqual(after.u32(0x7009000),before.u32(0x7009000))
        self.assertEqual(after.u32(0x7009004),0x521f94)
        self.assertEqual(after.u32(0x522230),(before.u32(0x522230)+1)&0xffffffff)
        self.assertEqual(after.u32(0x521fb4),0x7009000)

    def test_requested_loop_flag_is_cleared_by_original_dictator_branch(self):
        result=replay(self.cases['clear-list-1-1-0']);m=QueueFixtureMemory.restore(result['output'])
        self.assertEqual(m.u32(0x521fa0),0)
        self.assertEqual(next(c for c in result['com'] if c['method']=='Play')['args'],[0,0,0])

    def test_is_stopped_uses_written_mask_despite_error_hresult(self):
        states=[]
        for status in (0,1,5):
            result=replay(self.cases[f'clear-list-0-{status}-80004005'])
            states.append(QueueFixtureMemory.restore(result['output']).u32(0x521f90))
        self.assertEqual(states,[0,1,1])

    def test_explicit_clear_releases_even_after_stop_error(self):
        result=replay(self.cases['clear-explicit-0-1-80004005']);m=QueueFixtureMemory.restore(result['output'])
        self.assertEqual([c['method'] for c in result['com']][-3:],['GetStatus','Stop','Release'])
        self.assertEqual(m.u32(0x521f90),0);self.assertEqual(m.u32(REFS+72*4),0xffffffff)

    def test_start_failures_still_claim_separate_dictator_record(self):
        for failure in ('position','volume','play'):
            result=replay(self.cases['start-error-'+failure]);m=QueueFixtureMemory.restore(result['output'])
            self.assertEqual(result['value'],0);self.assertEqual(m.u32(0x521f90),1)
            self.assertEqual(m.u32(0x498f68),19);self.assertEqual(m.u32(0x498f60),0xffffffff)

    def test_null_allocator_is_a_named_boundary_without_later_initialization(self):
        case=self.cases['init-0'];result=replay(case)
        self.assertIn('MessageBoxA',result['stop']);self.assertEqual(result['output'],case['input']['memory'])
        self.assertEqual([c['method'] for c in result['com']],['GlobalAlloc'])

    def test_active_pending_sequence_preserves_all_intermediate_memory(self):
        case=self.cases['active-pending-clear-relaunch'];result=replay(case)
        self.assertEqual(len(result['steps']),8)
        self.assertEqual([s['memory'] for s in result['steps']],[s['memory'] for s in case['steps']])
        occupied=QueueFixtureMemory.restore(result['steps'][4]['memory'])
        self.assertEqual(occupied.u32(0x498f68),20);self.assertEqual(occupied.u32(0x521f90),1)
        final=QueueFixtureMemory.restore(result['output'])
        self.assertEqual(final.u32(REFS+72*4),0xffffffff);self.assertEqual(final.u32(REFS+73*4),0xffffffff)

    def test_global_volume_uses_signed_clamp_and_ignores_update_hresult(self):
        for raw,expected in ((0,0),(128,128),(256,256),(257,256),(0xffffffff,0)):
            result=replay(self.cases[f'volume-active-{raw:x}']);m=QueueFixtureMemory.restore(result['output'])
            self.assertEqual(m.u32(0x498f58),expected);self.assertEqual(m.u32(0x498f5c),0)
            self.assertEqual(result['com'][-1]['hresult'],0x80004005)

    def test_missing_platform_and_invalid_scalar_never_invent_state(self):
        m=QueueFixtureMemory.restore(self.cases['init-7009000']['input']['memory']);before=m.snapshot()
        with self.assertRaises(DependenciaSom):AudioQueue(m,None).init_dictator()
        with self.assertRaises(ValueError):AudioQueue(m,None).set_game_volume(-1)
        self.assertEqual(m.snapshot(),before)
