"""Transport status queries compared to complete unpatched native routines."""
import os
from pathlib import Path
import random
import sys
import unittest

PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))
from consultas_transporte import ConsultasTransporte
from recrutamento import Recrutamento
from construcoes import EconomiaConstrucoes
from test_saida_tropa import estado,w


def preparar(indice=0,alvo=0):
    r=Recrutamento(EconomiaConstrucoes(estruturas=bytes(276000)))
    o=indice*276
    r.unidades[o+2]=5
    r.unidades[o+0x82]=2
    w(r.unidades,o+0x80,alvo)
    w(r.unidades,o+0x84,1)
    if alvo<1000:
        r.mundo.estruturas[alvo*276+8]=255
        r.mundo.estruturas[alvo*276+4]=1
    return ConsultasTransporte(r)


class ExemplosConsultasTransporte(unittest.TestCase):
    def test_return_compares_building_type_and_ignores_unit_owner(self):
        c=preparar()
        c.recrutamento.unidades[0]=200
        self.assertTrue(c.retorna(0,255))
        self.assertFalse(c.retorna(0,1))
        self.assertTrue(c.retorna(0x10000,0x1ff))

    def test_only_three_literal_states_are_accepted(self):
        c=preparar()
        for st in range(256):
            c.recrutamento.unidades[2]=st
            self.assertEqual(c.retorna(0,255),st in (5,17,18))
            self.assertEqual(c.aporta(0,1),st in (5,17,18))

    def test_full_word_field_does_not_compare_only_low_byte(self):
        c=preparar()
        self.assertTrue(c.aporta(0,0x101))
        w(c.recrutamento.unidades,0x84,257)
        self.assertFalse(c.aporta(0,1))
        self.assertFalse(c.aporta(0,257))

    def test_mode_zero_is_wildcard_after_low_byte_truncation(self):
        c=preparar()
        c.recrutamento.unidades[0x82]=255
        self.assertTrue(c.aporta(0,1,0))
        self.assertTrue(c.aporta(0,1,0x100))
        self.assertTrue(c.aporta(0,1,0x1ff))
        self.assertFalse(c.aporta(0,1,2))

    def test_unused_invalid_building_reference_is_not_read(self):
        c=preparar(alvo=65535)
        u=c.recrutamento.unidades
        u[2]=0
        self.assertFalse(c.retorna(0,255))
        u[2],u[0x82]=5,1
        self.assertFalse(c.retorna(0,255))
        u[0x82]=2
        with self.assertRaises(ValueError):c.retorna(0,255)
        self.assertTrue(c.aporta(0,1))

    def test_index_and_pool_guards_and_read_only_state(self):
        c=preparar()
        antes=estado(c.recrutamento)
        c.retorna(0,255)
        c.aporta(0,1)
        self.assertEqual(estado(c.recrutamento),antes)
        for i in (800,65535,-1):
            with self.assertRaises(ValueError):c.retorna(i,255)
            with self.assertRaises(ValueError):c.aporta(i,1)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialConsultasTransporte(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        from bancada_consultas_transporte import BancadaConsultasTransporte
        self.b=BancadaConsultasTransporte()
        type(self).bancadas.append(self.b)
        self.rng=random.Random(0x456cd9)

    def comparar(self,c,entrada,indice,argumento,modo=0,*,invalido=False):
        from emulador import RETORNO,PILHA
        self.b.carregar_recrutamento(c.recrutamento)
        guardas=self.b.guardas_recrutamento()
        if invalido:
            with self.assertRaises(ValueError):c.retorna(indice,argumento)
            esperado=None
        else:
            esperado=(c.retorna(indice,argumento) if entrada==0x456cd9 else c.aporta(indice,argumento,modo))
        regs=self.b.consultar(entrada,indice|0xabcd0000,argumento|0xface0000,modo|0xbabe0000,parar_indice=invalido)
        self.assertEqual(regs['EIP'],0x41a4f4 if invalido else RETORNO)
        if not invalido:
            self.assertEqual(regs['EAX']&255,int(esperado))
            self.assertEqual(regs['ESP'],PILHA+0x8004)
            for nome,valor in dict(EBX=modo|0xbabe0000,ECX=0x12345678,ESI=0x89abcdef,EDI=0x76543210,EBP=0xfedcba98).items():
                self.assertEqual(regs[nome],valor,nome)
        atual=self.b.estado()
        atual.update(self.b.estado_recrutamento())
        esperado_estado=estado(c.recrutamento)
        for nome,valor in atual.items():self.assertEqual(valor,esperado_estado[nome],nome)
        self.assertEqual(self.b.guardas_recrutamento(),guardas)
        self.assertEqual(self.b.guardas(),(b'\xa6'*16,b'\x6a'*16))
        self.assertEqual(self.b.outras_guardas(),(b'\xc7'*8,b'\x7c'*8,b'\xe9'*8,b'\x9e'*8,0x12345678))

    def test_1024_all_state_bytes_both_queries_and_edge_unit_slots(self):
        for i in (0,799):
            c=preparar(i,999)
            for st in range(256):
                c.recrutamento.unidades[i*276+2]=st
                for entrada,arg in ((0x456cd9,255),(0x456d35,1)):
                    self.comparar(c,entrada,i,arg)

    def test_512_return_mode_bytes_and_building_type_comparison(self):
        c=preparar()
        for modo in range(256):
            c.recrutamento.unidades[0x82]=modo
            c.recrutamento.mundo.estruturas[8]=modo
            for pedido in (modo,(modo+1)&255):
                self.comparar(c,0x456cd9,0,pedido)

    def test_2304_apporte_mode_wildcard_and_exact_matches(self):
        c=preparar()
        for st in (5,17,18):
            c.recrutamento.unidades[2]=st
            for modo in range(256):
                c.recrutamento.unidades[0x82]=modo
                for pedido in (0,modo,modo^255):
                    self.comparar(c,0x456d35,0,1,pedido)

    def test_1024_apporte_comparison_bytes_and_high_word_nonmatches(self):
        c=preparar(799)
        for argumento in range(256):
            for valor in (argumento,argumento|0x100,65535,(argumento+1)&255):
                w(c.recrutamento.unidades,799*276+0x84,valor)
                self.comparar(c,0x456d35,799,argumento)

    def test_6_invalid_building_references_stop_only_at_conditional_lookup(self):
        c=preparar()
        for st in (5,17,18):
            c.recrutamento.unidades[2]=st
            for alvo in (1000,65535):
                w(c.recrutamento.unidades,0x80,alvo)
                self.comparar(c,0x456cd9,0,255,invalido=True)

    def test_64_seeded_complete_pools_and_untouched_economy(self):
        for n in range(32):
            i,alvo=(799,999) if n%2 else (0,0)
            c=preparar(i,alvo)
            r=c.recrutamento
            r.unidades[:]=self.rng.randbytes(220800)
            r.mundo.estruturas[:]=self.rng.randbytes(276000)
            r.mundo.economia.memoria[:]=self.rng.randbytes(128)
            r.unidades[i*276+2]=(0,5,17,18)[n%4]
            r.unidades[i*276+0x82]=2
            w(r.unidades,i*276+0x80,alvo)
            w(r.unidades,i*276+0x84,n)
            self.comparar(c,0x456cd9,i,r.mundo.estruturas[alvo*276+8])
            self.comparar(c,0x456d35,i,n)


if __name__=='__main__':unittest.main()
