"""S1 sound origin, argument order, wrapper and compatibility regressions."""
import os
import hashlib
import json
import unittest

from validar_som_luta_s1_combate import (CAPTURE, HERE, load, compare, state_before,
                                       expected_requests, request, memory, factory)

CAPTURES = (CAPTURE, HERE/'evidencias/som-morte-s1-original-v2.json.xz')


class FightSoundSites(unittest.TestCase):
    def test_real_frame11753_registers_volume_and_original_call(self):
        data=load()
        self.assertFalse(data['translation_executed'])
        self.assertTrue(data['s1']['code_unchanged'])
        self.assertEqual(data['s1']['frames_checked'],251)
        event=next(e for e in data['requests'] if e['frame']==11753 and e['call']=='0x4525a1')
        self.assertEqual(event['return_address'],'0x4525a6')
        expected=dict(EAX=0x50,EDX=0x2300,EBX=0x474a9358,ECX=0,ESI=0x474a9254,
                      EDI=17,EBP=17,ESP=0x2007dbc)
        self.assertEqual({k:int(v,16) for k,v in event['registers'].items()},expected)
        self.assertEqual(event['stack_words'],[90])

    def test_parent_memory_and_ordered_sound_requests(self):
        for path in CAPTURES:
            with self.subTest(path=path.name):
                report=compare(path)
                self.assertGreater(report['summary']['cases'],0)
                self.assertEqual(report['summary']['mismatches'],0,report)

    def test_owned_native_report_bindings(self):
        for name in ('som-luta-s1-native-v1.json','som-morte-s1-native-v1.json'):
            report=json.loads((HERE/'validacao'/name).read_bytes())
            self.assertTrue(report['native'])
            self.assertEqual(report['summary']['mismatches'],0)
            for owned,digest in report['source_sha256'].items():
                self.assertEqual(hashlib.sha256((HERE/owned).read_bytes()).hexdigest(),digest)

    def test_structure_and_owner_voice_sites_are_captured(self):
        cases=load(CAPTURES[1])['cases']
        self.assertTrue(any(c['routine']=='BatimentInfligeDegat' for c in cases))
        sites={e['call'] for c in cases for e in c['sound_requests']}
        self.assertTrue({'0x41a331','0x41a1d3','0x41a221'}<=sites)

    def test_legacy_and_keyword_callbacks_and_exception_propagation(self):
        case=next(c for c in load()['cases'] if c['routine']=='CalculAttaqueEngin' and c['frame']==11753)
        wanted=expected_requests(case)
        for wrapper, keyword in ((False,False),(False,True),(True,False),(True,True)):
            m,_=memory(state_before(case)); calls=[]
            def legacy(name,regs,words):
                event=request(name,regs,words,0)
                event.pop('call')  # Legacy callbacks receive no origin metadata.
                calls.append(event);return regs['EAX']
            def kw(name,regs,words,**kwargs):
                calls.append(request(name,regs,words,kwargs['chamada']));return regs['EAX']
            live=factory(m)
            callback=kw if keyword else legacy
            if wrapper: live.som=callback
            else: live.combate.som=callback
            with self.subTest(wrapper=wrapper,keyword=keyword):
                live.combate.calcular_ataque(int(case['entry_registers']['EAX'],16))
                expected=wanted if keyword else [{k:v for k,v in e.items() if k!='call'} for e in wanted]
                self.assertEqual(calls,expected)
        m,_=memory(state_before(case));live=factory(m);calls=[]
        def failed(name,regs,words,*,chamada):
            calls.append(chamada)
            raise TypeError('provider body failure')
        live.som=failed
        m.u8(0x474a9254+0xf9,0xa5)
        with self.assertRaisesRegex(TypeError,'provider body failure'):
            live.combate.calcular_ataque(int(case['entry_registers']['EAX'],16))
        self.assertEqual(calls,[0x4525a1])
        self.assertEqual(m.u8(0x474a9254+0xf9),0)  # earlier store retained


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','RISING_EMULAR=1 runs fresh S1 fight/death parents')
class FightSoundSitesNative(unittest.TestCase):
    def test_original_parent_differential(self):
        for path in CAPTURES:
            with self.subTest(path=path.name):
                report=compare(path,native=True)
                self.assertEqual(report['summary']['mismatches'],0,report)


if __name__=='__main__': unittest.main()
