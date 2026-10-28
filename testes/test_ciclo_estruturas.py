"""Public structure lifecycle contract, including deliberately retained bytes."""
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from ciclo_estruturas import (inicializar_registros_estruturas, resetar_todas_estruturas,
                             resetar_estrutura, buscar_estrutura_livre)
from navegacao_unidades import MundoNavegacao


def memoria_fixture(padrao=0xa5):
    return bytearray([padrao]) * 276000, bytearray([padrao]) * 88, bytearray([padrao]) * 8


class CicloEstruturas(unittest.TestCase):
    def test_startup_selective_defaults_and_retained_bytes(self):
        r, f, s = memoria_fixture()
        inicializar_registros_estruturas(r, f)
        self.assertEqual(f, bytes(88))
        self.assertEqual(s, b'\xa5' * 8)
        for i in (0, 499, 999):
            p = i * 276
            self.assertEqual(r[p:p+10], b'\xff\xa5\xff\xff\xff\x00\x00\x00\xff\xa5')
            self.assertEqual(r[p+0xc:p+0x74], b'\xa5' * 0x68)  # bag not reset here
            self.assertEqual(r[p+0x90], 1)
            self.assertEqual(r[p+0x100:p+0x104], b'\xff' * 4)
            self.assertEqual(r[p+0x110:p+0x114], bytes(4))

    def test_reset_all_is_distinct_from_startup(self):
        r, f, s = memoria_fixture()
        resetar_todas_estruturas(r, f, s)
        self.assertEqual((f, s), (bytes(88), b'\xff' * 8))
        for i in (0, 499, 999):
            p = i * 276
            self.assertEqual(r[p+2:p+4], b'\xa5' * 2)
            self.assertEqual(r[p+8], 0xa5)
            self.assertEqual(r[p+0x90], 0)
            self.assertEqual(r[p+0x88:p+0x8a], b'\xa5' * 2)
            self.assertEqual(r[p+0x100:p+0x114], b'\xa5' * 20)
            self.assertEqual(struct.unpack_from('<H', r, p+0x84)[0], 200)

    def test_single_reset_keeps_type20_payload_and_state3(self):
        r, _, _ = memoria_fixture()
        p = 999 * 276
        r[p+8], r[p+5] = 20, 3
        resetar_estrutura(r, 0x123403e7)
        self.assertEqual(r[p+0x80:p+0x84], b'\xa5' * 4)
        self.assertEqual(r[p+5], 3)
        self.assertEqual(r[p+0x76], 0xa5)
        self.assertEqual(r[:p], b'\xa5' * p)

    def test_single_reset_other_types_clear_payload_and_change_state(self):
        r, _, _ = memoria_fixture()
        r[8] = 12
        resetar_estrutura(r, 0)
        self.assertEqual(r[5], 5)
        self.assertEqual(r[0x80:0x84], bytes(4))
        self.assertEqual(r[0x7a], 0xa5)
        self.assertEqual(r[0x76], 0xa5)
        self.assertEqual(r[0x8c:0x90], bytes(4))

    def test_free_query_checks_only_state_and_does_not_reserve(self):
        r, _, _ = memoria_fixture(0xff)
        self.assertEqual(buscar_estrutura_livre(r), 0xffff)
        for i in (999, 500, 0):
            r[i*276+5] = 0
            before = bytes(r)
            self.assertEqual(buscar_estrutura_livre(r), i)
            self.assertEqual(buscar_estrutura_livre(r), i)
            self.assertEqual(r, before)

    def test_invalid_model_inputs_fail_before_mutation(self):
        r, f, s = memoria_fixture()
        before = bytes(r)
        for indice in (1000, -1, 0x1234ffff):
            with self.assertRaises(ValueError):
                resetar_estrutura(r, indice)
        with self.assertRaises(ValueError):
            inicializar_registros_estruturas(r, bytearray(87))
        with self.assertRaises(ValueError):
            resetar_todas_estruturas(r, f, bytes(8))
        with self.assertRaises(ValueError):
            buscar_estrutura_livre(bytearray(275999))
        self.assertEqual(r, before)
        self.assertEqual(f, b'\xa5' * 88)
        self.assertEqual(s, b'\xa5' * 8)

    def test_world_adapter_is_explicit_and_has_no_terrain_effects(self):
        m = MundoNavegacao()
        m.estruturas[:] = b'\xa5' * 276000
        m.atributos[0x505] = 0x83
        m.regioes[0x505] = 0x8000
        m.inicializar_registros_estruturas()
        self.assertEqual(m.buscar_estrutura_livre(), 0)
        m.estruturas[5] = 2
        m.resetar_estrutura(0)
        self.assertEqual(m.buscar_estrutura_livre(), 1)
        m.resetar_todas_estruturas()
        self.assertEqual(m.buscar_estrutura_livre(), 0)
        self.assertEqual((m.atributos[0x505], m.regioes[0x505]), (0x83, 0x8000))
