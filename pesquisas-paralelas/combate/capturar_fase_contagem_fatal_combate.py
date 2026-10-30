"""Native late-in-phase death followed by the next count rebuild.

The original 800-slot unit loop executes every body. Declared one-life victim
and high-life raider variations keep the duel bounded; no position/occupancy
is changed and no game callback is substituted.
"""
import hashlib
import json
from pathlib import Path
import struct

from bancada_luta_fatal_combate import BancadaLutaFatal, estado_contato, json_bytes

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'evidencias/captura-fase-contagem-fatal-original-v1.json'


def main():
    if OUTPUT.exists(): raise SystemExit('Original phase capture already exists')
    state,pin=estado_contato();b=BancadaLutaFatal(state);cases=[];events=[]
    for kind in (0,5):
        b.restore(state);parent='contact';died=False
        for tick in range(1,65):
            writes=[(0x508f7c,struct.pack('<I',10683+tick))]
            if tick==1:
                writes += [(b.record(0)+1,bytes([kind])),(b.record(0)+0x9a,b'\1\0'),
                           (b.record(16)+0x9a,b'\xff\xff')]
                if kind==5: writes.append((b.record(0)+2,b'\7'))
            for a,data in writes:b.cpu.mem_write(a,data)
            before_state=b.read(b.record(0)+2,1)[0]
            c,_,_=b.call('CalculEnginNextEtape',{})
            label=f'late-death-type{kind}-t{tick}'
            c.update(case=label,state_ref=parent,declared_writes=[[hex(a),v.hex()] for a,v in writes])
            cases.append(c);parent=label
            after_state=b.read(b.record(0)+2,1)[0]
            event=dict(case=label,state_before=before_state,state_after=after_state,
                       local_population=b.u16(0x4e1a3a),local_military=b.u16(0x4e1928),
                       type_count=b.u16(0x4e1a3c+2*kind))
            events.append(event)
            if not c['reached_return']:break
            if died:break
            if after_state==4:died=True
    out=dict(schema='rising-lands/combat-fatal-count-phase-original/1',translation_executed=False,
             provenance=pin,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,events=events)
    OUTPUT.write_text(json.dumps(out,indent=1,default=json_bytes)+'\n')
    print(json.dumps(dict(cases=len(cases),faults=[(c['case'],c['fault']) for c in cases if not c['reached_return']],
                         transitions=[e for e in events if e['state_before']!=e['state_after']],last=events[-1])),flush=True)


if __name__=='__main__':main()
