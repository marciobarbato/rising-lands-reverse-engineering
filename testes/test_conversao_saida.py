"""Shared conversion, pending handoff, and partial live-state failures."""
from dataclasses import dataclass
import struct
import sys
from pathlib import Path
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from conversao_unidades import converter_unidade, retomar_conversao_saida
from ordens_unidades import MundoUnidades, ContextoBusca

# Explicit original-capacity query fixture, not a second economic provider.
CAPACIDADES = {5: 1, 6: 1, 7: 1, 11: 1, 12: 2, 13: 5, 14: 1, 15: 3, 16: 1, 17: 6}


def tipos_fixture():
    tipos = bytearray(1300)
    for tipo in range(26):
        for off, valor in ((0, 10), (0x2a, 0x105 + tipo), (0x2c, 0x224 + tipo), (0x30, 0x178 + tipo)):
            struct.pack_into('<H', tipos, tipo * 50 + off, valor)
    return tipos


@dataclass(frozen=True)
class PedidoFixture:
    indice: int = 7
    direcao: int = 9
    unidade: int = 799
    tipo_unidade: int = 25  # deliberately stale diagnostic snapshot
    endereco_dependencia: int = 0x420698


def preparar(tipo=7, dono=0, estado=14, indice=799):
    m = MundoUnidades()
    m.unidades[:] = b'\xa5' * 220800
    p = indice * 276
    m.unidades[p], m.unidades[p+1], m.unidades[p+2] = dono, 9, estado
    m.busca = ContextoBusca(indice, 1, 1, 0x12345678, 77)
    s = 7 * 276
    struct.pack_into('<H', m.estruturas, s+2, 0x505)
    m.estruturas[s+8], m.estruturas[s+0x7b] = 1, tipo
    return m, tipos_fixture()


def estado_compartilhado(m):
    b = m.busca
    return (bytes(m.unidades), bytes(m.estruturas),
            (b.unidade, b.ocupada, b.sucesso, b.ponteiro_rota, b.concluida))


class ConversaoSaida(unittest.TestCase):
    def test_live_record_and_core_search_release_preserve_completion_flag(self):
        m, tipos = preparar()
        antes = bytes(m.unidades)
        m.converter_unidade(0xabcd031f, 0x12340808, 0x109, 0x107, tipos,
                           capacidade_tipo=lambda t: CAPACIDADES.get(t, 0), modificador=lambda *args: 0)
        p = 799 * 276
        self.assertEqual(m.unidades[:p], antes[:p])
        self.assertEqual(tuple(struct.unpack_from('<H', m.unidades, p+o)[0] for o in (8, 0x7c, 0x7e)), (0x808,) * 3)
        self.assertEqual((m.unidades[p+1], m.unidades[p+2], m.unidades[p+0x8a], m.unidades[p+0x8b]), (7, 7, 0xa5, 0))
        self.assertEqual(estado_compartilhado(m)[2], (65535, 0, 0, 0, 77))

    def test_inactive_states_and_other_search_are_preserved(self):
        for estado in (0, 4):
            m, tipos = preparar(estado=estado)
            m.busca.unidade = 0
            converter_unidade(m, 799, 0x808, 9, 7, tipos,
                             capacidade_tipo=lambda t: 1, modificador=lambda *args: 0)
            self.assertEqual(m.unidades[799*276+2], estado)
            self.assertEqual(estado_compartilhado(m)[2], (0, 1, 1, 0x12345678, 77))

    def test_query_order_observes_live_mutations_and_original_bag(self):
        m, tipos = preparar(tipo=4)
        p = 799 * 276
        chamadas = []
        def capacidade(tipo):
            chamadas.append(('capacity', tipo))
            self.assertEqual((m.unidades[p+1], m.unidades[p+2]), (4, 7))
            self.assertEqual(m.unidades[p+0xa:p+0x72], b'\xa5' * 104)
            return 6
        def bonus(dono, tipo, seletor):
            chamadas.append(('bonus', dono, tipo, seletor))
            self.assertEqual(m.busca.unidade, 65535)
            return 250 if seletor == 12 else 255
        converter_unidade(m, 799, 0x808, 9, 4, tipos, capacidade_tipo=capacidade, modificador=bonus)
        self.assertEqual(chamadas, [('bonus', 0, 4, 12), ('capacity', 4), ('bonus', 0, 4, 1)])
        self.assertEqual(struct.unpack_from('<H', m.unidades, p+0xc)[0], 261)
        self.assertEqual(m.unidades[p+0xda], 4)

    def test_missing_queries_retain_prior_live_effects(self):
        for ausente in ('capacity', 'bonus'):
            m, tipos = preparar()
            p = 799 * 276
            with self.assertRaises(NotImplementedError):
                converter_unidade(m, 799, 0x808, 9, 7, tipos,
                                 capacidade_tipo=None if ausente == 'capacity' else lambda t: 1,
                                 modificador=None)
            self.assertEqual((m.unidades[p+1], m.unidades[p+2]), (7, 7))
            self.assertEqual(m.busca.unidade, 65535)
            self.assertEqual(m.unidades[p+0xa:p+0x72], b'\xa5' * 104)

    def test_special_owners_bypass_bonus_queries(self):
        for dono in (4, 200):
            m, tipos = preparar(tipo=4, dono=dono)
            converter_unidade(m, 799, 0x808, 9, 4, tipos, capacidade_tipo=lambda t: 0)
            self.assertEqual(m.unidades[799*276+0xda], 10)

    def test_pending_resume_reloads_type_and_stops_before_healing(self):
        m, tipos = preparar(tipo=7)
        p = 799 * 276
        antes = struct.unpack_from('<H', m.unidades, p+0x9a)[0]
        resultado = retomar_conversao_saida(m, PedidoFixture(), tipos,
                                          capacidade_tipo=lambda t: 1, modificador=lambda *args: 0)
        self.assertEqual((resultado.indice, resultado.unidade, resultado.celula, resultado.tipo_unidade), (7, 799, 0x808, 7))
        self.assertEqual(resultado.endereco_dependencia, 0x420f6e)
        self.assertEqual(struct.unpack_from('<H', m.unidades, p+0x9a)[0], antes)

    def test_protected_errors_precede_mutation(self):
        m, tipos = preparar()
        antes = estado_compartilhado(m)
        for indice, tipo, tabela in ((800, 7, tipos), (-1, 7, tipos), (0, 26, tipos), (0, 7, bytes(1299))):
            with self.assertRaises(ValueError):
                converter_unidade(m, indice, 0x808, 9, tipo, tabela)
        self.assertEqual(estado_compartilhado(m), antes)

    def test_committed_economy_preparation_bonus_queries_and_conversion_join(self):
        from demonstrar_saida_tropa import demonstrar
        exemplo = demonstrar()
        self.assertTrue(exemplo['shares_unit_and_structure_buffers'])
        self.assertFalse(exemplo['x86_executed'])
        antes, depois = exemplo['events']
        self.assertEqual((antes['unit_type'], antes['balance']), (9, [1, 2, 0, 0]))
        self.assertEqual((depois['unit_type'], depois['cell'], depois['life']), (7, 0x808, 50))
        self.assertEqual((depois['bag_count'], depois['bag_capacity']), (0, 1))
        self.assertEqual(depois['pending_address'], '0x420f6e')
