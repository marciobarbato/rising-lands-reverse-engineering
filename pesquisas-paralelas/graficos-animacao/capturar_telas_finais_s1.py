"""Isolate real S1 MenuInit13/MenuInit11/PartieGetResultat calls without changing game state.

Requires a native scripted S1 checkpoint at frame16933..17031 (frame17000 recommended). The full prefix belongs on the Mac mini.
At each actual call, save CPU, stack, all native blocks, host state and DirectDraw pixels. Execute the original
to its real caller return; record entry/exit blocks, surfaces and raster arguments; restore the exact entry.
The ordinary call must then produce precisely the isolated surface. No menu mode or victory byte is injected.
"""
import argparse,json,lzma,pickle,struct,time
from pathlib import Path
from capturar_escritas_cave_m3 import original,REF,sha
from oraculo_quadro_missao import Isolamento,BancadaCargaMissaoOriginal

class CapturaTextoTela(original.CapturadorSondasGraficos):
    def text(self,c,address,size,user):
        if self.current is None:return
        r=lambda k:c.reg_read(getattr(original.x86,'UC_X86_REG_'+k))&0xffffffff
        ptr=struct.unpack('<I',self.read(r('ESP')+4,4))[0];data=bytearray();error=None
        try:
            for i in range(65536):
                value=self.read(ptr+i,1)[0]
                if not value:break
                data.append(value)
            else:raise ValueError('No terminator within65536 bytes')
        except Exception as problem:error=f'{type(problem).__name__}: {problem}'
        # An opaque argument is retained explicitly; it never becomes an invented empty string or glyph default.
        self.current['text_boundaries'].append(dict(text_pointer=hex(ptr),text_hex=bytes(data).hex() if error is None else None,
            text_read_stop=error,registers={k:hex(r(k)) for k in ('EAX','EBX','ECX','EDX','ESI','EDI')},
            stack=self.read(r('ESP'),24).hex(),surface_before=self.blob(self.b.directdraw.pixels('offscreen')),
            blits_before=len(self.current['blits']),address=hex(address)))

class TelasS1(Isolamento):
    def __init__(self,b):
        super().__init__(b,('MenuInit','PartieGetResultat','AffObjectif'));self.frame=None;self.pending=[]
        self.cap=object.__new__(CapturaTextoTela);self.cap.b=b;self.cap.blobs={};self.cap.current=None
        for pc in original.BLITS:b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,self.cap.blit,begin=pc,end=pc)
        b.cpu.hook_add(original.unicorn.UC_HOOK_BLOCK,self.cap.text,begin=b.sym['AffText'],end=b.sym['AffText'])

    def metadata(self,blocks):
        return {n:dict(base=hex(a),bytes=len(v),sha256=sha(v)) for n,(a,v) in blocks.items()}

    def inputs(self,blocks):
        """Only bounded render-state regions are exported; complete native asset banks stay on original media."""
        b=self.b;cap=self.cap;m=b.cpu.mem_read
        regions=dict(dgroup=(0x494000,0x8f000),crt_thread_data=(0x3400000,4096))
        regions.update({name:(int.from_bytes(m(slot,4),'little'),size) for name,slot,size in original.BLOCOS})
        available={};missing=[]
        for name,(base,size) in regions.items():
            block=next((v[base-a:base-a+size] for a,v in blocks.values() if a<=base and base+size<=a+len(v)),None)
            if block is None:missing.append(name)
            else:available[name]=[hex(base),cap.blob(block)]
        return dict(regions=available,unavailable_regions=missing)

    def executar(self,regs):
        b=self.b;cpu=b.cpu;name=self.entradas[regs['EIP']]
        if name=='MenuInit' and not ({regs['EAX']&255,regs['EDX']&255}&{0x11,0x13}):return
        ctx,blocks=self._salvar();ret=struct.unpack('<I',cpu.mem_read(regs['ESP'],4))[0]
        host=original.seg._python(b);host.pop('isolamento');host=pickle.dumps(host,protocol=4)
        dd=b.directdraw;surfaces=bytes(cpu.mem_read(dd.base_superficies,dd.tamanho_superficies))
        ordinary_phase=self.phasecap.current;blit_start=len(ordinary_phase['blits']);text_start=len(ordinary_phase['text_boundaries'])
        cap=self.cap;row=dict(frame=self.frame,phase=b.fase,routine=name,declared_writes=[],entry_registers=regs,
            before=cap.blob(dd.pixels('offscreen')),entry_blocks=self.metadata(blocks),entry_inputs=self.inputs(blocks),
            blits=[],text_boundaries=[])
        self.ativo=False;cap.current=row
        hook=cpu.hook_add(original.unicorn.UC_HOOK_CODE,b._parar_se_pedido,begin=ret,end=ret);cpu.ctl_flush_tb()
        try:
            b._retomando={regs['EIP']};out=BancadaCargaMissaoOriginal._correr(b,'isolated-S1-screen',regs['EIP'],{},(ret,),retomar=True)
            after=b.imagem()
            row.update(exit_registers=out,returned=out['EIP']==ret,after=cap.blob(dd.pixels('offscreen')),
                exit_blocks=self.metadata(after),exit_inputs=self.inputs(after),isolated_whole_state_sha256=b.resumo_imagem(after)['sha256'])
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
            row['whole_state_equal']=b.resumo_imagem(b.imagem())['sha256']==row['isolated_whole_state_sha256']
            row['raster_arguments_equal']=ordinary_phase['blits'][blit_start:]==row['blits']
            actual_text=[dict(e,blits_before=e['blits_before']-blit_start) for e in ordinary_phase['text_boundaries'][text_start:]]
            row['text_arguments_equal']=actual_text==row['text_boundaries']
            assert row['surface_equal'] and row['whole_state_equal'] and row['raster_arguments_equal'] and row['text_arguments_equal']
            c.hook_del(normal_hook)
        normal_hook=cpu.hook_add(original.unicorn.UC_HOOK_CODE,ordinary,begin=ret,end=ret)
        print('S1 isolated',row['frame'],row['routine'],'returned',flush=True)

