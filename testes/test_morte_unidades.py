"""Supported physical dying transition and truthful dependency boundaries."""
import struct
import sys
from pathlib import Path
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca
from morte_unidades import iniciar_morte_unidade, DependenciaMorteUnidade


def preparar(tipo=1, indice=7, estado=7, *, dono=0, atual=0x505, passo=0x506):
    m = MundoNavegacao()
    m.regioes[:] = [1] * 65536
    p = indice*276
    m.unidades[p:p+276] = b'\xa5' * 276
    m.unidades[p], m.unidades[p+1], m.unidades[p+2] = dono, tipo, estado
    m.unidades[p+0xbd], m.unidades[p+0xdc] = 0, 0
    for off, valor in ((8, atual), (0x7c, passo), (0xa, 0), (0x9a, 123)):
        struct.pack_into('<H', m.unidades, p+off, valor)
    struct.pack_into('<I', m.unidades, p+0x104, 0xffffffff)
    struct.pack_into('<I', m.unidades, p+0x10c, 0xffffffff)
    m.busca = ContextoBusca(indice, 1, 1, 0x12345678, 77)
    m.mini_unidades[atual] = 42
    m.ocupar(indice, atual, True)
    m.ocupar(indice, passo, True)
    return m


class MorteUnidades(unittest.TestCase):
    def test_complete_transition_frees_current_and_reserved_cell_without_zeroing_life(self):
        m = preparar()
        p = 7*276
        self.assertEqual((m.regioes[0x505], m.regioes[0x506]), (0x4038, 0x4038))
        m.iniciar_morte_unidade(0xabcd0007)
        self.assertEqual((m.unidades[p+2], m.unidades[p+0xa4]), (4, 0))
        self.assertEqual(struct.unpack_from('<H', m.unidades, p+0xc2)[0], 0)
        self.assertEqual(struct.unpack_from('<H', m.unidades, p+0x9a)[0], 123)
        self.assertEqual((m.regioes[0x505], m.regioes[0x506]), (1, 1))
        self.assertEqual((m.atributos[0x505], m.atributos[0x506]), (0, 0))
        self.assertEqual((m.busca.unidade, m.busca.ocupada, m.busca.sucesso,
                          m.busca.ponteiro_rota, m.busca.concluida), (65535, 0, 0, 0, 77))
        self.assertEqual(m.mini_unidades[0x505], 42)
        self.assertEqual(m.unidades[p+0x8a:p+0x8c], b'\xa5\xa5')

    def test_inactive_without_special_bit_is_noop_even_with_unresolved_fields(self):
        for estado in (0, 4):
            m = preparar(estado=estado)
            p = 7*276
            m.unidades[p+1] = 255  # type is not consulted by the inactive guard
            m.unidades[p+0xbd] = 1
            struct.pack_into('<H', m.unidades, p+0xa, 1)
            antes = bytes(m.unidades), bytes(m.atributos), list(m.regioes)
            iniciar_morte_unidade(m, 7)
            self.assertEqual((bytes(m.unidades), bytes(m.atributos), m.regioes), antes)

    def test_bag_stop_keeps_state_change_and_search_release_before_collision_removal(self):
        m = preparar()
        struct.pack_into('<H', m.unidades, 7*276+0xa, 1)
        with self.assertRaises(DependenciaMorteUnidade) as caught:
            iniciar_morte_unidade(m, 7)
        self.assertEqual(caught.exception.endereco, 0x443dfc)
        self.assertEqual((m.unidades[7*276+2], m.busca.unidade), (4, 65535))
        self.assertEqual(m.unidades[7*276+0xa4], 0xa5)
        self.assertEqual(m.regioes[0x505], 0x4038)

    def test_selection_stop_clears_flag_after_local_reset_but_retains_collision(self):
        m = preparar()
        m.unidades[7*276+0xbd] = 255
        with self.assertRaises(DependenciaMorteUnidade) as caught:
            iniciar_morte_unidade(m, 7)
        self.assertEqual(caught.exception.endereco, 0x472576)
        self.assertEqual((m.unidades[7*276+2], m.unidades[7*276+0xbd], m.unidades[7*276+0xa4]), (4, 0, 0))
        self.assertEqual(m.regioes[0x505], 0x4038)

    def test_human_control_bypasses_group_effect_without_touching_group(self):
        m = preparar()
        m.controle_jogadores[0] = 0
        struct.pack_into('<I', m.unidades, 7*276+0x10c, 0)
        antes = bytes(m.grupos)
        iniciar_morte_unidade(m, 7)
        self.assertEqual(m.unidades[7*276+2], 4)
        self.assertEqual(m.grupos, antes)

    def test_unsupported_guard_dependencies_precede_record_changes(self):
        for variante, endereco in (('special', 0x444c7e), ('group', 0x4829c8),
                                    ('sound', 0x48aac0), ('visible', 0x440c5d)):
            m = preparar()
            p = 7*276
            if variante == 'special': m.unidades[p+0xdc] = 4
            elif variante == 'group': struct.pack_into('<I', m.unidades, p+0x10c, 0)
            elif variante == 'sound': struct.pack_into('<I', m.unidades, p+0x104, 0)
            else: m.descoberto[0][0x505] = 0
            antes = bytes(m.unidades), bytes(m.atributos), list(m.regioes)
            with self.assertRaises(DependenciaMorteUnidade) as caught:
                iniciar_morte_unidade(m, 7)
            self.assertEqual(caught.exception.endereco, endereco)
            self.assertEqual((bytes(m.unidades), bytes(m.atributos), m.regioes), antes)
