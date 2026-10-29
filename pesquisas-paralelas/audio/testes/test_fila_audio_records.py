"""Queue record/COM provider replay against original-only v9 captures."""
import copy
import json
from pathlib import Path
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from audio_queue_fixtures import QueueFixtureMemory,ScriptedCOM,TABLE,INDEX,REFS
from fila_audio import AudioQueue
from bancos_som import DependenciaSom
from reproduzir_fila_audio import compare,replay


def capture():return json.loads((OWNED/'evidencias/captura-fila-audio-original-v9.json').read_text())


class AudioQueueRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.original=capture();cls.cases={c['name']:c for c in cls.original['cases']}

    def test_all_native_record_com_and_partial_effect_cases(self):
        self.assertFalse(self.original['translation_executed'])
        self.assertEqual((self.original['native_calls'],self.original['scenario_count']),(244,238))
        for case in self.original['cases']:
            with self.subTest(case=case['name']):
                errors,_=compare(case);self.assertEqual(errors,[])

    def test_persistent_post_sequence_checks_every_intermediate_image(self):
        case=self.cases['post-natural-sequence'];errors,result=compare(case)
        self.assertEqual(errors,[]);self.assertEqual(len(result['steps']),7)
        self.assertEqual(result['steps'],case['steps'])

    def test_index_70_alias_is_preserved_not_clamped(self):
        result=replay(self.cases['post-41-12340002-69']);memory=QueueFixtureMemory.restore(result['output'])
        self.assertEqual(memory.u32(INDEX),70)
        self.assertEqual(memory.u32(REFS+72*4),70)
        self.assertEqual(memory.u32(TABLE+70*44),1) # Last request ID aliases the dirty-global store.

    def test_pending_manage_stops_after_seek_and_physical_reservation(self):
        result=replay(self.cases['manage-pending-provider']);memory=QueueFixtureMemory.restore(result['output'])
        self.assertIn('CreateSoundBuffer',result['stop'])
        self.assertEqual(memory.u32(0x498f60),0)
        self.assertEqual([c['method'] for c in result['com']],['_llseek'])

    def test_constructor_keeps_inherited_memory_and_does_not_initialize(self):
        case=self.cases['manage-empty'];memory=QueueFixtureMemory.restore(case['input']['memory'])
        before=memory.snapshot();q=AudioQueue(memory,None)
        self.assertIs(q.memory,memory);self.assertEqual(memory.snapshot(),before)

    def test_null_status_guards_need_no_fabricated_backend(self):
        q=AudioQueue(None,None)
        self.assertEqual(q.status(0,'playing'),0);self.assertEqual(q.status(0,'looped'),0)
        self.assertEqual(q.status(0,'stopped'),1);self.assertEqual(q.stop_buffer(0),1)
        with self.assertRaises(DependenciaSom):q.status(0x1234,'playing')

    def test_unknown_status_write_is_a_stop_not_zero(self):
        plan=ScriptedCOM([dict(method='GetStatus',object=0x1234,args=[],hresult=0x80004005)])
        q=AudioQueue(None,plan)
        with self.assertRaisesRegex(DependenciaSom,'explicitly write'):q.status(0x1234,'stopped')

    def test_unknown_index_stops_before_compaction_write(self):
        memory=QueueFixtureMemory.restore(self.cases['manage-empty']['input']['memory'])
        before=memory.snapshot();q=AudioQueue(memory,None)
        with self.assertRaises(DependenciaSom):q.compact(TABLE+3,True)
        self.assertEqual(memory.snapshot(),before)

    def test_hresult_does_not_substitute_for_written_status(self):
        cases=[c for c in self.original['cases'] if c['name'].startswith('is_stopped-1-')]
        self.assertEqual(len(cases),2)
        self.assertTrue(all(replay(c)['value']==0 for c in cases))

    def test_active_manage_ignores_volume_hresult_but_keeps_stores(self):
        cases=[self.cases['manage-active-1-0'],self.cases['manage-active-1-80004005']]
        results=[replay(c) for c in cases]
        self.assertEqual(results[0]['output'],results[1]['output'])
        self.assertEqual([c['method'] for c in results[1]['com']],['GetStatus','SetVolume'])

    def test_creation_output_is_used_even_on_error_hresult(self):
        null=replay(self.cases['manage-create-0-80004005'])
        self.assertIsNone(null['stop']);self.assertEqual(null['value'],0)
        nonnull=replay(self.cases['manage-create-7101000-80004005'])
        self.assertIn('Lock',nonnull['stop']);self.assertEqual(len(nonnull['com']),3)

    def test_pcm_success_and_short_reads_keep_original_memory(self):
        for name,size in (('pcm-good',64),('short-read',32),('empty-read',0)):
            case=self.cases['manage-'+name];result=replay(case)
            before=QueueFixtureMemory.restore(case['input']['memory']);after=QueueFixtureMemory.restore(result['output'])
            self.assertEqual(after.read(0x7004000,size),bytes((i*7+3)&255 for i in range(size)))
            self.assertEqual(after.read(0x7004000+size,64-size),before.read(0x7004000+size,64-size))
            self.assertEqual(after.u32(INDEX),19);self.assertEqual(after.u8(TABLE+8),1)
            self.assertEqual([c['method'] for c in result['com']],['_llseek','CreateSoundBuffer','_llseek','Lock','_hread','Unlock','GetStatus','SetPosition','SetVolume','Play'])

    def test_start_failure_still_transfers_request_as_original_does(self):
        for name in ('position-error','volume-error','play-error'):
            result=replay(self.cases['manage-'+name]);memory=QueueFixtureMemory.restore(result['output'])
            self.assertEqual(result['value'],0);self.assertEqual(memory.u8(TABLE+8),1)
            self.assertEqual(memory.u32(INDEX),19);self.assertIsNone(result['stop'])

    def test_multiple_pending_requests_are_a_named_boundary(self):
        memory=QueueFixtureMemory.restore(self.cases['manage-empty']['input']['memory']);memory.w32(INDEX,21)
        with self.assertRaisesRegex(DependenciaSom,'Multiple pending'):AudioQueue(memory,None).manage()

    def test_external_hresult_requires_an_explicit_u32(self):
        plan=ScriptedCOM([dict(method='GetStatus',object=0x1234,args=[],hresult=0x100000000,value=0)])
        with self.assertRaisesRegex(ValueError,'u32'):AudioQueue(None,plan).status(0x1234,'stopped')
