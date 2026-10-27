"""Navegação local e geração de regiões sem dependência de Unicorn."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ferramentas'))
from navegacao_unidades import MundoNavegacao
from test_emulacao_navegacao import preparar


class Navegacao(unittest.TestCase):
    def test_desvio_local_e_pedido_de_busca(self):
        m=preparar();m.atributos[0x506]=1
        self.assertTrue(m.escolher_direto(0))
        self.assertEqual(m.palavra(0,0x7c),0x406)
        m=preparar();m.atributos[0x506]=m.atributos[0x406]=1
        self.assertFalse(m.escolher_direto(0))
        self.assertEqual(m.unidades[0x88],3)
        with self.assertRaises(NotImplementedError):m.atualizar_estado_caminho(0)

    def test_espera_da_busca_nao_bloqueia_passo_em_andamento(self):
        m=preparar();m.unidades[0x88]=3;m.unidades[0x86]=1
        m.busca.ocupada=1;m.busca.unidade=1
        self.assertTrue(m.atualizar_estado_caminho(0))
        self.assertEqual(m.busca.unidade,1)
        m.unidades[0x86]=0
        self.assertFalse(m.atualizar_estado_caminho(0))
        self.assertEqual(m.unidades[0x88],3)

    def test_estados_inativos_e_espera_20(self):
        m=preparar();m.unidades[0x88]=1
        self.assertFalse(m.atualizar_estado_caminho(0));self.assertEqual(m.unidades[0x88],0)
        m.unidades[0x88]=6
        for _ in range(19):m.atualizar_estado_caminho(0)
        self.assertEqual(m.unidades[0x88],6)
        m.atualizar_estado_caminho(0)
        self.assertEqual((m.unidades[0x88],m.unidades[0x8b]),(3,0))

    def test_rota_bloqueada_e_vazia_retornam_ao_movimento_direto(self):
        from caminhos import serializar_rota
        m=preparar();m.unidades[0x88]=5;m.rotas[0]=bytearray(serializar_rota([0x506]))
        m.atributos[0x506]=1
        self.assertFalse(m.escolher_da_rota(0));self.assertEqual(m.unidades[0x88],0)
        m.unidades[0x88]=5;m.rotas[0]=bytearray(2)
        self.assertFalse(m.escolher_da_rota(0));self.assertEqual(m.unidades[0x88],0)

    def test_remapeamento_ignora_colisao_nao_natural(self):
        m=preparar()
        m.atributos[0x506]=1
        m.refazer_regioes()
        a=m.palavra(0,0xfa)
        self.assertEqual(a,m.regioes[0x506])
        self.assertEqual(m.regioes[0x1000],0)
        self.assertEqual(m.atributos[0x1000],1)
