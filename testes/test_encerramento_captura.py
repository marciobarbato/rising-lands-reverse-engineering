"""Durable fast exit for native captures: evidence is fsynced and uc_close never runs at shutdown."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
TEM_UNICORN = importlib.util.find_spec('unicorn') is not None or (RAIZ / '.local/python/unicorn').is_dir()
# Disjoint 4 KiB regions in the child. Unicorn 2.1.4 needs about 3 s to free 3,000 such
# regions in uc_close (docs/core/UNICORN_TEARDOWN.md); the fast exit must not depend on the count.
REGIOES = 3000
LIMITE_SAIDA_S = 1.0


def _filho(corpo, *argumentos):
    """Run ``corpo`` in a fresh interpreter; return (exit status, stdout lines, seconds from 'written' to exit)."""
    programa = textwrap.dedent('''
        import sys, time
        sys.path.insert(0, {ferramentas!r}); sys.path.insert(0, {local!r})
        from encerramento_captura import encerrar_captura
    ''').format(ferramentas=str(RAIZ / 'ferramentas'), local=str(RAIZ / '.local/python')) + textwrap.dedent(corpo)
    linhas, marca = [], None
    with subprocess.Popen([sys.executable, '-B', '-c', programa, *argumentos], stdout=subprocess.PIPE, text=True,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1')) as p:
        for linha in p.stdout:
            linhas.append(linha.rstrip('\n'))
            if linha.startswith('written'):
                marca = time.monotonic()
        codigo = p.wait(timeout=120)
    return codigo, linhas, None if marca is None else time.monotonic() - marca


class EncerramentoCaptura(unittest.TestCase):
    def test_sync_refuses_a_missing_output(self):
        from encerramento_captura import sincronizar
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                sincronizar(Path(d) / 'absent.json')

    def test_exit_status_must_be_a_byte(self):
        from encerramento_captura import encerrar_captura
        for codigo in (-1, 256, '0', 1.0):
            with self.assertRaises(ValueError):
                encerrar_captura(codigo)

    def test_output_and_stdout_survive_with_the_given_status(self):
        with tempfile.TemporaryDirectory() as d:
            saida = Path(d) / 'evidence.json'
            codigo, linhas, _ = _filho('''
                import atexit
                atexit.register(lambda: print('atexit ran'))
                with open(sys.argv[1], 'x') as f:
                    f.write('{"calls": 1}\\n')
                print('written', flush=False)
                encerrar_captura(3, sys.argv[1])
            ''', str(saida))
            self.assertEqual(codigo, 3)
            self.assertEqual(saida.read_text(), '{"calls": 1}\n')
            # Unflushed stdout reaches the parent; atexit handlers do not run.
            self.assertEqual(linhas, ['written'])

    def test_missing_output_raises_instead_of_exiting(self):
        with tempfile.TemporaryDirectory() as d:
            codigo, linhas, _ = _filho('''
                try:
                    encerrar_captura(0, sys.argv[1])
                except FileNotFoundError:
                    print('refused')
            ''', str(Path(d) / 'never-written.json'))
            self.assertEqual((codigo, linhas), (0, ['refused']))


@unittest.skipUnless(TEM_UNICORN, 'Unicorn not installed in .local/python')
class PaginasCoalescidas(unittest.TestCase):
    PAGINAS = [0x3400000, *range(0x41400000, 0x41440000, 0x1000), 0x41441000, 0x47bd6000, 0x47bd7000]

    def test_runs_of_contiguous_pages(self):
        from emulador import paginas_em_execucoes
        self.assertEqual(paginas_em_execucoes(reversed(self.PAGINAS + [0x41400000])),
                         [(0x3400000, 0x1000), (0x41400000, 0x40000), (0x41441000, 0x1000), (0x47bd6000, 0x2000)])
        with self.assertRaises(ValueError):
            paginas_em_execucoes([0x3400800])

    def test_coalesced_mapping_has_the_same_bytes_and_bounds(self):
        from emulador import mapear_paginas, unicorn
        motores = []
        for coalescer in (False, True):
            cpu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
            if coalescer:
                self.assertEqual(len(mapear_paginas(cpu, self.PAGINAS)), 4)
            else:
                for p in self.PAGINAS:
                    cpu.mem_map(p, 0x1000)
            # A write across a page boundary inside a run, and bytes on both sides of each run.
            cpu.mem_write(0x41400ffe, b'\x11\x22\x33\x44')
            cpu.mem_write(0x47bd6ffc, b'\x55' * 8)
            motores.append(cpu)
        regioes = [{(a, z) for a, z, _ in cpu.mem_regions()} for cpu in motores]
        self.assertEqual((len(regioes[0]), len(regioes[1])), (len(self.PAGINAS), 4))
        for p in self.PAGINAS:
            self.assertEqual(*(bytes(cpu.mem_read(p, 0x1000)) for cpu in motores))
        for fora in (0x33ff000, 0x3401000, 0x41440000, 0x41442000, 0x47bd8000):
            for cpu in motores:
                with self.assertRaises(unicorn.UcError):
                    cpu.mem_read(fora, 1)


@unittest.skipUnless(TEM_UNICORN, 'Unicorn not installed in .local/python')
class SaidaRapidaComMuitasRegioes(unittest.TestCase):
    def test_exit_after_evidence_is_bounded_with_thousands_of_regions(self):
        with tempfile.TemporaryDirectory() as d:
            saida = Path(d) / 'evidence.json'
            codigo, linhas, segundos = _filho('''
                import unicorn
                cpu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
                n = int(sys.argv[2])
                for i in range(n):
                    cpu.mem_map(0x1000000 + 0x2000 * i, 0x1000)
                assert len(list(cpu.mem_regions())) == n
                with open(sys.argv[1], 'x') as f:
                    f.write(str(n))
                print('written', flush=True)
                encerrar_captura(0, sys.argv[1])
            ''', str(saida), str(REGIOES))
            self.assertEqual((codigo, linhas, saida.read_text()), (0, ['written'], str(REGIOES)))
            self.assertLess(segundos, LIMITE_SAIDA_S, f'{REGIOES} regions took {segundos:.2f} s to exit')


if __name__ == '__main__':
    unittest.main()
