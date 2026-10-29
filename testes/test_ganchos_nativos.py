"""Native pass-2 hook tooling without the compiled library (always runs).

The library itself is exercised by test_emulacao_ganchos_nativos (RISING_EMULAR=1).
"""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
for caminho in (RAIZ / 'ferramentas', RAIZ / 'pesquisas-paralelas/missoes'):
    if str(caminho) not in sys.path:
        sys.path.insert(0, str(caminho))

import compilar_ganchos_nativos as comp  # noqa: E402
import ganchos_nativos as gn  # noqa: E402

AUSENTE = RAIZ / '.local/nativo/inexistente/libganchos_memoria.dylib'


class Compilacao(unittest.TestCase):
    def test_comando_deterministico(self):
        cmd = comp.comando()
        self.assertEqual(cmd, comp.comando())
        self.assertEqual(cmd[0], '/usr/bin/clang')
        self.assertEqual(cmd[-1], 'ferramentas/nativo/ganchos_memoria.c')     # relative: no absolute path embedded
        self.assertIn(f'-DGANCHOS_IDENTIDADE="sha256={comp.identidade()}"', cmd)
        self.assertEqual(comp.BIBLIOTECA.relative_to(RAIZ).parts[:2], ('.local', 'nativo'))

    def test_identidade_cobre_fonte_e_opcoes(self):
        with tempfile.TemporaryDirectory() as pasta:
            fonte = Path(pasta) / 'g.c'
            fonte.write_bytes(comp.FONTE.read_bytes())
            self.assertEqual(comp.identidade(fonte), comp.identidade())
            fonte.write_bytes(comp.FONTE.read_bytes() + b' ')
            self.assertNotEqual(comp.identidade(fonte), comp.identidade())
        with mock.patch.object(comp, 'OPCOES', comp.OPCOES + ('-DX',)):
            outra = comp.identidade()
        self.assertNotEqual(outra, comp.identidade())

    def test_binario_ignorado(self):
        import subprocess
        r = subprocess.run(['git', '-C', str(RAIZ), 'check-ignore', '-q', str(comp.BIBLIOTECA)])
        self.assertEqual(r.returncode, 0)


class SemFallback(unittest.TestCase):
    def test_biblioteca_ausente_falha_com_instrucao(self):
        with self.assertRaisesRegex(gn.BibliotecaNativaIndisponivel, 'missing.*compilar_ganchos_nativos'):
            gn.carregar(AUSENTE)

    def test_ganchos_politica_nao_toca_a_bancada(self):
        class Cpu:
            _uch = None

            def hook_add(self, *a, **k):
                raise AssertionError('no hook may be installed without the native library')

        class Bancada:
            sym, fase, cpu = {}, 'load_tail', Cpu()
        b = Bancada()
        with self.assertRaises(gn.BibliotecaNativaIndisponivel):
            gn.ganchos_politica(b, {0x4e0000}, biblioteca=AUSENTE)
        self.assertIs(type(b), Bancada)

    def test_injecao_falha_antes_de_trocar_os_ganchos(self):
        import politica_comparacao_quadros as pol
        import politica_ganchos_nativos as pgn
        original = pol.ganchos
        with mock.patch.object(comp, 'BIBLIOTECA', AUSENTE):
            with self.assertRaises(gn.BibliotecaNativaIndisponivel):
                pgn.injetar('nativo')
        self.assertIs(pol.ganchos, original)
        self.assertIs(pgn.injetar('python'), pol)
        self.assertIs(pol.ganchos, original)


class Faixas(unittest.TestCase):
    def test_faixas_do_python(self):
        alvos = {10, 11, 12, 14, 20, 21}
        self.assertEqual(gn.faixas_gancho(alvos), [(7, 12), (11, 14), (17, 21)])


class Comparacao(unittest.TestCase):
    def relatorio(self):
        return dict(schema='s', source_revision='r', translation_executed=False, evidence=True, frames=1,
                    cumulative=dict(totals=dict(display_only=2, game_logic=1, read_only_in_window=0),
                                    exclusion_mask=[['0x10', '0x12']]),
                    windows={}, game_logic_bytes={'0x20': dict(block='dgroup', phases=['frame1'],
                                                               writers=['logic:Random'], readers=['logic:Random'])},
                    surfaces=dict(accesses_by_context={}, logic_context_accesses={}, excluded_with_proof=True),
                    seconds=1.0, passed=True)

    def test_igual_ignorando_proveniencia(self):
        import politica_ganchos_nativos as pgn
        ref = self.relatorio()
        novo = copy.deepcopy(ref)
        novo.update(source_revision='x', seconds=9.0, evidence=False)
        c = pgn.comparar_relatorios(ref, novo)
        self.assertEqual(c['result'], 'equal')
        self.assertTrue(c['body_json_equal'] and c['exclusion_mask_equal'] and c['game_logic_writers_readers_equal'])

    def test_diferenca_de_leitor(self):
        import politica_ganchos_nativos as pgn
        ref = self.relatorio()
        novo = copy.deepcopy(ref)
        novo['game_logic_bytes']['0x20']['readers'].append('display:AffGame')
        c = pgn.comparar_relatorios(ref, novo)
        self.assertEqual((c['result'], c['differing_fields'], c['game_logic_writers_readers_equal']),
                         ('different', ['game_logic_bytes'], False))


if __name__ == '__main__':
    unittest.main()
