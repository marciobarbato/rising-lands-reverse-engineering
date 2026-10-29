"""Selection and order-setter translations without a CPU, over the original-first capture.

- The capture and the exported bodies are intact original evidence.
- The committed native differential (130 cases, whole touched state) is bound to the current
  sources: editing the translation or the harness requires rerunning it.
- Every captured case whose path stays outside Core's navigation world (ResetOrdre,
  SetDeplaceEngin) and Combat's SetAttaqueEngin replays exactly from the bytes the original
  read before writing: registers EAX..EBP, every changed byte and the sound requests.
- Named dependencies raise instead of defaulting.
"""
import hashlib
import json
from pathlib import Path
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
sys.path.insert(0, str(RAIZ / 'testes'))
PASTA = RAIZ / 'evidencias/selecao-ordens'
CAPTURA = PASTA / 'captura-selecao-ordens-exibicao.json'
LEITURAS = PASTA / 'leituras-selecao-ordens-exibicao.json'
RELATORIO = RAIZ / 'relatorios/selecao-ordens-emulada.json'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
# Paths through Core's live navigation world or Combat's provider are compared only natively.
NATIVAS = {'ResetOrdre', 'SetDeplaceEngin', 'SetAttaqueEngin'}


def capturados():
    return json.loads(CAPTURA.read_bytes())['cases']


def memoria_replay(caso, leituras):
    from test_chamadas_quadro_core import MemoriaEsparsa
    conhecidos = {}
    for inicio, valores in leituras[caso['case']]:
        a = int(inicio, 16)
        for i in range(len(valores) // 2):
            conhecidos[a + i] = int(valores[2 * i:2 * i + 2], 16)
    return MemoriaEsparsa(conhecidos)


def nativa(caso):
    return caso['routine'] in NATIVAS or any(c.split('|')[1] in NATIVAS for c in caso['calls'])


class EvidenciaOriginal(unittest.TestCase):
    def test_capture_is_original_only_and_reproduces_the_accepted_path(self):
        d = json.loads(CAPTURA.read_bytes())
        self.assertFalse(d['translation_executed'])
        self.assertTrue(all(d['path_reproduction'].values()), d['path_reproduction'])
        self.assertEqual(d['pause']['routine'], 'ProcessInputGame')
        self.assertEqual(len(d['cases']), 130)
        self.assertTrue(all(c['reached_return'] for c in d['cases']))
        self.assertEqual(len({c['case'] for c in d['cases']}), len(d['cases']))

    def test_exported_bodies_match_the_intact_executable(self):
        import struct
        exe = RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE'
        if not exe.exists():
            self.skipTest('original executable not present')
        raw = exe.read_bytes()
        manifesto = json.loads((PASTA / 'manifesto.json').read_text())
        self.assertEqual(hashlib.sha256(raw).hexdigest(), manifesto['original_sha256'])
        pe = struct.unpack_from('<I', raw, 60)[0]
        n, op = (struct.unpack_from('<H', raw, pe + o)[0] for o in (6, 20))
        secoes = [struct.unpack_from('<III', raw, pe + 24 + op + i * 40 + 12) for i in range(n)]

        def ler(va, k):
            rva = va - 0x400000
            for base, t, o in secoes:
                if o and base <= rva < base + t:
                    return raw[o + rva - base:o + rva - base + k]
        for t in manifesto['intervals']:
            a, z = int(t['start'], 16), int(t['end_exclusive'], 16)
            self.assertEqual(hashlib.sha256(ler(a, z - a)).hexdigest(), t['sha256'], t['name'])

    def test_translation_constants_are_the_original_jump_tables(self):
        from selecao_ordens import DECALAGEM, QUATRO_CELULAS
        tabelas = {t['name']: [int(x, 16) for x in t['entries']]
                   for t in json.loads((PASTA / 'manifesto.json').read_text())['jump_tables']}
        valores = {0x41aeb5: 0x201, 0x41aebb: 0x101, 0x41aec1: 0x202, 0x41aec7: 0x300, 0x41aecd: 0x100,
                   0x41aed3: 0x200, 0x41aed9: 1, 0x41aedf: 0}   # the MOV EAX targets of 0x41aea4
        self.assertEqual(tuple(valores[a] for a in tabelas['BatimentGetDecalageConstruction by structure type']),
                         DECALAGEM)
        self.assertEqual({t for t, a in enumerate(tabelas['EnginInZone by unit type']) if a == 0x4462b0},
                         set(QUATRO_CELULAS))


class DiferencialNativoComprometido(unittest.TestCase):
    def test_report_has_no_mismatch_and_is_bound_to_the_current_sources(self):
        r = json.loads(RELATORIO.read_bytes())
        self.assertEqual(r['mismatches'], [])
        self.assertEqual(r['comparisons'], len(capturados()))
        self.assertTrue(all(r['path_reproduction'].values()))
        self.assertEqual(r['capture']['sha256'], hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        for caminho, h in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), h,
                             f'{caminho} changed since the native differential: rerun validar_selecao_ordens.py')


