"""Prepared 2/3/5-live-raider display cases from native S1 frame12500.

Explicitly copy the original soldier16 record into unused slots18 onward and
update only the monster counter. These are display fixtures, not allocations or
additional S1 simulation frames. Every original world block must remain unchanged
after the prepared AffGame call.
"""
import argparse,base64,json,lzma,zlib
from pathlib import Path
import capturar_affgame_glifos as native

cases=[];Base=native.original.CapturadorSondasGraficos


class CapturaRaideMultiS1(Base):
    def entry(self,c,a,n,user):
        self.case=None
        if self.b.sym['AffText'] not in self.b.pulos:
            extra=(1,2,4)[len(cases)];pool=int.from_bytes(c.mem_read(0x4e19a0,4),'little')
            record=bytes(c.mem_read(pool+16*276,276));writes=[]
            for i in range(extra):
                address=pool+(18+i)*276
                assert not bytes(c.mem_read(address+2,1))[0]
                c.mem_write(address,record);writes.append(dict(address=hex(address),bytes=record.hex()))
            c.mem_write(0x50b178,bytes([1+extra]));writes.append(dict(address='0x50b178',bytes=bytes([1+extra]).hex()))
            self.case=dict(case=f'prepared-{1+extra}-live-raiders',declared_writes=writes)
        super().entry(c,a,n,user)
    def end(self,c,a,n,user):
        if self.current is not None and self.case is not None:
            audit={}
            for name,(address,key) in self.current['entry'].items():
                if name in ('dgroup','minimap','saved_background'):continue
                before=zlib.decompress(base64.b64decode(self.blobs[key]))
                audit[name]=native.sha(c.mem_read(int(address,16),len(before)))==key
            assert all(audit.values());self.case['world_unchanged']=audit;cases.append(self.case)
        super().end(c,a,n,user)


def main(a):
    native.original.CapturadorSondasGraficos=CapturaRaideMultiS1
    a.capture=['s1-render-12221-12500.json.xz:12500-12500']*3
    native.main(a);p=Path(a.output);d=json.loads(lzma.decompress(p.read_bytes()))
    assert len(d['rows'])==len(cases)==3
    for row,case in zip(d['rows'],cases):row.update(case)
    d['multi_raid_observer']=dict(method=__doc__,source_sha256=native.sha(Path(__file__).read_bytes()))
    p.write_bytes(lzma.compress(json.dumps(d).encode(),preset=3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',required=True);p.add_argument('--output',required=True);main(p.parse_args())
