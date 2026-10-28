"""Aplicação e limpeza de terreno: registros e grades integrais contra o x86."""
import os
import random
import struct
import unittest
from test_terreno_estruturas import mundo_estrutura
from pegadas_estruturas import TAMANHOS_E_MASCARAS


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Emulação opcional: RISING_EMULAR=1')
class DiferencialTerrenoEstruturas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_terreno_estruturas import BancadaTerrenoEstruturas
        cls.bancada=BancadaTerrenoEstruturas()

    def _conferir(self,m,caso):
        self.assertEqual(self.bancada.conferir_terreno(m),[],caso)

    def test_todos_tipos_origens_bordas_e_ambos_modos_de_limpeza(self):
        b=self.bancada
        for tipo in range(22):
            for origem in (0x505,0,0xfffe,0xfeff):
                m=mundo_estrutura(tipo,indice=999,origem=origem)
                mascara=bytes(int(v) for v in TAMANHOS_E_MASCARAS[tipo][2]) if tipo==20 else None
                b.carregar_navegacao(m)
                b.aplicar_terreno(999,origem,65530,mascara)
                m.aplicar_terreno_estrutura(999,origem,65530,mascara)
                self._conferir(m,(tipo,origem,'aplicar'))
                b.resetar_terreno(999,0);m.resetar_terreno_estrutura(999,0)
                self._conferir(m,(tipo,origem,'piso'))
                b.resetar_terreno(999,255);m.resetar_terreno_estrutura(999,255)
                self._conferir(m,(tipo,origem,'colisao'))
                b.remover_regioes(999);m.remover_regioes_estrutura(999)
                self._conferir(m,(tipo,origem,'regioes'))

    def test_regioes_heterogeneas_e_sobreposicoes_que_nao_podem_ser_substituidas(self):
        b=self.bancada; rng=random.Random(0x41ba49)
        for tipo in range(22):
            m=mundo_estrutura(tipo)
            w,h,mascara=TAMANHOS_E_MASCARAS[tipo]
            for j in range(w*h):
                c=0x505+j//w*256+j%w
                m.atributos[c]=rng.randrange(256)
                m.objetos[c]=rng.randrange(256)
                m.regioes[c]=rng.choice((0,1,0x3fff,0x4000,0x8000))
            dinamica=bytes(rng.randrange(256) for _ in range(20)) if tipo==20 else None
            b.carregar_navegacao(m)
            for _ in range(2):
                b.aplicar_terreno(7,0x505,80,dinamica)
                m.aplicar_terreno_estrutura(7,0x505,80,dinamica)
                self._conferir(m,(tipo,'sobreposicao'))
            b.remover_regioes(7);m.remover_regioes_estrutura(7)
            self._conferir(m,(tipo,'retirada'))

    def test_tipo20_mascara_mutavel_diferente_da_usada_na_remocao(self):
        b=self.bancada
        for mascara in (bytes(20),bytes([1])*20,bytes(range(20)),bytes([255,0])*10):
            m=mundo_estrutura(20)
            b.carregar_navegacao(m)
            b.aplicar_terreno(7,0x505,800,mascara)
            m.aplicar_terreno_estrutura(7,0x505,800,mascara)
            self._conferir(m,'tipo20_aplicacao')
            b.resetar_terreno(7,1);m.resetar_terreno_estrutura(7,1)
            b.remover_regioes(7);m.remover_regioes_estrutura(7)
            self._conferir(m,'tipo20_remocao_nao_uniformizar')

    def test_modo_e_indices_truncados_e_origem_recebida_independente_do_registro(self):
        b=self.bancada
        for modo in (0,1,256,257,65535):
            m=mundo_estrutura(tipo=5,indice=0,origem=0x808)
            b.carregar_navegacao(m)
            b.aplicar_terreno(65536,0x505,65535)
            m.aplicar_terreno_estrutura(65536,0x505,65535)
            b.resetar_terreno(65536,modo);m.resetar_terreno_estrutura(65536,modo)
            b.remover_regioes(65536);m.remover_regioes_estrutura(65536)
            self._conferir(m,modo)

    def test_estrutura_retirada_reconecta_componentes_de_cores(self):
        b=self.bancada; m=mundo_estrutura(9,indice=0,origem=0x505)
        b.carregar_navegacao(m)
        for indice,origem in ((0,0x505),(1,0x507),(2,0x506)):
            m.estruturas[indice*276+8]=9
            struct.pack_into('<H',m.estruturas,indice*276+2,origem)
            b.cpu.mem_write(0x49a0c8+indice*276,bytes(m.estruturas[indice*276:(indice+1)*276]))
            b.aplicar_terreno(indice,origem,600);m.aplicar_terreno_estrutura(indice,origem,600)
            self._conferir(m,indice)
        self.assertEqual(m.cores_estruturas.grade[0x505],m.cores_estruturas.grade[0x507])
        b.resetar_terreno(2,1);m.resetar_terreno_estrutura(2,1)
        b.remover_regioes(2);m.remover_regioes_estrutura(2)
        self._conferir(m,'componentes_separados')
        self.assertNotEqual(m.cores_estruturas.grade[0x505],m.cores_estruturas.grade[0x507])

    def test_trajetos_com_aplicacao_e_remocao_durante_o_movimento(self):
        from demonstrar_terreno_estruturas import preparar_terreno_cenario,aplicar_cenario,retirar_cenario
        b=self.bancada
        for nome in ('edificio','edificio_retirado','parede'):
            m,maquina,estruturas=preparar_terreno_cenario(nome)
            m.solucionador.identificadores_rotas=tuple(b.grades['rotas']+i*512 for i in range(800))
            b.carregar(maquina.programa);b.carregar_navegacao(m)
            for indice,tipo,origem in estruturas:b.aplicar_terreno(indice,origem,400)
            aplicar_cenario(m,estruturas);self._conferir(m,(nome,'aplicacao'))
            self.assertEqual(maquina.postar(0,1,(0,0x40a)),b.postar(0,1,(0,0x40a)))
            self.assertEqual(maquina.atualizar(0),b.atualizar(0))
            for ciclo in range(1,1201):
                if nome=='edificio_retirado' and ciclo==28:
                    for indice,_,_ in estruturas:
                        b.resetar_terreno(indice,1);b.remover_regioes(indice);b.resetar_terreno(indice,0)
                    retirar_cenario(m,estruturas);self._conferir(m,(nome,'retirada'))
                b.pulso_navegacao(0);m.atualizar_movimento(0,maquina)
                self._conferir(m,(nome,ciclo))
                self.assertEqual(b.memoria_tarefas(),bytes(maquina.memoria))
                self.assertFalse(m.regioes[m.palavra(0,8)]&0x8000)
                if m.unidades[2]==7:break
            else:self.fail('O trajeto não terminou: '+nome)
            self.assertEqual(m.palavra(0,8),0x40a)
            self.assertEqual(maquina.atualizar(0),b.atualizar(0))
            self.assertEqual(maquina.ativas,0)
