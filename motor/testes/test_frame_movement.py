"""Stage2c original-first raid/movement providers and live-grid Python regressions.

Frozen call read sets and old changed bytes are overlaid on the committed M1
state to make standalone fixtures. Extra fields preserve that declared fixture;
this does not claim the complete original call-entry image was captured.
"""
from pinned_reference import activate, reference_file, pinned_file
SOURCE_ROOT = activate()

import base64
import bisect
import ctypes as C
import hashlib
import json
import random
import struct
import sys
import unittest
import zlib
from pathlib import Path
from frame_abi import Frames
from test_frame_core_economy import Memory

ROOT=Path(__file__).resolve().parents[2]
for f in ('ferramentas','pesquisas-paralelas/combate','pesquisas-paralelas/economia'):
    if str(SOURCE_ROOT/f) not in sys.path:sys.path.append(str(SOURCE_ROOT/f))
import incursao_core
from compactar_captura_isolada import expandir
from mundo_vivo import mundo_vivo
from solucionador_vivo import SolucionadorCaminhosVivo
from otimizacao_caminhos import ContextoLinha,otimizar_rota,testar_linha
from integracao.providers import load_economy_bonus

M1='pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json'
RAID='evidencias/fundacoes-quadro/captura-incursao-core-exibicao.json'
MOVEMENT='evidencias/fundacoes-quadro/captura-movimento-incursao-v1.json'
IDS={'GetFreeCell':450,'CreerEngin':451,'EnginSetPlayer':452,'PlaceEngin':453,
'EnginGetCase':454,'GetRandCaseChamps':455,'GetRandCaseTypeBatPlayer':456,
'Chemin_Accessible':457,'SetDeplaceEngin':458,'EnginEnArret':459,'DeplaceEngin':460,
'CalculNextCase':461,'AvanceEngin':462,'EnginNextCase':463,'EnginNextCaseChemin':464,
'CheminCalcul':465,'OptimiseChemin':466,'Chemin_Verouille':467,'RotateEngin':468,
'SetMiniMap':469,'EnginSetType':470,'EnginSetTypeCaract':471,'TestLigneOptimise':472,
'ResetEnginCollision':473,'EnginPeutPasser':474,'ChercheIndiceEngin':475,
'CalculDirection':476,'CalculDirCase':477,'Distance2d':478,'ResetOrdre':479,
'EnginEstVivant':480,'TerrainEnCollision':481,'ResetCollision':482,'memset':483,
'GetNumIndiceTypeBatiment':484,'GetCaseIndiceBatiment':485,'PlayerGetColor':486,
'EnginTypeGetCapacite':487}
PINS={'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json': 'eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc', 'evidencias/fundacoes-quadro/captura-incursao-core-exibicao.json': 'a76e3fac8c835e46805e594834f10f2bcb39734f944b57bde6a674bf5089f897', 'evidencias/fundacoes-quadro/captura-movimento-incursao-v1.json': '1881f8bfba7806050a7d3200130745cf21429b0479cfdb2d01c8294df91c349d', 'ferramentas/incursao_core.py': '1f5fa0cd43247d83387aa8650de9edf0b8ccd356250df469953469e79ad5873b', 'ferramentas/mundo_vivo.py': 'a4c5c2e5f73d09ce6f7bcbd6a15dbbcc5d264cff1c880bc7602ebf317dc3df5c', 'ferramentas/solucionador_vivo.py': '4a39571f29e5106c1d79411948e001a6972b5013975da6664d01f6f8c3344b73', 'ferramentas/solucionador_python.py': '67bddc7c5cc197ddd8dc1608457b2155f33554999502ddcdacec4add943465eb', 'ferramentas/navegacao_unidades.py': 'bb122c74953d43eb97cde4076fe1f53bd811087f87e575810bce90240930aedf', 'ferramentas/avanco_unidades.py': 'b0592c2101f26f59d927be5dcb64010b7d4849f9502fc130ad85c7e36ecf8276', 'ferramentas/visao_movimento.py': 'cd61354c6afcd0bc26eb9e7a8db93f5a3cf056d95e58606476783d3e4695255c', 'ferramentas/passagem_unidades.py': 'c7e74e05a86fb3789238c5fc89964d095cf90586c1e80ed4cb0b9dd320b13d1a', 'ferramentas/movimento.py': '1b814260ad8ec47a7c53e3e649655789ddb7db6ff704e9f329766a68a6e0cfed', 'ferramentas/caminhos.py': '37756835bc3ea010d2b3771d2d6ea8ebb9f400646becb4c35129b39df5173573', 'ferramentas/preparacao_destino.py': '4a760d637c9e1f0421cba08931c0a416e5e3a01b6e62eb51b9a9d259478fbc80', 'ferramentas/candidatos_rota.py': '35968ce6e78cc2bddca1dbafc4f2ecf38f0ff4e85178f5bfd03ca1ee7e118eec', 'ferramentas/contornos_caminhos.py': 'd671d4ff0347d02485d72362da6725986cbf779185cdc088bd4226e1278ca30b', 'ferramentas/otimizacao_caminhos.py': '1c5d3a83cf8c6f8af8ea7e80fbe5411e28decad5aeb5fab9c90ca21b234b235a', 'ferramentas/estruturas_caminhos.py': '2051800644f6bf9385e0072929897539e14265c86262252f38d6bf7293d8da3d', 'pesquisas-paralelas/combate/inicializacao_ataque.py': '4d1dc28c4b8dbcca1a0ea203d95c89cb3db3e5738eaad3f6b21be9abd7be55fc', 'ferramentas/ordens_unidades.py': '95b282cca6c29ff5fdbb3bb3c9cd25a25bec0202670a6dc78784ea6677cfefaf', 'ferramentas/grade_u16.py': '669d8ac6cb3bb6955aa73d98adda08d63a9675fb31946219b0b2a24c108a7bb4', 'ferramentas/compactar_captura_isolada.py': 'ff17d801df9d4e96f13f59901f5680b2422d719f4be52e3037ca9ee2a01e6f0f'}


