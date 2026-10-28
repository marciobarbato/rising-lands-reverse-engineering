"""Actual production update through live shared providers and native caller."""
import os
from pathlib import Path
import random
import struct
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest import mock

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(PASTA.parents[1] / 'ferramentas'))
from ordens_unidades import MundoUnidades, ContextoBusca
from bonus_unidades import BonusUnidades, capacidade_tipo
import producao_compartilhada as composto
from test_ciclo_producao import preparar as preparar_ciclo, progresso
from test_saida_tropa import estado, observar_depositos, w, d


def preparar(tipo=16, indice=0, unidade=799, destino=7, dono=0, vida=50, maximo=100, rng=None):
    p = preparar_ciclo(tipo, indice, progresso=999)
    r = p.recrutamento
    mundo = MundoUnidades()
    # Explicit shared identity, never a copy/writeback of a record.
    mundo.estruturas = r.mundo.estruturas
    mundo.unidades = r.unidades
    if unidade != 799:
        r.unidades[unidade*276:(unidade+1)*276] = r.unidades[799*276:800*276]
        r.unidades[799*276:800*276] = bytes(276)
        for slot in range(3):
            w(mundo.estruturas, indice*276+0x12+slot*2, unidade)
    u = unidade*276
    r.unidades[u], r.unidades[u+1], r.unidades[u+2] = dono, 9, 2
    w(r.unidades, u+0x9a, vida)
    w(r.unidades, u+0x74, 4321)
    w(r.unidades, u+0x76, 9876)
    mundo.busca = ContextoBusca(unidade, 1, 1, 0x12345678, 0x9a)
    mundo.estruturas[indice*276+0x7b] = destino
    # Unit time and max are loaded runtime type words, never inferred from INI.
    w(r.tipos_unidades, destino*50, 10)
    w(r.tipos_unidades, destino*50+8, maximo)
    for off, v in ((0x2a,0x123),(0x2c,0x234),(0x30,0x345)):
        w(r.tipos_unidades, destino*50+off, v)
    # Runtime dimensions belong to the same production type table.
    struct.pack_into('<HH', p.tipos_construcoes, tipo*52, 2, 3)
    w(mundo.estruturas, indice*276+2, 0x505)
    bonus = BonusUnidades(rng.randbytes(1872) if rng else bytes(1872))
    return p, mundo, bonus


def busca(mundo):
    b = mundo.busca
    return b.unidade, b.ocupada, b.sucesso, b.ponteiro_rota, b.concluida


