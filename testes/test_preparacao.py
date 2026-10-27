"""Propriedades da preparação e dos dados iniciais, sem Unicorn."""
import struct
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from candidatos_rota import iniciar_candidatos, selecionar_candidato
from navegacao_unidades import MundoNavegacao
from otimizacao_caminhos import ContextoLinha
from preparacao_destino import celulas_do_anel, preparar_destino, regiao_preservada


class Preparacao(unittest.TestCase):
    def setUp(self):
        self.m = MundoNavegacao(16, 16)
        self.m.unidades[1:3] = bytes([7, 2])
        self.m.palavra(0, 8, 0x505)
        self.m.palavra(0, 0x7c, 0x505)

    def test_destino_livre_mesma_celula_e_regiao_distinta(self):
        p = preparar_destino(self.m, 0, 0x505, 0x50a)
        self.assertEqual((p.retorno, p.concluida, p.status, p.registrar_extremos), (True, 0, 1, True))
        p = preparar_destino(self.m, 0, 0x505, 0x505)
        self.assertEqual((p.concluida, p.sucesso, p.registrar_extremos), (1, 1, False))
        self.m.regioes[0x50a] = 1
        p = preparar_destino(self.m, 0, 0x505, 0x50a)
        self.assertEqual((p.retorno, p.status, p.concluida), (False, 7, 1))

    def test_anel_preserva_ordem_e_repeticao_das_laterais(self):
        self.assertEqual(list(celulas_do_anel(0x505, 1, 16, 16)),
                         [0x404, 0x405, 0x406, 0x604, 0x605, 0x606, 0x404, 0x406])
        self.m.atributos[0x50a] = 1
        p = preparar_destino(self.m, 0, 0x505, 0x50a)
        self.assertEqual((p.destino, p.alternativa, p.status), (0x409, 0x409, 2))

    def test_anel_da_origem_precede_consulta_e_limite_e_29(self):
        self.m.atributos[:] = bytes([1]) * 65536
        p = preparar_destino(self.m, 0, 0x505, 0x508)
        self.assertEqual((p.destino, p.status, p.sucesso), (0x505, 2, 1))
        self.m.largura = self.m.altura = 64
        p = preparar_destino(self.m, 0, 0x505, 0x2828)
        self.assertEqual((p.destino, p.status), (0xffff, 7))

    def test_regiao_sob_unidade_e_estrutura_sem_recursao(self):
        self.m.regioes[0x505] = 0x4000 | (1 << 3) | 2
        self.m.palavra(1, 0xfe, 0x8007)
        self.assertEqual(regiao_preservada(self.m, 0x505), 0x8007)
        self.m.regioes[0x505] = 0x8000 | (2 << 5) | 3
        struct.pack_into('<H', self.m.estruturas, 2 * 276 + 0xcc + 6, 37)
        self.assertEqual(regiao_preservada(self.m, 0x505), 37)

    def test_inicio_escolhe_obstaculo_mais_alinhado_e_deduplica_regioes(self):
        for c in (0x504, 0x404, 0x405, 0x406, 0x506):
            self.m.atributos[c], self.m.regioes[c] = 1, 7
        r = iniciar_candidatos(ContextoLinha.da_unidade(self.m, 0), 0x505, 0x50a)
        self.assertEqual(r.obstaculo_proximo, 0x506)
        self.assertEqual(r.regioes, (7,))
        self.assertFalse(r.todos_bloqueados)

    def test_inicio_sem_saida_e_empate_conserva_primeiro(self):
        self.m.atributos[:] = bytes([1]) * 65536
        r = iniciar_candidatos(ContextoLinha.da_unidade(self.m, 0), 0x505, 0x50a)
        self.assertTrue(r.todos_bloqueados)
        self.assertEqual(r.obstaculo_proximo, 0x506)
        self.assertEqual(r.regioes, ())

    def test_selecao_de_ocupante_preserva_escrita_no_segundo_buffer(self):
        buffers = [bytearray(512), bytearray(512)]
        for b in buffers: struct.pack_into('<H', b, 0, 255)
        registros = [bytearray(10), bytearray(10)]
        registros[0][4], registros[0][8] = 1, 17
        r = selecionar_candidato(buffers, (5,6), registros, 1)
        self.assertEqual((r.escolhido, r.status, r.semente), (0,4,1))
        self.assertEqual([struct.unpack_from('<H', b)[0] for b in r.buffers], [255,17])

    def test_desempate_usa_rng_so_quando_custos_iguais(self):
        buffers, registros = (bytes(512), bytes(512)), (bytes(10), bytes(10))
        r = selecionar_candidato(buffers, (2,3), registros, 1)
        self.assertEqual((r.escolhido,r.semente), (0,1))
        r = selecionar_candidato(buffers, (2,2), registros, 1)
        self.assertEqual((r.escolhido,r.semente), (1,16807))