class FastMemory(Memory):
    def __init__(self,blocks):
        super().__init__(sorted(blocks))
        self.bases=[a for a,_ in self.blocks]
    def vista(self,address,size):
        i=bisect.bisect_right(self.bases,address)-1
        if i>=0:
            base,data=self.blocks[i]
            if address+size<=base+len(data):return memoryview(data)[address-base:address-base+size]
        raise ValueError(f'Undeclared test memory {address:#x}+{size}')

Memory=FastMemory


def args_for(name,r,m,case):
    if name in ('GetRandCaseChamps','CheminCalcul'):return []
    if name in ('CreerEngin','EnginSetType'):return [r['EAX'],r['EDX'],r['EBX'],r['ECX']]
    if name in ('GetNumIndiceTypeBatiment','SetMiniMap','memset'):return [r['EAX'],r['EDX'],r['EBX']]
    if name=='Distance2d':return [r['EAX'],r['EDX'],r['EBX'],r['ECX']]
    if name=='AvanceEngin':return [r['EAX'],0]
    if name=='OptimiseChemin':return [m.u16(0x496304),r['EAX']]
    if name=='TestLigneOptimise':return [m.u16(0x496304),r['EAX'],r['EDX'],r['EBX']]
    if name=='Chemin_Verouille':
        if case['caller']!='DeplaceEngin+0xac':raise AssertionError('No declared stack contract for caller')
        # DeplaceEngin pushes this unit's route pointer and two literal zero
        # flags; these caller inputs are published by solucionador_vivo.py.
        stack=[m.u32(m.u32(0x4e1924)+4*(r['EBX']&65535)),0,0]
        return [r['EAX'],r['EDX'],r['EBX'],r['ECX'],*stack]
    if name in ('GetFreeCell','EnginSetPlayer','GetRandCaseTypeBatPlayer','Chemin_Accessible',
                'SetDeplaceEngin','ResetEnginCollision','EnginPeutPasser','CalculDirection',
                'CalculDirCase','TerrainEnCollision','ResetCollision'):return [r['EAX'],r['EDX']]
    return [r['EAX']]


