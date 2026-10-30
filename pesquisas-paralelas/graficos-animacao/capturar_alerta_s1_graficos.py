"""Original full AffGame calls plus the alert's actual MouseSetZone leaf arguments.

Uses the glyph-enabled two-pass display replay unchanged. This passive observer
records zone geometry from the original, before any alert/zone translation.
"""
import argparse,json,lzma,struct
from pathlib import Path
import capturar_affgame_glifos as native

observations=[]
Base=native.original.CapturadorSondasGraficos


class CapturaAlertaS1(Base):
    def __init__(self,b):
        super().__init__(b)
        self.hooks.append(b.cpu.hook_add(native.original.unicorn.UC_HOOK_CODE,self.zone,begin=0x479c50,end=0x479c50))
        self.hooks.append(b.cpu.hook_add(native.original.unicorn.UC_HOOK_CODE,self.zone,begin=0x479c9e,end=0x479c9e))
    def zone(self,c,address,n,user):
        if self.current is None:return
        r=lambda name:c.reg_read(getattr(native.original.x86,'UC_X86_REG_'+name))&0xffffffff
        observations.append(dict(frame=self.phase_frame,address=hex(address),
            registers={name:r(name) for name in ('EAX','EDX','EBX','ECX')},
            stack=bytes(c.mem_read(r('ESP'),8)).hex()))


def main(a):
    native.original.CapturadorSondasGraficos=CapturaAlertaS1
    native.main(a)
    p=Path(a.output);d=json.loads(lzma.decompress(p.read_bytes()))
    d['alert_zone_observer']=dict(method=__doc__,source_sha256=native.sha(Path(__file__).read_bytes()),calls=observations)
    p.write_bytes(lzma.compress(json.dumps(d).encode(),preset=3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',required=True)
    p.add_argument('--capture',action='append',required=True);p.add_argument('--output',required=True);main(p.parse_args())