class ReplaySemCPU(unittest.TestCase):
    def test_every_case_outside_the_native_only_paths_replays_exactly(self):
        from selecao_ordens import SelecaoOrdens
        leituras = json.loads(LEITURAS.read_bytes())['cases']
        replayed = 0
        for caso in capturados():
            if nativa(caso):
                continue
            with self.subTest(case=caso['case']):
                m = memoria_replay(caso, leituras)
                pedidos = []

                def som(nome, regs, pilha):
                    pedidos.append(dict(routine=nome, registers={k: hex(v) for k, v in regs.items()},
                                        stack=[hex(v) for v in pilha]))
                    return regs['EAX']
                entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
                pilha = [int(x, 16) for x in caso['stack_words']]
                saida = SelecaoOrdens(m, som=som).chamar(caso['routine'], entrada, pilha)
                self.assertEqual({k: hex(saida[k]) for k in REGISTROS},
                                 {k: caso['exit_registers'][k] for k in REGISTROS})
                m.conferir(self, caso['changed_bytes'])
                self.assertEqual(pedidos, [dict(routine=b['routine'], registers=b['registers'],
                                                stack=b['stack_words'][:1] if b['routine'] == 'PlaySnd_PostSound'
                                                else []) for b in caso['boundaries']])
                replayed += 1
        self.assertGreaterEqual(replayed, 80)


class DependenciasNomeadas(unittest.TestCase):
    def caso(self, nome):
        return next(c for c in capturados() if c['case'] == nome)

    def executar(self, nome, **provedores):
        from selecao_ordens import SelecaoOrdens
        c = self.caso(nome)
        m = memoria_replay(c, json.loads(LEITURAS.read_bytes())['cases'])
        entrada = {k: int(c['entry_registers'][k], 16) for k in REGISTROS}
        return m, c, SelecaoOrdens(m, **provedores).chamar(c['routine'], entrada, [int(x, 16) for x in c['stack_words']])

    def test_sound_requests_without_the_audio_provider_raise_after_the_prior_stores(self):
        from chamadas_quadro_core import DependenciaRamoCore
        for nome, endereco in (('box_u12', 0x440de7), ('struct_sanctuary', 0x41b785),
                               ('box_builder_state11', 0x474582), ('ask_u12_mode16_full_volume', 0x440de7)):
            with self.subTest(case=nome), self.assertRaises(DependenciaRamoCore) as erro:
                self.executar(nome)
            self.assertEqual(erro.exception.endereco, endereco)

    def test_paths_without_a_sound_request_need_no_provider(self):
        for nome in ('box_u12_handle_busy', 'box_u12_undiscovered', 'struct_sound_busy', 'add_u12_p0'):
            with self.subTest(case=nome):
                self.executar(nome)

    def test_attack_orders_require_combats_provider(self):
        from chamadas_quadro_core import DependenciaRamoCore
        from memoria_quadro_core import MemoriaQuadro
        from selecao_ordens import SelecaoOrdens
        dgroup, pool = bytearray(0x8f000), bytearray(800 * 276)
        m = MemoriaQuadro([(0x494000, dgroup), (0x10000000, pool)])
        m.u32(0x4e19a0, 0x10000000)
        m.u16(0x508728, 1)
        m.u16(0x50872a, 0)
        pool[2] = 7
        t = SelecaoOrdens(m, som=lambda n, r, p: r['EAX'])
        with self.assertRaises(DependenciaRamoCore) as erro:
            t.chamar('SetAttaqueEnginSelect', dict(EAX=0, EBX=12, ECX=0, EDX=1, ESI=0, EDI=0, EBP=0))
        self.assertEqual(erro.exception.endereco, 0x473e39)
        self.assertEqual(m.u32(0x10000000 + 0x110), m.u32(0x508f7c))   # +0x110 is stored before the call

    def test_bag_count_outside_mode_1_is_not_translated(self):
        from chamadas_quadro_core import DependenciaRamoCore
        from memoria_quadro_core import MemoriaQuadro
        from selecao_ordens import SelecaoOrdens
        t = SelecaoOrdens(MemoriaQuadro([(0x494000, bytearray(0x8f000))]))
        with self.assertRaises(DependenciaRamoCore):
            t._bag_contient(0x49a0d4, 2, 9)

    def test_engin_in_zone_requires_its_pushed_word(self):
        from memoria_quadro_core import MemoriaQuadro
        from selecao_ordens import SelecaoOrdens
        t = SelecaoOrdens(MemoriaQuadro([(0x494000, bytearray(0x8f000))]))
        with self.assertRaises(ValueError):
            t.chamar('EnginInZone', dict(EAX=12, EBX=0, ECX=0, EDX=0, ESI=0, EDI=0, EBP=0))


if __name__ == '__main__':
    unittest.main()
