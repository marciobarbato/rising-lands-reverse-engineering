"""Renderer cache/effect exports used only by the original/Python proof oracle."""
import ctypes as C
class Observation(C.Structure):
    _fields_=[('kind',C.c_uint32),('address',C.c_uint32),('name',C.c_uint8*48),('count',C.c_uint32),('args',C.c_int32*8),('before',C.c_uint8*8),('after',C.c_uint8*8)]
class RenderDiagnostics:
    def __init__(self,frames):
        self.f=frames;self.lib=frames.lib
        self.lib.rl_render_cache.argtypes=[C.c_uint64,C.POINTER(C.c_uint8),C.c_uint32,C.POINTER(C.c_uint8),C.c_uint32,C.POINTER(C.c_uint32),C.POINTER(C.c_uint32),C.POINTER(C.c_uint32)]
        self.lib.rl_render_cache.restype=C.c_int32
        self.lib.rl_render_observacoes.argtypes=[C.c_uint64,C.POINTER(Observation),C.c_uint32,C.POINTER(C.c_uint32)]
        self.lib.rl_render_observacoes.restype=C.c_int32
        self.keys=(C.c_uint8*1024)();self.payloads=(C.c_uint8*270336)()
    def compare(self,renderer,python_result):
        kr,pr,cursor=C.c_uint32(),C.c_uint32(),C.c_uint32()
        self.f.check(self.lib.rl_render_cache(renderer,self.keys,len(self.keys),self.payloads,len(self.payloads),C.byref(kr),C.byref(pr),C.byref(cursor)))
        assert (bytes(self.keys),bytes(self.payloads),cursor.value)==(python_result.cache.registros,python_result.cache.blocos_crus,python_result.cache.proximo),'Native cache mismatch'
        count=C.c_uint32();code=self.lib.rl_render_observacoes(renderer,None,0,C.byref(count))
        if code not in (0,6):self.f.check(code)
        if count.value>65536:raise ValueError('Observation count outside proof bound')
        values=(Observation*count.value)()
        self.f.check(self.lib.rl_render_observacoes(renderer,values,len(values),C.byref(count)))
        effects=[(bytes(v.name).split(b'\0')[0].decode(),v.address,bytes(v.before[:v.count]).hex(),bytes(v.after[:v.count]).hex()) for v in values if v.kind==1]
        assert effects==list(python_result.efeitos),'Native ordered effects mismatch'
