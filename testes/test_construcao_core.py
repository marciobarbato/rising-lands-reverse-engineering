"""Core construction translations without a CPU, over the original-first capture (M3 groundwork).

- The capture and the exported bodies are intact original evidence; the capture matches the declared matrix.
- The committed native differential (153 cases, whole touched state) is bound to the current sources:
  editing the translation or the harness requires rerunning it.
- Every captured case outside M2.3's navigation world (DeplaceEngin) replays exactly from the bytes the
  original read before writing: registers EAX..EBP and every changed byte. Deliberate mutations are caught.
- Economy's committed native capture of CreerBatiment and CalculConstruireBatiment replays through Economy's
  ``OrdensEconomia`` with this module's ``provedor_construcao`` (and Core's selection-orders provider) in
  place of the original callees: exit registers and every final stored byte, the CAVE target included.
- Named dependencies raise instead of defaulting.
"""
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'testes'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
PASTA = RAIZ / 'evidencias/construcao-core'
CAPTURA = PASTA / 'captura-construcao-core-exibicao.json'
LEITURAS = PASTA / 'leituras-construcao-core-exibicao.json'
RELATORIO = RAIZ / 'relatorios/construcao-core-emulada.json'
ECONOMIA = RAIZ / 'pesquisas-paralelas/economia'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
NATIVAS = {'DeplaceEngin'}            # M2.3's live world needs the whole mapped state


def capturados():
    return json.loads(CAPTURA.read_bytes())['cases']


def memoria_replay(leituras):
    from test_chamadas_quadro_core import MemoriaEsparsa
    conhecidos = {}
    for inicio, valores in leituras:
        a = int(inicio, 16)
        for i in range(len(valores) // 2):
            conhecidos[a + i] = int(valores[2 * i:2 * i + 2], 16)
    return MemoriaEsparsa(conhecidos)


def replay(teste, caso, leituras):
    from construcao_core import ConstrucaoCore
    m = memoria_replay(leituras[caso['case']])
    entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
    saida = ConstrucaoCore(m).chamar(caso['routine'], entrada)
    teste.assertEqual({k: hex(saida[k]) for k in REGISTROS}, {k: caso['exit_registers'][k] for k in REGISTROS})
    m.conferir(teste, caso['changed_bytes'])


class EvidenciaOriginal(unittest.TestCase):
    def test_capture_is_original_only_and_matches_the_declared_matrix(self):
        import casos_construcao_core as ccc
        d = json.loads(CAPTURA.read_bytes())
        self.assertFalse(d['translation_executed'])
        self.assertTrue(all(d['path_reproduction'].values()), d['path_reproduction'])
        self.assertEqual(d['pause']['routine'], 'ProcessInputGame')
        self.assertTrue(all(c['reached_return'] for c in d['cases']))
        self.assertEqual(len(d['cases']), 153)
        dentro = next(c for c in d['cases'] if c['case'] == 'posable_cave_one_cell_hidden')
        ponteiros = {n: 0 for n in ccc.GRADES}
        ponteiros['descoberta0'] = int(dentro['writes'][0][0], 16) - ccc.celula(20, 11)
        alvo = next(c for c in d['cases'] if c['case'] == 'constructible_cave_builder_inside')
        ponteiros['atributos'] = int(alvo['writes'][-1][0], 16) - ccc.celula(20, 11)
        for nome, caso, indice, celula in (('objetos', 'place_wall_west_south', -2, ccc.CLIQUE - 1),
                                           ('regioes', 'reset_placed_wall_no_colour', -2, ccc.CLIQUE),
                                           ('tiles', 'grass_low_bound', 0, ccc.CLIQUE),
                                           ('cores', 'reset_placed_wall', -2, ccc.CLIQUE)):
            c = next(x for x in d['cases'] if x['case'] == caso)
            ponteiros[nome] = int(c['writes'][indice][0], 16) - celula * (2 if nome in ('tiles', 'regioes') else 1)
        declarados = ccc.casos(ponteiros)
        self.assertEqual([(c['case'], c['routine']) for c in d['cases']], [(c['case'], c['routine']) for c in declarados])
        self.assertEqual([c['writes'] for c in d['cases']],
                         [[[hex(a), bytes(b).hex()] for a, b in c['writes']] for c in declarados])

    def test_cave_target_is_placed_at_origin_19_10(self):
        c = next(x for x in capturados() if x['case'] == 'place_cave_target_19_10')
        self.assertTrue(c['calls'][0].startswith('0|BatimentModifyTerrain|0xa13,0x306,0x1,'))   # origin (19,10)
        self.assertNotIn('BatimentModifyMap', c['callee_counts'])
        self.assertNotIn('BatimentAlloc', c['callee_counts'])

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

    def test_translation_constants_are_the_original_tables(self):
        from colocacao_estruturas import PRIMEIROS_TILES
        from construcao_core import TIPOS_QUATRO_CELULAS
        tabelas = {t['name']: [int(x, 16) for x in t['entries']]
                   for t in json.loads((PASTA / 'manifesto.json').read_text())['jump_tables']}
        corpo = (PASTA / '0041c4ac.asm').read_text().splitlines()
        tiles = {int(l.split()[0], 16): int(l.split(', ')[-1], 16) for l in corpo if 'mov edx, 0x' in l}
        primeiro = [tiles.get(a) for a in tabelas['PlaceBatiment first tile by structure type']]
        self.assertEqual([p for t, p in enumerate(primeiro) if t not in (9, 12)],
                         [p for t, p in enumerate(PRIMEIROS_TILES) if t not in (9, 12)])
        # EnginOccupeCase's four-cell types, read from its compare chain (0x4424d3..0x442581).
        self.assertEqual(TIPOS_QUATRO_CELULAS, frozenset((3, 11, 12, 13, 14, 15, 16, 25)))


class DiferencialNativoComprometido(unittest.TestCase):
    def test_report_has_no_mismatch_and_is_bound_to_the_current_sources(self):
        r = json.loads(RELATORIO.read_bytes())
        self.assertEqual(r['mismatches'], [])
        self.assertEqual(r['comparisons'], len(capturados()))
        self.assertTrue(all(r['path_reproduction'].values()))
        self.assertEqual(r['capture']['sha256'], hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        for caminho, h in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), h,
                             f'{caminho} changed since the native differential: rerun validar_construcao_core.py')


