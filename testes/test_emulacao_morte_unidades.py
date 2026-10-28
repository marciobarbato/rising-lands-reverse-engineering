"""Complete original physical returns and exact unsupported native checkpoints."""
import os
import struct
import unittest
from test_morte_unidades import preparar, iniciar_morte_unidade, DependenciaMorteUnidade


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional x86: RISING_EMULAR=1')
class DiferencialMorteUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_morte_unidades import BancadaMorteUnidades
        cls.bancada = BancadaMorteUnidades()

    def conferir(self, m):
        self.assertEqual(self.bancada.conferir_fisica(m), [])

    def test_complete_ordinary_types_states_indices_and_reservations(self):
        for tipo in (*range(11), *range(18, 26)):
            for indice in (0, 799):
                for estado in (1, 7, 14):
                    for passo in (0x505, 0x506):
                        m = preparar(tipo, indice, estado, passo=passo)
                        self.bancada.carregar_fisica(m)
                        self.bancada.morrer(0xabcd0000 | indice)
                        iniciar_morte_unidade(m, 0xabcd0000 | indice)
                        self.conferir(m)

    def test_inactive_and_control_guard_complete_returns(self):
        for dono in (0, 3, 4, 200):
            for estado in (0, 4, 7):
                for controle in (0, 2, 255):
                    m = preparar(dono=dono, estado=estado)
                    if estado in (0, 4):
                        m.unidades[7*276+1] = 255
                    if dono < 4:
                        m.controle_jogadores[dono] = controle
                    if dono < 4 and controle != 2:
                        struct.pack_into('<I', m.unidades, 7*276+0x10c, 0)
                    self.bancada.carregar_fisica(m)
                    self.bancada.morrer(7)
                    iniciar_morte_unidade(m, 7)
                    self.conferir(m)

    def test_dependency_boundaries_preserve_exact_prior_world_state(self):
        for variante, parada in (('special', 0x444c7e), ('group', 0x482c58),
                                  ('sound', 0x48a446), ('visible', 0x440c5d),
                                  ('bag', 0x443dfc), ('selected', 0x472683)):
            for indice in (0, 799):
                m = preparar(indice=indice)
                p = indice*276
                if variante == 'special': m.unidades[p+0xdc] = 4
                elif variante == 'group': struct.pack_into('<I', m.unidades, p+0x10c, 0)
                elif variante == 'sound': struct.pack_into('<I', m.unidades, p+0x104, 0)
                elif variante == 'visible': m.descoberto[0][0x505] = 0
                elif variante == 'bag': struct.pack_into('<H', m.unidades, p+0xa, 1)
                else: m.unidades[p+0xbd] = 1
                self.bancada.carregar_fisica(m)
                self.bancada.morrer(indice, parada)
                with self.assertRaises(DependenciaMorteUnidade):
                    iniciar_morte_unidade(m, indice)
                self.conferir(m)

    def test_vehicle_effect_dependencies_follow_physical_cleanup(self):
        for tipo in range(11, 18):
            m = preparar(tipo=tipo)
            parada = 0x46e44c if tipo == 16 else 0x4704dc
            self.bancada.carregar_fisica(m)
            self.bancada.morrer(7, parada)
            with self.assertRaises(DependenciaMorteUnidade):
                iniciar_morte_unidade(m, 7)
            self.conferir(m)
