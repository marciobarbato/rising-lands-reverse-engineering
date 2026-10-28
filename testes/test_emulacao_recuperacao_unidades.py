"""Fresh intact-x86 recovery helpers and unpatched production caller calls."""
import os
import random
import unittest

from test_recuperacao_unidades import (preparar, maximo, estado_compartilhado,
                                      adicionar_vida_unidade, resetar_fadiga_unidade,
                                      retomar_recuperacao_saida, ConversaoSaidaTropa,
                                      retomar_conversao_saida)
from test_conversao_saida import PedidoFixture


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialRecuperacaoUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_recuperacao_unidades import BancadaRecuperacaoUnidades
        cls.bancada = BancadaRecuperacaoUnidades()

    def test_live_healing_all_types_indices_and_arithmetic_edges(self):
        casos = ((0, 0, 0), (0, 1, 0), (80, 19, 100), (80, 20, 100),
                 (80, 21, 100), (65535, 1, 100), (65535, 65535, 65535),
                 (65535, 0, 65535), (32768, 32768, 65535), (50, 0xabcdffff, 1000),
                 (65000, 1000, 65535), (60000, -1, 65534))
        for tipo in range(26):
            for indice in (0, 799):
                for n, (vida, acrescimo, limite) in enumerate(casos):
                    m, tipos = preparar(tipo=tipo, indice=indice, estado=(0, 4, 7, 255)[n % 4])
                    m.unidades[indice*276+1] = tipo
                    m.palavra(indice, 0x9a, vida)
                    maximo(tipos, tipo, limite)
                    self.bancada.carregar_mundo(m, tipos)
                    regs = self.bancada.adicionar_vida(0xabcd0000 | indice, acrescimo)
                    flag = adicionar_vida_unidade(m, 0xabcd0000 | indice, acrescimo, tipos)
                    self.assertEqual(estado_compartilhado(m), self.bancada.estado())
                    self.assertEqual(regs['EAX'] & 255, int(flag))
                    self.assertEqual((regs['EBX'], regs['ECX']), (0xfedcba98, 0x76543210))

    def test_fatigue_all_type_bytes_including_inactive_and_unknown(self):
        rng = random.Random(0x4530fd)
        for tipo in range(256):
            for indice in (0, 799):
                m, tipos = preparar(indice=indice, estado=(0, 4, 7, 255)[tipo % 4])
                m.unidades[indice*276], m.unidades[indice*276+1] = (0, 3, 4, 200)[tipo % 4], tipo
                for off in (4, 0x74, 0x76):
                    m.palavra(indice, off, rng.randrange(65536))
                self.bancada.carregar_mundo(m, tipos)
                regs = self.bancada.resetar_fadiga(0xabcd0000 | indice)
                resetar_fadiga_unidade(m, 0xabcd0000 | indice)
                self.assertEqual(estado_compartilhado(m), self.bancada.estado())
                self.assertEqual(regs['EDX'], 0xabcd1234)

    def test_original_recovery_caller_calls_both_helpers_in_order(self):
        for tipo in range(26):
            for indice in (0, 799):
                for vida, limite in ((0, 0), (50, 100), (50, 1050), (50, 5000),
                                     (65000, 65535), (65535, 1)):
                    m, tipos = preparar(indice=indice)
                    m.unidades[indice*276+1] = tipo
                    m.palavra(indice, 0x9a, vida)
                    m.palavra(indice, 0x76, tipo*1733)
                    maximo(tipos, tipo, limite)
                    pedido = ConversaoSaidaTropa(7, 0xabcd0000 | indice, 0xfdfc, (tipo+1) % 26)
                    self.bancada.carregar_mundo(m, tipos)
                    regs = self.bancada.recuperar_saida(pedido)
                    r = retomar_recuperacao_saida(m, pedido, tipos)
                    self.assertEqual(estado_compartilhado(m), self.bancada.estado())
                    self.assertEqual((regs['EIP'], regs['EBP'], r.endereco_dependencia, r.celula),
                                     (0x420f81, 0xfdfc, 0x420f81, 0xfdfc))

    def test_position_conversion_and_recovery_full_original_caller_prefix(self):
        from demonstrar_saida_tropa import BonusUnidades, capacidade_tipo
        bonus = BonusUnidades(bytes(1872))
        for tipo_estrutura in range(22):
            for tipo in range(26):
                indice = (0, 799)[tipo % 2]
                m, tipos = preparar(tipo=tipo, indice=indice)
                m.estruturas[7*276+8] = tipo_estrutura
                m.palavra(indice, 0x9a, 65000 if tipo % 2 else 50)
                m.palavra(indice, 0x76, 0x1234)
                maximo(tipos, tipo, 100+tipo)
                pedido = PedidoFixture(unidade=indice, direcao=(0, 255)[tipo_estrutura % 2])
                self.bancada.carregar_mundo(m, tipos)
                regs = self.bancada.retomar_saida(pedido, parada=0x420f81)
                convertido = retomar_conversao_saida(m, pedido, tipos, capacidade_tipo=capacidade_tipo,
                                                    modificador=bonus.consultar)
                r = retomar_recuperacao_saida(m, convertido, tipos)
                self.assertEqual(estado_compartilhado(m), self.bancada.estado())
                self.assertEqual((regs['EIP'], regs['EBP']), (r.endereco_dependencia, r.celula))
