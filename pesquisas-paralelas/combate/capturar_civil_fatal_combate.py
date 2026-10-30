"""Original-only civil reaction and count-phase supplements on the real contact."""
import hashlib
import json
from pathlib import Path
import struct

from bancada_luta_fatal_combate import BancadaLutaFatal, estado_contato, json_bytes

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'evidencias/captura-civil-fatal-original-v1.json'


def main():
    if OUTPUT.exists(): raise SystemExit('Original supplement already exists')
    state,pin=estado_contato();b=BancadaLutaFatal(state);cases=[]
    def run(label,name,regs,writes=(),words=()):
        b.restore(state)
        for address,data in writes: b.cpu.mem_write(address,data)
        c,_,_=b.call(name,regs,words=words)
        c.update(case=label,state_ref='contact',declared_writes=[[hex(a),v.hex()] for a,v in writes]);cases.append(c)
    for kind in (0,5):
        for status in (5,7,18):
            for life in (100,1):
                run(f'civil-t{kind}-s{status}-life{life}','InfligeDegat',dict(EAX=0x2d05,EDX=1,EBX=16,ECX=0),
                    [(b.record(0)+1,bytes([kind])),(b.record(0)+2,bytes([status])),
                     (b.record(0)+0x9a,struct.pack('<H',life))],(0,))
    for u in (0,13):
        b.restore(state)
        run(f'refuge-u{u}','ChercheBatimentProximiteCaveOuSanctuaire',dict(EAX=b.u16(b.record(u)+8),EDX=0))
    inactive=[(b.record(u)+2,b'\0') for u in range(800)]
    run('recount-all-inactive','CalculEnginNextEtape',{},inactive)
    # Explicit marker variation exercises exclusion of corpses while the body advances.
    run('recount-corpse-only','CalculEnginNextEtape',{},inactive+[(b.record(0)+2,b'\4'),
        (b.record(0)+0xa4,b'\1'),(b.record(0)+0xc2,b'\0\0')])
    out=dict(schema='rising-lands/combat-fatal-civil-original/1',translation_executed=False,
             provenance=pin,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases)
    OUTPUT.write_text(json.dumps(out,indent=1,default=json_bytes)+'\n')
    print(json.dumps(dict(cases=len(cases),returns=sum(c['reached_return'] for c in cases),
                         faults=[(c['case'],c['fault']) for c in cases if c['fault']],limits=sum(c['limit'] for c in cases))))


if __name__=='__main__':main()
