"""Whole producer/cleanup comparisons with distinct live remaining units."""
import os
from pathlib import Path
import sys
import unittest
from unittest import mock

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
import test_producao_solicitada as anterior
from test_saida_tropa import bag, estado, w, d
from test_ciclo_producao import progresso
from voz_unidades import DependenciaVozUnidade
import limpeza_saida
import producao_limpa as produtor

JANELA = anterior.JANELA


def preparar(tipo=16, indice=0, unidade=799, destino=7, dono=0,
             reter=True, tipo_restante=9, estado_construcao=3, **kwargs):
    p,m,b = anterior.preparar(tipo,indice,unidade,destino,dono,**kwargs)
    outro = 0 if unidade == 799 else 799
    m.unidades[outro*276+1] = tipo_restante
    m.unidades[outro*276+2] = 14
    m.unidades[outro*276] = dono
    entradas = [(1,unidade)] + ([(1,outro)] if reter else [])
    bag(m.estruturas,indice*276+0xc,entradas)
    m.estruturas[indice*276+5] = estado_construcao
    return p,m,b


class ExemplosProducaoLimpa(unittest.TestCase):
    def test_four_retained_branches_reset_after_real_conversion_and_request(self):
        for tipo in (1,2,13,16):
            p,m,b = preparar(tipo)
            q = produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0,janela=JANELA)
            self.assertEqual((q.endereco_dependencia,q.funcao_dependencia,q.parametro),(0x4211d3,0x4829c8,70))
            self.assertEqual((m.unidades[799*276+1],m.unidades[1]),(7,9))
            self.assertEqual((m.estruturas[0x74],m.estruturas[0x7b],progresso(p)),(0,255,0))
            self.assertEqual(m.unidades[799*276+0xf9],0)
            self.assertEqual(m.efeitos[-1],('move',799,0x909))

    def test_empty_branches_reset_only_one_two_before_terrain_query(self):
        for tipo in (1,2,13,16):
            p,m,b = preparar(tipo,reter=False,estado_construcao=255)
            q = produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0,janela=JANELA)
            self.assertEqual((q.endereco_dependencia,q.funcao_dependencia,q.parametro),
                             (0x42110c,0x41aee2,10 if tipo==2 else 8))
            self.assertEqual((m.estruturas[0x74],progresso(p)),(0,0) if tipo in (1,2) else (1,1111))
            self.assertEqual(m.estruturas[5],5 if tipo in (1,2) else 255)

    def test_count_zero_still_retains_distinct_stale_capacity_colonist(self):
        p,m,b = preparar()
        w(m.estruturas,0xc,1)  # output live; distinct colonist tagged beyond count
        q = produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0,janela=JANELA)
        self.assertEqual(q.endereco_dependencia,0x4211d3)
        self.assertEqual(m.estruturas[0xc:0xe],bytes(2))
        self.assertEqual(m.estruturas[0x4f],1)

    def test_type_two_retains_accepted_noncolonist_but_other_building_does_not(self):
        for tipo in (1,2):
            p,m,b = preparar(tipo,tipo_restante=4)
            q = produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0,janela=JANELA)
            self.assertEqual(q.endereco_dependencia,0x4211d3 if tipo==2 else 0x42110c)

    def test_reset_import_failure_preserves_full_prior_world_and_progress(self):
        for tipo,reter in ((16,True),(1,False)):
            p,m,b = preparar(tipo,reter=reter)
            with mock.patch.object(limpeza_saida,'_resetter_core',side_effect=ImportError('pending reset')):
                with self.assertRaises(ImportError):
                    produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0,janela=JANELA)
            self.assertEqual((m.estruturas[0x74],m.estruturas[0x7b]),(1,7))
            self.assertEqual(progresso(p),1124 if reter else 1111)
            self.assertEqual(m.unidades[799*276+0x72],1)
            self.assertEqual(m.efeitos[-1],('move',799,0x909))

    def test_empty_thirteen_sixteen_do_not_import_reset_at_terrain_boundary(self):
        for tipo in (13,16):
            p,m,b = preparar(tipo,reter=False)
            with mock.patch.object(limpeza_saida,'_resetter_core',side_effect=ImportError('not reached')):
                self.assertEqual(produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0,janela=JANELA).endereco_dependencia,0x42110c)

    def test_pending_sound_and_viewport_never_reach_cleanup(self):
        for janela,checkpoint in ((None,0x440d9f),(JANELA,0x440de7)):
            p,m,b = preparar(handle=0xffffffff)
            with mock.patch.object(produtor,'retomar_limpeza_saida',side_effect=AssertionError('cleanup not reached')):
                with self.assertRaises(DependenciaVozUnidade) as ctx:
                    produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0,janela=janela)
            self.assertEqual(ctx.exception.checkpoint,checkpoint)
            self.assertEqual((m.estruturas[0x74],progresso(p)),(1,1124))

    def test_incomplete_update_does_not_import_reset_or_cleanup(self):
        p,m,b = preparar()
        d(m.estruturas,0x8c,1)
        with mock.patch.object(produtor,'retomar_limpeza_saida',side_effect=AssertionError('cleanup not reached')):
            self.assertIsNone(produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,0))
        self.assertEqual(progresso(p),126)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialProducaoLimpa(unittest.TestCase):
    bancadas = []

    def setUp(self):
        from bancada_producao_limpa import BancadaProducaoLimpa
        self.b = BancadaProducaoLimpa()
        type(self).bancadas.append(self.b)

    def comparar(self,p,m,b,i=0,*,janela=JANELA,erro=None,carregar=True):
        from emulador import RETORNO
        if carregar:
            self.b.carregar_solicitado(p,m,b,janela)
            self.guardas = self.b.guardas_recrutamento()
        m.efeitos = []
        dependencia = None
        if erro in ('reset_reter','reset_vazio'):
            with mock.patch.object(limpeza_saida,'_resetter_core',side_effect=ImportError('pending reset')):
                with self.assertRaises(ImportError):
                    produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,i,janela=janela)
            q = None
        elif erro in ('som','volume'):
            with self.assertRaises(DependenciaVozUnidade) as ctx:
                produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,i,janela=janela)
            dependencia = ctx.exception
            q = None
        else:
            q = produtor.calcular_tropa_com_limpeza_no_mundo(p,m,b,i,janela=janela)
        regs = self.b.calcular_limpo(i,parada=erro)
        alvo = {'som':0x440de7,'volume':0x440d9f,'reset_reter':0x42116e,'reset_vazio':0x421097}.get(
            erro,RETORNO if q is None else q.endereco_dependencia)
        self.assertEqual(regs['EIP'],alvo)
        self.assertEqual(self.b.conferir_saida(m),[])
        self.assertEqual(self.b.efeitos,m.efeitos)
        esperado = estado(p.recrutamento)
        esperado.update(tipos_construcoes=bytes(p.tipos_construcoes),ajuste_hospital=p.ajuste_hospital)
        for nome,valor in self.b.estado_economico().items():
            self.assertEqual(valor,esperado[nome],nome)
        self.assertEqual(self.b.guardas_recrutamento(),self.guardas)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x49a070,88)),bytes(m.realizaveis_estruturas))
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfba0,1872)),bytes(b.memoria))
        if q is not None:
            self.assertEqual((regs['EAX']&65535,regs['EDX']),
                             (q.unidade,70) if alvo==0x4211d3 else (q.indice,q.parametro))
            if alvo==0x4211d3:self.assertEqual(regs['EBX'],0)
        if erro=='som':
            r = dependencia.solicitacao
            self.assertEqual(self.b.pedido_som(regs),dict(opcode=r.opcode,codigo=r.codigo,flag=r.flag,
                                                        volume=r.volume,offset_handle=r.offset_handle))
        if dependencia is not None:self.assertEqual(dependencia.checkpoint,alvo)
        return q

    def test_four_distinct_colonist_producer_cleanup_paths(self):
        for tipo in (1,2,13,16):self.comparar(*preparar(tipo))

    def test_208_building_output_type_and_retention_pairs(self):
        for tipo in (1,2,13,16):
            for t in range(26):
                for reter in (False,True):
                    i,u = (999,0) if t%2 else (0,799)
                    p,m,b = preparar(tipo,i,u,t,t%4,reter=reter,local=t%4,
                                     estado_construcao=3 if t%2 else 255)
                    self.comparar(p,m,b,i|0xabcd0000)

    def test_32_remaining_type_predicates_use_capacity_not_only_colonists(self):
        for tipo in (1,2,13,16):
            for t in (3,4,9,11,14,18,25,255):
                self.comparar(*preparar(tipo,tipo_restante=t))

    def test_eight_stale_capacity_entries_survive_live_output_removal(self):
        for tipo in (1,2,13,16):
            for i,u in ((0,799),(999,0)):
                p,m,b = preparar(tipo,i,u)
                w(m.estruturas,i*276+0xc,1)
                self.assertEqual(self.comparar(p,m,b,i).endereco_dependencia,0x4211d3)

    def test_36_inactive_or_incomplete_producers_do_not_enter_cleanup(self):
        for tipo in (1,2,13,16):
            for ativo in (0,1,255):
                for valor in (0,1,3):
                    p,m,b = preparar(tipo,handle=0xffffffff)
                    m.estruturas[0x74] = ativo
                    d(m.estruturas,0x8c,valor)
                    w(p.recrutamento.tipos_unidades,7*50,65535)
                    self.assertIsNone(self.comparar(p,m,b,janela=None))

    def test_eight_pending_sound_or_viewport_dependencies_preserve_prior_effects(self):
        for tipo in (1,16):
            for t in (0,7,25):
                self.comparar(*preparar(tipo,destino=t,handle=0xffffffff),erro='som')
            self.comparar(*preparar(tipo),janela=None,erro='volume')

    def test_two_reset_import_stops_match_first_original_inline_store(self):
        self.comparar(*preparar(16),erro='reset_reter')
        self.comparar(*preparar(1,reter=False),erro='reset_vazio')

    def test_four_persistent_sequences_stop_at_first_terrain_or_message(self):
        for tipo in (1,2,13,16):
            p,m,b = preparar(tipo,reter=tipo in (1,13))
            d(m.estruturas,0x8c,1)
            p.tipos_construcoes[tipo*52+18] = 7
            for n in range(20):
                q = self.comparar(p,m,b,carregar=n==0)
                if q is not None:break
            self.assertIsNotNone(q)


if __name__=='__main__':unittest.main()
