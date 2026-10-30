"""Core structure vision, group selection, minimap view and exit position without a CPU (M3.1 round 2).

- The capture and the exported bodies are intact original evidence; the capture matches the declared matrix.
- The committed native differential (329 measured steps, whole touched state) is bound to the current sources:
  editing the translation or the harness requires rerunning it.
- Every captured step replays exactly from the bytes the original read before writing: registers EAX..EBP (except
  the declared uncertain bits) and every changed byte. Deliberate mutations are caught.
- The adapters keep ai-runtime's and Economy's call shapes; named dependencies raise instead of defaulting.
"""
import hashlib
import json
import lzma
from pathlib import Path
import struct
import sys
import unittest
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
for _p in (RAIZ / 'ferramentas', RAIZ / 'testes'):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
PASTA = RAIZ / 'evidencias/visao-grupos'
CAPTURA = PASTA / 'captura-visao-grupos-exibicao.json.xz'
LEITURAS = PASTA / 'leituras-visao-grupos-exibicao.json.xz'
RELATORIO = RAIZ / 'relatorios/visao-grupos-emulada.json'
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff
_cache = {}


def captura():
    if 'c' not in _cache:
        _cache['c'] = json.loads(lzma.decompress(CAPTURA.read_bytes()))
    return _cache['c']


def leituras():
    if 'l' not in _cache:
        _cache['l'] = json.loads(lzma.decompress(LEITURAS.read_bytes()))['cases']
    return _cache['l']


def memoria_replay(runs):
    from test_chamadas_quadro_core import MemoriaEsparsa
    conhecidos = {}
    for inicio, valores in runs:
        a = int(inicio, 16)
        for i in range(len(valores) // 2):
            conhecidos[a + i] = int(valores[2 * i:2 * i + 2], 16)
    return MemoriaEsparsa(conhecidos)


def replay(teste, caso):
    """Run one captured step over its read-before-write bytes; returns the sound requests made."""
    from visao_grupos import VisaoGrupos
    m = memoria_replay(leituras()[caso['case']])
    pedidos = []

    def som(nome, regs, pilha):
        pedidos.append(nome)
        return regs['EAX']
    entrada = {k: int(caso['entry_registers'][k], 16) for k in REGISTROS}
    saida = VisaoGrupos(m, som=som).chamar(caso['routine'], entrada)
    incertos = saida.get('_incertos') or {}
    teste.assertEqual({k: hex(saida[k] & ~incertos.get(k, 0) & M32) for k in REGISTROS},
                      {k: hex(int(caso['exit_registers'][k], 16) & ~incertos.get(k, 0) & M32) for k in REGISTROS})
    m.conferir(teste, caso['changed_bytes'])
    teste.assertEqual(pedidos, [b['routine'] for b in caso['boundaries']])
    return pedidos


class EvidenciaOriginal(unittest.TestCase):
    def test_capture_is_original_only_and_matches_the_declared_matrix(self):
        import casos_visao_grupos as cvg
        d = captura()
        self.assertFalse(d['translation_executed'])
        self.assertTrue(all(d['path_reproduction'].values()), d['path_reproduction'])
        self.assertEqual(d['pause']['routine'], 'ProcessInputGame')
        self.assertTrue(all(c['reached_return'] for c in d['cases']))
        self.assertEqual((d['declared_cases'], len(d['cases'])), (320, 329))
        # rebuild the matrix from the grid pointers the capture's own writes reveal (the type-5 neighbour aims
        # depend on the type table's size words, so those writes are not compared here)
        por_nome = {c['case']: c for c in d['cases']}
        ponteiro = lambda caso, i, x, y: int(por_nome[caso]['writes'][i][0], 16) - cvg.celula(x, y)
        grades = dict(D=[0, ponteiro('decouvre_minimap_known_cells', -2, 31, 31), 0, 0], B=[0] * 4,
                      N=[ponteiro('illumine_sanctuary_p0_off_count1', 0, 12, 11),
                         ponteiro('illumine_sanctuary_p1_saturated', 0, 14, 12),
                         ponteiro('illuminecase_count0', 0, 20, 20),
                         0], atributos=0)
        progresso = d['preparations']['illumine_cave_p0_on'][1]
        alvo = int.from_bytes(bytes.fromhex(progresso['bytes']), 'little') + 2
        declarados = cvg.casos(alvo, grades, [(1, 1)] * 22)
        nomes = []
        for c in declarados:
            unico = len(c['steps']) == 1
            nomes += [(c['case'] if unico else f"{c['case']}/{i}.0", s['routine']) for i, s in enumerate(c['steps'])]
        self.assertEqual([(c['case'], c['routine']) for c in d['cases']], nomes)
        for c in declarados:
            if len(c['steps']) == 1 and not c['case'].startswith('decalage_type5_'):
                self.assertEqual(por_nome[c['case']]['writes'],
                                 [[hex(a), bytes(b).hex()] for a, b in c['steps'][0]['writes']], c['case'])

    def test_exported_bodies_match_the_intact_executable(self):
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

    def test_translation_tables_are_the_original_tables(self):
        import visao_grupos as vg
        tabelas = {t['name']: [int(x, 16) for x in t['entries']]
                   for t in json.loads((PASTA / 'manifesto.json').read_text())['jump_tables']}
        geometria = tabelas['CalculPosition geometry by structure type']
        self.assertEqual([None if a == 0x420b9e else a for a in geometria], list(vg.GEOMETRIA_POR_TIPO))
        self.assertEqual(set(vg.GEOMETRIA), set(geometria) - {0x420b9e})
        self.assertEqual(set(tabelas['TypeEnginEstEnLoop by type - 0xb']), {0x440c57})       # every entry -> AL 1
        rds = tabelas['RechercheDecalageSortie by structure type']
        self.assertEqual({t for t, a in enumerate(rds) if a == 0x41d23d}, {9, 12, 17})
        # the correction each type's second switch loads (mov eax, imm; or xor eax, eax at the shared tails)
        corpo = (PASTA / '00420698.asm').read_text().splitlines()
        imediatos = {}
        for linha in corpo:
            partes = linha.split()
            if len(partes) >= 4 and partes[2] == 'mov' and partes[3] == 'eax,' and partes[4].startswith('0x'):
                imediatos[int(partes[0], 16)] = int(partes[4], 16)
        for tipo, ramo in enumerate(vg.GEOMETRIA_POR_TIPO):
            if ramo is None:
                continue
            tabela = next(v for k, v in tabelas.items() if k.startswith('CalculPosition correction') and
                          int(k.split()[-1], 16) == self._tabela_do_ramo(corpo, ramo))
            self.assertEqual(imediatos.get(tabela[tipo], 0), vg.CORRECAO_POR_TIPO[tipo], tipo)

    @staticmethod
    def _tabela_do_ramo(corpo, ramo):
        """The correction table the geometry branch at ``ramo`` dispatches through (its first jmp dword ptr)."""
        dentro = False
        for linha in corpo:
            endereco = int(linha.split()[0], 16) if linha[:1] != ';' else None
            if endereco == ramo:
                dentro = True
            if dentro and 'jmp dword ptr' in linha:
                return int(linha.split('*4 + ')[1].rstrip(']'), 16)


class DiferencialNativoComprometido(unittest.TestCase):
    def test_report_has_no_mismatch_and_is_bound_to_the_current_sources(self):
        r = json.loads(RELATORIO.read_bytes())
        self.assertEqual(r['mismatches'], [])
        self.assertEqual(r['comparisons'], len(captura()['cases']))
        self.assertTrue(all(r['path_reproduction'].values()))
        self.assertEqual(r['capture']['sha256'], hashlib.sha256(CAPTURA.read_bytes()).hexdigest())
        for caminho, h in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / caminho).read_bytes()).hexdigest(), h,
                             f'{caminho} changed since the native differential: rerun validar_visao_grupos.py')


