"""No-input Rust ABI 1.1 session, chained from accepted display S0.

Only initialization reads captured inputs. Later expected states are comparison
oracles, never loaded into the engine. One worker serializes lifetime and calls.
"""
import ctypes as C
import bisect
import hashlib
import json
from pathlib import Path
import struct
import time
from macos_rust_abi import Frames, FrameInput, FrameRegisters
from macos_fast_projection import MacOSBulkProjection, MacOSGraphicsView
from macos_m22_playback import MacOSM22Playback, MacOSPlaybackImage, CHECKPOINTS, PHASES
from macos_state_consumer import MacOSMemoryBlock, StateValidationError, EXECUTABLE_SHA256, _sha

POLICY = 'pesquisas-paralelas/missoes/validacao/m2-2-politica-comparacao-128-quadros.json'
POLICY_SHA = 'bf36e6e8f6a38202fa3248256d3de9f768497caa835a563a3ef119be994127f0'
FIRST = 'pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-exibicao-v2.json'
FIRST_SHA = 'd800be5aee2cda363b6fca08fd162e5f7a1a61e849c1384e29fefe9e031e1d1d'
STATIC_TABLES = ((0x45ed20,160),(0x454344,104),(0x4543c8,100),(0x426880,84))


def original_tables(executable, state):
    """Read only the four published immutable PE tables, checking overlaps."""
    raw = Path(executable).read_bytes()
    if _sha(raw) != EXECUTABLE_SHA256:
        raise StateValidationError('Original executable hash mismatch')
    pe, = struct.unpack_from('<I', raw, 0x3c)
    count, = struct.unpack_from('<H', raw, pe+6)
    optional, = struct.unpack_from('<H', raw, pe+20)
    base, = struct.unpack_from('<I', raw, pe+24+28)
    sections = [struct.unpack_from('<IIII', raw, pe+24+optional+i*40+8) for i in range(count)]
    tables = {}
    for address, size in STATIC_TABLES:
        offset = next((ptr+address-base-va for vs,va,rs,ptr in sections
                       if va <= address-base and address-base+size <= va+rs), None)
        if offset is None: raise StateValidationError('Missing original static table')
        data = raw[offset:offset+size]
        start, pending = address, bytearray()
        for i, byte in enumerate(data):
            at = address+i
            captured = next((b[at-a] for a,b in state.values() if a <= at < a+len(b)), None)
            if captured is not None:
                if captured != byte: raise StateValidationError('Static/captured table disagreement')
                if pending: tables[start] = bytes(pending); pending.clear()
            else:
                if not pending: start = at
                pending.append(byte)
        if pending: tables[start] = bytes(pending)
    return tables


def masked_summary(state, ranges):
    h = hashlib.sha256()
    starts = [a for a,z in ranges]
    for name in sorted(state):
        base, data = state[name]
        h.update(struct.pack('<II',base,len(data)))
        cursor=0
        i=max(0,bisect.bisect_right(starts,base)-1)
        while i<len(ranges) and ranges[i][0]<base+len(data):
            a,z=ranges[i];i+=1
            lo,hi=max(a,base)-base,min(z,base+len(data))-base
            if lo>=hi:continue
            if cursor<lo:h.update(data[cursor:lo])
            h.update(bytes(hi-lo));cursor=hi
        if cursor<len(data):h.update(data[cursor:])
    return h.hexdigest()


