"""Bounded original S1 render windows with a passive world/DGROUP effect audit.

The unchanged S1 recorder still checks every full native frame state and both phase
surfaces against the published probe. This observer additionally hashes every captured
world block after AffGame and records every value-changing DGROUP byte. It never
changes native state or the Missions display-v2 text boundaries.
"""
import argparse, json, lzma
from pathlib import Path
import capturar_janelas_s1_graficos as windows

original=windows.original


class CapturaS1Tardia(original.CapturadorSondasGraficos):
    def end(self,c,a,n,user):
        if self.current is None:return
        row=self.current
        immutable={}
        for name,(base,key) in row['entry'].items():
            if name in ('dgroup','minimap','saved_background'):continue
            base=int(base,16)
            import base64,zlib
            before=zlib.decompress(base64.b64decode(self.blobs[key]))
            after=bytes(c.mem_read(base,len(before)))
            immutable[name]=dict(before=key,after=original.sha(after),equal=before==after)
        base,key=row['entry']['dgroup']
        import base64,zlib
        before=zlib.decompress(base64.b64decode(self.blobs[key]));after=self.read(0x494000,len(before))
        row['changing_dgroup_bytes']=[hex(0x494000+i) for i,(x,y) in enumerate(zip(before,after)) if x!=y]
        row['world_effect_audit']=immutable
        assert all(v['equal'] for v in immutable.values()),(row['frame'],'AffGame changed a world input',immutable)
        super().end(c,a,n,user)


def main(a):
    original.CapturadorSondasGraficos=CapturaS1Tardia
    windows.main(a)
    path=Path(a.output);d=json.loads(lzma.decompress(path.read_bytes()))
    d['world_audit_observer']=dict(method=__doc__,source_sha256=original.sha(Path(__file__).read_bytes()))
    path.write_bytes(lzma.compress(json.dumps(d).encode(),preset=3))
    manifest_path=Path(str(path)+'.manifest.json');manifest=json.loads(manifest_path.read_text())
    manifest.update(compressed_sha256=original.sha(path.read_bytes()),raw_sha256=original.sha(json.dumps(d).encode()),
        world_audit_observer=d['world_audit_observer'])
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--start',required=True);p.add_argument('--resume')
    p.add_argument('--ref',default=windows.S1_REF);p.add_argument('--to',type=int,required=True);p.add_argument('--output',required=True)
    main(p.parse_args())
