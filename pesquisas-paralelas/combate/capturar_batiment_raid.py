"""Supplemental original-only solid sanctuary footprint and projectile-global captures.

The sanctuary origin +2 is not a collision cell. Select an actual building-0
cell from the original region grid, without changing that grid or geometry.
"""
import hashlib
import json
from pathlib import Path
import struct
from bancada_combate_raid import checkpoints, BancadaCombateRaid, DEPENDENCIES

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'evidencias/captura-batiment-raid-original-v3.json'


def execute(sound=False):
    global OUTPUT
    if sound:
        OUTPUT=HERE/'evidencias/captura-batiment-raid-original-v4-som.json'
    boundaries=dict(DEPENDENCIES)
    if sound:
        boundaries.pop(0x48aa79)
    if OUTPUT.exists():raise SystemExit(f'Refusing to overwrite {OUTPUT}')
    states, provenance=checkpoints()
    bench=BancadaCombateRaid(states[9000][0]);cases=[]
    def call(label,routine,regs,words=(),writes=(),stops=None):
        for address,data in writes:bench.cpu.mem_write(address,data)
        row,_,_=bench.call(routine,regs,words=words,stops=boundaries if stops is None else stops)
        row.update(case=label,checkpoint=frame,declared_writes=[[hex(a),d.hex()] for a,d in writes])
        cases.append(row)
        print(json.dumps(dict(case=label,returned=row['reached_return'],stop=row['stop'],fault=row['fault'])),flush=True)
    for frame,(state,_) in states.items():
        bench.restore(state)
        grid=bench.u32(0x4e0f38)
        cell=next(c for c in range(65536) if bench.u16(grid+2*c)&0xffe0==0x8000)
        maximum=bench.u16(0x495d90+52*bench.read(0x49a0d0,1)[0])
        life=bench.u16(0x49a0d2)
        for source in (0,1,2,16):
            for camera in (0,1):
                bench.restore(state)
                call(f'f{frame}-solid-impact-source{source}-camera{camera}','InfligeDegat',
                     dict(EAX=cell,EDX=1,EBX=source,ECX=0),(0,),((0x508041,bytes([camera])),))
        for direction in (29,30):
            bench.restore(state)
            call(f'f{frame}-solid-impact-mode4-dir{direction}','InfligeDegat',
                 dict(EAX=cell,EDX=4,EBX=16,ECX=direction),(0,),((0x508041,b'\x01'),))
        for damage in (life-1,life,life+1,maximum-1,maximum,maximum+1):
            bench.restore(state)
            call(f'f{frame}-solid-threshold-{damage}','BatimentInfligeDegat',
                 dict(EAX=0,EDX=damage,EBX=4),writes=((0x508041,b'\x01'),))
        # Native initialization followed by a declared arrival-ready frame and
        # remaining-line word. The original reaches its own first impact; the
        # stop is an internal checkpoint, not a substituted callee.
        bench.restore(state)
        pool=bench.u32(0x5080f0)
        free=next(i for i in range(100) if bench.read(pool+56*i+2,1)==b'\0')
        raid_cell=bench.u16(bench.record(16)+0x7c)
        call(f'f{frame}-type30-init','ProjectileInit',dict(EAX=30,EDX=raid_cell,EBX=raid_cell,ECX=4),
             (0,0,0,0,0))
        record=pool+56*free
        stops=dict(boundaries);stops[0x450874]='InfligeDegat checkpoint'
        call(f'f{frame}-type30-first-impact','ProjectileAvance',dict(EAX=record),
             writes=((record+0x18,b'\x0c'),(record+0x34,b'\0\0')),stops=stops)
    result=dict(schema='rising-lands/combat-real-raid-original/1',translation_executed=False,
                original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                provenance=provenance,cases=cases,
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                               (Path(__file__),HERE/'bancada_combate_raid.py')})
    with OUTPUT.open('x') as f:json.dump(result,f,indent=1);f.write('\n')
    print(json.dumps(dict(cases=len(cases),returns=sum(c['reached_return'] for c in cases),
                         faults=sum(bool(c['fault']) for c in cases),limits=sum(c['limit'] for c in cases))),flush=True)


if __name__=='__main__':
    execute()
    execute(sound=True)
