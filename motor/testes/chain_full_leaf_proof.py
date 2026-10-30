"""Original turret full-state corpus, reconstructed from pinned original checkpoints/deltas only."""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain8')
import argparse,hashlib,io,json,subprocess,time
from pathlib import Path
from chain_leaf_proof import SOURCE,REGS,word,blob,readword,readblob
from player_provenance import begin,finish
from bancada_ordens_torres_combate import carregar_estados_torres
from delta_estado_missao import aplicar,resumo
from validar_combate_raid import write_state

def merge(state):
 out=[]
 for a,b in sorted(state.values()):
  if out and out[-1][0]+len(out[-1][1])==a:out[-1][1].extend(b)
  else:out.append((a,bytearray(b)))
 return {a:bytes(b)for a,b in out}

def prove(binary):
 start=time.monotonic();identity=begin(binary);states,pins=carregar_estados_torres();path=SOURCE/'pesquisas-paralelas/combate/evidencias/captura-ordens-torres-original-v1.json';raw=path.read_bytes();capture=json.loads(raw)
 if capture['translation_executed']or capture['original_sha256']!='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'or pins!=capture['state_provenance']:raise ValueError('Original corpus identity')
 rows=[]
 for c in capture['cases']:
  before=write_state(states[c['state']],c['declared_writes']);after=aplicar(before,c['delta'],c['case'])
  if resumo(before)!=c['state_before']or resumo(after)!=c['state_after']:raise ValueError('Original delta/hash identity')
  memory=merge(before);expected=merge(after);payload=word(1)+blob(c['routine'].encode())+b''.join(word(int(c['entry_registers'][k],16))for k in REGS)+word(len(memory))
  payload+=b''.join(word(a)+blob(b)for a,b in memory.items());run=subprocess.run([str(Path(binary).resolve())],input=payload,capture_output=True,check=True,timeout=20);f=io.BytesIO(run.stdout);code=readword(f);error=readblob(f).decode();regs={k:readword(f)for k in REGS};actual={}
  for _ in range(readword(f)):a=readword(f);actual[a]=readblob(f)
  rd={k:[hex(regs[k]),c['exit_registers'][k]]for k in REGS if regs[k]!=int(c['exit_registers'][k],16)}
  dif=[hex(a)for a in actual.keys()|expected.keys()if actual.get(a)!=expected.get(a)]
  rows.append(dict(case=c['case'],routine=c['routine'],equal=not(code or rd or dif),error=error,register_differences=rd,whole_state_equal=not dif,differing_blocks=dif[:10],compared_bytes=sum(map(len,expected.values()))))
  if len(rows)%25==0:print(len(rows),'original entries checked',flush=True)
 return dict(schema='rising-lands/rust-turret-full-state-proof/1',cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,capture_sha256=hashlib.sha256(raw).hexdigest(),state_provenance=pins,provenance=finish(identity,binary),harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),normalization='Adjacent original regions coalesced for fixture transport without adding a byte. Every original byte compared. EFLAGS/EIP outside engine register contract.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/chain_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();r=prove(a.binary)
 with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
