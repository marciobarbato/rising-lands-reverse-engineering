"""Isolated original render entries, separate from the advancing-world proofs."""
import os,sys
os.environ['RL_REFERENCE_PROFILE']='chain6'
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'motor/testes'))
import hashlib,json,struct,time
from pinned_reference import activate,provenance
SOURCE=activate()
from render_probe_proof import Stream
from validar_sondas_graficos_m3 import CapturaSondaGrafica
from player_provenance import begin,finish

def prove(filename,facades):
 binary=ROOT/'motor/target/release/render_probe_stream';identity=begin(binary);cap=CapturaSondaGrafica(SOURCE/'pesquisas-paralelas/graficos-animacao/evidencias'/filename);stream=Stream(binary);rows=[];start=time.monotonic()
 try:
  for row in cap.d['rows']:
   memory=cap.memory(row);tick=struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0]
   facade=(row['registers']['EAX'],row['registers']['EDX'],row['cell'])if facades else None
   result=stream.frame(memory,tick,initial=(cap.blob(row['before']),cap.cache_entry(row)),boundaries=row.get('text_boundaries',[]),facade=facade)
   effects=[]
   if facades:
    native=cap.blob(row['exit_dgroup']);projected=bytearray(memory.ler_mundo(0x494000,len(native)))
    for name,a,old,new in result['effects']:
     data=bytes.fromhex(new)
     if 0x494000<=a and a+len(data)<=0x523000:projected[a-0x494000:a-0x494000+len(data)]=data
     else:raise ValueError('Unexpected facade output')
    effects=[hex(0x494000+i)for i,(a,b)in enumerate(zip(projected,native))if a!=b]
   check=dict(case=row.get('name'),frame=row.get('frame'),pixels_equal=result['pixels']==cap.blob(row['after']),calls_equal=result['calls']==row['blits'],stop=result['stop'],effects=effects,text_checked=result['text_checked'])
   check['equal']=check['pixels_equal']and check['calls_equal']and not(check['stop']or effects);rows.append(check)
   if not check['equal']:break
 finally:stream.close()
 return dict(schema='rising-lands/native-graphics19-original-entries/1',reference=provenance(),provenance=finish(identity,binary),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),capture=filename,capture_sha256=cap.sha,independent_original_openings=True,cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),rows=rows,seconds=time.monotonic()-start)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--capture',default='camadas-habitadas-api18.json.xz');p.add_argument('--facades',action='store_true');p.add_argument('--output',required=True);a=p.parse_args();r=prove(a.capture,a.facades);Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(bool(r['first_difference']))
