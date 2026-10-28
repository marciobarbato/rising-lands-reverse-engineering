"""Type-4 modifier callback boundary, including its two higher-level callers."""
import os
import random
import unittest

from inicializacao_ataque import (CaracteristicasTipo, caracterizar_tipo,
    definir_tipo, preparar_apos_carga_missao)
from animacao_disparo import BuscaAtaque


class ModifierUnavailable(NotImplementedError):
    pass


def unavailable(*args):
    raise ModifierUnavailable('Modifier 12 provider boundary')


class ContratosOrdemTipo4(unittest.TestCase):
    def test_query_sees_inherited_frame_and_common_amount(self):
        u = bytearray([173] * 276)
        u[0], u[1] = 0, 4
        seen = []
        def query(owner, kind):
            seen.append((owner, kind, u[0x7a], u[0xda]))
            raise ModifierUnavailable()
        with self.assertRaises(ModifierUnavailable):
            caracterizar_tipo(memoryview(u), 0x1234, query)
        self.assertEqual(seen, [(0, 4, 173, 1)])
        self.assertEqual((u[0x7a], u[0xda]), (173, 1))

    def test_callback_return_then_frame_then_amount(self):
        u = bytearray([173] * 276)
        u[0], u[1] = 0, 4
        def query(owner, kind):
            u[0x7a] = 88
            return 255
        caracterizar_tipo(u, 0, query)
        self.assertEqual((u[0x7a], u[0xda]), (5, 9))


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional: RISING_EMULAR=1')
class DiferencialOrdemTipo4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_inicializacao import BancadaInicializacao
        cls.b = BancadaInicializacao()
        cls.modifier_stops = 0
        cls.successful_returns = 0

    def original(self, u, index, entry, c, registers=None, stack=None, stop=0x428cc0):
        from bancada_inicializacao import INICIALIZACAO
        intervals = INICIALIZACAO + [(0x46ad8b, 0x46b01e), (0x441fff, 0x442045)]
        self.b.parametros_tipo(4, c, u[0], mod12=255)
        self.b.escrever_unidade(u, index)
        result = self.b.executar(entry, intervals, registers or dict(EAX=index),
            parada=stop, pilha=stack)
        return result

    def test_original_characterization_dependency_boundary(self):
        rng = random.Random(0x457845)
        c = CaracteristicasTipo(0x1234, 0x2345, 0x3456)
        for owner in range(4):
            for frame in (0, 5, 255):
                for index in (0, 7, 799):
                    u = bytearray(rng.randbytes(276))
                    u[0], u[1], u[0x7a] = owner, 4, frame
                    r = self.original(u, index, 0x457350, c)
                    self.assertEqual((r['EAX'] & 255, r['EDX'] & 255, r['EBX'] & 255), (owner, 12, 4))
                    with self.assertRaises(ModifierUnavailable):
                        caracterizar_tipo(memoryview(u), c.recarga, unavailable)
                    self.assertEqual(self.b.ler_unidade(index), u)
                    self.assertEqual(u[0x7a], frame)
                    type(self).modifier_stops += 1

    def test_original_type_conversion_dependency_boundary(self):
        rng = random.Random(0x457b87)
        c = CaracteristicasTipo(0x1234, 0x2345, 0x3456)
        for owner in range(4):
            for state in (0, 4, 7):
                for index in (0, 7, 799):
                    u = bytearray(rng.randbytes(276))
                    u[0], u[1], u[2], u[0x7a] = owner, 12, state, 222
                    search = BuscaAtaque(index, 1, 1, 0x12345678)
                    self.b.preparar_busca(search)
                    r = self.original(u, index, 0x457b87, c,
                        dict(EAX=index, EDX=0x8080, EBX=255, ECX=4))
                    self.assertEqual(r['EIP'], 0x428cc0)
                    def modifier(o, t, selector):
                        self.assertEqual((o, t, selector), (owner, 4, 12))
                        raise ModifierUnavailable()
                    with self.assertRaises(ModifierUnavailable):
                        definir_tipo(memoryview(u), index, 0x8080, 255, 4, c,
                                     unavailable, modifier, search)
                    self.assertEqual(self.b.ler_unidade(index), u)
                    self.assertEqual(self.b.ler_busca(), search)
                    self.assertEqual(u[0x7a], 222)
                    type(self).modifier_stops += 1

    def test_original_mission_postload_dependency_boundary(self):
        rng = random.Random(0x46ad8b)
        c = CaracteristicasTipo(0x1234, 0x2345, 0x3456)
        for owner in range(4):
            for state in (4, 7, 14):
                for index in (0, 7, 799):
                    u = bytearray(rng.randbytes(276))
                    u[0], u[1], u[2], u[0x7a] = owner, 4, state, 222
                    import struct
                    self.original(u, index, 0x46ad8b, c,
                        registers={'ESP': 0x2008004}, stack={12: struct.pack('<I', index)})
                    with self.assertRaises(ModifierUnavailable):
                        preparar_apos_carga_missao(memoryview(u), c, unavailable)
                    self.assertEqual(self.b.ler_unidade(index), u)
                    self.assertEqual(u[0x7a], 222)
                    type(self).modifier_stops += 1

    def test_original_success_and_special_owner_bypass(self):
        from bancada_combate import RETORNO
        c = CaracteristicasTipo(5, 36, 0x1234)
        for owner in (0, 1, 2, 3, 4, 200):
            for frame in (0, 5, 255):
                u = bytearray([173] * 276)
                u[0], u[1], u[0x7a] = owner, 4, frame
                self.original(u, 7, 0x457350, c, stop=RETORNO)
                caracterizar_tipo(memoryview(u), c.recarga, lambda *args: 255)
                self.assertEqual(self.b.ler_unidade(7), u)
                self.assertEqual((u[0x7a], u[0xda]), (5, 10 if owner in (4, 200) else 9))
                type(self).successful_returns += 1
