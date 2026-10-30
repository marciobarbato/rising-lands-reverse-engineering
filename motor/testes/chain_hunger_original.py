"""Fresh intact-original hunger body variants on a replay-checked S1 world.

These explicit meal inputs cover refill/restoration, not an in-situ hunger-flow claim.
"""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain8')
import argparse,hashlib,io,json,signal,struct,subprocess,time
from pathlib import Path
from chain_leaf_proof import SOURCE,REGS,word,blob,readword,readblob
from chain_full_leaf_proof import merge
from player_provenance import begin,finish
import bancada_s1 as bs

def prove(binary):
 start=time.monotonic();identity=begin(binary)
 p=SOURCE/'.local/m3'
 if not p.exists():p.symlink_to(Path(os.environ.get('RL_S1_SNAPSHOTS','/Users/marcio/git/Rising Lands/worktrees/re-core/.local/m3')),target_is_directory=True)
 from ambiente_ia_runtime import EXE
 from oraculo_carga_missao import BancadaCargaMissaoOriginal
 from unicorn import x86_const as x86, UC_HOOK_CODE
 bs.EXE=Path(EXE);original=hashlib.sha256(bs.EXE.read_bytes()).hexdigest()
 if original!='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb':raise ValueError('Intact oracle identity')
 bench=bs.BancadaS1(8000);b=bench.b
 b.cpu.hook_add(UC_HOOK_CODE,b._parar_se_pedido,begin=0x454ccd,end=0x454ccd);b.cpu.ctl_flush_tb()
 opening=bs.imagem(b);context=b.cpu.context_save();rows=[]
 def read(a,n):return int.from_bytes(b.cpu.mem_read(a,n),'little')
 pool=read(0x4e19a0,4);objects=read(0x507d74,4);quantity=read(0x507dac,4);discovery=read(0x507d78+12,4)
 for u in (11,12,13,14,15):
  for saved in (2,5,17):
   for visibility in (0,1,16,31):
    bs.restaurar(b,opening);b.cpu.context_restore(context);r=pool+276*u;cell=read(r+8,2)
    writes=[(0x508041,b'\x03'),(r+2,b'\x13'),(r+0xa0,struct.pack('<H',saved)),(r+0xc2,b'\xff\xff'),(r+0x7e,struct.pack('<H',cell)),(r+0x86,b'\0\0'),(r+0x82,b'\0'),(objects+cell,b'\x43'),(quantity+cell,b'\x02'),(discovery+cell,bytes([visibility])),(r+0xf9,b'\x7f'),(r+0x104,b'\0\0\0\0')]
    for a,data in writes:b.cpu.mem_write(a,data)
    esp=b.cpu.reg_read(x86.UC_X86_REG_ESP)-0x100
    regs=dict(EAX=0xabcd0000,EBX=0x12345678,ECX=0x87654321,EDX=0xabcdef01,ESI=r,EDI=u,EBP=0x55556666,ESP=esp)
    for k,v in regs.items():b.cpu.reg_write(getattr(x86,'UC_X86_REG_'+k),v)
    before=bs.imagem(b);phase=b.fase;boundaries=len(b.eventos_fronteira);events=len(b.vinculos_declarados.eventos);b._retomando=set()
    try:out=BancadaCargaMissaoOriginal._correr(b,'leaf',0x4554db,{},(0x454ccd,),retomar=True)
    finally:b.fase=phase
    if out['EIP']!=0x454ccd or out['ESP']!=esp:raise ValueError(('Hunger body exit',out))
    if len(b.eventos_fronteira)!=boundaries or len(b.vinculos_declarados.eventos)!=events:raise ValueError('Unexpected boundary with an existing declared sound handle')
    after=bs.imagem(b);after['native_stack']=before['native_stack'];memory=merge(before);expected=merge(after)
    payload=word(1)+blob(b'EnginNextEtape:19:effects')+b''.join(word(regs[k])for k in REGS)+word(len(memory))+b''.join(word(a)+blob(data)for a,data in memory.items())
    run=subprocess.run([str(Path(binary).resolve())],input=payload,capture_output=True,check=True,timeout=20);f=io.BytesIO(run.stdout);code=readword(f);error=readblob(f).decode();actual_regs={k:readword(f)for k in REGS};actual={}
    for _ in range(readword(f)):a=readword(f);actual[a]=readblob(f)
    bd=[hex(a)for a in actual.keys()|expected.keys()if actual.get(a)!=expected.get(a)]
    rows.append(dict(unit=u,saved_state=saved,discovery_byte=visibility,equal=not(code or bd or actual_regs['ESP']!=out['ESP']),error=error,whole_game_memory_equal=not bd,differing_blocks=bd,register_masks={k:0xffffffff if k=='ESP'else 0 for k in REGS},declared_writes=[[hex(a),data.hex()]for a,data in writes]))
    print('unit',u,'saved',saved,'discovery',visibility,'equal',rows[-1]['equal'],error,flush=True)
 bs.restaurar(b,opening);b.cpu.context_restore(context);bench.conferir()
 return dict(schema='rising-lands/rust-hunger-body-original/1',cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,original_sha256=original,snapshot=bench.reproducao(),provenance=finish(identity,binary),harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Fresh original state19 body 0x4554db -> 0x454ccd, S1 frame8000 plus declared sack/arrival/saved-state/discovery inputs and existing sound handle. No mission-flow claim. All game bytes and ESP; scratch GPRs outside typed effects API; original callee stack writes excluded.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/chain_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=prove(a.binary)
 with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