class ReplaySemCPU(unittest.TestCase):
    def test_every_case_outside_the_live_world_replays_exactly(self):
        leituras = json.loads(LEITURAS.read_bytes())['cases']
        replayed = 0
        for caso in capturados():
            if caso['routine'] in NATIVAS:
                continue
            with self.subTest(case=caso['case']):
                replay(self, caso, leituras)
                replayed += 1
        self.assertEqual(replayed, 135)

    def test_deliberate_mutations_are_detected(self):
        import construcao_core as cc
        leituras = json.loads(LEITURAS.read_bytes())['cases']
        por_nome = {c['case']: c for c in capturados()}
        tiles = list(cc.PRIMEIROS_TILES)
        tiles[3] += 1
        mutacoes = (('place_cave_target_19_10', mock.patch.object(cc, 'PRIMEIROS_TILES', tuple(tiles))),
                    ('constructible_cave_quad_builder', mock.patch.object(cc, 'TIPOS_QUATRO_CELULAS', frozenset())),
                    ('posable_cave_target', mock.patch.object(cc, 'MATRIZ_POSAVEL', cc.MATRIZ_POSAVEL + 1)),
                    ('reset_sanctuary', mock.patch.object(cc, 'CORES_LIVRES', cc.CORES_LIVRES + 0x100)))
        for nome, mutacao in mutacoes:
            with self.subTest(case=nome), mutacao, self.assertRaises((AssertionError, LookupError)):
                replay(self, por_nome[nome], leituras)


class ComposicaoEconomia(unittest.TestCase):
    """Economy's CreerBatiment/CalculConstruireBatiment over Economy's own native capture, with Core's
    providers instead of the replayed original callees."""

    def test_economy_build_path_replays_with_cores_providers(self):
        sys.path.insert(0, str(ECONOMIA))
        from construcao_core import ConstrucaoCore, provedor_construcao
        from ordens_economia import OrdensEconomia, provedor_core
        from selecao_ordens import SelecaoOrdens
        import validar_ordens_economia as v
        captura = json.loads(v.CAPTURA.read_bytes())['cases']
        leituras = json.loads((ECONOMIA / 'evidencias/ordens-economia/leituras-ordens-economia-exibicao.json')
                              .read_bytes())['cases']
        alcancados, replayed = set(), 0
        for caso in captura:
            nomes = [c.split('|')[1] for c in caso['calls']]
            if caso['routine'] not in ('CreerBatiment', 'CalculConstruireBatiment') or caso['case'] in v.FORA_DO_DOMINIO:
                continue
            if 'ResetOrdre' in nomes or 'DeplaceEngin' in nomes:
                continue
            with self.subTest(case=caso['case']):
                m = v.Gravadora(memoria_replay(leituras[caso['case']]))
                externo = provedor_core(SelecaoOrdens(m, som=lambda n, r, p: r['EAX']),
                                        provedor_construcao(ConstrucaoCore(m)))
                entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS + ('ESP',)}
                saida = OrdensEconomia(m, externo=externo).chamar(caso['routine'], entrada)
                self.assertEqual({k: hex(saida[k]) for k in REGISTROS},
                                 {k: caso['exit_registers'][k] for k in REGISTROS})
                self.assertEqual(m.finais, v.finais_nativos(caso))
                alcancados |= set(nomes) & {'PlaceBatiment', 'BatimentConstructible', 'BatimentCollision',
                                            'ResetCheminTerrainModify'}
                replayed += 1
        self.assertEqual(alcancados, {'PlaceBatiment', 'BatimentConstructible', 'BatimentCollision',
                                      'ResetCheminTerrainModify'})
        self.assertGreaterEqual(replayed, 20)

    def test_cave_target_charges_20_24_and_places_origin_19_10(self):
        sys.path.insert(0, str(ECONOMIA))
        from construcao_core import ConstrucaoCore, provedor_construcao
        from ordens_economia import OrdensEconomia, provedor_core
        from selecao_ordens import SelecaoOrdens
        import validar_ordens_economia as v
        caso = next(c for c in json.loads(v.CAPTURA.read_bytes())['cases'] if c['case'] == 'build_tick_arrived_cave')
        leituras = json.loads((ECONOMIA / 'evidencias/ordens-economia/leituras-ordens-economia-exibicao.json')
                              .read_bytes())['cases']
        m = memoria_replay(leituras[caso['case']])
        externo = provedor_core(SelecaoOrdens(m, som=lambda n, r, p: r['EAX']), provedor_construcao(ConstrucaoCore(m)))
        entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS + ('ESP',)}
        OrdensEconomia(m, externo=externo).chamar('CalculConstruireBatiment', entrada)
        registro = 0x49a0c8 + 276
        self.assertEqual((m.u8(registro + 5), m.u8(registro + 8), m.u16(registro + 2)), (2, 3, 0x0a13))
        self.assertEqual((m.u16(0x4e2ea8 + 8 + 2), m.u16(0x4e2ea8 + 16 + 2)), (20, 24))   # food, stone totals
        tiles = m.u32(0x507d70)
        self.assertEqual(m.u16(tiles + 2 * 0x0a13), 0x306)                               # first CAVE tile


