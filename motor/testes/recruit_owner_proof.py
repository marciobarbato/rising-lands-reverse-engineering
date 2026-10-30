"""Reexecute Core's frozen 277 original recruitment entries against native Rust.

The original-only runner supplies each actual entry image to the Rust fixture
transport instead of its Python comparator. Every mapped byte and all eight
exit GPRs are checked; each native case must reproduce the committed capture.
"""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain9')
import argparse,hashlib,io,json,lzma,signal,subprocess,time
from pathlib import Path
from pinned_reference import activate,provenance
SOURCE=activate()
from chain_leaf_proof import REGS,word,blob,readword,readblob
from chain_full_leaf_proof import merge
from player_provenance import begin,finish
import validar_recrutamento_core as original
import bancada_s1 as bs

def prove(binary):
 start=time.monotonic();identity=begin(binary)
 # Snapshots are local, replay-verified by BancadaS1 against the immutable
 # original trajectory. Only the intact executable host path is rebound.
 link=SOURCE/'.local/m3';target=Path(os.environ.get('RL_S1_SNAPSHOTS','/Users/marcio/git/Rising Lands/worktrees/re-core/.local/m3'))
 if not link.exists():link.symlink_to(target,target_is_directory=True)
 from ambiente_ia_runtime import EXE
 bs.EXE=Path(EXE)
 raw=(SOURCE/'evidencias/recrutamento-core/original.json.xz').read_bytes();capture=json.loads(lzma.decompress(raw));rows=[]
 def compare(c,blocks):
  memory=merge(blocks);expected={a:bytearray(b)for a,b in memory.items()}
  for address,old,new in c['changed_bytes']:
   address=int(address,16);base=next(a for a,b in expected.items()if a<=address<a+len(b))
   if expected[base][address-base]!=old:raise ValueError('Original change does not match entry byte')
   expected[base][address-base]=new
  payload=word(1)+blob(c['routine'].encode())+b''.join(word(int(c['entry_registers'][k],16)if k!='ESP'else int(c['esp'],16))for k in REGS)+word(len(memory))+b''.join(word(a)+blob(b)for a,b in memory.items())
  run=subprocess.run([str(Path(binary).resolve())],input=payload,capture_output=True,check=True,timeout=20);f=io.BytesIO(run.stdout);code=readword(f);error=readblob(f).decode();regs={k:readword(f)for k in REGS};actual={}
  for _ in range(readword(f)):a=readword(f);actual[a]=readblob(f)
  if f.read():raise ValueError('Trailing fixture output')
  rd={k:[hex(regs[k]),c['exit_registers'][k]]for k in REGS if regs[k]!=int(c['exit_registers'][k],16)}
  bd=[hex(a)for a in expected.keys()|actual.keys()if expected.get(a)!=actual.get(a)]
  ref=capture['cases'][len(rows)]
  row=dict(routine=c['routine'],kind=c['kind'],label=c.get('label'),frame=c.get('frame'),equal=not(code or rd or bd)and c==ref,error=error,register_differences=rd,differing_blocks=bd[:5],whole_memory_equal=not bd,native_equals_capture=c==ref,compared_bytes=sum(map(len,memory.values())))
  rows.append(row)
  if len(rows)%25==0:print(len(rows),'recruitment entries;',sum(not r['equal']for r in rows),'differences',flush=True)
  return row
 original.comparar=compare
 replay=original.executar(traduzir=True)
 if len(rows)!=len(capture['cases']):raise ValueError('Frozen original case count differs')
 return dict(schema='rising-lands/rust-recruitment-owner-proof/1',cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,reference=provenance(),capture_sha256=hashlib.sha256(raw).hexdigest(),original_sha256=replay['original_sha256'],by_routine=replay['by_routine'],s1=replay['s1'],provenance=finish(identity,binary),scope='Original replay-checked SortieTroupe calls plus declared leaf variants. Every mapped byte and all seven data GPRs/ESP; no register masks, callbacks, skips or synthetic memory. Stack writes are outside original changed-byte policy.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/chain_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=prove(a.binary)
 with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
