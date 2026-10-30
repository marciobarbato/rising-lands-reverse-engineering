"""Original prepared farmer counterpart of S1's visible hunger-state19 body.

Change only the type byte of the actual hungry unit11 in frame12001; its original
normal eight-phase animation and empty bag are retained. This is a prepared display
case, not a recruitment or simulation result.
"""
import argparse,json,lzma
from pathlib import Path
import capturar_affgame_glifos as native

writes=[];Base=native.original.CapturadorSondasGraficos


class CapturaFomeFazendeiroS1(Base):
    def entry(self,c,a,n,user):
        if self.b.sym['AffText'] not in self.b.pulos:
            pool=int.from_bytes(c.mem_read(0x4e19a0,4),'little');address=pool+11*276+1
            assert bytes(c.mem_read(pool+11*276+2,1))==b'\x13'
            c.mem_write(address,b'\x05');writes.append(dict(address=hex(address),bytes='05'))
        super().entry(c,a,n,user)


def main(a):
    native.original.CapturadorSondasGraficos=CapturaFomeFazendeiroS1
    a.capture=['s1-render-12001-12220.json.xz:12001-12001'];native.main(a)
    p=Path(a.output);d=json.loads(lzma.decompress(p.read_bytes()));assert len(d['rows'])==len(writes)==1
    d['rows'][0].update(case='prepared-farmer-hunger19',declared_writes=writes)
    d['farmer_hunger_observer']=dict(method=__doc__,source_sha256=native.sha(Path(__file__).read_bytes()))
    p.write_bytes(lzma.compress(json.dumps(d).encode(),preset=3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',required=True);p.add_argument('--output',required=True);main(p.parse_args())
