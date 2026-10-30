"""Bounded fresh intact-original leaves on an attested S1 snapshot; explicit input variants only."""
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
 p=SOURCE/'.local/m3';target=Path(os.environ.get('RL_S1_SNAPSHOTS','/Users/marcio/git/Rising Lands/worktrees/re-core/.local/m3'))
 if not p.exists():p.symlink_to(target,target_is_directory=True)
 from ambiente_ia_runtime import EXE
 bs.EXE=Path(EXE);bench=bs.BancadaS1(8000);b=bench.b;opening=bs.imagem(b);context=b.cpu.context_save()
 def u16(a):return int.from_bytes(b.cpu.mem_read(a,2),'little')
 def u32(a):return int.from_bytes(b.cpu.mem_read(a,4),'little')
 pool=u32(0x4e19a0);objects=u32(0x507d74);cell=u16(pool+14*276+8);cases=[]
 for value in range(256):cases.append(('TerrainEstGc',dict(EAX=0xabcd0000|cell,EBX=0x12345678,ECX=0x87654321,EDX=0xabcdef01,ESI=0x11112222,EDI=0x33334444,EBP=0x55556666),[(objects+cell,bytes([value]))],f'object byte {value}'))
 for owner in (0,1,2,3,200):
  for mode in range(1,8):cases.append(('SetMiniMap',dict(EAX=owner,EBX=cell,ECX=0x87654321,EDX=mode,ESI=0x11112222,EDI=0x33334444,EBP=0x55556666),[],f'owner {owner}, mode {mode}'))
 for u in (11,12,13,14,15):
  r=pool+276*u;c=u16(r+8)
  for variant in ('actual','depleted','food_here'):
   writes=[]
   if variant!='actual':writes=[(0x508041,b'\x03'),(r+4,b'\x00\x00'),(r+2,b'\x05'),(r+0x74,b'\x01\x00')]
   if variant=='food_here':writes.append((objects+c,b'\x43'))
   cases.append(('EnginSetFatigue',dict(EAX=u,EBX=0x12345678,ECX=0x87654321,EDX=0xabcdef01,ESI=0x11112222,EDI=0x33334444,EBP=0x55556666),writes,f'unit {u}, {variant}'))
 rows=[];skips=[]
 for name,regs,writes,label in cases:
  bs.restaurar(b,opening);b.cpu.context_restore(context);c,before=bs.folha(b,name,regs,(),writes,label,8000)
  if c['boundaries']:
   skips.append(dict(routine=name,label=label,reason='Original-declared sound nonexecution requires observed-request fixture transport',boundaries=c['boundaries']));continue
  memory=merge(before);expected=dict(memory)
  for address,old,value in c['changed_bytes']:
   a=int(address,16);base=next(base for base,data in expected.items()if base<=a<base+len(data));data=bytearray(expected[base]);data[a-base]=value;expected[base]=bytes(data)
  typed=name+(':effects'if name in ('EnginSetFatigue','SetMiniMap')else'');payload=word(1)+blob(typed.encode())+b''.join(word(int(c['entry_registers'][k],16)if k!='ESP'else int(c['esp'],16))for k in REGS)+word(len(memory))+b''.join(word(a)+blob(data)for a,data in memory.items())
  run=subprocess.run([str(Path(binary).resolve())],input=payload,capture_output=True,check=True,timeout=20);f=io.BytesIO(run.stdout);code=readword(f);error=readblob(f).decode();actual_regs={k:readword(f)for k in REGS};actual={}
  for _ in range(readword(f)):a=readword(f);actual[a]=readblob(f)
  masks={k:0 if name=='EnginSetFatigue'and k=='EAX'or name=='SetMiniMap'and k in ('EAX','EBX','EDX')else 0xffffffff for k in REGS}
  rd={k:[hex(actual_regs[k]),c['exit_registers'][k]]for k in REGS if(actual_regs[k]^int(c['exit_registers'][k],16))&masks[k]};bd=[hex(a)for a in actual.keys()|expected.keys()if actual.get(a)!=expected.get(a)]
  rows.append(dict(routine=name,label=label,equal=not(code or rd or bd),error=error,register_differences=rd,register_masks=masks,whole_game_memory_equal=not bd,differing_blocks=bd[:10],native_changed=len(c['changed_bytes']),declared_writes=c['writes']))
  if len(rows)%50==0:print(len(rows),'checked',sum(not r['equal']for r in rows),'differences',flush=True)
 bs.restaurar(b,opening);b.cpu.context_restore(context);bench.conferir();original=hashlib.sha256(bs.EXE.read_bytes()).hexdigest()
 if original!='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb':raise ValueError('Intact oracle identity')
 return dict(schema='rising-lands/rust-fatigue-query-original/1',cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,skips=skips,snapshot=bench.reproducao(),original_sha256=original,provenance=finish(identity,binary),scope='Original S1 frame8000 plus explicitly listed input variants. No mission-flow claim for variants. Original game bytes and declared register widths compared; callee stack writes excluded.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/chain_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=prove(a.binary)
 with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