class ReplaySemCPU(unittest.TestCase):
    def test_every_captured_step_replays_exactly(self):
        sons = 0
        for caso in captura()['cases']:
            with self.subTest(case=caso['case']):
                sons += len(replay(self, caso))
        self.assertEqual(sons, 19)

    def test_deliberate_mutations_are_detected(self):
        import visao_grupos as vg
        por_nome = {c['case']: c for c in captura()['cases']}
        correcao = list(vg.CORRECAO_POR_TIPO)
        correcao[3] += 1
        mutacoes = (('position_type3', mock.patch.object(vg, 'CORRECAO_POR_TIPO', tuple(correcao))),
                    ('restaure_loop_type_first', mock.patch.object(vg, 'TIPOS_LOOP', range(0xb, 0xc))),
                    ('recentre_scroll_past_x', mock.patch.object(vg, 'VISTA_L', vg.VISTA_A)),
                    ('position_type1', mock.patch.dict(vg.REPOSICAO, {0x42072e: 0x102})))
        for nome, mutacao in mutacoes:
            with self.subTest(case=nome), mutacao, self.assertRaises((AssertionError, LookupError)):
                replay(self, por_nome[nome])

    def test_p3_cave_light_and_discovery(self):
        """The P3/P6/P7 stop: the structure loop lights the new 0xc8 cave for player 0 (BatimentIllumine on) and
        discovers it for the other players (BatimentDecouvre)."""
        por_nome = {c['case']: c for c in captura()['cases']}
        luz = por_nome['illumine_cave_created_p0_on']
        self.assertEqual(int(luz['exit_registers']['EAX'], 16), 5)                     # cave height
        descoberta = por_nome['decouvre_cave_created_p1']
        self.assertEqual(int(descoberta['exit_registers']['EAX'], 16), 6)              # height + 1
        self.assertEqual(len(descoberta['changed_bytes']), 7 * 7 + 4 * 7)             # 7x7 cells, border ring
        for nome in ('illumine_cave_created_p0_on', 'decouvre_cave_created_p1'):
            replay(self, por_nome[nome])


