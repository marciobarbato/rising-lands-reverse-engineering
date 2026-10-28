"""Original half-life byte truncation, reduction and explicit lethal boundary."""
import os
import struct
import unittest

from consumo_dano import LimiteMorte
from projeteis import u16
import test_consumo_dano as damage_tests
import test_dano_modo8 as special_tests


class ContratosDanoModo9(unittest.TestCase):
    def test_life_half_is_truncated_before_zero_to_one(self):
        for life, remaining in ((0, None), (1, None), (2, 1), (255, 128),
                                (256, 255), (511, 510), (512, 511), (514, 513),
                                (65535, 65534)):
            us, rows = damage_tests.fixture(vida=life)
            c, calls = damage_tests.local(us, rows)
            if remaining is None:
                with self.assertRaises(LimiteMorte) as caught:
                    c.infligir(1, 0x109, 0)
                self.assertEqual(caught.exception.modo, 9)
                self.assertEqual(u16(us[1], 0x9a), life)
            else:
                c.infligir(1, 9, 0)
                self.assertEqual(u16(us[1], 0x9a), remaining)
            self.assertEqual([name for name, _ in calls], ['Modificateur', 'TerrainEstDecouvert'])

    def test_mode1_lethal_handler_is_not_called_for_mode9(self):
        us, rows = damage_tests.fixture(vida=1)
        c, _ = damage_tests.local(us, rows)
        c.morte = lambda *args: self.fail('Mode-1 death handler must not run')
        with self.assertRaises(LimiteMorte) as caught:
            c.infligir(1, 9, 0)
        self.assertEqual((caught.exception.modo, u16(us[1], 0x9a)), (9, 1))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialDanoModo9(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_dano import BancadaConsumoDano
        cls.b = BancadaConsumoDano()
        cls.complete_returns = cls.death_stops = cls.audio_stops = 0

    def compare(self, us, rows, **kwargs):
        return special_tests.DiferencialDanoModo8.compare(self, us, rows, None, mode=9, **kwargs)

    def test_original_all_raw_damage_bytes_at_multiple_life_bands(self):
        for base in (0, 512, 32768, 65024):
            for offset in range(512):
                us, rows = damage_tests.fixture(vida=base+offset)
                us[0][0xf7] = 255
                self.compare(us, rows)

    def test_original_reduction_protection_and_life_edges(self):
        for life in (0, 1, 2, 3, 254, 255, 256, 511, 512, 513, 65534, 65535):
            for reduction in (0, 1, 255):
                for modifier in (0, 1, 255):
                    for protection in (0, 8):
                        us, rows = damage_tests.fixture(vida=life)
                        us[1][0xf6], us[1][0xdc] = reduction, protection
                        self.compare(us, rows, mod6=modifier)

    def test_original_sources_targets_and_aliased_ids(self):
        for source in range(26):
            for target in (0, 2, 12, 25):
                us, rows = damage_tests.fixture(tipo_fonte=source, tipo_alvo=target, vida=1000)
                self.compare(us, rows, mod6=17)
        for victim in (0, 1, 798, 799):
            for attacker in (0, 799):
                us, rows = damage_tests.fixture(vida=1000)
                source, target = bytes(us[0]), bytes(us[1])
                us[attacker][:], us[victim][:] = source, target
                self.compare(us, rows, victim=victim, attacker=attacker)

    def test_original_visible_audio_and_existing_handles(self):
        for kind in (0, 2, 12, 25):
            for handle in (0, 1, 0x80000000, 0xfffffffe, 0xffffffff):
                us, rows = damage_tests.fixture(tipo_alvo=kind)
                us[1][0xf9] = 223
                struct.pack_into('<I', us[1], 0x104, handle)
                self.compare(us, rows, visible=True)
