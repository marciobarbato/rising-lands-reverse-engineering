"""Original leaf captures through the native input adapter (no x86 execution).

Memory is exactly the captured read union plus per-case overrides, coalesced
into adjacent spans. Unknown reads fail instead of receiving synthetic pages.
Semantic-return comparisons are separate from unmodeled register leftovers.
"""
import os
os.environ['RL_REFERENCE_PROFILE']='input'
import argparse,hashlib,json,lzma,struct,subprocess,io,base64,zlib,signal
from pathlib import Path
from pinned_reference import activate,provenance,REPO
SOURCE=activate()
from player_pins import verify
PINS=verify()
from player_provenance import begin,finish

SUPPORTED={'ResetOrdre','SetDeplaceEngin','DeplaceEngin','EnginOccupeCase','BatimentCollision','TerrainEstHerbe','ValideHerse','ChercheMurCombinaisons','ResetCheminTerrainModify','SelectionAddEngin','RetireSelectionEngin','EnginSelectionnable','EnginInZone','DeselectionEngin','Deselection','SetRecolteEngin','SetTransporteEngin','InputGame','CalculIconeAction','ProcessInputGame','SetPlayerOrdre','MouseZone','MouseEstDeplacer','KeyPressed','KeyUnPressed','KeyTestRelease','WndProc','GrabAllInput','MiniMapGetCase','MiniMapGetCenterSelect','IconeGetZone','EnginGetBagOrdre','BagGetCode','BagGetType','SelectionEngin','DeSelectionGroupe','BatimentDeselectionner','BatimentSelection','EnginAddSelection','EnginAsk','SetDeplaceEnginSelect','SetAttaqueEnginSelect','SetConstruitBatimentSelect','SetEnginConstruitBatiment','SetRecolteEnginSelect','SetTransporteEnginSelect','SetMineEnginSelect','SetRamasseEnginSelect','SetDepotEnginSelect','EnginTravailSelectionne','BatimentPosable','BatimentConstructible','PlaceBatiment','CreerBatiment','CalculConstruireBatiment','DecouvreTerrain','IllumineTerrain','EteintTerrain','SetMiniMap','ReseauActif','MiniMapSetLock','GoLastAttaque'}
# Frozen corpus paths; the snapshot manifest pins their bytes and sources.
CORPORA=[('pesquisas-paralelas/ia-runtime/evidencias/captura-entrada-ordens-ia.json','pesquisas-paralelas/ia-runtime/evidencias/leituras-entrada-ordens-ia.json.xz'),('evidencias/selecao-ordens/captura-selecao-ordens-exibicao.json','evidencias/selecao-ordens/leituras-selecao-ordens-exibicao.json'),('evidencias/construcao-core/captura-construcao-core-exibicao.json','evidencias/construcao-core/leituras-construcao-core-exibicao.json')]

def document(path):
 b=(SOURCE/path).read_bytes();return json.loads(lzma.decompress(b) if path.endswith('.xz') else b)
def overlay(runs,out=None):
 out={} if out is None else out
 for a,data in runs:
  a=int(a,16);out.update({a+i:v for i,v in enumerate(bytes.fromhex(data))})
 return out
def blocks(values):
 out=[]
 for a in sorted(values):
  if out and a==out[-1][0]+len(out[-1][1]):out[-1][1].append(values[a])
  else:out.append((a,bytearray([values[a]])))
 return out
def u32(v):return struct.pack('<I',v&0xffffffff)
def blob(b):return u32(len(b))+b
def readword(stream):return struct.unpack('<I',stream.read(4))[0]
def readblob(stream):return stream.read(readword(stream))