def main(a):
    original.REF=a.ref;m=original.modulo_entrada();b,_,start=m.abrir(a.start,Path(a.snapshot))
    if not (16933<=start<17032 and 17044<=a.to<=17050):
        raise ValueError('Requires real S1 checkpoint16933..17031; stop17044..17050 to include both transitions')
    raw=original.remoto(original.PROBE_ROOT+'entradas/S1.json');b.roteiro.quadros=m.carregar_entrada(json.loads(raw))[0]
    metadata_path=Path(a.snapshot).parent/'passo-a.json';checkpoint_metadata=None
    if metadata_path.exists():
        metadata=json.loads(metadata_path.read_text());assert metadata['probe']=='S1' and metadata['input_sha256']==sha(raw)
        checkpoint_metadata=dict(path=str(metadata_path),sha256=sha(metadata_path.read_bytes()))
    iso=TelasS1(b);iso.instalar();checks=[];phases=[];t=time.monotonic()
    phasecap=object.__new__(CapturaTextoTela);phasecap.b=b;phasecap.blobs=iso.cap.blobs;phasecap.current=None
    iso.phasecap=phasecap
    refs={}
    if a.probe_records:
        refs={r['frame']:r for r in map(json.loads,lzma.decompress(Path(a.probe_records).read_bytes()).splitlines())}
        assert b.resumo_imagem(b.imagem())['sha256']==refs[start]['state_sha256'],('S1 opening checkpoint differs',start)
    def blit(c,pc,size,user):
        if iso.ativo:phasecap.blit(c,pc,size,user)
    def text(c,pc,size,user):
        if iso.ativo:phasecap.text(c,pc,size,user)
    for pc in original.BLITS:b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,blit,begin=pc,end=pc)
    b.cpu.hook_add(original.unicorn.UC_HOOK_BLOCK,text,begin=b.sym['AffText'],end=b.sym['AffText'])
    b.cpu.ctl_flush_tb()
    for k in range(start+1,a.to+1):
        iso.frame=k;b.roteiro.iniciar_quadro(k)
        for label,execute in (('between_frames',b.executar_entre_quadros),('frame',b.executar_quadro)):
            blocks=b.imagem();phasecap.current=dict(frame=k,phase=label,before=phasecap.blob(b.directdraw.pixels('offscreen')),
                entry_inputs=iso.inputs(blocks),entry_blocks=iso.metadata(blocks),blits=[],text_boundaries=[])
            execute(600,k)
            phasecap.current.update(after=phasecap.blob(b.directdraw.pixels('offscreen')),
                whole_state_sha256=b.resumo_imagem(b.imagem())['sha256'])
            phases.append(phasecap.current);phasecap.current=None
        between=phases[-2]['after']
        checks.append(dict(frame=k,between_surface=between,frame_surface=sha(b.directdraw.pixels('offscreen')),
            whole_state_sha256=b.resumo_imagem(b.imagem())['sha256']))
        if refs:
            ref=refs[k];check=checks[-1]
            assert check['between_surface']==ref['surfaces_between']['offscreen']
            assert check['frame_surface']==ref['surfaces_frame']['offscreen'] and check['whole_state_sha256']==ref['state_sha256']
            check['published_phase_and_state_equal']=True
        b.roteiro.eventos.clear()
        if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
    assert iso.registros and all(r.get('surface_equal') for r in iso.registros)
    for frame,mode in ((17032,0x13),(17043,0x11)):
        assert any(r['routine']=='MenuInit' and r['frame']==frame and
            mode in {r['entry_registers']['EAX']&255,r['entry_registers']['EDX']&255} for r in iso.registros),('Missing real S1 screen transition',frame,mode)
    result=dict(schema='rising-lands/s1-native-isolated-screens/1',method=__doc__,probe_ref=a.ref,frames=[start+1,a.to],
        executable_sha256=__import__('emulador').HASH_ORIGINAL,code_sha256=b.sha256_codigo(),
        source_sha256=sha(Path(__file__).read_bytes()),snapshot_sha256=sha(Path(a.snapshot).read_bytes()),input_sha256=sha(raw),
        checkpoint_metadata=checkpoint_metadata,probe_records_sha256=sha(Path(a.probe_records).read_bytes()) if a.probe_records else None,
        rows=iso.registros,phases=phases,blobs=iso.cap.blobs,checks=checks,elapsed_seconds=time.monotonic()-t)
    Path(a.output).write_bytes(lzma.compress(json.dumps(result).encode()));print('native isolated screens',len(iso.registros),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--ref',default=REF);p.add_argument('--probe-records');p.add_argument('--to',type=int,default=17050);p.add_argument('--output',required=True);main(p.parse_args())
