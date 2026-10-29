"""Original RetireEngin from the exact captured post-kill state, with zero life."""
import hashlib
import json
from pathlib import Path
import struct

from bancada_combate_raid import checkpoints, BancadaCombateRaid
from delta_estado_missao import aplicar, resumo

HERE=Path(__file__).resolve().parent
INPUT=HERE/'evidencias/captura-combate-raid-original-v2.json'
OUTPUT=HERE/'evidencias/captura-remocao-pos-dano-raid-original-v5.json'


def main():
    if OUTPUT.exists():raise SystemExit(f'Refusing to overwrite {OUTPUT}')
    capture=json.loads(INPUT.read_bytes())
    states,provenance=checkpoints()
    bench=BancadaCombateRaid(states[9000][0]);cases=[]
    for frame,(state,_) in states.items():
        source=next(c for c in capture['cases'] if c['case']==f'f{frame}-camera1-lethal-hp1-16')
        bench.restore(state)
        for address,data in source['declared_writes']:
            bench.cpu.mem_write(int(address,16),bytes.fromhex(data))
        before=bench.snapshot()
        if resumo(before)!=source['state_before']:raise ValueError('Post-kill source entry mismatch')
        killed=aplicar(before,source['delta'],source['case'])
        if resumo(killed)!=source['state_after']:raise ValueError('Post-kill source delta mismatch')
        bench.restore(killed)
        if bench.u16(bench.record(16)+0x9a)!=0 or bench.read(bench.record(16)+2,1)!=b'\x04':
            raise ValueError('Original lethal source must have zero life and state 4')
        row,_,_=bench.call('RetireEngin',dict(EAX=16))
        row.update(case=f'f{frame}-retire-after-actual-damage',checkpoint=frame,
                   source_case=source['case'],declared_writes=[])
        cases.append(row)
    result=dict(schema='rising-lands/combat-post-damage-removal-original/1',translation_executed=False,
                original_sha256=capture['original_sha256'],provenance=provenance,
                source_capture=dict(path=str(INPUT.relative_to(HERE)),sha256=hashlib.sha256(INPUT.read_bytes()).hexdigest()),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases)
    with OUTPUT.open('x') as f:json.dump(result,f,indent=1);f.write('\n')
    print(json.dumps(dict(cases=len(cases),returns=sum(c['reached_return'] for c in cases),
                         faults=sum(bool(c['fault']) for c in cases),limits=sum(c['limit'] for c in cases))),flush=True)


if __name__=='__main__':main()
