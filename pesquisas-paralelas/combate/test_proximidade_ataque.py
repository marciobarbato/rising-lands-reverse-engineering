"""Original radius-10 AL results, unchanged buffers and computed damage query."""
import os
import random
import struct
import unittest

from proximidade_ataque import proximidade_dono_ataque, ConsultaProximidadeAtaque
from bonus_combate import ConsultaBonusCombate
from consumo_dano import ConsumidorDanoUnidade
from projeteis import u16
import test_consumo_dano as damage_tests
import test_bonus_combate as bonus_tests


def set_word(grid, cell, value):
    struct.pack_into('<H', grid, 2 * cell, value)


class ContratosProximidadeAtaque(unittest.TestCase):
    def test_exact_owner_without_type_or_activity_filter(self):
        us, _ = damage_tests.fixture()
        us[7][0], us[7][1], us[7][2] = 200, 255, 0
        grid = bytearray(131072)
        set_word(grid, 0x1010, 0x4000 | (7 << 3) | 7)
        self.assertEqual(proximidade_dono_ataque(us, grid, 200, 0x1010), 1)
        self.assertEqual(proximidade_dono_ataque(us, grid, 0, 0x1010), 0)

    def test_domain_and_explicit_delegation_failures(self):
        us, _ = damage_tests.fixture()
        grid = bytearray(131072)
        q = ConsultaProximidadeAtaque(us, grid)
        with self.assertRaises(NotImplementedError):
            q('ChercheTypeEnginProximite', (3, 0, 0, 10))
        with self.assertRaises(NotImplementedError):
            q('ChercheTypeEnginProximite', (2, 0, 0, 11))
        with self.assertRaises(NotImplementedError):
            q('Modificateur', (0, 5, 0))
        set_word(grid, 0, 0x4000 | (800 << 3))
        with self.assertRaises(ValueError):
            q('ChercheTypeEnginProximite', (2, 0, 0, 10))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialProximidadeAtaque(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_dano import BancadaConsumoDano
        cls.b = BancadaConsumoDano()
        cls.proximity_returns = 0
        cls.composed_damage_returns = 0

    def compare(self, us, grid, owner, cell, desired_type=2):
        from bancada_consumo_dano import CONSUMO
        from bancada_combate import GRADE
        before = b''.join(us)
        raw = bytes(grid)
        self.b.mundo(us)
        self.b.cpu.mem_write(GRADE, raw)
        result = self.b.executar(0x4500e4, CONSUMO,
            dict(EAX=0xabcd0000 | desired_type, EDX=0xface0000 | owner,
                 EBX=0xbeef0000 | cell, ECX=10), limite_instrucoes=100000)
        self.assertEqual(result['EAX'] & 255, proximidade_dono_ataque(us, grid, owner, cell))
        self.assertEqual(self.b.ler_unidades(), before)
        self.assertEqual(b''.join(us), before)
        self.assertEqual(bytes(self.b.cpu.mem_read(GRADE, 131072)), raw)
        self.assertEqual(bytes(grid), raw)
        type(self).proximity_returns += 1

    def test_original_edge_clipping_and_circle_boundary(self):
        us, _ = damage_tests.fixture()
        us[7][0], us[7][1], us[7][2] = 2, 255, 0
        for cx in (0, 1, 9, 10, 127, 245, 255):
            for cy in (0, 1, 9, 10, 127, 245, 255):
                for dx, dy in ((0, 0), (10, 0), (10, 1), (7, 7), (8, 7), (-10, 0), (0, -10), (0, 10)):
                    grid = bytearray(131072)
                    if 0 <= cx + dx < 256 and 0 <= cy + dy < 256:
                        set_word(grid, cx + dx + 256 * (cy + dy), 0x4000 | (7 << 3))
                    self.compare(us, grid, 2, cx + 256 * cy)

    def test_original_grid_tags_indices_owners_and_unused_type(self):
        for index in (0, 7, 799):
            for owner in (0, 1, 4, 200, 255):
                us, _ = damage_tests.fixture()
                us[index][0], us[index][1], us[index][2] = owner, 255, 0
                for tag in (0, 0x4000, 0x8000, 0xc000):
                    for desired in (0, 2, 255):
                        grid = bytearray(131072)
                        set_word(grid, 0x8080, tag | (index << 3) | 7)
                        self.compare(us, grid, owner, 0x8080, desired)

    def test_original_mixed_square_records(self):
        rng = random.Random(0x4500e4)
        us, _ = damage_tests.fixture()
        for index in range(800):
            us[index][0] = rng.randrange(5)
        for case in range(64):
            grid = bytearray(131072)
            cx, cy = rng.randrange(256), rng.randrange(256)
            for _ in range(32):
                x, y = min(255, max(0, cx + rng.randrange(-11, 12))), min(255, max(0, cy + rng.randrange(-11, 12)))
                set_word(grid, x + 256 * y, rng.choice((0, 0x4000, 0x8000, 0xc000)) | (rng.randrange(800) << 3))
            self.compare(us, grid, case % 5, cx + 256 * cy)

    def test_real_proximity_and_bonus_in_complete_damage_consumers(self):
        from bancada_combate import GRADE
        for kind in (0, 2, 8, 12, 25):
            us, rows = damage_tests.fixture(tipo_fonte=kind)
            self.b.preparar_consumo(us, rows, mod5=257, mod6=9, bonus=9, grade={0x1010: 0x4000})
            grid = bytes(self.b.cpu.mem_read(GRADE, 131072))
            bonus = bonus_tests.BonusUnidades(bytes(self.b.cpu.mem_read(0x4dfba0, 1872)))
            self.b.infligir_unidade(1, 0)
            events = iter(self.b.eventos_consumo)
            def take(n, a):
                event = next(events)
                self.assertEqual((n, a), (event[0], event[1]))
                return event
            def other(n, a):
                return take(n, a)[2]
            proximity = ConsultaProximidadeAtaque(us, grid, other)
            real_queries = ConsultaBonusCombate(bonus, proximity)
            def query(n, a):
                if n in ('Modificateur', 'ChercheTypeEnginProximite'):
                    event = take(n, a)
                    result = real_queries(n, a)
                    self.assertEqual(event[2] & (65535 if n == 'Modificateur' and a[1] == 5 else 255), result)
                    return result
                return real_queries(n, a)
            c = ConsumidorDanoUnidade(us, rows, query, lambda n, a: take(n, a), bonus_4965ac=9)
            c.infligir(1, 1, 0)
            self.assertEqual(list(events), [])
            self.assertEqual(u16(us[1], 0x9a), 79)
            self.assertEqual(self.b.ler_unidades(), b''.join(us))
            self.assertEqual(bytes(self.b.cpu.mem_read(GRADE, 131072)), grid)
            type(self).composed_damage_returns += 1
