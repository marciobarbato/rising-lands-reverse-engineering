"""Actual production entry through committed physical placement; no request."""
import os
from pathlib import Path
import random
import sys
from types import SimpleNamespace
import unittest
from unittest import mock

PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))
sys.path.insert(0,str(PASTA.parents[1]/'testes'))
sys.path.insert(0,str(PASTA.parents[1]/'ferramentas'))
import test_colocacao_saida as core_fixtures
from colocacao_saida import DependenciaColocacaoSaida
import insercao_unidades
import producao_colocada as produtor
from test_producao_compartilhada import preparar as preparar_recrutamento
from test_producao_experiente import fila
from test_saida_tropa import estado,w,d
from test_ciclo_producao import progresso

# Core publishes its supported normal-owner vision sum; 8 predates that symbol.
LIMITE_VISAO=getattr(insercao_unidades,'SOMA_VISAO_MAXIMA_INSERCAO',8)
# The fixture's type vision word reaches u8 unit+0xBB (at most 255); level 3
# adds +0xF5=1. With no representable sum above the limit, no stop is
# reachable and those cases compare the original continuation instead.
VISAO_FIXTURA_MAXIMA=255


def casos_visao_grande():
    if LIMITE_VISAO+1<=VISAO_FIXTURA_MAXIMA:
        return ((LIMITE_VISAO+1,0,'visao'),(LIMITE_VISAO,3,'visao'))
    return ((VISAO_FIXTURA_MAXIMA,0,None),(VISAO_FIXTURA_MAXIMA,3,None))

def preparar(tipo=16,indice=0,unidade=799,destino=7,dono=0,raio=1,nivel=4):
    p,anterior,b=preparar_recrutamento(tipo,indice,unidade,destino,dono)
    m=core_fixtures.MundoRastreado(16,16)
    m.unidades=anterior.unidades
    m.estruturas=anterior.estruturas
    m.busca=anterior.busca
    m.regioes[:]=[1]*65536
    # Explicit original raw-pointer aliases; neither entry silently fixes them.
    p.recrutamento.mundo.terreno.tipos=m.objetos
    p.recrutamento.mundo.terreno.quantidades=m.donos_objetos
    fila(m,tipo=destino,experiencia=(nivel<<5)|1)
    if dono:
        m.experiencias_unidades[dono*10:dono*10+2]=bytes((destino,(nivel<<5)|1))
    w(p.recrutamento.tipos_unidades,destino*50+0x2a,raio)
    w(p.recrutamento.tipos_unidades,destino*50+0x2e,65535)
    w(m.estruturas,indice*276+0x7c,0x909)
    w(m.unidades,unidade*276+8,0x505)
    w(m.unidades,unidade*276+0x7c,0x506)
    m.ocupar(unidade,0x505,True)
    m.ocupar(unidade,0x506,True)
    m.efeitos=[]
    adicionar=p.recrutamento.mundo.adicionar
    def depositar(j,r,q,i):
        m.efeitos.append(('deposit',j,r,q,i))
        return adicionar(j,r,q,i)
    p.recrutamento.mundo.adicionar=depositar
    return p,m,b


