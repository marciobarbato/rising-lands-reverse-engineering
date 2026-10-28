"""Real production caller branches: once-per-update progress and exit ordering."""
import os
from pathlib import Path
import random
import struct
import sys
import unittest

PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))
from producao import Producao
from test_saida_tropa import preparar as preparar_saida, bag, estado


def w(b,o,v):struct.pack_into('<H',b,o,v&65535)
def d(b,o,v):struct.pack_into('<I',b,o,v&0xffffffff)


def preparar(tipo=16,indice=0,quantidade=3,divisor=8,tempo=10,progresso=1):
    saida=preparar_saida(indice=indice)
    p=Producao(saida.recrutamento)
    r=p.recrutamento
    o=indice*276
    r.mundo.estruturas[o+8]=tipo
    bag(r.mundo.estruturas,o+0xc,[(1,799)]*quantidade)
    r.mundo.estruturas[o+0x74]=1
    w(r.tipos_unidades,7*50,tempo)
    d(r.mundo.estruturas,o+0x8c,progresso)
    p.tipos_construcoes[tipo*52+18]=divisor
    return p


def progresso(p,i=0):return struct.unpack_from('<I',p.recrutamento.mundo.estruturas,i*276+0x8c)[0]


class ExemplosCicloProducao(unittest.TestCase):
    def test_active_update_advances_once_and_calls_exit_below_threshold(self):
        p=preparar(quantidade=3,divisor=8)
        calls=[]
        def saida(i,d):calls.append((i,d,progresso(p)))
        self.assertIsNone(p.calcular_tropa(0,saida_tropa=saida))
        self.assertEqual(calls,[(0,4,138)])
        self.assertEqual(progresso(p),138)

    def test_post_increment_completion_reuses_existing_preparation(self):
        p=preparar(progresso=999)
        pending=p.calcular_tropa(0)
        self.assertEqual((pending.indice,pending.direcao,pending.unidade,pending.endereco_dependencia),(0,4,799,0x420698))
        self.assertEqual(progresso(p),1136)
        self.assertEqual(p.recrutamento.mundo.economia.consultar(0),(1,4,0,0))

    def test_type13_direction_and_argument_width(self):
        p=preparar(tipo=13,indice=999,progresso=1000)
        pending=p.calcular_tropa(0xabcd03e7)
        self.assertEqual((pending.indice,pending.direcao),(999,14))
        self.assertEqual(progresso(p,999),1000)

    def test_inactive_does_not_query_time_or_call_exit(self):
        for off in (0x8c,0x74):
            p=preparar()
            p.recrutamento.mundo.estruturas[off]=0
            p.recrutamento.mundo.estruturas[0x7b]=255
            self.assertIsNone(p.calcular_tropa(0,saida_tropa=lambda *a:self.fail('inactive exit')))

    def test_callback_failure_preserves_increment(self):
        p=preparar()
        def falhar(*args):raise RuntimeError('external exit failure')
        with self.assertRaisesRegex(RuntimeError,'exit failure'):p.calcular_tropa(0,saida_tropa=falhar)
        self.assertEqual(progresso(p),138)

    def test_other_dispatches_are_outside_protected_caller_domain(self):
        for t in (0,5,6,14,18,20,21):
            p=preparar(tipo=t)
            before=bytes(p.recrutamento.mundo.estruturas)
            with self.assertRaises(ValueError):p.calcular_tropa(0)
            self.assertEqual(bytes(p.recrutamento.mundo.estruturas),before)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialCicloProducao(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        self.nova_bancada()
        self.rng=random.Random(0x4259e6)

    def nova_bancada(self):
        from bancada_ciclo_producao import BancadaCicloProducao
        self.b=BancadaCicloProducao()
        type(self).bancadas.append(self.b)

    def conferir(self,p):
        expected=estado(p.recrutamento)
        expected.update(tipos_construcoes=bytes(p.tipos_construcoes),ajuste_hospital=p.ajuste_hospital)
        actual=self.b.estado()
        actual.update(self.b.estado_recrutamento())
        actual.update(self.b.estado_producao())
        for k,v in actual.items():self.assertTrue(v==expected[k],k)
        self.assertEqual(self.b.guardas_producao(),self.guardas)
        self.assertEqual(self.b.guardas(),(b'\xa6'*16,b'\x6a'*16))
        self.assertEqual(self.b.outras_guardas(),(b'\xc7'*8,b'\x7c'*8,b'\xe9'*8,b'\x9e'*8,0x12345678))

    def comparar(self,p,i=0):
        from emulador import RETORNO,x86,PILHA
        self.b.carregar_producao(p)
        self.guardas=self.b.guardas_producao()
        r=p.recrutamento
        o=(i&65535)*276
        ativo=progresso(p,i&65535)!=0 and r.mundo.estruturas[o+0x74]!=0
        tipo=r.mundo.estruturas[o+8]
        pending=p.calcular_tropa(i)
        regs={n:self.rng.getrandbits(32) for n in ('EBX','ECX','EDX','ESI','EDI','EBP')}
        actual=self.b.calcular(i,regs)
        self.assertEqual(actual['EIP'],RETORNO if pending is None else 0x420698)
        self.assertEqual(self.b.saidas_tropa,[(i&65535,14 if tipo==13 else 4)] if ativo else [])
        if pending is None:
            self.assertEqual(actual['ESP'],PILHA+0x8004)
            for n,v in regs.items():self.assertEqual(actual[n],v,n)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPCW),0x127f)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPTAG),0xffff)
        self.conferir(p)
        return pending

    def test_992_colonist_capacity_float_samples_in_real_caller(self):
        for t in (1,2,13,16):
            for q in range(31):
                for div in (0,1,2,3,7,29,100,255):
                    self.comparar(preparar(t,quantidade=q,divisor=div,tempo=65535))

    def test_thresholds_activity_time_zero_and_index_widths(self):
        for t in (1,2,13,16):
            for tempo in (0,1,65535):
                for valor in sorted({0,1,max(0,tempo*100-1),tempo*100,0xffffffff}):
                    for flag in (0,1,255):
                        for i in (0,999):
                            p=preparar(t,i,tempo=tempo,progresso=valor)
                            p.recrutamento.mundo.estruturas[i*276+0x74]=flag
                            self.comparar(p,i|0xabcd0000)

    def test_16_real_update_sequences_stop_after_preparation(self):
        for t in (1,2,13,16):
            for div in (0,1,7,255):
                p=preparar(t,divisor=div)
                for step in range(20):
                    pending=self.comparar(p)
                    if pending is not None:break
                self.assertIsNotNone(pending)

    def test_4_post_increment_deposit_exceptions_keep_partial_effects(self):
        from emulador import unicorn,x86
        for t in (1,2,13,16):
            if self.b.execucoes:self.nova_bancada()
            p=preparar(t,progresso=999)
            p.recrutamento.mundo.capacidades.configurar(0,1,0)
            self.b.carregar_producao(p)
            self.guardas=self.b.guardas_producao()
            with self.assertRaises(ZeroDivisionError):p.calcular_tropa(0)
            with self.assertRaises(unicorn.UcError) as ctx:self.b.calcular(0)
            self.assertEqual(ctx.exception.errno,unicorn.UC_ERR_EXCEPTION)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP),0x423501)
            self.b.excecoes_esperadas+=1
            self.conferir(p)


if __name__=='__main__':unittest.main()
