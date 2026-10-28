"""Actual producer reaches cleanup only after supported original request path."""
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest import mock

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
import test_producao_colocada as etapa_anterior
from voz_unidades import DependenciaVozUnidade
import producao_solicitada as produtor
from test_saida_tropa import estado, w, d
from test_ciclo_producao import progresso

JANELA = (0,0,16,16)


def preparar(tipo=16, indice=0, unidade=799, destino=7, dono=0, local=0,
             dono_construcao=None, handle=0):
    p,m,b = etapa_anterior.preparar(tipo,indice,unidade,destino,dono)
    m.jogador_local = local
    m.estruturas[indice*276+4] = dono if dono_construcao is None else dono_construcao
    for jogador in range(4):
        p.recrutamento.mundo.capacidades.configurar(jogador,1,100)
    d(m.unidades,unidade*276+0x104,handle)
    m.unidades[unidade*276+0xf9] = 0xa5
    return p,m,b


class ExemplosProducaoSolicitada(unittest.TestCase):
    def test_foreign_owner_does_not_require_viewport_or_post_sound(self):
        p,m,b = preparar(local=1,handle=0xffffffff)
        q = produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,0)
        self.assertEqual(q.endereco_dependencia,0x420fb7)
        self.assertEqual(m.palavra(799,0x104),65535)
        self.assertEqual(progresso(p),1136)

    def test_local_visible_active_handle_queries_volume_and_reaches_cleanup(self):
        p,m,b = preparar()
        q = produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,0,janela=JANELA)
        self.assertEqual(q.endereco_dependencia,0x420fb7)
        self.assertEqual(m.unidades[799*276+0xf9],0)
        self.assertEqual(m.estruturas[0x74],1)  # cleanup remains pending

    def test_visible_inactive_handle_preserves_exact_pending_request(self):
        p,m,b = preparar(handle=0xffffffff)
        with self.assertRaises(DependenciaVozUnidade) as ctx:
            produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,0,janela=JANELA)
        e = ctx.exception
        self.assertEqual((e.checkpoint,e.endereco),(0x440de7,0x48aa79))
        self.assertEqual((e.solicitacao.opcode,e.solicitacao.codigo,e.solicitacao.flag,e.solicitacao.offset_handle),
                         (0x50,(7<<16)|(6<<8),0,799*276+0x104))
        self.assertEqual(m.unidades[799*276+0xf9],0)
        self.assertEqual((m.palavra(799,0x9a),m.unidades[799*276+0xaf],m.unidades[799*276+0x72]),(100,129,1))

    def test_visible_active_handle_still_requires_loaded_viewport(self):
        for handle in (0,0xffffffff):
            p,m,b = preparar(handle=handle)
            with self.assertRaises(DependenciaVozUnidade) as ctx:
                produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,0)
            self.assertEqual(ctx.exception.checkpoint,0x440d9f)
            self.assertIsNone(ctx.exception.solicitacao)

    def test_hidden_request_returns_without_inventing_viewport(self):
        p,m,b = preparar(local=1,dono_construcao=1,handle=0xffffffff)
        m.descoberto[1][:] = b'\x1f'*65536
        q = produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,0)
        self.assertEqual(q.endereco_dependencia,0x420fb7)
        self.assertEqual(m.unidades[799*276+0x104:799*276+0x108],b'\xff'*4)

    def test_zero_volume_still_leaves_post_sound_pending(self):
        p,m,b = preparar(handle=0xffffffff)
        with self.assertRaises(DependenciaVozUnidade) as ctx:
            produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,0,janela=(1024,1024,1,1))
        self.assertEqual(ctx.exception.solicitacao.volume,0)

    def test_foreign_voice_provider_error_preserves_completed_placement(self):
        p,m,b = preparar()
        with mock.patch.dict(sys.modules,{'voz_unidades':SimpleNamespace(__file__='/other/voz_unidades.py')}):
            with self.assertRaises(ImportError):
                produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,0,janela=JANELA)
        self.assertEqual((m.unidades[799*276+0x72],m.unidades[799*276+0xaf]),(1,129))
        self.assertEqual(m.efeitos[-1],('move',799,0x909))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialProducaoSolicitada(unittest.TestCase):
    bancadas = []

    def setUp(self):
        from bancada_producao_solicitada import BancadaProducaoSolicitada
        self.b = BancadaProducaoSolicitada()
        type(self).bancadas.append(self.b)

    def comparar(self,p,m,b,i=0,*,janela=JANELA,erro=None,carregar=True):
        from emulador import RETORNO
        if carregar:
            self.b.carregar_solicitado(p,m,b,janela)
            self.guardas = self.b.guardas_recrutamento()
        m.efeitos = []
        dependencia = None
        if erro == 'import':
            with mock.patch.object(produtor,'_voz_core',side_effect=ImportError('pending voice import')):
                with self.assertRaises(ImportError):
                    produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,i,janela=janela)
            q = None
        elif erro in ('som','volume'):
            with self.assertRaises(DependenciaVozUnidade) as ctx:
                produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,i,janela=janela)
            dependencia = ctx.exception
            self.assertEqual(dependencia.checkpoint,0x440de7 if erro=='som' else 0x440d9f)
            q = None
        else:
            q = produtor.calcular_tropa_com_solicitacao_no_mundo(p,m,b,i,janela=janela)
        regs = self.b.calcular_solicitado(i,parada=erro or 'limpeza')
        alvo = {'som':0x440de7,'volume':0x440d9f,'import':0x420f9e}.get(erro,RETORNO if q is None else 0x420fb7)
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
        if erro == 'som':
            r = dependencia.solicitacao
            self.assertEqual(self.b.pedido_som(regs),dict(opcode=r.opcode,codigo=r.codigo,flag=r.flag,
                                                        volume=r.volume,offset_handle=r.offset_handle))
        return q

    def test_four_local_active_producer_returns(self):
        for tipo in (1,2,13,16):self.comparar(*preparar(tipo))

    def test_104_output_types_buildings_and_supported_or_pending_requests(self):
        for tipo in (1,2,13,16):
            for t in range(26):
                dono = t%4
                local = dono if t%4<2 else (dono+1)%4
                handle = 0xffffffff if t%2 else 0
                i,u = (999,0) if t%2 else (0,799)
                p,m,b = preparar(tipo,i,u,t,dono,local,handle=handle)
                som = local==dono and handle==0xffffffff
                self.comparar(p,m,b,i|0xabcd0000,erro='som' if som else None)

    def test_64_building_owner_camera_pairs_with_live_inherited_handles(self):
        for tipo in (1,2,13,16):
            for dono in range(4):
                for local in range(4):
                    handle = 0xffffffff if dono%2 else 0
                    p,m,b = preparar(tipo,dono=dono,local=local,handle=handle)
                    som = dono==local and handle==0xffffffff
                    self.comparar(p,m,b,janela=JANELA if dono==local else None,erro='som' if som else None)

    def test_20_viewport_words_and_exact_volume_or_post_boundaries(self):
        janelas = (JANELA,(65534,65534,5,7),(1024,1024,1,1),(65000,50000,65535,65535),None)
        for tipo in (1,2,13,16):
            for n,janela in enumerate(janelas):
                p,m,b = preparar(tipo,handle=0xffffffff)
                m.unidades[799*276+0xbd] = 255 if n%2 else 0
                self.comparar(p,m,b,janela=janela,erro='volume' if janela is None else 'som')

    def test_four_hidden_local_requests_return_without_viewport(self):
        for tipo in (1,2,13,16):
            p,m,b = preparar(tipo,local=1,dono_construcao=1,handle=0xffffffff)
            m.descoberto[1][:] = b'\x1f'*65536
            self.comparar(p,m,b,janela=None)

    def test_36_inactive_or_incomplete_producers_return_without_request(self):
        for tipo in (1,2,13,16):
            for ativo in (0,1,255):
                for valor in (0,1,3):
                    p,m,b = preparar(tipo,handle=0xffffffff)
                    m.estruturas[0x74] = ativo
                    d(m.estruturas,0x8c,valor)
                    w(p.recrutamento.tipos_unidades,7*50,65535)
                    self.assertIsNone(self.comparar(p,m,b,janela=None))

    def test_2_late_import_errors_retain_completed_physical_order(self):
        for tipo in (1,13):self.comparar(*preparar(tipo),erro='import')

    def test_four_persistent_sequences_stop_at_the_first_cleanup_handoff(self):
        for tipo in (1,2,13,16):
            p,m,b = preparar(tipo)
            d(m.estruturas,0x8c,1)
            p.tipos_construcoes[tipo*52+18] = 7
            for n in range(20):
                q = self.comparar(p,m,b,carregar=n==0)
                if q is not None:break
            self.assertIsNotNone(q)



if __name__=='__main__':unittest.main()
