"""Prepared original animated message marker: every phase at native S1 frame11754.

Only the explicit queue marker byte and live drawing clock are changed for the
second call. The original historical baseline is reproduced first, unchanged.
Both real text calls execute in each prepared full AffGame call.
"""
import argparse,json,lzma,struct
from pathlib import Path
import capturar_affgame_glifos as native

prepared=[];Base=native.original.CapturadorSondasGraficos


class CapturaIconeAlertaS1(Base):
    def entry(self,c,a,n,user):
        if self.b.sym['AffText'] not in self.b.pulos:
            phase=len(prepared);index=int.from_bytes(c.mem_read(0x507d54,2),'little')
            address=0x4e7754+518*index+0x106
            writes=[dict(address=hex(address),bytes='01'),dict(address='0x508f80',bytes=struct.pack('<I',phase).hex())]
            for write in writes:c.mem_write(int(write['address'],16),bytes.fromhex(write['bytes']))
            prepared.append(dict(case=f'message-marker-phase-{phase}',declared_writes=writes))
        super().entry(c,a,n,user)


def main(a):
    native.original.CapturadorSondasGraficos=CapturaIconeAlertaS1
    a.capture=['s1-render-11751-11900.json.xz:11754-11754']*32
    native.main(a);p=Path(a.output);d=json.loads(lzma.decompress(p.read_bytes()))
    assert len(d['rows'])==len(prepared)==32
    for row,case in zip(d['rows'],prepared):row.update(case)
    d['message_marker_observer']=dict(method=__doc__,source_sha256=native.sha(Path(__file__).read_bytes()))
    p.write_bytes(lzma.compress(json.dumps(d).encode(),preset=3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',required=True);p.add_argument('--output',required=True);main(p.parse_args())
