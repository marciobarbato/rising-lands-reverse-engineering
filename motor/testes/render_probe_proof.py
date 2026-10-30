"""Graphics 1.7 original probe windows with strict/default text contracts.

Each probe carries Rust surface/cache/background through all native render-entry
states. No later native surface/cache is reloaded. Full-window qualification is
ONLY the published, exactly attested AffText non-execution; the production C ABI
has no way to install it and retains the original-address glyph stop.
"""
import argparse,ctypes as C,hashlib,json,lzma,struct,subprocess,sys,time
from pathlib import Path
from render_abi import *
from render_proof import renderer_pins,inhabited
from frame_long_differential import source_hashes,metadata,write_json
from validar_sondas_graficos_m3 import CapturaSondaGrafica,FronteiraTextoGravada
from validar_entrada_m3 import MemoriaEntradaM3
sha=lambda b:hashlib.sha256(b).hexdigest()
OBS=struct.Struct('<II48sI8i8s8s')
class Stream:
 def __init__(self,binary):
  self.p=subprocess.Popen([str(binary)],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
  self.p.stdin.write(b'RLRP1700')
  for value in original_assets():self.send_blob(value)
  self.p.stdin.flush()
 def send_u32(self,n):self.p.stdin.write(struct.pack('<I',n&0xffffffff))
 def send_blob(self,b):self.send_u32(len(b));self.p.stdin.write(b)
 def read(self,n):
  out=bytearray()
  while len(out)<n:
   chunk=self.p.stdout.read(n-len(out))
   if not chunk:raise RuntimeError('Rust fixture stream exited: '+str(self.p.poll()))
   out.extend(chunk)
  return bytes(out)
 def u32(self):return struct.unpack('<I',self.read(4))[0]
 def blob(self):return self.read(self.u32())
 def frame(self,memory,tick,initial=None,boundaries=None,facade=None):
  flags=(1 if initial else 0)|(2 if boundaries is not None else 0)|(4 if facade else 0)
  self.send_u32(flags);self.send_u32(tick);self.send_u32(len(memory.blocks))
  for a,b in memory.blocks:self.send_u32(a);self.send_blob(b)
  if initial:
   surface,cache=initial;self.send_blob(surface);self.send_blob(cache.registros);self.send_blob(cache.blocos_crus);self.send_u32(cache.proximo)
  if boundaries is not None:
   self.send_u32(len(boundaries))
   for event in boundaries:
    regs=event['registers'];stack=bytes.fromhex(event['stack']);self.send_blob(bytes.fromhex(event['text_hex']))
    for name in ['EAX','EDX','EBX','ECX']:self.send_u32(int(regs[name],16))
    for v in struct.unpack_from('<III',stack,8):self.send_u32(v)
    self.p.stdin.write(bytes.fromhex(event['surface_before']))
  if facade:
   for v in facade:self.send_u32(v)
  self.p.stdin.flush();disposition=self.u32();stop=self.u32();reason=self.blob().decode();text_checked=self.u32();pixels=self.blob();cache=EstadoCache(self.blob(),self.blob(),self.u32());address=self.u32();background=self.blob()
  calls=[];effects=[];requests=[]
  for _ in range(self.u32()):
   kind,a,name,count,*tail=OBS.unpack(self.read(OBS.size));name=name.split(b'\0')[0].decode();args=tail[:8];old,new=tail[8:]
   if kind==1:effects.append((name,a,old[:count].hex(),new[:count].hex()))
   elif kind==2:calls.append([name,*args[:count]])
   elif kind==3:
    if address!=a or count!=len(background):raise AssertionError('Saved-background observation/query disagree')
    effects.append((name,a,'',background.hex()))
   elif kind==4:requests.append(dict(text=(old+new)[:args[7]].hex(),rectangle=args[:4],font=args[4],flags=args[5:7]))
   else:raise AssertionError('Unknown renderer observation')
  return dict(disposition=disposition,stop=stop,reason=reason,text_checked=text_checked,pixels=pixels,cache=cache,background=(address,background) if background else None,calls=calls,effects=effects,text_requests=requests)
 def close(self):
  self.p.stdin.close();self.p.stdout.close();code=self.p.wait()
  if code:raise RuntimeError('Rust probe driver exit '+str(code))

def prove(probe,binary=None,frames=None,strict=False,python=True):
 renderer_pins();path=RAIZ/f'evidencias/sonda-render-{probe}-api17.json.xz';cap=CapturaSondaGrafica(path);catalog=Catalogo();binary=Path(binary or ROOT/'motor/target/release/render_probe_stream');stream=Stream(binary)
 expected_count={'P1':501,'P2':601,'P3':172}[probe]
 if len(cap.d['rows'])!=expected_count:raise ValueError('Published 1.7 probe window changed')
 rows=[];cache=previous=background=None;first_stop=None;t0=time.monotonic()
 try:
  for row in cap.d['rows'][:frames]:
   m=cap.memory(row);native_cache=cap.cache_entry(row)
   entry_cache_equal=cache is None or cache==native_cache
   entry_background_equal=background is None or 'saved_background' not in row['entry'] or sha(background[1])==row['entry']['saved_background'][1]
   tick=struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0]
   result=stream.frame(m,tick,initial=(cap.blob(row['before']),native_cache) if previous is None else None,boundaries=None if strict else row['text_boundaries'])
   expected=cap.blob(row['after']);record=dict(frame=row['frame'],stop=hex(result['stop']) if result['stop'] else None,reason=result['reason'],sha256=sha(result['pixels']),native_sha256=row['after'],entry_cache_equal=entry_cache_equal,entry_background_equal=entry_background_equal,text_checked=result['text_checked'])
   record['original_equal']=not result['stop'] and result['pixels']==expected
   record['arguments_equal']=result['calls']==(row['blits'][:len(result['calls'])] if result['stop'] else row['blits'])
   dg=bytearray(m.ler_mundo(0x494000,len(cap.blob(row['exit_dgroup']))))
   for name,a,old,new in result['effects']:
    value=bytes.fromhex(new)
    if 0x494000<=a<a+len(value)<=0x523000:dg[a-0x494000:a-0x494000+len(value)]=value
   struct.pack_into('<H',dg,0x49a04e-0x494000,result['cache'].proximo)
   native_dg=cap.blob(row['exit_dgroup']);excluded={a+i for a in (0x508f70,0x4e17a4) for i in range(4)}
   record['dgroup_equal']=None if result['stop'] else all(a==b or 0x494000+i in excluded for i,(a,b) in enumerate(zip(dg,native_dg)))
   if python:
    py=cap.render(row,catalog,previous,cache,saved_background=background,texto=None if strict else FronteiraTextoGravada(cap,row))
    record.update(python_equal=result['pixels']==py.pixels,cache_equal=result['cache']==py.cache,effects_equal=result['effects']==list(py.efeitos),stop_equal=result['stop']==(int(py.parada['endereco'],16) if py.parada else 0))
   if result['stop']:
    record['native_partial_equal']=bool(row['text_boundaries']) and result['pixels']==cap.blob(row['text_boundaries'][0]['surface_before'])
    first_stop=record
   rows.append(record);previous,cache=result['pixels'],result['cache']
   if result['background'] is not None:background=result['background']
   if result['stop']:break
   if any(record.get(k) is False for k in ('original_equal','arguments_equal','dgroup_equal','python_equal','cache_equal','effects_equal','entry_cache_equal','entry_background_equal')):
    print('FIRST DIFFERENCE',probe,record,flush=True);break
   if len(rows)%50==0:print(probe,len(rows),row['frame'],'equal',flush=True)
 finally:stream.close()
 return dict(schema='rising-lands/rust-graphics17-probe-proof/1',probe=probe,scope='production default glyph stop' if strict else 'published exact recorded AffText non-execution contract; not glyph reconstruction',capture_sha256=cap.sha,frames_requested=frames or expected_count,frames=len(rows),full_equal=sum(r['original_equal'] for r in rows),text_boundaries_checked=sum(r['text_checked'] for r in rows),first_stop=first_stop,first_difference=next((r for r in rows if any(r.get(k) is False for k in ('arguments_equal','python_equal','cache_equal','effects_equal','stop_equal','entry_cache_equal','entry_background_equal')) or (not r['stop'] and (not r['original_equal'] or not r['dgroup_equal']))),None),wall_seconds=time.monotonic()-t0,rows=rows)

def main():
 p=argparse.ArgumentParser();p.add_argument('--probe',choices=['P1','P2','P3'],required=True);p.add_argument('--binary');p.add_argument('--frames',type=int);p.add_argument('--strict',action='store_true');p.add_argument('--no-python',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
 if Path(a.output).exists():raise SystemExit('Refusing overwrite')
 before=source_hashes();report=prove(a.probe,a.binary,a.frames,a.strict,not a.no_python);after=source_hashes();report.update(metadata(),source_sha256=before,sources_unchanged=before==after,reference_pins=renderer_pins(),binary_sha256=sha(Path(a.binary or ROOT/'motor/target/release/render_probe_stream').read_bytes()));write_json(a.output,report);print({k:v for k,v in report.items() if k not in ('rows','source_sha256','reference_pins')});return bool(report['first_difference']) or before!=after
if __name__=='__main__':sys.exit(main())
