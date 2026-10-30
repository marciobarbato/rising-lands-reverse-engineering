"""The bounded P4 verdict executes both default and explicit-boundary rendering."""
import unittest

from validar_fronteira_p4_graficos import validar
from validar_sondas_graficos_m3 import AQUI


class FronteiraP4Graficos(unittest.TestCase):
    def test_native_boundary_and_exact_rendered_surface(self):
        result = validar(AQUI / 'evidencias/p4-texto-484-auditoria.json')
        self.assertEqual(result['native_equal'], 356)
        self.assertEqual(result['explicit_boundary_surfaces_equal'], 1)
        self.assertIsNone(result['explicit_boundary_stop'])
