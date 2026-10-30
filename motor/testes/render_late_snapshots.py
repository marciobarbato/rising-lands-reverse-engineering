"""Bounded isolated original late P6/P7 render snapshots; no advancing-world claim."""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain8')
import argparse,hashlib,json,signal,struct,time
from pathlib import Path
from pinned_reference import activate
SOURCE=activate()
from render_probe_proof import Stream
from validar_janelas_api18 import CapturaLimitada,PARTS
from player_provenance import begin,finish

def prove(binary):
 start=time.monotonic();identity=begin(binary);stream=Stream(Path(binary));rows=[];pins={}
 try:
  for name in PARTS['P6']+PARTS['P7']:
   path=SOURCE/'pesquisas-paralelas/graficos-animacao/evidencias'/name;cap=CapturaLimitada(path);pins[name]=cap.sha
   for row in cap.d['rows']:
    memory=cap.memory(row);cache=cap.cache_entry(row);tick=struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0]
    actual=stream.frame(memory,tick,initial=(cap.blob(row['before']),cache),boundaries=row['text_boundaries'])
    check=dict(frame=row['frame'],stop=actual['stop'],reason=actual['reason'],pixels_equal=actual['pixels']==cap.blob(row['after']),calls_equal=actual['calls']==row['blits'],cache_cursor_equal=actual['cache'].proximo==struct.unpack_from('<H',cap.blob(row['exit_dgroup']),0x49a04e-0x494000)[0],text_checked=actual['text_checked'],text_expected=len(row['text_boundaries']))
    check['equal']=not check['stop']and check['pixels_equal']and check['calls_equal']and check['cache_cursor_equal']and check['text_checked']==check['text_expected'];rows.append(check)
    if not check['equal']and sum(not r['equal']for r in rows)<5:print('DIFFERENCE',check,flush=True)
    if len(rows)%100==0:print(len(rows),'snapshots',sum(not r['equal']for r in rows),'differences',flush=True)
 finally:stream.close()
 return dict(schema='rising-lands/rust-late-render-snapshots/1',cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,capture_sha256=pins,provenance=finish(identity,binary),scope='Original render-entry inputs2001–3700. Every snapshot starts from its own native surface/cache; no advancing-world claim. Exact original pixels,raster calls,cache cursor and strictly attested AffText nonexecution. Full cache/effects/Python equality belongs to the advancing proof.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/render_probe_stream');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=prove(a.binary)
 with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
