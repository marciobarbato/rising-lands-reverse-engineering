"""Original-capture differentials and stream corruption checks for M3 Audio."""
import copy
import json
import os
from pathlib import Path
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1];sys.path.insert(0,str(OWNED))
from audio_queue_fixtures import QueueFixtureMemory, decode
from bancos_som import DependenciaSom
from fluxo_pedidos_audio import AudioRequestStream, from_boundaries, compare_streams, validate
from provedor_pedidos_m3_audio import SoundRequestProvider, LiveAudioMemory
from validar_pedidos_m3_audio import provider_replay


def display_fixture():
    return json.loads((OWNED/'evidencias/m3-pedidos-original-v1.json').read_bytes())['cases'][0]['input']


class M3SoundProviderTests(unittest.TestCase):
    def test_display_and_initialized_native_EAX_and_all_memory(self):
        result=provider_replay()
        self.assertEqual(result['display_calls'],58)
        self.assertEqual(result['initialized_calls'],111)
        self.assertEqual(result['initialized_scenarios'],99)
        self.assertEqual(result['failures'],[])

    def test_live_core_memory_and_manager_dirty_word(self):
        f=display_fixture();m=QueueFixtureMemory.restore(f['memory'])
        class CoreMemory:
            def u8(self,a,v=None): return m.u8(a) if v is None else m.w8(a,v)
            def u16(self,a,v=None): return m.u16(a) if v is None else m.w16(a,v)
            def u32(self,a,v=None): return m.u32(a) if v is None else m.w32(a,v)
            def vista(self,a,n): return m.view(a,n)
        provider=SoundRequestProvider(LiveAudioMemory(CoreMemory()),domain='unopened-display')
        self.assertEqual(m.u32(0x498f5c),1)
        self.assertEqual(provider('PlaySnd_Manage',{},[]),1)
        self.assertEqual(m.u32(0x498f5c),0)
        self.assertEqual(provider('PlaySnd_PostSound',f['regs'],f['arguments']),0)
        self.assertEqual(m.u32(f['regs']['EBX']),0xffffffff)
        self.assertEqual(m.u32(0x498f68),19)

    def test_unknown_private_state_and_busy_handle_raise(self):
        f=display_fixture()
        for mutation in (lambda m:m.w8(0x521fc4,1),lambda m:m.w32(0x498f68,20),
                         lambda m:m.w32(f['regs']['EBX'],20)):
            m=QueueFixtureMemory.restore(f['memory']);p=SoundRequestProvider(m,domain='unopened-display')
            mutation(m)
            with self.assertRaises(DependenciaSom):p('PlaySnd_PostSound',f['regs'],f['arguments'])

    def test_initialized_requires_exact_request_and_preserves_physical_logical_state(self):
        artifact='captura-continuacao-audio-original-v3.json'
        doc=json.loads((OWNED/'evidencias'/artifact).read_bytes())
        case=next(c for c in doc['cases'] if c['name']=='post-manage-promotion-repost-cancel-sequence')
        f=case['input'];m=QueueFixtureMemory.restore(f['memory'])
        p=SoundRequestProvider(m,domain='captured-initialized',capture=(artifact,case['name']))
        request=f['sequence'][0]
        regs=dict(request['regs'],EDX=request['regs']['EDX']+1)
        with self.assertRaises(DependenciaSom):p('PlaySnd_PostSound',regs,request['arguments'])
        self.assertEqual(m.snapshot(),f['memory'])
        names={'post':'PlaySnd_PostSound','manage':'PlaySnd_Manage','stop_handle':'PlaySnd_StopSound'}
        for i,r in enumerate(f['sequence'][:7]):
            self.assertEqual(p(names[r['operation']],r['regs'],r['arguments']),int(case['steps'][i]['eax'],16))
            self.assertEqual(m.snapshot(),case['steps'][i]['memory'])

    def test_failed_request_is_logged_before_domain_stop(self):
        f=display_fixture();m=QueueFixtureMemory.restore(f['memory']);stream=AudioRequestStream()
        p=SoundRequestProvider(m,domain='unopened-display',stream=stream)
        p.phase,p.caller_return='frame129',0x440dfc
        m.w8(0x521fc4,1)
        with self.assertRaises(DependenciaSom):p('PlaySnd_PostSound',f['regs'],f['arguments'])
        self.assertEqual(len(stream.events),1)
        self.assertEqual(stream.events[0]['stack_words'],f['arguments'])


