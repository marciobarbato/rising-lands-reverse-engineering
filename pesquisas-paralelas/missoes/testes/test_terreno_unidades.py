"""Original placement-prefix buffers/call order with actual core callbacks."""
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import unittest

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from capturar_terreno_unidades import preparar_caso,resumo_original
from terreno_unidades import (preparar_unidades_no_terreno,provedores_terreno_core,
    ProvedoresTerrenoUnidades,DependenciaTerrenoUnidades)
from carregador_unidades import carregar_unidades_missao
from formatos import Leitor
from bonus_unidades import BonusUnidades
from colocacao_missao import DependenciaColocacaoMissao
from navegacao_unidades import MundoNavegacao


class MundoRastreado(MundoNavegacao):
    """Diagnostic delegations only; physical behavior stays in core methods."""
    def __init__(self,*args):
        self.efeitos=[]
        super().__init__(*args)

    def ocupar(self,index,cell,insert):
        self.efeitos.append(('collision' if insert else 'remove',index,cell))
        return super().ocupar(index,cell,insert)

    def descobrir_area(self,cell,radius,owner):
        self.efeitos.append(('discovery',cell,radius,owner))
        return super().descobrir_area(cell,radius,owner)

    def iluminar_area(self,cell,radius,owner):
        self.efeitos.append(('light',cell,radius,owner))
        return super().iluminar_area(cell,radius,owner)

    def minimapa(self,owner,cell,mode):
        self.efeitos.append(('minimap',owner,cell,mode))
        return super().minimapa(owner,cell,mode)


def carregar_python(args):
    world,data,offset,types,bonus,loader=args
    provider=BonusUnidades(bonus)
    carregar_unidades_missao(Leitor(data,offset),world.unidades,loader,types,world.selecoes_unidades,
                             modificador12=lambda owner,kind:provider.consultar(owner,kind,12))
    world.efeitos=[]
    return provider


def rastrear(providers,trace):
    def wrap(name,function):
        def call(value):
            trace.append((name,value))
            return function(value)
        return call
    return ProvedoresTerrenoUnidades(wrap('exists',providers.existe),
        wrap('visible',providers.visibilidade),wrap('place',providers.colocar),
        wrap('capacity_refresh',providers.capacidades))


def resumo_python(world,trace):
    buffers={}
    for name in ('atributos','regioes','tiles','mini_final','mini_unidades','mini_estruturas',
                 'descoberto','luz_bordas','contagem_luz','donos_objetos'):
        value=getattr(world,name)
        data=(struct.pack('<65536H',*value) if name in ('regioes','tiles') else
              b''.join(bytes(g) for g in value) if name in ('descoberto','luz_bordas','contagem_luz') else bytes(value))
        buffers[name]=hashlib.sha256(data).hexdigest()
    return dict(unit_pool_sha256=hashlib.sha256(world.unidades).hexdigest(),physical_sha256=buffers,
                selection_sha256=hashlib.sha256(world.selecoes_unidades).hexdigest(),
                search=[world.busca.unidade,world.busca.ocupada,world.busca.sucesso,
                        world.busca.ponteiro_rota,world.busca.concluida],
                parent_calls=[list(e) for e in trace],physical_effect_count=len(world.efeitos),
                physical_effect_sha256=hashlib.sha256(json.dumps(world.efeitos,separators=(',',':')).encode()).hexdigest())


