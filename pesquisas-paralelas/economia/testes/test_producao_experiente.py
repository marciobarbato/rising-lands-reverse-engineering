"""Whole original production update through the live raw experience queue."""
import os
from pathlib import Path
import random
import sys
from types import SimpleNamespace
import unittest
from unittest import mock

PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))
import producao_experiente as produtor
from producao_compartilhada import calcular_tropa_no_mundo
import test_producao_compartilhada as testes_compartilhados
preparar=testes_compartilhados.preparar
from test_ciclo_producao import progresso
from test_saida_tropa import w,d


def fila(mundo,tipo=7,experiencia=129):
    # Explicit synthetic loaded queue, not the world's constructor default.
    mundo.experiencias_unidades[:]=bytes((7,0,8,1,9,2,10,3,11,4))*4
    mundo.experiencias_unidades[0:2]=bytes((tipo,experiencia))


class ExemplosProducaoExperiente(unittest.TestCase):
    def test_actual_producer_consumes_first_pair_after_recovery(self):
        p,m,b=preparar()
        fila(m)
        w(p.recrutamento.tipos_unidades,7*50+0x2e,65535)
        pedido=produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,0)
        self.assertEqual((pedido.endereco_dependencia,pedido.unidade),(0x420f8a,799))
        self.assertEqual(m.unidades[799*276+0xaf],129)
        self.assertEqual(m.unidades[799*276+0xf8],30)
        self.assertEqual(m.experiencias_unidades[:10],bytes((8,1,9,2,10,3,11,4,255,0)))
        self.assertEqual(progresso(p),1136)
        self.assertEqual(m.palavra(799,0x9a),100)

    def test_old_recovery_endpoint_preserves_queue_and_remains_stable(self):
        p,m,b=preparar()
        fila(m)
        antes=bytes(m.experiencias_unidades)
        self.assertEqual(calcular_tropa_no_mundo(p,m,b,0).endereco_dependencia,0x420f81)
        self.assertEqual(bytes(m.experiencias_unidades),antes)

    def test_does_not_search_matching_later_pair(self):
        p,m,b=preparar()
        fila(m,tipo=8,experiencia=1)
        m.experiencias_unidades[2:4]=bytes((7,129))
        antes=bytes(m.experiencias_unidades)
        produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,0)
        self.assertEqual(bytes(m.experiencias_unidades),antes)

    def test_inactive_or_incomplete_never_loads_experience_provider(self):
        for ativo in (0,1):
            p,m,b=preparar()
            m.estruturas[0x74]=ativo
            d(m.estruturas,0x8c,1)
            with mock.patch.object(produtor,'_experiencia_core',side_effect=AssertionError('unexpected import')):
                self.assertIsNone(produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,0))

    def test_invalid_queue_retains_completed_recovery(self):
        p,m,b=preparar()
        m.experiencias_unidades=bytes(40)
        with self.assertRaises(ValueError):produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,0)
        self.assertEqual((progresso(p),m.unidades[799*276+1],m.palavra(799,0x9a),m.palavra(799,0x74)),(1136,7,100,0))

    def test_foreign_provider_fails_after_recovery(self):
        p,m,b=preparar()
        fila(m)
        antes=bytes(m.experiencias_unidades)
        with mock.patch.dict(sys.modules,{'experiencia_unidades':SimpleNamespace(__file__='/other/experiencia_unidades.py')}):
            with self.assertRaises(ImportError):produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,0)
        self.assertEqual(m.palavra(799,0x9a),100)
        self.assertEqual(bytes(m.experiencias_unidades),antes)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialProducaoExperiente(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        from bancada_producao_experiente import BancadaProducaoExperiente
        self.b=BancadaProducaoExperiente()
        type(self).bancadas.append(self.b)
        self.rng=random.Random(0x420f8a)

    def carregar(self,p,m,b):
        self.b.carregar_experiente(p,m,b)
        self.guardas=self.b.guardas_producao()
        self.grupos_antes=bytes(m.grupos)
        self.objetos_antes=bytes(m.objetos)

    def comparar(self,p,m,b,i=0,*,carregar=True,erro=None):
        from emulador import RETORNO
        if carregar:self.carregar(p,m,b)
        if erro=='import':
            with mock.patch.object(produtor,'_experiencia_core',side_effect=ImportError('pending experience import')):
                with self.assertRaises(ImportError):produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,i)
            pedido=None
        elif erro=='fila':
            with self.assertRaises(ValueError):produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,i)
            pedido=None
        else:
            pedido=produtor.calcular_tropa_com_experiencia_no_mundo(p,m,b,i)
        regs=self.b.calcular_experiente(i,parar_recuperacao=erro is not None)
        self.assertEqual(regs['EIP'],0x420f81 if erro else (RETORNO if pedido is None else 0x420f8a))
        testes_compartilhados.DiferencialProducaoCompartilhada.conferir(self,p,m,b)
        esperado=self.b.fila_antes if erro else b'\x39'*4+bytes(m.experiencias_unidades)+b'\x93'*4
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4e19c0,48)),esperado)
        return pedido

    def test_416_building_type_owner_pairs_and_all_eight_levels(self):
        for n,tipo in enumerate((1,2,13,16)):
            for t in range(26):
                for dono in range(4):
                    i,u=(999,0) if dono%2 else (0,799)
                    p,m,b=preparar(tipo,i,u,t,dono,rng=self.rng)
                    m.experiencias_unidades[:]=self.rng.randbytes(40)
                    m.experiencias_unidades[dono*10:dono*10+2]=bytes((t,((t+dono+n)%8)*32+1))
                    w(p.recrutamento.tipos_unidades,t*50+0x2e,(0,99,100,32768,65535)[t%5])
                    self.comparar(p,m,b,i|0xabcd0000)

    def test_32_first_pair_guards_do_not_search_later_matching_pairs(self):
        for tipo in (1,2,13,16):
            for dono in range(4):
                for nao_casa in (False,True):
                    p,m,b=preparar(tipo,dono=dono)
                    fila(m)
                    base=dono*10
                    m.experiencias_unidades[base:base+4]=bytes((8 if nao_casa else 7,1 if nao_casa else 0,7,129))
                    antes=bytes(m.experiencias_unidades)
                    self.comparar(p,m,b)
                    self.assertEqual(bytes(m.experiencias_unidades),antes)

    def test_36_inactive_or_incomplete_returns(self):
        for tipo in (1,2,13,16):
            for ativo in (0,1,255):
                for valor in (0,1,3):
                    p,m,b=preparar(tipo)
                    fila(m)
                    m.estruturas[0x74]=ativo
                    d(m.estruturas,0x8c,valor)
                    w(p.recrutamento.tipos_unidades,7*50,65535)
                    self.assertIsNone(self.comparar(p,m,b))

    def test_14_after_recovery_queue_and_import_failures(self):
        for tipo in (1,2,13,16):
            for caso in ('immutable','short','neutral'):
                p,m,b=preparar(tipo,dono=4 if caso=='neutral' else 0)
                fila(m)
                if caso=='immutable':m.experiencias_unidades=bytes(m.experiencias_unidades)
                if caso=='short':m.experiencias_unidades=bytearray(39)
                self.comparar(p,m,b,erro='fila')
        for tipo in (1,13):
            p,m,b=preparar(tipo)
            fila(m)
            self.comparar(p,m,b,erro='import')

    def test_12_persistent_update_sequences_stop_once_before_placement(self):
        for tipo in (1,2,13,16):
            for div in (0,7,255):
                p,m,b=preparar(tipo)
                fila(m)
                d(m.estruturas,0x8c,1)
                p.tipos_construcoes[tipo*52+18]=div
                for n in range(30):
                    pedido=self.comparar(p,m,b,carregar=n==0)
                    if pedido is not None:break
                self.assertIsNotNone(pedido)


if __name__=='__main__':
    unittest.main()
