"""Bounded original-only fight inventory around raid target 0x2e03.

Declared unit-window experiment, not D1/CalculGame: move soldiers 0..2 by
native SetDeplaceEngin while the raid waits, then resume raid unit 16 and
issue native reciprocal attack orders on contact. No position, life, owner,
occupancy or damage byte is poked. Capture each combat leaf's first actual
entry by native isolation, restore the exact CPU/stack/world, and continue
original code. No game routine is replaced by Python.
"""
import base64
import hashlib
import json
from pathlib import Path
import signal
import struct
import time
import zlib

from bancada_combate_raid import BancadaCombateRaid, checkpoints
from delta_estado_missao import estado_completo, resumo

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'evidencias/captura-contato-alvo-incursao-original-v1.json'
TARGET=0x2e03
LEAVES=('CalculAttaqueEngin','InfligeDegat','EnginInfligeDegat','SetDyingEngin','RetireEngin','EnginSetLevelExperience')


def main():
    if OUTPUT.exists():raise SystemExit(f'Refusing to overwrite {OUTPUT}')
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('1100-second native window budget')))
    signal.alarm(1100)
    started=time.monotonic();states,pins=checkpoints((9000,))
    b=BancadaCombateRaid(states[9000][0]);x=b.x86
    leaves={b.symbols[n]:n for n in LEAVES};pending=set(leaves)
    records=[];seen={};orders=[];tick=0;phase='setup';tracking=False
    def observe(cpu,address,size,_):
        if tracking and address in b.names and b.names[address] not in seen:
            r=b.registers();seen[b.names[address]]=dict(counter=9000+tick,phase=phase,
              caller_return=hex(b.u32(r['ESP'])),registers={k:hex(r[k]) for k in ('EAX','EDX','EBX','ECX')})
    b.cpu.hook_add(b.unicorn.UC_HOOK_BLOCK,observe);b.cpu.ctl_flush_tb()
    def fast(name,args):
        nonlocal tracking
        regs=dict(EAX=0,EBX=0,ECX=0,EDX=0,ESI=0,EDI=0,EBP=0,ESP=b.stack+0x8000,EFLAGS=2)
        regs.update(args)
        for k,v in regs.items():b.cpu.reg_write(getattr(x,'UC_X86_REG_'+k),v&0xffffffff)
        b.cpu.mem_write(regs['ESP'],struct.pack('<I',b.return_address))
        address=b.symbols[name]
        while True:
            b.stops=set(pending);b.stopped=None;b.stores=[];b.entries=[];b.outside=[]
            b.active=True;tracking=True
            try:b.cpu.emu_start(address,b.return_address,timeout=5000000,count=2000000)
            finally:b.active=False;tracking=False
            r=b.registers()
            if r['EIP']==b.return_address:return
            if r['EIP'] not in pending:raise RuntimeError(f'Native window limit/fault at {r["EIP"]:#x}')
            entry=r['EIP'];routine=leaves[entry];pending.remove(entry)
            context=b.cpu.context_save();stack=b.read(b.stack,65536);before=b.snapshot()
            words=(b.u32(r['ESP']+4),) if routine=='InfligeDegat' else ()
            result,_,_=b.call(routine,{k:v for k,v in r.items() if k not in ('ESP','EIP')},words=words,stops={})
            result.update(counter=9000+tick,phase=phase,
                          actual_caller_return=hex(struct.unpack_from('<I',stack,r['ESP']-b.stack)[0]),
                          full_state_before=estado_completo(before))
            records.append(result)
            if not result['reached_return']:raise RuntimeError(f'Isolated {routine} did not return: {result["fault"]}')
            b.restore(before);b.cpu.mem_write(b.stack,stack);b.cpu.context_restore(context)
            address=entry
    def order(unit,mode,target):
        fast('SetAttaqueEngin',dict(EAX=unit,EDX=mode,EBX=target))
        orders.append(dict(counter=9000+tick,unit=unit,mode=mode,reference=target))
    def cells():return {str(u):dict(cell=hex(b.u16(b.record(u)+8)),state=b.read(b.record(u)+2,1)[0],life=b.u16(b.record(u)+0x9a)) for u in (0,1,2,16)}
    stop=None;contact=None;steps=[]
    try:
        for unit in (0,1,2):fast('SetDeplaceEngin',dict(EAX=unit,EDX=TARGET))
        phase='soldiers-to-target'
        for _ in range(750):
            tick+=1;b.cpu.mem_write(0x508f7c,struct.pack('<I',9000+tick))
            for unit in (0,1,2):fast('EnginNextEtape',dict(EAX=unit))
            if b.u16(b.record(0)+8)==TARGET and b.read(b.record(0)+2,1)[0]==7:break
        steps.append(dict(phase=phase,counter=9000+tick,units=cells()))
        phase='raid-to-contact';attacking=False;after_contact=0
        for _ in range(1400):
            tick+=1;b.cpu.mem_write(0x508f7c,struct.pack('<I',9000+tick))
            if not attacking:
                raid=b.u16(b.record(16)+8)
                distances={u:((raid&255)-(b.u16(b.record(u)+8)&255))**2+((raid>>8)-(b.u16(b.record(u)+8)>>8))**2 for u in (0,1,2)}
                target=min(distances,key=distances.get)
                if distances[target]<=4:
                    contact=dict(counter=9000+tick,units=cells(),distance2=distances[target])
                    order(16,1,target)
                    for unit in (0,1,2):order(unit,1,16)
                    attacking=True;phase='reciprocal-attack'
            for unit in (0,1,2,16):
                if b.read(b.record(unit)+2,1)[0]!=0:fast('EnginNextEtape',dict(EAX=unit))
            fast('ProjectileCalcul',{})
            if attacking:
                after_contact+=1
                if after_contact>=400:break
            if tick%200==0:print(json.dumps(dict(counter=9000+tick,phase=phase,units=cells())),flush=True)
        steps.append(dict(phase=phase,counter=9000+tick,units=cells()))
    except Exception as exc:
        stop=repr(exc)
    finally:
        signal.alarm(0)
        result=dict(schema='rising-lands/combat-raid-contact-inventory/1',translation_executed=False,
          original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
          provenance=pins,declared_driver=__doc__,target_cell=hex(TARGET),orders=orders,steps=steps,contact=contact,
          first_entries=seen,calls=records,never_reached=[leaves[a] for a in sorted(pending)],stop=stop,
          final_state_summary=resumo(b.snapshot()),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          code_sha256=hashlib.sha256(b.read(0x401000,0x92c00)).hexdigest(),seconds=round(time.monotonic()-started,3))
        with OUTPUT.open('x') as f:json.dump(result,f,indent=1);f.write('\n')
        print(json.dumps(dict(contact=contact,calls=[c['routine'] for c in records],never_reached=result['never_reached'],stop=stop,seconds=result['seconds'])),flush=True)
    return bool(stop)


if __name__=='__main__':raise SystemExit(main())