class CapturasTerrenoUnidades(unittest.TestCase):
    def test_four_original_prefix_snapshots_and_actual_callbacks(self):
        report=json.loads((OWNED/'evidencias/captura-terreno-unidades-original-v2.json').read_text())
        previous=json.loads((OWNED/'evidencias/captura-terreno-unidades-original.json').read_text())
        self.assertEqual([c['output'] for c in report['cases']],[c['output'] for c in previous['cases']])
        boundary=json.loads((OWNED/'evidencias/captura-terreno-unidades-monde01-limite.json').read_text())
        for case in report['cases']:
            args=preparar_caso(case['name'],MundoRastreado);world=args[0]
            bonus=carregar_python(args)
            self.assertEqual(resumo_python(world,[]),case['input_after_native_unit_load'])
            trace=[]
            if case['name']=='MONDE01':
                with self.assertRaises(DependenciaColocacaoMissao) as error:
                    preparar_unidades_no_terreno(rastrear(provedores_terreno_core(world,bonus_unidades=bonus),trace))
                self.assertEqual(error.exception.unidade,15)
                self.assertEqual(resumo_python(world,trace),boundary['output'])
                continue
            result=preparar_unidades_no_terreno(rastrear(provedores_terreno_core(world,bonus_unidades=bonus),trace))
            self.assertEqual(resumo_python(world,trace),case['output'])
            self.assertEqual(result.endereco_dependencia,0x46c16d)

    def test_original_caller_aligned_dependency_snapshots(self):
        report=json.loads((OWNED/'evidencias/captura-terreno-unidades-limites-chamador.json').read_text())
        for case in report['cases']:
            args=list(preparar_caso('ordinary',MundoRastreado))
            if case['name']=='vision9':
                types=bytearray(args[3]);struct.pack_into('<H',types,42,9);args[3]=types
            bonus=carregar_python(args);world=args[0];trace=[]
            if case['name']=='missing_bonus':
                bonus=None
            error_type=DependenciaTerrenoUnidades if bonus is None else DependenciaColocacaoMissao
            with self.assertRaises(error_type):
                preparar_unidades_no_terreno(rastrear(provedores_terreno_core(world,bonus_unidades=bonus),trace))
            self.assertEqual(resumo_python(world,trace),case['output'])

    def test_missing_callbacks_stop_when_reached_and_unused_bonus_is_not_defaulted(self):
        with self.assertRaises(DependenciaTerrenoUnidades) as error:
            preparar_unidades_no_terreno(ProvedoresTerrenoUnidades(None,None,None,None))
        self.assertEqual((error.exception.endereco,error.exception.argumentos),(0x441fff,(0,)))
        args=preparar_caso('state4_neutral',MundoRastreado);carregar_python(args)
        # No active normal-owner capacity query is reached; no bonus table is created.
        result=preparar_unidades_no_terreno(provedores_terreno_core(args[0]))
        self.assertEqual(result.colocadas,(7,))
        self.assertEqual(args[0].unidades[7*276+2],4)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialTerrenoUnidades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_terreno_unidades import BancadaTerrenoUnidades
        cls.native=BancadaTerrenoUnidades()

    def compare(self,args,stop=None,stop_unit_index=None):
        native=self.native
        native.carregar_caso(*args)
        native.prefixo(stop,stop_unit_index)
        world=args[0];bonus=carregar_python(args);trace=[]
        if stop==0x428cc0:
            bonus=None
        providers=rastrear(provedores_terreno_core(world,bonus_unidades=bonus),trace)
        if stop:
            error_type=DependenciaTerrenoUnidades if stop==0x428cc0 else DependenciaColocacaoMissao
            with self.assertRaises(error_type):
                preparar_unidades_no_terreno(providers)
        else:
            preparar_unidades_no_terreno(providers)
        self.assertEqual(resumo_python(world,trace),resumo_original(native))
        self.assertEqual(native.conferir_saida(world),[])

    def test_loaded_mission1_and_three_declared_physical_fixtures(self):
        for name in ('ordinary','state4_neutral','hidden14','MONDE01'):
            self.compare(preparar_caso(name,MundoRastreado),
                         0x457019 if name=='MONDE01' else None,15 if name=='MONDE01' else None)

    def test_literal_state_flag_owner_and_pool_edges(self):
        for index in (0,799):
            for state in (0,4,7,14):
                for owner in (0,3,4,200):
                    for flag in (0,1,255):
                        args=list(preparar_caso('ordinary',MundoRastreado))
                        data=bytearray(args[1]);struct.pack_into('<H',data,4,index)
                        data[6],data[8],data[6+0x72]=owner,state,flag
                        args[1]=data;args[0].busca.unidade=index
                        self.compare(args)

    def test_partial_bonus_and_original_discovery_call_boundaries(self):
        self.compare(preparar_caso('ordinary',MundoRastreado),0x428cc0)
        args=list(preparar_caso('ordinary',MundoRastreado))
        types=bytearray(args[3]);struct.pack_into('<H',types,42,9);args[3]=types
        self.compare(args,0x457019)
