"""Prepared player-0 counterpart of the original S1 soldier's attack/normal display calls.

The original baseline remains the exact recorded S1 full surface. Only the second
call changes unit17's owner byte, explicitly, before executing the intact original.
No simulation step, unit allocation or text resource is fabricated.
"""
import argparse,json,lzma
from pathlib import Path
import capturar_affgame_glifos as native

prepared=[];Base=native.original.CapturadorSondasGraficos


class CapturaCorpoAliadoS1(Base):
    def entry(self,c,address,n,user):
        if self.b.sym['AffText'] not in self.b.pulos:
            pool=int.from_bytes(c.mem_read(0x4e19a0,4),'little');target=pool+17*276
            c.mem_write(target,b'\0');prepared.append([dict(address=hex(target),bytes='00')])
        super().entry(c,address,n,user)


def main(a):
    native.original.CapturadorSondasGraficos=CapturaCorpoAliadoS1
    a.capture=['s1-render-11751-11900.json.xz:11846-11846','s1-render-12001-12220.json.xz:12001-12001']
    native.main(a)
    p=Path(a.output);d=json.loads(lzma.decompress(p.read_bytes()))
    assert len(d['rows'])==len(prepared)==2
    for row,writes in zip(d['rows'],prepared):row.update(case='prepared-player0-soldier',declared_writes=writes)
    d['allied_body_observer']=dict(method=__doc__,source_sha256=native.sha(Path(__file__).read_bytes()))
    p.write_bytes(lzma.compress(json.dumps(d).encode(),preset=3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',required=True);p.add_argument('--output',required=True);main(p.parse_args())
