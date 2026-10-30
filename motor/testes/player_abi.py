"""Copied declared-input ABI 1.5; schema answers, never game-state edits."""
import ctypes as C
import struct
from frame_abi import Frames,FrameInput

class Message(C.Structure):
 _fields_=[('message',C.c_uint32),('wparam',C.c_uint32),('lparam',C.c_uint32)]
class Key(C.Structure):
 _fields_=[('vk',C.c_uint32),('value',C.c_int32)]
class Declared(C.Structure):
 _fields_=[('size',C.c_uint32),('flags',C.c_uint32),('cursor_x',C.c_int32),('cursor_y',C.c_int32),('messages',C.POINTER(Message)),('message_count',C.c_uint32),('keys',C.POINTER(Key)),('key_count',C.c_uint32)]
class Event(C.Structure):
 _fields_=[('kind',C.c_uint32),('phase',C.c_uint32),('site',C.c_uint32),('frame',C.c_uint32),('values',C.c_uint32*12)]
class Player(Frames):
 def __init__(self,path=None):
  super().__init__(path);self.lib.rl_passo_quadro_entrada.argtypes=[C.c_uint64,C.c_uint32,C.POINTER(FrameInput),C.POINTER(Declared)];self.lib.rl_passo_quadro_entrada.restype=C.c_int32
  self.lib.rl_eventos_entrada.argtypes=[C.c_uint64,C.POINTER(Event),C.c_uint32,C.POINTER(C.c_uint32)];self.lib.rl_eventos_entrada.restype=C.c_int32
 def input(self,h,phase,inp,cursor=None,messages=(),keys=None,text_boundary=True,sound_boundary=True):
  messages=(Message*len(messages))(*(Message(*(v&0xffffffff for v in row)) for row in messages));keys=keys or {};ks=(Key*len(keys))(*(Key(k,v) for k,v in keys.items()))
  d=Declared(C.sizeof(Declared),int(cursor is not None)|int(text_boundary)*2|int(sound_boundary)*4,*(cursor or (0,0)),messages,len(messages),ks,len(ks))
  return self.lib.rl_passo_quadro_entrada(h,phase,C.byref(inp),C.byref(d))
 def consumed(self,h):
  n=C.c_uint32();code=self.lib.rl_eventos_entrada(h,None,0,C.byref(n));assert code in(0,6),code
  out=(Event*n.value)();self.check(self.lib.rl_eventos_entrada(h,out,len(out),C.byref(n)));return list(out)

def inputs(events):
 out=[]
 for e in events:
  v=e.values;r=dict(frame=e.frame,kind={1:'peek_message',2:'get_message',3:'translate_message',4:'dispatch_message',5:'cursor',6:'key'}.get(e.kind),site=hex(e.site))
  if e.kind==1:r['message']=list(v[1:4]) if v[0] else None
  elif e.kind==2:r['message']=list(v[:3])
  elif e.kind==3:r['result']=v[0]
  elif e.kind==4:r.update(message=list(v[:3]),wndproc='0x4181a1',wndproc_flags_after=struct.pack('<III',*v[4:7])[:11].hex())
  elif e.kind==5:r.update(x=v[0],y=v[1])
  elif e.kind==6:r.update(vk=v[0],value=C.c_int32(v[1]).value)
  else:continue
  out.append(r)
 return out

def orders(events):
 out=[]
 for e in events:
  v=e.values
  if e.kind==7:out.append(dict(frame=e.frame,site=hex(e.site),player=v[0],tag=v[1],word2=v[2],word4=v[3],word6=v[4],word8=v[5]))
  elif e.kind==8:out.append(dict(frame=e.frame,event='ProcessInputGame',player=v[0],tag=v[1],packet=struct.pack('<III',*v[2:5])[:10].hex(),jump_target=hex(v[5])))
 return out
