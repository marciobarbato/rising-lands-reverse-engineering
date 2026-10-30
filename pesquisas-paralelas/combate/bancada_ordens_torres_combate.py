"""Original-first turret input leaves on pinned Missions M3 probe states.

No translated game code executes here. Full state is read with the existing
Missions delta decoder and AI compressed reader. All native hooks only record
or halt; the intact EXE remains executable and unmodified.
"""
import hashlib
import json
import struct
from pathlib import Path

from ambiente_combate_raid import ROOT
from bancada_combate_raid import BancadaCombateRaid
from delta_estado_missao import _decodificar, aplicar, resumo
from comparar_quadros_ia import carregar_captura

HERE=Path(__file__).resolve().parent
EVIDENCE=HERE/'evidencias/captura-ordens-torres-original-v1.json'
REGS=('EAX','EBX','ECX','EDX','ESI','EDI','EBP')
STRUCTURES=0x49a0c8
SELECTION=0x495be0


def carregar_estados_torres():
    """Real frame250/P1 and frame2020/P6 (sanctuary selected, cave constructed)."""
    from provar_entrada_janelas_ia import manifesto
    states={};pins=[]
    for name,frame,part_number in (('P1',250,0),('P6',2020,1)):
        manifest=manifesto(name)
        mp=manifest['parts'][part_number]
        path=ROOT/mp['artifact']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=mp['compressed_sha256']:
            raise ValueError('Compressed probe part hash mismatch')
        part,raw_hash=carregar_captura(path,mp['raw_sha256'])
        end=next(i for i,p in enumerate(part['phases']) if p['phase']==f'frame{frame}')
        full=[i for i,p in enumerate(part['phases'][:end+1]) if 'full_state' in p['state_after']]
        start=full[-1] if full else -1
        opened=part['opening_state'] if start<0 else part['phases'][start]['state_after']
        state={n:(int(b['base'],16),_decodificar(b)) for n,b in opened['full_state'].items()}
        if resumo(state)!=opened['summary']:raise ValueError('Probe full-state summary mismatch')
        for phase in part['phases'][start+1:end+1]:
            state=aplicar(state,phase['state_delta'],phase['phase'])
            if resumo(state)!=phase['state_after']['summary']:raise ValueError('Probe replay summary mismatch')
        key=f'{name}-frame{frame}'
        states[key]=state
        pins.append(dict(state=key,artifact=mp['artifact'],raw_sha256=raw_hash,
                         compressed_sha256=mp['compressed_sha256'],summary=resumo(state),
                         reconstructed_from=part['phases'][start]['phase'] if start>=0 else 'opening_state'))
    return states,pins