class MovementProviders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for p,h in PINS.items():
            if hashlib.sha256(pinned_file(ROOT/p).read_bytes()).hexdigest()!=h:raise AssertionError(f'Reference identity changed: {p}')
        cls.abi=Frames();fn=cls.abi.lib.rl_executar_rotina_quadro
        fn.argtypes=[C.c_uint64,C.c_uint32,C.POINTER(C.c_uint32),C.c_uint32,C.POINTER(C.c_uint32)];fn.restype=C.c_int32
        raw=json.loads((ROOT/M1).read_bytes())['oracle']['final_state']['blocks']
        cls.baseline={int(b['base'],16):zlib.decompress(base64.b64decode(b['zlib_base64'])) for b in raw.values()}
        # Keep only world/navigation blocks; omitted media assets are not read.
        whole=Memory(sorted(cls.baseline.items()))
        needed={0x494000,whole.u32(0x4e19a0),whole.u32(0x4e19b8),whole.u32(0x4e1924)}
        for a in (0x507d70,0x507d74,0x507da8,0x507dac,0x4e0f38,0x4e156c,0x4e24b4,0x507db0,
                  0x507d5c,0x507d60,0x507d64):needed.add(whole.u32(a))
        for table in (0x507d78,0x507d88,0x507d98):
            needed.update(whole.u32(table+4*j) for j in range(4))
        rt=whole.u32(0x4e1924);needed.update(whole.u32(rt+4*j) for j in range(800))
        bt=whole.u32(0x4e19b8);needed.update(whole.u32(bt+4*j) for j in range(4))
        cls.world_blocks=sorted((a,b) for a,b in cls.baseline.items() if a in needed)
        cls.raid_frames={f['counter']:bytes.fromhex(f['raid_unit']) for f in json.loads((ROOT/MOVEMENT).read_bytes())['frames']}

    def rust(self,name,m,args):
        handle=self.abi.create()
        try:
            self.abi.load(handle,list(m.export().items()));argv=(C.c_uint32*len(args))(*args);out=C.c_uint32()
            self.abi.check(self.abi.lib.rl_executar_rotina_quadro(handle,IDS[name],argv,len(args),C.byref(out)))
            return self.abi.snapshot(handle),out.value
        finally:self.abi.free(handle)

    def fixture(self,case):
        known={int(a,16):v for a,v,_ in case['read_before_write']}
        for a,old,new in case['changed_bytes']:known[int(a,16)]=old
        blocks=list(self.world_blocks)
        # Capture scenarios have different allocation identities. Their exact read
        # bytes live in explicit synthetic-zero pages outside the v1 fixture.
        bases=[a for a,_ in blocks]
        def declared(address):
            i=bisect.bisect_right(bases,address)-1
            return i>=0 and address<bases[i]+len(blocks[i][1])
        pages={a&~4095 for a in known if not declared(a)}
        ranges=[]
        for p in sorted(pages):
            if ranges and ranges[-1][0]+len(ranges[-1][1])==p:ranges[-1][1].extend(bytes(4096))
            else:ranges.append((p,bytearray(4096)))
        m=Memory(sorted(blocks+ranges))
        counter=case.get('counter')
        if counter is not None and counter-1 in self.raid_frames:
            m.vista(m.u32(0x4e19a0)+16*276,276)[:]=self.raid_frames[counter-1]
        if case['routine'] in ('TestLigneOptimise','OptimiseChemin'):
            # Published first-search scenario: the raid unit is index16. Some
            # early-rejected native line probes never reread this global.
            m.u16(0x496304,16)
        for a,v in known.items():m.u8(a,v)
        return m,known

    def test_native_raid_and_movement_calls(self):
        checked={};sources=(RAID,MOVEMENT)
        for source in sources:
            for original in json.loads((ROOT/source).read_bytes())['calls']:
                name=original['routine']
                if name not in IDS:continue
                # All first-search calls, plus first four occurrences/family.
                key=(source,name);n=checked.get(key,0)
                if n>=4 and not 9175<=original.get('counter',0)<=9180:continue
                case=expandir(original)
                with self.subTest(source=source,routine=name,counter=case.get('counter'),index=n):
                    m,known=self.fixture(case);regs={k:int(v,16) for k,v in case['entry_registers'].items()}
                    args=args_for(name,regs,m,case);actual,value=self.rust(name,m,args)
                    result=Memory(sorted(actual.items()))
                    for a,old,new in case['changed_bytes']:
                        address=int(a,16)
                        if 0x2000000<=address<0x2010000:continue
                        self.assertEqual(result.u8(address),new,(name,a,old))
                    changed={int(a,16):new for a,_,new in case['changed_bytes']}
                    for address,old in known.items():
                        if 0x2000000<=address<0x2010000:continue
                        self.assertEqual(result.u8(address),changed.get(address,old),(name,hex(address)))
                    if name in ('GetFreeCell','CreerEngin','GetRandCaseChamps','GetRandCaseTypeBatPlayer','ChercheIndiceEngin','CalculDirCase'):
                        self.assertEqual(value&65535,int(case['exit_registers']['EAX'],16)&65535)
                    if name in ('EnginTypeGetCapacite','EnginEnArret','EnginEstVivant','PlayerGetColor',
                                'CalculDirection','EnginPeutPasser','TerrainEnCollision','TestLigneOptimise',
                                'Chemin_Verouille','Chemin_Accessible'):
                        self.assertEqual(value&255,int(case['exit_registers']['EAX'],16)&255)
                    if name in ('SetDeplaceEngin','ResetOrdre','EnginGetCase','SetMiniMap'):
                        self.assertEqual(value,int(case['exit_registers']['EAX'],16))
                    checked[key]=n+1
        self.assertEqual(sum(checked.values()),155)

    def python_world(self,m):return mundo_vivo(m,SolucionadorCaminhosVivo(m))

    def test_perturbed_live_movement_and_grid_aliases(self):
        rng=random.Random(0x448f50)
        methods={'RotateEngin':'girar','SetDeplaceEngin':'definir_movimento',
                 'EnginNextCase':'escolher_direto','EnginNextCaseChemin':'escolher_da_rota',
                 'AvanceEngin':'avancar_passo','CalculNextCase':'calcular_proxima_celula','DeplaceEngin':'deslocar'}
        for trial in range(24):
            for name,method in methods.items():
                m=Memory(self.world_blocks);w=self.python_world(m);i=16;u=w.unidades;p=i*276
                # This is an explicit synthetic neutral unit over actual live grids.
                u[p:p+276]=bytes(276);u[p]=4;u[p+1]=0;u[p+2]=2;u[p+0x72]=1
                for off,v in ((8,0x3030),(0x7c,0x3030),(0x7e,0x2e2e),(4,4),(0xfa,1),(0x74,rng.randrange(100))):w.palavra(i,off,v)
                for off,v in ((0x90,rng.randrange(1,17)),(0x91,rng.randrange(1,17)),(0x93,rng.randrange(4)),(0x98,2),(0xa5,8),(0xa7,2),(0xa4,rng.randrange(256)),(0xa9,rng.randrange(256))):u[p+off]=v
                m.u16(0x496304,65535);m.u8(0x4e0f36,0)
                for y in range(0x2b,0x34):
                    for x in range(0x2b,0x34):
                        c=x+256*y;w.atributos[c]=0;w.regioes[c]=1;w.objetos[c]=0
                w.ocupar(i,0x3030,True)
                route=w.rotas[i];route[:]=bytes(512);struct.pack_into('<HH',route,0,1,0x2f2f)
                args=[i];extra=[]
                if name=='SetDeplaceEngin':args.append(0x2d2d);extra=[0x2d2d]
                if name=='AvanceEngin':args.append(0);u[p+0x90]=u[p+0x91]=3;w.palavra(i,0x7c,0x2f2f);u[p+0x97]=rng.randrange(32)
                if name=='EnginNextCaseChemin':u[p+0x88]=5
                if name=='DeplaceEngin':u[p+0x88]=rng.choice([0,1,2,5,6])
                initial=Memory(list(m.export().items()));getattr(w,method)(i,*extra)
                actual,_=self.rust(name,initial,args);self.assertEqual(actual,m.export(),(trial,name))

    def test_perturbed_path_search_scratch_and_routes(self):
        rng=random.Random(0x42f214)
        for trial in range(8):
            m=Memory(self.world_blocks);w=self.python_world(m);i=16;p=i*276;u=w.unidades
            u[p:p+276]=bytes(276);u[p]=4;u[p+1]=0;u[p+2]=2;u[p+0x72]=1
            for off,v in ((8,0x1818),(0x7c,0x1818),(0x7e,0x1010),(0xfa,1),(4,4)):w.palavra(i,off,v)
            for y in range(8,33):
                for x in range(8,33):
                    c=x+256*y;w.atributos[c]=0;w.regioes[c]=1;w.objetos[c]=0
            # Deterministic wall with a gap drives contour/optimization choices.
            for x in range(10,29):
                if x==11+trial:continue
                c=x+0x14*256;w.atributos[c]=1;w.regioes[c]=3
            w.ocupar(i,0x1818,True);m.u16(0x496304,i);m.u8(0x4e0f36,1);m.u8(0x4e0f37,0);m.u8(0x496302,0)
            for a,n in ((0x4e116a,512),(0x4e136a,512),(0x4e0f6a,510),(0x4e0f54,10),(0x4e0f5e,10)):
                m.vista(a,n)[:]=rng.randbytes(n)
            # Candidate counts are always initialized by CheminCalcul.
            m.u8(0x4e0f34,0);m.u8(0x4e0f35,0)
            initial=Memory(list(m.export().items()));w.solucionador.calcular(w)
            actual,_=self.rust('CheminCalcul',initial,[]);self.assertEqual(actual,m.export(),trial)
