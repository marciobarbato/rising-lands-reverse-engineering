"""Coverage-run helpers without a CPU: entry counting inside executed blocks and the atomic summary."""
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
TEM_UNICORN = (RAIZ / '.local/python/unicorn').is_dir()


class _Cpu:
    def __init__(self):
        self.ganchos, self.flush = [], 0

    def hook_add(self, tipo, funcao, begin, end):
        self.ganchos.append((tipo, funcao, begin, end))

    def ctl_flush_tb(self):
        self.flush += 1


@unittest.skipUnless(TEM_UNICORN, 'Unicorn not installed in .local/python')
class ContadorEntradas(unittest.TestCase):
    def test_counts_every_entry_inside_each_block_once(self):
        import unicorn
        from cobrir_quadros_exibicao import ContadorEntradas
        cpu = _Cpu()
        b = types.SimpleNamespace(cpu=cpu, nomes={0x401000: 'A', 0x401010: 'B', 0x401014: 'C', 0x500000: 'Dados'},
                                  vinculos_declarados=types.SimpleNamespace(vinculos={0x401014: None}),
                                  fronteiras={}, pulos={})
        c = ContadorEntradas(b)
        (tipo, bloco, inicio, fim), = cpu.ganchos
        self.assertEqual((tipo, inicio, fim, cpu.flush), (unicorn.UC_HOOK_BLOCK, 0x401000, 0x493bff, 1))
        self.assertEqual(c.fronteiras, ['C'])
        bloco(None, 0x401000, 0x10, None)     # starts at A, ends before B
        bloco(None, 0x40100c, 0x0c, None)     # falls through B and C
        bloco(None, 0x401011, 0x02, None)     # inside B, no entry
        bloco(None, 0x401010, 0x04, None)     # starts at B, ends before C
        self.assertEqual(c.drenar(), {'A': 1, 'B': 2, 'C': 1})
        self.assertEqual(c.drenar(), {})


class Resumo(unittest.TestCase):
    def test_atomic_rewrite_leaves_no_temporary(self):
        from cobrir_quadros_exibicao import escrever_atomico
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'cobertura.json'
            escrever_atomico(p, dict(status='running'))
            escrever_atomico(p, dict(status='completed'))
            self.assertEqual(json.loads(p.read_text()), dict(status='completed'))
            self.assertEqual(sorted(x.name for x in Path(d).iterdir()), ['cobertura.json'])


if __name__ == '__main__':
    unittest.main()
