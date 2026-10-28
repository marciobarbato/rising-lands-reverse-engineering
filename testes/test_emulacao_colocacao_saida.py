"""New unpatched original physical exit, movement and joined prefix tests."""
import os
import struct
import unittest

from test_colocacao_saida import (preparar, colocar_unidade_saida, retomar_colocacao_saida,
                                 DependenciaColocacaoSaida, ExperienciaSaidaTropa)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional x86: RISING_EMULAR=1')
class DiferencialColocacaoSaida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_colocacao_saida import BancadaColocacaoSaida
        cls.bancada = BancadaColocacaoSaida()

    def comparar(self,m,indice,celula,parada=None):
        self.bancada.carregar_saida(m)
        if parada:
            self.bancada.colocar(indice,celula,parada)
            with self.assertRaises(DependenciaColocacaoSaida):
                colocar_unidade_saida(m,indice,celula)
        else:
            self.bancada.colocar(indice,celula)
            colocar_unidade_saida(m,indice,celula)
        self.assertEqual(self.bancada.conferir_saida(m),[])
        self.assertEqual(self.bancada.efeitos,m.efeitos)

    def test_all_types_owners_edge_indices_and_every_activity_byte(self):
        for tipo in range(26):
            for dono in (0,1,2,3,4,200):
                for indice in (0,799):
                    m = preparar(tipo,dono,(0,4,14)[tipo % 3],indice)
                    if tipo % 2:
                        m.busca.unidade = 17
                    self.comparar(m,0xabcd0000 | indice,0x12340808)
        for estado in range(256):
            self.comparar(preparar(estado=estado),7,0x808)

    def test_geometry_edges_wrapped_quad_footprints_and_vision_limits(self):
        for largura,altura in ((16,16),(32,16),(64,64),(128,64),(256,256)):
            for celula in (0,largura-1,(altura-1)*256,(altura-1)*256+largura-1):
                for tipo in (1,3,16,17):
                    m = preparar(tipo,(0,200)[tipo % 2],largura=largura,altura=altura)
                    self.comparar(m,7,celula)
        for raio in range(9):
            for dono in (0,3):
                m = preparar(dono=dono,raio=raio,extra=0)
                for c in m.circulo(0x808,raio):
                    m.contagem_luz[dono][c] = 255 if c % 2 else 2
                self.comparar(m,7,0x808)

    def test_large_vision_original_pre_discovery_checkpoint(self):
        for indice in (0,799):
            for raio,extra in ((9,0),(8,1),(255,255)):
                self.comparar(preparar(indice=indice,raio=raio,extra=extra),indice,0x808,0x446146)

    def test_placement_and_original_movement_caller_all_types(self):
        for tipo in range(26):
            for objeto in (0,0x36):
                m = preparar(tipo)
                struct.pack_into('<H',m.estruturas,7*276+0x7c,0x909)
                m.objetos[0x909] = objeto
                pedido = ExperienciaSaidaTropa(7,7,0x808,25)
                self.bancada.carregar_saida(m)
                regs = self.bancada.retomar_colocacao(pedido)
                r = retomar_colocacao_saida(m,pedido)
                self.assertEqual(self.bancada.conferir_saida(m),[])
                self.assertEqual(self.bancada.efeitos,m.efeitos)
                self.assertEqual((regs['EIP'],r.destino_ordem),(0x420f9e,0x909))

    def test_unsaturated_vision_radius_edges_with_preserved_native_resumptions(self):
        from bancada_colocacao_saida import BancadaColocacaoSaida
        b = BancadaColocacaoSaida(segmentar=True)
        self.bancadas_auxiliares = (b,)
        type(self).bancada_segmentada = b
        for raio in range(9):
            for dono in (0,3):
                m = preparar(tipo=3,dono=dono,raio=raio)
                b.carregar_saida(m)
                b.colocar(7,0x808)
                colocar_unidade_saida(m,7,0x808)
                self.assertEqual(b.conferir_saida(m),[])
                self.assertEqual(b.efeitos,m.efeitos)
        self.assertGreater(b.retomadas_minimapa,0)

    def test_joined_position_conversion_recovery_experience_placement_and_order(self):
        from test_conversao_saida import PedidoFixture,tipos_fixture
        from test_experiencia_unidades import maximo,fadiga,fila
        from demonstrar_saida_tropa import BonusUnidades,capacidade_tipo
        from conversao_unidades import retomar_conversao_saida
        from recuperacao_unidades import retomar_recuperacao_saida
        from experiencia_unidades import retomar_experiencia_saida
        bonus = BonusUnidades(bytes(1872))
        for estrutura in (1,2,13,16):
            for tipo in range(26):
                m = preparar(9,dono=tipo % 4,indice=799)
                m.atributos[:] = bytes(65536)
                m.regioes[:] = [1]*65536
                m.estruturas[7*276+8],m.estruturas[7*276+0x7b] = estrutura,tipo
                struct.pack_into('<H',m.estruturas,7*276+2,0x505)
                struct.pack_into('<H',m.estruturas,7*276+0x7c,0x909)
                tipos = tipos_fixture()
                struct.pack_into('<H',tipos,tipo*50+0x2a,1)
                maximo(tipos,tipo,100)
                fadiga(tipos,tipo,65535)
                fila(m,tipo % 4,tipo,((tipo % 8) << 5) | 1)
                pedido = PedidoFixture(direcao=14 if estrutura == 13 else 4)
                self.bancada.carregar_saida(m,tipos)
                regs = self.bancada.retomar_saida(pedido)
                convertido = retomar_conversao_saida(m,pedido,tipos,capacidade_tipo=capacidade_tipo,
                                                    modificador=bonus.consultar)
                recuperado = retomar_recuperacao_saida(m,convertido,tipos)
                experiente = retomar_experiencia_saida(m,recuperado,tipos)
                r = retomar_colocacao_saida(m,experiente)
                self.assertEqual(self.bancada.conferir_saida(m),[])
                self.assertEqual(self.bancada.efeitos,m.efeitos)
                self.assertEqual((regs['EIP'],r.endereco_dependencia),(0x420f9e,0x420f9e))
