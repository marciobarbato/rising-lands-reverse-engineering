"""Surfaces from the advancing Rust world; only frame128 surface/cache are inputs.

Graphics and simulation reference imports live in separate processes because the
historical profiles have distinct modules named construcoes. No module swapping.
The offline AffText adapter accepts only the original attested non-execution.
"""
import os
os.environ['RL_REFERENCE_PROFILE']='chain5'
import argparse,ctypes as C,hashlib,json,pickle,struct,subprocess,sys,time
from pathlib import Path

def worker(binary):
 from pinned_reference import activate
 source=activate()
 from render_probe_proof import Stream
 from render_abi import Catalogo
 from validar_sondas_graficos_m3 import CapturaSondaGrafica,FronteiraTextoGravada
 from validar_entrada_m3 import MemoriaEntradaM3,ArgumentosRasterM3,CatalogoRastreado
 from render_quadro import renderizar_quadro
 from render_proof import inhabited
 cap=CapturaSondaGrafica(source/'pesquisas-paralelas/graficos-animacao/evidencias/sonda-render-P3-api17.json.xz')
 stream=Stream(Path(binary));catalog=CatalogoRastreado();previous=cache=background=None;display_state={}
 try:
  for row in cap.d['rows']:
   blocks=pickle.load(sys.stdin.buffer)
   if blocks is None:break
   memory=MemoriaEntradaM3(blocks);native_cache=cap.cache_entry(row)
   tick=struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0]
   result=stream.frame(memory,tick,initial=(cap.blob(row['before']),native_cache)if previous is None else None,boundaries=row['text_boundaries'])
   py_blocks=[]
   for base,data in memory.blocks:
    data=bytearray(data)
    for address,value in display_state.items():
     if base<=address<base+len(data):data[address-base]=value
    py_blocks.append((base,bytes(data)))
   py_memory=MemoriaEntradaM3(([background]if background is not None else[])+py_blocks)
   with ArgumentosRasterM3(catalog)as raster:
    py=renderizar_quadro(py_memory,superficie_anterior=cap.blob(row['before'])if previous is None else previous,cache=native_cache if cache is None else cache,catalogo=catalog,habitado=lambda i:inhabited(py_memory,i),hud=True,relogio=lambda:tick,texto=FronteiraTextoGravada(cap,row))
   check=dict(frame=row['frame'],original_equal=result['pixels']==cap.blob(row['after']),python_equal=result['pixels']==py.pixels,cache_equal=result['cache']==py.cache,calls_equal=result['calls']==raster.calls,original_calls_equal=result['calls']==row['blits'],stop=result['stop'],text_boundaries=result['text_checked'],capture_sha256=cap.sha)
   check['native_calls_count']=len(result['calls']);check['original_calls_count']=len(row['blits'])
   check['original_call_differences']=[dict(index=i,rust=a,original=b)for i,(a,b)in enumerate(zip(result['calls'],row['blits']))if a!=b][:3] if result['calls']!=row['blits'] else []
   if result['pixels']!=cap.blob(row['after']):
    check['last_calls']={'rust':result['calls'][-5:],'original':row['blits'][-5:]}
    check['display_diff']=[[hex(a),memory.u8(a),cap.memory(row).u8(a)]for a in range(0x4e05a0,0x4e0630)if memory.u8(a)!=cap.memory(row).u8(a)]
    check['pixel_difference']=[i for i,(a,b)in enumerate(zip(result['pixels'],cap.blob(row['after'])))if a!=b][:20]
    check['display_fields']={hex(a):dict(world=memory.u16(a),original=cap.memory(row).u16(a))for a in (0x49a040,0x49a046,0x49a048,0x49a04a,0x49a04c,0x4e05a2,0x496204,0x4e05ac)}
   check['equal']=all(check[q]for q in ('original_equal','python_equal','cache_equal','calls_equal'))and not check['stop']
   pickle.dump(check,sys.stdout.buffer);sys.stdout.buffer.flush()
   previous,cache=result['pixels'],result['cache']
   if result['background']is not None:background=result['background']
   for name,address,old,new in result['effects']:
    for i,value in enumerate(bytes.fromhex(new)):
     if address+i==0x49a041 or 0x49a046<=address+i<0x49a04e:display_state[address+i]=value
 finally:stream.close()

