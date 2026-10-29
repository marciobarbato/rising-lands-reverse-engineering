"""ctypes binding for the app-owned, allocation-free native byte codec v1."""
import ctypes as C
import os
from pathlib import Path


class Entry(C.Structure):
    _fields_=[('base',C.c_uint32),('length',C.c_uint32),('offset',C.c_uint32)]


class Span(C.Structure):
    _fields_=[('offset',C.c_uint32),('length',C.c_uint32),('zero',C.c_uint32)]


class ProjectionCodec:
    def __init__(self,path=None):
        self.path=Path(path or os.environ.get('RL_MACOS_PROJECTION_LIBRARY',Path(__file__).with_name('librising_macos_projection.dylib')))
        self.lib=C.CDLL(str(self.path.resolve()))
        u32=C.c_uint32;ptr=C.POINTER(C.c_uint8)
        self.lib.macos_projection_codec_version.argtypes=[]
        self.lib.macos_projection_codec_version.restype=u32
        if self.lib.macos_projection_codec_version()!=1:raise RuntimeError('macOS projection codec version mismatch')
        self.lib.macos_projection_validate.argtypes=[ptr,u32,C.POINTER(Entry),u32]
        self.lib.macos_projection_validate.restype=C.c_int32
        self.lib.macos_projection_sha256.argtypes=[ptr,u32,C.POINTER(Span),u32,ptr]
        self.lib.macos_projection_sha256.restype=C.c_int32
        self.digest=(C.c_uint8*32)()

    def validate(self,bulk):
        return self.lib.macos_projection_validate(bulk.foreign,len(bulk.view),bulk.native_entries,len(bulk.entries))==0

    def summary(self,bulk):
        code=self.lib.macos_projection_sha256(bulk.foreign,len(bulk.view),bulk.native_spans,len(bulk.native_spans),self.digest)
        if code:raise RuntimeError('macOS projection codec rejected hash spans')
        return bytes(self.digest).hex()
