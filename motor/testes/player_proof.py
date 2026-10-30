"""Native declared-input chain versus immutable Mac mini probes and pinned Python.

The indicator comparison is precisely provar_entrada_ia's domain, not an
implicit whole-state claim. No later captured state is loaded into Rust.
"""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','input')
import argparse,bisect,ctypes as C,hashlib,json,lzma,subprocess,time,re,signal
from pathlib import Path
from pinned_reference import activate,provenance,REPO,INPUT_REVISION
SOURCE=activate()
from player_pins import verify
PINS=verify()
from player_abi import Player,inputs,orders
from player_provenance import begin,finish
from frame_abi import FrameInput,FrameRegisters
from provar_entrada_ia import estado_quadro128,indicadores,comparar_quadro,eventos_referencia,normalizar_eventos
from composicao_entrada_ia import ComposicaoEntrada,RoteiroEntrada
from composicao_quadros_ia import carregar_cenario_exibicao,MSG_LACO
from composicao_encadeada_ia import MemoriaMapaRapida
from frame_differential import static_inputs,OriginalImage
import ambiente_ia_runtime

class Memory:
 def __init__(self,blocks):self.blocks=dict(blocks);self.bases=sorted(self.blocks)
 def read(self,a,n):
  base=self.bases[bisect.bisect_right(self.bases,a)-1];data=self.blocks[base][a-base:a-base+n]
  if len(data)!=n:raise ValueError(hex(a))
  return data
 def u8(self,a):return self.read(a,1)[0]
 def u16(self,a):return int.from_bytes(self.read(a,2),'little')
 def u32(self,a):return int.from_bytes(self.read(a,4),'little')

def canonical_orders(rows):
 return [(o.get('event','SetPlayerOrdre'),o['player'],o['tag'],o.get('word2'),o.get('word4'),o.get('word6'),o.get('word8'),o.get('packet'),o.get('jump_target')) for o in rows]

