"""Fresh native shared-pool conversion and original caller checkpoint tests."""
import os
import random
import struct
import unittest
from test_conversao_saida import (preparar, tipos_fixture, PedidoFixture,
                                 estado_compartilhado, converter_unidade, retomar_conversao_saida)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialConversaoSaida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_conversao_saida import BancadaConversaoSaida
        cls.bancada = BancadaConversaoSaida()

    def consultas(self, mod1, mod12, dono=0, tipo=0):
        from demonstrar_saida_tropa import BonusUnidades, capacidade_tipo
        memoria = bytearray(1872)
        if dono not in (4, 200):
            base = dono * 468 + tipo * 18
            memoria[base+11], memoria[base+16] = mod1, mod12
        bonus_original = BonusUnidades(memoria)
        chamadas = []
        def capacidade(t):
            chamadas.append(('capacity', t))
            return capacidade_tipo(t)
        def bonus(dono, t, seletor):
            chamadas.append(('bonus', dono, t, seletor))
            return bonus_original.consultar(dono, t, seletor)
        return capacidade, bonus, chamadas

    def test_complete_conversion_full_pools_states_owners_and_indices(self):
        rng = random.Random(0x457b87)
        tipos = tipos_fixture()
        for tipo in range(26):
            for estado in (0, 1, 4, 14):
                for dono in (0, 3, 4, 200):
                    for indice in (0, 799):
                        m, _ = preparar(tipo, dono, estado, indice)
                        if rng.randrange(2):
                            m.busca.unidade = 65535
                        celula, direcao = rng.randrange(65536), rng.randrange(256)
                        mod1, mod12 = rng.randrange(256), rng.randrange(256)
                        self.bancada.carregar_mundo(m, tipos, mod1=mod1, mod12=mod12, tipo=tipo, dono=dono)
                        self.bancada.converter(0xabcd0000 | indice, celula, direcao, tipo)
                        capacidade, bonus, chamadas = self.consultas(mod1, mod12, dono, tipo)
                        converter_unidade(m, 0xabcd0000 | indice, celula, direcao, tipo, tipos,
                                         capacidade_tipo=capacidade, modificador=bonus)
                        self.assertEqual(estado_compartilhado(m), self.bancada.estado())
                        self.assertEqual(chamadas, self.bancada.chamadas)

    def test_position_and_live_type_reload_complete_original_caller_fragment(self):
        for tipo_estrutura in range(22):
            for tipo_unidade in range(26):
                for direcao in (0, 255):
                    m, tipos = preparar(tipo_unidade)
                    m.estruturas[7*276+8] = tipo_estrutura
                    pedido = PedidoFixture(direcao=direcao, tipo_unidade=(tipo_unidade+1) % 26)
                    self.bancada.carregar_mundo(m, tipos, mod1=17, mod12=250, tipo=tipo_unidade)
                    native = self.bancada.retomar_saida(pedido)
                    capacidade, bonus, chamadas = self.consultas(17, 250, tipo=tipo_unidade)
                    resultado = retomar_conversao_saida(m, pedido, tipos,
                                                      capacidade_tipo=capacidade, modificador=bonus)
                    self.assertEqual(estado_compartilhado(m), self.bancada.estado())
                    self.assertEqual(chamadas, self.bancada.chamadas)
                    self.assertEqual((native['EIP'], native['EBP'], resultado.tipo_unidade),
                                     (0x420f6e, resultado.celula, tipo_unidade))

    def test_missing_capacity_and_bonus1_match_native_checkpoint_memory(self):
        for indice in (0, 799):
            for tipo in (2, 4):
                for consulta, parada in (('capacity', 0x4475ac), ('bonus1', 0x457da2)):
                    m, tipos = preparar(tipo=tipo, indice=indice)
                    self.bancada.carregar_mundo(m, tipos, tipo=tipo, mod12=250)
                    self.bancada.converter(indice, 0x808, 9, tipo, parada)
                    def bonus(dono, t, seletor):
                        if seletor == 1:
                            raise NotImplementedError('BonusGetValEngin selector 1')
                        return 250
                    with self.assertRaises(NotImplementedError):
                        converter_unidade(m, indice, 0x808, 9, tipo, tipos,
                                         capacidade_tipo=None if consulta == 'capacity' else lambda t: 0,
                                         modificador=bonus)
                    self.assertEqual(estado_compartilhado(m), self.bancada.estado())

    def test_missing_bonus12_matches_native_frame_write_order(self):
        for indice in (0, 799):
            m, tipos = preparar(tipo=4, indice=indice)
            self.bancada.carregar_mundo(m, tipos, tipo=4)
            self.bancada.converter(indice, 0x808, 9, 4, 0x457845)
            with self.assertRaises(NotImplementedError):
                converter_unidade(m, indice, 0x808, 9, 4, tipos, capacidade_tipo=lambda t: 0)
            self.assertEqual(estado_compartilhado(m), self.bancada.estado())
