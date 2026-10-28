"""Exact query widths, neutral-owner bypass, dispatch and incoming-ECX returns."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from bonus_unidades import BonusUnidades, capacidade_tipo, TAMANHO_BONUS_UNIDADES


class ExemplosBonusUnidades(unittest.TestCase):
    def test_fixed_capacities_and_byte_inputs(self):
        self.assertEqual([capacidade_tipo(t) for t in range(26)],
                         [0,0,0,0,0,1,1,1,0,0,0,1,2,5,1,3,1,6,0,0,0,0,0,0,0,0])
        self.assertEqual(capacidade_tipo(0x1000d), 5)
        self.assertEqual(capacidade_tipo(255), 0)

    def test_conversion_selectors_are_bytes_not_words(self):
        b = BonusUnidades()
        pos = 3 * 468 + 25 * 18
        b.memoria[pos + 11:pos + 13] = bytes((255, 0x81))
        b.memoria[pos + 16:pos + 18] = bytes((0x80, 0xff))
        self.assertEqual(b.consultar(3, 25, 1), 255)
        self.assertEqual(b.consultar(3, 25, 12), 128)
        self.assertEqual(b.consultar(0x103, 0x119, 0x10c), 128)

    def test_neutral_bypass_precedes_type_and_selector_validation(self):
        b = BonusUnidades(b'\xff' * TAMANHO_BONUS_UNIDADES)
        for j in (4, 200, 0x104, 0x1c8):
            self.assertEqual(b.consultar(j, 255, 255, ecx=0xdeadbeef), 0)

    def test_default_dispatch_preserves_caller_ecx_without_lookup(self):
        b = BonusUnidades()
        for seletor in (8, 13, 255, 0x108):
            self.assertEqual(b.consultar(255, 255, seletor, ecx=-1), 0xffffffff)
            self.assertEqual(b.consultar(255, 255, seletor, ecx=0x123456789), 0x23456789)

    def test_unsigned_words_and_opaque_bytes(self):
        b = BonusUnidades(bytes(range(18)) * 104)
        for seletor, offset in ((0,0), (3,4), (5,8)):
            struct.pack_into('<H', b.memoria, offset, 0x8000 + seletor)
            self.assertEqual(b.consultar(0, 0, seletor), 0x8000 + seletor)
        antes = bytes(b.memoria)
        for seletor in range(256):
            b.consultar(0, 0, seletor)
        self.assertEqual(bytes(b.memoria), antes)

    def test_guarded_lookup_domain_only_when_table_is_read(self):
        with self.assertRaises(ValueError):
            BonusUnidades(bytes(18))
        b = BonusUnidades()
        for j, t in ((5,0), (255,0), (0,26), (3,255)):
            with self.assertRaises(ValueError):
                b.consultar(j, t, 1)
        self.assertEqual(b.consultar(255, 255, 8, ecx=7), 7)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional original x86: RISING_EMULAR=1')
class DiferencialBonusUnidades(unittest.TestCase):
    b = None

    @classmethod
    def setUpClass(cls):
        from bancada_bonus_unidades import BancadaBonusUnidades
        cls.b = BancadaBonusUnidades()

    def setUp(self):
        self.rng = random.Random(0x428cc0)
        self.bonus = BonusUnidades(self.rng.randbytes(TAMANHO_BONUS_UNIDADES))
        self.b.carregar_bonus(self.bonus)

    def comparar(self, j, t, s, ecx=0):
        from emulador import RETORNO, PILHA
        esperado = self.bonus.consultar(j, t, s, ecx=ecx)
        regs = self.b.consultar(j, t, s, ecx)
        self.assertEqual(regs['EAX'], esperado)
        self.assertEqual((regs['EIP'], regs['ESP']), (RETORNO, PILHA + 0x8004))
        self.assertEqual(regs['ECX'], ecx & 0xffffffff)
        self.assertEqual(regs['EBX'], t & 0xffffffff)
        self.assertTrue(self.b.conferir_memoria())

    def test_1352_valid_owner_type_selector_combinations(self):
        for j in range(4):
            for t in range(26):
                for s in range(13):
                    self.comparar(j, t, s, self.rng.getrandbits(32))

    def test_all_selector_bytes_bypasses_and_untouched_invalid_indices(self):
        for s in range(256):
            for j in (0, 4, 200):
                self.comparar(j | 0xabcd0000, 7 | 0xfade0000, s | 0xface0000, 0x81234567)
            for j in (4, 200):
                self.comparar(j, 255, s, 0xdeadbeef)
            if s == 8 or s > 12:
                self.comparar(255, 255, s, 0x92345678)

    def test_768_capacity_queries_and_register_preservation(self):
        from emulador import RETORNO
        for t in range(256):
            for high in (0, 0x12340000, 0xffffff00):
                edx = self.rng.getrandbits(32)
                regs = self.b.capacidade(t | high, edx)
                self.assertEqual(regs['EAX'], capacidade_tipo(t))
                self.assertEqual(regs['EDX'], edx)
                self.assertEqual(regs['EIP'], RETORNO)
                self.assertTrue(self.b.conferir_memoria())

    def test_416_boundary_word_byte_loads(self):
        # Poison adjacent bytes to distinguish u8 loads and unsigned u16 loads.
        for valor in (0, 127, 128, 255):
            self.bonus.memoria[:] = bytes([valor]) * TAMANHO_BONUS_UNIDADES
            self.b.carregar_bonus(self.bonus)
            for t in range(26):
                for s in (0, 1, 5, 12):
                    self.comparar(3, t, s, 0xffffffff)


if __name__ == '__main__':
    unittest.main()
