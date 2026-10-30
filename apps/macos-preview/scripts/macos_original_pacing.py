"""Read-only, reproducible static pacing audit of the intact PT-BR RISING.EXE.

Requires the repository's existing pefile/capstone dependencies. This records
original instructions; it never executes or normalizes the executable.
"""
import argparse
import hashlib
import json
from pathlib import Path
import capstone
import pefile

ORIGINAL='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
RANGES=[('WinMain',0x460170,0x460277),('game_iteration',0x47500e,0x47509d),
        ('CalculFrame',0x43f710,0x43f7af),('draw_divisor',0x4178f7,0x41793c),
        ('DDFlipPage',0x43f14f,0x43f31c),('GameNextFrame',0x45d015,0x45d01c),
        ('OpenFli_timer',0x45a692,0x45a6b1),('ReadFli_timer',0x45aac6,0x45aaeb),
        ('GetNextNbFrameEllapsedFli',0x45abb1,0x45abce),
        ('network_input_timer',0x45ea7c,0x45eabf),
        ('MCICD_deadline',0x467a34,0x467a4d),('MCICD_Manage_timer',0x467bf0,0x467c33),
        ('iaRandom_seed',0x489775,0x4897a4),
        ('CRT_semaphore',0x490d41,0x490d9e),('CRT_thread_join',0x4936a7,0x4936c9)]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    if a.output.exists() or a.output.with_suffix('.asm').exists():p.error('Refusing to overwrite evidence')
    raw=a.exe.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if digest!=ORIGINAL:raise ValueError('Intact original identity mismatch')
    pe=pefile.PE(data=raw);base=pe.OPTIONAL_HEADER.ImageBase;im=pe.get_memory_mapped_image()
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32);cs.detail=True;cs.skipdata=True
    imports={x.address:x.name.decode() for d in pe.DIRECTORY_ENTRY_IMPORT for x in d.imports if x.name}
    timed={addr:name for addr,name in imports.items() if any(t in name.lower() for t in ('time','tick','sleep','wait','timer'))}
    code=[i for s in pe.sections if s.Characteristics&0x20000000 for i in cs.disasm(s.get_data(),base+s.VirtualAddress) if i.id]
    indirect=[i for i in code if i.mnemonic in ('call','jmp') and any(o.type==capstone.x86.X86_OP_MEM and o.mem.disp in timed for o in i.operands)]
    thunks={i.address:timed[i.operands[0].mem.disp] for i in indirect if i.mnemonic=='jmp'}
    sites=[dict(address=f'0x{i.address:08x}',bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str,api=timed[i.operands[0].mem.disp]) for i in indirect]
    sites += [dict(address=f'0x{i.address:08x}',bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str,api=thunks[i.operands[0].imm]) for i in code if i.mnemonic in ('call','jmp') and i.operands[0].type==capstone.x86.X86_OP_IMM and i.operands[0].imm in thunks]
    # Byte-backed anchors distinguish a frequency display and a draw divisor
    # from an elapsed-time simulation gate.
    anchors={0x46020d:'e8fc4d0100',0x47505e:'e80578fbff',0x475063:'e83026faff',
             0x43f71a:'2eff15b8315200',0x43f730:'81fae8030000',
             0x45d015:'ff05406d4900',0x43f220:'6a10',0x43f244:'ff521c'}
    for addr,value in anchors.items():assert im[addr-base:addr-base+len(bytes.fromhex(value))].hex()==value,(hex(addr),value)
    lines=[f'; Intact original SHA-256 {digest}', '; Static evidence only; ranges end exclusively.']
    spans=[]
    for name,lo,hi in RANGES:
        data=im[lo-base:hi-base];spans.append(dict(name=name,start=hex(lo),end=hex(hi),sha256=hashlib.sha256(data).hexdigest()))
        lines.append(f'\n; {name} {lo:08x}..{hi:08x}')
        for i in cs.disasm(data,lo):
            api=''
            if i.id:
                for o in i.operands:
                    if o.type==capstone.x86.X86_OP_MEM and o.mem.disp in imports:api=' ; '+imports[o.mem.disp]
                    elif o.type==capstone.x86.X86_OP_IMM and o.imm in thunks:api=' ; '+thunks[o.imm]
            lines.append(f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}{api}')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.with_suffix('.asm').write_text('\n'.join(lines)+'\n')
    report=dict(schema='rising-lands/macos-original-pacing-static/1',original_path=str(a.exe.resolve()),original_sha256=digest,
                scope='Intact executable static instructions and all executable-section timer-import/thunk xrefs; not a wall-clock measurement',
                disassembler=capstone.__version__,pefile=pefile.__version__,ranges=spans,
                timer_imports={hex(k):v for k,v in timed.items()},timer_sites=sites,
                anchors={hex(k):v for k,v in anchors.items()},
                finding='Active idle loop advances one CalculGame per iteration, without a recovered fixed-Hz timer gate. GetTickCount counts display iterations per >=1000 ms; draw divisor does not divide logic.',
                presentation='DDFlipPage calls surface vtable +0x1c (BltFast), flags 0x10 (DDBLTFAST_WAIT), retrying still-drawing; no fixed-Hz or vertical-blank wait in this routine.',
                default_policy='Original active-loop policy: uncapped. Host 20/60 Hz remain explicit optional caps; virtual TickClock stays 20 to preserve audited states.',
                gaps=['No historical Windows/hardware wall-clock FPS measurement; CPU/driver/message/workload dependent.',
                      'No claim that native Apple Silicon throughput equals the wall-clock pace on a 1997 machine.',
                      'Static import scan cannot bound external DirectDraw/driver latency or runtime-loaded components.'])
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(report['finding'])


if __name__=='__main__':main()
