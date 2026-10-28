"""Real economic/graphic/mission providers coexist without flat-name swaps."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ProviderImports(unittest.TestCase):
    def run_process(self, body, *args):
        bootstrap = 'import sys\nsys.path.insert(0, sys.argv[1])\n'
        result = subprocess.run(
            [sys.executable, '-I', '-B', '-c', bootstrap + body,
             str(ROOT), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_actual_providers_and_shared_mission_buffers_in_both_orders(self):
        body = '''
from pathlib import Path
import struct
from integracao.providers import load_economy_resources, load_graphics_structures
before_path = list(sys.path)
if sys.argv[2] == 'graphics-first':
    graphics = load_graphics_structures()
    assert 'construcoes' not in sys.modules
    economy = load_economy_resources()
else:
    economy = load_economy_resources()
    graphics = load_graphics_structures()
assert sys.path == before_path
assert load_graphics_structures() is graphics
assert load_economy_resources() is economy
import construcoes, graficos
assert hasattr(construcoes, 'TerrenoSacolas')
assert graphics is not construcoes
assert graphics.Catalogo is graficos.Catalogo
assert Path(construcoes.__file__).resolve() == Path(sys.argv[1]) / 'pesquisas-paralelas/economia/construcoes.py'
assert graphics.tabelas_jogador()[0] == bytes(range(256))

# Real providers share caller-owned buffers in this SAME process.
sys.path.insert(0, str(Path(sys.argv[1]) / 'pesquisas-paralelas/missoes'))
from carregador_auxiliares import carregar_minas_missao
from carregador_estruturas import carregar_estruturas_missao
from formatos import Leitor
resources = economy.RecursosTerreno(minas=b'\\x63' * 80)
mines = resources.minas
carregar_minas_missao(Leitor(struct.pack('<H', 0)), mines)
assert resources.minas is mines
for index in range(20):
    assert mines[index*4:index*4+2] == b'\\0\\0'
    assert resources.capacidade_mina(index) == 0x6363

payload = bytes(range(204))
eta = bytearray(0x50030)
eta[:4] = b'V0.3'
eta += struct.pack('<HHH', 1, 204, 7) + payload
records = graphics.ler_estruturas_eta(eta)
pool = bytearray(b'\\x63' * 276000)
carregar_estruturas_missao(Leitor(eta, 0x50030), pool)
assert records[0]['bytes'] == pool[7*276:7*276+204] == payload
assert pool[7*276+204:8*276] == b'\\x63' * 72
assert sys.modules['construcoes'] is construcoes
'''
        for order in ('graphics-first', 'economy-first'):
            with self.subTest(order=order):
                self.run_process(body, order)

    def test_existing_legacy_collision_is_rejected_without_rebinding(self):
        self.run_process('''
from pathlib import Path
from integracao.providers import load_economy_resources
sys.path.insert(0, str(Path(sys.argv[1]) / 'pesquisas-paralelas/graficos-animacao'))
import construcoes
before = dict(sys.modules)
before_path = list(sys.path)
try:
    load_economy_resources()
except ImportError as error:
    assert 'construcoes' in str(error) and 'already bound' in str(error)
else:
    raise AssertionError('Legacy graphic binding was silently replaced')
assert sys.path == before_path
assert all(sys.modules.get(name) is module for name, module in before.items())
assert set(sys.modules) == set(before)
assert sys.modules['construcoes'] is construcoes
''')

    def test_foreign_snapshot_bindings_fail_before_any_import(self):
        self.run_process('''
from types import ModuleType
from integracao.providers import load_economy_resources, load_graphics_structures
for name, loader in (('graficos', load_graphics_structures),
                     ('economia', load_economy_resources),
                     ('construcoes', load_economy_resources),
                     ('extracao', load_economy_resources)):
    module = ModuleType(name)
    module.__file__ = '/different-checkout/' + name + '.py'
    sys.modules[name] = module
    before = dict(sys.modules)
    try:
        loader()
    except ImportError:
        pass
    else:
        raise AssertionError('Foreign provider accepted: ' + name)
    assert set(sys.modules) == set(before)
    assert all(sys.modules.get(key) is value for key, value in before.items())
    del sys.modules[name]
''')


if __name__ == '__main__':
    unittest.main()
