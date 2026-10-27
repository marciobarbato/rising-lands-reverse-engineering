"""Contratos públicos e cenários de fronteira das reconstruções."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from caminhos import aliados, resolver_regiao, mesma_regiao, serializar_rota, proxima_celula
from ia import EstadoIA, atualizar_ia, ETAPAS


class CaminhosIA(unittest.TestCase):
    def test_alianca_nao_e_simetrica(self):
        self.assertTrue(aliados(0, 1, [2, 0, 0, 0, 0]))
        self.assertFalse(aliados(1, 0, [2, 0, 0, 0, 0]))
        self.assertTrue(aliados(200, 200, []))
        self.assertFalse(aliados(200, 0, []))

    def test_rotulo_sob_ocupacao_nao_e_recursivo(self):
        self.assertEqual(resolver_regiao(0x4004, [[0x8001, 2, 3, 4]], []), 0x8001)
        self.assertEqual(resolver_regiao(0x8023, [], {1: [0, 0, 0, 17]}), 17)
        self.assertFalse(mesma_regiao(0, 1, 1, 1, [0, 0], [], []))

    def test_rota_consumida_do_final(self):
        self.assertEqual(serializar_rota([0x102, 0x203]), b'\x02\x00\x03\x02\x02\x01')
        self.assertEqual(proxima_celula(serializar_rota([0x102, 0x203])), 0x102)
        self.assertIsNone(proxima_celula(serializar_rota([])))
        with self.assertRaises(ValueError):
            serializar_rota([0] * 256)

    def test_ia_decimo_ciclo_inativa(self):
        estado, chamadas = EstadoIA(), []
        def chamar(endereco, *argumentos):
            chamadas.append(endereco)
            return 0
        for _ in range(9):
            atualizar_ia(1, 2, estado, 0, 0, chamar)
        self.assertEqual(estado.inativo, 0)
        chamadas.clear()
        atualizar_ia(1, 2, estado, 0, 0, chamar)
        self.assertEqual(chamadas, [0x483d95])
        self.assertEqual(estado.inativo, 1)
        chamadas.clear()
        atualizar_ia(1, 2, estado, 100, 100, chamar)
        self.assertEqual(chamadas, [])

    def test_ia_para_no_primeiro_retorno(self):
        chamadas = []
        def chamar(endereco, *argumentos):
            chamadas.append(endereco)
            return 0x1a1a000e if endereco == ETAPAS[2] else 0
        self.assertEqual(atualizar_ia(2, 3, EstadoIA(), 1, 1, chamar), 0x1a1a000e)
        self.assertEqual(chamadas, list(ETAPAS[:3]))
