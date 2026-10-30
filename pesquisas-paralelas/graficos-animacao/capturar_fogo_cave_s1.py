"""Prepared original CAVE fire/technology cases at the actual S1 frame12500 entry.

The historical full AffGame surface/raster sequence is first reproduced unchanged
for every case. Only the second original call receives the explicitly recorded
damage, clock or research-level input writes. AffText executes in that second call.
These are prepared display cases, not additional natural S1 trajectory frames.
"""
import argparse,base64,json,lzma,struct,zlib
from pathlib import Path
import capturar_affgame_glifos as native

cases=[]; observations=[];Base=native.original.CapturadorSondasGraficos


class CapturaFogoCaveS1(Base):
    def __init__(self,b):
        super().__init__(b);self.prepared=None;self.flame=None
        self.hooks.append(b.cpu.hook_add(native.original.unicorn.UC_HOOK_CODE,self.fire_entry,begin=0x40323c,end=0x40323c))
        self.hooks.append(b.cpu.hook_add(native.original.unicorn.UC_HOOK_CODE,self.fire_end,begin=0x40d602,end=0x40d602))
    def entry(self,c,a,n,user):
        self.prepared=None
        if self.b.sym['AffText'] not in self.b.pulos:
            self.prepared=dict(cases[len(observations)]);self.prepared['flames']=[]
            for write in self.prepared['declared_writes']:c.mem_write(int(write['address'],16),bytes.fromhex(write['bytes']))
        super().entry(c,a,n,user)
    def fire_entry(self,c,a,n,user):
        if self.current is None or self.prepared is None:return
        r=lambda name:c.reg_read(getattr(native.original.x86,'UC_X86_REG_'+name))&0xffffffff
        self.flame=dict(registers={name:r(name) for name in ('EAX','EDX','EBX','ECX')},
            clock=int.from_bytes(c.mem_read(0x508f80,4),'little'),start=len(self.current['blits']))
    def fire_end(self,c,a,n,user):
        if self.flame is None:return
        self.flame['blits']=self.current['blits'][self.flame.pop('start'):]
        self.prepared['flames'].append(self.flame);self.flame=None
    def end(self,c,a,n,user):
        if self.current is not None and self.prepared is not None:
            audit={}
            for name,(address,key) in self.current['entry'].items():
                if name in ('dgroup','minimap','saved_background'):continue
                before=zlib.decompress(base64.b64decode(self.blobs[key]))
                audit[name]=native.sha(c.mem_read(int(address,16),len(before)))==key
            assert all(audit.values());self.prepared['world_unchanged']=audit
            observations.append(self.prepared)
        super().end(c,a,n,user)


def main(a):
    global cases
    cave=0x49a0c8+276
    # Full 0..100 damage domain, all32 fire phases at maximum intensity, all
    # eight visible technology levels. Exact writes remain in every result row.
    cases=[dict(case=f'damage-{damage}',declared_writes=[dict(address=hex(cave+6),bytes=struct.pack('<H',damage).hex())]) for damage in range(101)]
    cases += [dict(case=f'clock-{clock}',declared_writes=[dict(address=hex(cave+6),bytes='6400'),
        dict(address='0x508f80',bytes=struct.pack('<I',clock).hex())]) for clock in range(32)]
    cases += [dict(case=f'level-{level}',declared_writes=[dict(address='0x4dfb30',bytes=bytes([level]).hex())]) for level in range(8)]
    native.original.CapturadorSondasGraficos=CapturaFogoCaveS1
    a.capture=['s1-render-12221-12500.json.xz:12500-12500']*len(cases)
    native.main(a)
    p=Path(a.output);d=json.loads(lzma.decompress(p.read_bytes()))
    assert len(d['rows'])==len(observations)==141
    for row,case in zip(d['rows'],observations):row.update(case)
    d['prepared_fire_observer']=dict(method=__doc__,source_sha256=native.sha(Path(__file__).read_bytes()))
    p.write_bytes(lzma.compress(json.dumps(d).encode(),preset=3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',required=True);p.add_argument('--output',required=True);main(p.parse_args())
