"""Opt-in mode-3/4 original lethal tails sharing actual Core physical state."""
import os
import struct
import unittest

from consumo_fisico import criar_consumidor_fisico
from consumo_dano import LimiteMorte
from fonte_batiment import ConsultaFonteBatiment
from projeteis import u16
import test_consumo_fisico as world_tests


class ContratosMorteSemExperiencia(unittest.TestCase):
    def test_factory_preserves_mode3_mode4_stop_without_new_opt_in(self):
        for mode in (3, 4):
            w, rows, pool = world_tests.fixture()
            w.unidades[1] = 0
            w.estruturas[4], w.estruturas[8] = 3, 10
            c = criar_consumidor_fisico(w, pool, rows,
                efeito=lambda n, a: world_tests.fixture_message(w, n, a))
            c.danos_modo4 = bytes([127, 124])
            c.consulta = world_tests.queries(w, c.unidades)
            if mode == 3:
                c.consulta = ConsultaFonteBatiment(w.estruturas, bytes([127]*26), bytes([124]*26), c.consulta)
            with self.assertRaises(LimiteMorte) as caught:
                c.infligir(1, mode, 0, 29)
            self.assertEqual((caught.exception.modo, u16(c.unidades[1], 0x9a), c.unidades[1][2]), (mode, 1, 6))
            self.assertIsNone(c.morte_sem_experiencia)

    def test_undefined_owner_modes8_mode9_remain_stops_with_opt_in(self):
        for mode in (8, 9):
            w, rows, pool = world_tests.fixture()
            c = criar_consumidor_fisico(w, pool, rows+[bytes([127]*26)],
                                        mortes_sem_experiencia=True)
            c.consulta = world_tests.queries(w, c.unidades)
            with self.assertRaises(LimiteMorte) as caught:
                c.infligir(1, mode, 0)
            self.assertEqual((caught.exception.modo, u16(c.unidades[1], 0x9a), c.unidades[1][2]), (mode, 1, 6))
            self.assertIsNotNone(c.morte_sem_experiencia)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialMorteSemExperiencia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_consumo_fisico import BancadaConsumoFisico
        cls.b = BancadaConsumoFisico()
        cls.complete_consumers = cls.complete_projectiles = cls.sympathy_stops = 0
        cls.physical_stops = {}

    def compare(self, **kwargs):
        return world_tests.DiferencialConsumoFisico.compare(self, **kwargs)

    def test_original_ordinary_modes3_mode4_current_reserved_cells(self):
        for mode in (3, 4):
            for kind in [*range(11), *range(18, 26)]:
                for step in (0x505, 0x506):
                    for stop in (False, True):
                        self.compare(mode=mode, direction=29, kind=kind, step=step, sympathy_stop=stop)
        for kind in (1, 3, 25):
            for stop in (False, True):
                self.compare(mode=4, direction=30, kind=kind, sympathy_stop=stop)
                self.compare(mode=3, source_kind=11, kind=kind, sympathy_stop=stop)

    def test_original_physical_partial_failures_keep_life_child_and_cleanup(self):
        cases = [
            (2, 0x444c7e, lambda w: w.unidades.__setitem__(276+0xdc, 4)),
            (2, 0x48a446, lambda w: struct.pack_into('<I', w.unidades, 276+0x104, 123)),
            (1, 0x443dfc, lambda w: struct.pack_into('<H', w.unidades, 276+0xa, 1)),
            (1, 0x472683, lambda w: w.unidades.__setitem__(276+0xbd, 1)),
        ]
        cases.extend((kind, 0x46e44c if kind == 16 else 0x4704dc, None) for kind in range(11, 18))
        for mode in (3, 4):
            for kind, checkpoint, prepare in cases:
                self.compare(mode=mode, direction=29, kind=kind, checkpoint=checkpoint, prepare=prepare)

    def test_original_child_pool_saturation_and_id_edges(self):
        for mode in (3, 4):
            for victim, attacker in ((1, 0), (799, 798), (0, 799)):
                for full in (False, True):
                    self.compare(mode=mode, direction=29, kind=1, victim=victim, attacker=attacker, full=full)

    def test_original_inactive_physical_guards_without_experience(self):
        for mode in (3, 4):
            for state in (0, 4):
                self.compare(mode=mode, direction=29, state=state)