def casos_torres(b,key):
    """Declared leaf variations, not newly placed turrets or synthetic game flow."""
    out=[]
    def add(label,name,regs,writes=()):
        out.append(dict(case=key+'-'+label,state=key,routine=name,registers=regs,
                        writes=[[hex(a),bytes(d).hex()] for a,d in writes]))
    def byte(a,v):return (a,bytes([v]))
    def word(a,v):return (a,struct.pack('<H',v&65535))
    units=b.u32(0x4e19a0)
    for source in (0,1,999):
        add(f'actual-type-{source}','BatimentPeutAttaquer',dict(EAX=0xabcd0000|source,EDX=0x98760001,EBX=0x87650000))
    for kind in (10,11):
        base=[byte(STRUCTURES+8,kind)]
        for target in (0,1,2,12,15,799):
            add(f'type{kind}-unit{target}','BatimentPeutAttaquer',dict(EAX=0xabc00000,EDX=0x12340001,EBX=0x76540000|target),base)
        for target_kind in (16,17):
            add(f'type{kind}-flying{target_kind}','BatimentPeutAttaquer',dict(EAX=0,EDX=1,EBX=0),
                base+[byte(units+1,target_kind)])
        add(f'type{kind}-neutral-unit','BatimentPeutAttaquer',dict(EAX=0,EDX=1,EBX=0),base+[byte(units,200)])
        targets=(0,1) if key.startswith('P6') else (0,)
        for target in targets:
            add(f'type{kind}-building{target}','BatimentPeutAttaquer',dict(EAX=0,EDX=3,EBX=target),base)
        add(f'type{kind}-neutral-building','BatimentPeutAttaquer',dict(EAX=0,EDX=3,EBX=0),base+[byte(STRUCTURES+4,200)])
        for owner in (0,1,2,3,4,200):
            bonus=[] if owner>=4 else [byte(0x4dfba0+468*owner+18*11+6,255)]
            for mode,target in ((1,799),(3,0),(5,0xffff)):
                add(f'type{kind}-owner{owner}-mode{mode}-bonus255','BatimentPeutAttaquer',
                    dict(EAX=0,EDX=0xface0000|mode,EBX=0xdead0000|target),base+[byte(STRUCTURES+4,owner)]+bonus)
        # Inclusive range boundary at 7, outside 8; query-only target step-cell variation.
        cell=b.u16(STRUCTURES+2)
        for delta in (0,7,8,0x0700,0x0800,0xffff):
            add(f'type{kind}-range-{delta:x}','BatimentPeutAttaquer',dict(EAX=0,EDX=1,EBX=0),
                base+[word(units+0x7c,(cell+delta)&65535)])
    # P6 contains a genuine selected sanctuary. Other players/IDs/modes are
    # explicitly declared ABI/alias variations; this setter has no type gate.
    if key.startswith('P6'):
        for player,selected in ((0,0),(1,1),(2,999),(3,0)):
            for mode in (0,1,3,5,255):
                for target in (selected,0xffff):
                    add(f'set-p{player}-s{selected}-m{mode}-r{target}','BatimentInitAttaqueSelect',
                        dict(EAX=0xabcd0000|player,EDX=0x87654300|mode,EBX=0xfedc0000|target),
                        [word(SELECTION+2*player,selected)])
    return out


def capturar_torres():
    if EVIDENCE.exists():raise SystemExit(f'Refusing to overwrite {EVIDENCE}')
    states,pins=carregar_estados_torres()
    b=BancadaCombateRaid(next(iter(states.values())))
    results=[]
    for key,state in states.items():
        b.restore(state)
        cases=casos_torres(b,key)
        for case in cases:
            b.restore(state)
            for a,d in case['writes']:b.cpu.mem_write(int(a,16),bytes.fromhex(d))
            native,_,_=b.call(case['routine'],case['registers'],stops={},seconds=5)
            native.update(case=case['case'],state=key,declared_writes=case['writes'])
            results.append(native)
    from inventario_ia_runtime import OriginalImage
    image=OriginalImage()
    intervals=[('BatimentInitAttaqueSelect',0x4242cc,0x424314),
               ('BatimentPeutAttaquer',0x42436c,0x4245c6),('range-table',0x424314,0x42436c)]
    code={name:dict(start=hex(a),end=hex(z),sha256=hashlib.sha256(image.read(a,z)).hexdigest(),hex=image.read(a,z).hex())
          for name,a,z in intervals}
    report=dict(schema='rising-lands/combat-turret-orders-original/1',translation_executed=False,
                original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                state_provenance=pins,code=code,cases=results,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='Real M3 P1/P6 full memory; all type/owner/bonus/step-cell/selection variations declared. No physical turret placement claim.')
    with EVIDENCE.open('x') as f:json.dump(report,f,indent=1);f.write('\n')
    counts={name:sum(c['routine']==name for c in results) for name in ('BatimentPeutAttaquer','BatimentInitAttaqueSelect')}
    summary=dict(cases=counts,returns=sum(c['reached_return'] for c in results),faults=sum(bool(c['fault']) for c in results),
                 limits=sum(c['limit'] for c in results),outside_writes=sum(bool(c['writes_outside_checkpoint']) for c in results))
    print(json.dumps(summary),flush=True)
    if summary['faults'] or summary['limits'] or summary['outside_writes']:raise SystemExit(2)


if __name__=='__main__':capturar_torres()
