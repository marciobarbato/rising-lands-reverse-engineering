"""Ciclo integrado de rota, chegada e mensagem; limites explícitos do modelo."""
import struct
import sys
import unittest
from pathlib import Path
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'ferramentas'))
from avanco_unidades import MundoFisico
from caminhos import serializar_rota
from movimento import PARAMETROS_TIPOS
from tarefas_ia import MaquinaTarefas
from simbolos_ia import Instrucao
from test_tarefas_ia import programa


from demonstrar_chegada import preparar_trajeto


class AvancoUnidades(unittest.TestCase):
    def test_duas_celulas_e_uma_mensagem_ao_destino(self):
        mundo,maquina=preparar_trajeto()
        tarefa=maquina.postar(0,1,(0,0x507))
        maquina.atualizar(0)
        self.assertEqual(maquina.byte(tarefa,0x5e),1)
        eventos=[]
        celulas=[]
        for ciclo in range(1,40):
            evento=mundo.atualizar_movimento(0,maquina)
            celulas.append(mundo.palavra(0,8))
            if evento:eventos.append((ciclo,evento))
        self.assertIn(0x506,celulas)
        self.assertEqual(mundo.palavra(0,8),0x507)
        self.assertEqual(len(eventos),1)
        self.assertEqual(eventos[0][0],33)
        self.assertEqual(mundo.unidades[2],7)
        self.assertEqual(struct.unpack_from('<H',mundo.rotas[0])[0],0)
        self.assertEqual(maquina.ler(tarefa,0x54),1)
        maquina.atualizar(0)
        self.assertEqual(maquina.ativas,0)
        self.assertEqual(maquina.ler(tarefa,0x20),1)

    def test_passo_intermediario_nao_conclui_ordem(self):
        mundo,maquina=preparar_trajeto()
        maquina.postar(0,1,(0,0x507))
        maquina.atualizar(0)
        for _ in range(16):self.assertIsNone(mundo.atualizar_movimento(0,maquina))
        self.assertEqual(mundo.palavra(0,8),0x506)
        self.assertEqual(mundo.unidades[2],2)
        self.assertEqual(maquina.ativas,1)
        self.assertEqual(maquina.byte(0,0x5e),1)

    def test_fadiga_e_armadilha_hostil_exigem_integracao_explicita(self):
        mundo,_=preparar_trajeto()
        mundo.unidades[0x72]=1
        mundo.limites_fadiga[7]=1
        antes=mundo.ler_unidade(0)
        with self.assertRaises(NotImplementedError):mundo.avancar_passo(0)
        self.assertEqual(mundo.ler_unidade(0),antes)
        mundo.unidades[0x72]=0
        mundo.objetos[0x505]=0x46
        mundo.donos_objetos[0x505]=1
        with self.assertRaises(NotImplementedError):mundo.avancar_passo(0)

    def test_proxima_celula_bloqueada_nao_e_ignorada(self):
        mundo,_=preparar_trajeto()
        mundo.atributos[0x506]=1
        with self.assertRaises(NotImplementedError):mundo.iniciar_passo(0,0x506)
