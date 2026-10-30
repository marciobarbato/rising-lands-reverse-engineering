"""Original fatal-fight matrix, strict register guards and real profile answers."""
import json
import os
from pathlib import Path
import unittest

from abi_luta_fatal_combate import REG7, DependenciaLutaFatal
from entrada_estruturas import ArgumentoNaoPassado
from memoria_quadro_core import MemoriaQuadro
from bancada_luta_fatal_combate import estado_contato
from validar_combate_raid import memory, serialize
from validar_luta_fatal_combate import CAPTURE, compare, factory

HERE=Path(__file__).resolve().parent
CIVIL=HERE/'evidencias/captura-civil-fatal-original-v1.json'
PHASE=HERE/'evidencias/captura-fase-contagem-fatal-original-v1.json'


class FatalFightMemory(unittest.TestCase):
    def test_complete_original_matrix_and_persistent_corpse_chains(self):
        report=compare()
        self.assertEqual(report['summary']['cases'],1088)
        self.assertEqual(report['summary']['mismatches'],0)
        self.assertEqual(report['summary']['outside_protected_domain'],1)
        corpses=[c for c in report['cases'] if c['routine']=='EnginNextEtape']
        self.assertEqual(len(corpses),990)
        self.assertTrue(all(c['python_chain'] for c in corpses))

    def test_civilian_refuge_and_late_count_phase(self):
        for path,count in ((CIVIL,16),(PHASE,82)):
            with self.subTest(path=path.name):
                report=compare(path)
                self.assertEqual(report['summary']['cases'],count)
                self.assertEqual(report['summary']['mismatches'],0)
        events=json.loads(PHASE.read_bytes())['events']
        for kind in (0,5):
            rows={e['case']:e for e in events}
            death=rows[f'late-death-type{kind}-t40'];following=rows[f'late-death-type{kind}-t41']
            self.assertEqual((death['state_after'],death['local_population'],death['type_count']),(4,16,3))
            self.assertEqual((following['state_after'],following['local_population'],following['type_count']),(4,15,2))

    def test_constructor_and_every_missing_register_leave_memory_intact(self):
        state,_=estado_contato();m,blocks=memory(state);before=serialize(blocks)
        live=factory(m)
        self.assertEqual(serialize(blocks),before)
        for name,call in live.provedores().items():
            for missing in REG7:
                with self.subTest(name=name,missing=missing):
                    regs={r:0 for r in REG7 if r!=missing}
                    with self.assertRaises(ArgumentoNaoPassado) as raised:call(regs)
                    self.assertEqual(raised.exception.registradores,(missing,))
        self.assertEqual(serialize(blocks),before)

    def test_required_stack_arguments_are_explicit(self):
        state,_=estado_contato();m,blocks=memory(state);live=factory(m);before=serialize(blocks)
        regs={r:0 for r in REG7}
        for name in ('InfligeDegat','KERNEL32.GetPrivateProfileStringA'):
            with self.subTest(name=name):
                with self.assertRaises(ArgumentoNaoPassado):live.provedores()[name](regs)
        self.assertEqual(serialize(blocks),before)

    def test_profile_import_full_registers_against_recorded_external_answer(self):
        capture=json.loads(CAPTURE.read_bytes())
        case=next(c for c in capture['cases'] if c['bindings'])
        event=case['bindings'][0]
        state,_=estado_contato();_,blocks=memory(state)
        scratch=bytearray(65536);base=0x2000000
        key=bytes.fromhex(case['profile_calls'][0][2]['bytes_hex'])
        key_pointer=event['arguments'][1]
        scratch[key_pointer-base:key_pointer-base+len(key)+1]=key+b'\0'
        m=MemoriaQuadro([(b,d) for b,d in blocks.values()]+[(base,scratch)])
        live=factory(m)
        regs={r:event['registers_before'][r] for r in REG7}
        out=live.chamar('KERNEL32.GetPrivateProfileStringA',regs,pilha=event['arguments'])
        expected=dict(regs,**event['results'])
        self.assertEqual(out,expected)
        answer=bytes.fromhex(case['profile_calls'][0][-1]['bytes_hex'])+b'\0'
        self.assertEqual(m.ler(event['arguments'][3],len(answer)),answer)

    def test_unknown_handler_and_raw_scope_stop_before_effects(self):
        state,_=estado_contato();m,blocks=memory(state);live=factory(m)
        regs=dict(zip(REG7,(16,0xffff,0x31415926,0x48,4,5,6)))
        before=serialize(blocks)
        with self.assertRaises(ValueError):live.chamar('iagUnitSendMessage',regs)
        self.assertEqual(serialize(blocks),before)
        table=m.u32(0x498e94+9*4);m.u32(table,0x12345678)
        before=serialize(blocks);regs['EBX']=0
        with self.assertRaises(DependenciaLutaFatal) as raised:live.chamar('iagUnitSendMessage',regs)
        self.assertEqual(raised.exception.endereco,0x12345678)
        self.assertEqual(serialize(blocks),before)
        victim=m.u32(0x4e19a0);m.u32(victim+0x104,0)
        before=serialize(blocks);regs.update(EAX=0,EDX=1,EBX=16,ECX=0)
        with self.assertRaises(DependenciaLutaFatal) as raised:live.chamar('EnginInfligeDegat',regs)
        self.assertEqual(raised.exception.endereco,0x4502f0)
        self.assertEqual(serialize(blocks),before)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','RISING_EMULAR=1 runs the original civil/count supplements')
class FatalFightNative(unittest.TestCase):
    def test_native_civilian_and_count_phase_supplements(self):
        for path,count in ((CIVIL,16),(PHASE,82)):
            with self.subTest(path=path.name):
                report=compare(path,native=True)
                self.assertEqual(report['summary']['cases'],count)
                self.assertEqual(report['summary']['mismatches'],0)


if __name__=='__main__':unittest.main()
