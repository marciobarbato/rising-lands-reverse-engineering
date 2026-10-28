"""PlaceBatiment, vizinhanças e efeitos observáveis confrontados com o x86."""
import itertools
import os
import random
import struct
import unittest
from test_terreno_estruturas import mundo_estrutura
from colocacao_estruturas import combinacao_muro,validar_portao


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Emulação opcional: RISING_EMULAR=1')
class DiferencialColocacaoEstruturas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_colocacao_estruturas import BancadaColocacaoEstruturas
        cls.bancada=BancadaColocacaoEstruturas()

    def _conferir(self,m,caso):
        self.assertEqual(self.bancada.conferir_terreno(m),[],caso)

    def test_combinacoes_e_validade_dos_portoes_com_ids_de_objeto_variaveis(self):
        b=self.bancada
        for muro,portao in ((254,253),(37,38),(0,1)):
            for valores in itertools.product((19,muro,portao),repeat=4):
                m=mundo_estrutura(tipo=9)
                m.objeto_muro,m.objeto_portao=muro,portao
                for c,v in zip((0x504,0x605,0x506,0x405),valores):m.objetos[c]=v
                for centro in (19,portao):
                    m.objetos[0x505]=centro
                    b.carregar_navegacao(m)
                    self.assertEqual(b.combinacao(0x505),combinacao_muro(m,0x505),valores)
                    self.assertEqual(b.validar_portao(0x505),validar_portao(m,0x505),valores)
                    self._conferir(m,(valores,centro))

    def test_colocacao_todos_tipos_e_origens_com_bordas_entre_linhas(self):
        b=self.bancada
        for tipo in range(22):
            for origem in (0x505,0x0100,0x0eff):
                m=mundo_estrutura(tipo,indice=999,origem=origem)
                m.atributos[origem]=0x40
                mascara=bytes(range(20)) if tipo==20 else None
                b.carregar_navegacao(m)
                b.colocar(999,mascara);m.colocar_estrutura(999,mascara)
                self._conferir(m,(tipo,origem))

    def test_portoes_todas_as_vizinhancas_e_sobreposicoes_da_regiao(self):
        b=self.bancada
        for valores in itertools.product((19,254,253),repeat=4):
            for regiao in (1,0x4000,0x8000):
                m=mundo_estrutura(tipo=12)
                for c,v in zip((0x504,0x605,0x506,0x405),valores):m.objetos[c]=v
                m.regioes[0x505]=regiao
                b.carregar_navegacao(m)
                b.colocar(7);m.colocar_estrutura(7)
                self._conferir(m,(valores,regiao))

    def test_muros_vizinhos_exigem_objeto_e_rotulo_sem_filtrar_tipo_do_registro(self):
        b=self.bancada;rng=random.Random(0x41c251)
        for caso in range(64):
            m=mundo_estrutura(tipo=9,indice=0,origem=0x505)
            for i,c in enumerate((0x504,0x506,0x405,0x605),1):
                m.objetos[c]=rng.choice((19,254,253))
                m.regioes[c]=rng.choice((1,0x4000,0x8000|i<<5))
                m.estruturas[i*276+8]=rng.randrange(22)
            for c in (0x503,0x404,0x604,0x507,0x406,0x606,0x305,0x705):
                m.objetos[c]=rng.choice((19,254,253))
            b.carregar_navegacao(m)
            b.atualizar_vizinhos(0x505);m.atualizar_muros_vizinhos(0x505)
            self._conferir(m,caso)

    def test_limites_lineares_e_preferencia_horizontal(self):
        b=self.bancada
        for celula in (0,1,255,256,0x1ff,0xfefe):
            m=mundo_estrutura(tipo=12,origem=celula)
            for delta in (-256,-1,1,256):
                c=celula+delta
                if 0<=c<65536:m.objetos[c]=254
            b.carregar_navegacao(m)
            self.assertEqual(b.validar_portao(celula),validar_portao(m,celula),celula)
            b.colocar(7);m.colocar_estrutura(7)
            self._conferir(m,celula)

    def test_trajetos_mensagens_e_tarefas_depois_da_colocacao(self):
        from demonstrar_colocacao_estruturas import preparar_colocacao_cenario,colocar_cenario
        b=self.bancada
        for nome in ('edificio','muro_com_portao','portao_sem_encaixe'):
            m,maquina,estruturas=preparar_colocacao_cenario(nome)
            m.solucionador.identificadores_rotas=tuple(b.grades['rotas']+i*512 for i in range(800))
            b.carregar(maquina.programa);b.carregar_navegacao(m)
            for indice,tipo,celula in estruturas:b.colocar(indice)
            for indice,tipo,celula in estruturas:
                if tipo in (9,12):b.atualizar_vizinhos(celula)
            colocar_cenario(m,estruturas)
            self._conferir(m,(nome,'colocacao'))
            self.assertEqual(maquina.postar(0,1,(0,0x40a)),b.postar(0,1,(0,0x40a)))
            self.assertEqual(maquina.atualizar(0),b.atualizar(0))
            for ciclo in range(1200):
                b.pulso_navegacao(0);m.atualizar_movimento(0,maquina)
                self._conferir(m,(nome,ciclo))
                self.assertEqual(b.memoria_tarefas(),bytes(maquina.memoria))
                if m.unidades[2]==7:break
            else:self.fail('Trajeto não terminou: '+nome)
            self.assertEqual(m.palavra(0,8),0x40a)
            self.assertEqual(maquina.atualizar(0),b.atualizar(0))
            self.assertEqual(maquina.ativas,0)
