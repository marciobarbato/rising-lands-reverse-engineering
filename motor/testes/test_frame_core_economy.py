"""Rust provider replay against original-only captures and unchanged Python.

Unobserved bytes in declared pages are synthetic zero fixtures, never evidence.
Every captured read and changed-byte entry is overlaid before both executions;
all projected bytes must equal Python, and every original compared write/result
must equal the capture. Rendering/unknown register effects are not asserted.
"""
from pinned_reference import activate, reference_file, pinned_file
SOURCE_ROOT = activate()

import ctypes as C
import hashlib
import json
from pathlib import Path
import random
import sys
import unittest

from frame_abi import Frames

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SOURCE_ROOT / 'ferramentas'))
sys.path.insert(0, str(SOURCE_ROOT))
import chamadas_quadro_core as core
from integracao.providers import load_economy_bonus
load_economy_bonus()
sys.path.insert(0, str(SOURCE_ROOT / 'pesquisas-paralelas/economia'))
import quadro_economia as economy

PINS = {'ferramentas/chamadas_quadro_core.py': 'd8b3568c3346422744868a2b7900e4afdbf84c85e840450f9da5ec863bbb626a', 'pesquisas-paralelas/economia/quadro_economia.py': '28342fb2e68f4e400e79ff321bc6eef5098628ac4941bff25fc48ff48bc38ea2', 'evidencias/fundacoes-quadro/captura-chamadas-quadro1.json': 'fd209b2fb85794a52f778cb757ef79b6a4c42495763407ff731f98a05b4a5a8a', 'evidencias/fundacoes-quadro/captura-zonas-animacao-quadro1.json': '277496ffb203b28e02120f202cd7430af757bedc777f4941b2eb752fba8f1adc', 'evidencias/fundacoes-quadro/captura-exibicao-quadro1.json': 'b4e6747324346ac1aacc1a36b5c31f4ae87b3a35551c6303b32265133385dee0', 'pesquisas-paralelas/economia/evidencias/captura-quadro1-economia-exibicao.json': '53c9d5db27d66483750e9a9df24f6de8538cead45621e81425cc89812fef4439', 'pesquisas-paralelas/economia/evidencias/captura-consultas-economia-exibicao-v2.json': 'fada576f61e00203097cb8c6b610650117416620011835fd9f55c86aea4559c0'}

CORE_IDS = {'Random':200,'rand':201,'GetBit':202,'SetBit':203,'CaseEstDecouverte':204,
            'CaseEstIlluminee':205,'BatimentCollision':206,'BatimentGetCase':207,
            'BatimentEstDecouvert':208,'BatimentContourEstIllumine':209,
            'SetEnginCollision':210,'CalculFatigue':211,'SetClipping':212,'InitGameZone':213,
            'MouseSetZone':214,'MouseTestZone':215,'NextAnimTerrain':216,'NextAnimVeget':217,
            'GameNextFrame':219,'SetCollision':220,'ChercheContacteur':221,
            'MessageBoxExiste':222,'PlayerEstContacterPourAlliance':223}
ECON_IDS={'CalculMatiere':250,'RechercheCalcul':251,'PlayerInitAllianceCompteur':252,
          'PlayerAttaqueCalculSympa':253,'MAJSympathie':254,'SetUpdateChamp':255,
          'UpdateChamp':256,'ResetTableauHangar':257,'GetMeteo':258,'CalculCompteurMarche':259,
          'CalculCompteurProposition':260,'BonusGetValEngin':261,'EnginNextEtape:state7':262,
          'BatimentNextEtape:type1_2_13_16':263,'CalculTroupe':264,'PlayerGetType':265,
          'PlayerEstAllie':266,'RechercheGetNbInvention':267,'BatimentGetType':268,
          'BagVide':269,'PlayerGetColor':270,'BagContientTroupe':271}


