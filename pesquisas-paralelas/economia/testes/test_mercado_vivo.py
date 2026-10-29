"""Economia.vivo / Mercado.vivo bind the live resource table, player records and market buffers by identity."""
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from economia import Economia  # noqa: E402
from mercado import BUFFERS, Mercado  # noqa: E402


def buffers():
    return {n: bytearray(t) for n, (_, t) in BUFFERS.items()}


class EconomiaViva(unittest.TestCase):
    def test_binds_the_given_buffer_and_sees_later_writes(self):
        tabela = bytearray(128)
        e = Economia.vivo(tabela)
        self.assertIs(e.memoria, tabela)
        struct.pack_into('<H', tabela, 32 * 2 + 8 * 1 + 2, 77)   # player 2, food total
        self.assertEqual(e.consultar(2).comida, 77)
        self.assertTrue(e.suficiente(2, 77, 0, 0))
        self.assertFalse(e.suficiente(2, 78, 0, 0))

    def test_memoryview_slice_writes_reach_the_owner(self):
        dono = bytearray(256)
        e = Economia.vivo(memoryview(dono)[16:144])
        struct.pack_into('<H', dono, 16 + 2, 5)
        self.assertEqual(e.consultar(0).pecas, 5)

    def test_rejects_copies_and_wrong_sizes(self):
        for ruim in (bytes(128), bytearray(127), memoryview(bytes(128))):
            with self.assertRaises(ValueError):
                Economia.vivo(ruim)


class MercadoVivo(unittest.TestCase):
    def test_binds_every_buffer_by_identity(self):
        tabela, jogadores, b = bytearray(128), bytearray(80), buffers()
        mercado = Mercado.vivo(Economia.vivo(tabela), jogadores=jogadores, **b)
        self.assertIs(mercado.economia.memoria, tabela)
        self.assertIs(mercado.jogadores, jogadores)
        for nome, buffer in b.items():
            self.assertIs(getattr(mercado, nome), buffer)
        jogadores[20 * 3 + 1] = 1
        jogadores[20 * 1 + 6] = 1 << 2
        self.assertEqual(mercado.tipo_jogador(3), 1)
        self.assertEqual(mercado.aliado(1, 2), 1)
        self.assertEqual(mercado.aliado(2, 1), 0)

    def test_requires_a_live_economy_and_all_buffers(self):
        b = buffers()
        with self.assertRaises(TypeError):
            Mercado.vivo(bytearray(128), jogadores=bytearray(80), **b)
        incompletos = dict(b)
        incompletos.pop('contatos')
        with self.assertRaises(TypeError):
            Mercado.vivo(Economia.vivo(bytearray(128)), jogadores=bytearray(80), **incompletos)
        with self.assertRaises(ValueError):
            Mercado.vivo(Economia.vivo(bytearray(128)), jogadores=bytes(80), **b)


if __name__ == '__main__':
    unittest.main()
