"""Standalone input/mission captures and perturbed Rust/Python frame providers.

Input entry captures contain changed bytes but no read set. Their fixtures use
historical MissionLoad DGROUP bytes, declared cursor inputs and captured old
bytes; they are not claimed to reproduce the whole original entry image.
Missing pages in other isolated fixtures are synthetic, as documented by the
shared helper. Native claims cover captured writes and defined return bits.
"""
import base64
import ctypes as C
import hashlib
import json
from pathlib import Path
import random
import sys
import zlib

import unittest
from frame_abi import Frames
from test_frame_core_economy import Memory, blocks_from_capture, core, economy

ROOT=Path(__file__).resolve().parents[2]
for folder in ('pesquisas-paralelas/ia-runtime','pesquisas-paralelas/missoes',
               'pesquisas-paralelas/combate','pesquisas-paralelas/graficos-animacao'):
    path=str(ROOT/folder)
    if path not in sys.path:sys.path.append(path)
import ambiente_ia_runtime  # noqa: F401
import entrada_quadro_ia as input_reference
import fim_missao as mission_reference
import influencia_missao as influence_reference
import affgame_hud_ia as hud_reference
import efeitos_logicos_exibicao as display_reference
from projeteis import PoolProjeteis
from maquina_projeteis import MaquinaProjeteis
from alvos_alcance import ocupa_celula

INPUT_CAPTURE='pesquisas-paralelas/ia-runtime/evidencias/captura-entradas-quadro1-ia-exibicao.json'
MISSION_CAPTURE='pesquisas-paralelas/missoes/evidencias/captura-isolada-missoes-quadro1.json'
M1_CAPTURE='pesquisas-paralelas/missoes/evidencias/captura-carga-missao-exibicao.json'
FRAME_CAPTURE='pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-exibicao.json'
IDS={'InputGame':300,'InputSend':301,'CalculIconeAction':302,'EvenementEnCours':303,
     'TestFinDeMission':304,'ProjectileCalcul':305,'AffGame':306}
PINS = {'pesquisas-paralelas/ia-runtime/evidencias/captura-entradas-quadro1-ia-exibicao.json': 'ac0c36efb2a9dccd78cf17fb39a8b4bc283c1cee7e9e7ef29e99a73cdac5b275', 'pesquisas-paralelas/missoes/evidencias/captura-isolada-missoes-quadro1.json': 'd0365055c113ae09fb3a078d54802c3538e84ec7b6b72d7268b062763da18e25', 'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-exibicao.json': '6339736e9cc1b0c53628295a2a81d51e168e37ac14d6255eb7c30a99a784dcf6', 'pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-exibicao.json': 'b7e55bb2e00672fa0941682eb797f6678bdf29ca5ed2e0dc25b3790665aaaad1', 'pesquisas-paralelas/ia-runtime/entrada_quadro_ia.py': 'cd8554870537125e4424762e4e2ed485a7d6c0a7b042a01908c543615c7962ed', 'pesquisas-paralelas/missoes/fim_missao.py': 'd4fd4ba3db45952f7f31c83a5e80b0481c58f99257b84f2bf68888b0862697da', 'pesquisas-paralelas/missoes/influencia_missao.py': '5a601f8bbd7cb3c4396b1f8c72e01b25dec394625cab5cbf195d06f6e01ecaaa', 'pesquisas-paralelas/ia-runtime/affgame_hud_ia.py': 'afdb24dacf4c58646b81e16e6826a106065a2e8b200e3013ed3f89bdb9332708', 'pesquisas-paralelas/graficos-animacao/efeitos_logicos_exibicao.py': 'ba95194a67c700528e27ad87640cf5c95de92e9c9d9e8feb054002edf71d2f93', 'pesquisas-paralelas/combate/maquina_projeteis.py': '4e2ba7a57edddbc57f7980d1ed8bdad5c100f037c269e54a9e7b4c224651e7d9', 'pesquisas-paralelas/combate/avanco_projeteis.py': '02a50742ad595d1ed73ed5d9ae725ce0734f4afd4ff27e51fb16dee969d9be3f', 'pesquisas-paralelas/combate/projeteis.py': 'a25e6f4c386410e09b96d3b94d5e787f0ed44984264312af350ccb5f44f3ce89'}


