"""Recruitment ABI, live bonus/failure semantics and committed native proof."""
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from entrada_estruturas import ArgumentoNaoPassado
from memoria_quadro_core import MemoriaQuadro
from recrutamento_core import (RecrutamentoCore, provedor_recrutamento, bonus_recrutamento,
                                ARGUMENTOS, REG7, DependenciaRecrutamentoCore)


def memoria():
    m = MemoriaQuadro([(0x490000, bytearray(0xa0000)), (0x1000000, bytearray(220800))])
    m.u32(0x4e19a0, 0x1000000)
    m.u16(0x496304, 0xffff)
    m.u8(0x1000002, 14)
    return m


class ProtocoloRecrutamento(unittest.TestCase):
    def test_every_missing_behaviour_register_fails_before_memory_access(self):
        class Proibida:
            def __getattr__(self, k):
                raise AssertionError('memory accessed before argument check')
        p = provedor_recrutamento(RecrutamentoCore(Proibida()))
        for nome, exigidos in ARGUMENTOS.items():
            for reg in exigidos:
                r = {k: 0 for k in exigidos if k != reg}
                with self.subTest(routine=nome, register=reg):
                    with self.assertRaises(ArgumentoNaoPassado) as e:
                        p(nome, 0x420f69, r)
                    self.assertIn(reg, e.exception.registradores)

    def test_missing_preserved_registers_remain_explicitly_unknown(self):
        m = memoria()
        p = provedor_recrutamento(RecrutamentoCore(m))
        out = p('EnginResetFatigue', 0x420f7c, {'EAX': 0})
        self.assertEqual(out['EAX'], 0x1000000)
        self.assertEqual(out['_incertos'], {k: 0xffffffff for k in REG7 if k != 'EAX'})
        # Fully determined EAX=0 remains known even when the omitted register entered as zero.
        out = p('EnginSetExperimente', 0x420f85, {'EAX': 0, 'EDX': 257})
        self.assertEqual(out['EAX'], 0)
        self.assertNotIn('EAX', out['_incertos'])

    def test_unknown_behaviour_bits_and_pushed_words_are_rejected(self):
        p = provedor_recrutamento(RecrutamentoCore(memoria()))
        with self.assertRaises(ArgumentoNaoPassado):
            p('EnginResetFatigue', 0x420f7c, dict(EAX=0, _incertos={'EAX': 1}))
        with self.assertRaises(ValueError):
            p('EnginResetFatigue', 0x420f7c, dict(EAX=0, _pilha=[1]))

    def test_bonus_reads_the_live_table_on_each_query(self):
        m = memoria()
        b = bonus_recrutamento(m)
        a = 0x4dfba0 + 18*7 + 11
        m.u8(a, 3)
        self.assertEqual(b(0, 7, 1), 3)
        m.u8(a, 9)
        self.assertEqual(b(0, 7, 1), 9)

    def test_missing_bonus_is_named_and_callback_failure_retains_earlier_stores(self):
        m = memoria()
        r = dict.fromkeys(REG7, 0)
        r.update(EDX=0x1234, EBX=4, ECX=4)
        with self.assertRaises(DependenciaRecrutamentoCore):
            RecrutamentoCore(m).chamar('EnginSetType', r)
        self.assertEqual(m.u16(0x1000008), 0)
        def bonus(*args):
            self.assertEqual(m.u16(0x1000008), 0x1234)
            self.assertEqual(m.u8(0x1000001), 4)
            raise RuntimeError('owner stopped')
        with self.assertRaisesRegex(RuntimeError, 'owner stopped'):
            RecrutamentoCore(m, bonus=bonus).chamar('EnginSetType', r)
        self.assertEqual(m.u16(0x1000008), 0x1234)

    def test_direct_calls_require_every_register(self):
        t = RecrutamentoCore(memoria())
        for nome in ARGUMENTOS:
            for missing in REG7:
                with self.subTest(routine=nome, register=missing):
                    with self.assertRaises(ArgumentoNaoPassado):
                        t.chamar(nome, {k: 0 for k in REG7 if k != missing})

    def test_experience_failure_retains_af_and_does_not_shift_queue(self):
        m = memoria()
        m.u8(0x1000001, 7)
        m.vista(0x4e19c4, 10)[:] = bytes((7, 0x23, 1, 0x43, 2, 0x63, 3, 0x83, 4, 0xa3))
        before = m.ler(0x4e19c4, 10)
        u16 = m.u16
        def read(a, v=None):
            if a == 0x4965ae + 50*7 + 0x2e:
                raise LookupError('missing live characteristic')
            return u16(a, v)
        with mock.patch.object(m, 'u16', side_effect=read):
            with self.assertRaisesRegex(LookupError, 'missing live'):
                RecrutamentoCore(m).chamar('EnginSetExperimente', dict.fromkeys(REG7, 0))
        self.assertEqual(m.u8(0x10000af), 0x23)
        self.assertEqual(m.ler(0x4e19c4, 10), before)

    def test_placement_radius_stop_retains_record_and_collision_prefix(self):
        m = memoria()
        m.u16(0x497168, 32)
        m.u16(0x49716a, 32)
        m.u16(0x496304, 0)
        m.u16(0x496fe0, 128)
        m.u16(0x496fe2, 128)
        m.u8(0x10000bb, 12)
        r = dict.fromkeys(REG7, 0)
        r['EDX'] = 257
        with mock.patch('recrutamento_core.definir_colisao_unidade') as collision:
            with self.assertRaises(DependenciaRecrutamentoCore) as e:
                RecrutamentoCore(m).chamar('SetSortEngin', r)
        self.assertEqual(e.exception.endereco, 0x446146)
        collision.assert_called_once_with(m, 0, 257)
        self.assertEqual(m.u16(0x1000008), 257)
        self.assertEqual(m.u8(0x1000002), 7)
        self.assertEqual(m.u8(0x1000072), 1)
        self.assertEqual(m.u16(0x496304), 65535)

    def test_unknown_name_delegates_without_changing_arguments(self):
        calls = []
        p = provedor_recrutamento(RecrutamentoCore(memoria()), outros=lambda *a: calls.append(a) or {'EAX': 7})
        r = {'EDX': 3}
        self.assertEqual(p('OtherOwner', 123, r), {'EAX': 7})
        self.assertIs(calls[0][2], r)


