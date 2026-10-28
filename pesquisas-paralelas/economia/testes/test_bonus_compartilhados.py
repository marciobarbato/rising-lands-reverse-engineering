"""Actual committed producer/refresh/query composition on identical buffers."""
import os
from pathlib import Path
import random
import struct
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))
from bonus_unidades import BonusUnidades
from bonus_compartilhados import definir_bonus_no_mundo


def unit(m,i,tipo=12,dono=0,estado=7):
    p=i*276
    m.unidades[p:p+3]=bytes((dono,tipo,estado))
    struct.pack_into('<HH',m.unidades,p+0xa,65535,500)


def preparar():
    m=SimpleNamespace(unidades=bytearray(220800))
    b=BonusUnidades(bytes([0x31])*1872,tipos_unidades=bytes([1])*1300)
    for i,t in ((0,5),(7,12),(799,15)):unit(m,i,t)
    return b,m


class ExemplosBonusCompartilhados(unittest.TestCase):
    def test_setter_then_real_refresh_uses_same_new_bonus_state(self):
        b,m=preparar()
        original=m.unidades
        self.assertIsNone(definir_bonus_no_mundo(b,m,0,30,1,255))
        self.assertIs(m.unidades,original)
        self.assertEqual([struct.unpack_from('<H',m.unidades,i*276+0xc)[0] for i in (0,7,799)],[50,257,258])
        self.assertEqual([struct.unpack_from('<H',m.unidades,i*276+0xa)[0] for i in (0,7,799)],[65535]*3)

    def test_nonrefresh_alias_updates_bonus_without_touching_world(self):
        b,m=preparar()
        original=bytes(m.unidades)
        definir_bonus_no_mundo(b,m,0,12,7,99)
        self.assertEqual(b.consultar(0,12,1),99)
        self.assertEqual(bytes(m.unidades),original)

    def test_world_guard_occurs_after_table_store(self):
        b,m=preparar()
        m.unidades=bytearray(276)
        with self.assertRaises(ValueError):definir_bonus_no_mundo(b,m,0,12,1,99)
        self.assertEqual(b.consultar(0,12,1),99)

    def test_wrong_snapshot_provider_rejected_after_table_store(self):
        b,m=preparar()
        original=bytes(m.unidades)
        with patch.dict(sys.modules,{'capacidades_unidades':SimpleNamespace(__file__='/private/tmp/foreign/capacidades_unidades.py')}):
            with self.assertRaises(ImportError):definir_bonus_no_mundo(b,m,0,12,1,77)
        self.assertEqual(b.consultar(0,12,1),77)
        self.assertEqual(bytes(m.unidades),original)

    def test_nonrefresh_noop_needs_no_world_provider(self):
        b=BonusUnidades()
        definir_bonus_no_mundo(b,object(),255,255,255,0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialBonusCompartilhados(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        from bancada_bonus_compartilhados import BancadaBonusCompartilhados
        self.b=BancadaBonusCompartilhados()
        type(self).bancadas.append(self.b)
        self.rng=random.Random(0x428c60)

    def conferir(self,b,m):
        from emulador import UNIDADES
        self.assertEqual(self.b.unidades(),bytes(m.unidades))
        self.assertEqual(bytes(self.b.cpu.mem_read(UNIDADES+220800,8)),b'\x36'*8)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfb98,1888)),b'\xa7'*8+bytes(b.memoria)+b'\x7a'*8)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4965aa,1308)),b'\xd5'*4+bytes(b.tipos_unidades)+b'\x5d'*4)

    def comparar(self,b,m,j,t,s,v):
        from emulador import RETORNO
        self.b.carregar_compartilhado(b,m)
        before=bytes(m.unidades)
        definir_bonus_no_mundo(b,m,j,t,s,v)
        regs=self.b.definir(j,t,s,v)
        self.assertEqual(regs['EIP'],RETORNO)
        self.conferir(b,m)
        expected=[]
        if s&255==1:
            for i in range(800):
                p=i*276
                if before[p+2] not in (0,4) and before[p]==(j&255):
                    expected += [('capacity',before[p+1]),('bonus',j&255,before[p+1],1)]
        self.assertEqual(self.b.consultas,expected)
        # Table mutation always precedes the first unit-capacity store.
        seen_unit=False
        for address,width,value in self.b.escritas:
            if address>=0x1000000:seen_unit=True
            else:self.assertFalse(seen_unit)

    def test_104_single_type_mutations_refresh_all_matching_units(self):
        for j in range(4):
            for t in range(26):
                b,m=preparar()
                for i in (0,7,799):m.unidades[i*276]=j
                self.comparar(b,m,j|0xabcd0000,t|0xface0000,0x10001,200+t)

    def test_32_all_type_sentinel_and_byte_boundaries(self):
        for j in range(4):
            for v in (0,1,29,30,254,255,256,65535):
                b,m=preparar()
                for i in (0,7,799):m.unidades[i*276]=j
                self.comparar(b,m,j,30,1,v)

    def test_256_seeded_complete_pools_and_untouched_fields(self):
        for n in range(256):
            m=SimpleNamespace(unidades=bytearray(self.rng.randbytes(220800)))
            for i in range(800):
                m.unidades[i*276]=i%6
                m.unidades[i*276+1]=i%26
            b=BonusUnidades(self.rng.randbytes(1872),tipos_unidades=self.rng.randbytes(1300))
            self.comparar(b,m,n%4,30 if n%5==0 else n%26,1,self.rng.getrandbits(32))

    def test_56_other_selectors_do_not_refresh_world(self):
        for j in range(4):
            for s in (0,2,3,4,5,6,7,8,9,10,11,12,13,255):
                b,m=preparar()
                self.comparar(b,m,j,12,s,10)

    def test_3_later_bonus_failures_keep_table_and_prior_unit_stores(self):
        for fail_tipo,indice in ((5,0),(12,7),(15,799)):
            class BonusComFalha(BonusUnidades):
                def consultar(self,j,t,s,**kwargs):
                    if t==fail_tipo:raise RuntimeError('query failure after earlier stores')
                    return super().consultar(j,t,s,**kwargs)
            b,m=preparar()
            b=BonusComFalha(b.memoria,tipos_unidades=b.tipos_unidades)
            self.b.carregar_compartilhado(b,m)
            with self.assertRaisesRegex(RuntimeError,'earlier stores'):definir_bonus_no_mundo(b,m,0,30,1,77)
            regs=self.b.definir(0,30,1,77,checkpoint=(0x44763a,indice))
            self.assertEqual(regs['EIP'],0x44763a)
            self.conferir(b,m)

    def test_3_invalid_type_guards_compare_prequery_native_checkpoints(self):
        for indice in (0,7,799):
            b,m=preparar()
            m.unidades[indice*276+1]=255
            self.b.carregar_compartilhado(b,m)
            with self.assertRaises(ValueError):definir_bonus_no_mundo(b,m,0,30,1,55)
            regs=self.b.definir(0,30,1,55,checkpoint=(0x44763a,indice))
            self.assertEqual(regs['EIP'],0x44763a)
            self.conferir(b,m)


if __name__=='__main__':unittest.main()
