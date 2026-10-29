"""Real-raid live-memory regression and optional fresh original-x86 differential."""
import hashlib
import json
import os
from pathlib import Path
import unittest

from bancada_combate_raid import checkpoints
from combate_raid_vivo import CombateRaidVivo, DependenciaCombateRaid
from delta_estado_missao import resumo
from validar_combate_raid import entry_states, execute, memory, serialize, compare

HERE=Path(__file__).resolve().parent
CAPTURE=HERE/'evidencias/captura-combate-raid-original-v2.json'
SELECTED=('f9000-scan-0','f9176-scan-16','f9000-order-0-1-16','f9176-order-16-3-0',
          'f9000-attack-0-1-16','f9176-attack-16-1-0','f9000-sanctuary-camera1-1',
          'f9176-sanctuary-camera1-65536','f9000-sanctuary-camera1-65535','f9176-sanctuary-camera1-4294967295','f9000-sanctuary-1','f9176-sanctuary-65535')


class RealRaidMemory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.states,cls.provenance=checkpoints()
        cls.capture=json.loads(CAPTURE.read_bytes())
        cls.selected={}
        cls.count=0
        for case,before,after in entry_states(cls.capture,cls.states):
            cls.count+=1
            if case['case'] in SELECTED:
                cls.selected[case['case']]=(case,before,after)

    def test_original_evidence_integrity(self):
        self.assertFalse(self.capture['translation_executed'])
        self.assertEqual(self.count,184)
        self.assertEqual(self.capture['provenance'],self.provenance)
        self.assertEqual(sum(c['reached_return'] for c in self.capture['cases']),164)
        self.assertTrue(all(not c['fault'] and not c['limit'] and not c['writes_outside_checkpoint']
                            for c in self.capture['cases']))
        self.assertEqual(len(self.selected),len(SELECTED))

    def test_constructor_preserves_all_inherited_bytes(self):
        state=self.states[9000][0]
        m,blocks=memory(state)
        live=CombateRaidVivo(m)
        self.assertEqual(resumo(serialize(blocks)),resumo(state))
        self.assertEqual(live.maquina.campo_4dfb44,m.u8(0x4dfb44))

    def test_original_returned_entries_over_whole_checkpoint(self):
        for label,(case,before,after) in self.selected.items():
            if case['stop']:
                continue
            with self.subTest(label):
                actual,regs,checked,dependency=execute(case,before,guarded=label in (
                    'f9000-sanctuary-camera1-65535','f9176-sanctuary-camera1-4294967295'))
                self.assertIsNone(dependency)
                self.assertEqual(resumo(actual),resumo(after))
                for reg in checked:
                    self.assertEqual(regs[reg],int(case['exit_registers'][reg],16),(label,reg))

    def test_local_sanctuary_sound_stops_after_accumulator_store(self):
        for label,(case,before,after) in self.selected.items():
            if case['stop']!='PlaySnd_PostSound':
                continue
            with self.subTest(label):
                actual,_,_,dependency=execute(case,before)
                self.assertEqual(dependency['name'],'PlaySnd_PostSound')
                self.assertEqual(dependency['address'],0x48aa79)
                self.assertEqual(resumo(actual),resumo(after))
                self.assertEqual(dependency['arguments'][-1],0x49a1c8)

    def test_core_three_argument_order_callback(self):
        case,before,after=self.selected['f9000-order-0-1-16']
        m,blocks=memory(before);live=CombateRaidVivo(m)
        result=live.ordem_core(0,1,16)
        self.assertEqual(result,{k:int(case['exit_registers'][k],16) for k in ('EAX','EDX')})
        self.assertEqual(resumo(serialize(blocks)),resumo(after))

    def test_core_lifecycle_is_a_named_provider(self):
        m,blocks=memory(self.states[9176][0]);live=CombateRaidVivo(m)
        before=resumo(serialize(blocks))
        for function,address in ((live.iniciar_morte,0x444938),(live.retirar,0x457058)):
            with self.subTest(address=hex(address)):
                with self.assertRaises(DependenciaCombateRaid) as stopped:
                    function(16)
                self.assertEqual(stopped.exception.endereco,address)
                self.assertEqual(stopped.exception.argumentos,(16,))
                self.assertEqual(resumo(serialize(blocks)),before)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','RISING_EMULAR=1 runs the real-raid original leaves')
class RealRaidNative(unittest.TestCase):
    def test_full_checkpoint_and_consumed_register_differential(self):
        report=compare(CAPTURE,native=True)
        self.assertEqual(report['summary']['cases'],174)
        self.assertEqual(report['summary']['mismatches'],0)
        self.assertEqual(report['summary']['dependency_not_compared'],0)
        self.assertTrue(all(c.get('dependency_arguments_equal',True) for c in report['cases']))

    def test_solid_footprint_with_original_read_only_guards_and_audio(self):
        report=compare(HERE/'evidencias/captura-batiment-raid-original-v4-som.json',native=True,audio=True,guarded=True)
        self.assertEqual(report['summary']['cases'],36)
        self.assertEqual(report['summary']['mismatches'],0)
        self.assertEqual(report['summary']['dependency_not_compared'],0)
        self.assertTrue(all(c.get('dependency_arguments_equal',True) for c in report['cases']))


if __name__=='__main__':unittest.main()