class M3SoundStreamTests(unittest.TestCase):
    def stream(self):
        stream=AudioRequestStream()
        stream.append('frame129',0x440dfc,'PlaySnd_PostSound',dict(EAX=0x50,EDX=0x70800,EBX=0x474a8000,ECX=0x101),[256])
        stream.append('between_frames130',0x460220,'PlaySnd_Manage',{},[])
        stream.append('frame130',0x47436b,'PlaySnd_StopSound',dict(EAX=0x474a8000),[])
        return stream.document()

    def test_exact_stream_and_each_corruption(self):
        expected=self.stream();self.assertTrue(compare_streams(expected,copy.deepcopy(expected))['equal'])
        for field in ('caller_return','phase','frame','routine','registers','stack_words'):
            actual=copy.deepcopy(expected)
            if field=='caller_return':actual['events'][0][field]+=1
            elif field=='phase':
                actual['events'][0][field]='frame131';actual['events'][0]['frame']=131
            elif field=='frame':
                actual['events'][0][field]=131;actual['events'][0]['phase']='frame131'
            elif field=='routine':
                actual['events'][0][field]='PlaySnd_Manage';actual['events'][0]['registers']={};actual['events'][0]['stack_words']=[]
            elif field=='registers':actual['events'][0][field]['ECX']^=0x100
            else:actual['events'][0][field][0]-=1
            self.assertFalse(compare_streams(expected,actual)['equal'],field)
        for events in (expected['events'][:-1],expected['events']+[dict(expected['events'][-1],sequence=3)]):
            self.assertFalse(compare_streams(expected,dict(schema=expected['schema'],events=events))['equal'])
        swapped=copy.deepcopy(expected)
        swapped['events'][0],swapped['events'][1]=swapped['events'][1],swapped['events'][0]
        for i,e in enumerate(swapped['events']):e['sequence']=i
        self.assertFalse(compare_streams(expected,swapped)['equal'])

    def test_invalid_schema_and_unsigned_width_raise(self):
        for value in (-1,0x100000000,True):
            s=AudioRequestStream()
            with self.assertRaises(ValueError):s.append('frame1',value,'PlaySnd_Manage',{},[])
        s=self.stream();s['events'][1]['sequence']=True
        with self.assertRaises(ValueError):validate(s)

    def test_unused_manager_registers_and_stack_are_not_arguments(self):
        phases=[dict(phase='between_frames',boundaries=[dict(routine='PlaySnd_Manage',caller_return='0x460220',
                  registers=dict(EAX='0xdeadbeef'),stack_words=['0xcdcdcdcd']*4)])]
        event=from_boundaries(phases)['events'][0]
        self.assertEqual((event['registers'],event['stack_words']),({},[]))

    def test_committed_window_counts_and_source_bindings(self):
        report=json.loads((OWNED/'validacao/m3-pedidos-replay-v4.json').read_bytes())
        windows=report['windows']
        self.assertEqual(windows['m22']['comparison']['expected_events'],128)
        self.assertEqual(windows['m23_events'],9200)
        self.assertEqual(windows['raid_window']['comparison']['expected_events'],210)
        self.assertTrue(windows['m22_prefix_comparison']['equal'])
        self.assertTrue(all(c['equal'] for c in windows['committed_stream_comparisons']))
        self.assertTrue(all(p['comparison']['equal'] for p in [windows['m22']]+windows['m23_parts']))
        import hashlib
        for name,sha in report['source_sha256'].items():
            self.assertEqual(hashlib.sha256((OWNED/name).read_bytes()).hexdigest(),sha,name)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class M3SoundNativeTests(unittest.TestCase):
    def test_fresh_58_original_calls_equal_frozen_capture(self):
        from capturar_pedidos_m3_audio import leaves
        original=json.loads((OWNED/'evidencias/m3-pedidos-original-v1.json').read_bytes())
        original.pop('seconds')
        self.assertEqual(leaves(),original)
