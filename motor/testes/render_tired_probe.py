"""Original P6 snapshots covering Graphics' type9 shifted tired-icon exception."""
import os
os.environ.setdefault('RL_REFERENCE_PROFILE','chain8')
import argparse,hashlib,json,signal,struct,time
from pathlib import Path
from pinned_reference import activate
SOURCE=activate()
from render_probe_proof import Stream
from render_proof import inhabited
from validar_janelas_api18 import CapturaLimitada
from validar_sondas_graficos_m3 import FronteiraTextoGravada
from validar_entrada_m3 import CatalogoRastreado,ArgumentosRasterM3
from render_quadro import renderizar_quadro
from player_provenance import begin,finish

def prove(binary):
 start=time.monotonic();identity=begin(binary);path=SOURCE/'pesquisas-paralelas/graficos-animacao/evidencias/janela-P6-2001-2400-api18.json.xz';cap=CapturaLimitada(path);stream=Stream(Path(binary));catalog=CatalogoRastreado();rows=[]
 try:
  for row in cap.d['rows']:
   if row['frame']not in (2031,2032,2033,2034,2035,2036,2037,2038):continue
   memory=cap.memory(row);cache=cap.cache_entry(row);tick=struct.unpack_from('<I',cap.blob(row['exit_dgroup']),0x4e17b4-0x494000)[0]
   actual=stream.frame(memory,tick,initial=(cap.blob(row['before']),cache),boundaries=row['text_boundaries'])
   with ArgumentosRasterM3(catalog)as raster:
    py=renderizar_quadro(memory,superficie_anterior=cap.blob(row['before']),cache=cache,catalogo=catalog,habitado=lambda i:inhabited(memory,i),hud=True,relogio=lambda:tick,texto=FronteiraTextoGravada(cap,row))
   check=dict(frame=row['frame'],stop=actual['stop'],reason=actual['reason'],python_stop=py.parada,original_pixels_equal=actual['pixels']==cap.blob(row['after']),python_pixels_equal=actual['pixels']==py.pixels,original_calls_equal=actual['calls']==row['blits'],python_calls_equal=actual['calls']==raster.calls,python_effects_equal=actual['effects']==list(py.efeitos),cache_equal=actual['cache']==py.cache)
   check['equal']=not check['stop']and not py.parada and all(check[k]for k in ('original_pixels_equal','python_pixels_equal','original_calls_equal','python_calls_equal','python_effects_equal','cache_equal'));rows.append(check);print(check,flush=True)
 finally:stream.close()
 return dict(schema='rising-lands/rust-shifted-tired-icon-proof/1',cases=len(rows),equal=sum(r['equal']for r in rows),first_difference=next((r for r in rows if not r['equal']),None),results=rows,capture_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),provenance=finish(identity,binary),scope='Eight immutable original P6 render-entry snapshots, not advancing-world proof. Exact pixels,raster calls,Python effects/cache. Original AffText nonexecution remains explicitly attested.',seconds=time.monotonic()-start)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--binary',default='motor/target/release/render_probe_stream');ap.add_argument('--output',required=True);a=ap.parse_args();signal.alarm(1140);r=prove(a.binary)
 with Path(a.output).open('x')as f:json.dump(r,f,indent=2,sort_keys=True);f.write('\n')
 print({k:r[k]for k in ('cases','equal','first_difference','seconds')});raise SystemExit(r['first_difference']is not None)
