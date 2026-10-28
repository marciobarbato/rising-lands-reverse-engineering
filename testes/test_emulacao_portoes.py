"""Predicados, comandos e transições de portões contra os corpos x86 originais."""
import os
import struct
import unittest
from test_portoes import grupo_portoes
from portoes import (portao_em_transicao,portao_na_fase15,portao_na_fase0_31,
                     portao_horizontal,solicitar_liberacao_portoes,solicitar_bloqueio_portoes)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Emulação opcional: RISING_EMULAR=1')
class DiferencialPortoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_portoes import BancadaPortoes
        cls.bancada=BancadaPortoes()

    def _conferir(self,m,caso):self.assertEqual(self.bancada.conferir_terreno(m),[],caso)

    def test_predicados_todos_os_bytes_e_orientacoes(self):
        b=self.bancada;m,_=grupo_portoes()
        for fase in range(256):
            m.estruturas[7*276+0x76]=fase
            struct.pack_into('<H',m.estruturas,7*276+0x7c,(0,1,256,65535)[fase%4])
            b.carregar_navegacao(m)
            for endereco,funcao in ((0x4191fd,portao_em_transicao),(0x41934f,portao_na_fase15),
                                   (0x419379,portao_na_fase0_31),(0x4193ac,portao_horizontal)):
                self.assertEqual(b.predicado(endereco,7),funcao(m,7),(endereco,fase))
            self._conferir(m,fase)

    def test_avanco_todas_as_fases_e_bits_de_colisao(self):
        b=self.bancada
        for fase in range(256):
            for atributo in (0,1,3,0x82):
                m,celulas=grupo_portoes(fase=fase)
                m.atributos[celulas[0]]=atributo
                b.carregar_navegacao(m)
                b.avancar_portao(7);m.avancar_estado_portao(7)
                self._conferir(m,(fase,atributo))

    def test_liberacao_horizontal_vertical_e_membros_sem_filtro_de_tipo(self):
        b=self.bancada
        for horizontal in (True,False):
            for fase in (0,15,31,255):
                m,celulas=grupo_portoes(horizontal,fase=fase)
                m.estruturas[8*276+8]=9;m.estruturas[9*276+8]=0
                b.carregar_navegacao(m)
                b.liberar(celulas[1],8);solicitar_liberacao_portoes(m,celulas[1],8)
                self._conferir(m,(horizontal,fase))

    def test_liberacao_conserva_exclusao_da_ultima_coluna_ou_linha(self):
        b=self.bancada
        for horizontal,celulas in ((True,(0x5fd,0x5fe,0x5ff)),(False,(0xfd05,0xfe05,0xff05))):
            m,_=grupo_portoes(horizontal,celulas=celulas)
            b.carregar_navegacao(m)
            b.liberar(celulas[1],8);solicitar_liberacao_portoes(m,celulas[1],8)
            self._conferir(m,horizontal)
            self.assertEqual([m.estruturas[i*276+0x76] for i in (7,8,9)],[1,1,0])

    def test_bloqueio_com_e_sem_ocupacao_nas_duas_orientacoes(self):
        b=self.bancada
        for horizontal in (True,False):
            for ocupado in (True,False):
                m,celulas=grupo_portoes(horizontal,fase=15)
                if ocupado:m.atributos[celulas[1]]=1
                b.carregar_navegacao(m)
                b.bloquear(celulas[1],8);solicitar_bloqueio_portoes(m,celulas[1],8)
                self._conferir(m,(horizontal,ocupado))

    def test_residuos_da_lista_e_teste_vertical_de_coluna_zero(self):
        b=self.bancada
        for horizontal,celulas in ((True,(0x503,0x504,0x505)),(False,(0x300,0x400,0x500,0x600))):
            m,_=grupo_portoes(horizontal,celulas=celulas,fase=15)
            if horizontal:m.objetos[0x505]=0
            b.carregar_navegacao(m)
            b.bloquear(0x505 if horizontal else 0x500,9)
            solicitar_bloqueio_portoes(m,0x505 if horizontal else 0x500,9)
            self._conferir(m,horizontal)

    def test_lista_horizontal_de_bloqueio_pode_alcancar_a_linha_seguinte(self):
        b=self.bancada;m,celulas=grupo_portoes(celulas=(0x5fe,0x5ff,0x600),fase=15)
        b.carregar_navegacao(m)
        b.bloquear(celulas[0],7);solicitar_bloqueio_portoes(m,celulas[0],7)
        self._conferir(m,'virada_da_coluna255')
        self.assertEqual([m.estruturas[i*276+0x76] for i in (7,8,9)],[16,16,16])

    def test_ciclo_de_liberacao_e_bloqueio_com_cores_e_regioes(self):
        b=self.bancada;m,celulas=grupo_portoes()
        b.carregar_navegacao(m)
        b.alternar(celulas[1],8);m.alternar_portoes(celulas[1],8)
        for ciclo in range(14):
            for i in (7,8,9):
                b.avancar_portao(i);m.avancar_estado_portao(i)
                self._conferir(m,('liberacao',ciclo,i))
        b.alternar(celulas[1],8);m.alternar_portoes(celulas[1],8)
        for ciclo in range(15):
            for i in (7,8,9):
                b.avancar_portao(i);m.avancar_estado_portao(i)
                self._conferir(m,('bloqueio',ciclo,i))

    def test_trajeto_atravessa_portao_e_recusa_bloqueio_enquanto_ocupado(self):
        from demonstrar_portoes import preparar_portao_cenario
        b=self.bancada;m,maquina,indice,celula=preparar_portao_cenario()
        m.solucionador.identificadores_rotas=tuple(b.grades['rotas']+i*512 for i in range(800))
        b.carregar(maquina.programa);b.carregar_navegacao(m)
        self.assertEqual(maquina.postar(0,1,(0,0x40a)),b.postar(0,1,(0,0x40a)))
        self.assertEqual(maquina.atualizar(0),b.atualizar(0))
        b.alternar(celula,indice);m.alternar_portoes(celula,indice)
        recusou=solicitou=passou=False
        for ciclo in range(1200):
            b.avancar_portao(indice);m.avancar_estado_portao(indice)
            ocupada=celula in (m.palavra(0,8),m.palavra(0,0x7c))
            if ocupada and not recusou:
                b.alternar(celula,indice);m.alternar_portoes(celula,indice)
                self.assertEqual(m.estruturas[indice*276+0x76],15)
                recusou=True
            elif recusou and not ocupada and not solicitou:
                b.alternar(celula,indice);m.alternar_portoes(celula,indice)
                self.assertEqual(m.estruturas[indice*276+0x76],16)
                solicitou=True
            b.pulso_navegacao(0);m.atualizar_movimento(0,maquina)
            self._conferir(m,ciclo)
            self.assertEqual(b.memoria_tarefas(),bytes(maquina.memoria))
            passou|=m.palavra(0,8)==celula
            if m.unidades[2]==7 and m.estruturas[indice*276+0x76]==0:break
        else:self.fail('O ciclo de portão/trajeto não terminou')
        self.assertTrue(recusou and solicitou and passou)
        self.assertEqual(m.palavra(0,8),0x40a)
        self.assertEqual(maquina.atualizar(0),b.atualizar(0))
        self.assertEqual(maquina.ativas,0)
