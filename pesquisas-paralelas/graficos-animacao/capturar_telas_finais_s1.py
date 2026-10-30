"""Isolate real S1 MenuInit13/MenuInit11/PartieGetResultat calls without changing game state.

Requires a native scripted S1 checkpoint at frame17000 or later. The full prefix belongs on the Mac mini.
At each actual call, save CPU, stack, all native blocks, host state and DirectDraw pixels. Execute the original
to its real caller return; record entry/exit blocks, surfaces and raster arguments; restore the exact entry.
The ordinary call must then produce precisely the isolated surface. No menu mode or victory byte is injected.
"""
import argparse,json,lzma,pickle,struct,time
from pathlib import Path
from capturar_escritas_cave_m3 import original,REF,sha
from oraculo_quadro_missao import Isolamento,BancadaCargaMissaoOriginal

class TelasS1(Isolamento):
    def __init__(self,b):
        super().__init__(b,('MenuInit','PartieGetResultat'));self.frame=None;self.pending=[]
        self.cap=object.__new__(original.CapturadorSondasGraficos);self.cap.b=b;self.cap.blobs={};self.cap.current=None
        for pc in original.BLITS:b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,self.cap.blit,begin=pc,end=pc)
        b.cpu.hook_add(original.unicorn.UC_HOOK_BLOCK,self.cap.text,begin=b.sym['AffText'],end=b.sym['AffText'])

    def executar(self,regs):
        b=self.b;cpu=b.cpu;name=self.entradas[regs['EIP']]
        if name=='MenuInit' and not ({regs['EAX']&255,regs['EDX']&255}&{0x11,0x13}):return
        ctx,blocks=self._salvar();ret=struct.unpack('<I',cpu.mem_read(regs['ESP'],4))[0]
        host=original.seg._python(b);host.pop('isolamento');host=pickle.dumps(host,protocol=4)
        dd=b.directdraw;surfaces=bytes(cpu.mem_read(dd.base_superficies,dd.tamanho_superficies))
        cap=self.cap;row=dict(frame=self.frame,phase=b.fase,routine=name,declared_writes=[],entry_registers=regs,
            before=cap.blob(dd.pixels('offscreen')),entry_blocks={n:[hex(a),cap.blob(v)] for n,(a,v) in blocks.items()},
            blits=[],text_boundaries=[])
        self.ativo=False;cap.current=row
        hook=cpu.hook_add(original.unicorn.UC_HOOK_CODE,b._parar_se_pedido,begin=ret,end=ret);cpu.ctl_flush_tb()
        try:
            b._retomando={regs['EIP']};out=BancadaCargaMissaoOriginal._correr(b,'isolated-S1-screen',regs['EIP'],{},(ret,),retomar=True)
            row.update(exit_registers=out,returned=out['EIP']==ret,after=cap.blob(dd.pixels('offscreen')),
                exit_blocks={n:[hex(a),cap.blob(v)] for n,(a,v) in b.imagem().items()})
            assert row['returned'];self.registros.append(row)
        finally:
            cap.current=None;cpu.hook_del(hook);self._restaurar(ctx,blocks);cpu.mem_write(dd.base_superficies,surfaces)
            for name,value in pickle.loads(host).items():
                if name in original.seg.COM_CPU:
                    target=getattr(b,name)
                    for key,item in value.items():vars(target)[key]=original.seg._no_lugar(vars(target).get(key),item)
                else:vars(b)[name]=original.seg._no_lugar(vars(b).get(name),value)
            self.ativo=True;cpu.ctl_flush_tb()
        def ordinary(c,pc,size,user):
            row['ordinary_surface_sha256']=sha(dd.pixels('offscreen'));row['surface_equal']=row['ordinary_surface_sha256']==row['after']
            assert row['surface_equal'];c.hook_del(normal_hook)
        normal_hook=cpu.hook_add(original.unicorn.UC_HOOK_CODE,ordinary,begin=ret,end=ret)
        print('S1 isolated',row['frame'],row['routine'],'returned',flush=True)

def main(a):
    original.REF=a.ref;m=original.modulo_entrada();b,_,start=m.abrir(a.start,Path(a.snapshot))
    if not 17000<=start<a.to<=17050:raise ValueError('Requires real S1 checkpoint17000..17049; stop<=17050')
    raw=original.remoto(original.PROBE_ROOT+'entradas/S1.json');b.roteiro.quadros=m.carregar_entrada(json.loads(raw))[0]
    iso=TelasS1(b);iso.instalar();checks=[];t=time.monotonic()
    for k in range(start+1,a.to+1):
        iso.frame=k;b.roteiro.iniciar_quadro(k);b.executar_entre_quadros(300,k)
        between=sha(b.directdraw.pixels('offscreen'));b.executar_quadro(600,k)
        checks.append(dict(frame=k,between_surface=between,frame_surface=sha(b.directdraw.pixels('offscreen')),
            whole_state_sha256=b.resumo_imagem(b.imagem())['sha256']))
        b.roteiro.eventos.clear()
        if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
    assert iso.registros and all(r.get('surface_equal') for r in iso.registros)
    result=dict(schema='rising-lands/s1-native-isolated-screens/1',method=__doc__,probe_ref=a.ref,frames=[start+1,a.to],
        executable_sha256=__import__('emulador').HASH_ORIGINAL,code_sha256=b.sha256_codigo(),
        source_sha256=sha(Path(__file__).read_bytes()),snapshot_sha256=sha(Path(a.snapshot).read_bytes()),input_sha256=sha(raw),
        rows=iso.registros,blobs=iso.cap.blobs,checks=checks,elapsed_seconds=time.monotonic()-t)
    Path(a.output).write_bytes(lzma.compress(json.dumps(result).encode()));print('native isolated screens',len(iso.registros),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--ref',default=REF);p.add_argument('--to',type=int,default=17050);p.add_argument('--output',required=True);main(p.parse_args())
