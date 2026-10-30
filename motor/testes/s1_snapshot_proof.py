"""Fresh original leaf comparisons on replay-checked S1 snapshots, with explicit register variants.

These are new snapshot leaf cases, not replay claims for the historical in-situ corpus.
"""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain8')
import argparse,hashlib,io,json,lzma,signal,subprocess,time,struct
from pathlib import Path
from chain_leaf_proof import SOURCE,REGS,word,blob,readword,readblob
from chain_full_leaf_proof import merge
from pinned_reference import activate
from player_provenance import begin,finish
import bancada_s1 as bs

def prove(window,binary):
 start=time.monotonic();identity=begin(binary);p=SOURCE/'.local/m3';target=Path(os.environ.get('RL_S1_SNAPSHOTS','/Users/marcio/git/Rising Lands/worktrees/re-core/.local/m3'))
 if not p.exists():p.symlink_to(target,target_is_directory=True)
 from ambiente_ia_runtime import EXE
 bs.EXE=Path(EXE) # Host path to exactly the intact oracle; no executable bytes changed.
 frame={'a':2250,'b':3250,'c':12000}[window];bench=bs.BancadaS1(frame);b=bench.b;opening=bs.imagem(b);context=b.cpu.context_save();path=SOURCE/f'evidencias/lacunas-s1/captura-{window}.json.xz';raw=path.read_bytes();cap=json.loads(lzma.decompress(raw));cases=[];seen=set();rows=[];skips=[]
 for c in cap['cases']:
  key=(c['routine'],tuple(c['entry_registers'][k]for k in REGS if k!='ESP'))
  if key in seen:continue
  seen.add(key);cases.append(c)
 for old in cases:
  if old['routine']=='VoixOffAsk':skips.append(dict(routine=old['routine'],reason='Original-declared sound body requires observed-request fixture transport'));continue
  bs.restaurar(b,opening);b.cpu.context_restore(context);regs={k:int(old['entry_registers'][k],16)for k in REGS if k!='ESP'}
  writes=[(0x496304,struct.pack('<H',13))] if old['routine']in ('IsDirectlyBlocking','IsIndirectlyBlocking') else []
  c,before=bs.folha(b,old['routine'],regs,(),writes,old['label']+' / snapshot-leaf variant',frame)
  memory=merge(before);expected=dict(memory)
  for a,previous,value in c['changed_bytes']:
   a=int(a,16);base=next(base for base,data in expected.items()if base<=a<base+len(data));data=bytearray(expected[base]);data[a-base]=value;expected[base]=bytes(data)
  payload=word(1)+blob(c['routine'].encode())+b''.join(word(int(c['entry_registers'][k],16)if k!='ESP'else int(c['esp'],16))for k in REGS)+word(len(memory))+b''.join(word(a)+blob(data)for a,data in memory.items())
  run=subprocess.run([str(Path(binary).resolve())],input=payload,capture_output=True,check=True,timeout=20);f=io.BytesIO(run.stdout);code=readword(f);error=readblob(f).decode();out={k:readword(f)for k in REGS};actual={}
  for _ in range(readword(f)):a=readword(f);actual[a]=readblob(f)
  rd={k:[hex(out[k]),c['exit_registers'][k]]for k in REGS if out[k]!=int(c['exit_registers'][k],16)};bd=[hex(a)for a in actual.keys()|expected.keys()if actual.get(a)!=expected.get(a)]
  rows.append(dict(routine=c['routine'],label=old['label'],frame=frame,equal=not(code or rd or bd),error=error,register_differences=rd,whole_game_memory_equal=not bd,differing_blocks=bd[:5],native_changed=len(c['changed_bytes']),declared_writes=c['writes']))
  if len(rows)%25==0:print(window,len(rows),'checked',sum(not r['equal']for r in rows),'differences',flush=True)
 bs.restaurar(b,opening);b.cpu.context_restore(context);bench.conferir()
 return dict(schema='rising-lands/rust-s1-snapshot-leaves/1',window=window,cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,skips=skips,snapshot=bench.reproducao(),original_sha256=hashlib.sha256(bs.EXE.read_bytes()).hexdigest(),variant_parameters_sha256=hashlib.sha256(raw).hexdigest(),provenance=finish(identity,binary),scope='Original S1 snapshot plus declared register tuples from historical captures; blocking variants explicitly set search owner to live unit13. Fresh intact-x86 calls. Game bytes and eight registers compared; stack is residue input, original callee stack writes excluded.',harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--window',choices=['a','b','c'],required=True);ap.add_argument('--binary',default='motor/target/release/chain_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=prove(a.window,a.binary)
 with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('window','cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
