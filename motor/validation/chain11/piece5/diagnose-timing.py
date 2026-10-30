import os,sys,time,gc,json,statistics
from pathlib import Path
os.environ['RL_REFERENCE_PROFILE']='chain11';sys.path.insert(0,'motor/testes')
import probe_benchmark as bench
from player_proof import indicadores,Memory
root=Path('.local/chain11');native=json.loads((root/'S1-native.json').read_text());real_wall=time.perf_counter;real_cpu=time.thread_time;records=[];events=[];pending=None

def observe_gc(phase,info):events.append(dict(phase=phase,generation=info['generation'],wall=real_wall(),frame=129+len(records)))
def timer():
 global pending
 wall=real_wall();cpu=real_cpu()
 if pending is None:pending=(wall,cpu,len(events))
 else:
  start,cpu_start,at=pending;records.append(dict(frame=129+len(records),wall_ms=1000*(wall-start),thread_cpu_ms=1000*(cpu-cpu_start),gc_events=events[at:]));pending=None
 return wall
original_snapshot=bench.Player.snapshot;terminal=[]
def snapshot(self,h):
 blocks=original_snapshot(self,h);terminal.append(indicadores(Memory(blocks)));return blocks
bench.Player.snapshot=snapshot;gc.callbacks.append(observe_gc);bench.time.perf_counter=timer
try:diagnostic=bench.run('S1',10672,'motor/target/release/librising_engine.dylib')
finally:bench.time.perf_counter=real_wall;gc.callbacks.remove(observe_gc);bench.Player.snapshot=original_snapshot
assert len(records)==10672 and pending is None
assert terminal[-1]==native['results'][-1]['indicators']
(root/'timing-S1-diagnostic.json').write_text(json.dumps(diagnostic,indent=2,sort_keys=True)+'\n')
report=dict(schema='rising-lands/s1-timing-diagnostic/1',scope='Same play benchmark with wall/thread CPU paired readings and Python GC event observations. Instrumentation is confined to this diagnostic; native source and library unchanged.',terminal_indicators_equal=True,worst=sorted(records,key=lambda r:r['wall_ms'],reverse=True)[:20],gc_events=events,frames=records)
(root/'timing-diagnostic.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('Diagnostic:',{k:diagnostic[k]for k in ('logic_mean_ms','p99_ms','max_ms')},'worst:',report['worst'][0],flush=True)
assert diagnostic['terminal_projection_sha256']==json.loads((root/'timing-S1-extended.json').read_text())['terminal_projection_sha256']
