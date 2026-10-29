"""All 600 original Graphics 1.7 construction calls; no glyph qualification."""
import argparse,json,struct,time
from pathlib import Path
from render_probe_proof import Stream,sha
from render_abi import *
from render_proof import renderer_pins
from frame_long_differential import source_hashes,metadata,write_json
from validar_sondas_graficos_m3 import CapturaSondaGrafica

def prove(binary=None,limit=None):
 renderer_pins();cap=CapturaSondaGrafica(RAIZ/'evidencias/matriz-cave-toda-vida-api17.json.xz');stream=Stream(binary or ROOT/'motor/target/release/render_probe_stream');rows=[];t0=time.monotonic()
 try:
  for row in cap.d['rows'][:limit]:
   m=cap.memory(row);r=stream.frame(m,0xffffffff,initial=(cap.blob(row['before']),cap.cache_entry(row)),facade=(row['registers']['EAX'],row['registers']['EDX'],row['cell']))
   dg=bytearray(m.ler_mundo(0x494000,len(cap.blob(row['exit_dgroup']))))
   for name,a,old,new in r['effects']:
    value=bytes.fromhex(new);dg[a-0x494000:a-0x494000+len(value)]=value
   item=dict(case=row['name'],stop=r['stop'],pixels_equal=r['pixels']==cap.blob(row['after']),arguments_equal=r['calls']==row['blits'],dgroup_equal=dg==cap.blob(row['exit_dgroup']),cache_unchanged=r['cache']==cap.cache_entry(row))
   rows.append(item)
   if not all(item[k] for k in ('pixels_equal','arguments_equal','dgroup_equal','cache_unchanged')) or item['stop']:print('DIFFERENCE',item,flush=True);break
 finally:stream.close()
 return dict(schema='rising-lands/rust-graphics17-facade-matrix/1',capture_sha256=cap.sha,cases=len(rows),equal=sum(not r['stop'] and all(r[k] for k in ('pixels_equal','arguments_equal','dgroup_equal','cache_unchanged')) for r in rows),wall_seconds=time.monotonic()-t0,rows=rows)

def main():
 p=argparse.ArgumentParser();p.add_argument('--binary');p.add_argument('--limit',type=int);p.add_argument('--output',required=True);a=p.parse_args()
 if Path(a.output).exists():raise SystemExit('Refusing overwrite')
 before=source_hashes();r=prove(a.binary,a.limit);r.update(metadata(),source_sha256=before,sources_unchanged=before==source_hashes(),reference_pins=renderer_pins(),binary_sha256=sha(Path(a.binary or ROOT/'motor/target/release/render_probe_stream').read_bytes()));write_json(a.output,r);print({k:v for k,v in r.items() if k not in ('rows','source_sha256','reference_pins')});return r['equal']!=r['cases']
if __name__=='__main__':raise SystemExit(main())
