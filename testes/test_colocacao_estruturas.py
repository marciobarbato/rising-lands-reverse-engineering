"""Contratos de colocação, escolha de tiles e conexão local de muros/portões."""
import json
import struct
import subprocess
import sys
import unittest
from pathlib import Path
from test_terreno_estruturas import mundo_estrutura
from colocacao_estruturas import PRIMEIROS_TILES,combinacao_muro,validar_portao


class ColocacaoEstruturas(unittest.TestCase):
    def test_demonstracoes_sem_emulacao_reproduzem_relatorio(self):
        raiz=Path(__file__).resolve().parents[1]
        codigo='''
import json,sys
sys.path.insert(0,'ferramentas')
for nome in ('unicorn','emulador','solucionador_original','solucionador_misto'):
    sys.modules[nome]=None
from demonstrar_colocacao_estruturas import executar_colocacao_cenario
print(json.dumps([executar_colocacao_cenario(n) for n in ('edificio','muro_com_portao','portao_sem_encaixe')]))
'''
        p=subprocess.run([sys.executable,'-B','-c',codigo],cwd=raiz,text=True,capture_output=True,check=True)
        r=json.loads((raiz/'relatorios/colocacao-estruturas-python.json').read_text())
        self.assertEqual(json.loads(p.stdout),r['cenarios'])

    def test_tiles_derivados_do_seletor_original(self):
        p=Path(__file__).resolve().parents[1]/'evidencias/colocacao-estruturas/manifesto.json'
        m=json.loads(p.read_text())
        self.assertEqual(PRIMEIROS_TILES,tuple(t['primeiro_tile'] for t in m['tabela']['tipos']))
        self.assertEqual(m['objetos_iniciais'],dict(muro=254,portao=253))

    def test_edificio_usa_origem_guardada_e_primeiro_tile_por_tipo(self):
        m=mundo_estrutura(tipo=0)
        m.colocar_estrutura(7)
        self.assertEqual(m.tiles[0x505],0x2fa)
        self.assertEqual(m.tiles[0x506],0x2fb)
        self.assertEqual(m.regioes[0x505],0x8000|7<<5)
        self.assertEqual(m.objetos[0x505],0)

    def test_muro_e_objeto_usa_mascara1_e_conserva_tile(self):
        m=mundo_estrutura(tipo=9)
        m.objetos[0x504],m.objetos[0x605]=m.objeto_muro,m.objeto_portao
        m.atributos[0x505]=0x40
        self.assertEqual(combinacao_muro(m,0x505),11)
        m.colocar_estrutura(7)
        self.assertEqual(m.objetos[0x505],254)
        self.assertEqual(m.atributos[0x505],0x41)
        self.assertEqual(m.tiles[0x505],77)
        self.assertEqual(struct.unpack_from('<H',m.estruturas,7*276+0x7c)[0],11)

    def test_portao_horizontal_tem_prioridade_e_libera_campo86(self):
        m=mundo_estrutura(tipo=12)
        for c in (0x504,0x506,0x405,0x605):m.objetos[c]=m.objeto_muro
        m.atributos[0x505]=0x40
        self.assertEqual(validar_portao(m,0x505),0)
        m.colocar_estrutura(7)
        self.assertEqual(m.objetos[0x505],253)
        self.assertEqual(m.atributos[0x505],0x41)
        self.assertEqual(m.tiles[0x505],77)
        self.assertEqual(struct.unpack_from('<H',m.estruturas,7*276+0x7c)[0],0)
        self.assertEqual(struct.unpack_from('<H',m.estruturas,7*276+0x86)[0],0)

    def test_portao_sem_encaixe_nao_altera_o_mundo(self):
        m=mundo_estrutura(tipo=12)
        antes=(bytes(m.estruturas),bytes(m.objetos),bytes(m.atributos),m.tiles[:],m.regioes[:])
        self.assertEqual(validar_portao(m,0x505),255)
        m.colocar_estrutura(7)
        self.assertEqual(antes,(bytes(m.estruturas),bytes(m.objetos),bytes(m.atributos),m.tiles[:],m.regioes[:]))

    def test_atualizar_muros_ao_redor_e_chamada_separada(self):
        m=mundo_estrutura(tipo=9,indice=0,origem=0x505)
        m.estruturas[276+8]=9
        struct.pack_into('<H',m.estruturas,276+2,0x504)
        m.colocar_estrutura(1)
        m.colocar_estrutura(0)
        self.assertEqual(struct.unpack_from('<H',m.estruturas,276+0x7c)[0],0)
        m.atualizar_muros_vizinhos(0x505)
        self.assertEqual(struct.unpack_from('<H',m.estruturas,276+0x7c)[0],1)

    def test_portao_no_centro_zera_combinacao_do_muro(self):
        m=mundo_estrutura(tipo=9)
        for c in (0x504,0x506,0x405,0x605):m.objetos[c]=m.objeto_muro
        self.assertEqual(combinacao_muro(m,0x505),14)
        m.objetos[0x505]=m.objeto_portao
        self.assertEqual(combinacao_muro(m,0x505),0)

    def test_leituras_lineares_nao_envolvem_o_indice_em_bordas(self):
        m=mundo_estrutura(tipo=9,origem=0x0100)
        m.objetos[0x00ff]=m.objeto_muro
        self.assertEqual(combinacao_muro(m,0x0100),7)
        struct.pack_into('<H',m.estruturas,7*276+2,0)
        antes=bytes(m.estruturas)
        with self.assertRaises(NotImplementedError):m.colocar_estrutura(7)
        self.assertEqual(bytes(m.estruturas),antes)

    def test_mascara_em_ram_do_tipo20_permanece_explicita(self):
        m=mundo_estrutura(tipo=20)
        with self.assertRaises(NotImplementedError):m.colocar_estrutura(7)
        m.colocar_estrutura(7,bytes(20))
        self.assertEqual(m.tiles[0x505],0x3c3)
        self.assertEqual(m.regioes[0x505],1)
