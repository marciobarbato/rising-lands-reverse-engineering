"""M3 pass-2 evidence reader and exact per-phase comparison under its published mask."""
import hashlib,json,lzma
from pinned_reference import source_root
from frame_evidence import (_dados,MascaraEnderecos,fases_referencia,resumo_estado,resumos_mascarados,comparar_estado)

class WholeState:
 def __init__(self,probe,start):
  root=source_root();base=root/'pesquisas-paralelas/missoes/m3/sondas'/probe
  self.manifest=json.loads((base/'captura-janela.manifest.json').read_bytes());maskdoc=json.loads((base/'mascara-janela.json').read_bytes())
  policy=root/maskdoc['window_policy']['path']
  if hashlib.sha256(policy.read_bytes()).hexdigest()!=maskdoc['window_policy']['sha256'] or not maskdoc['window_policy']['passed']:raise ValueError('M3 comparison policy identity')
  if len(self.manifest['parts'])!=1:raise ValueError('M3 capture requires an explicit segmented reader extension')
  meta=self.manifest['parts'][0];raw=(root/meta['artifact']).read_bytes()
  if len(raw)!=meta['compressed_bytes'] or hashlib.sha256(raw).hexdigest()!=meta['compressed_sha256']:raise ValueError('M3 compressed part identity')
  raw=lzma.decompress(raw)
  if len(raw)!=meta['raw_bytes'] or hashlib.sha256(raw).hexdigest()!=meta['raw_sha256']:raise ValueError('M3 raw part identity')
  part=json.loads(raw)
  if part['original_sha256']!='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb' or part['translation_executed']:raise ValueError('M3 original-only capture identity')
  if part['mask']['sha256']!=hashlib.sha256((base/'mascara-janela.json').read_bytes()).hexdigest():raise ValueError('M3 mask identity')
  self.mask=MascaraEnderecos(maskdoc['cumulative']['exclusion_mask']);self.published_mask=maskdoc
  opened=part['opening_state'];state={n:(int(b['base'],16),_dados(b)) for n,b in opened['full_state'].items()}
  compared,masked=resumos_mascarados(self.mask,state)
  if resumo_estado(state)!=opened['summary'] or compared!=opened['compared_summary'] or masked!=opened['masked_sha256']:raise ValueError('M3 opening integrity')
  if {n:v for n,v in start.items() if n!='native_stack'}!=state:raise ValueError('M3 opening differs from accepted frame128; no later original-state reload permitted')
  self.iterator=iter(fases_referencia(part,state,self.mask));self.results=[];self.meta=meta;self.allocated=0
 def compare(self,name,snapshot,static,registers):
  phase,expected,integrity=next(self.iterator)
  if phase['phase']!=name:raise ValueError('M3 phase order')
  if any(snapshot.get(a)!=b for a,b in static.items()):raise ValueError('Original static input table mutated')
  names={a:n for n,(a,b) in expected.items()};actual={names.get(a,'rust_extra_'+hex(a)):(a,b) for a,b in snapshot.items() if a not in static}
  result=comparar_estado(self.mask,actual,expected)
  expected_regs=phase['exit']['registers']
  fields=('EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP') if name.startswith('between') else ('EBX','ECX','EDX','ESI','EDI','EBP','ESP')
  register_diff={k:[registers[k],int(expected_regs[k],16)] for k in fields if registers[k]!=int(expected_regs[k],16)}
  result.update(phase=name,integrity=integrity,allocations_created=phase['allocations_created'],registers_equal=not register_diff,register_differences=register_diff,not_modeled_registers=[] if name.startswith('between') else ['EAX'])
  result['equal']=result['equal'] and not register_diff
  if phase['state_delta'].get('allocated') or phase['state_delta'].get('released'):raise ValueError('M3 allocation delta requires explicit support')
  if phase['allocations_created']!=0:raise ValueError('M3 allocation domain requires explicit native allocator support')
  self.results.append(result);return result
 def report(self):
  return dict(schema='rising-lands/rust-m3-whole-state-proof/1',phases_equal=sum(r['equal'] for r in self.results),phases_compared=len(self.results),phases_requested=self.meta['phases'],mask_bytes=self.mask.bytes,compared_bytes_per_phase=sorted({r['compared_bytes'] for r in self.results}),part_compressed_sha256=self.meta['compressed_sha256'],part_raw_sha256=self.meta['raw_sha256'],allocation_domain='No allocation/free or binding changes in the published windows; all block identities and byte lengths compared.',results=self.results)
