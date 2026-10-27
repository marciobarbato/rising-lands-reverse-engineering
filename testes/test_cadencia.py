import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ferramentas'))
from cadencia import avancar_contadores, deve_desenhar, proximo_aleatorio


class Cadencia(unittest.TestCase):
    def test_contadores_acumulados_e_overflow(self):
        valores = (0, 0, 0)
        for _ in range(6):
            valores = avancar_contadores(*valores)
        self.assertEqual(valores, (6, 3, 2))
        self.assertEqual(avancar_contadores(0xffffffff, 0xffffffff, 0xffffffff), (0, 0, 0))

    def test_divisor_e_desenho_forcado(self):
        self.assertEqual([i for i in range(1, 13) if deve_desenhar(i, 4)], [4, 8, 12])
        self.assertTrue(deve_desenhar(1, 4, True))
        with self.assertRaises(ValueError):
            deve_desenhar(1, 0)

    def test_sequencia_aleatoria_e_semente_degenerada(self):
        estado, primeiro = proximo_aleatorio(1, 100)
        self.assertEqual((estado, primeiro), (16807, 7))
        self.assertEqual(proximo_aleatorio(estado, 100), (282475249, 49))
        self.assertEqual(proximo_aleatorio(0, 100), (0x7fffffff, 47))
