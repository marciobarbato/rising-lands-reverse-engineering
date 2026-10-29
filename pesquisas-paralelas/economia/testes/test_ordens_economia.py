"""Economy order setters and construction gates (M3 groundwork) over the original-first capture.

- The capture is original-only, reproduces Core's accepted pause path and matches the declared matrix;
  the exported bodies are the intact original bytes.
- The committed native differential (121 cases, whole touched state) is bound to the current sources.
- Every case whose path avoids Core's ResetOrdre (live navigation world) replays without a CPU from the
  bytes the original read before writing: exit registers, the final value of every stored byte, each
  call into another front (name and arguments) and the sound requests. Deliberate mutations are caught.
- Named dependencies raise instead of defaulting.
- RISING_EMULAR=1 reruns the native differential (about 2 minutes).
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
from unittest import mock

PASTA = Path(__file__).resolve().parents[1]
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import validar_ordens_economia as v  # noqa: E402

REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP')


def captura():
    return json.loads(v.CAPTURA.read_bytes())


class MemoriaEsparsa:
    """Only the bytes the original read before writing are known; any other read raises."""
    def __init__(self, leituras):
        self.bytes = {}
        for inicio, valores in leituras:
            a = int(inicio, 16)
            for i in range(len(valores) // 2):
                self.bytes[a + i] = int(valores[2 * i:2 * i + 2], 16)

    def _acesso(self, n, a, valor):
        if valor is None:
            try:
                return int.from_bytes(bytes(self.bytes[(a + i) & 0xffffffff] for i in range(n)), 'little')
            except KeyError as erro:
                raise LookupError(f'read of 0x{a:x} outside the recorded reads') from erro
        valor &= (1 << 8 * n) - 1
        for i in range(n):
            self.bytes[(a + i) & 0xffffffff] = valor >> 8 * i & 0xff
        return valor

    def u8(self, a, v=None):
        return self._acesso(1, a, v)

    def u16(self, a, v=None):
        return self._acesso(2, a, v)

    def u32(self, a, v=None):
        return self._acesso(4, a, v)


def sem_cpu(c):
    lista = v.chamadas(c)
    return not any(lista[i]['name'] == 'ResetOrdre' for i, _ in v.externas(lista))


def replay(caso, leituras):
    m = v.Gravadora(MemoriaEsparsa(leituras[caso['case']]))
    declarado = dict(case=caso['case'], routine=caso['routine'], stack=[int(x, 16) for x in caso['stack_words']])
    registro, _, saida = v.traduzir(declarado, caso, m)
    if 'raised' in registro:
        registro['ok'] = registro['ok'] and not m.finais
    elif saida is not None:
        registro['stores_equal'] = m.finais == v.finais_nativos(caso)
        registro['ok'] = registro['ok'] and registro['stores_equal']
    return registro


class EvidenciaOriginal(unittest.TestCase):
    def test_capture_is_original_only_and_matches_the_matrix(self):
        import casos_ordens_economia as coe
        d = captura()
        self.assertFalse(d['translation_executed'])
        self.assertTrue(all(d['path_reproduction'].values()), d['path_reproduction'])
        self.assertEqual(d['pause']['routine'], 'ProcessInputGame')
        self.assertTrue(all(c['reached_return'] for c in d['cases']))
        alvo = next(c for c in d['cases'] if c['case'] == 'mine_unit_cell_undiscovered')
        grade = int(alvo['writes'][-1][0], 16) - coe.celula(17, 16)
        declarados = coe.casos(grade)
        self.assertEqual([(c['case'], c['routine']) for c in d['cases']], [(c['case'], c['routine']) for c in declarados])
        self.assertEqual([c['writes'] for c in d['cases']],
                         [[[hex(a), bytes(b).hex()] for a, b in c['writes']] for c in declarados])
        self.assertEqual(len(d['cases']), 121)

    def test_exported_bodies_match_the_intact_executable(self):
        manifesto = json.loads((PASTA / 'evidencias/ordens-economia/manifesto.json').read_text())
        exe = RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE'
        if not exe.exists():
            self.skipTest('intact RISING.EXE not present')
        import extrair_ordens_economia as e
        ler = e.ler_pe()
        for t in manifesto['intervals']:
            a, z = int(t['start'], 16), int(t['end_exclusive'], 16)
            self.assertEqual(hashlib.sha256(ler(a, z - a)).hexdigest(), t['sha256'], t['name'])

    def test_native_report_is_bound_to_the_current_sources(self):
        r = json.loads(v.RELATORIO.read_bytes())
        self.assertEqual(r['capture']['sha256'], hashlib.sha256(v.CAPTURA.read_bytes()).hexdigest())
        for p, h in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((RAIZ / p).read_bytes()).hexdigest(), h,
                             f'{p} changed: rerun validar_ordens_economia.py')
        self.assertEqual(r['comparisons'], 121)
        self.assertEqual(r['mismatches'], [])
        self.assertTrue(all(r['path_reproduction'].values()))


class ReplaySemCpu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.casos = [c for c in captura()['cases'] if sem_cpu(c)]
        cls.leituras = json.loads(v.LEITURAS.read_bytes())['cases']

    def test_cases_replay_exactly(self):
        registros = [replay(c, self.leituras) for c in self.casos]
        self.assertGreaterEqual(len(registros), 90)
        self.assertEqual([r for r in registros if not r['ok']], [])

    def test_mutations_are_detected(self):
        import ordens_economia as oe
        original_set_depot = oe.OrdensEconomia.set_depot_engin
        mutacoes = {
            'travail food asks for stone': ('engin_travail_selectionne', 'work_food_u13'),
            'depot +0x84 not zero-extended': ('set_depot_engin', 'engin_depot_u12'),
            'debit wraps instead of flooring': ('enleve_matiere', 'debit_above_total'),
            'cave owner is the player': ('creer_batiment', 'create_cave_p0'),
            'abandon keeps the order type': ('_abandonar', 'build_tick_target_moved'),
        }

        def travail(self, regs):
            r = dict(regs)
            if r['EDX'] & 0xff == 1:
                r['EDX'] = (r['EDX'] & ~0xff) | 2
            return mutado_travail(self, r)
        mutado_travail = oe.OrdensEconomia.engin_travail_selectionne

        def depot(self, regs):
            saida = original_set_depot(self, regs)
            self.m.u16(self._pool() + (regs['EAX'] & 0xffff) * 276 + 0x84, regs['ECX'] | 0x100)
            return saida

        def debito(self, regs):
            o = ((regs['EBX'] & 0xffff) * 4 + (regs['EAX'] & 0xff)) * 8
            self.m.u16(oe.RECURSOS + 2 + o, self.m.u16(oe.RECURSOS + 2 + o) - regs['EDX'])
            return self._sair(regs, dict(regs, EAX=o), ('ECX', 'EDX', 'ESI', 'EDI', 'EBP'))
        criar_original = oe.OrdensEconomia.creer_batiment

        def criar(self, regs):
            saida = criar_original(self, regs)
            if saida['EAX'] != 0xffff:
                self.m.u8(oe.ESTRUTURAS + 276 * saida['EAX'] + 4, regs['EBX'])
            return saida
        abandonar_original = oe.OrdensEconomia._abandonar

        def abandonar(self, regs, r, u, rec):
            tipo = self.m.u8(rec + 0xbe)
            saida = abandonar_original(self, regs, r, u, rec)
            self.m.u8(rec + 0xbe, tipo)
            return saida
        substitutos = {'engin_travail_selectionne': travail, 'set_depot_engin': depot, 'enleve_matiere': debito,
                       'creer_batiment': criar, '_abandonar': abandonar}
        por_nome = {c['case']: c for c in self.casos}
        for rotulo, (metodo, caso) in mutacoes.items():
            with self.subTest(rotulo), mock.patch.object(oe.OrdensEconomia, metodo, substitutos[metodo]):
                self.assertFalse(replay(por_nome[caso], self.leituras)['ok'], rotulo)


class Dependencias(unittest.TestCase):
    def test_other_fronts_raise_without_a_provider(self):
        import ordens_economia as oe
        m = MemoriaEsparsa([[hex(oe.PONTEIRO_UNIDADES), '00804a47']])
        regs = dict(EAX=12, EBX=0, ECX=0, EDX=0x82b, ESI=0, EDI=0, EBP=0, ESP=0x1000)
        with self.assertRaises(oe.DependenciaOrdemEconomia) as erro:
            oe.OrdensEconomia(m).chamar('SetMineEngin', regs)
        self.assertEqual(erro.exception.chamada, 0x444f67)

    def test_core_provider_does_not_cover_other_fronts(self):
        import ordens_economia as oe
        externo = oe.provedor_core(object())
        with self.assertRaises(oe.DependenciaOrdemEconomia) as erro:
            externo('PlaceBatiment', 0x420274, dict.fromkeys(REG7, 0))
        self.assertEqual(erro.exception.rotina, 'PlaceBatiment')

    def test_out_of_domain_branches_raise_before_any_store(self):
        self.assertEqual(sorted(v.FORA_DO_DOMINIO), ['build_tick_gate_type9', 'build_tick_progress_byte1',
                                                     'build_tick_state15'])


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialNativo(unittest.TestCase):
    def test_every_declared_case_matches_the_original(self):
        import capturar_ordens_economia as coe
        por_nome = {c['case']: c for c in captura()['cases']}
        registros = []

        def observador(caso, antes, resultado):
            nativo = dict(resultado, calls=[coe.chamada_compacta(c) for c in resultado['calls']])
            registros.append(v.comparar(caso, antes, nativo, por_nome.get(caso['case'])))
        _, _, _, reproducao, _, _ = coe.executar('exibicao', observador)
        self.assertTrue(all(reproducao.values()), reproducao)
        self.assertEqual(len(registros), len(por_nome))
        self.assertEqual([r for r in registros if not r['ok']], [])


if __name__ == '__main__':
    unittest.main()
