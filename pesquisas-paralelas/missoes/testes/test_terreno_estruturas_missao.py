"""Frozen whole-state structure captures and optional fresh intact-x86 checks."""
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

OWNED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OWNED))
from casos_terreno_estruturas_missao import (casos_captura_terreno_estruturas,
    preparar_terreno_estruturas_missao)
from casos_habitaveis import montar_habitacao
from bonus_unidades import BonusUnidades
from construcoes_habitaveis import DependenciaHabitacao
from consultas_missao import numero_missao,existe_estrutura
from terreno_estruturas_missao import (ProvedoresTerrenoEstruturas,DependenciaTerrenoEstruturas,
    CHAMADAS_ESTRUTURAS,provedores_terreno_estruturas_core,preparar_estruturas_no_terreno,
    preparar_terreno_missao)
from terreno_unidades import ProvedoresTerrenoUnidades,provedores_terreno_core

CAPTURE=OWNED/'evidencias/captura-terreno-estruturas-missao-original.json'
CAPTURE_SHA='52232213ef3585a8523a04d24d5bcc9d472c90ff137769fb0cea48f9a41b777e'
NAMES=dict(existe='structure_exists',colocar='structure_place',habitada='structure_inhabited',
           habitar='structure_habitable',modificar_mapa='structure_map')


def hashes(blocos):
    return {nome:hashlib.sha256(dados).hexdigest() for nome,dados in blocos.items()}


def traced(function,name,trace):
    if not callable(function):
        return function
    def call(*args):
        trace.append((name,*args))
        return function(*args)
    return call


def preparar_python(caso,trace,missing=None):
    h=montar_habitacao(caso.economico)
    providers=provedores_terreno_estruturas_core(caso.mundo,habitacao=h,
                                               mascara_tipo20=caso.mascara_tipo20)
    if missing is not None:
        providers=replace(providers,**{missing:None})
    elif caso.nome=='missing_map':
        providers=replace(providers,modificar_mapa=None)
    providers=ProvedoresTerrenoEstruturas(**{name:traced(getattr(providers,name),label,trace)
                                           for name,label in NAMES.items()})
    if caso.entrada=='joined':
        bonus=BonusUnidades(caso.bonus,tipos_unidades=caso.tipos)
        bonus.memoria=caso.bonus  # constructor copies; bind the actual live declared allocation
        unit=provedores_terreno_core(caso.mundo,bonus_unidades=bonus)
        unit=ProvedoresTerrenoUnidades(traced(unit.existe,'unit_exists',trace),
            traced(unit.visibilidade,'unit_visible',trace),traced(unit.colocar,'unit_place',trace),
            traced(unit.capacidades,'capacity_refresh',trace))
        return lambda:preparar_terreno_missao(unit,providers)
    return lambda:preparar_estruturas_no_terreno(providers)


class MemoriaDeclaradaSemCPU:
    """Byte ledger for the existing fixture serializer; cannot execute instructions.

    This is only a local capture-replay memory backend. Fresh native oracles
    keep the real Unicorn class; no engine operation is modeled here.
    """
    def __init__(self,*args):
        self.regions={};self.registers={};self.hooks=[]

    def mem_map(self,address,size,permissions=7):
        if any(address<base+len(data) and base<address+size for base,data in self.regions.items()):
            raise ValueError('Overlapping fixture allocation')
        self.regions[address]=bytearray(size)

    def _region(self,address,size):
        for base,data in self.regions.items():
            if base<=address and address+size<=base+len(data):
                return data,address-base
        raise ValueError(f'Unmapped fixture range0x{address:x}/{size}')

    def mem_write(self,address,value):
        data,offset=self._region(address,len(value))
        data[offset:offset+len(value)]=value

    def mem_read(self,address,size):
        data,offset=self._region(address,size)
        return bytes(data[offset:offset+size])

    def mem_regions(self):
        return [(base,base+len(data)-1,7) for base,data in sorted(self.regions.items())]

    def reg_write(self,name,value):
        self.registers[name]=value

    def reg_read(self,name):
        return self.registers.get(name,0)

    def hook_add(self,*args):
        self.hooks.append(args)

    def emu_start(self,*args,**kwargs):
        raise AssertionError('Memory ledger has no CPU or instruction execution')


