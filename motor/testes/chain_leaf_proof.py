"""Strict register/byte comparison of native owner entries with committed original captures."""
import os
os.environ['RL_REFERENCE_PROFILE']='chain5'
import argparse,hashlib,io,json,lzma,struct,subprocess,time
from pathlib import Path
from pinned_reference import activate,provenance,REPO
SOURCE=activate()
from player_pins import verify
PINS=verify()
from player_provenance import begin,finish
REGS=('EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP')
def word(n):return struct.pack('<I',n&0xffffffff)
def blob(b):return word(len(b))+b
def readword(f):return struct.unpack('<I',f.read(4))[0]
def readblob(f):return f.read(readword(f))
def blocks(values):
 out=[]
 for a,v in sorted(values.items()):
  if out and a==out[-1][0]+len(out[-1][1]):out[-1][1].append(v)
  else:out.append((a,bytearray([v])))
 return out
def initial(c,reads=None):
 known={int(a,16)+i:v for a,b in c.get('read_before_write',reads or [])for i,v in enumerate(bytes.fromhex(b))}
 old={int(a,16):v for a,v,_ in c['changed_bytes']};stored={}
 for store in c['stores']:
  a,n,v=int(store[2],16),store[3],int(store[4],16)
  stored.update({a+i:b for i,b in enumerate(v.to_bytes(n,'little'))})
 for a,v in stored.items():
  if a not in old:
   if a in known and known[a]!=v:raise ValueError(('Capture unchanged-store contradiction',hex(a)))
   known[a]=v
 known.update(old);return known,stored
def prove(binary,routines,capture=None):
 start=time.monotonic();identity=begin(binary);name=capture or 'pesquisas-paralelas/economia/evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz';raw=(SOURCE/name).read_bytes();cap=json.loads(lzma.decompress(raw))
 assert cap['original_sha256']=='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
 cases=[c for c in cap.get('calls',cap.get('cases',[]))if c['routine']in routines];assert cases
 reads={}
 if 'cases'in cap:
  read_path=name.replace('captura-','leituras-');read_raw=(SOURCE/read_path).read_bytes();read_doc=json.loads(lzma.decompress(read_raw));reads=read_doc['cases']
  if read_doc['capture']['sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('Footprint capture identity')
  cases=[dict(c,read_before_write=reads[c['case']])for c in cases]
 payload=bytearray(word(len(cases)));prepared=[]
 for c in cases:
  values,stores=initial(c);memory=blocks(values);prepared.append((values,stores))
  payload+=blob(c['routine'].encode())+b''.join(word(int(c['entry_registers'][k],16))for k in REGS)+word(len(memory))
  for a,b in memory:payload+=word(a)+blob(b)
 run=subprocess.run([str(Path(binary).resolve())],input=payload,capture_output=True,check=True,timeout=1000);f=io.BytesIO(run.stdout);rows=[]
 for c,(values,stores)in zip(cases,prepared):
  code=readword(f);error=readblob(f).decode();regs={k:readword(f)for k in REGS};actual={}
  for _ in range(readword(f)):
   a=readword(f);actual.update({a+i:v for i,v in enumerate(readblob(f))})
  expected=dict(values);expected.update(stores)
  # Compare every supplied byte, every original changed byte and all modeled exit registers.
  changed={int(a,16):v for a,_,v in c['changed_bytes']};expected.update(changed)
  rd={k:[hex(regs[k]),c['exit_registers'][k]]for k in REGS if regs[k]!=int(c['exit_registers'][k],16)}
  bd=[hex(a)for a in actual.keys()|expected.keys()if actual.get(a)!=expected.get(a)]
  rows.append(dict(routine=c['routine'],frame=c.get('frame'),case=c.get('case'),counter=c.get('counter'),equal=not(code or rd or bd),error=error,register_differences=rd,byte_differences=bd[:20],bytes_compared=len(expected)))
 if f.read():raise ValueError('Trailing fixture output')
 return dict(schema='rising-lands/native-chain-owner-leaf-proof/1',reference=provenance(),pins=PINS,provenance=finish(identity,binary),capture=name,capture_sha256=hashlib.sha256(raw).hexdigest(),cases=len(rows),equal=sum(c['equal']for c in rows),first_difference=next((c for c in rows if not c['equal']),None),results=rows,seconds=time.monotonic()-start)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/chain_fixtures');ap.add_argument('--routine',action='append',default=[]);ap.add_argument('--capture');ap.add_argument('--output',required=True);a=ap.parse_args();r=prove(a.binary,a.routine or ['BatimentNextEtape'],a.capture);p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print({k:r[k]for k in ('cases','equal','first_difference','seconds')});return int(r['first_difference']is not None)
if __name__=='__main__':raise SystemExit(main())
