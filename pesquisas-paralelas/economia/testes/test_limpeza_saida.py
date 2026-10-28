"""Cleanup prefix is explicitly isolated from missing preceding world calls."""
import os
from pathlib import Path
import random
import sys
from types import SimpleNamespace
import unittest
from unittest import mock

PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))
from limpeza_saida import bag_vide,retomar_limpeza_saida
from test_producao_compartilhada import preparar as preparar_mundo
from test_saida_tropa import bag,estado


def preparar(tipo=16,indice=0,entradas=((1,0),),tipo_bag=9,estado_construcao=3):
    p,mundo,_=preparar_mundo(tipo,indice)
    r=p.recrutamento
    mundo.unidades[799*276+1]=7  # output unit already converted, outside the Bag
    bag(mundo.unidades,799*276+0xa,())
    mundo.unidades[1]=tipo_bag
    bag(mundo.estruturas,indice*276+0xc,entradas)
    mundo.estruturas[indice*276+5]=estado_construcao
    return p,mundo,SimpleNamespace(indice=indice,unidade=799,endereco_dependencia=0x420fb7)


class ExemplosLimpezaSaida(unittest.TestCase):
    def test_retained_colonist_uses_actual_core_reset_and_stops_before_message(self):
        p,m,q=preparar()
        r=retomar_limpeza_saida(p,m,q)
        self.assertEqual((r.endereco_dependencia,r.funcao_dependencia,r.parametro),(0x4211d3,0x4829c8,70))
        self.assertEqual(m.estruturas[5],3)
        self.assertEqual(m.estruturas[0x74],0)
        self.assertEqual(m.estruturas[0x7b],255)
        self.assertEqual(m.estruturas[0x8c:0x90],bytes(4))

    def test_empty_branch_resets_only_types_one_two_before_pending_terrain(self):
        for tipo in (1,2,13,16):
            p,m,q=preparar(tipo,entradas=(),estado_construcao=255)
            r=retomar_limpeza_saida(p,m,q)
            self.assertEqual((r.endereco_dependencia,r.funcao_dependencia,r.parametro),(0x42110c,0x41aee2,10 if tipo==2 else 8))
            self.assertEqual(m.estruturas[5],5 if tipo in (1,2) else 255)
            self.assertEqual(m.estruturas[0x74],0 if tipo in (1,2) else 1)

    def test_type_two_predicate_is_not_empty_count_or_colonist_only(self):
        p,m,q=preparar(2,tipo_bag=4)
        # A stale tagged capacity entry is read even with live count zero.
        m.estruturas[0xc:0xe]=bytes(2)
        self.assertTrue(bag_vide(p.recrutamento,0))
        self.assertEqual(retomar_limpeza_saida(p,m,q).endereco_dependencia,0x4211d3)
        p,m,q=preparar(2,tipo_bag=3)
        self.assertFalse(bag_vide(p.recrutamento,0))
        self.assertEqual(retomar_limpeza_saida(p,m,q).endereco_dependencia,0x42110c)

    def test_pending_and_shared_identity_guards_before_mutations(self):
        p,m,q=preparar()
        antes=estado(p.recrutamento)
        q.endereco_dependencia=0x420f81
        with self.assertRaises(ValueError):retomar_limpeza_saida(p,m,q)
        self.assertEqual(estado(p.recrutamento),antes)
        q.endereco_dependencia=0x420fb7
        m.unidades=bytearray(m.unidades)
        with self.assertRaises(ValueError):retomar_limpeza_saida(p,m,q)
        self.assertEqual(estado(p.recrutamento),antes)

    def test_query_guards_and_early_return_preserve_original_read_order(self):
        p,m,q=preparar(2,entradas=((1,0),(1,800)))
        self.assertTrue(bag_vide(p.recrutamento,0))  # later invalid ref is not read
        m.unidades[1]=3
        with self.assertRaises(ValueError):bag_vide(p.recrutamento,0)
        m.estruturas[0xe]=31
        with self.assertRaises(ValueError):bag_vide(p.recrutamento,0)

    def test_foreign_reset_provider_rejected_only_when_original_reset_needed(self):
        with mock.patch.dict(sys.modules,{'ciclo_estruturas':SimpleNamespace(__file__='/other/ciclo_estruturas.py')}):
            p,m,q=preparar()
            antes=estado(p.recrutamento)
            with self.assertRaises(ImportError):retomar_limpeza_saida(p,m,q)
            self.assertEqual(estado(p.recrutamento),antes)
            p,m,q=preparar(13,entradas=())
            self.assertEqual(retomar_limpeza_saida(p,m,q).endereco_dependencia,0x42110c)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialLimpezaSaida(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        from bancada_limpeza_saida import BancadaLimpezaSaida
        self.b=BancadaLimpezaSaida()
        type(self).bancadas.append(self.b)
        self.rng=random.Random(0x420fb7)

    def carregar(self,p):
        self.b.carregar_recrutamento(p.recrutamento)
        self.guardas=self.b.guardas_recrutamento()

    def conferir(self,p):
        esperado=estado(p.recrutamento)
        atual=self.b.estado()
        atual.update(self.b.estado_recrutamento())
        for nome,valor in atual.items():self.assertEqual(valor,esperado[nome],nome)
        self.assertEqual(self.b.guardas_recrutamento(),self.guardas)
        self.assertEqual(self.b.guardas(),(b'\xa6'*16,b'\x6a'*16))
        self.assertEqual(self.b.outras_guardas(),(b'\xc7'*8,b'\x7c'*8,b'\xe9'*8,b'\x9e'*8,0x12345678))

    def comparar(self,p,m,q):
        self.carregar(p)
        r=retomar_limpeza_saida(p,m,q)
        regs=self.b.limpar(q.indice|0xabcd0000,q.unidade|0xcafe0000)
        self.assertEqual(regs['EIP'],r.endereco_dependencia)
        self.assertEqual((regs['EAX']&65535,regs['EDX']),
                         (q.unidade,70) if r.endereco_dependencia==0x4211d3 else (q.indice,r.parametro))
        if r.endereco_dependencia==0x4211d3:self.assertEqual(regs['EBX'],0)
        self.conferir(p)

    def test_512_complete_bag_predicates_all_type_bytes_and_count_independence(self):
        for tipo in range(256):
            for quantidade in (0,1):
                p,m,q=preparar(2,tipo_bag=tipo)
                m.estruturas[0xc]=quantidade
                self.carregar(p)
                self.assertEqual(self.b.consultar_bag(0),bag_vide(p.recrutamento,0))
                self.conferir(p)

    def test_96_cleanup_building_state_index_and_retention_boundaries(self):
        for tipo in (1,2,13,16):
            for st in (0,1,3,4,5,255):
                for indice in (0,999):
                    for reter in (False,True):
                        self.comparar(*preparar(tipo,indice,entradas=((1,0),) if reter else (),estado_construcao=st))

    def test_512_type_two_cleanup_paths_include_unknown_types_and_stale_capacity(self):
        for tipo in range(256):
            for quantidade in (0,1):
                p,m,q=preparar(2,tipo_bag=tipo)
                m.estruturas[0xc]=quantidade
                self.comparar(p,m,q)

    def test_64_seeded_mixed_bags_and_duplicate_references(self):
        for n in range(64):
            p,m,q=preparar((1,2,13,16)[n%4],n%2*999,entradas=())
            r=p.recrutamento
            # Seed complete records and then retain valid referenced indices.
            m.estruturas[q.indice*276+0x78:q.indice*276+0x90]=self.rng.randbytes(24)
            m.estruturas[q.indice*276+5]=self.rng.randrange(256)
            entradas=[(self.rng.randrange(4),self.rng.randrange(32)) for _ in range(n%31)]
            for u in range(32):m.unidades[u*276+1]=self.rng.randrange(256)
            bag(m.estruturas,q.indice*276+0xc,entradas,capacidade=n%31)
            self.comparar(p,m,q)


if __name__=='__main__':
    unittest.main()
