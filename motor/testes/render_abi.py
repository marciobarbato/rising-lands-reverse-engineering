"""Copied ABI 1.3 render buffers. Assets are original catalog inputs, never test outputs."""
import ctypes as C
from pathlib import Path
import sys
from frame_abi import Frames
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'pesquisas-paralelas/graficos-animacao'))
from graficos import Catalogo, ORDEM, RAIZ
from test_quadro_jogo import tabelas
from render_quadro import carregar_superficie_inicial,carregar_cache_inicial,EstadoCache
U8=C.c_uint8;U32=C.c_uint32;U64=C.c_uint64
class Bytes(C.Structure):
    _fields_=[('data',C.POINTER(U8)),('length',U32)]
class Cache(C.Structure):
    _fields_=[('keys',Bytes),('payloads',Bytes),('cursor',U32)]
class Result(C.Structure):
    _fields_=[('abi_status',C.c_int32),('disposition',U32),('generation',U64),('frame_counter',U32),('width',U32),('height',U32),('stride',U32),('required_pixels',U32),('required_palette',U32),('palette_generation',U64),('cache_generation',U64),('stop_address',U32),('stop_callee',U8*48),('stop_reason',U8*192)]
class Observation(C.Structure):
    _fields_=[('kind',U32),('address',U32),('name',U8*48),('count',U32),('args',C.c_int32*8),('before',U8*8),('after',U8*8)]
def blob(data):
    b=(U8*len(data)).from_buffer_copy(data)
    return b,Bytes(b,len(b))
def original_assets():
    c=Catalogo();return [c._ler('cd/INSTALHD/GRAPHICS/'+name) for name in ORDEM]+[c._ler('cd/INSTALHD/PLATGAME.PIE'),*tabelas()]
def initial(catalog=None):
    c=catalog or Catalogo()
    return carregar_superficie_inicial(RAIZ/'evidencias/superficie-inicial-m22-v2.json'),carregar_cache_inicial(RAIZ/'evidencias/cache-terreno-inicial-m22-v2.json',c)
class Render:
    def __init__(self,frames):
        self.f=frames;self.lib=frames.lib;L=self.lib
        L.rl_render_criar.argtypes=[U64,C.POINTER(Bytes),U32,C.POINTER(Bytes),C.POINTER(Cache),C.POINTER(U64)]
        L.rl_render_geracao.argtypes=[U64,C.POINTER(U64),C.POINTER(U32),C.POINTER(U32)]
        L.rl_render_quadro.argtypes=[U64,U64,U32,C.POINTER(U8),U32,C.POINTER(U8),U32,C.POINTER(Result)]
        L.rl_render_reset.argtypes=[U64,C.POINTER(Bytes),C.POINTER(Cache)]
        L.rl_render_liberar.argtypes=[U64]
        L.rl_render_observacoes.argtypes=[U64,C.POINTER(Observation),U32,C.POINTER(U32)]
        L.rl_render_cache.argtypes=[U64,C.POINTER(U8),U32,C.POINTER(U8),U32,C.POINTER(U32),C.POINTER(U32),C.POINTER(U32)]
        self.pixels=(U8*480000)();self.palette=(U8*768)()
    def create(self,world,surface,cache,assets=None):
        inputs=[blob(x) for x in (assets or original_assets())]
        array=(Bytes*9)(*[x[1] for x in inputs]);s,desc=blob(surface);k,kd=blob(cache.registros);p,pd=blob(cache.blocos_crus);ca=Cache(kd,pd,cache.proximo);out=U64()
        self.f.check(self.lib.rl_render_criar(world,array,9,C.byref(desc),C.byref(ca),C.byref(out)))
        return out.value
    def reset(self,handle,surface,cache):
        s,desc=blob(surface);k,kd=blob(cache.registros);p,pd=blob(cache.blocos_crus);ca=Cache(kd,pd,cache.proximo)
        self.f.check(self.lib.rl_render_reset(handle,C.byref(desc),C.byref(ca)))
    def generation(self,world):
        g=U64();p=U32();f=U32();self.f.check(self.lib.rl_render_geracao(world,C.byref(g),C.byref(p),C.byref(f)));return g.value,p.value,f.value
    def draw(self,handle,generation,hud=True):
        result=Result();self.f.check(self.lib.rl_render_quadro(handle,generation,int(hud),self.pixels,len(self.pixels),self.palette,len(self.palette),C.byref(result)));return result
    def cache(self,handle):
        k=(U8*1024)();p=(U8*270336)();kr=U32();pr=U32();cursor=U32();self.f.check(self.lib.rl_render_cache(handle,k,len(k),p,len(p),C.byref(kr),C.byref(pr),C.byref(cursor)));return EstadoCache(bytes(k),bytes(p),cursor.value)
    def observations(self,handle):
        count=U32();code=self.lib.rl_render_observacoes(handle,None,0,C.byref(count))
        if code not in (0,6):self.f.check(code)
        data=(Observation*count.value)();self.f.check(self.lib.rl_render_observacoes(handle,data,len(data),C.byref(count)));return list(data)
    def free(self,handle):self.f.check(self.lib.rl_render_liberar(handle))
