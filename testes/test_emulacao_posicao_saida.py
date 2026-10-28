"""Complete original CalculPosition over directions, dimensions and u16 edges."""
import os
import random
import struct
import unittest
from test_posicao_saida import MundoUnidades


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialPosicaoSaida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_posicao_saida import BancadaPosicaoSaida
        cls.bancada = BancadaPosicaoSaida()

    def comparar(self, m, indice, direcao, dimensoes=None):
        self.assertEqual(m.calcular_posicao_saida(indice, direcao, dimensoes),
                         self.bancada.calcular(indice, direcao))

    def test_all_direction_bytes_and_types(self):
        m = MundoUnidades()
        for tipo in range(22):
            m.estruturas[8] = tipo
            struct.pack_into('<H', m.estruturas, 2, 0x505 + tipo * 257)
            self.bancada.carregar(m.estruturas)
            for direcao in range(256):
                self.comparar(m, 0, direcao)
            self.assertEqual(self.bancada.registros(), m.estruturas)

    def test_origins_at_wrap_and_index_truncation(self):
        m = MundoUnidades()
        for indice in (0, 999):
            p = indice * 276
            for tipo in range(22):
                m.estruturas[p+8] = tipo
                for origem in (0, 1, 255, 256, 0x1234, 0xfefe, 0xffff):
                    struct.pack_into('<H', m.estruturas, p+2, origem)
                    self.bancada.carregar(m.estruturas)
                    self.comparar(m, 0xbeef0000 | indice, 0xabcd01ff)
            self.assertEqual(self.bancada.registros(), m.estruturas)

    def test_modified_dimensions_with_32bit_underflow_and_overflow(self):
        m = MundoUnidades()
        rng = random.Random(0x420698)
        dimensoes = [(0, 0), (1, 1), (65535, 65535), (0, 65535), (65535, 0),
                     (256, 257), (32768, 32767)]
        dimensoes += [(rng.randrange(65536), rng.randrange(65536)) for _ in range(16)]
        for tipo in range(22):
            m.estruturas[8] = tipo
            for largura, altura in dimensoes:
                self.bancada.dimensoes(tipo, largura, altura)
                for origem in (0, 0xff, 0xffff):
                    struct.pack_into('<H', m.estruturas, 2, origem)
                    self.bancada.carregar(m.estruturas)
                    self.comparar(m, 0, rng.randrange(256), (largura, altura))
            from pegadas_estruturas import tamanho_estrutura
            self.bancada.dimensoes(tipo, *tamanho_estrutura(tipo))
            self.assertEqual(self.bancada.registros(), m.estruturas)

    def test_poison_record_bytes_do_not_add_eligibility_conditions(self):
        m = MundoUnidades()
        for padrao in (0, 1, 0xff, 0xa5):
            m.estruturas[:] = bytes([padrao]) * 276000
            for tipo in range(22):
                m.estruturas[8] = tipo
                self.bancada.carregar(m.estruturas)
                self.comparar(m, 0, 0x78)
                self.assertEqual(self.bancada.registros(), m.estruturas)
