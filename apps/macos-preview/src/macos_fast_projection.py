"""Persistent caller-owned ABI bulk buffer and bounded Graphics read views.

ABI 1.1 cannot filter on the Rust side. Only declared Graphics regions leave
this bulk buffer; the full state proof streams hashes without block copies.
Views are serial leases, valid until their slot is reused, never Rust pointers.
"""
import bisect
import ctypes as C
import hashlib
import struct
from macos_state_consumer import StateValidationError, _sha
from macos_m22_playback import MacOSPlaybackImage, WORDS

MAX_BULK = 64*1024*1024 + 8*65536 + 4


class MacOSBulkProjection:
    def __init__(self, abi, capacity):
        self.abi = abi
        self.buffer = bytearray(capacity)
        self.foreign = (C.c_uint8*capacity).from_buffer(self.buffer)
        self.entries = ()
        self.starts = ()
        self.view = memoryview(self.buffer)[:0]
        self.allocations = 1
        self.calls = 0
        self._plan = None

    def update(self, handle):
        required = C.c_uint32()
        fn = self.abi.lib.rl_projetar_tudo
        code = fn(handle,self.foreign,len(self.buffer),C.byref(required))
        self.calls += 1
        if code==6:
            if not len(self.buffer)<required.value<=MAX_BULK:
                raise StateValidationError('Invalid bulk projection growth')
            self.buffer = bytearray(required.value)
            self.foreign = (C.c_uint8*len(self.buffer)).from_buffer(self.buffer)
            self.allocations += 1
            code = fn(handle,self.foreign,len(self.buffer),C.byref(required))
            self.calls += 1
        self.abi.check(code)
        if not 4<=required.value<=len(self.buffer):
            raise StateValidationError('Invalid bulk projection size')
        self.view = memoryview(self.buffer)[:required.value]
        count, = struct.unpack_from('<I',self.view)
        if count>65536: raise StateValidationError('Bulk block limit exceeded')
        entries=[]
        offset,end,total=4,0,0
        for i in range(count):
            if offset+8>len(self.view): raise StateValidationError('Truncated bulk descriptor')
            base,size=struct.unpack_from('<II',self.view,offset)
            offset += 8
            if not size or base<end or base+size>2**32 or offset+size>len(self.view):
                raise StateValidationError('Invalid bulk extent/order')
            total += size
            if total>64*1024*1024: raise StateValidationError('Bulk byte limit exceeded')
            entries.append((base,size,offset))
            offset,end=offset+size,base+size
        if offset!=len(self.view): raise StateValidationError('Trailing bulk bytes')
        entries=tuple(entries)
        if entries!=self.entries:
            self.entries=entries
            self.starts=tuple(a for a,n,o in entries)
            self._plan=None
        return self

    def read(self,address,size):
        if type(address) is not int or type(size) is not int or size<=0:
            raise StateValidationError('Invalid live read range')
        index=bisect.bisect_right(self.starts,address)-1
        if index>=0:
            base,length,offset=self.entries[index]
            at=address-base
            if at+size<=length: return self.view[offset+at:offset+at+size].toreadonly()
        raise StateValidationError(f'Undeclared live range 0x{address:x}/{size}')

    ler_mundo=read
    def u8(self,a): return self.read(a,1)[0]
    def u16(self,a): return struct.unpack_from('<H',self.read(a,2))[0]
    def u32(self,a): return struct.unpack_from('<I',self.read(a,4))[0]

    def masked_summary(self,names,static,ranges):
        if self._plan is None:
            starts=[a for a,z in ranges]
            plan=[]
            for base,size,offset in sorted(self.entries,key=lambda e:names.get(e[0],f'rust_extra_{e[0]:08x}')):
                if base in static: continue
                chunks=[]
                cursor=base
                i=max(0,bisect.bisect_right(starts,base)-1)
                while i<len(ranges) and ranges[i][0]<base+size:
                    a,z=ranges[i];i+=1
                    lo,hi=max(base,a),min(base+size,z)
                    if lo>=hi:continue
                    if cursor<lo:chunks.append((offset+cursor-base,offset+lo-base,None))
                    chunks.append((0,0,bytes(hi-lo)))
                    cursor=hi
                if cursor<base+size:chunks.append((offset+cursor-base,offset+size,None))
                plan.append((struct.pack('<II',base,size),chunks))
            self._plan=plan
        h=hashlib.sha256()
        for header,chunks in self._plan:
            h.update(header)
            for a,z,zeros in chunks: h.update(self.view[a:z] if zeros is None else zeros)
        return h.hexdigest()


class MacOSGraphicsView:
    """A persistent, read-only caller lease over only Graphics-declared bytes."""
    def __init__(self, source_sha256):
        self.source_sha256=source_sha256
        self.regions=[]
        self.starts=[]
        self.allocations=0

    def capture(self,bulk,api,index,name,summary,checkpoint):
        declarations=sorted(api.regioes_necessarias(bulk,hud=True))
        signature=[(a,z,label) for a,z,label in declarations]
        if [(a,a+len(data),label) for a,data,label in self.regions]!=signature:
            self.regions=[(a,bytearray(z-a),label) for a,z,label in declarations]
            self.starts=[a for a,data,label in self.regions]
            self.allocations+=len(self.regions)
        # Preflight every source before changing this unpublished slot.
        sources=[bulk.read(a,len(data)) for a,data,label in self.regions]
        for (a,data,label),source in zip(self.regions,sources): data[:]=source
        self.phase_index,self.phase_name=index,name
        self.summary_sha256,self.checkpoint=summary,checkpoint
        return self

    def read(self,address,size):
        if type(address) is not int or type(size) is not int or size<=0:
            raise StateValidationError('Invalid Graphics read range')
        i=bisect.bisect_right(self.starts,address)-1
        if i>=0:
            base,data,label=self.regions[i]
            at=address-base
            if at+size<=len(data):return memoryview(data)[at:at+size].toreadonly()
        raise StateValidationError(f'Range outside declared Graphics view: 0x{address:x}/{size}')

    ler_mundo=read
    def u8(self,a):return self.read(a,1)[0]
    def u16(self,a):return struct.unpack_from('<H',self.read(a,2))[0]
    def u32(self,a):return struct.unpack_from('<I',self.read(a,4))[0]
    observed_words=MacOSPlaybackImage.observed_words
    @property
    def identity(self):return ('rising-lands/macos-live/2',self.source_sha256,self.phase_name,self.summary_sha256)

    def inspect(self):
        return dict(contract='rising-lands/macos-live/2',source_sha256=self.source_sha256,
                    phase=self.phase_name,phase_index=self.phase_index,
                    summary_sha256=self.summary_sha256,summary_scope='m22-masked-state',
                    checkpoint_verified=self.checkpoint,observed=self.observed_words(),
                    blocks=len(self.regions),bytes=sum(len(b) for a,b,n in self.regions),
                    memory=[dict(name=n,base=hex(a),bytes=len(b),sha256=_sha(b)) for a,b,n in self.regions],
                    memory_scope='Graphics declared regions; address reads use the complete current bulk snapshot')