class InputMemory(Memory):
    def s8(self,address):
        value=self.u8(address)
        return value-256 if value&128 else value


class DeclaredWindows:
    def tecla(self,vk):
        if vk not in {0x1b,0x10,0x11,0x2e,0x12,0x20,0x26,0x28,0x27,0x25,0x0d,0x58}:
            raise AssertionError(f'Unexpected key query {vk:#x}')
        return 0


class BindingLog:
    def __init__(self):self.bindings=[]
    def vinculo(self,*args,**kwargs):self.bindings.append((args,kwargs))


def python_mission(m,player):
    q=mission_reference.ConsultasFimMissao(
        existe=lambda j:int(m.u8(0x49a0c8+276*j+5)!=0),
        dono=lambda j:m.u8(0x49a0c8+276*j+4),
        tipo=lambda j:economy.tipo_estrutura_viva(m,j),
        recursos=lambda p,f,s,t:economy.recursos_suficientes(m,p,f,s,t),
        numero_missao=lambda:m.u8(0x496fe4),
        celula=lambda j:core.caso_estrutura(m,j)['EAX'],
        zona=lambda c:influence_reference.zona_influencia(m.vista(0x50c614,4000),c),
        invencoes=lambda p:economy.numero_invencoes(m,p),
        aliado=lambda a,b:economy.aliado(m,a,b),
        canto_zona=lambda z:influence_reference.canto_zona_influencia(m.vista(0x50c614,4000),z),
        iluminada=lambda c,p:core.caso_esta_iluminada(m,c,p)['EAX'])
    return mission_reference.testar_fim_missao(player,m.vista(0x4e1d20,100),m.vista(0x4e1d84,14),
        m.vista(0x4e1a3a,2),m.vista(0x4e1928,8),m.vista(0x4dfaa8,16),q)


def python_input(name,m,player=0):
    if name=='InputGame':
        providers=core.provedores_core(m)
        providers['EnginOccupeCase']=lambda sitio,unidade,celula,filtro:int(ocupa_celula(
            m.ler(m.u32(0x4e19a0)+276*unidade,276),celula,filtro))
        input_reference.entrada_jogo(m,player,BindingLog(),DeclaredWindows(),providers)
    elif name=='InputSend':input_reference.enviar_entrada(m,player)
    elif name=='CalculIconeAction':return input_reference.calcular_icone_acao(m)
    else:raise AssertionError(name)


