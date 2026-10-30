"""Exact S1 query registers and all captured bytes; original footprints stay sparse."""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain11')
import argparse,hashlib,io,json,lzma,subprocess,time
from pathlib import Path
from chain_leaf_proof import SOURCE,REGS,word,blob,readword,readblob,blocks,initial,PINS
from pinned_reference import provenance
from player_provenance import begin,finish
CAPTURES=(('pesquisas-paralelas/economia/evidencias/lacunas-s1/captura-sac-v2.json.xz',None),('pesquisas-paralelas/economia/evidencias/lacunas-s1/captura-tuyau.json.xz',None),('pesquisas-paralelas/ia-runtime/evidencias/consulta-mina-original.json.xz','MineGetCapacite'),('pesquisas-paralelas/ia-runtime/evidencias/mensagem-cidade-original-v2.json.xz','iagVilleSendMessage'))
def prove(binary):
 start=time.monotonic();identity=begin(binary);prepared=[];payload=bytearray();captures={}
 for path,name in CAPTURES:
  raw=(SOURCE/path).read_bytes();capture=json.loads(lzma.decompress(raw));captures[path]=hashlib.sha256(raw).hexdigest()
  assert capture['original_sha256']=='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
  for c in capture['cases']:
   c=dict(c,stores=c.get('stores',[]));values,stores=initial(c);assert not stores and not c['changed_bytes'];memory=blocks(values)
   regs=dict(c['entry_registers'],ESP=c.get('esp','0x0'))
   payload+=blob((name or c['routine']).encode())+b''.join(word(int(regs[k],16))for k in REGS)+word(len(memory))+b''.join(word(a)+blob(b)for a,b in memory)
   prepared.append((path,c,values))
 run=subprocess.run([str(Path(binary).resolve())],input=word(len(prepared))+payload,capture_output=True,check=True,timeout=120);f=io.BytesIO(run.stdout);rows=[]
 for path,c,expected in prepared:
  code=readword(f);error=readblob(f).decode();regs={k:readword(f)for k in REGS};actual={}
  for _ in range(readword(f)):
   a=readword(f);actual.update({a+i:v for i,v in enumerate(readblob(f))})
  stop=c.get('stop');rd={} if stop else {k:[hex(regs[k]),v]for k,v in c['exit_registers'].items()if regs[k]!=int(v,16)}
  bd=[hex(a)for a in expected.keys()|actual.keys()if expected.get(a)!=actual.get(a)]
  stopped=bool(stop and code and error=='iagVilleSendMessage AI city handler at 0x0048484c')
  rows.append(dict(capture=path,frame=c.get('frame'),kind=c['kind'],routine=c.get('routine','iagVilleSendMessage'),equal=not bd and (stopped if stop else not(code or rd)),expected_stop=stop,error=error,register_differences=rd,byte_differences=bd[:10],bytes_compared=len(expected),registers_compared=[]if stop else list(c['exit_registers'])))
 if f.read():raise ValueError('Trailing fixture output')
 return dict(schema='rising-lands/rust-s1-query-proof/1',reference=provenance(),pins=PINS,provenance=finish(identity,binary),captures=captures,cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,scope='All seven data registers and captured ESP, all supplied bytes, no masks. City captures omit ESP; transport ESP=0 is not compared. Four AI city cases compare the addressed stop and unchanged bytes, not exit registers.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/chain_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();r=prove(a.binary);Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
