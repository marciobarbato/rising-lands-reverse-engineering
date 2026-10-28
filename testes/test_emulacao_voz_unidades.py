"""Original query returns, request payload checkpoints and production branch."""
from dataclasses import asdict
import os
import struct
import unittest

from test_voz_unidades import (preparar_voz,consultar_volume_unidade,unidade_selecionada,
                              solicitar_voz_unidade,retomar_solicitacao_saida,
                              DependenciaVozUnidade,ColocacaoSaidaTropa)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1','Optional x86: RISING_EMULAR=1')
class DiferencialVozUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_voz_unidades import BancadaVozUnidades
        cls.bancada=BancadaVozUnidades(segmentar=True)

    def test_selection_all_flag_bytes_owners_activity_and_indices(self):
        from emulador import UNIDADES
        for indice in (0,799):
            m=preparar_voz(indice=indice)
            for flag in range(256):
                for dono in (0,3,4,200):
                    p=indice*276
                    m.unidades[p],m.unidades[p+0xbd],m.unidades[p+2]=dono,flag,(0,4,7,255)[flag % 4]
                    jogador=dono if flag % 2 else (dono+1) & 255
                    self.bancada.carregar_consulta(m)
                    r=self.bancada.selecionada(jogador | 0xabcd0000,indice | 0xabcd0000)
                    self.assertEqual(r,int(unidade_selecionada(m,jogador | 0xabcd0000,indice | 0xabcd0000)))
                    self.assertEqual(bytes(self.bancada.cpu.mem_read(UNIDADES,220800)),bytes(m.unidades))

    def test_volume_distance_threshold_grid_selection_camera_words_and_overflow(self):
        from emulador import UNIDADES
        m=preparar_voz()
        for x in range(32):
            for y in range(32):
                for flag in (0,255):
                    m.palavra(7,8,y*256+x)
                    m.unidades[7*276+0xbd]=flag
                    self.bancada.carregar_consulta(m)
                    self.assertEqual(self.bancada.volume(0xabcd0007),consultar_volume_unidade(m,0xabcd0007,(0,0,0,0)))
        for camera in range(4):
            for janela in ((0,0,16,16),(65535,65535,0,0),(65535,65535,3,3),
                           (32768,0,65535,65535),(0x12348080,-1,65537,2)):
                for celula in (0,255,0xff00,65535,0x808):
                    m.jogador_local=camera
                    m.palavra(7,8,celula)
                    self.bancada.carregar_consulta(m,janela)
                    self.assertEqual(self.bancada.volume(7),consultar_volume_unidade(m,7,janela))
                    self.assertEqual(bytes(self.bancada.cpu.mem_read(UNIDADES,220800)),bytes(m.unidades))

    def test_every_discovery_byte_hidden_guard_and_visible_active_handle_returns(self):
        for valor in range(256):
            m=preparar_voz(handle=0)
            m.descoberto[0][0x808]=valor
            m.unidades[7*276+1],m.unidades[7*276+2]=255,(0,4,7,255)[valor % 4]
            modo=(6,16,0x1200,65535)[valor % 4]
            self.bancada.carregar_voz(m,(0,0,16,16))
            self.bancada.solicitar(0xabcd0007,0xabcd0000 | modo,0xabcd0000 | valor)
            solicitar_voz_unidade(m,0xabcd0007,0xabcd0000 | modo,0xabcd0000 | valor,janela=(0,0,16,16))
            self.assertEqual(self.bancada.conferir_saida(m),[])

    def test_missing_viewport_and_post_sound_exact_payload_partial_state(self):
        for indice in (0,799):
            for handle in (0,0xffffffff):
                for modo in (6,16):
                    m=preparar_voz(indice=indice,handle=handle)
                    self.bancada.carregar_voz(m)
                    self.bancada.solicitar(indice,modo,255,0x440d9f)
                    with self.assertRaises(DependenciaVozUnidade):
                        solicitar_voz_unidade(m,indice,modo,255)
                    self.assertEqual(self.bancada.conferir_saida(m),[])
        for indice in (0,799):
            for tipo in (0,7,25,255):
                for modo in (0,6,16,0x1200,65535):
                    for flag in (0,255):
                        for celula in (0x808,0xf0f0):
                            m=preparar_voz(indice=indice)
                            m.unidades[indice*276+1]=tipo
                            m.palavra(indice,8,celula)
                            m.descoberto[0][celula]=0
                            self.bancada.carregar_voz(m,(0,0,16,16))
                            regs=self.bancada.solicitar(indice,modo,flag,0x440de7)
                            with self.assertRaises(DependenciaVozUnidade) as captura:
                                solicitar_voz_unidade(m,indice,modo,flag,janela=(0,0,16,16))
                            esperado=asdict(captura.exception.solicitacao);esperado.pop('unidade')
                            self.assertEqual(self.bancada.pedido_som(regs),esperado)
                            self.assertEqual(self.bancada.conferir_saida(m),[])

    def test_production_live_building_owner_camera_and_request_boundaries(self):
        pedido=ColocacaoSaidaTropa(7,7,0x808,1,0x909)
        for dono in range(256):
            for camera in (0,3):
                m=preparar_voz(handle=0)
                m.jogador_local=camera
                m.descoberto[camera][0x808]=0
                m.estruturas[7*276+4]=dono
                self.bancada.carregar_voz(m,(0,0,16,16))
                regs=self.bancada.retomar_solicitacao(pedido)
                r=retomar_solicitacao_saida(m,pedido,janela=(0,0,16,16) if dono == camera else None)
                self.assertEqual((regs['EIP'],r.endereco_dependencia),(0x420fb7,0x420fb7))
                self.assertEqual(self.bancada.conferir_saida(m),[])

    def test_complete_joined_prefix_foreign_cleanup_or_original_post_sound_stop(self):
        from test_colocacao_saida import preparar
        from test_conversao_saida import PedidoFixture,tipos_fixture
        from test_experiencia_unidades import maximo
        from demonstrar_saida_tropa import BonusUnidades,capacidade_tipo
        from conversao_unidades import retomar_conversao_saida
        from recuperacao_unidades import retomar_recuperacao_saida
        from experiencia_unidades import retomar_experiencia_saida
        from colocacao_saida import retomar_colocacao_saida
        bonus=BonusUnidades(bytes(1872))
        for estrutura in (1,2,13,16):
            for tipo in (0,6,16,25):
                for dono,handle in ((0,0),(0,0xffffffff),(3,0),(3,0xffffffff)):
                    m=preparar(9,dono=dono,indice=799)
                    struct.pack_into('<I',m.unidades,799*276+0x104,handle)
                    m.atributos[:]=bytes(65536);m.regioes[:]=[1]*65536
                    m.estruturas[7*276+4],m.estruturas[7*276+8],m.estruturas[7*276+0x7b]=dono,estrutura,tipo
                    struct.pack_into('<H',m.estruturas,7*276+2,0x505)
                    struct.pack_into('<H',m.estruturas,7*276+0x7c,0x909)
                    tipos=tipos_fixture();struct.pack_into('<H',tipos,tipo*50+0x2a,1);maximo(tipos,tipo,100)
                    pedido=PedidoFixture(direcao=14 if estrutura == 13 else 4)
                    self.bancada.carregar_voz(m,(0,0,16,16),tipos)
                    pendente=dono == 0 and handle == 0xffffffff
                    regs=self.bancada.retomar_saida(pedido,parada=0x440de7 if pendente else 0x420fb7)
                    r=retomar_conversao_saida(m,pedido,tipos,capacidade_tipo=capacidade_tipo,modificador=bonus.consultar)
                    r=retomar_recuperacao_saida(m,r,tipos);r=retomar_experiencia_saida(m,r,tipos);r=retomar_colocacao_saida(m,r)
                    if pendente:
                        with self.assertRaises(DependenciaVozUnidade) as captura:
                            retomar_solicitacao_saida(m,r,janela=(0,0,16,16))
                        esperado=asdict(captura.exception.solicitacao);esperado.pop('unidade')
                        self.assertEqual(self.bancada.pedido_som(regs),esperado)
                    else:
                        final=retomar_solicitacao_saida(m,r,janela=(0,0,16,16) if dono == 0 else None)
                        self.assertEqual(final.endereco_dependencia,0x420fb7)
                    self.assertEqual(self.bancada.conferir_saida(m),[])
                    self.assertEqual(self.bancada.efeitos,m.efeitos)
