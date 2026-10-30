"""Original-only P7 real-state origin recordings, pinned to integrated Missions probes.

Every invocation replays at most 750 frames, retains an 18-minute checkpoint budget and verifies both native phase
surfaces and the complete end-frame state against the published probe. Hooks observe; native bytes are unchanged.
"""
import argparse,json,lzma,struct,time,subprocess
from pathlib import Path
import capturar_sondas_graficos_m3 as original

AQUI=original.AQUI
REF='fd56f69'
sha=original.sha

class CapturadorPausavel(original.CapturadorSondasGraficos):
    resume_entry=False
    def entry(self,c,a,n,user):
        if self.phase_frame is None:return
        if self.resume_entry:
            self.resume_entry=False
            if self.current is None or self.current['frame']!=self.phase_frame:raise RuntimeError('Missing paused AffGame entry')
            return
        return super().entry(c,a,n,user)

def main(a):
    original.REF=REF
    m=original.modulo_entrada();t=time.monotonic()
    b,_,start=m.abrir(a.start,Path(a.resume) if a.resume else None)
    raw=original.remoto(original.PROBE_ROOT+'entradas/'+a.probe+'.json');schedule=json.loads(raw)
    frames,end=m.carregar_entrada(schedule);b.roteiro.quadros=frames;end=min(end,a.to)
    if not 0<end-start<=750:raise ValueError('Each window must contain 1..750 native frames')
    raw_ref=original.remoto(original.PROBE_ROOT+'sondas/'+a.probe+'/quadros.jsonl.xz')
    refs={r['frame']:r for r in map(json.loads,lzma.decompress(raw_ref).splitlines())}
    if start!=128 and b.resumo_imagem(b.imagem())['sha256']!=refs[start]['state_sha256']:
        raise RuntimeError('Opening checkpoint does not match this probe prefix')
    cap=CapturadorPausavel(b);checks=[];boundaries=[];pointer_reads=[]
    from isolar_origens_sondas_graficas import IsolamentoOrigensSondas
    iso=IsolamentoOrigensSondas(b,cap,a.probe,refs,REF);iso.instalar()
    x86,uc=original.x86,original.unicorn
    def text_boundary(cpu,address,size,_):
        if cap.phase_frame is None:return
        boundaries.append(dict(frame=cap.phase_frame,phase=b.fase,address=hex(address),
            eax=hex(cpu.reg_read(x86.UC_X86_REG_EAX)),routine='TextGetMessage',declared_return=0))
    def text_pointer(cpu,access,address,size,value,_):
        if cap.phase_frame is not None:pointer_reads.append(dict(frame=cap.phase_frame,phase=b.fase,address=hex(address),
            size=size,eip=hex(cpu.reg_read(x86.UC_X86_REG_EIP))))
    hooks=[b.cpu.hook_add(uc.UC_HOOK_BLOCK,text_boundary,begin=b.sym['TextGetMessage'],end=b.sym['TextGetMessage']),
           b.cpu.hook_add(uc.UC_HOOK_MEM_READ,text_pointer,begin=0x5099a4,end=0x5099a7)]
    b.cpu.ctl_flush_tb();requested=end;status='complete'
    for k in range(start+1,end+1):
        b.roteiro.iniciar_quadro(k);cap.phase_frame=k;b.executar_entre_quadros(300,k)
        expected=refs[k]['surfaces_between']['offscreen'];actual=sha(b.directdraw.pixels('offscreen'))
        if actual!=expected:raise RuntimeError(f'{a.probe} {k}: between-frame surface differs')
        drawn=cap.rows[-1] if cap.rows and cap.rows[-1]['frame']==k else None
        if drawn:
            if drawn['after']!=expected:raise RuntimeError('AffGame end differs from published phase end')
            drawn['probe_surface_sha256']=expected
        b.executar_quadro(600,k)
        if sha(b.directdraw.pixels('offscreen'))!=refs[k]['surfaces_frame']['offscreen']:raise RuntimeError(f'{k}: frame surface differs')
        if b.resumo_imagem(b.imagem())['sha256']!=refs[k]['state_sha256']:raise RuntimeError(f'{k}: whole-state differs')
        checks.append(dict(frame=k,drawn=bool(drawn),surface_equal=True,state_equal=True));b.roteiro.eventos.clear()
        if k%50==0:print(a.probe,k,'native surface/state equal',flush=True)
        if k in a.checkpoint:
            path=Path(a.start)/f'{a.probe}-{k:05d}.pickle'
            if path.exists():raise FileExistsError(path)
            b.isolamento=None
            try:original.seg.salvar(b,path,k)
            finally:b.isolamento=iso
        if time.monotonic()-t>1080:status='budget_stop';end=k;break
    cap.phase_frame=None;cap.detach()
    Path(a.output+'.origins.json').write_text(json.dumps(iso.report(),indent=1)+'\n')
    b.isolamento=None  # Capturing hooks are not part of a resumable native checkpoint.
    for hook in hooks:b.cpu.hook_del(hook)
    checkpoint=Path(a.start)/f'{a.probe}-{end:05d}.pickle'
    if checkpoint.exists():digest=sha(checkpoint.read_bytes())
    else:digest=original.seg.salvar(b,checkpoint,end)
    result=dict(schema='rising-lands/m3-probe-render-native/1',method=__doc__,probe=a.probe,probe_ref=REF,
        frames=[start+1,end],input_sha256=sha(raw),probe_records_sha256=sha(raw_ref),executable_sha256=__import__('emulador').HASH_ORIGINAL,
        source_sha256=sha(Path(__file__).read_bytes()),recording_helper_sha256=sha(Path(original.__file__).read_bytes()),
        producing_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),status=status,requested_stop=requested,
        snapshot=dict(path=str(checkpoint),sha256=digest),elapsed_seconds=round(time.monotonic()-t,3),checks=checks,
        text_get_message_boundaries=boundaries,text_pointer_native_reads=pointer_reads,rows=cap.rows,blobs=cap.blobs,code_sha256=b.sha256_codigo())
    raw=json.dumps(result).encode();compressed=lzma.compress(raw,preset=6);Path(a.output).write_bytes(compressed)
    Path(a.output+'.manifest.json').write_text(json.dumps(dict(raw_sha256=sha(raw),compressed_sha256=sha(compressed),
        **{k:v for k,v in result.items() if k not in ('checks','rows','blobs','method','text_get_message_boundaries','text_pointer_native_reads')}),indent=1)+'\n')
    print(json.dumps(dict(probe=a.probe,frames=result['frames'],status=status,seconds=result['elapsed_seconds'],
        drawn=len(cap.rows),snapshot=result['snapshot'],text_boundaries=len(boundaries),text_pointer_reads=len(pointer_reads))),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--resume');p.add_argument('--probe',choices=('P7',),required=True)
    p.add_argument('--to',type=int,required=True);p.add_argument('--checkpoint',type=int,action='append',default=[]);p.add_argument('--output',required=True)
    main(p.parse_args())