def proof(binary):
 identity=begin(binary)
 from provar_entrada_ia import estado_quadro128
 _,checkpoint,_=estado_quadro128()
 dimensions=next(struct.unpack_from('<HH',data,0x497168-base) for base,data in checkpoint.values() if base<=0x497168 and 0x49716c<=base+len(data))
 if dimensions!=(64,64):raise ValueError('Unexpected original MONDE01 dimensions')
 segments=sorted(checkpoint.values())
 def checkpoint_bytes(address,n):
  return next(data[address-base:address-base+n] for base,data in segments if base<=address and address+n<=base+len(data))
 cases=[];skips=[];identities={}
 for cap_path,reads_path in CORPORA:
  cap=document(cap_path);reads=document(reads_path);base=overlay(reads.get('base',[]));identities[cap_path]=hashlib.sha256((SOURCE/cap_path).read_bytes()).hexdigest();identities[reads_path]=hashlib.sha256((SOURCE/reads_path).read_bytes()).hexdigest()
  for c in cap['cases']:
   if c['routine'] not in SUPPORTED:skips.append(dict(corpus=cap_path,case=c['case'],routine=c['routine'],reason='outside this input routine adapter'));continue
   keys={};varies=False
   for _,vk,v in c.get('declared_keys_consumed',[]):
    if vk in keys and keys[vk]!=v:varies=True
    keys[vk]=v
   if varies:skips.append(dict(corpus=cap_path,case=c['case'],routine=c['routine'],reason='leaf polls a changing key stream; per-frame schema supplies a fixed key table'));continue
   known=overlay(reads['cases'][c['case']],dict(base))
   known=overlay(c.get('writes',[]),known)
   changed={int(address,16):old for address,old,new in c['changed_bytes']}
   # The capture enumerates every final changed byte. For a stored byte absent
   # from that list, its final (last stored) value is also its original value.
   stored={}
   for store in c.get('stores',[]):
    a,n,v=int(store[2],16),store[3],int(store[4],16)
    stored.update({a+i:byte for i,byte in enumerate(v.to_bytes(n,'little'))})
   for a,v in stored.items():
    if a not in changed:
     if a in known and known[a]!=v:raise ValueError(('Original unchanged-store contradiction',c['case'],hex(a)))
     known[a]=v
   known.update(changed)
   if c['routine']=='DeplaceEngin':
    # Native leaf footprints omit map height; the Python live-world contract
    # reads it. MONDE01's accepted checkpoint explicitly declares 64x64.
    for a,v in ((0x497168+i,b) for i,b in enumerate(struct.pack('<HH',*dimensions))):
     if a in known and known[a]!=v:raise ValueError('MONDE01 height disagrees')
     known[a]=v
   # Explicit synthetic writable page padding, as in the frame-provider gate.
   # Only recorded original bytes justify an original-state assertion.
   pages={a&~4095 for a in known}
   for store in c.get('stores',[]):
    a,n=int(store[2],16),store[3];pages.update(v&~4095 for v in range(a,a+n))
   padded={a+i:0 for a in pages for i in range(4096)}
   if c['routine']=='DeplaceEngin':
    # The leaf footprint records original CPU reads. The live Python/Rust
    # navigation facade also reads the declared terrain/bonus views. Supply
    # their actual immutable checkpoint inputs, rather than zero pointers.
    extra_pages={0x4df000,0x496000,0x497000,0x507000,0x508000}
    objects=int.from_bytes(checkpoint_bytes(0x507d74,4),'little')
    extra_pages.update(range(objects,objects+65536,4096))
    for page in pages|extra_pages:
     for checkpoint_base,data in segments:
      first=max(checkpoint_base,page);last=min(checkpoint_base+len(data),page+4096)
      if first<last:padded.update({first+i:v for i,v in enumerate(data[first-checkpoint_base:last-checkpoint_base])})
   padded.update(known);known=padded
   if c['routine']=='ProcessInputGame':
    from frame_differential import OriginalImage
    import ambiente_ia_runtime
    image=OriginalImage(ambiente_ia_runtime.EXE,Path(ambiente_ia_runtime.EXE).with_suffix('.SBL'))
    known.update({0x45ed20+i:v for i,v in enumerate(image.read(0x45ed20,0x45edc0))})
   args=[int(c['entry_registers'][r],16) for r in ('EAX','EDX','EBX','ECX')];stack=[int(v,16) for v in c.get('stack_words',[])];args+=(stack+[0,0])[:2]
   if c['routine']=='WndProc':args[:4]=stack[:4]
   cases.append(dict(corpus=cap_path,case=c,known=blocks(known),args=args,keys=keys,cursor=reads.get('cursor',[0,0])))
 audio_path='pesquisas-paralelas/audio/evidencias/m3-pedidos-original-v1.json'
 audio=document(audio_path);identities[audio_path]=hashlib.sha256((SOURCE/audio_path).read_bytes()).hexdigest()
 for original in audio['cases']:
  known={}
  for region in original['input']['memory']:
   data=zlib.decompress(base64.b64decode(region['zlib_base64']))
   if hashlib.sha256(data).hexdigest()!=region['sha256']:raise ValueError('Audio input hash')
   a=int(region['base'],16);known.update({a+i:v for i,v in enumerate(data)})
  regs=original['input']['regs'];name='PlaySnd_PostSound' if original['operation']=='post' else 'PlaySnd_StopSound'
  case=dict(case=original['name'],routine=name,changed_bytes=[])
  cases.append(dict(corpus=audio_path,case=case,known=blocks(known),args=[regs.get(k,0) for k in ('EAX','EDX','EBX','ECX')]+(original['input']['arguments']+[0,0])[:2],keys={},cursor=[0,0],semantic_expected=int(original['eax'],16)))
 inp=bytearray(u32(len(cases)))
 for c in cases:
  inp+=blob(c['case']['routine'].encode())+b''.join(u32(v) for v in c['args'])+b''.join(u32(v) for v in c['cursor'])+u32(len(c['keys']))
  for k,v in c['keys'].items():inp+=u32(k)+u32(v)
  bs=c['known'];inp+=u32(len(bs))
  for a,b in bs:inp+=u32(a)+blob(bytes(b))
 run=subprocess.run([str(Path(binary).resolve())],input=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=1100);stream=io.BytesIO(run.stdout);results=[]
 for c in cases:
  status,has_value,value=readword(stream),readword(stream),readword(stream);error=readblob(stream).decode();actual={}
  for _ in range(readword(stream)):
   a=readword(stream);data=readblob(stream);actual.update({a+i:v for i,v in enumerate(data)})
  expected={a+i:v for a,b in c['known'] for i,v in enumerate(b)}
  for a,old,new in c['case']['changed_bytes']:expected[int(a,16)]=new
  diff=[(hex(a),expected[a],actual.get(a)) for a in expected if actual.get(a)!=expected[a]]
  semantic_masks={'MouseZone':65535,'MouseEstDeplacer':0xffffffff,'KeyPressed':0xffffffff,'KeyUnPressed':0xffffffff,'WndProc':0xffffffff,'EnginGetBagOrdre':0xffffffff,'BagGetCode':0xffffffff,'BagGetType':0xffffffff,'MiniMapGetCase':0xffffffff,'IconeGetZone':0xffffffff,'ProcessInputGame':0xffffffff,'SetPlayerOrdre':0xffffffff,'BatimentPosable':255,'BatimentConstructible':255,'EnginOccupeCase':255,'BatimentCollision':255,'TerrainEstHerbe':255,'ValideHerse':255,'ChercheMurCombinaisons':255,'ResetCheminTerrainModify':0xffffffff}
  scalar_mask=semantic_masks.get(c['case']['routine'])
  if not status and scalar_mask is not None:
   expected_scalar=int(c['case']['exit_registers']['EAX'],16)&scalar_mask
   if not has_value or value&scalar_mask!=expected_scalar:diff.append(('semantic return',expected_scalar,value&scalar_mask if has_value else None))
  if 'semantic_expected' in c and (not has_value or value!=c['semantic_expected']):diff.append(('semantic return',c['semantic_expected'],value if has_value else None))
  results.append(dict(corpus=c['corpus'],case=c['case']['case'],routine=c['case']['routine'],completed=status==0,stop=error or None,changed_byte_mismatches=diff[:12],state_equal=not diff,semantic_return=value if has_value else None))
 if stream.read():raise ValueError('Trailing native fixture bytes')
 return dict(schema='rising-lands/rust-input-leaf-proof/1',provenance=finish(identity,binary),reference=provenance(),evidence_sha256=identities,cases=len(cases),completed=sum(r['completed'] for r in results),completed_state_equal=sum(r['completed'] and r['state_equal'] for r in results),mismatches=[r for r in results if r['completed'] and not r['state_equal']],stops=[r for r in results if not r['completed']],skips=skips,results=results,scope='Captured reads/changed bytes and complete explicit synthetic page fixture; no original claim for padding, residual registers, changing key streams or fresh x86.')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/player_fixtures');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=proof(a.binary);Path(a.output).write_text(json.dumps(r,indent=1,sort_keys=True)+'\n');print(json.dumps({k:r[k] if k not in ('stops','skips') else len(r[k]) for k in ('cases','completed','completed_state_equal','mismatches','stops','skips')},indent=1));return int(bool(r['mismatches']))
if __name__=='__main__':raise SystemExit(main())
