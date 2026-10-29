"""Live unit-bonus binding by identity (0x4dfba0 / 0x4965ae); the constructor stays the copying fixture form."""
from pathlib import Path
import random
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from bonus_unidades import (BonusUnidades, BASE_BONUS_UNIDADES, BASE_TIPOS_UNIDADES,  # noqa: E402
                            TAMANHO_BONUS_UNIDADES, TAMANHO_TIPOS_UNIDADES)


class MapaPlano:
    """A DGROUP-like arena with ``vista`` over original addresses."""
    BASE = 0x494000

    def __init__(self, rng):
        self.arena = bytearray(rng.randbytes(0x523000 - self.BASE))

    def vista(self, endereco, tamanho):
        return memoryview(self.arena)[endereco - self.BASE:endereco - self.BASE + tamanho]


class BonusVivo(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(0x4dfba0)

    def test_live_binding_keeps_the_callers_buffers(self):
        tabela, tipos = bytearray(self.rng.randbytes(1872)), bytearray(self.rng.randbytes(1300))
        b = BonusUnidades.vivo(tabela, tipos_unidades=tipos)
        self.assertIs(b.memoria, tabela)
        self.assertIs(b.tipos_unidades, tipos)
        # A store by another owner after construction is seen by the next query.
        pos = 2 * 468 + 7 * 18
        tabela[pos + 4:pos + 6] = (0x1234).to_bytes(2, 'little')
        self.assertEqual(b.consultar(2, 7, 3), 0x1234)
        # Economy's own stores land in the caller's buffer.
        b.reiniciar()
        legado = BonusUnidades(bytes(tabela), tipos_unidades=bytes(tipos))
        legado.reiniciar()
        self.assertEqual(bytes(tabela), bytes(legado.memoria))

    def test_memory_map_binding_writes_the_original_addresses(self):
        mapa = MapaPlano(self.rng)
        b = BonusUnidades.da_memoria(mapa)
        antes = bytes(mapa.arena)
        b.definir(1, 4, 2, 0x77)
        mudados = [i + MapaPlano.BASE for i in range(len(antes)) if antes[i] != mapa.arena[i]]
        self.assertTrue(mudados)
        self.assertTrue(all(BASE_BONUS_UNIDADES <= a < BASE_BONUS_UNIDADES + TAMANHO_BONUS_UNIDADES for a in mudados))
        self.assertEqual(b.consultar(1, 4, 2), 0x77)
        self.assertEqual(bytes(b.tipos_unidades),
                         bytes(mapa.arena[BASE_TIPOS_UNIDADES - MapaPlano.BASE:][:TAMANHO_TIPOS_UNIDADES]))

    def test_queries_equal_the_fixture_form(self):
        for _ in range(4):
            tabela, tipos = bytearray(self.rng.randbytes(1872)), bytearray(self.rng.randbytes(1300))
            vivo, legado = BonusUnidades.vivo(tabela, tipos_unidades=tipos), BonusUnidades(tabela, tipos_unidades=tipos)
            for jogador in range(4):
                for tipo in range(26):
                    for seletor in range(16):
                        self.assertEqual(vivo.consultar(jogador, tipo, seletor, ecx=0xabc),
                                         legado.consultar(jogador, tipo, seletor, ecx=0xabc))

    def test_constructor_remains_a_copy(self):
        tabela = bytearray(1872)
        b = BonusUnidades(tabela)
        self.assertIsNot(b.memoria, tabela)
        tabela[0] = 9
        self.assertEqual(b.memoria[0], 0)

    def test_rejects_non_live_buffers_before_binding(self):
        bom_t, bom_u = bytearray(1872), bytearray(1300)
        grande = bytearray(3744)
        for tabela, tipos in ((bytes(1872), bom_u), (bom_t, bytes(1300)),
                              (memoryview(bytes(1872)), bom_u), (bytearray(1871), bom_u), (bom_t, bytearray(1301)),
                              (memoryview(grande)[::2], bom_u), (memoryview(bytearray(1872 * 4)).cast('I'), bom_u),
                              (bom_t, bom_t[:0]), (list(bom_t), bom_u)):
            with self.assertRaises(ValueError):
                BonusUnidades.vivo(tabela, tipos_unidades=tipos)
        mesmo = bytearray(1872)
        with self.assertRaises(ValueError):
            BonusUnidades.vivo(mesmo, tipos_unidades=mesmo)
        self.assertEqual(bom_t, bytearray(1872))


if __name__ == '__main__':
    unittest.main()
