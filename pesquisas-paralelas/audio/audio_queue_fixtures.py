"""Explicit synthetic memory/COM inputs for original-first Audio queue research.

These objects are fixtures, not initialized game state or DirectSound semantics.
No region, response or callback result is supplied when it was not declared.
"""
import base64
import copy
import hashlib
import struct
import zlib

GLOBAL_BASE, GLOBAL_SIZE=0x498f14,0x58
QUEUE_BASE, QUEUE_SIZE=0x521358,0xedc
EXTERNAL, EXTERNAL_SIZE=0x7000000,0x10000
COM_BASE, COM_SIZE=0x7100000,0x10000
COM_BUFFER=COM_BASE+0x1000
COM_DUPLICATE=COM_BASE+0x1100
COM_DEVICE=COM_BASE+0x1200
TABLE, STRIDE=0x52137c,44
INDEX=0x498f68
REFS=EXTERNAL+0x100
HEADER=EXTERNAL+0x2000
ENTRY1,ENTRY2=HEADER,HEADER+12
DATA1,DATA2=HEADER+24,HEADER+40
BANK_A,BANK_B,BANK_P=0x521fc8,0x521fe4,0x522000
ID1,ID2=0x12340001,0x12340002


def encode(data):return base64.b64encode(zlib.compress(bytes(data),9)).decode()
def decode(data):return zlib.decompress(base64.b64decode(data))


class QueueFixtureMemory:
    def __init__(self,regions):
        self.regions=regions
    def _view(self,address,size):
        for base,data in self.regions:
            if base<=address and address+size<=base+len(data):return data,address-base
        raise ValueError(f'Undeclared queue memory 0x{address:08x}+{size}')
    def view(self,address,size):
        data,offset=self._view(address,size);return memoryview(data)[offset:offset+size]
    def read(self,address,size):
        data,offset=self._view(address,size);return bytes(data[offset:offset+size])
    def write(self,address,data):
        target,offset=self._view(address,len(data));target[offset:offset+len(data)]=data
    def u8(self,address):return self.read(address,1)[0]
    def u16(self,address):return struct.unpack('<H',self.read(address,2))[0]
    def u32(self,address):return struct.unpack('<I',self.read(address,4))[0]
    def w8(self,address,value):self.write(address,bytes([value&255]))
    def w16(self,address,value):self.write(address,struct.pack('<H',value&65535))
    def w32(self,address,value):self.write(address,struct.pack('<I',value&0xffffffff))
    def snapshot(self):return [dict(base=hex(a),zlib_base64=encode(d),sha256=hashlib.sha256(d).hexdigest()) for a,d in self.regions]
    @classmethod
    def restore(cls,snapshot):return cls([(int(r['base'],16),bytearray(decode(r['zlib_base64']))) for r in snapshot])


def fixture_memory(original_globals):
    m=QueueFixtureMemory([(GLOBAL_BASE,bytearray(original_globals)),
       (QUEUE_BASE,bytearray((i*17+83)&255 for i in range(QUEUE_SIZE))),
       (EXTERNAL,bytearray((i*29+11)&255 for i in range(EXTERNAL_SIZE)))])
    for i in range(71):
        r=TABLE+i*STRIDE
        m.w8(r+8,0);m.w32(r+20,0);m.w32(r+32,0);m.w32(r+40,REFS+4*i)
        m.w32(REFS+4*i,i)
    for base in (0x52211c,0x52216c):
        for i in range(10):m.write(base+i*8,bytes(8))
    m.w32(INDEX,19);m.w32(0x498f60,-1);m.w32(0x498f64,-1)
    m.w32(0x521f84,0);m.w32(0x521f88,0);m.w32(0x521f90,0)
    m.w32(0x522228,COM_DEVICE);m.w32(0x5221bc,0)
    for bank in (BANK_A,BANK_B,BANK_P):
        m.write(bank,struct.pack('<IHHIIIII',1,2,0,0x1234,HEADER,0,0,4096))
    m.write(HEADER,struct.pack('<IHHI',ID1,100,1,24)+struct.pack('<IHHI',ID2,256,3,40))
    m.write(DATA1,struct.pack('<IIBBHBBH',0,64,1,16,22050,0,0,512))
    for i in range(3):m.write(DATA2+16*i,struct.pack('<IIBBHBBH',64*i,64,1,16,22050,4,200,512))
    m.w32(REFS+4*72,0xffffffff)
    return m


def record(m,index,*,state=2,sound_id=ID1,bank=BANK_A,slot=0,kind=0,flags=0,volume=256):
    r=TABLE+index*STRIDE
    for offset,value in ((0,sound_id),(4,bank),(12,flags),(16,volume),(20,1),(24,ENTRY1),(28,DATA1),(32,slot),(36,kind),(40,REFS+4*index)):
        m.w32(r+offset,value)
    m.w8(r+8,state);m.w32(REFS+4*index,index)
    return r


class ScriptedCOM:
    """One exact ordered answer list; no default success/status/position."""
    def __init__(self,responses):self.responses=copy.deepcopy(responses);self.calls=[]
    def answer(self,method,pointer,args):
        if not self.responses:raise ValueError('Undeclared DirectSound call: '+method)
        expected=self.responses.pop(0)
        if (method,pointer,list(args))!=(expected['method'],expected['object'],expected['args']):
            raise ValueError('DirectSound call differs from declared sequence: '+repr((method,pointer,args)))
        result=copy.deepcopy(expected);self.calls.append(result);return result
