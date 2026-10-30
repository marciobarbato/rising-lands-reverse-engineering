"""Proof binding to the exact app-owned frame driver used by Swift/Metal."""
import ctypes as C
from pathlib import Path

FIELDS64=('world','generation','frames','surfaces_equal','phases_equal','checkpoints_equal','logic_ns','render_ns','proof_ns')
FIELDS32=('phase_index','disposition','stopped','stop_phase','counter')
class NativeStatus(C.Structure):
    _fields_=[(n,C.c_uint64) for n in FIELDS64]+[(n,C.c_uint32) for n in FIELDS32]+[('state_sha',C.c_uint8*32),('surface_sha',C.c_uint8*32),('message',C.c_char*512)]
OBSERVER=C.CFUNCTYPE(C.c_int32,C.c_void_p,C.c_uint64,C.c_uint32,C.c_uint32)
class InputMessage(C.Structure):
    _fields_=[('message',C.c_uint32),('wparam',C.c_uint32),('lparam',C.c_uint32)]
class InputKey(C.Structure):
    _fields_=[('vk',C.c_uint32),('value',C.c_int32)]
class DeclaredInput(C.Structure):
    _fields_=[('size',C.c_uint32),('flags',C.c_uint32),('cursor_x',C.c_int32),('cursor_y',C.c_int32),('messages',C.POINTER(InputMessage)),('message_count',C.c_uint32),('keys',C.POINTER(InputKey)),('key_count',C.c_uint32)]
    @classmethod
    def answers(cls,answers,phase):
        rows=answers['messages'] if phase==2 else []
        messages=(InputMessage*len(rows))(*(InputMessage(*row) for row in rows))
        keys=(InputKey*len(answers['keys']))(*(InputKey(k,v) for k,v in sorted(answers['keys'].items())))
        cursor=answers['cursor'] if phase==2 else None
        out=cls(C.sizeof(cls),6|int(cursor is not None),*(cursor or (0,0)),messages,len(messages),keys,len(keys))
        out._storage=(messages,keys)
        return out

class SoundEvent(C.Structure):
    _fields_=[(n,C.c_uint32) for n in ('kind','frame','phase','site','eax','edx','ebx','ecx','volume','has_volume')]

class NativeDriver:
    def __init__(self,driver_library,engine_library,inputs):
        self.lib=C.CDLL(str(Path(driver_library).resolve()))
        signatures={
            'macos_live_abi_version':([],C.c_uint32),'macos_live_status_size':([],C.c_uint32),
            'macos_live_create':([C.c_char_p,C.c_char_p,C.c_char_p,C.c_uint32],C.c_void_p),
            'macos_live_validation':([C.c_void_p,C.c_uint32],C.c_int32),
            'macos_live_audit_window':([C.c_void_p,C.c_uint32],None),
            'macos_live_human_phase':([C.c_void_p,C.c_uint32],C.c_int32),
            'macos_live_input_phase':([C.c_void_p,C.c_uint32,C.POINTER(DeclaredInput)],C.c_int32),
            'macos_live_frame_context':([C.c_void_p,C.POINTER(C.c_uint8),C.c_uint32],C.c_int32),
            'macos_live_event':([C.c_void_p]+[C.c_uint32]*2+[C.c_int32]*2+[C.c_uint32]*3,C.c_int32),
            'macos_live_advance':([C.c_void_p,OBSERVER,C.c_void_p],C.c_int32),
            'macos_live_status':([C.c_void_p,C.POINTER(NativeStatus)],None),
            'macos_live_renderer':([C.c_void_p],C.c_uint64),
            'macos_live_pixels':([C.c_void_p],C.POINTER(C.c_uint8)),
            'macos_live_palette':([C.c_void_p],C.POINTER(C.c_uint8)),
            'macos_live_free':([C.c_void_p],None),
        }
        for name,(args,result) in signatures.items():
            f=getattr(self.lib,name);f.argtypes=args;f.restype=result
        # Sound transport (play mode); older proof dylibs simply lack it.
        for name,(args,result) in {'macos_live_sound_capture':([C.c_void_p,C.c_uint32],C.c_int32),
                                   'macos_live_sound_events':([C.c_void_p,C.POINTER(SoundEvent),C.c_uint32],C.c_uint32),
                                   'macos_live_sound_dropped':([C.c_void_p],C.c_uint64)}.items():
            if hasattr(self.lib,name):f=getattr(self.lib,name);f.argtypes=args;f.restype=result
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
    def input_phase(self,phase,answers):
        declared=DeclaredInput.answers(answers,phase)
        return self.lib.macos_live_input_phase(self.handle,phase,C.byref(declared))
    def context(self):
        from macos_rust_abi import FrameInput
        raw=(C.c_uint8*C.sizeof(FrameInput))()
        if self.lib.macos_live_frame_context(self.handle,raw,len(raw)):raise RuntimeError('NativeFrameContextUnavailable')
        return FrameInput.from_buffer_copy(raw)
    def event(self,event):
        kind=event['kind']
        return self.lib.macos_live_event(self.handle,1 if kind=='mouse' else 2,event.get('msg',0),event.get('x',0),event.get('y',0),event.get('wParam',0),event.get('vkey',0),int(event.get('down',False)))
    def sound_events(self):
        out=[];buffer=(SoundEvent*1024)()
        while True:
            n=self.lib.macos_live_sound_events(self.handle,buffer,1024);out+=[SoundEvent.from_buffer_copy(buffer[i]) for i in range(n)]
            if n<1024:return out
    def pixels(self):return C.string_at(self.lib.macos_live_pixels(self.handle),480000)
    def palette(self):return C.string_at(self.lib.macos_live_palette(self.handle),768)
    def close(self):
        if self.handle:self.lib.macos_live_free(self.handle);self.handle=None