class Memory:
    def __init__(self, blocks):
        self.blocks = [(a, bytearray(b)) for a,b in blocks]
    def vista(self,a,n):
        for base,data in self.blocks:
            if base <= a and a+n <= base+len(data):
                return memoryview(data)[a-base:a-base+n]
        raise ValueError(f'Undeclared test memory {a:#x}+{n}')
    def ler(self,a,n): return bytes(self.vista(a,n))
    def _access(self,n,a,v):
        view=self.vista(a&0xffffffff,n)
        if v is None:return int.from_bytes(view,'little')
        view[:]=(v&((1<<(8*n))-1)).to_bytes(n,'little')
        return v
    def u8(self,a,v=None):return self._access(1,a,v)
    def u16(self,a,v=None):return self._access(2,a,v)
    def u32(self,a,v=None):return self._access(4,a,v)
    def export(self):return {a:bytes(b) for a,b in self.blocks}


def blocks_from_capture(case):
    known={}
    for field in ('read_before_write','changed_bytes','written_unchanged',
                  'caller_stack_changes','caller_stack_written_unchanged'):
        for a,old,*_ in case.get(field,[]):
            if old is not None:known[int(a,16)]=old
    pages={a&~4095 for a in known}
    pages.update(range(0x494000,0x523000,4096))
    # Frame providers may write bytes natively written unchanged but absent from
    # historical Core capture write sets. These are explicitly synthetic pages.
    if case['routine']=='InitGameZone':pages.update(range(0x509000,0x50b000,4096))
    ranges=[]
    for page in sorted(pages):
        if ranges and ranges[-1][0]+len(ranges[-1][1])==page:ranges[-1][1].extend(bytes(4096))
        else:ranges.append((page,bytearray(4096)))
    m=Memory(ranges)
    for a,v in known.items():m.u8(a,v)
    return m


def arguments(name,r,case):
    if name in ('Random','rand','GameNextFrame','CalculMatiere','RechercheCalcul',
                'PlayerInitAllianceCompteur','PlayerAttaqueCalculSympa','SetUpdateChamp',
                'UpdateChamp','ResetTableauHangar','GetMeteo'):return []
    if name in ('SetBit','MAJSympathie'):return [r['EAX'],r['EDX'],r['EBX']]
    if name=='SetClipping':return [r['EAX'],r['EDX'],r['EBX'],r['ECX']]
    if name=='MouseSetZone':return [r['EAX'],r['EDX'],r['EBX'],r['ECX'],int(case['exit_registers']['EDX'],16)]
    if name=='BonusGetValEngin':return [r['EAX'],r['EBX'],r['EDX'],r['ECX']]
    if name in ('EnginNextEtape:state7','BatimentNextEtape:type1_2_13_16'):return [r['EDI']]
    if name in ('GetBit','CaseEstDecouverte','CaseEstIlluminee','BatimentCollision',
                'BatimentEstDecouvert','BatimentContourEstIllumine','SetEnginCollision',
                'MouseTestZone','NextAnimTerrain','NextAnimVeget','PlayerEstContacterPourAlliance',
                'SetCollision','CalculCompteurProposition','PlayerEstAllie'):return [r['EAX'],r['EDX']]
    return [r['EAX']]


def economy_python(name,m,a):
    methods={'CalculMatiere':economy.calcular_materia,'RechercheCalcul':economy.calcular_pesquisa,
             'PlayerInitAllianceCompteur':economy.contar_aliancas,
             'PlayerAttaqueCalculSympa':economy.calcular_simpatia_ataques,
             'ResetTableauHangar':economy.resetar_tabela_hangar,'GetMeteo':economy.calcular_meteo,
             'CalculCompteurMarche':economy.calcular_contador_mercado,
             'CalculCompteurProposition':economy.calcular_contador_proposicao,
             'MAJSympathie':economy.atualizar_simpatia,
             'EnginNextEtape:state7':economy.estado_parado_unidade,
             'PlayerGetType':economy.tipo_jogador,'PlayerEstAllie':economy.aliado,
             'BatimentGetType':economy.tipo_estrutura_viva,'BagVide':economy.bolsa_vazia}
    if name=='BonusGetValEngin':
        return load_economy_bonus().BonusUnidades.da_memoria(m).consultar(*a[:3],ecx=a[3])
    return methods[name](m,*a)


