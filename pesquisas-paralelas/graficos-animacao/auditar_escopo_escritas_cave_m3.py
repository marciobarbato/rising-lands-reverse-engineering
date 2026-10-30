"""Native scope audit: every observed display root must have returned before frame logic ends."""
import argparse,json,lzma
from pathlib import Path
import capturar_escritas_cave_m3 as base

AUDIT=[]
class EscopoAuditado(base.EscritasBatiments):
    def stop(self):
        if self.frame is not None:
            AUDIT.append(dict(frame=self.frame,phase=self.b.fase,remaining_roots=list(self.stack)))
            assert not self.stack,('Display root not returned before outside-reader observation',self.frame,self.stack)
        super().stop()

def main(a):
    base.EscritasBatiments=EscopoAuditado
    first=base.run(a);targets={int(x,16) for x in first['observation']['changing_bytes']};second=base.run(a,targets)
    assert first['checks']==second['checks'] and first['observation']==second['observation']
    result=dict(schema='rising-lands/cave-native-root-scope-audit/1',probe=a.probe,probe_ref=base.REF,
        source_sha256=base.sha(Path(__file__).read_bytes()),observer_source_sha256=base.sha(Path(base.__file__).read_bytes()),
        executable_sha256=__import__('emulador').HASH_ORIGINAL,snapshot_sha256=base.sha(Path(a.snapshot).read_bytes()),
        observed_frames=a.observe,scope_ends=AUDIT,passes=[first,second],passes_equal=True)
    Path(a.output).write_bytes(lzma.compress(json.dumps(result).encode()));print('native scope audit',len(AUDIT),'empty root stacks',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--probe',choices=('P3',),required=True);p.add_argument('--to',type=int,required=True)
    p.add_argument('--observe',type=lambda s:list(map(int,s.split(','))),required=True);p.add_argument('--output',required=True);main(p.parse_args())