def proof(probe,library=None,frames=None,python=False,whole=False):
 t=time.monotonic();base=SOURCE/'pesquisas-paralelas/missoes/m3';raw=(base/'entradas'/f'{probe}.json').read_bytes();data=json.loads(raw)
 files={n:(base/'sondas'/probe/n).read_bytes() for n in ('quadros.jsonl.xz','entradas.jsonl.xz','comandos.jsonl.xz','replay.json')}
 if not json.loads(files['replay.json'])['equal']:raise ValueError('Native probe replay not equal')
 rows=lambda n:[json.loads(v) for v in lzma.decompress(files[n]).splitlines() if v]
 native={r['frame']:r for r in rows('quadros.jsonl.xz')};ev_ref=rows('entradas.jsonl.xz');ord_ref=rows('comandos.jsonl.xz')
 cap,state,regs=estado_quadro128();rust=Player(library);identity=begin(rust.path);h=rust.create();image=OriginalImage(ambiente_ia_runtime.EXE,Path(ambiente_ia_runtime.EXE).with_suffix('.SBL'))
 static=static_inputs(image,state);static[0x45ed20]=image.read(0x45ed20,0x45ed20+160)
 rust.load(h,sorted([(a,b) for name,(a,b) in state.items() if name!='native_stack']+list(static.items())))
 full=None
 if whole:
  from player_state_evidence import WholeState
  full=WholeState(probe,state)
 rust.check(rust.lib.rl_avancar_ticks(h,129))
 mirror=None;play_checks=[]
 if int(os.environ.get('RL_COMPARE_PLAY','0')):
  if int(os.environ.get('RL_EXECUTION_MODE','0'))!=2:raise ValueError('Paired play proof requires mode 2')
  mirror=rust.create();rust.load(mirror,sorted([(a,b)for name,(a,b)in state.items()if name!='native_stack']+list(static.items())));rust.execution(mirror,1);rust.check(rust.lib.rl_avancar_ticks(mirror,129))
 _,_,entry,m1=carregar_cenario_exibicao();comp=None;iterator=None
 if python:
  script=RoteiroEntrada(data);comp=ComposicaoEntrada(state,cap,entry,m1,script,inicio=128,alocacoes=cap['allocations'],regs_inicio=regs);iterator=iter(comp.executar(frames or max(native)-128))
 inp=FrameInput(0,0,0,FrameRegisters.from_values({k:int(v,16) for k,v in regs.items()}),(C.c_uint32*3)(0,0,0),(C.c_uint32*4)(*MSG_LACO))
 mirror_inp=FrameInput.from_buffer_copy(bytes(inp))
 schedule={q['frame']:q for q in data['frames']};results=[];stop=None;difference=None;native_events=[];native_orders=[];runtime=0.0
 try:
  for k in range(129,129+(frames or max(native)-128)):
   q=schedule.get(k,{});keys={int(v,0) if isinstance(v,str) else v:int(value,0) if isinstance(value,str) else value for v,value in (q.get('keys') or {}).items()};events=[];py_events=[];py_orders=[]
   for phase in (2,3):
    before=time.perf_counter();code=rust.input(h,phase,inp,cursor=q.get('cursor') if phase==2 else None,messages=q.get('messages',()) if phase==2 else (),keys=keys);runtime+=time.perf_counter()-before
    native_error=rust.error() if code else None
    consumed=rust.consumed(h);events+=consumed
    if mirror is not None:
     mirror_code=rust.input(mirror,phase,mirror_inp,cursor=q.get('cursor') if phase==2 else None,messages=q.get('messages',()) if phase==2 else (),keys=keys)
     mirror_error=rust.error() if mirror_code else None
     mirror_events=rust.consumed(mirror)
     left=consumed if code else [e for e in consumed if e.kind>=7]
     check=dict(frame=k,phase=phase,state_equal=rust.snapshot(h)==rust.snapshot(mirror),registers_equal=bytes(inp)==bytes(mirror_inp),clock_equal=rust.clock(h)==rust.clock(mirror),stop_equal=(code,native_error)==(mirror_code,mirror_error),events_equal=[bytes(e)for e in left]==[bytes(e)for e in mirror_events])
     check['equal']=all(v for key,v in check.items() if key.endswith('_equal'));play_checks.append(check)
     if not check['equal']:difference=dict(frame=k,differences=dict(play_mode=check));break
    py_stop=None
    if iterator is not None:
     py_event_start=len(script.eventos)
     try:r=next(iterator);py_events+=r['eventos'];py_orders+=r['ordens']
     except Exception as e:py_stop=dict(type=type(e).__name__,dependency=str(e),callee=getattr(e,'rotina',None) or getattr(e,'nome',None),address=getattr(e,'sitio',None) or getattr(e,'endereco',None) or getattr(e,'chamada',None))
     if py_stop:
      py_events+=script.eventos[py_event_start:]
      if phase==3:py_orders+=getattr(comp,'ordens_fase',[])
    if code or py_stop:
     stop=dict(frame=k,phase=phase,rust=native_error,python=py_stop,orders_before_stop=orders(events),inputs_before_stop=inputs(events))
     match=re.search(r' at 0x([0-9a-f]+)',native_error or '')
     native_address=int(match[1],16) if match else None
     native_name=(native_error or '').split(' at 0x')[0]
     stop['equal']=bool(code and py_stop and native_address==py_stop['address'] and native_name==py_stop['callee']) if python else None
     if python:
      stop['inputs_equal']=inputs(events)==normalizar_eventos(py_events)
      stop['orders_equal']=canonical_orders(orders(events))==canonical_orders([dict(o,frame=k) for o in py_orders])
      if not all(stop[v] for v in ('equal','inputs_equal','orders_equal')):difference=dict(frame=k,differences=dict(stop_contract=stop))
     break
    if full is not None:
     check=full.compare(('between_frames' if phase==2 else 'frame')+str(k),rust.snapshot(h),static,inp.registers.values())
     if not check['equal']:difference=dict(frame=k,differences=dict(whole_state=check));break
   if stop or difference:break
   actual=indicadores(Memory(rust.snapshot(h)));dif=comparar_quadro(k,actual,native[k]);in_ev=inputs(events);ord_ev=orders(events)
   if in_ev!=eventos_referencia(ev_ref,k):dif['inputs']=dict(rust=in_ev,original=eventos_referencia(ev_ref,k))
   ref_orders=[o for o in ord_ref if o['frame']==k]
   if canonical_orders(ord_ev)!=canonical_orders(ref_orders):dif['orders']=dict(rust=ord_ev,original=ref_orders)
   if comp is not None:
    py=indicadores(MemoriaMapaRapida(comp.mapa));pd=comparar_quadro(k,actual,py)
    if pd:dif['python_indicators']=pd
    if in_ev!=normalizar_eventos(py_events):dif['python_inputs']=dict(rust=in_ev,python=normalizar_eventos(py_events))
    if canonical_orders(ord_ev)!=canonical_orders([dict(o,frame=k) for o in py_orders]):dif['python_orders']=dict(rust=ord_ev,python=py_orders)
   native_events+=in_ev;native_orders+=ord_ev;results.append(dict(frame=k,equal=not dif,indicators=actual))
   if k%250==0:print(probe,k,"equal"if not dif else "different",flush=True)
   if dif:difference=dict(frame=k,differences=dif);break
 finally:
  final_clock=rust.clock(h);rust.free(h)
  if mirror is not None:rust.free(mirror)
 return dict(schema='rising-lands/rust-player-input-proof/1',execution_mode=int(os.environ.get('RL_EXECUTION_MODE','0')),probe=probe,play_comparison=dict(phases=len(play_checks),equal=sum(c['equal']for c in play_checks),checks=play_checks) if mirror is not None else None,provenance=finish(identity,rust.path),whole_state=full.report() if full is not None else None,reference=provenance(),input_sha256=hashlib.sha256(raw).hexdigest(),probe_files_sha256={n:hashlib.sha256(v).hexdigest() for n,v in files.items()},library_sha256=hashlib.sha256(rust.path.read_bytes()).hexdigest(),source_revision=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip(),source_dirty=bool(subprocess.check_output(['git','-C',str(REPO),'status','--porcelain'],text=True)),frames_equal=sum(r['equal'] for r in results),frames_compared=len(results),python_compared=python,first_difference=difference,stop=stop,results=results,orders=native_orders,input_events=len(native_events),native_seconds=runtime,virtual_clock=dict(start_tick=129,end_tick=final_clock[0],milliseconds=final_clock[1],rate=20),seconds=time.monotonic()-t)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--probe',required=True);ap.add_argument('--frames',type=int);ap.add_argument('--library');ap.add_argument('--python',action='store_true');ap.add_argument('--whole-state',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=proof(a.probe,a.library,a.frames,a.python,a.whole_state);p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(r,indent=1,sort_keys=True)+'\n');print(json.dumps({k:r[k] for k in ('probe','frames_equal','python_compared','first_difference','stop','seconds')},indent=1));return int(r['first_difference'] is not None)
if __name__=='__main__':raise SystemExit(main())