class InputMissionsProviders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for path,expected in PINS.items():
            if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected:
                raise AssertionError(f'Reference identity changed: {path}')
        cls.abi=Frames()
        fn=cls.abi.lib.rl_executar_rotina_quadro
        fn.argtypes=[C.c_uint64,C.c_uint32,C.POINTER(C.c_uint32),C.c_uint32,C.POINTER(C.c_uint32)]
        fn.restype=C.c_int32

    def rust(self,name,blocks,args):
        handle=self.abi.create()
        try:
            self.abi.load(handle,blocks)
            array=(C.c_uint32*len(args))(*args);out=C.c_uint32(0xdeadbeef)
            self.abi.check(self.abi.lib.rl_executar_rotina_quadro(handle,IDS[name],array,len(args),C.byref(out)))
            return self.abi.snapshot(handle),out.value
        finally:self.abi.free(handle)

    def test_original_mission_isolated_captures(self):
        total=0
        for call in json.loads((ROOT/MISSION_CAPTURE).read_bytes())['calls']:
            for captured in call['cases']:
                name=call['routine'];case=dict(captured,routine=name)
                with self.subTest(routine=name,phase=call['phase'],case=captured['case']):
                    m=blocks_from_capture(case);initial=list(m.export().items())
                    p=int(case['entry_registers']['EAX'],16)&255
                    expected=(mission_reference.evento_em_curso(m.vista(0x4e1b0e,1)) if name=='EvenementEnCours'
                              else python_mission(m,p))
                    actual,value=self.rust(name,initial,[] if name=='EvenementEnCours' else [p])
                    self.assertEqual(actual,m.export());self.assertEqual(value&255,case['al'])
                    self.assertEqual(value&255,expected&255)
                    for a,old,new in case['changed_bytes']:self.assertEqual(m.u8(int(a,16)),new,(name,a,old))
                    total+=1
        self.assertEqual(total,4)

    def test_original_input_captured_writes(self):
        capture=json.loads((ROOT/INPUT_CAPTURE).read_bytes())
        captured_blocks=json.loads((ROOT/M1_CAPTURE).read_bytes())['oracle']['final_state']['blocks']
        block=captured_blocks['dgroup']
        original=zlib.decompress(base64.b64decode(block['zlib_base64']))
        self.assertEqual(hashlib.sha256(original).hexdigest(),block['sha256'])
        blocks=[(int(block['base'],16),original)]
        m=InputMemory(blocks)
        pointers={m.u32(a) for a in (0x507d78,0x507d88,0x507d74,0x507d70,0x4e0f38,0x4e19a0)}
        for captured in captured_blocks.values():
            base=int(captured['base'],16)
            if base not in pointers:continue
            data=zlib.decompress(base64.b64decode(captured['zlib_base64']))
            self.assertEqual(hashlib.sha256(data).hexdigest(),captured['sha256'])
            blocks.append((base,data))
        self.assertEqual(len(blocks),len(pointers)+1)
        m=InputMemory(blocks)
        frame=json.loads((ROOT/FRAME_CAPTURE).read_bytes())
        total=0
        for case in capture['calls']:
            name=case['routine']
            if name in ('InputGame','InputSend','CalculIconeAction'):
                with self.subTest(routine=name,phase=case['phase']):
                    # Explicit per-call fixture inputs: only changed old bytes are
                    # native observations of entry; all other fixture bytes retain
                    # their documented source, without an entry-image hash claim.
                    for a,old,new in case['changed_bytes']:m.u8(int(a,16),old)
                    if case['phase']=='frame1':
                        x,y=frame['named_inputs']['frame']['cursor'];m.u16(0x5099a8,x);m.u16(0x5099aa,y)
                    initial=list(m.export().items());player=int(case['entry_registers']['EAX'],16)&255
                    value_python=python_input(name,m,player)
                    actual,value=self.rust(name,initial,[] if name=='CalculIconeAction' else [player])
                    self.assertEqual(actual,m.export())
                    for a,old,new in case['changed_bytes']:self.assertEqual(m.u8(int(a,16)),new,(name,a,old))
                    if value_python is not None:
                        self.assertEqual(value,value_python);self.assertEqual(value,int(case['exit_registers']['EAX'],16))
                    total+=1
            # Carry only recorded DGROUP changes to later standalone fixtures.
            for change in case['changed_bytes']:
                if isinstance(change,dict):
                    self.assertEqual(change['event'],'released')
                    continue  # DGROUP fixture has no allocation records.
                a,old,new=change
                address=int(a,16)
                if int(block['base'],16)<=address<int(block['base'],16)+len(original):m.u8(address,new)
        self.assertEqual(total,6)

    def test_randomized_mission_conditions_resources_and_latch(self):
        rng=random.Random(0x458606)
        for trial in range(64):
            m=Memory([(0x494000,bytes(0x523000-0x494000)),
                      (0x10000000,bytes(100)),(0x10010000,bytes(65536))])
            m.u32(0x5080a8,0x10000000);m.u8(0x496fe4,rng.choice([1,2,3,4,5,7,9,10,11,12]))
            p=rng.randrange(4);m.u16(0x4e1a3a,rng.choice([0,1,16,65535]))
            m.u8(0x4e1d84,rng.randrange(256))
            for owner in range(4):
                m.u8(0x10000000+20*owner+6,rng.randrange(256))
                m.u8(0x50871c+owner,rng.randrange(256))
                m.u16(0x4e1928+2*owner,rng.choice([0,0,1,65535]))
                m.u32(0x4dfaa8+4*owner,rng.choice([0,0,1,0xffffffff]))
                for resource in range(4):m.u16(0x4e2ea8+32*owner+8*resource+2,rng.randrange(65536))
            for i in range(10):
                r=0x4e1d20+10*i;kind=rng.choice([0,1,2,3,4,5,6,254,255])
                m.u8(r,kind);m.u16(r+2,rng.choice([0,1,50,255,65535]));m.u8(0x4e1d88+i,rng.randrange(256))
                for o in (4,6,8):m.u16(r+o,rng.choice([0,255,399,65535]))
            initial=list(m.export().items());expected=python_mission(m,p)
            actual,value=self.rust('TestFinDeMission',initial,[p])
            self.assertEqual(actual,m.export(),trial);self.assertEqual(value,expected,trial)

    def test_randomized_rain_scroll_and_input_help_timer(self):
        rng=random.Random(0x45ac31)
        for trial in range(32):
            m=InputMemory([(0x494000,bytes(0x523000-0x494000))])
            # Zone1 avoids unrelated hover callees and takes the accepted scroll path.
            m.u16(0x50a9b4,1);m.u16(0x50a9b6,1)
            for o,v in enumerate([0,0,1,1]):m.u32(0x5099c4+4*o,v)
            m.u16(0x508720,rng.randrange(65536));m.u16(0x508722,rng.randrange(65536))
            m.u16(0x4e0610,rng.randrange(65536));m.u16(0x49620a,rng.randrange(65536))
            m.u8(0x496d2c,1);m.u16(0x496d2e,rng.choice([0xffff,0xfffe,0xfffd,0xfffc,0xfffa,0xff80]))
            for i in range(120):
                r=0x4e1da0+6*i;m.u16(r,rng.randrange(65536));m.u16(r+2,rng.randrange(65536));m.u8(r+4,rng.randrange(256))
            initial=list(m.export().items());python_input('InputGame',m,0)
            actual,_=self.rust('InputGame',initial,[0]);self.assertEqual(actual,m.export(),trial)

    def test_randomized_affgame_effects_and_inactive_projectile_animation(self):
        rng=random.Random(0x417698)
        for trial in range(24):
            m=Memory([(0x494000,bytes(0x523000-0x494000)),(0x10000000,bytes(5600))])
            m.u32(0x5080f0,0x10000000);m.u8(0x4e2f78,0x12);m.u16(0x496204,65535)
            m.u16(0x508724,25);m.u16(0x508726,17);m.u32(0x4e179c,1)
            m.u32(0x508f7c,rng.getrandbits(32));m.u8(0x497284,rng.randrange(1,256))
            m.u8(0x4e05a2,rng.randrange(2));m.u8(0x4dfb44,rng.randrange(256));m.u8(0x4e1d18,rng.randrange(256));m.u8(0x49a05b,rng.randrange(8))
            initial=list(m.export().items())
            def draw(memory):
                effect=display_reference.desenhar_jogo(memory)
                for address,width,value in effect.escritas:{1:memory.u8,2:memory.u16,4:memory.u32}[width](address,value)
            effect=hud_reference.affgame_hud(m,draw)
            for address,width,value in effect.escritas:{1:m.u8,2:m.u16,4:m.u32}[width](address,value)
            actual,value=self.rust('AffGame',initial,[])
            self.assertEqual(actual,m.export(),trial);self.assertEqual(value,effect.eax,trial)
            for i in range(100):
                a=0x10000000+56*i;m.u8(a,rng.choice([0,1,2,5,17,20,21,23,24,29,30,31,32,33,34,255]));m.u8(a+1,rng.randrange(256));m.u8(a+0x18,rng.randrange(256))
            initial=list(m.export().items())
            MaquinaProjeteis(PoolProjeteis(memoria=m.vista(0x10000000,5600))).calcular(m.u8(0x508f7c))
            actual,_=self.rust('ProjectileCalcul',initial,[]);self.assertEqual(actual,m.export(),trial)