class ExemplosProducaoCompartilhada(unittest.TestCase):
    def test_shared_update_advances_once_and_returns_before_experience(self):
        p, mundo, bonus = preparar()
        pedido = composto.calcular_tropa_no_mundo(p, mundo, bonus, 0)
        self.assertEqual((pedido.indice,pedido.unidade,pedido.tipo_unidade,pedido.endereco_dependencia), (0,799,7,0x420f81))
        self.assertEqual(progresso(p), 1136)
        self.assertEqual(mundo.palavra(799,0x9a), 100)
        self.assertEqual(mundo.palavra(799,0x74), 0)
        self.assertEqual(mundo.palavra(799,4), mundo.palavra(799,0x76))
        self.assertEqual(p.recrutamento.mundo.economia.consultar(0), (1,4,0,0))
        self.assertEqual(mundo.estruturas[0x74], 1)  # cleanup still pending
        self.assertEqual(busca(mundo), (65535,0,0,0,0x9a))

    def test_scoped_provider_imports_work_without_permanent_core_search_path(self):
        programa = """import sys
sys.path.insert(0, 'pesquisas-paralelas/economia/testes')
from test_producao_compartilhada import preparar, composto, PASTA
p,mundo,bonus=preparar()
core=str(PASTA.parents[1]/'ferramentas')
sys.path[:]=[v for v in sys.path if v != core]
for nome in ('posicao_saida','conversao_unidades','recuperacao_unidades','unidades'):
 sys.modules.pop(nome,None)
pedido=composto.calcular_tropa_no_mundo(p,mundo,bonus,0)
assert pedido.endereco_dependencia == 0x420f81
assert core not in sys.path
"""
        subprocess.run([sys.executable,'-B','-c',programa],cwd=PASTA.parents[1],check=True)

    def test_mismatched_shared_buffers_fail_before_progress(self):
        for nome in ('unidades','estruturas'):
            p, mundo, bonus = preparar()
            setattr(mundo, nome, bytearray(getattr(mundo, nome)))
            antes = estado(p.recrutamento)
            with self.assertRaises(ValueError):
                composto.calcular_tropa_no_mundo(p,mundo,bonus,0)
            self.assertEqual(estado(p.recrutamento), antes)

    def test_inactive_and_below_threshold_do_not_load_core(self):
        for ativo in (False,True):
            p,mundo,bonus = preparar()
            d(mundo.estruturas,0x8c,1)
            if not ativo:
                mundo.estruturas[0x74] = 0
            with mock.patch.object(composto,'_continuacoes_core',side_effect=AssertionError('unexpected core')):
                self.assertIsNone(composto.calcular_tropa_no_mundo(p,mundo,bonus,0))
            self.assertEqual(progresso(p),138 if ativo else 1)

    def test_late_import_failure_retains_progress_removals_and_credits(self):
        p,mundo,bonus = preparar()
        with mock.patch.object(composto,'_continuacoes_core',side_effect=ImportError('missing provider')):
            with self.assertRaises(ImportError):
                composto.calcular_tropa_no_mundo(p,mundo,bonus,0)
        self.assertEqual(progresso(p),1136)
        self.assertEqual(p.recrutamento.mundo.economia.consultar(0),(1,4,0,0))
        self.assertEqual(mundo.unidades[799*276+1],9)
        self.assertEqual(busca(mundo),(799,1,1,0x12345678,0x9a))

    def test_wrong_checkout_provider_is_rejected_after_economic_preparation(self):
        p,mundo,bonus = preparar()
        with mock.patch.dict(sys.modules, {'recuperacao_unidades':SimpleNamespace(__file__='/other/recuperacao_unidades.py')}):
            with self.assertRaises(ImportError):
                composto.calcular_tropa_no_mundo(p,mundo,bonus,0)
        self.assertEqual(progresso(p),1136)
        self.assertEqual(mundo.unidades[799*276+1],9)
        self.assertEqual(p.recrutamento.mundo.economia.consultar(0),(1,4,0,0))

    def test_live_loaded_bonus_and_dimensions_feed_actual_core_providers(self):
        p,mundo,bonus = preparar(tipo=13,destino=4)
        bonus.memoria[4*18+11] = 200
        bonus.memoria[4*18+16] = 7
        struct.pack_into('<HH',p.tipos_construcoes,13*52,0xffff,0xffff)
        pedido=composto.calcular_tropa_no_mundo(p,mundo,bonus,0xabcd0000)
        self.assertEqual(mundo.palavra(799,0xc),200)  # type4 base0 + actual bonus
        self.assertEqual((pedido.indice,pedido.endereco_dependencia),(0,0x420f81))


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional original x86: RISING_EMULAR=1')
class DiferencialProducaoCompartilhada(unittest.TestCase):
    bancadas=[]

    def setUp(self):
        self.nova_bancada()
        self.rng=random.Random(0x420f81)

    def nova_bancada(self):
        from bancada_producao_compartilhada import BancadaProducaoCompartilhada
        self.b=BancadaProducaoCompartilhada()
        type(self).bancadas.append(self.b)

    def carregar(self,p,mundo,bonus):
        self.b.carregar_compartilhado(p,mundo,bonus)
        self.guardas=self.b.guardas_producao()
        self.grupos_antes=bytes(mundo.grupos)
        self.objetos_antes=bytes(mundo.objetos)

    def conferir(self,p,mundo,bonus):
        esperado=estado(p.recrutamento)
        esperado.update(tipos_construcoes=bytes(p.tipos_construcoes),ajuste_hospital=p.ajuste_hospital)
        atual=self.b.estado()
        atual.update(self.b.estado_recrutamento())
        atual.update(self.b.estado_producao())
        for k,v in atual.items():
            self.assertEqual(v,esperado[k],k)
        self.assertEqual(self.b.guardas_producao(),self.guardas)
        self.assertEqual(self.b.guardas(),(b'\xa6'*16,b'\x6a'*16))
        self.assertEqual(self.b.outras_guardas(),(b'\xc7'*8,b'\x7c'*8,b'\xe9'*8,b'\x9e'*8,0x12345678))
        self.assertEqual(self.b.estado_busca(),busca(mundo))
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfb9c,1880)),self.b.vizinhos_bonus)
        self.assertEqual(bytes(self.b.cpu.mem_read(0x4dfba0,1872)),bytes(bonus.memoria))
        self.assertEqual(bytes(mundo.grupos),self.grupos_antes)
        self.assertEqual(bytes(mundo.objetos),self.objetos_antes)

    def comparar(self,p,mundo,bonus,i=0,*,carregar=True,erro=None):
        from emulador import RETORNO,x86
        if carregar:
            self.carregar(p,mundo,bonus)
        consultas=[]
        consultar=bonus.consultar
        def consulta(j,t,s):
            if erro=='bonus':
                raise RuntimeError('pending bonus query')
            valor=consultar(j,t,s)
            if j not in (4,200):
                consultas.append(('bonus',j,t,s))
            return valor
        def capacidade(t):
            consultas.append(('capacity',t))
            return capacidade_tipo(t)
        adicionar=p.recrutamento.mundo.adicionar
        depositos=observar_depositos(p)
        try:
            with mock.patch.object(composto,'capacidade_tipo',capacidade), mock.patch.object(bonus,'consultar',consulta):
                if erro=='import':
                    with mock.patch.object(composto,'_continuacoes_core',side_effect=ImportError('pending import')):
                        with self.assertRaises(ImportError):composto.calcular_tropa_no_mundo(p,mundo,bonus,i)
                    pedido=None
                elif erro=='bonus':
                    with self.assertRaises(RuntimeError):composto.calcular_tropa_no_mundo(p,mundo,bonus,i)
                    pedido=None
                else:
                    pedido=composto.calcular_tropa_no_mundo(p,mundo,bonus,i)
        finally:
            # Remove only the observer installed for this call; avoid stacking it
            # across persistent update sequences.
            p.recrutamento.mundo.adicionar=adicionar
        regs=self.b.calcular_compartilhado(i,consulta_pendente=erro=='bonus',importacao_pendente=erro=='import')
        esperado=0x420698 if erro=='import' else (0x428cc0 if erro=='bonus' else (RETORNO if pedido is None else 0x420f81))
        self.assertEqual(regs['EIP'],esperado)
        self.assertEqual(self.b.consultas,consultas)
        self.assertEqual(self.b.depositos,depositos)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPCW),0x127f)
        self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_FPTAG),0xffff)
        self.conferir(p,mundo,bonus)
        return pedido

    def test_624_all_building_unit_owner_combinations(self):
        for tipo in (1,2,13,16):
            for t in range(26):
                for n,dono in enumerate((0,1,2,3,4,200)):
                    i,u=(0,799) if n%2 else (999,0)
                    p,mundo,bonus=preparar(tipo,i,u,t,dono,(0,1,64535,65535)[n%4],(0,1000,65535)[n%3],self.rng)
                    mundo.unidades[u*276+2]=(0,2,4)[n%3]
                    if n%2:
                        mundo.busca.unidade=(u+1)%800
                    struct.pack_into('<HH',p.tipos_construcoes,tipo*52,*((0,0),(2,3),(65535,65535))[n%3])
                    self.comparar(p,mundo,bonus,i|0xabcd0000)

    def test_36_inactive_or_below_threshold_returns(self):
        for tipo in (1,2,13,16):
            for ativo in (0,1,255):
                for valor in (0,1,3):
                    p,mundo,bonus=preparar(tipo)
                    p.recrutamento.mundo.estruturas[0x74]=ativo
                    d(mundo.estruturas,0x8c,valor)
                    w(p.recrutamento.tipos_unidades,7*50,65535)
                    self.assertIsNone(self.comparar(p,mundo,bonus))

    def test_12_persistent_update_sequences_end_at_one_shot_handoff(self):
        for tipo in (1,2,13,16):
            for div in (0,7,255):
                p,mundo,bonus=preparar(tipo)
                d(mundo.estruturas,0x8c,1)
                p.tipos_construcoes[tipo*52+18]=div
                for n in range(30):
                    pedido=self.comparar(p,mundo,bonus,carregar=n==0)
                    if pedido is not None:
                        break
                self.assertIsNotNone(pedido)

    def test_4_bonus_query_failures_retain_progress_credit_and_partial_conversion(self):
        for tipo in (1,2,13,16):
            self.comparar(*preparar(tipo),erro='bonus')

    def test_2_post_preparation_import_boundaries(self):
        for tipo in (1,13):
            self.comparar(*preparar(tipo),erro='import')

    def test_4_deposit_division_exceptions_before_core_calls(self):
        from emulador import unicorn,x86
        for tipo in (1,2,13,16):
            if self.b.execucoes:
                self.nova_bancada()
            p,mundo,bonus=preparar(tipo)
            p.recrutamento.mundo.capacidades.configurar(0,1,0)
            self.carregar(p,mundo,bonus)
            with self.assertRaises(ZeroDivisionError):composto.calcular_tropa_no_mundo(p,mundo,bonus,0)
            with self.assertRaises(unicorn.UcError) as ctx:self.b.calcular_compartilhado(0)
            self.assertEqual(ctx.exception.errno,unicorn.UC_ERR_EXCEPTION)
            self.assertEqual(self.b.cpu.reg_read(x86.UC_X86_REG_EIP),0x423501)
            self.b.excecoes_esperadas+=1
            self.conferir(p,mundo,bonus)


if __name__=='__main__':
    unittest.main()
