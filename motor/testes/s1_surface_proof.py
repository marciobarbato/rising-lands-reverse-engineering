"""Advancing Rust S1 surfaces with original-only raster/text attestations.

The initial surface/cache is the original frame128 opening. Every subsequent
world, surface, cache and background is carried; no native checkpoint repairs
Rust. Graphics Python imports stay in a separate worker from game logic.
"""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain9')
import argparse,hashlib,json,lzma,pickle,signal,struct,subprocess,sys,time
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()

def attestations(paths,source):
 base=source/'pesquisas-paralelas/missoes/m3';script=(base/'entradas/S1.json').read_bytes();raw=(base/'sondas/S1/quadros.jsonl.xz').read_bytes();refs={r['frame']:r for r in map(json.loads,lzma.decompress(raw).splitlines())};rows={};pins={}
 for path in paths:
  data=Path(path).read_bytes();doc=json.loads(lzma.decompress(data));pins[str(path)]=sha(data)
  if doc['translation_executed']or doc['original_sha256']!='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'or doc['input_sha256']!=sha(script)or doc['records_sha256']!=sha(raw):raise ValueError('S1 original attestation identity')
  checks={r['frame']:r for r in doc['checks']}
  for row in doc['rows']:
   k=row['frame'];check=checks[k]
   if k in rows or not check['equal']or check['state_sha256']!=refs[k]['state_sha256']or row['after']!=refs[k]['surfaces_between']['offscreen']or check['frame_sha256']!=refs[k]['surfaces_frame']['offscreen']:raise ValueError('S1 original replay differs')
   rows[k]=row
 return rows,refs,pins

def worker(args):
 from pinned_reference import activate
 source=activate()
 from render_probe_proof import Stream
 from render_abi import Catalogo
 from validar_sondas_graficos_m3 import CapturaSondaGrafica,FronteiraTextoGravada
 from validar_entrada_m3 import MemoriaEntradaM3,ArgumentosRasterM3,CatalogoRastreado
 from render_quadro import renderizar_quadro
 from render_proof import inhabited
 rows,refs,pins=attestations(args.capture,source)
 initial=CapturaSondaGrafica(source/'pesquisas-paralelas/graficos-animacao/evidencias/sonda-render-P3-api17.json.xz');first=initial.d['rows'][0]
 if first['frame']!=129 or first['before']!=rows[129]['before']:raise ValueError('S1 frame128 renderer opening differs')
 stream=Stream(Path(args.binary));catalog=CatalogoRastreado();previous=cache=background=None;display={}
 try:
  for k in range(129,129+args.frames):
   blocks=pickle.load(sys.stdin.buffer)
   if blocks is None:break
   row=rows[k];m=MemoriaEntradaM3(blocks)
   if previous is not None and sha(previous)!=row['before']:raise ValueError('Original render entry surface differs from carried Rust output')
   # CalculFrame's harness clock is refreshed once per captured frame.
   # The committed original has the same 1,000,000-ms virtual timer as M2.
   tick=m.u32(0x4e17b4)
   result=stream.frame(m,tick,initial=(initial.blob(first['before']),initial.cache_entry(first))if previous is None else None,boundaries=row['text_boundaries'])
   py_blocks=[]
   for address,data in m.blocks:
    data=bytearray(data)
    for a,value in display.items():
     if address<=a<address+len(data):data[a-address]=value
    py_blocks.append((address,bytes(data)))
   pm=MemoriaEntradaM3(([background]if background else[])+py_blocks)
   with ArgumentosRasterM3(catalog)as raster:
    py=renderizar_quadro(pm,superficie_anterior=initial.blob(first['before'])if previous is None else previous,cache=initial.cache_entry(first)if cache is None else cache,catalogo=catalog,habitado=lambda i:inhabited(pm,i),hud=True,relogio=lambda:tick,texto=FronteiraTextoGravada(initial,row))
   check=dict(frame=k,original_equal=sha(result['pixels'])==row['after'],python_equal=result['pixels']==py.pixels,cache_equal=result['cache']==py.cache,calls_equal=result['calls']==raster.calls,original_calls_equal=result['calls']==row['blits'],effects_equal=result['effects']==list(py.efeitos),stop=result['stop'],python_stop=py.parada,reason=result['reason'],text_boundaries=result['text_checked'],surface_sha256=sha(result['pixels']),native_surface_sha256=row['after'])
   check['equal']=not check['stop']and not check['python_stop']and all(v for name,v in check.items()if name.endswith('_equal'))
   pickle.dump(check,sys.stdout.buffer);sys.stdout.buffer.flush()
   if not check['equal']:break
   previous,cache=result['pixels'],result['cache']
   if result['background']is not None:background=result['background']
   for name,address,old,new in result['effects']:
    for i,value in enumerate(bytes.fromhex(new)):
     if address+i==0x49a041 or 0x49a046<=address+i<0x49a04e:display[address+i]=value
 finally:stream.close()