class EvidenciaRecrutamento(unittest.TestCase):
    def test_native_report_is_complete_and_bound_only_to_core_sources(self):
        cpath = RAIZ / 'evidencias/recrutamento-core/original.json.xz'
        cap = json.loads(lzma.decompress(cpath.read_bytes()))
        report = json.loads((RAIZ / 'relatorios/recrutamento-core-emulada.json').read_bytes())
        self.assertFalse(cap['translation_executed'])
        self.assertEqual(report['capture_sha256'], hashlib.sha256(cpath.read_bytes()).hexdigest())
        self.assertEqual(report['mismatches'], [])
        self.assertEqual(report['comparisons'], len(cap['cases']))
        self.assertEqual(report['capture_cases'], len(cap['cases']))
        self.assertEqual(report['s1']['frames_checked'], 48)
        self.assertTrue(report['s1']['code_unchanged'])
        self.assertEqual(set(report['by_routine']), set(ARGUMENTOS))
        for nome in ARGUMENTOS:
            cases = [c for c in cap['cases'] if c['routine'] == nome]
            self.assertEqual(sum(c['kind'] == 'economy_fixture' for c in cases), 3)
            self.assertEqual(sum(c['kind'] == 'in_situ' for c in cases), 1)
        for path, digest in report['source_sha256'].items():
            self.assertTrue(path.startswith('ferramentas/'))
            self.assertEqual(hashlib.sha256((RAIZ/path).read_bytes()).hexdigest(), digest,
                             'Rerun validar_recrutamento_core.py through heavy_lease.py')