class MacOSLiveSession:
    def __init__(self, root, library, executable, renderer=None, playback=None):
        self.root = Path(root)
        self.oracle = playback or MacOSM22Playback.open(root)
        self.renderer = renderer
        self.abi = Frames(library)
        self.library_sha256 = _sha(Path(library).read_bytes())
        for path, pin in ((POLICY,POLICY_SHA),(FIRST,FIRST_SHA)):
            if _sha((self.root/path).read_bytes()) != pin:
                raise StateValidationError('Unpinned live input: '+path)
        policy = json.loads((self.root/POLICY).read_bytes())
        self.ranges = sorted((int(a,16),int(z,16)) for a,z in policy['cumulative']['exclusion_mask'])
        first = json.loads((self.root/FIRST).read_bytes())
        self.phase1_registers = {k:int(v,16) for k,v in first['phases'][0]['entry']['registers'].items()}
        self.phase2_registers = {k:int(v,16) for k,v in first['phases'][1]['entry']['registers'].items()}
        self.offscreen = int(next(s for s in first['phases'][0]['display_state']['surfaces'] if s['role']=='offscreen')['pixels'],16)
        self.s0 = {n:v for n,v in self.oracle._s0.items() if n != 'native_stack'}
        self.names = {a:n for n,(a,b) in self.s0.items()}
        self.static = original_tables(executable,self.s0)
        # Replay/hash expected states once at initialization, never in the live loop.
        # The accepted reader still checks every summary and full checkpoint.
        self.expected = tuple(masked_summary(state,self.ranges)
            for _,state,_ in self.oracle._reader.fases_referencia(self.oracle._capture,self.s0))
        self.handle = None
        self.reset()

    def close(self):
        if self.handle is not None:
            self.abi.free(self.handle); self.handle = None

    def reset(self):
        self.close()
        self.handle = self.abi.create(rate=20,epoch=0)
        try: self.abi.load(self.handle,sorted(list(self.s0.values())+list(self.static.items())))
        except Exception: self.close(); raise
        self.oracle.reset()
        capacity=4+sum(8+len(b) for a,b in list(self.s0.values())+list(self.static.items()))
        self.bulks=[MacOSBulkProjection(self.abi,capacity),MacOSBulkProjection(self.abi,capacity)]
        self.bulk=self.bulks[0]
        self.views=[MacOSGraphicsView(self.library_sha256),MacOSGraphicsView(self.library_sha256)]
        self.index = -1
        self.stop = None
        self.records = []
        self.current = self.oracle.current
        self.inputs = FrameInput(0,0,self.offscreen,FrameRegisters.from_values(self.phase1_registers),
                                 (C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
        if self.renderer: self.renderer.reset()
        return self.current

    def apply_frame(self):
        """Advance one published phase. A frame body follows its between phase.

        A failed ABI phase is atomic. A subsequent projection/render/verification
        failure latches a stop; the private world is never reused until reset.
        No orders are accepted by this interface.
        """
        if self.stop: return self.current
        index = self.index+1
        phase = 1 if index==0 else 2 if index%2 else 3
        number = (index+1)//2
        name = 'load_tail' if index==0 else ('between_frames' if number==1 else f'between_frames{number}') if phase==2 else f'frame{number}'
        previous = self.current
        if index==1: self.inputs.registers = FrameRegisters.from_values(self.phase2_registers)
        t0 = time.perf_counter()
        try:
            self.abi.frame(self.handle,phase,self.inputs)
            rust_seconds = time.perf_counter()-t0
            t1 = time.perf_counter()
            checkpoint=index<=256 and number in CHECKPOINTS and phase==3
            if self.renderer is not None:
                bulk=self.bulks[index%2].update(self.handle)
                if any(bulk.read(a,len(b))!=b for a,b in self.static.items()):
                    raise StateValidationError('Immutable static table changed')
                summary=bulk.masked_summary(self.names,self.static,self.ranges)
                equal=summary==self.expected[index] if index<=256 else None
                if equal is False:raise StateValidationError('Live masked state mismatch: '+name)
                image=self.views[index%2].capture(bulk,self.renderer.api,index,name,summary,checkpoint)
            else:
                # Explicit full immutable diagnostic path (no renderer); production
                # and the rendered equality proof both use the persistent path above.
                raw=self.abi.snapshot(self.handle)
                if any(raw.get(a)!=b for a,b in self.static.items()):
                    raise StateValidationError('Immutable static table changed')
                state={self.names.get(a,f'rust_extra_{a:08x}'):(a,b) for a,b in raw.items() if a not in self.static}
                summary=masked_summary(state,self.ranges)
                equal=summary==self.expected[index] if index<=256 else None
                if equal is False:raise StateValidationError('Live masked state mismatch: '+name)
                blocks=tuple(MacOSMemoryBlock(n,a,b,_sha(b)) for n,(a,b) in sorted(state.items(),key=lambda x:(x[1][0],x[0])))
                image=MacOSPlaybackImage('rising-lands/macos-live/1',self.library_sha256,blocks,index,name,summary,checkpoint)
            projection_seconds = time.perf_counter()-t1
            t2 = time.perf_counter()
            render = self.renderer.consume(image,previous if phase==2 else None) if self.renderer else None
            render_seconds = time.perf_counter()-t2
            events = [dict(kind=e.kind,id=e.id,site=hex(e.site),args=list(e.args),result=e.result) for e in self.abi.events(self.handle)]
            record = dict(phase=name,phase_index=index,masked_state_sha256=summary,state_equal=equal,
                          checkpoint=image.checkpoint,rust_seconds=rust_seconds,projection_seconds=projection_seconds,
                          render_seconds=render_seconds,projection_path='persistent-graphics-regions' if self.renderer else 'full-diagnostic',total_seconds=time.perf_counter()-t0,render=render,events=events)
            self.index,self.current = index,image
            if self.renderer is not None:self.bulk=bulk
            self.records.append(record)
            if render and (render.get('stop') or render.get('inherited_stop')):
                self.stop = dict(type='GraphicsDependencyStop',phase=name,detail=render.get('stop') or render.get('inherited_stop'))
        except Exception as exc:
            self.stop = dict(type=type(exc).__name__,phase=name,detail=str(exc))
        return self.current

    def read(self,address,size):
        if self.index>=0 and self.renderer is not None:return self.bulk.read(address,size)
        return self.current.read(address,size)

    def inspect(self):
        result = self.current.inspect()
        result.update(mode='live-rust-no-input',scenario='MONDE01 · Rust ao vivo · sem ordens',
                      summary_verified=self.index>=0 and self.index<=256,
                      verified_phases=sum(r['state_equal'] is True for r in self.records),
                      verified_checkpoints=sum(r['checkpoint'] for r in self.records),
                      live_stop=self.stop,input_policy='record-only',phases=list(PHASES)+( [] if self.index<=256 else [self.current.phase_name]))
        if self.renderer: result['render'] = self.renderer.present(raw=True)
        return result
