"""Avanço e visão comparados com todas as chamadas originais, sem mocks."""
import os
import struct
import sys
import unittest
from pathlib import Path
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'ferramentas'))
from avanco_unidades import MundoFisico
from movimento import PARAMETROS_TIPOS, direcao_entre_celulas
from caminhos import serializar_rota
from tarefas_ia import MaquinaTarefas
from simbolos_ia import Instrucao
from test_tarefas_ia import programa


def mundo_passo(tipo=7,dono=0,raio=1,origem=0x505,destino=0x506):
    m=MundoFisico(16,16)
    u=bytearray(276)
    u[0],u[1],u[2]=dono,tipo,2
    u[0x90]=u[0x91]=direcao_entre_celulas(origem,destino)
    u[0x98],u[0x93],u[0xa5],u[0xa7]=PARAMETROS_TIPOS[tipo]
    u[0x97]=31
    u[0xbb]=raio
    struct.pack_into('<H',u,8,origem)
    struct.pack_into('<H',u,0x7c,destino)
    struct.pack_into('<H',u,0x7e,destino)
    struct.pack_into('<I',u,0x10c,0xffffffff)
    m.escrever_unidade(0,u)
    m.ocupar(0,origem,True)
    m.ocupar(0,destino,True)
    m.rotas[0]=bytearray(serializar_rota([destino]))
    if dono<4:
        m.descobrir_area(origem,raio+2,dono)
        m.iluminar_area(origem,raio,dono)
    m.minimapa(dono,origem,4)
    return m


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Emulação opcional: RISING_EMULAR=1')
class DiferencialAvanco(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_avanco import BancadaAvanco
        cls.bancada=BancadaAvanco()

    def test_chegada_visao_ocupacao_tipos_e_donos(self):
        for tipo in (0,3,7,11,16,17,25):
            for dono in (0,1,4,200):
                m=mundo_passo(tipo,dono)
                self.bancada.carregar_fisica(m)
                m.avancar_passo(0)
                self.bancada.avancar(0)
                self.assertEqual(self.bancada.conferir_fisica(m),[],(tipo,dono))

    def test_prefixo_e_conclusao_da_ordem(self):
        for tipo in range(26):
            m=mundo_passo(tipo,0,0)
            m.unidades[0x97]=0
            self.bancada.carregar_fisica(m)
            for _ in range(34):
                chegou=m.avancar_passo(0)
                self.bancada.avancar(0)
                self.assertEqual(self.bancada.conferir_fisica(m),[],tipo)
                if chegou:break
            self.assertTrue(chegou)
            m.concluir_movimento(0)
            self.bancada.concluir(0)
            self.assertEqual(self.bancada.conferir_fisica(m),[],tipo)

    def test_visao_bordas_sobreposicao_cores_e_desconto(self):
        for origem,destino,raio in ((0x000,0x001,0),(0x101,0x202,2),(0xf0e,0xf0f,2),(0x808,0x708,1)):
            m=mundo_passo(7,0,raio,origem,destino)
            m.tiles=[i % 740 for i in range(65536)]
            m.mini_estruturas[:]=bytes([77])*65536
            # Sobreposição de fontes, incluindo saturação/decrescimento de 255.
            for c in m.circulo(origem,raio):m.contagem_luz[0][c]=255 if c%2 else 2
            m.unidades[0xf5]=1
            self.bancada.carregar_fisica(m)
            m.avancar_passo(0,1)
            self.bancada.avancar(0,1)
            self.assertEqual(self.bancada.conferir_fisica(m),[],(origem,destino,raio))

    def test_notificacao_acorda_tarefa_sucesso_e_falha(self):
        from mensagens_chegada import notificar_estado
        for mascara in (8,1):
            p=programa([Instrucao('I_AttenteMessageGroupe',0x123,1,2,mascara)])
            m=mundo_passo(7,0,1)
            m.definir_grupo(0,[0])
            struct.pack_into('<H',m.grupos,0x16,1)
            struct.pack_into('<I',m.unidades,0x10c,0)
            maquina=MaquinaTarefas(p,mundo=m)
            self.bancada.carregar(p)
            self.bancada.carregar_fisica(m)
            self.assertEqual(maquina.postar(0,1,(0,)),self.bancada.postar(0,1,(0,)))
            self.assertEqual(maquina.atualizar(0),self.bancada.atualizar(0))
            self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
            self.assertIsNone(notificar_estado(m,0,maquina))
            self.bancada.notificar(0)
            self.assertEqual(self.bancada.conferir_fisica(m),[])
            m.avancar_passo(0)
            self.bancada.avancar(0)
            m.concluir_movimento(0)
            self.bancada.concluir(0)
            evento=notificar_estado(m,0,maquina)
            self.bancada.notificar(0)
            self.assertEqual(evento['resultado'],1 if mascara==8 else 0xffffffff)
            self.assertEqual(self.bancada.conferir_fisica(m),[])
            self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
            self.assertEqual(maquina.atualizar(0),self.bancada.atualizar(0))
            self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
            self.assertEqual(maquina.ativas,0)

    def test_payload_cache_e_filtros_de_notificacao(self):
        from mensagens_chegada import notificar_estado
        p=programa([Instrucao('I_AttenteMessageGroupe',0x123,1,2,4)])
        for dono,controle,estado,sub,cache in ((0,2,11,1,False),(0,1,7,0,False),
                                              (4,2,7,0,False),(0,2,7,0,True),(0,2,2,0,False)):
            m=mundo_passo(7,dono,0)
            m.controle_jogadores[0]=controle
            m.unidades[2],m.unidades[0x89]=estado,sub
            m.unidades[0x10a]=estado if cache else 0
            m.unidades[0x10b]=sub if cache else 0
            struct.pack_into('<I',m.unidades,0x10c,0)
            m.palavra(0,0xc0,123)
            struct.pack_into('<H',m.grupos,0x16,1)
            maquina=MaquinaTarefas(p,mundo=m)
            self.bancada.carregar(p)
            self.bancada.carregar_fisica(m)
            self.assertEqual(maquina.postar(0,1,(0,)),self.bancada.postar(0,1,(0,)))
            maquina.atualizar(0)
            self.bancada.atualizar(0)
            evento=notificar_estado(m,0,maquina)
            self.bancada.notificar(0)
            self.assertEqual(self.bancada.conferir_fisica(m),[])
            self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
            if dono==0 and controle==2 and estado==11:
                self.assertEqual(evento['resultado'],123)
            else:self.assertIsNone(evento)

    def test_fadiga_acumula_consume_provisao_e_preserva_overflow(self):
        for dono in (0,1,4,200):
            for contador,limite,bonus in ((0,20,0),(4,5,0),(8,5,4),(65535,1,0)):
                m=mundo_passo(7,dono,0)
                m.unidades[0x72]=1
                m.unidades[0x97]=0
                m.palavra(0,4,2)
                m.palavra(0,0x74,contador)
                m.limites_fadiga[7]=limite
                if dono<4:m.bonus_fadiga[dono][7]=bonus
                self.bancada.carregar_fisica(m)
                m.avancar_passo(0)
                self.bancada.avancar(0)
                self.assertEqual(self.bancada.conferir_fisica(m),[],(dono,contador,limite,bonus))

    def test_rota_duas_celulas_tarefa_e_mensagem_com_chamadas_originais(self):
        from test_avanco_unidades import preparar_trajeto
        from mensagens_chegada import notificar_estado
        from caminhos import proxima_celula
        m,maquina=preparar_trajeto()
        self.bancada.carregar(maquina.programa)
        self.bancada.carregar_fisica(m)
        self.assertEqual(maquina.postar(0,1,(0,0x507)),self.bancada.postar(0,1,(0,0x507)))
        self.assertEqual(maquina.atualizar(0),self.bancada.atualizar(0))
        eventos=[]
        for ciclo in range(1,34):
            chegou=m.palavra(0,8)==m.palavra(0,0x7e)
            self.bancada.concluir(0)
            if not chegou:
                if m.palavra(0,8)==m.palavra(0,0x7c) and not m.unidades[0x86] and not m.unidades[0x87]:
                    self.bancada.escolher_proximo(0)
                self.bancada.avancar(0)
            self.bancada.notificar(0)
            evento=m.atualizar_movimento(0,maquina)
            if evento:eventos.append(evento)
            self.assertEqual(self.bancada.conferir_fisica(m),[],ciclo)
            self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
        self.assertEqual(len(eventos),1)
        self.assertEqual(maquina.atualizar(0),self.bancada.atualizar(0))
        self.assertEqual(self.bancada.memoria_tarefas(),bytes(maquina.memoria))
        self.assertEqual(maquina.ativas,0)

    def test_giro_completo_e_campo_auxiliar_dos_tipos_12_15(self):
        for tipo in range(26):
            for desejada,atual,contador,periodo in ((9,1,0,1),(1,16,1,2),(16,16,0,0)):
                m=mundo_passo(tipo,0,0)
                m.unidades[0x90:0x94]=bytes([desejada,atual,contador,periodo])
                self.bancada.carregar_fisica(m)
                m.girar(0)
                self.bancada.girar(0)
                self.assertEqual(self.bancada.conferir_fisica(m),[],(tipo,desejada,atual))
