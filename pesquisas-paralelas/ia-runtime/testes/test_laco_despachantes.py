"""Python dispatcher loops at the M1 post-load input, without emulation.

Inputs are the frozen accepted M1 final blocks. Expected effects are the
committed native captures (``captura-quadro-m2-pos-carga.json``). PlayerGetType
is Economy's committed ``Mercado.tipo_jogador`` over the actual player records.
The per-unit/per-structure bodies are not reconstructed yet. In the loop tests
they are declared recording stubs, and only the bytes the loops themselves own
are compared. The native hybrid comparison is
``validar_despachantes_m2.py`` (``validacao/m2-despachantes-native.json``).
"""
import json
from pathlib import Path
import struct
import sys
import unittest

OWNED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OWNED))
from ambiente_ia_runtime import ROOT  # noqa: E402
sys.path.insert(0, str(ROOT / 'pesquisas-paralelas/economia'))
from mercado import Mercado  # noqa: E402
from inventario_quadro_m2 import load_m1_post_load_state  # noqa: E402
from laco_despachantes import (PASSO, REGIOES_DESPACHO, UNIDADES, calcular_proxima_etapa_estruturas,  # noqa: E402
                               calcular_proxima_etapa_unidades, testar_utilidade)
from memoria_ia_runtime import MemoriaDeclarada  # noqa: E402
from quadro_calcul_game import Quadro  # noqa: E402
from reinicio_ia import DependenciaIA  # noqa: E402

CAPTURE = json.loads((OWNED / 'evidencias/captura-quadro-m2-pos-carga.json').read_text())
BY_LABEL = {c['label']: c for c in CAPTURE['captures']}
BLOCKS = load_m1_post_load_state()
VALIDATION = OWNED / 'validacao/m2-despachantes-native.json'


def world():
    segments = [(base, bytearray(data)) for base, data in BLOCKS]
    lookup = lambda a, n: next(bytes(d[a - b:a - b + n]) for b, d in segments if b <= a and a + n <= b + len(d))
    pool = struct.unpack('<I', lookup(0x4e19a0, 4))[0]
    players = lookup(struct.unpack('<I', lookup(0x5080a8, 4))[0], 80)
    regions = REGIOES_DESPACHO + ((pool, pool + UNIDADES * PASSO, 'unit pool'), (0x51a98c, 0x51a9dc, 'AI contexts'))
    mercado = Mercado(jogadores=players)
    providers = {'PlayerGetType': lambda sitio, jogador: mercado.tipo_jogador(jogador)}
    return MemoriaDeclarada(segments, regions), segments, providers


def apply_original(segments, changes):
    image = {b: bytearray(d) for b, d in segments}
    for change in changes:
        address = int(change['address'], 16)
        for base, data in image.items():
            if base <= address < base + len(data):
                data[address - base:address - base + change['size']] = bytes.fromhex(change['after'])
    return image


def owned_bytes(image, ranges):
    out = []
    for start, end in ranges:
        for base, data in image.items():
            if base <= start and end <= base + len(data):
                out.append(bytes(data[start - base:end - base]))
    return out


class DispatcherLoopTests(unittest.TestCase):
    def test_ia_test_utilite_matches_every_live_unit_and_structure_capture(self):
        for label, kind, index in [(f'ia_test_utilite_unit{u}', 1, u) for u in range(16)] + \
                                  [('ia_test_utilite_structure0', 3, 0)]:
            with self.subTest(label):
                memory, segments, providers = world()
                testar_utilidade(memory, providers, kind, index)
                expected = apply_original(BLOCKS, BY_LABEL[label]['changes'])
                self.assertEqual({b: bytes(d) for b, d in segments}, {b: bytes(d) for b, d in expected.items()})

    def test_unit_loop_owned_bytes_and_dispatch_order(self):
        memory, segments, providers = world()
        dispatched = []
        providers['EnginNextEtape'] = lambda sitio, unidade: dispatched.append((sitio, unidade))   # declared stub
        calcular_proxima_etapa_unidades(memory, providers)
        self.assertEqual(dispatched, [(0x456ead, u) for u in range(16)])
        pool = struct.unpack('<I', owned_bytes({b: d for b, d in BLOCKS}, [(0x4e19a0, 0x4e19a4)])[0])[0]
        ranges = [(0x4e1928, 0x4e1932), (0x4e1a38, 0x4e1a3c + 4 * 0x34)] + \
                 [(pool + u * PASSO + 0x10a, pool + u * PASSO + 0x10c) for u in range(16)]
        original = apply_original(BLOCKS, BY_LABEL['calcul_engin_next_etape']['changes'])
        self.assertEqual(owned_bytes({b: d for b, d in segments}, ranges), owned_bytes(original, ranges))

    def test_structure_loop_named_dependency_and_owned_counters(self):
        memory, segments, providers = world()
        with self.assertRaises(DependenciaIA) as raised:
            calcular_proxima_etapa_estruturas(memory, providers)
        self.assertEqual((raised.exception.rotina, raised.exception.sitio), ('ResetTableauHangar', 0x4281d0))

    def test_inactive_ai_players_and_monster_dependency(self):
        for player in (1, 2, 3):
            memory, segments, providers = world()
            self.assertEqual(Quadro(memory, providers).calcul_next_reflect(player, 1), 1)
            self.assertEqual({b: bytes(d) for b, d in segments}, {b: d for b, d in BLOCKS})
            self.assertEqual(BY_LABEL[f'calcul_next_reflect_p{player}']['changes'], [])
        memory, segments, providers = world()
        with self.assertRaises(DependenciaIA) as raised:
            Quadro(memory, providers).calcul_next_reflect(4, 1)
        self.assertEqual((raised.exception.rotina, raised.exception.sitio), ('AvanceMonstre', 0x47f939))

    def test_native_hybrid_validation_report_is_all_equal(self):
        report = json.loads(VALIDATION.read_text())
        self.assertEqual(report['summary'], dict(cases=23, equal=23))
        self.assertEqual(report['source_dirty_paths'], [])
        self.assertTrue(all(c['state_equal'] and c['call_order_equal'] for c in report['cases']))


if __name__ == '__main__':
    unittest.main()
