"""Original AffGame leaf calls at the first actual probe entry of each previously unproved view origin.

No writes are applied. Save CPU/state/stack, declared host state and DirectDraw surfaces, execute the intact call
to its native caller return, record every DGROUP/CRT/heap difference, then restore the exact entry before replay.
The normal phase must still reproduce the published whole-state and full-surface hashes.
"""
import ast,json,pickle,struct,subprocess,hashlib
from pathlib import Path
import capturar_sondas_graficos_m3 as original
from oraculo_quadro_missao import Isolamento,BancadaCargaMissaoOriginal

sha=lambda b:hashlib.sha256(b).hexdigest()

class IsolamentoOrigensSondas(Isolamento):
    def __init__(self,b,cap,probe,refs,ref):
        super().__init__(b,('AffGame',));self.cap=cap;self.probe=probe;self.refs=refs;self.ref=ref
        raw=subprocess.check_output(['git','show',ref+':pesquisas-paralelas/graficos-animacao/efeitos_logicos_exibicao.py'])
        node=next(n for n in ast.parse(raw).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ORIGENS_PROVADAS' for t in n.targets))
        baseline=ast.literal_eval(node.value.args[0]);self.targets={tuple(r['view_origin']) for r in refs.values()}-baseline
        self.seen=set();self.baseline_sha=sha(raw)

    def executar(self,regs):
        self.cap.resume_entry=True
        b=self.b;cpu=b.cpu;m=cpu.mem_read;origin=struct.unpack('<2H',m(0x508720,4))
        if origin not in self.targets or origin in self.seen:return
        self.seen.add(origin);frame=self.cap.phase_frame
        if frame is None:raise RuntimeError('Origin isolation outside an attested drawing phase')
        context,blocks=self._salvar();ret=struct.unpack('<I',m(regs['ESP'],4))[0]
        host=original.seg._python(b);host.pop('isolamento');host=pickle.dumps(host,protocol=4)
        dd=b.directdraw;surface_base=dd.base_superficies;surfaces=bytes(m(surface_base,dd.tamanho_superficies))
        pending,phase=self.cap.current,self.cap.phase_frame;self.cap.current=None;self.cap.phase_frame=None
        self.ativo=False
        hook=cpu.hook_add(original.unicorn.UC_HOOK_CODE,b._parar_se_pedido,begin=ret,end=ret)
        cpu.ctl_flush_tb()
        try:
            b._retomando={regs['EIP']}
            out=BancadaCargaMissaoOriginal._correr(b,'isolated-origin',regs['EIP'],{},(ret,),retomar=True)
            after=b.imagem();changed={}
            for name,(base,data) in after.items():
                old=blocks[name][1]
                if data==old:continue
                rows=[(hex(base+i),a,z) for i,(a,z) in enumerate(zip(old,data)) if a!=z]
                changed[name]=rows if name in ('dgroup','crt_thread_data') else dict(bytes=len(rows),first=rows[0][0],before_sha256=sha(old),after_sha256=sha(data))
            surface=sha(dd.pixels('offscreen'))
            self.registros.append(dict(probe=self.probe,frame=frame,origin=list(origin),routine='AffGame',entry='0x417698',
                caller_return=hex(ret),entry_registers={k:hex(v) for k,v in regs.items()},exit_registers={k:hex(v) for k,v in out.items()},
                declared_writes=[],returned=out['EIP']==ret,changed=changed,entry_state_sha256=b.resumo_imagem({k:v for k,v in blocks.items() if k!='native_stack'})['sha256'],
                surface_sha256=surface,published_phase_sha256=self.refs[frame]['surfaces_between']['offscreen'],
                original_code_sha256=b.sha256_codigo()))
            if out['EIP']!=ret or surface!=self.refs[frame]['surfaces_between']['offscreen']:raise RuntimeError('Isolated original does not reproduce the probe surface')
        finally:
            cpu.hook_del(hook);self._restaurar(context,blocks);cpu.mem_write(surface_base,surfaces)
            for name,value in pickle.loads(host).items():
                if name in original.seg.COM_CPU:
                    target=getattr(b,name)
                    for key,item in value.items():vars(target)[key]=original.seg._no_lugar(vars(target).get(key),item)
                else:vars(b)[name]=original.seg._no_lugar(vars(b).get(name),value)
            self.cap.current=pending;self.cap.phase_frame=phase;self.ativo=True;cpu.ctl_flush_tb()
        print(self.probe,frame,'isolated original origin',origin,'returned',flush=True)

    def report(self):
        return dict(schema='rising-lands/probe-origin-isolation/1',method=__doc__,probe=self.probe,probe_ref=self.ref,
            executable_sha256=__import__('emulador').HASH_ORIGINAL,source_sha256=sha(Path(__file__).read_bytes()),
            baseline_provider_sha256=self.baseline_sha,targets=sorted(map(list,self.targets)),records=self.registros)
