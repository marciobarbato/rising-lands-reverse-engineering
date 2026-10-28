"""Experience queue local effects, ordered failure and handoff contracts."""
from dataclasses import replace
import struct
import unittest

from test_recuperacao_unidades import preparar, maximo
from test_conversao_saida import estado_compartilhado, PedidoFixture
from recuperacao_unidades import RecuperacaoSaidaTropa, retomar_recuperacao_saida
from conversao_unidades import retomar_conversao_saida
from experiencia_unidades import (aplicar_nova_experiencia, consumir_experiencia_unidade,
                                  retomar_experiencia_saida, DependenciaExperienciaUnidade)


def estado(m):
    return estado_compartilhado(m) + (bytes(m.experiencias_unidades),)


def fila(m, dono, tipo, experiencia):
    m.experiencias_unidades[dono*10:dono*10+10] = bytes((tipo, experiencia, 9, 3, 8, 4, 7, 5, 6, 6))


def fadiga(tipos, tipo, valor):
    struct.pack_into('<H', tipos, tipo*50+0x2e, valor)


class ExperienciaUnidades(unittest.TestCase):
    def test_local_effects_preserve_af_and_other_flags_and_double_before_division(self):
        m, tipos = preparar()
        p = 799*276
        m.unidades[p+1] = 4
        fadiga(tipos, 4, 65535)
        antes_af = m.unidades[p+0xaf]
        aplicar_nova_experiencia(m, 799, 4, tipos)
        self.assertEqual(m.unidades[p+0xf8], 30)  # floor(2*65535/100), low byte
        for nivel, off in ((2, 0xf6), (3, 0xf5)):
            self.assertIsNone(m.aplicar_nova_experiencia(0xabcd031f, nivel))
            self.assertEqual(m.unidades[p+off], 1)
        m.unidades[p+1] = 25
        m.aplicar_nova_experiencia(799, 0x101)
        self.assertEqual((m.unidades[p+0xf7], m.unidades[p+0xaf]), (1, antes_af))

    def test_queue_owner_isolation_exact_pairs_and_unknown_type_table_free_path(self):
        for dono in range(4):
            m, _ = preparar(dono=dono, estado=0)
            m.unidades[799*276+1] = 255
            fila(m, dono, 255, 65)
            antes = bytearray(m.experiencias_unidades)
            m.consumir_experiencia_unidade(799)
            antes[dono*10:dono*10+10] = bytes((9, 3, 8, 4, 7, 5, 6, 6, 255, 0))
            self.assertEqual(m.experiencias_unidades, antes)
            self.assertEqual((m.unidades[799*276+0xaf], m.unidades[799*276+0xf6]), (65, 1))

    def test_missing_type_data_retains_af_before_queue_shift(self):
        m, _ = preparar()
        m.unidades[799*276+1] = 4
        fila(m, 0, 4, 0x81)
        antes = estado(m)
        with self.assertRaises(DependenciaExperienciaUnidade) as captura:
            consumir_experiencia_unidade(m, 799)
        self.assertEqual((captura.exception.unidade, captura.exception.nivel, captura.exception.endereco),
                         (799, 4, 0x44fafa))
        esperado = bytearray(antes[0]); esperado[799*276+0xaf] = 0x81
        self.assertEqual(estado(m), (bytes(esperado),) + antes[1:])

    def test_first_zero_or_mismatch_does_not_search_later_pairs(self):
        for primeiro_tipo, experiencia in ((255, 0), (7, 255)):
            m, _ = preparar(estado=4)
            m.unidades[799*276+1] = 255
            fila(m, 0, primeiro_tipo, experiencia)
            m.experiencias_unidades[2:4] = bytes((255, 97))
            antes = estado(m)
            consumir_experiencia_unidade(m, 799)
            self.assertEqual(estado(m), antes)

    def test_continuation_preserves_cell_and_rejects_wrong_checkpoint(self):
        m, _ = preparar()
        pedido = RecuperacaoSaidaTropa(0x10007, 0xabcd031f, 0x12340808, 4)
        antes = estado(m)
        with self.assertRaises(ValueError):
            retomar_experiencia_saida(m, replace(pedido, endereco_dependencia=0x420f6e))
        self.assertEqual(estado(m), antes)
        r = retomar_experiencia_saida(m, pedido)
        self.assertEqual((r.indice, r.unidade, r.celula, r.tipo_unidade, r.endereco_dependencia),
                         (7, 799, 0x808, 9, 0x420f8a))

    def test_protected_owner_index_and_table_fail_at_declared_points(self):
        m, _ = preparar(dono=4)
        antes = estado(m)
        for indice in (800, -1, 799):
            with self.assertRaises(ValueError):
                consumir_experiencia_unidade(m, indice)
        self.assertEqual(estado(m), antes)
        m.unidades[799*276], m.unidades[799*276+1] = 0, 4
        fila(m, 0, 4, 33)
        with self.assertRaises(ValueError):
            consumir_experiencia_unidade(m, 799, bytes(1299))
        self.assertEqual(m.unidades[799*276+0xaf], 33)
        self.assertEqual(m.experiencias_unidades[:2], bytes((4, 33)))

    def test_synthetic_queue_demo(self):
        from demonstrar_experiencia_saida import demonstrar
        d = demonstrar()
        self.assertFalse(d['x86_executed'])
        self.assertEqual((d['experience_byte'], d['f8'], d['pending_address']), (0x81, 30, '0x420f8a'))
        self.assertEqual(d['queue_after'], [9, 3, 8, 4, 7, 5, 6, 6, 255, 0])
