"""Whole-buffer comparisons against original instructions, not copied formulas."""
import os
import random
import unittest
from test_ciclo_estruturas import memoria_fixture
from ciclo_estruturas import (inicializar_registros_estruturas, resetar_todas_estruturas,
                             resetar_estrutura, buscar_estrutura_livre)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialCicloEstruturas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_ciclo_estruturas import BancadaCicloEstruturas
        cls.bancada = BancadaCicloEstruturas()

    def conferir(self, r, f, s):
        self.assertEqual(self.bancada.ler(), (bytes(r), bytes(f), bytes(s)))

    def fixtures(self):
        for padrao in (0, 0xff, 0xa5):
            yield memoria_fixture(padrao)
        rng = random.Random(0x418e95)
        for _ in range(3):
            yield tuple(bytearray(rng.getrandbits(8) for _ in range(n)) for n in (276000, 88, 8))

    def test_startup_full_pool_and_untouched_globals(self):
        for r, f, s in self.fixtures():
            self.bancada.carregar(r, f, s)
            self.bancada.inicializar()
            inicializar_registros_estruturas(r, f)
            self.conferir(r, f, s)

    def test_reset_all_full_pool_and_global_tables(self):
        for r, f, s in self.fixtures():
            self.bancada.carregar(r, f, s)
            self.bancada.resetar_todas()
            resetar_todas_estruturas(r, f, s)
            self.conferir(r, f, s)

    def test_single_reset_types_states_and_index_width(self):
        r, f, s = memoria_fixture()
        for indice in (0, 499, 999):
            for tipo in tuple(range(22)) + (22, 127, 254, 255):
                for estado in (0, 1, 2, 3, 4, 5, 200, 255):
                    p = indice * 276
                    r[p:p+276] = bytes((i * 37 + estado + tipo) & 255 for i in range(276))
                    r[p+8], r[p+5] = tipo, estado
                    self.bancada.carregar(r, f, s)
                    entrada = 0xbeef0000 | indice
                    self.bancada.resetar(entrada)
                    resetar_estrutura(r, entrada)
                    self.conferir(r, f, s)

    def test_first_free_scan_full_and_sparse_without_mutation(self):
        for livres in ((), (0,), (999,), (499,), (999, 1, 500), (998, 999), (0, 1, 999)):
            r, f, s = memoria_fixture(0xff)
            for indice in livres:
                r[indice*276+5] = 0
            self.bancada.carregar(r, f, s)
            self.assertEqual(self.bancada.buscar_livre(), buscar_estrutura_livre(r))
            self.conferir(r, f, s)

    def test_original_lifecycle_sequence(self):
        r, f, s = memoria_fixture(0x77)
        self.bancada.carregar(r, f, s)
        self.bancada.inicializar()
        inicializar_registros_estruturas(r, f)
        for tipo, estado in ((20, 3), (12, 15), (9, 1)):
            r[8], r[5] = tipo, estado
            self.bancada.carregar(r, f, s)
            self.bancada.resetar(0)
            resetar_estrutura(r, 0)
            self.conferir(r, f, s)
        self.bancada.resetar_todas()
        resetar_todas_estruturas(r, f, s)
        self.conferir(r, f, s)