class DependenciasNomeadas(unittest.TestCase):
    def test_fatigue_after_a_step_requires_economys_bonus(self):
        from chamadas_quadro_core import DependenciaRamoCore
        from construcao_core import ConstrucaoCore
        from memoria_quadro_core import MemoriaQuadro
        dgroup, pool = bytearray(0x8f000), bytearray(800 * 276)
        m = MemoriaQuadro([(0x494000, dgroup), (0x10000000, pool)])
        m.u32(0x4e19a0, 0x10000000)
        rec = 0x10000000 + 12 * 276
        m.u8(rec + 1, 7)
        m.u8(rec + 2, 11)
        m.u8(rec + 0x72, 1)
        antes = dict(tipo=7, dono=0, visivel=1, contador=0, provisoes=0, f8=0)
        with self.assertRaises(DependenciaRamoCore) as erro:
            ConstrucaoCore(m)._saida_avance(12, rec, antes)
        self.assertEqual(erro.exception.endereco, 0x452d48)
        self.assertEqual(ConstrucaoCore(m, bonus=lambda j, t, s: 5)._saida_avance(12, rec, antes), 5)

    def test_economy_adapter_raises_for_other_routines_and_forwards_when_given(self):
        from chamadas_quadro_core import DependenciaRamoCore
        from construcao_core import ConstrucaoCore, provedor_construcao
        from memoria_quadro_core import MemoriaQuadro
        m = MemoriaQuadro([(0x494000, bytearray(0x8f000))])
        regs = dict(EAX=3, EBX=0, ECX=0, EDX=0, ESI=0, EDI=0, EBP=0, ESP=0x2000000)
        with self.assertRaises(DependenciaRamoCore) as erro:
            provedor_construcao(ConstrucaoCore(m))('EnginAsk', 0x44ad00, regs)
        self.assertEqual(erro.exception.endereco, 0x44ad00)
        self.assertEqual(provedor_construcao(ConstrucaoCore(m), lambda n, c, r: dict(r, EAX=7))('EnginAsk', 1, regs)['EAX'],
                         7)
        entrada = dict(regs, EAX=0x16, EDX=0x1234, ECX=0xabcd0000, _incertos={'ECX': 0xffff0000})
        saida = provedor_construcao(ConstrucaoCore(m))('BatimentCollision', 0x420199, entrada)
        self.assertEqual((saida['EAX'], saida['ECX'], saida['_incertos']), (0x1200, 0xabcd0000, {'ECX': 0xffff0000}))

    def test_protected_inputs_raise_before_any_store(self):
        from construcao_core import ConstrucaoCore
        from memoria_quadro_core import MemoriaQuadro
        dgroup = bytearray(0x8f000)
        m = MemoriaQuadro([(0x494000, dgroup)])
        regs = dict(EAX=1000, EBX=0, ECX=0, EDX=0, ESI=0, EDI=0, EBP=0)
        for rotina in ('PlaceBatiment', 'ResetCheminTerrainModify'):
            with self.subTest(routine=rotina), self.assertRaises(ValueError):
                ConstrucaoCore(m).chamar(rotina, regs)
        m.u8(0x49a0c8 + 276 + 8, 22)
        with self.assertRaises(ValueError):
            ConstrucaoCore(m).chamar('PlaceBatiment', dict(regs, EAX=1))
        self.assertEqual(bytes(dgroup).count(0), len(dgroup) - 1)


if __name__ == '__main__':
    unittest.main()
