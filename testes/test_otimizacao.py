"""Propriedades observáveis do teste de linha e da compactação de laços."""
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from navegacao_unidades import MundoNavegacao
from otimizacao_caminhos import ContextoLinha, compactar_lacos, direcao_busca, otimizar_rota, testar_linha


class Otimizacao(unittest.TestCase):
    def setUp(self):
        self.mundo = MundoNavegacao(16, 16)
        self.contexto = ContextoLinha(self.mundo, 0, 1, 1, 0)

    def test_linha_inclui_origem_e_exclui_destino(self):
        r = testar_linha(self.contexto, 0x505, 0x508)
        self.assertTrue(r.permitido)
        self.assertEqual(r.celulas, (0x505, 0x506, 0x507))
        self.assertEqual(direcao_busca(0x505, 0x505), 5)

    def test_recusa_inicial_preserva_contador_e_falha_posterior_tem_prefixo(self):
        self.mundo.atributos[0x506] = 1
        self.assertIsNone(testar_linha(self.contexto, 0x505, 0x508).contador)
        self.mundo.atributos[0x506], self.mundo.atributos[0x507] = 0, 1
        r = testar_linha(self.contexto, 0x505, 0x508)
        self.assertFalse(r.permitido)
        self.assertEqual(r.celulas, (0x505, 0x506))

    def test_contador_de_255_nao_e_garantia_de_destino(self):
        self.mundo.largura = self.mundo.altura = 256
        r = testar_linha(self.contexto, 0, 0xfffe)
        self.assertTrue(r.permitido)
        self.assertEqual(r.contador, 255)
        self.assertEqual(r.celulas[-1], 0xfefe)

    def test_compactacao_reconhece_laco_e_adjacencia_com_overflow(self):
        self.assertEqual(compactar_lacos([0x505, 0x506, 0x607, 0x606, 0x605]), [0x505, 0x605])
        self.assertEqual(compactar_lacos([0x500, 0x502, 0x5ff]), [0x500, 0x5ff])

    def test_buffer_vazio_conserva_cauda(self):
        b = bytearray(range(256)) * 2
        struct.pack_into('<H', b, 0, 0)
        self.assertEqual(otimizar_rota(self.contexto, b), bytes(b))
        with self.assertRaises(ValueError): otimizar_rota(self.contexto, b[:4])