def prove(args):
 import ctypes as C
 from player_proof import Player,FrameInput,FrameRegisters,estado_quadro128,static_inputs,OriginalImage,ambiente_ia_runtime,SOURCE
 from player_provenance import begin,finish
 start=time.monotonic();rust=Player(args.library);identity=begin(rust.path);_,state,regs=estado_quadro128();h=rust.create();image=OriginalImage(ambiente_ia_runtime.EXE,Path(ambiente_ia_runtime.EXE).with_suffix('.SBL'));static=static_inputs(image,state);static[0x45ed20]=image.read(0x45ed20,0x45edc0)
 rust.load(h,sorted([(a,b)for n,(a,b)in state.items()if n!='native_stack']+list(static.items())));rust.execution(h,2);rust.check(rust.lib.rl_avancar_ticks(h,129))
 inp=FrameInput(0,0,0,FrameRegisters.from_values({k:int(v,16)for k,v in regs.items()}),(C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
 script=(SOURCE/'pesquisas-paralelas/missoes/m3/entradas/S1.json').read_bytes();schedule={q['frame']:q for q in json.loads(script)['frames']};_,refs,pins=attestations(args.capture,SOURCE)
 proc=subprocess.Popen([sys.executable,'-B',__file__,'--worker','--frames',str(args.frames),'--binary',args.binary,*[v for p in args.capture for v in ('--capture',p)]],stdin=subprocess.PIPE,stdout=subprocess.PIPE);rows=[];stop=None
 try:
  for k in range(129,129+args.frames):
   pickle.dump(sorted(rust.snapshot(h).items()),proc.stdin);proc.stdin.flush();row=pickle.load(proc.stdout)
   if row['frame']!=k:raise ValueError('S1 render order')
   rows.append(row)
   if not row['equal']:break
   q=schedule.get(k,{});keys={int(v,0)if isinstance(v,str)else v:int(value,0)if isinstance(value,str)else value for v,value in(q.get('keys')or{}).items()}
   for phase in (2,3):
    code=rust.input(h,phase,inp,cursor=q.get('cursor')if phase==2 else None,messages=q.get('messages',())if phase==2 else(),keys=keys)
    if code:stop=dict(frame=k,phase=phase,error=rust.error());break
   if stop:break
   if k%250==0:print(k,'S1 surfaces equal',flush=True)
 finally:
  proc.stdin.close();proc.stdout.close();rust.free(h)
  if proc.wait():raise ValueError('S1 Graphics worker failed')
 return dict(schema='rising-lands/rust-s1-own-state-surface-proof/1',frames=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),engine_stop=stop,rows=rows,attestation_sha256=pins,input_sha256=sha(script),provenance=finish(identity,rust.path),renderer_binary_sha256=sha(Path(args.binary).read_bytes()),qualified_text_boundary=True,seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--worker',action='store_true');ap.add_argument('--frames',type=int,required=True);ap.add_argument('--capture',action='append',required=True);ap.add_argument('--binary',default='motor/target/release/render_probe_stream');ap.add_argument('--library',default='motor/target/release/librising_engine.dylib');ap.add_argument('--output');a=ap.parse_args();signal.alarm(1140)
 if a.worker:worker(a)
 else:
  r=prove(a)
  with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
  print({k:r[k]for k in ('frames','equal','first_difference','engine_stop','seconds')});raise SystemExit(r['first_difference']is not None)
