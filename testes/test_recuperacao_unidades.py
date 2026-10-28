"""Live recovery contracts, protected inputs and joined economic handoff."""
from dataclasses import replace
import struct
import unittest

from test_conversao_saida import preparar, estado_compartilhado
from conversao_unidades import ConversaoSaidaTropa, retomar_conversao_saida
from recuperacao_unidades import (adicionar_vida_unidade, resetar_fadiga_unidade,
                                  retomar_recuperacao_saida)


def maximo(tipos, tipo, valor):
    struct.pack_into('<H', tipos, tipo*50+8, valor)


class RecuperacaoUnidades(unittest.TestCase):
    def test_healing_strict_clamp_wrap_and_only_life_writes(self):
        m, tipos = preparar()
        p = 799*276
        m.unidades[p+1] = 7
        maximo(tipos, 7, 100)
        for vida, incremento, final, flag in ((80, 19, 99, False), (80, 20, 100, False),
                                             (80, 21, 100, True), (65535, 1, 0, False),
                                             (80, -1, 79, False), (0, 0x10064, 100, False)):
            m.palavra(799, 0x9a, vida)
            antes = bytearray(m.unidades)
            self.assertIs(m.adicionar_vida_unidade(0xabcd031f, incremento, tipos), flag)
            struct.pack_into('<H', antes, p+0x9a, final)
            self.assertEqual(m.unidades, antes)

    def test_no_activity_owner_or_life_guard(self):
        m, tipos = preparar()
        p = 799*276
        m.unidades[p+1] = 7
        maximo(tipos, 7, 65535)
        for estado in (0, 4, 7, 255):
            m.unidades[p], m.unidades[p+2] = 200, estado
            m.palavra(799, 0x9a, 0)
            self.assertFalse(adicionar_vida_unidade(m, 799, 1, tipos))
            self.assertEqual(m.palavra(799, 0x9a), 1)

    def test_fatigue_copies_word_and_ignores_unknown_type(self):
        m, _ = preparar()
        p = 799*276
        m.unidades[p+1] = 255
        m.palavra(799, 0x76, 0xabcd)
        antes = bytearray(m.unidades)
        self.assertIsNone(m.resetar_fadiga_unidade(0xabcd031f))
        struct.pack_into('<H', antes, p+0x74, 0)
        struct.pack_into('<H', antes, p+4, 0xabcd)
        self.assertEqual(m.unidades, antes)

    def test_continuation_uses_live_type_and_preserves_exit_metadata(self):
        m, tipos = preparar()
        p = 799*276
        m.unidades[p+1] = 8
        m.palavra(799, 0x9a, 50)
        m.palavra(799, 0x76, 0xbeef)
        maximo(tipos, 8, 1500)
        maximo(tipos, 7, 1)
        pedido = ConversaoSaidaTropa(0x10007, 0xabcd031f, 0x12340808, 7)
        r = retomar_recuperacao_saida(m, pedido, tipos)
        self.assertEqual((r.indice, r.unidade, r.celula, r.tipo_unidade, r.endereco_dependencia),
                         (7, 799, 0x808, 8, 0x420f81))
        self.assertEqual((m.palavra(799, 0x9a), m.palavra(799, 0x74), m.palavra(799, 4)),
                         (1050, 0, 0xbeef))

    def test_bad_handoff_and_protected_inputs_fail_before_mutation(self):
        m, tipos = preparar()
        m.unidades[799*276+1] = 7
        antes = estado_compartilhado(m)
        for indice, tabela in ((800, tipos), (-1, tipos), (799, bytes(1299)), (799, [0]*1300)):
            with self.assertRaises(ValueError):
                adicionar_vida_unidade(m, indice, 1000, tabela)
        for indice in (800, -1):
            with self.assertRaises(ValueError):
                resetar_fadiga_unidade(m, indice)
        with self.assertRaises(ValueError):
            retomar_recuperacao_saida(m, replace(ConversaoSaidaTropa(7, 799, 0x808, 7),
                                                endereco_dependencia=0x420f81), tipos)
        self.assertEqual(estado_compartilhado(m), antes)
        m.unidades[799*276+1] = 26
        antes = estado_compartilhado(m)
        with self.assertRaises(ValueError):
            retomar_recuperacao_saida(m, ConversaoSaidaTropa(7, 799, 0x808, 7), tipos)
        self.assertEqual(estado_compartilhado(m), antes)

    def test_committed_economy_conversion_and_recovery_share_buffers(self):
        from demonstrar_recuperacao_saida import demonstrar
        d = demonstrar()
        self.assertTrue(d['shares_unit_and_structure_buffers'])
        self.assertFalse(d['x86_executed'])
        self.assertEqual((d['life_before'], d['life_after'], d['fatigue_after'], d['copied_word']),
                         (50, 100, 0, 4))  # conversion sets the current +0x76 word
        self.assertEqual(d['pending_address'], '0x420f81')
