"""Existing-unit Bag-capacity refresh with real committed economic queries."""
import struct
import sys
from pathlib import Path
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from capacidades_unidades import atualizar_capacidades_unidades
from ordens_unidades import MundoUnidades
from demonstrar_saida_tropa import BonusUnidades, capacidade_tipo


def preparar():
    m = MundoUnidades()
    m.unidades[:] = b'\xa5' * 220800
    # Most slots inactive, with poisoned owners/types/Bags preserved.
    for indice in range(800):
        m.unidades[indice*276+2] = 0
    return m, BonusUnidades(bytes(1872))


def unidade(m, indice, dono, tipo, estado, capacidade=0xa5a5):
    p = indice*276
    m.unidades[p], m.unidades[p+1], m.unidades[p+2] = dono, tipo, estado
    struct.pack_into('<HH', m.unidades, p+0xa, 30, capacidade)


class CapacidadesUnidades(unittest.TestCase):
    def test_only_active_owner_capacity_word_changes_even_below_count(self):
        m, bonus = preparar()
        for i, estado in enumerate((0, 1, 4, 14, 255)):
            unidade(m, i, 2, 12, estado)
        unidade(m, 799, 3, 12, 1)
        bonus.memoria[2*468+12*18+11] = 7
        antes = bytes(m.unidades)
        m.atualizar_capacidades_unidades(0x12340102, capacidade_tipo=capacidade_tipo,
                                        modificador=bonus.consultar)
        diferentes = {i for i, (a, b) in enumerate(zip(antes, m.unidades)) if a != b}
        self.assertEqual(diferentes, {i*276+o for i in (1, 3, 4) for o in (0xc, 0xd)})
        for i in (1, 3, 4):
            self.assertEqual(struct.unpack_from('<HH', m.unidades, i*276+0xa), (30, 9))
            self.assertEqual(m.unidades[i*276+0x10:i*276+0x72], antes[i*276+0x10:i*276+0x72])

    def test_no_eligible_units_needs_no_query_provider(self):
        m, _ = preparar()
        antes = bytes(m.unidades)
        self.assertIsNone(atualizar_capacidades_unidades(m, 255))
        self.assertEqual(m.unidades, antes)

    def test_neutral_owner_still_calls_bonus_for_raw_type(self):
        for dono in (4, 200):
            m, bonus = preparar()
            unidade(m, 799, dono, 255, 255)
            chamadas = []
            def capacidade(t):
                chamadas.append(('capacity', t))
                return capacidade_tipo(t)
            def mod(d, t, seletor):
                chamadas.append(('bonus', d, t, seletor))
                return bonus.consultar(d, t, seletor)
            atualizar_capacidades_unidades(m, dono, capacidade_tipo=capacidade, modificador=mod)
            self.assertEqual(chamadas, [('capacity', 255), ('bonus', dono, 255, 1)])
            self.assertEqual(struct.unpack_from('<HH', m.unidades, 799*276+0xa), (30, 0))

    def test_query_order_and_later_failure_preserve_earlier_capacity(self):
        m, bonus = preparar()
        unidade(m, 1, 0, 7, 14)
        unidade(m, 7, 0, 12, 14)
        chamadas = []
        def capacidade(t):
            chamadas.append(('capacity', t))
            return capacidade_tipo(t)
        def mod(d, t, seletor):
            chamadas.append(('bonus', d, t, seletor))
            if t == 12:
                raise NotImplementedError('provider stop')
            return bonus.consultar(d, t, seletor)
        with self.assertRaises(NotImplementedError):
            atualizar_capacidades_unidades(m, 0, capacidade_tipo=capacidade, modificador=mod)
        self.assertEqual(chamadas, [('capacity', 7), ('bonus', 0, 7, 1),
                                    ('capacity', 12), ('bonus', 0, 12, 1)])
        self.assertEqual(struct.unpack_from('<H', m.unidades, 276+0xc)[0], 1)
        self.assertEqual(struct.unpack_from('<H', m.unidades, 7*276+0xc)[0], 0xa5a5)

    def test_missing_queries_at_first_unit_do_not_store_capacity(self):
        m, _ = preparar()
        unidade(m, 0, 0, 12, 1)
        antes = bytes(m.unidades)
        for cap in (None, capacidade_tipo):
            with self.assertRaises(NotImplementedError):
                atualizar_capacidades_unidades(m, 0, capacidade_tipo=cap)
            self.assertEqual(m.unidades, antes)

    def test_invalid_pool_is_rejected_before_query_or_mutation(self):
        m, _ = preparar()
        m.unidades = bytes(m.unidades)
        with self.assertRaises(ValueError):
            atualizar_capacidades_unidades(m, 0)
