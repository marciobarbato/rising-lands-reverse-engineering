"""Intact native queue/local-level and complete production-prefix comparisons."""
import os
import unittest

from test_experiencia_unidades import (preparar, maximo, fila, fadiga, estado, PedidoFixture,
                                      aplicar_nova_experiencia, consumir_experiencia_unidade,
                                      retomar_experiencia_saida, retomar_recuperacao_saida,
                                      retomar_conversao_saida, DependenciaExperienciaUnidade)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialExperienciaUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_experiencia_unidades import BancadaExperienciaUnidades
        cls.bancada = BancadaExperienciaUnidades()

    def comparar_local(self, tipo, nivel, valor, indice=799):
        m, tipos = preparar(indice=indice, estado=(0, 4, 7, 255)[nivel % 4])
        m.unidades[indice*276+1] = tipo
        if tipo < 26:
            fadiga(tipos, tipo, valor)
        self.bancada.carregar_mundo(m, tipos)
        self.bancada.aplicar(0xabcd0000 | indice, 0xabcd0000 | nivel)
        aplicar_nova_experiencia(m, 0xabcd0000 | indice, 0xabcd0000 | nivel, tipos)
        self.assertEqual(estado(m), self.bancada.estado())

    def test_local_all_types_levels_and_characteristic_division_edges(self):
        for tipo in range(26):
            for indice in (0, 799):
                for nivel in (0, 1, 2, 3, 4, 5, 7, 255):
                    self.comparar_local(tipo, nivel, 65535, indice)
            for valor in (0, 1, 99, 100, 12799, 12800, 25599, 25600, 32767, 32768, 65535):
                for nivel in (1, 4):
                    self.comparar_local(tipo, nivel, valor)

    def test_every_level_byte_and_unknown_type_table_free_branches(self):
        for nivel in range(256):
            for tipo in (4, 25):
                self.comparar_local(tipo, nivel, 32768)
        for nivel in (0, 2, 3, 5, 255):
            self.comparar_local(255, nivel, 0)

    def test_queue_all_owners_types_levels_indices_and_edx_preservation(self):
        for dono in range(4):
            for tipo in range(26):
                for experiencia in (1, 63, 65, 127, 129, 191, 193, 255):
                    for indice in (0, 799):
                        m, tipos = preparar(dono=dono, indice=indice, estado=(0, 4, 7)[tipo % 3])
                        m.unidades[indice*276+1] = tipo
                        fadiga(tipos, tipo, 65535)
                        fila(m, dono, tipo, experiencia)
                        self.bancada.carregar_mundo(m, tipos)
                        regs = self.bancada.consumir(0xabcd0000 | indice)
                        consumir_experiencia_unidade(m, 0xabcd0000 | indice, tipos)
                        self.assertEqual(estado(m), self.bancada.estado())
                        self.assertEqual(regs['EDX'], 0xabcd8080)

    def test_guards_and_nested_missing_table_preserve_original_partial_state(self):
        for dono in range(4):
            for indice in (0, 799):
                for primeiro, experiencia, seguinte_coincide in ((255, 0, False), (7, 255, False),
                                                                  (255, 0, True), (7, 1, True)):
                    m, tipos = preparar(dono=dono, indice=indice)
                    m.unidades[indice*276+1] = 255
                    fila(m, dono, primeiro, experiencia)
                    if seguinte_coincide:
                        m.experiencias_unidades[dono*10+2:dono*10+4] = bytes((255, 97))
                    self.bancada.carregar_mundo(m, tipos)
                    self.bancada.consumir(indice)
                    consumir_experiencia_unidade(m, indice)
                    self.assertEqual(estado(m), self.bancada.estado())
        for indice in (0, 799):
            for tipo, nivel, parada in ((4, 1, 0x44fa71), (0, 4, 0x44fa71), (4, 4, 0x44fafa)):
                for via_fila in (False, True):
                    m, tipos = preparar(indice=indice)
                    m.unidades[indice*276+1] = tipo
                    fila(m, 0, tipo, (nivel << 5) | 1)
                    self.bancada.carregar_mundo(m, tipos)
                    if via_fila:
                        self.bancada.consumir(indice, parada=parada)
                    else:
                        self.bancada.aplicar(indice, nivel, parada=parada)
                    with self.assertRaises(DependenciaExperienciaUnidade) as captura:
                        if via_fila:
                            consumir_experiencia_unidade(m, indice)
                        else:
                            aplicar_nova_experiencia(m, indice, nivel)
                    self.assertEqual(captura.exception.endereco, parada)
                    self.assertEqual(estado(m), self.bancada.estado())

    def test_joined_position_conversion_recovery_experience_original_prefix(self):
        from demonstrar_saida_tropa import BonusUnidades, capacidade_tipo
        bonus = BonusUnidades(bytes(1872))
        for tipo_estrutura in range(22):
            for tipo in range(26):
                indice, dono = (0, 799)[tipo % 2], tipo % 4
                m, tipos = preparar(tipo=tipo, dono=dono, indice=indice)
                m.estruturas[7*276+8] = tipo_estrutura
                m.palavra(indice, 0x9a, 50)
                maximo(tipos, tipo, 100+tipo)
                fadiga(tipos, tipo, 65535)
                fila(m, dono, tipo, ((tipo % 8) << 5) | 1)
                pedido = PedidoFixture(unidade=indice, direcao=(0, 255)[tipo_estrutura % 2])
                self.bancada.carregar_mundo(m, tipos)
                regs = self.bancada.retomar_saida(pedido, parada=0x420f8a)
                convertido = retomar_conversao_saida(m, pedido, tipos, capacidade_tipo=capacidade_tipo,
                                                    modificador=bonus.consultar)
                recuperado = retomar_recuperacao_saida(m, convertido, tipos)
                r = retomar_experiencia_saida(m, recuperado, tipos)
                self.assertEqual(estado(m), self.bancada.estado())
                self.assertEqual((regs['EIP'], regs['EDX'], regs['EBP']),
                                 (r.endereco_dependencia, r.celula, r.celula))