class ExemplosProducaoColocada(unittest.TestCase):
    def test_actual_update_places_and_orders_then_stops_before_request(self):
        p,m,b=preparar()
        pedido=produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,0)
        self.assertEqual((pedido.endereco_dependencia,pedido.destino_ordem),(0x420f9e,0x909))
        self.assertEqual(progresso(p),1136)
        self.assertEqual(m.palavra(799,8),pedido.celula)
        self.assertEqual(m.unidades[799*276+0x72],1)
        self.assertEqual(m.efeitos[:3],[('deposit',0,2,2,0),('deposit',0,2,2,0),('deposit',0,1,1,0)])
        self.assertEqual(m.efeitos[-1],('move',799,0x909))
        self.assertEqual(m.estruturas[0x74],1)  # economic cleanup is still pending

    def test_raw_alias_mismatch_rejects_before_progress(self):
        for nome in ('tipos','quantidades'):
            p,m,b=preparar()
            setattr(p.recrutamento.mundo.terreno,nome,bytearray(getattr(p.recrutamento.mundo.terreno,nome)))
            antes=estado(p.recrutamento)
            with self.assertRaises(ValueError):produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,0)
            self.assertEqual(estado(p.recrutamento),antes)
            self.assertEqual(m.efeitos,[])

    def test_late_import_error_retains_experience_and_healing(self):
        p,m,b=preparar()
        with mock.patch.object(produtor,'_colocacao_core',side_effect=ImportError('placement unavailable')):
            with self.assertRaises(ImportError):produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,0)
        self.assertEqual((progresso(p),m.palavra(799,0x9a),m.unidades[799*276+0xaf]),(1136,100,129))
        self.assertFalse(any(e[0]=='discovery' for e in m.efeitos))

    def test_large_vision_preserves_prior_economic_and_partial_physical_effects(self):
        raio,nivel,erro=casos_visao_grande()[0]
        p,m,b=preparar(raio=raio,nivel=nivel)
        if erro is None:
            pedido=produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,0)
            self.assertEqual(pedido.endereco_dependencia,0x420f9e)
            return
        with self.assertRaises(DependenciaColocacaoSaida):produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,0)
        self.assertEqual(m.unidades[799*276+0x72],1)
        self.assertEqual(m.efeitos[-1][0],'collision')
        self.assertEqual(p.recrutamento.mundo.economia.consultar(0),(1,4,0,0))

    def test_foreign_placement_provider_rejected_after_experience(self):
        p,m,b=preparar()
        with mock.patch.dict(sys.modules,{'colocacao_saida':SimpleNamespace(__file__='/other/colocacao_saida.py')}):
            with self.assertRaises(ImportError):produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,0)
        self.assertEqual(m.unidades[799*276+0xaf],129)
        self.assertEqual(m.palavra(799,0x9a),100)
        self.assertEqual(m.unidades[799*276+0x72],0)

    def test_inactive_or_incomplete_never_loads_placement(self):
        for ativo in (0,1):
            p,m,b=preparar()
            m.estruturas[0x74]=ativo
            d(m.estruturas,0x8c,1)
            with mock.patch.object(produtor,'_colocacao_core',side_effect=AssertionError('unexpected placement')):
                self.assertIsNone(produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,0))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialProducaoColocada(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        from bancada_producao_colocada import BancadaProducaoColocada
        self.b=BancadaProducaoColocada()
        type(self).bancadas.append(self.b)

    def comparar(self,p,m,b,i=0,*,carregar=True,erro=None):
        from emulador import RETORNO
        if carregar:
            self.b.carregar_produtor(p,m,b)
            self.guardas=self.b.guardas_recrutamento()
        m.efeitos=[]
        if erro=='visao':
            with self.assertRaises(DependenciaColocacaoSaida):produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,i)
            pedido=None
        elif erro=='import':
            with mock.patch.object(produtor,'_colocacao_core',side_effect=ImportError('pending placement import')):
                with self.assertRaises(ImportError):produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,i)
            pedido=None
        else:
            pedido=produtor.calcular_tropa_com_colocacao_no_mundo(p,m,b,i)
        regs=self.b.calcular_produtor(i,parar_visao=erro=='visao',parar_importacao=erro=='import')
        alvo=0x446146 if erro=='visao' else (0x420f8a if erro=='import' else (RETORNO if pedido is None else 0x420f9e))
        self.assertEqual(regs['EIP'],alvo)
        self.assertEqual(self.b.conferir_saida(m),[])
        self.assertEqual(self.b.efeitos,m.efeitos)
        esperado=estado(p.recrutamento)
        esperado.update(tipos_construcoes=bytes(p.tipos_construcoes),ajuste_hospital=p.ajuste_hospital)
        for nome,valor in self.b.estado_economico().items():self.assertEqual(valor,esperado[nome],nome)
        self.assertEqual(self.b.guardas_recrutamento(),self.guardas)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x49a070,88)),bytes(m.realizaveis_estruturas))
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfba0,1872)),bytes(b.memoria))
        return pedido

    def test_four_real_production_building_types(self):
        for tipo in (1,2,13,16):self.comparar(*preparar(tipo))

    def test_104_full_producer_types_owners_edges_and_live_movement_object(self):
        rng=random.Random(0x420f9e)
        for tipo in (1,2,13,16):
            for t in range(26):
                i,u=(999,0) if t%2 else (0,799)
                p,m,b=preparar(tipo,i,u,t,t%4,t%3,t%8)
                b.memoria[:]=rng.randbytes(1872)
                m.objetos[0x909]=0x36 if t%2 else 0
                pedido=self.comparar(p,m,b,i|0xabcd0000)
                self.assertEqual(pedido.destino_ordem,0x909)

    def test_6_unsaturated_vision_sum_boundaries_with_native_cpu_resumes(self):
        for dono in (0,3):
            for raio,nivel in ((0,0),(7,3),(8,0)):
                self.comparar(*preparar(destino=3,dono=dono,raio=raio,nivel=nivel))

    def test_8_large_vision_stops_after_economy_experience_and_collision(self):
        for tipo in (1,2,13,16):
            for raio,nivel,erro in casos_visao_grande():
                self.comparar(*preparar(tipo,raio=raio,nivel=nivel),erro=erro)

    def test_36_inactive_or_incomplete_native_returns(self):
        for tipo in (1,2,13,16):
            for ativo in (0,1,255):
                for valor in (0,1,3):
                    p,m,b=preparar(tipo)
                    m.estruturas[0x74]=ativo
                    d(m.estruturas,0x8c,valor)
                    w(p.recrutamento.tipos_unidades,7*50,65535)
                    self.assertIsNone(self.comparar(p,m,b))

    def test_2_late_provider_import_checkpoints_after_queue_consumption(self):
        for tipo in (1,13):self.comparar(*preparar(tipo),erro='import')

    def test_four_persistent_progress_sequences_stop_after_first_physical_exit(self):
        for tipo in (1,2,13,16):
            p,m,b=preparar(tipo)
            d(m.estruturas,0x8c,1)
            p.tipos_construcoes[tipo*52+18]=7
            for n in range(20):
                pedido=self.comparar(p,m,b,carregar=n==0)
                if pedido is not None:break
            self.assertIsNotNone(pedido)



if __name__=='__main__':unittest.main()