class Adaptadores(unittest.TestCase):
    def _memoria(self):
        from memoria_quadro_core import MemoriaQuadro
        return MemoriaQuadro([(0x494000, bytearray(0x8f000)), (0x10000000, bytearray(0x10000))])

    def test_economy_exit_adapter_marks_missing_registers(self):
        from chamadas_quadro_core import DependenciaRamoCore
        from visao_grupos import VisaoGrupos, escolher_saida, provedor_saida
        m = self._memoria()
        e = 0x49a0c8 + 2 * 276
        m.u8(e + 8, 5)
        m.u16(e + 2, 30 + 30 * 256)
        m.u16(0x495d8c + 52 * 5, 4)
        m.u16(0x495d8c + 52 * 5 + 2, 4)
        m.u32(0x507da8, 0x10000000)
        externo = provedor_saida(VisaoGrupos(m))
        saida = externo('CalculPosition', 0x420f5a, dict(EAX=2, EBX=0))
        self.assertEqual(saida['EAX'] & 0xffff, 0x2121)
        self.assertEqual(saida['_incertos']['EAX'], 0xffff0000)
        self.assertEqual(saida['_incertos']['ECX'], M32)
        exato = externo('CalculPosition', 0x420f5a, dict.fromkeys(REGISTROS, 0) | dict(EAX=2))
        self.assertEqual((exato['EAX'], exato.get('_incertos')), (0x2121, None))
        for dy in (-1, 0, 1):                  # every neighbour blocked: the CalculPosition cell itself
            for dx in (-1, 0, 1):
                m.u8(0x10000000 + 0x2121 + dy * 256 + dx, 1)
        self.assertEqual(escolher_saida(m)(2), 0x2121)
        m.u8(0x10000000 + 0x2122, 0)
        self.assertEqual(escolher_saida(m)(2), 0x2122)
        with self.assertRaises(DependenciaRamoCore):
            externo('EnginSetType', 0x420f69, dict(EAX=0))
        adiante = provedor_saida(VisaoGrupos(m), lambda n, c, r: dict(r, EAX=9))
        self.assertEqual(adiante('EnginSetType', 1, {})['EAX'], 9)

    def test_ai_runtime_keyword_providers(self):
        from visao_grupos import provedores_visao
        m = self._memoria()
        m.u16(0x497168, 64)
        m.u16(0x49716a, 64)
        m.u16(0x508724, 25)
        m.u16(0x508726, 17)
        m.u16(0x496fe0, 128)
        m.u16(0x496fe2, 128)
        p = provedores_visao(m)
        saida = p['MiniMapSetPos'](sitio=0x42bb5d, x=-3, y=40)
        self.assertEqual((m.u16(0x507d68), m.u16(0x507d6a), saida['EDX'], saida['ECX']), (0, 40, 40, 1))
        self.assertEqual(p['BatimentDecouvre'](sitio=0x428345, estrutura=0, jogador=0xc8)['EAX'], 0xc8)

    def test_named_dependencies_and_domain_raise(self):
        from chamadas_quadro_core import DependenciaRamoCore
        from visao_grupos import ForaDoDominioVisao, VisaoGrupos
        por_nome = {c['case']: c for c in captura()['cases']}
        caso = por_nome['restaure_builder_g1']
        m = memoria_replay(leituras()[caso['case']])
        with self.assertRaises(DependenciaRamoCore):
            VisaoGrupos(m).chamar('RestaureSelectionGroupe', {k: int(caso['entry_registers'][k], 16)
                                                              for k in REGISTROS})
        m = self._memoria()
        regs = dict.fromkeys(REGISTROS, 0)
        for nome, extra in (('BatimentIllumine', dict(EDX=4)), ('IllumineCase', dict(EDX=0xc8)),
                            ('DecouvreCase', dict(EDX=4))):
            with self.subTest(routine=nome), self.assertRaises(ForaDoDominioVisao):
                VisaoGrupos(m).chamar(nome, dict(regs, **extra))
        m.u8(0x49a0c8 + 8, 9)
        with self.assertRaises(ForaDoDominioVisao) as erro:
            VisaoGrupos(m).chamar('RechercheDecalageSortie', regs)
        self.assertEqual(erro.exception.endereco, 0x41d23d)


if __name__ == '__main__':
    unittest.main()
