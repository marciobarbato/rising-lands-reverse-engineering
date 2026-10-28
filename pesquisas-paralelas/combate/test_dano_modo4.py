"""Initialized direction-29/30 mode-4 damage and signed quarter table."""
import os
import struct
import unittest

from consumo_dano import ConsumidorDanoUnidade, LimiteMorte
from projeteis import u16
import test_consumo_dano as damage_tests
import test_dano_modo8 as special_tests


class ContratosDanoModo4(unittest.TestCase):
    def test_loaded_direction_selection_and_signed_quarter(self):
        for kind, value, loss in ((2, 127, 127), (3, 127, 31), (3, 128, 1),
                                   (3, 255, 0), (17, 127, 127)):
            us, rows = damage_tests.fixture(tipo_alvo=kind, vida=1000)
            c, calls = damage_tests.local(us, rows)
            c.danos_modo4 = bytes([value, 5])
            c.infligir(1, 4, 0, 0x11d)
            self.assertEqual(u16(us[1], 0x9a), 1000-loss)
            self.assertEqual([name for name, _ in calls], ['Modificateur', 'TerrainEstDecouvert'])

    def test_missing_values_and_uninitialized_directions_fail_early(self):
        us, rows = damage_tests.fixture()
        c, calls = damage_tests.local(us, rows)
        with self.assertRaisesRegex(ValueError, 'loaded'):
            c.infligir(1, 4, 0, 29)
        for direction in (0, 1, 28, 31, 255):
            with self.assertRaises(NotImplementedError):
                c.infligir(1, 4, 0, direction)
        with self.assertRaisesRegex(ValueError, 'u8'):
            ConsumidorDanoUnidade(us, rows, danos_modo4=(256, 0))
        self.assertEqual(calls, [])
        self.assertEqual(u16(us[1], 0x9a), 100)

    def test_mode4_does_not_call_mode1_lethal_handler(self):
        us, rows = damage_tests.fixture(vida=1)
        c, _ = damage_tests.local(us, rows)
        c.danos_modo4 = bytes([20, 30])
        c.morte = lambda *args: self.fail('Mode-1 death handler must not run')
        with self.assertRaises(LimiteMorte) as caught:
            c.infligir(1, 4, 0, 30)
        self.assertEqual((caught.exception.modo, u16(us[1], 0x9a)), (4, 1))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialDanoModo4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_dano import BancadaConsumoDano
        cls.b = BancadaConsumoDano()
        cls.complete_returns = cls.death_stops = cls.audio_stops = 0

    def compare(self, us, rows, raw=20, direction=29, **kwargs):
        pair = (raw, 37) if direction == 29 else (37, raw)
        return special_tests.DiferencialDanoModo8.compare(self, us, rows, None,
            mode=4, direction=direction, mode4=pair, **kwargs)

    def test_original_all_types_and_both_loaded_bytes(self):
        for kind in range(26):
            for direction in (29, 30):
                for raw in (0, 1, 3, 4, 127, 128, 255):
                    us, rows = damage_tests.fixture(tipo_alvo=kind, vida=1000)
                    self.compare(us, rows, raw, direction)

    def test_original_every_raw_byte_in_both_classes(self):
        for kind in (2, 3):
            for direction in (29, 30):
                for raw in range(256):
                    us, rows = damage_tests.fixture(tipo_alvo=kind, vida=1000)
                    self.compare(us, rows, raw, direction)

    def test_original_reduction_protection_and_life_edges(self):
        for kind in (2, 3):
            for direction in (29, 30):
                for life in (0, 1, 2, 20, 127, 65535):
                    for reduction in (0, 1, 255):
                        for modifier in (0, 1, 255):
                            for protection in (0, 8):
                                us, rows = damage_tests.fixture(tipo_alvo=kind, vida=life)
                                us[1][0xf6], us[1][0xdc] = reduction, protection
                                self.compare(us, rows, 127, direction, mod6=modifier)

    def test_original_id_aliases_and_audio_handles(self):
        for victim in (0, 1, 798, 799):
            for attacker in (0, 799):
                us, rows = damage_tests.fixture(vida=1000)
                source, target = bytes(us[0]), bytes(us[1])
                us[attacker][:], us[victim][:] = source, target
                self.compare(us, rows, victim=victim, attacker=attacker)
        for kind in (0, 2, 12, 25):
            for handle in (0, 1, 0x80000000, 0xfffffffe, 0xffffffff):
                us, rows = damage_tests.fixture(tipo_alvo=kind)
                us[1][0xf9] = 223
                struct.pack_into('<I', us[1], 0x104, handle)
                self.compare(us, rows, visible=True)
