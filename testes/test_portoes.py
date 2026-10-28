"""Estados físicos e comandos de portões, independentes de renderização."""
import struct
import json
import subprocess
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ferramentas'))
from navegacao_unidades import MundoNavegacao
from portoes import (portao_em_transicao,portao_na_fase15,portao_na_fase0_31,
                     portao_horizontal,solicitar_liberacao_portoes,solicitar_bloqueio_portoes)


def grupo_portoes(horizontal=True,celulas=None,fase=0):
    celulas=celulas or ((0x504,0x505,0x506) if horizontal else (0x405,0x505,0x605))
    m=MundoNavegacao(16,16)
    m.regioes[:]=[1]*65536
    for i,c in enumerate(celulas,7):
        p=i*276;m.estruturas[p+8]=12
        struct.pack_into('<H',m.estruturas,p+2,c)
        struct.pack_into('<H',m.estruturas,p+0x7c,0 if horizontal else 1)
        m.estruturas[p+0x76]=fase
        m.objetos[c]=m.objeto_portao
        if fase!=15:
            m.modificar_regiao_estrutura(i,0,c,True)
            m.atributos[c]|=1
    return m,celulas


class Portoes(unittest.TestCase):
    def test_demonstracao_reproduz_relatorio_com_emulacao_bloqueada(self):
        raiz=Path(__file__).resolve().parents[1]
        codigo='''
import json,sys
sys.path.insert(0,'ferramentas')
for nome in ('unicorn','emulador','solucionador_original','solucionador_misto'):
    sys.modules[nome]=None
from demonstrar_portoes import executar_portao_cenario
print(json.dumps(executar_portao_cenario()))
'''
        p=subprocess.run([sys.executable,'-B','-c',codigo],cwd=raiz,text=True,capture_output=True,check=True)
        r=json.loads((raiz/'relatorios/portoes-python.json').read_text())
        self.assertEqual(json.loads(p.stdout),r['cenario'])

    def test_predicados_preservam_fases_estaveis_e_orientacao(self):
        m,_=grupo_portoes()
        for fase,transicao in ((0,False),(1,True),(14,True),(15,False),(16,True),(30,True),(31,False),(255,True)):
            m.estruturas[7*276+0x76]=fase
            self.assertEqual(portao_em_transicao(m,7),transicao)
            self.assertEqual(portao_na_fase15(m,7),fase==15)
            self.assertEqual(portao_na_fase0_31(m,7),fase in (0,31))
        self.assertTrue(portao_horizontal(m,7))
        struct.pack_into('<H',m.estruturas,7*276+0x7c,256)
        self.assertFalse(portao_horizontal(m,7))

    def test_liberacao_so_restaura_a_regiao_ao_alcancar15(self):
        m,celulas=grupo_portoes();m.alternar_portoes(celulas[1],8)
        self.assertEqual([m.estruturas[i*276+0x76] for i in (7,8,9)],[1,1,1])
        for _ in range(13):
            for i in (7,8,9):m.avancar_estado_portao(i)
        self.assertTrue(all(m.atributos[c]&1 for c in celulas))
        for i in (7,8,9):m.avancar_estado_portao(i)
        self.assertTrue(all(not m.atributos[c]&1 and m.regioes[c]==1 for c in celulas))
        self.assertFalse(any(m.cores_estruturas.grade[c] for c in celulas))

    def test_bloqueio_recusa_grupo_inteiro_se_uma_celula_ocupada(self):
        m,celulas=grupo_portoes(fase=15)
        m.atributos[celulas[1]]|=1
        antes=bytes(m.estruturas)
        m.alternar_portoes(celulas[0],7)
        self.assertEqual(bytes(m.estruturas),antes)
        m.atributos[celulas[1]]&=254
        m.alternar_portoes(celulas[0],7)
        self.assertEqual([m.estruturas[i*276+0x76] for i in (7,8,9)],[16,16,16])
        for _ in range(15):
            for i in (7,8,9):m.avancar_estado_portao(i)
        self.assertTrue(all(m.atributos[c]&1 and m.regioes[c]&0x8000 for c in celulas))

    def test_comando_ignora_grupo_quando_referencia_em_transicao(self):
        m,celulas=grupo_portoes(fase=4);antes=bytes(m.estruturas)
        m.alternar_portoes(celulas[0],7)
        self.assertEqual(bytes(m.estruturas),antes)

    def test_bloqueio_conserva_slots_repetidos_na_lista(self):
        m,_=grupo_portoes(celulas=(0x503,0x504,0x505),fase=15)
        m.objetos[0x505]=0
        solicitar_bloqueio_portoes(m,0x505,9)
        self.assertEqual([m.estruturas[i*276+0x76] for i in (7,8,9)],[17,16,15])

    def test_fases_altas_voltam_a_zero_sem_criar_quadro_visual(self):
        m,celulas=grupo_portoes(fase=31)
        solicitar_liberacao_portoes(m,celulas[0],7)
        self.assertEqual(m.estruturas[7*276+0x76],32)
        m.avancar_estado_portao(7)
        self.assertEqual(m.estruturas[7*276+0x76],0)

    def test_avanco_exige_tipo12(self):
        m,_=grupo_portoes();m.estruturas[7*276+8]=9
        with self.assertRaises(ValueError):m.avancar_estado_portao(7)
