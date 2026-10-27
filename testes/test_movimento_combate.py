import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from movimento import (direcao_entre_celulas, celula_vizinha, atualizar_orientacao,
                       integrar_prefixo_passo, pode_avancar, parametros_tipo)
from combate import dano_bruto_unidade, reduzir_dano, aplicar_dano_parcial


class Movimento(unittest.TestCase):
    def test_direcoes_e_bordas_sem_colisao(self):
        self.assertEqual(direcao_entre_celulas(0x0808, 0x0509), 7)
        self.assertEqual(direcao_entre_celulas(0x0808, 0x0808), 0)
        self.assertEqual(celula_vizinha(0, 1, 64, 64), 65535)
        self.assertEqual(celula_vizinha(0, 11, 64, 64), 257)
        self.assertEqual(celula_vizinha(0, 2, 64, 64), 0)
        with self.assertRaises(ValueError):
            celula_vizinha(65, 1, 64, 64)

    def test_giro_meia_volta_e_permissao_de_avanco(self):
        self.assertEqual(atualizar_orientacao(9, 1, 0, 1), (16, 0))
        self.assertEqual(atualizar_orientacao(1, 16, 0, 1), (1, 0))
        self.assertTrue(pode_avancar(1, 15))
        self.assertFalse(pode_avancar(1, 14))

    def test_travessia_soldado_16_incrementos_sem_desconto(self):
        passo = parametros_tipo(0)['incremento_passo']
        progresso = 0
        for n in range(1, 17):
            estado = integrar_prefixo_passo(0, 0, progresso, 9, passo)
            progresso = estado['progresso']
            self.assertEqual(estado['chegou'], n == 16)
        # Este teste não estabelece uma duração em segundos.


class CombateParcial(unittest.TestCase):
    def test_adicao_truncada_e_reducao_com_sinal(self):
        self.assertEqual(dano_bruto_unidade(250, 10), 4)
        self.assertEqual(reduzir_dano(20, 1, 4), 15)
        self.assertEqual(reduzir_dano(20, 1, 19), 0)
        self.assertEqual(reduzir_dano(20, 1, 20), 1)
        self.assertEqual(reduzir_dano(200), 1)

    def test_protecao_apos_limite_e_morte(self):
        self.assertEqual(aplicar_dano_parcial(100, 20)['vida'], 80)
        self.assertTrue(aplicar_dano_parcial(20, 20)['entra_no_ramo_morte'])
        cura_acidental = aplicar_dano_parcial(100, 0, True)
        self.assertEqual(cura_acidental, dict(vida=101, dano_com_sinal=-1, entra_no_ramo_morte=False))
