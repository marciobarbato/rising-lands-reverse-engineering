"""Whole 800-slot native scans, original providers and partial-query stops."""
import os
import random
import unittest
from test_capacidades_unidades import (preparar, unidade, BonusUnidades, capacidade_tipo,
                                       atualizar_capacidades_unidades)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialCapacidadesUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_capacidades_unidades import BancadaCapacidadesUnidades
        cls.bancada = BancadaCapacidadesUnidades()

    def comparar(self, m, bonus, dono):
        self.bancada.carregar(m.unidades, bonus.memoria)
        self.bancada.atualizar(dono)
        chamadas = []
        def cap(t):
            chamadas.append(('capacity', t))
            return capacidade_tipo(t)
        def mod(d, t, seletor):
            chamadas.append(('bonus', d, t, seletor))
            return bonus.consultar(d, t, seletor)
        atualizar_capacidades_unidades(m, dono, capacidade_tipo=cap, modificador=mod)
        self.assertEqual(bytes(m.unidades), self.bancada.unidades())
        self.assertEqual(chamadas, self.bancada.consultas)
        self.assertEqual(bytes(bonus.memoria), bytes(self.bancada.cpu.mem_read(0x4dfba0, 1872)))

    def test_all_state_bytes_owner_filters_and_poisoned_bags(self):
        rng = random.Random(0x4475ef)
        for padrao in (0, 255, 0xa5):
            for dono in (0, 1, 2, 3, 4, 200):
                m, _ = preparar()
                m.unidades[:] = bytes([padrao]) * 220800
                bonus = BonusUnidades(bytes(rng.randrange(256) for _ in range(1872)))
                for i in range(800):
                    unidade(m, i, (0, 1, 2, 3, 4, 200)[i % 6], i % 26, i & 255)
                self.comparar(m, bonus, dono)

    def test_all_raw_types_for_neutral_bonus_bypass(self):
        for dono in (4, 200):
            for padrao in (0, 0xa5):
                m, bonus = preparar()
                for tipo in range(256):
                    unidade(m, tipo, dono, tipo, 255, padrao * 257)
                self.comparar(m, bonus, dono)

    def test_owner_argument_all_low_bytes_and_empty_scans(self):
        for dono in range(256):
            m, bonus = preparar()
            unidade(m, 799, 0, 12, 1)
            self.comparar(m, bonus, 0xabcd0000 | dono)

    def test_partial_query_failures_match_native_prior_record_stores(self):
        for indice in (0, 7, 799):
            for consulta, ponto in (('capacity', 0x44762a), ('bonus', 0x44763a)):
                m, bonus = preparar()
                for i in range(800):
                    unidade(m, i, 0, 12, 14)
                bonus.memoria[12*18+11] = 7
                self.bancada.carregar(m.unidades, bonus.memoria)
                self.bancada.atualizar(0, (ponto, indice))
                vistos = -1
                def cap(t):
                    nonlocal vistos
                    vistos += 1
                    if consulta == 'capacity' and vistos == indice:
                        raise NotImplementedError('native capacity checkpoint')
                    return capacidade_tipo(t)
                def mod(d, t, seletor):
                    if consulta == 'bonus' and vistos == indice:
                        raise NotImplementedError('native bonus checkpoint')
                    return bonus.consultar(d, t, seletor)
                with self.assertRaises(NotImplementedError):
                    atualizar_capacidades_unidades(m, 0, capacidade_tipo=cap, modificador=mod)
                self.assertEqual(bytes(m.unidades), self.bancada.unidades())
