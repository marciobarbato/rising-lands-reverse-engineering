"""Original read-set replay, strict register boundaries and owner routing (no foreign file pins).

Owner stubs below test forwarding/exception order only; they are not substitute implementations or
validation of Economy's restore or Combat's refuge game bodies.
"""
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from consultas_estado_core import ConsultasEstadoCore, REG7, provedor_consultas_estado
from entrada_estruturas import ArgumentoNaoPassado
from memoria_quadro_core import MemoriaQuadro
from provedores_lacunas_core import provedor_lacunas_s1, DependenciaLacunaS1, ROTINAS, EXIGE_ESP
from validar_consultas_estado_core import CAPTURA, RELATORIO, FONTES, comparar


def captura():
    return json.loads(lzma.decompress(CAPTURA.read_bytes()))


class EvidenciaOriginal(unittest.TestCase):
    def test_original_only_all_states_types_and_pool_endpoints(self):
        d = captura()
        self.assertFalse(d['translation_executed'])
        self.assertEqual(d['capture_script_sha256'],
                         hashlib.sha256((RAIZ / 'ferramentas/validar_consultas_estado_core.py').read_bytes()).hexdigest())
        self.assertEqual(d['original_sha256'], '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
        self.assertEqual(d['by_routine'], {'EnginEstVivant': 268, 'BatimentGetDecalageConstruction': 278})
        self.assertEqual(Counter(c['routine'] for c in d['cases']), Counter(d['by_routine']))
        self.assertTrue(d['fixture']['code_unchanged'])
        self.assertEqual((d['fixture']['last_frame'], d['fixture']['frames_checked']), (11250, 1))
        vivos = [c for c in d['cases'] if c['routine'] == 'EnginEstVivant']
        self.assertEqual({int(c['entry_registers']['EAX'], 16) & 0xffff for c in vivos}, {0, 15, 799})
        self.assertEqual({int(c['writes'][0][1], 16) for c in vivos if
                          int(c['entry_registers']['EAX'], 16) & 0xffff == 15}, set(range(256)))
        tipos = [c for c in d['cases'] if c['routine'] == 'BatimentGetDecalageConstruction']
        self.assertEqual({int(c['entry_registers']['EAX'], 16) & 255 for c in tipos}, set(range(256)))
        self.assertTrue(all(not c['changed_bytes'] and not c['boundaries'] for c in d['cases']))
        self.assertTrue(all(c['entry_reads'] for c in vivos))

    def test_replay_every_native_read_set_direct_and_both_providers(self):
        for c in captura()['cases']:
            with self.subTest(routine=c['routine'], label=c['label']):
                r = comparar(c)
                self.assertTrue(r['ok'], r)

    def test_replay_detects_wrong_state_rule_table_and_preserved_register(self):
        casos = captura()['cases']
        vivo = next(c for c in casos if c['routine'] == 'EnginEstVivant')
        construcao = next(c for c in casos if c['routine'] == 'BatimentGetDecalageConstruction')
        with patch('selecao_ordens.SelecaoOrdens._vivo', lambda self, r: r.update(EAX=1)):
            self.assertFalse(comparar(vivo)['ok'])
        with patch('consultas_estado_core.DECALAGEM', (0,) * 22):
            self.assertFalse(comparar(construcao)['ok'])
        original = ConsultasEstadoCore.chamar

        def perder_edx(self, nome, regs, pilha=()):
            return dict(original(self, nome, regs, pilha), EDX=0)

        with patch.object(ConsultasEstadoCore, 'chamar', perder_edx):
            self.assertFalse(comparar(construcao)['ok'])

    def test_fresh_native_report_and_current_core_source_bindings(self):
        self.assertTrue(RELATORIO.exists(), 'run the leased native comparison before delivery')
        d = json.loads(RELATORIO.read_text())
        self.assertEqual(d['capture']['sha256'], hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        self.assertEqual((d['comparisons'], d['capture_cases']), (546, 546))
        self.assertEqual(d['mismatches'], [])
        self.assertTrue(d['fixture']['code_unchanged'])
        self.assertTrue(all(c['ok'] and c['native_equals_capture'] for c in d['cases']))
        self.assertEqual(set(d['source_sha256']), set(FONTES))
        self.assertTrue(all(p.startswith('ferramentas/') for p in d['source_sha256']))
        for p, sha in d['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / p).read_bytes()).hexdigest(), sha, p)


class ContratoProvedores(unittest.TestCase):
    def setUp(self):
        self.r = dict(zip(REG7, (15, 0x12345678, 0x87654321, 0xabcdef01, 0x13572468, 0x24681357, 0x76543210)))

    def test_all_known_calls_reject_each_missing_register_before_effects(self):
        p = provedor_lacunas_s1(MemoriaQuadro(()))
        for nome in ROTINAS:
            for k in REG7 + (('ESP',) if nome in EXIGE_ESP else ()):
                with self.subTest(routine=nome, missing=k):
                    r = dict(self.r, ESP=0x2007000)
                    del r[k]
                    with self.assertRaises(ArgumentoNaoPassado) as e:
                        p(nome, 0x123456, r)
                    self.assertEqual((e.exception.chamada, e.exception.registradores), (0x123456, (k,)))

    def test_state_provider_requires_preserved_registers_and_never_reads_invalid_index(self):
        t = ConsultasEstadoCore(MemoriaQuadro(()))
        p = provedor_consultas_estado(t)
        for k in REG7:
            r = dict(self.r)
            del r[k]
            with self.assertRaises(ArgumentoNaoPassado):
                p('EnginEstVivant', 0x4731d3, r)
        with self.assertRaises(ValueError):
            t.chamar('EnginEstVivant', dict(self.r, EAX=800))
        with self.assertRaises(ValueError):
            t.chamar('BatimentGetDecalageConstruction', self.r, (1,))
        with self.assertRaises(ValueError):
            p('BatimentGetDecalageConstruction', 0x44ad30, dict(self.r, _pilha=[1]))

    def test_owner_routing_forwards_every_register_and_actual_call_address(self):
        seen = []

        def owner(nome, chamada, regs):
            seen.append((nome, chamada, dict(regs)))
            return dict(regs, EAX=0x12345678)

        p = provedor_lacunas_s1(MemoriaQuadro(()), restauracao=owner, refugio=owner)
        for nome, sitio in (('EnginRestaureEtat', 0x45566a),
                            ('ChercheBatimentProximiteCaveOuSanctuaire', 0x450001)):
            r = dict(self.r, ESP=0x2007000)
            saida = p(nome, sitio, r)
            self.assertEqual(seen[-1], (nome, sitio, r))
            self.assertEqual(set(saida), set(REG7))
            self.assertEqual(saida, dict(self.r, EAX=0x12345678))

    def test_missing_owner_or_unknown_register_result_is_explicit(self):
        r = dict(self.r, ESP=0x2007000)
        p = provedor_lacunas_s1(MemoriaQuadro(()))
        for nome in ('EnginRestaureEtat', 'ChercheBatimentProximiteCaveOuSanctuaire'):
            with self.assertRaises(DependenciaLacunaS1):
                p(nome, 0x1234, r)
        for resultado in ({'EAX': 1}, dict(self.r, _incertos={'EDX': 1})):
            p = provedor_lacunas_s1(MemoriaQuadro(()), refugio=lambda n, a, r: resultado)
            with self.assertRaises(DependenciaLacunaS1):
                p('ChercheBatimentProximiteCaveOuSanctuaire', 0x1234, r)

    def test_callback_exception_retains_prior_store_and_never_retries(self):
        dados = bytearray(1)
        m = MemoriaQuadro(((0x1000, dados),))
        calls = []

        def falhar(nome, chamada, regs):
            calls.append(nome)
            m.u8(0x1000, 17)
            raise RuntimeError('owner failed after its store')

        p = provedor_lacunas_s1(m, restauracao=falhar)
        with self.assertRaisesRegex(RuntimeError, 'owner failed'):
            p('EnginRestaureEtat', 0x45566a, dict(self.r, ESP=0x2007000))
        self.assertEqual((calls, dados[0]), (['EnginRestaureEtat'], 17))

    def test_unknown_names_are_forwarded_without_filling_registers(self):
        seen = []
        p = provedor_lacunas_s1(MemoriaQuadro(()), outros=lambda n, a, r: seen.append((n, a, r)) or r)
        r = {'custom': 17}
        self.assertIs(p('OtherOwner', 0x123, r), r)
        self.assertIs(seen[0][2], r)
        with self.assertRaises(DependenciaLacunaS1):
            provedor_lacunas_s1(MemoriaQuadro(()))('OtherOwner', 0x123, r)


if __name__ == '__main__':
    unittest.main()