def prove(probe,frames,library,binary):
 from player_proof import Player,FrameInput,FrameRegisters,estado_quadro128,static_inputs,OriginalImage,ambiente_ia_runtime,SOURCE
 from player_provenance import begin,finish
 start=time.monotonic();rust=Player(library);ident=begin(rust.path);_,state,regs=estado_quadro128();h=rust.create()
 image=OriginalImage(ambiente_ia_runtime.EXE,Path(ambiente_ia_runtime.EXE).with_suffix('.SBL'));static=static_inputs(image,state);static[0x45ed20]=image.read(0x45ed20,0x45edc0)
 rust.load(h,sorted([(a,b)for name,(a,b)in state.items()if name!='native_stack']+list(static.items())));rust.execution(h,2);rust.check(rust.lib.rl_avancar_ticks(h,129))
 inp=FrameInput(0,0,0,FrameRegisters.from_values({k:int(v,16)for k,v in regs.items()}),(C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
 root=SOURCE/'pesquisas-paralelas/missoes/m3';script=json.loads((root/'entradas'/f'{probe}.json').read_text());schedule={q['frame']:q for q in script['frames']}
 reference_script=json.loads((root/'entradas/P3.json').read_text())
 if [q for q in script['frames']if q['frame']<=128+frames]!=[q for q in reference_script['frames']if q['frame']<=128+frames]:raise ValueError('Probe scripts differ in this surface window')
 proc=subprocess.Popen([sys.executable,'-B',__file__,'--worker','--binary',str(binary)],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 rows=[];stop=None;logic=0.
 try:
  for k in range(129,129+frames):
   pickle.dump(sorted(rust.snapshot(h).items()),proc.stdin);proc.stdin.flush();check=pickle.load(proc.stdout)
   if check['frame']!=k:raise ValueError('Render frame order')
   rows.append(check)
   if not check['equal']:break
   q=schedule.get(k,{});keys={int(v,0)if isinstance(v,str)else v:int(value,0)if isinstance(value,str)else value for v,value in(q.get('keys')or{}).items()}
   for phase in (2,3):
    t=time.perf_counter();code=rust.input(h,phase,inp,cursor=q.get('cursor')if phase==2 else None,messages=q.get('messages',())if phase==2 else(),keys=keys);logic+=time.perf_counter()-t
    if code:stop=dict(frame=k,phase=phase,error=rust.error());break
   if stop:break
 finally:
  pickle.dump(None,proc.stdin);proc.stdin.close();proc.stdout.close()
  if proc.wait():raise ValueError('Graphics proof worker failed')
  rust.free(h)
 return dict(schema='rising-lands/native-chain-own-state-surface-proof/1',probe=probe,provenance=finish(ident,rust.path),renderer_binary_sha256=hashlib.sha256(Path(binary).read_bytes()).hexdigest(),qualified_text_boundary=True,frames=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),engine_stop=stop,rows=rows,native_logic_seconds=logic,seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--worker',action='store_true');ap.add_argument('--probe',default='P6');ap.add_argument('--frames',type=int,default=92);ap.add_argument('--library',default='motor/target/release/librising_engine.dylib');ap.add_argument('--binary',default='motor/target/release/render_probe_stream');ap.add_argument('--output');a=ap.parse_args()
 if a.worker:worker(a.binary)
 else:
  r=prove(a.probe,a.frames,a.library,a.binary);Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print({k:r[k]for k in ('frames','equal','first_difference','engine_stop','seconds')});raise SystemExit(bool(r['first_difference']))