class FrameProviders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path,expected in PINS.items():
            if hashlib.sha256(pinned_file(ROOT/path).read_bytes()).hexdigest()!=expected:
                raise AssertionError(f'Reference identity changed: {path}')
        cls.abi=Frames()
        fn=cls.abi.lib.rl_executar_rotina_quadro
        fn.argtypes=[C.c_uint64,C.c_uint32,C.POINTER(C.c_uint32),C.c_uint32,C.POINTER(C.c_uint32)]
        fn.restype=C.c_int32

    def rust(self,identifier,blocks,args):
        handle=self.abi.create()
        try:
            self.abi.load(handle,blocks)
            out=C.c_uint32(0xdeadbeef)
            array=(C.c_uint32*len(args))(*args)
            self.abi.check(self.abi.lib.rl_executar_rotina_quadro(handle,identifier,array,len(args),C.byref(out)))
            return self.abi.snapshot(handle),out.value
        finally:self.abi.free(handle)

    def test_original_core_capture_replay(self):
        total=0
        for path in ('evidencias/fundacoes-quadro/captura-chamadas-quadro1.json',
                     'evidencias/fundacoes-quadro/captura-zonas-animacao-quadro1.json',
                     'evidencias/fundacoes-quadro/captura-exibicao-quadro1.json'):
            for case in json.loads(pinned_file(ROOT/path).read_bytes())['calls']:
                name=case['routine']
                if name not in CORE_IDS:continue
                with self.subTest(source=path,routine=name,case=total):
                    m=blocks_from_capture(case);initial=list(m.export().items())
                    regs={k:int(v,16) for k,v in case['entry_registers'].items()}
                    args=arguments(name,regs,case)
                    # Direct callback preserves partial reads; no full bonus table filler.
                    def bonus(p,t,s):
                        return (0 if (p&255) in (4,200) else m.u16(0x4dfba0+(p&255)*468+(t&255)*18)) if s==0 else (_ for _ in ()).throw(AssertionError(s))
                    py=core.ROTINAS[name][1](m,regs,args[-1] if name=='MouseSetZone' else None,bonus)
                    actual,value=self.rust(CORE_IDS[name],initial,args)
                    self.assertEqual(actual,m.export())
                    for address,old,new in case['changed_bytes']:
                        self.assertEqual(m.u8(int(address,16)),new,(name,address,old))
                    if 'EAX' in py and name not in ('InitGameZone','NextAnimVeget'):
                        self.assertEqual(value,py['EAX'])
                        self.assertEqual(value,int(case['exit_registers']['EAX'],16))
                    total+=1
        self.assertEqual(total, 773)

    def test_original_economy_capture_replay(self):
        total=0
        # Production/field object joins are exercised by the whole-phase chain;
        # here each listed standalone provider is replayed from its own capture.
        supported=set(ECON_IDS)-{'SetUpdateChamp','UpdateChamp','BagContientTroupe',
                               'CalculTroupe','BatimentNextEtape:type1_2_13_16'}
        for path in ('pesquisas-paralelas/economia/evidencias/captura-quadro1-economia-exibicao.json',
                     'pesquisas-paralelas/economia/evidencias/captura-consultas-economia-exibicao-v2.json'):
            for case in json.loads(pinned_file(ROOT/path).read_bytes())['calls']:
                name=case['routine']
                if name not in supported:continue
                with self.subTest(source=path,routine=name,case=total):
                    m=blocks_from_capture(case);initial=list(m.export().items())
                    regs={k:int(v,16) for k,v in case['entry_registers'].items() if isinstance(v,str) and v.startswith('0x')}
                    args=arguments(name,regs,case)
                    expected=economy_python(name,m,args)
                    actual,value=self.rust(ECON_IDS[name],initial,args)
                    self.assertEqual(actual,m.export())
                    for address,old,new in case['changed_bytes']:
                        self.assertEqual(m.u8(int(address,16)),new,(name,address,old))
                    if expected is not None:
                        self.assertEqual(value,expected)
                        mask=0xffff if name=='BonusGetValEngin' else (0xffffffff if name=='BagVide' else 255)
                        self.assertEqual(value&mask,int(case['exit_registers']['EAX'],16)&mask)
                    total+=1
        self.assertEqual(total, 132)

    def test_perturbed_animation_and_resource_values(self):
        rng=random.Random(0x42c868)
        for k in range(24):
            data=bytearray(0x523000-0x494000)
            m=Memory([(0x494000,data),(0x10000000,bytes(0x20000)),
                      (0x10020000,bytes(0x10000)),(0x10030000,bytes(0x10000)),
                      (0x10040000,bytes(16))])
            for a,v in ((0x507d70,0x10000000),(0x507d74,0x10020000),
                        (0x507dac,0x10030000),(0x522244,0x10040000),
                        (0x4990cc,0x48e7c7),(0x1004000c,rng.getrandbits(32))):m.u32(a,v)
            m.u16(0x508724,9);m.u16(0x508726,5);m.u32(0x508f7c,k)
            m.u8(0x4e1d18,rng.randrange(256))
            for i in range(256):m.u8(0x4e1c18+i,rng.randrange(256))
            for y in range(5):
                for x in range(9):
                    c=y*256+x
                    m.u16(0x10000000+c*2,rng.choice([0x5d,0x94,0x95,0x9c,0x251,0x255,0x6d,0x8c]))
                    m.u8(0x10020000+c,rng.choice([0,1,9,0x18,0x1b,0x37,0x38,0x3a,0x3e]))
                    m.u8(0x10030000+c,rng.randrange(256))
            for name in ('NextAnimTerrain','NextAnimVeget'):
                initial=list(m.export().items())
                core.ROTINAS[name][1](m,dict(EAX=0,EDX=0,EDI=0,ECX=0),None,None)
                actual,_=self.rust(CORE_IDS[name],initial,[0,0])
                self.assertEqual(actual,m.export(),(k,name))
            for i in range(4):
                a=0x4e2ea8+8*i;m.u16(a+2,rng.randrange(65536));m.u16(a+4,rng.randrange(65536));m.u8(a+6,rng.randrange(256))
            initial=list(m.export().items());economy.calcular_materia(m)
            actual,_=self.rust(250,initial,[]);self.assertEqual(actual,m.export(),k)

    def test_perturbed_field_growth(self):
        from integracao.providers import load_economy_resources
        resources_type=load_economy_resources().RecursosTerreno
        rng=random.Random(0x478806)
        for k in range(12):
            m=Memory([(0x494000,bytes(0x523000-0x494000)),
                      (0x10000000,bytes(0x20000)),(0x10020000,bytes(0x10000)),
                      (0x10030000,bytes(0x10000)),(0x10040000,bytes(0x10000))])
            for a,v in ((0x507d70,0x10000000),(0x507d74,0x10020000),
                        (0x507dac,0x10030000),(0x507da8,0x10040000),
                        (0x497164,rng.getrandbits(32)),(0x508f7c,k*128)):m.u32(a,v)
            row=rng.randrange(1,256);m.u16(0x4973e8,row);m.u16(0x4973ea,128)
            m.u8(0x509952,k&1)
            for x in range(1,255):
                c=row*256+x
                m.u8(0x10020000+c,rng.choice([0,0x1c,0x1d,0x24,0x27,0x28,0x29,0x30,0x33,0x34]))
                for d in (-1,1,-256,256):
                    n=(c+d)&65535
                    m.u16(0x10000000+2*n,rng.choice([0x84,0x86,0x9d,0xdc,0x83,0xdd]))
                    m.u8(0x10040000+n,rng.randrange(2))
            for name,method in (('SetUpdateChamp',economy.agendar_campos),('UpdateChamp',economy.atualizar_campos)):
                initial=list(m.export().items())
                resources=resources_type.da_memoria(m)
                method(m,resources)
                actual,_=self.rust(ECON_IDS[name],initial,[])
                self.assertEqual(actual,m.export(),(k,name))