class ConsultasMissao(unittest.TestCase):
    def test_mission_getter_matches_original_and_reads_live_single_byte(self):
        report=json.loads(CAPTURE.read_text())
        for original in report['mission_number_query']['cases']:
            memory=bytearray([original['mission_byte'],original['neighbor_byte']])
            before=bytes(memory)
            self.assertEqual(numero_missao(memoryview(memory)[:1]),original['output_ax'])
            self.assertEqual(bytes(memory),before)
        memory=bytearray([1,255]);view=memoryview(memory)[:1]
        self.assertEqual(numero_missao(view),1)
        memory[0]=127
        self.assertEqual(numero_missao(view),127)
        self.assertEqual(numero_missao(memoryview(bytearray([255])).cast('b')),255)
        for invalid in (b'',b'\x01\x02',None,memoryview(bytearray(1)).cast('B',shape=(1,1))):
            with self.assertRaises(ValueError):
                numero_missao(invalid)

    def test_structure_query_width_live_pool_and_readonly_guards(self):
        pool=bytearray(276000)
        for index in (0,999):
            for state in range(256):
                pool[index*276+5]=state
                self.assertEqual(existe_estrutura(pool,index|0xa5000000),int(state!=0))
        before=bytes(pool)
        self.assertEqual(existe_estrutura(memoryview(pool).cast('b'),999),1)
        self.assertEqual(existe_estrutura(bytes(pool),999),1)
        self.assertEqual(bytes(pool),before)
        for index in (1000,65535,-1):
            with self.assertRaises(ValueError):
                existe_estrutura(pool,index)
        for invalid in (b'',memoryview(pool)[::2]):
            with self.assertRaises(ValueError):
                existe_estrutura(invalid,0)

    def test_live_lowAL_order_and_named_missing_call_keeps_previous_effects(self):
        events=[];state={'placed':False,'inhabited':False}
        def exists(index):
            return 0x101 if index==7 else 0x100
        def place(index):
            events.append(('place',index));state['placed']=True
        def inhabited(index):
            self.assertTrue(state['placed'])
            return 0x1ff
        def inhabit(index):
            events.append(('inhabit',index));state['inhabited']=True
        def modify(index,mode):
            self.assertTrue(state['inhabited']);events.append(('map',index,mode))
        providers=ProvedoresTerrenoEstruturas(exists,place,inhabited,inhabit,modify)
        result=preparar_estruturas_no_terreno(providers)
        self.assertEqual((result.colocadas,result.habitadas),((7,),(7,)))
        self.assertEqual(events,[('place',7),('inhabit',7),('map',7,1)])
        events.clear()
        with self.assertRaises(DependenciaTerrenoEstruturas) as error:
            preparar_estruturas_no_terreno(replace(providers,modificar_mapa=None))
        self.assertEqual((error.exception.endereco,error.exception.chamada,error.exception.argumentos),
                         (0x419e97,0x46c1b1,(7,1)))
        self.assertEqual(events,[('place',7),('inhabit',7)])

    def test_habitation_binding_rejects_copied_world_identity(self):
        caso=preparar_terreno_estruturas_missao('identity',habitantes=False)
        other=preparar_terreno_estruturas_missao('other',habitantes=False)
        with self.assertRaises(ValueError):
            provedores_terreno_estruturas_core(caso.mundo,habitacao=montar_habitacao(other.economico))


class CapturasEstruturasMissao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from bancada_terreno_estruturas_missao import BancadaTerrenoEstruturasMissao
            import emulador
        except ImportError as error:
            raise unittest.SkipTest(f'Optional memory-layout helper unavailable: {error}')
        class MemoriaSemExecucao(BancadaTerrenoEstruturasMissao):
            def executar(self,*args,**kwargs):
                raise AssertionError('Frozen capture replay must not execute original instructions')
            def retomar(self,*args,**kwargs):
                raise AssertionError('Frozen capture replay must not resume native execution')
        with patch.object(emulador.unicorn,'Uc',MemoriaDeclaradaSemCPU):
            cls.memory=MemoriaSemExecucao()

    def test_all_eight_whole_mapped_state_and_traces(self):
        self.assertEqual(hashlib.sha256(CAPTURE.read_bytes()).hexdigest(),CAPTURE_SHA)
        report=json.loads(CAPTURE.read_text())
        cases=list(casos_captura_terreno_estruturas())
        self.assertEqual(len(cases),len(report['cases']))
        for caso,original in zip(cases,report['cases']):
            with self.subTest(case=caso.nome):
                self.assertEqual(caso.nome,original['name'])
                self.memory.carregar_caso(caso)
                self.assertEqual(hashes(self.memory.antes),original['input_sha256'])
                trace=[];run=preparar_python(caso,trace)
                if caso.nome=='missing_map':
                    with self.assertRaises(DependenciaTerrenoEstruturas):
                        run()
                elif caso.nome=='owner4_discovery':
                    with self.assertRaises(DependenciaHabitacao):
                        run()
                else:
                    result=run()
                    if caso.entrada=='joined':
                        self.assertEqual(result.unidades.colocadas,(0,1,2,11,12,13,14,15))
                        result=result.estruturas
                    self.assertEqual(result.retorno_original,0x46b6f7)
                self.assertEqual(hashes(self.memory.estado_modelo(caso)),original['output']['sha256'])
                self.assertEqual([list(c) for c in trace],original['output']['calls'])
                self.assertEqual([list(e) for e in caso.mundo.efeitos],original['output']['effects'])
                self.assertEqual(self.memory.execucoes,0)


