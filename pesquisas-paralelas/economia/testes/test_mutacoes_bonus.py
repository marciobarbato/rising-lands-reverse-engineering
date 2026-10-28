"""Original bonus mutation/reset buffers, arithmetic and post-write dependency."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from bonus_unidades import BonusUnidades, CapacidadeUnidadesPendente, BASE_BONUS_UNIDADES


class ExemplosMutacoesBonus(unittest.TestCase):
    def test_reset_is_selective_in_every_record(self):
        b = BonusUnidades(b'\xff' * 1872)
        b.reiniciar()
        for i in range(104):
            self.assertEqual(bytes(b.memoria[i*18:(i+1)*18]),
                             bytes(3) + b'\xff' + bytes(3) + b'\xff' + bytes(7) + b'\xff' * 3)

    def test_capacity_mutation_precedes_pending_or_callback_failure(self):
        b = BonusUnidades()
        with self.assertRaises(CapacidadeUnidadesPendente) as ctx:
            b.definir(0x103, 30, 1, 0x1234)
        self.assertEqual(ctx.exception.jogador, 3)
        self.assertEqual([b.consultar(3,t,1) for t in range(26)],
                         [0x34 if t in (12,13,15) else 0 for t in range(26)])
        def falhar(j):
            self.assertEqual(b.consultar(j, 0, 1), 88)
            raise RuntimeError('refresh failed after write')
        with self.assertRaisesRegex(RuntimeError, 'after write'):
            b.definir(0, 0, 1, 88, recalcular_capacidades=falhar)

    def test_direct_alias_and_unqueried_field(self):
        b = BonusUnidades()
        self.assertIsNone(b.definir(0, 7, 7, 257))  # Same +0b as ID1, no refresh.
        self.assertEqual(b.consultar(0, 7, 1), 1)
        b.definir(0, 7, 8, 123)
        self.assertEqual(b.memoria[7*18+13],123)
        self.assertEqual(b.consultar(0,7,8,ecx=7),7)
        b.definir(0,7,12,0)
        self.assertEqual(b.consultar(0,7,12),246)

    def test_signed_product_wrap_and_division_zero(self):
        b = BonusUnidades()
        struct.pack_into('<HH',b.tipos_unidades,46,65535,100)
        b.definir(0,0,0,65535)
        self.assertEqual(b.consultar(0,0,0),(-13107)&65535)
        before=bytes(b.memoria)
        with self.assertRaises(ZeroDivisionError):
            b.definir(0,0,3,0)
        self.assertEqual(bytes(b.memoria),before)

    def test_noop_before_validation_and_active_domain_guards(self):
        b = BonusUnidades()
        b.definir(255,255,255,65535)
        for j,t,s in ((4,0,0),(200,0,1),(0,26,2),(0,30,12)):
            with self.assertRaises(ValueError):b.definir(j,t,s,10)
        with self.assertRaises(ValueError):BonusUnidades(tipos_unidades=bytes(50))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialMutacoesBonus(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        self.nova_bancada()
        self.rng=random.Random(0x428878)

    def nova_bancada(self):
        from bancada_mutacoes_bonus import BancadaMutacoesBonus
        self.b=BancadaMutacoesBonus()
        type(self).bancadas.append(self.b)

    def fixture(self):
        return BonusUnidades(self.rng.randbytes(1872),tipos_unidades=self.rng.randbytes(1300))

    def conferir(self,b):
        self.assertEqual(bytes(self.b.cpu.mem_read(BASE_BONUS_UNIDADES-8,1888)),b'\xa7'*8+bytes(b.memoria)+b'\x7a'*8)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4965ae-4,1308)),b'\xd5'*4+bytes(b.tipos_unidades)+b'\x5d'*4)

    def definir(self,b,j,t,s,v):
        from emulador import RETORNO
        self.b.carregar_mutacoes(b)
        if s&255==1:
            with self.assertRaises(CapacidadeUnidadesPendente):b.definir(j,t,s,v)
            stop=0x4475ef
        else:
            b.definir(j,t,s,v)
            stop=RETORNO
        regs=self.b.chamar_mutacao(0x428878,j,t,s,v)
        self.assertEqual(regs['EIP'],stop)
        if stop==0x4475ef:self.assertEqual(regs['EAX'],j&255)
        self.conferir(b)

    def test_1352_all_single_type_selectors_and_widths(self):
        for j in range(4):
            for t in range(26):
                for s in range(13):
                    self.definir(self.fixture(),j|0xabcd0000,t|0xface0000,s|0xbeef0000,self.rng.randrange(1,65536)|0xcafe0000)

    def test_120_all_type_sentinels_and_filters(self):
        for j in range(4):
            for s in (0,1,3,4,5,6):
                for v in (1,9,10,255,65535):
                    self.definir(self.fixture(),j,30,s,v)

    def test_486_unsupported_selector_noops_ignore_invalid_owner_type(self):
        for s in range(13,256):
            for j in (4,255):self.definir(self.fixture(),j,255,s,0xffffffff)

    def test_32_selective_resets_and_original_write_order(self):
        from emulador import RETORNO
        for n in range(32):
            b=self.fixture()
            self.b.carregar_mutacoes(b)
            b.reiniciar()
            regs=self.b.chamar_mutacao(0x428e71)
            self.assertEqual(regs['EIP'],RETORNO)
            self.conferir(b)
            esperado=[(BASE_BONUS_UNIDADES+j*468+t*18+off,width,0)
                      for j in range(4) for t in range(26)
                      for off,width in ((0,2),(2,1),(4,2),(12,1),(6,1),(11,1),(8,2),(10,1),(13,1),(14,1))]
            self.assertEqual(self.b.escritas_bonus,esperado)

    def test_24_divide_exceptions_preserve_buffers(self):
        from emulador import unicorn,x86
        for j in range(4):
            for t in (0,25,30):
                for fill in (0,255):
                    if self.b.execucoes:self.nova_bancada()
                    b=BonusUnidades(bytes([fill])*1872,tipos_unidades=bytes([255])*1300)
                    self.b.carregar_mutacoes(b)
                    with self.assertRaises(ZeroDivisionError):b.definir(j,t,3,0)
                    with self.assertRaises(unicorn.UcError) as ctx:self.b.chamar_mutacao(0x428878,j,t,3,0)
                    self.assertEqual(ctx.exception.errno,unicorn.UC_ERR_EXCEPTION)
                    self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP),0x428ace if t==30 else 0x428a67)
                    self.b.excecoes_esperadas+=1
                    self.conferir(b)

    def test_80_arithmetic_boundaries(self):
        for j in range(4):
            for base in (0,1,32768,65535):
                for s,vs in ((0,(0,1,65535)),(3,(1,65535))):
                    for v in vs:
                        b=self.fixture()
                        struct.pack_into('<HH',b.tipos_unidades,46,base,base)
                        self.definir(b,j,0,s,v)


if __name__=='__main__':unittest.main()
