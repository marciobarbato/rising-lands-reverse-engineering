"""Combat and committed economy provider composed against original damage."""
import os
from pathlib import Path
import sys
import unittest

from bonus_combate import ConsultaBonusCombate
from consumo_dano import ConsumidorDanoUnidade
from projeteis import por16
import test_consumo_dano as damage_tests

# Read the committed provider in this same branch; never another live worktree.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'economia'))
from bonus_unidades import BonusUnidades


class ContratosBonusCombate(unittest.TestCase):
    def test_provider_widths_and_argument_permutation(self):
        table = bytearray(1872)
        table[8:11] = b'\x34\x12\x80'
        bonus = BonusUnidades(table)
        query = ConsultaBonusCombate(bonus)
        self.assertEqual(query('Modificateur', (0, 5, 0)), 0x1234)
        self.assertEqual(query('Modificateur', (0, 6, 0)), 128)
        self.assertEqual(bytes(bonus.memoria), table)

    def test_no_guessed_provider_or_undefined_selector(self):
        with self.assertRaisesRegex(NotImplementedError, 'Loaded'):
            ConsultaBonusCombate(None)('Modificateur', (0, 5, 0))
        for selector in (1, 8, 12, 13, 255):
            with self.assertRaisesRegex(NotImplementedError, '5/6'):
                ConsultaBonusCombate(None)('Modificateur', (0, selector, 0))
        with self.assertRaisesRegex(NotImplementedError, 'TerrainEstDecouvert'):
            ConsultaBonusCombate(None)('TerrainEstDecouvert', (0, 0))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialBonusCombate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_dano import BancadaConsumoDano
        cls.b = BancadaConsumoDano()
        cls.complete_returns = 0

    def compare(self, owner, kind, word5, byte6, protected=False):
        us, rows = damage_tests.fixture(tipo_fonte=kind, vida=1000, matriz=77)
        us[0][0], us[1][0], us[1][0xdc] = owner, (owner + 1) % 4, 8 if protected else 0
        us[0][0xf7], us[1][0xf6] = 213, 47
        self.b.preparar_consumo(us, rows, mod5=word5, mod6=byte6)
        raw = bytes(self.b.cpu.mem_read(0x4dfba0, 1872))
        real_bonus = BonusUnidades(raw)
        # These assertions fail if the fixture writes the wrong field/width.
        self.assertEqual(real_bonus.consultar(owner, kind, 5), word5)
        self.assertEqual(real_bonus.consultar(owner, kind, 6), byte6)
        self.b.infligir_unidade(1, 0)
        events = iter(self.b.eventos_consumo)
        def take(n, a):
            e = next(events)
            self.assertEqual((n, a), (e[0], e[1]))
            return e
        outer = self
        class ObservedBonus:
            def consultar(self, o, t, s):
                event = take('Modificateur', (o, s, t))
                result = real_bonus.consultar(o, t, s)
                outer.assertEqual(event[2] & (65535 if s == 5 else 255), result)
                return result  # real committed economy query, no replayed result
        def other(n, a):
            return take(n, a)[2]
        def effect(n, a):
            take(n, a)
        c = ConsumidorDanoUnidade(us, rows, ConsultaBonusCombate(ObservedBonus(), other), effect)
        c.infligir(1, 1, 0)
        self.assertEqual(list(events), [])
        self.assertEqual(self.b.ler_unidades(), b''.join(us))
        self.assertEqual(bytes(real_bonus.memoria), raw)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfba0, 1872)), raw)
        type(self).complete_returns += 1

    def test_selector5_word_and_selector6_byte_boundaries(self):
        for word5 in (0, 1, 255, 256, 257, 32767, 32768, 65534, 65535):
            for byte6 in (0, 1, 127, 128, 255):
                for protected in (False, True):
                    self.compare(0, 0, word5, byte6, protected)

    def test_all_low_bytes_with_nonzero_high_bytes(self):
        for value in range(256):
            self.compare(value % 4, value % 26,
                         value | (((value * 17) & 255) << 8), (value * 7) & 255)

    def test_all_loaded_owners_and_types(self):
        for owner in range(4):
            for kind in range(26):
                self.compare(owner, kind, 0xff00 | (owner + kind), (owner * 26 + kind) & 255)
