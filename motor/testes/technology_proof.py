"""S1 technology: exact original GPRs, ordered stores, foreign calls and x87 pushes."""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain11')
import argparse,hashlib,io,json,lzma,subprocess,time
from pathlib import Path
from chain_leaf_proof import SOURCE,REGS,word,blob,readword,readblob,blocks,initial,PINS
from pinned_reference import provenance
from player_provenance import begin,finish
BASE='pesquisas-paralelas/economia/evidencias/lacunas-s1/'
ENTRIES={'IaRechercheAjuste':0x47fa88,'RechercheCalculNew':0x47150f}
def prove(binary):
 start=time.monotonic();identity=begin(binary);prepared=[];payload=bytearray();captures={}
 for file in ('captura-tecnologia.json.xz','captura-recherche-get-etat-x87.json.xz'):
  raw=(SOURCE/BASE/file).read_bytes();capture=json.loads(lzma.decompress(raw));captures[file]=hashlib.sha256(raw).hexdigest()
  assert capture['original_sha256']=='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
  for c in capture['cases']:
   values,stores=initial(c);memory=blocks(values);regs=dict(c['entry_registers'],ESP=c['esp']);prepared.append((file,c,values,stores))
   payload+=blob(c['routine'].encode())+b''.join(word(int(regs[k],16))for k in REGS)+word(len(memory))+b''.join(word(a)+blob(b)for a,b in memory)
 run=subprocess.run([str(Path(binary).resolve())],input=word(len(prepared))+payload,capture_output=True,check=True,timeout=120);f=io.BytesIO(run.stdout);rows=[]
 for file,c,values,stores in prepared:
  code=readword(f);error=readblob(f).decode();regs={k:readword(f)for k in REGS};fp=[readword(f)for _ in range(4)];actual_stores=[]
  for _ in range(readword(f)):a=readword(f);actual_stores.append((a,readblob(f)))
  calls=[]
  for _ in range(readword(f)):
   name=readblob(f).decode();site=readword(f);incoming={k:readword(f)for k in REGS};outgoing={k:readword(f)for k in REGS};calls.append((name,site,incoming,outgoing))
  actual={}
  for _ in range(readword(f)):
   a=readword(f);actual.update({a+i:v for i,v in enumerate(readblob(f))})
  expected=dict(values);expected.update(stores);expected.update({int(a,16):v for a,_,v in c['changed_bytes']})
  rd={k:[hex(regs[k]),v]for k,v in c['exit_registers'].items()if regs[k]!=int(v,16)};bd=[hex(a)for a in expected.keys()|actual.keys()if expected.get(a)!=actual.get(a)]
  expected_stores=[(int(s[2],16),int(s[4],16).to_bytes(s[3],'little'))for s in c['stores']];sd=next(([i,a,b]for i,(a,b)in enumerate(zip(actual_stores,expected_stores))if a!=b),None)
  # Capture arguments cover EAX/EBX/ECX/EDX. All seven exit GPRs are captured.
  external=[v for v in c['calls']if v[1]in ('MissionGetNum','PlayerGetType')];cd=[]
  for i,(native,call)in enumerate(zip(external,calls)):
   name,site,inc,out=call;owner,offset=native[3].split('+');expected_site=ENTRIES[owner]+int(offset,16)-5
   dif={k:[hex(inc[k]),v]for k,v in native[2].items()if inc[k]!=int(v,16)};outdif={k:[hex(out[k]),v]for k,v in native[5].items()if out[k]!=int(v,16)}
   if name!=native[1]or site!=expected_site or dif or outdif:cd.append(dict(index=i,name=name,site=hex(site),expected_site=hex(expected_site),inputs=dif,outputs=outdif))
  call_equal=len(calls)==len(external)and not cd
  fp_equal=True;fp_expected=None
  if 'x87_after'in c:
   before,after=c['x87_before'],c['x87_after'];top=(after['FPSW']>>11)&7
   assert top==(((before['FPSW']>>11)&7)-1)&7
   fp_expected=after[f'FP{top}'];fp_equal=fp[0]==1 and [fp[1]|fp[2]<<32,fp[3]]==fp_expected
  stores_equal=actual_stores==expected_stores
  rows.append(dict(routine=c['routine'],frame=c.get('frame'),kind=c['kind'],capture=file,equal=not(code or rd or bd)and stores_equal and call_equal and fp_equal,error=error,register_differences=rd,byte_differences=bd[:10],bytes_compared=len(expected),ordered_stores_equal=stores_equal,store_counts=[len(actual_stores),len(expected_stores)],first_store_difference=repr(sd)if sd else None,foreign_calls_equal=call_equal,foreign_call_counts=[len(calls),len(external)],foreign_call_differences=cd,x87_push_equal=fp_equal,x87_push_expected=fp_expected))
 if f.read():raise ValueError('Trailing fixture output')
 return dict(schema='rising-lands/rust-s1-technology-proof/1',reference=provenance(),pins=PINS,provenance=finish(identity,binary),captures=captures,cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,scope='All captured GPRs/ESP and supplied bytes, every ordered store (including unchanged values), all foreign calls in order with captured input registers and seven output GPRs. Live Rust MissionGetNum/PlayerGetType bodies execute from captured memory; no replayed returns. Nine x87 cases compare the exact newly pushed extended value and TOP change only, not a complete FPU stack/flags implementation. Validation tracing is compiled out of production.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/technology-trace/release/technology_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();r=prove(a.binary);Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