@unittest.skipUnless(os.environ.get('RISING_EMULAR')=='1','Optional intact-x86: RISING_EMULAR=1')
class DiferencialEstruturasMissao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from bancada_terreno_estruturas_missao import BancadaTerrenoEstruturasMissao
        from emulador import BancadaX86
        cls.native=BancadaTerrenoEstruturasMissao()
        cls.queries=BancadaX86()
        cls.structure_queries=cls.mission_queries=0

    def compare(self,caso,missing=None):
        b=self.native
        b.carregar_caso(caso)
        regs=b.executar_caso(caso)
        trace=[];run=preparar_python(caso,trace,missing)
        if missing or caso.nome=='missing_map':
            with self.assertRaises(DependenciaTerrenoEstruturas):
                run()
        elif caso.nome=='owner4_discovery':
            with self.assertRaises(DependenciaHabitacao):
                run()
        else:
            run()
        self.assertEqual(regs['EIP'],caso.parada[0] if caso.parada else 0x3000000)
        self.assertEqual(b.estado(),b.estado_modelo(caso),caso.nome)
        self.assertEqual(b.chamadas,trace,caso.nome)
        self.assertEqual(b.efeitos,caso.mundo.efeitos,caso.nome)

    def test_eight_original_inputs_fresh(self):
        for caso in casos_captura_terreno_estruturas():
            self.compare(caso)

    def test_slot_state_habitation_and_type_matrix(self):
        for index in (0,999):
            for state in (0,1,4,255):
                for inhabited in (False,True):
                    for kind in (2,9,17):
                        self.compare(preparar_terreno_estruturas_missao('matrix',tipo=kind,
                            dono=3 if index else 0,indice=index,estado=state,habitantes=inhabited))
        for index in (0,999):
            self.compare(preparar_terreno_estruturas_missao('type20',tipo=20,indice=index,
                                                        habitantes=False))

    def test_each_missing_callback_stops_at_original_callsite(self):
        for name,(_,callsite) in CHAMADAS_ESTRUTURAS.items():
            caso=preparar_terreno_estruturas_missao('MONDE01_missing_'+name)
            caso.parada=(callsite,None if name=='existe' else 0)
            self.compare(caso,name)

    def test_two_readonly_queries_over_full_original_consumed_domains(self):
        b=self.queries
        pool=bytearray(276000)
        b.cpu.mem_write(0x49a0c8,bytes(pool))
        for index in (0,999):
            for state in range(256):
                pool[index*276+5]=state
                b.cpu.mem_write(0x49a0c8+index*276+5,bytes([state]))
                before=bytes(b.cpu.mem_read(0x494000,0x8f000))
                regs=b.executar(0x41a735,[(0x41a735,0x41a75c)],dict(EAX=index|0xa5000000,EDX=0x5a5a5a5a))
                type(self).structure_queries+=1
                self.assertEqual(regs['EAX'],existe_estrutura(pool,index|0xa5000000))
                self.assertEqual(regs['EDX'],0x5a5a5a5a)
                self.assertEqual(bytes(b.cpu.mem_read(0x494000,0x8f000)),before)
        for number in range(256):
            field=bytearray([number])
            b.cpu.mem_write(0x496fe4,bytes([number,255-number]))
            before=bytes(b.cpu.mem_read(0x494000,0x8f000))
            regs=b.executar(0x46c11a,[(0x46c11a,0x46c122)],dict(EAX=0xa5a5ffff))
            type(self).mission_queries+=1
            self.assertEqual(regs['EAX'],0xa5a50000|numero_missao(field))
            self.assertEqual(bytes(b.cpu.mem_read(0x494000,0x8f000)),before)
