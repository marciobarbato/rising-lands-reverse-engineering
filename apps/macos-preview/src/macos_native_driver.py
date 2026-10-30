"""Proof binding to the exact app-owned frame driver used by Swift/Metal."""
import ctypes as C
from pathlib import Path

FIELDS64=('world','generation','frames','surfaces_equal','phases_equal','checkpoints_equal','logic_ns','render_ns','proof_ns')
FIELDS32=('phase_index','disposition','stopped','stop_phase','counter')
class NativeStatus(C.Structure):
    _fields_=[(n,C.c_uint64) for n in FIELDS64]+[(n,C.c_uint32) for n in FIELDS32]+[('state_sha',C.c_uint8*32),('surface_sha',C.c_uint8*32),('message',C.c_char*512)]
OBSERVER=C.CFUNCTYPE(C.c_int32,C.c_void_p,C.c_uint64,C.c_uint32,C.c_uint32)
class NativeDriver:
    def __init__(self,driver_library,engine_library,inputs):
        self.lib=C.CDLL(str(Path(driver_library).resolve()))
        signatures={
            'macos_live_abi_version':([],C.c_uint32),'macos_live_status_size':([],C.c_uint32),
            'macos_live_create':([C.c_char_p,C.c_char_p,C.c_char_p,C.c_uint32],C.c_void_p),
            'macos_live_audit_window':([C.c_void_p,C.c_uint32],None),
            'macos_live_advance':([C.c_void_p,OBSERVER,C.c_void_p],C.c_int32),
            'macos_live_status':([C.c_void_p,C.POINTER(NativeStatus)],None),
            'macos_live_renderer':([C.c_void_p],C.c_uint64),
            'macos_live_pixels':([C.c_void_p],C.POINTER(C.c_uint8)),
            'macos_live_palette':([C.c_void_p],C.POINTER(C.c_uint8)),
            'macos_live_free':([C.c_void_p],None),
        }
        for name,(args,result) in signatures.items():
            f=getattr(self.lib,name);f.argtypes=args;f.restype=result
        if self.lib.macos_live_abi_version()!=1 or self.lib.macos_live_status_size()!=C.sizeof(NativeStatus):
            raise RuntimeError('Native driver ABI/layout mismatch')
        error=C.create_string_buffer(512)
        self.handle=self.lib.macos_live_create(str(Path(engine_library).resolve()).encode(),str(Path(inputs).resolve()).encode(),error,len(error))
        if not self.handle:raise RuntimeError(error.value.decode())
    def status(self):
        out=NativeStatus();self.lib.macos_live_status(self.handle,C.byref(out));return out
    def advance(self,observer=None):
        callback=OBSERVER(observer) if observer else OBSERVER()
        return self.lib.macos_live_advance(self.handle,callback,None)
    def pixels(self):return C.string_at(self.lib.macos_live_pixels(self.handle),480000)
    def palette(self):return C.string_at(self.lib.macos_live_palette(self.handle),768)
    def close(self):
        if self.handle:self.lib.macos_live_free(self.handle);self.handle=None
