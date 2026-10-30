"""Release play-mode scripted probe timing; no audit/export/hash work in the timed loop."""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain8')
import argparse,ctypes as C,hashlib,json,time,statistics,signal
from pathlib import Path
from player_proof import Player,FrameInput,FrameRegisters,estado_quadro128,static_inputs,OriginalImage,ambiente_ia_runtime,SOURCE
from player_provenance import begin,finish

def run(probe,frames,library):
 rust=Player(library);identity=begin(rust.path);_,state,regs=estado_quadro128();h=rust.create()
 image=OriginalImage(ambiente_ia_runtime.EXE,Path(ambiente_ia_runtime.EXE).with_suffix('.SBL'));static=static_inputs(image,state);static[0x45ed20]=image.read(0x45ed20,0x45edc0)
 rust.load(h,sorted([(a,b)for n,(a,b)in state.items()if n!='native_stack']+list(static.items())));rust.execution(h,1);rust.check(rust.lib.rl_avancar_ticks(h,129))
 inp=FrameInput(0,0,0,FrameRegisters.from_values({k:int(v,16)for k,v in regs.items()}),(C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
 script=(SOURCE/'pesquisas-paralelas/missoes/m3/entradas'/f'{probe}.json').read_bytes();schedule={q['frame']:q for q in json.loads(script)['frames']};values=[];stop=None
 try:
  for k in range(129,129+frames):
   q=schedule.get(k,{});keys={int(v,0)if isinstance(v,str)else v:int(value,0)if isinstance(value,str)else value for v,value in(q.get('keys')or{}).items()}
   start=time.perf_counter();code=rust.input(h,2,inp,cursor=q.get('cursor'),messages=q.get('messages',()),keys=keys)
   if not code:code=rust.input(h,3,inp,keys=keys)
   elapsed=time.perf_counter()-start
   if code:stop=dict(frame=k,error=rust.error());break
   values.append(elapsed)
  clock=rust.clock(h);snapshot=rust.snapshot(h);digest=hashlib.sha256()
  for a,b in sorted(snapshot.items()):digest.update(a.to_bytes(4,'little')+len(b).to_bytes(4,'little')+b)
 finally:rust.free(h)
 ordered=sorted(values)
 return dict(schema='rising-lands/rust-scripted-play-benchmark/1',probe=probe,frames=len(values),requested=frames,stop=stop,execution_mode=1,logic_mean_ms=1000*statistics.mean(values),p99_ms=1000*ordered[min(len(ordered)-1,int(len(ordered)*.99))],max_ms=1000*max(values),terminal_projection_sha256=digest.hexdigest(),clock=clock,input_sha256=hashlib.sha256(script).hexdigest(),provenance=finish(identity,rust.path),excludes='Initialization, proof, snapshots, hashing, rendering and presentation; includes Python ctypes input packing and both logic calls')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--probe',default='P6');ap.add_argument('--frames',type=int,default=2272);ap.add_argument('--library',default='motor/target/release/librising_engine.dylib');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=run(a.probe,a.frames,a.library);p=Path(a.output)
 with p.open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('probe','frames','logic_mean_ms','p99_ms','max_ms','stop')});raise SystemExit(bool(r['stop'])or r['logic_mean_ms']>4)
