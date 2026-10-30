"""Original-only S1 raster/text attestation on replay-checked native segments.

No Rust or Python game translation runs here. Immutable entry_roteirizada and
Graphics observer sources are loaded from the chain8 Git-object snapshot.
Only hashes and raster/text arguments are retained, never an invented glyph.
"""
import argparse,hashlib,json,lzma,os,signal,subprocess,sys,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo');ap.add_argument('--start',required=True);ap.add_argument('--resume');ap.add_argument('--to',required=True,type=int);ap.add_argument('--output',required=True);a=ap.parse_args()
signal.alarm(1140)
os.environ['RL_REFERENCE_PROFILE']='chain8'
import pinned_reference as pin
if a.repo:pin.REPO=Path(a.repo).resolve()
root=pin.activate();sys.path.insert(0,str(root/'pesquisas-paralelas/graficos-animacao'))
import capturar_sondas_graficos_m3 as original
original.REF=pin.CHAIN8_REVISION
original.remoto=lambda p:pin.git('show',pin.CHAIN8_REVISION+':'+p)
m=original.modulo_entrada();start=time.monotonic();b,_,opening=m.abrir(a.start,Path(a.resume)if a.resume else None)
if not 0<a.to-opening<=750:raise ValueError('Native segment must contain 1..750 frames')
base=root/'pesquisas-paralelas/missoes/m3';script=(base/'entradas/S1.json').read_bytes();refs_raw=(base/'sondas/S1/quadros.jsonl.xz').read_bytes();refs={r['frame']:r for r in map(json.loads,lzma.decompress(refs_raw).splitlines())}
b.roteiro.quadros,_=m.carregar_entrada(json.loads(script))
opening_hash=b.resumo_imagem(b.imagem())['sha256']
if opening!=128 and opening_hash!=refs[opening]['state_sha256']:raise ValueError('Native opening differs from committed trajectory')
class Compact(original.CapturadorSondasGraficos):
 def blob(self,data):return original.sha(data)
 def entry(self,c,address,size,_):
  if self.phase_frame is None:return
  if self.current is not None:raise ValueError('Nested original AffGame')
  self.current=dict(frame=self.phase_frame,phase=b.fase,before=self.blob(b.directdraw.pixels('offscreen')),blits=[],text_boundaries=[])
 def end(self,c,address,size,_):
  if self.current is not None:
   self.current['after']=self.blob(b.directdraw.pixels('offscreen'));self.rows.append(self.current);self.current=None
cap=Compact(b);checks=[]
try:
 for k in range(opening+1,a.to+1):
  b.roteiro.iniciar_quadro(k);cap.phase_frame=k;b.executar_entre_quadros(300,k)
  between=original.sha(b.directdraw.pixels('offscreen'))
  b.executar_quadro(600,k);after=original.sha(b.directdraw.pixels('offscreen'));state=b.resumo_imagem(b.imagem())['sha256']
  if between!=refs[k]['surfaces_between']['offscreen']or after!=refs[k]['surfaces_frame']['offscreen']or state!=refs[k]['state_sha256']:raise ValueError(('Native S1 replay differs',k))
  if len(cap.rows)!=k-opening or cap.rows[-1]['after']!=between:raise ValueError('Expected exactly one complete AffGame per frame')
  checks.append(dict(frame=k,state_sha256=state,between_sha256=between,frame_sha256=after,equal=True));b.roteiro.eventos.clear()
  if k%100==0:print(k,'original state/surfaces equal',flush=True)
finally:cap.detach()
report=dict(schema='rising-lands/original-s1-render-attestation/1',translation_executed=False,reference=pin.provenance(),original_sha256=__import__('emulador').HASH_ORIGINAL,input_sha256=original.sha(script),records_sha256=original.sha(refs_raw),opening_frame=opening,opening_state_sha256=opening_hash,snapshot_sha256=original.sha(Path(a.resume).read_bytes())if a.resume else None,frames=[opening+1,a.to],rows=cap.rows,checks=checks,observer_sha256=original.sha(Path(original.__file__).read_bytes()),harness_sha256=original.sha(Path(__file__).read_bytes()),seconds=time.monotonic()-start)
with Path(a.output).open('xb')as f:f.write(lzma.compress((json.dumps(report,sort_keys=True)+'\n').encode()))
print({k:report[k]for k in ('frames','seconds')},flush=True)
