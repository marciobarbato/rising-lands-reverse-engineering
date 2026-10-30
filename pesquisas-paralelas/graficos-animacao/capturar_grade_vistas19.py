"""Original-only, bounded MONDE01 view-origin matrix for AffGame and RestoreAll.

Restore the exact accepted native frame128 for every call and apply only the two declared origin words.
The finite case matrix is every 25x17 viewport fitting the native64x64 map, split into bounded batches.
Record all DGROUP/CRT/allocation net changes, return registers, surface hashes and display RNG writer hits.
No reconstructed implementation is imported. This records evidence; it does not declare new origins safe.
"""
import argparse,base64,json,lzma,pickle,struct,time,zlib
from pathlib import Path
from capturar_escritas_cave_m3 import original,REF,sha
from oraculo_quadro_missao import Isolamento,BancadaCargaMissaoOriginal
from emulador import RETORNO

def main(a):
    original.REF=REF;m=original.modulo_entrada();b,_,k=m.abrir(a.start,None);assert k==128
    # Same observer-log compaction used by the original scripted-input harness. Logical event indices survive.
    # Keep the proof of native-memory preservation and independently recheck the first origin against v1.
    import delta_estado_missao as delta
    before_compaction=b.resumo_imagem(b.imagem())['sha256'];host_before=len(pickle.dumps(original.seg._python(b)))
    events=delta.compactar_eventos(b);discarded=len(events);events.descartar_ate(discarded)
    assert before_compaction==b.resumo_imagem(b.imagem())['sha256']
    iso=Isolamento(b,());ctx,image=iso._salvar();host=pickle.dumps(original.seg._python(b));dd=b.directdraw
    surfaces=bytes(b.cpu.mem_read(dd.base_superficies,dd.tamanho_superficies));rows=[];t=time.monotonic()
    assert bytes(b.cpu.mem_read(0x497168,4))==struct.pack('<HH',64,64)
    origins=[(x,y) for y in range(48) for x in range(40)]
    if not 0<=a.offset<len(origins) or not 0<a.count<=240:raise ValueError('1..240 origins per bounded run')
    writers={};sites=json.loads((original.AQUI/'evidencias/fechamento-escritas-affgame-modo12.json').read_text())['escritas_absolutas']['0x4e1d18']
    def writer(cpu,address,size,user):writers[hex(address)]=writers.get(hex(address),0)+1
    for address,*_ in sites:
        pc=int(address,16);b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,writer,begin=pc,end=pc)
    for origin in origins[a.offset:a.offset+a.count]:
        for routine in ('AffGame','RestoreAll'):
            iso._restaurar(ctx,image);b.cpu.mem_write(dd.base_superficies,surfaces)
            for name,value in pickle.loads(host).items():
                if name in original.seg.COM_CPU:
                    target=getattr(b,name)
                    for key,item in value.items():vars(target)[key]=original.seg._no_lugar(vars(target).get(key),item)
                else:vars(b)[name]=original.seg._no_lugar(vars(b).get(name),value)
            writes=[(0x508720,struct.pack('<H',origin[0])),(0x508722,struct.pack('<H',origin[1]))]
            for address,data in writes:b.cpu.mem_write(address,data)
            before=b.imagem();writers.clear()
            esp=b.cpu.reg_read(original.x86.UC_X86_REG_ESP)-0x100;b.cpu.mem_write(esp,struct.pack('<I',RETORNO))
            b.cpu.reg_write(original.x86.UC_X86_REG_ESP,esp)
            hook=b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,b._parar_se_pedido,begin=RETORNO,end=RETORNO);b.cpu.ctl_flush_tb()
            try:out=BancadaCargaMissaoOriginal._correr(b,'view-origin-matrix',b.sym[routine],{},(RETORNO,),retomar=True)
            finally:b.cpu.hook_del(hook)
            after=b.imagem();changed={}
            for name,(address,data) in before.items():
                new=after[name][1]
                if data==new:continue
                changes=[[hex(address+i),x,y] for i,(x,y) in enumerate(zip(data,new)) if x!=y]
                changed[name]=dict(base=hex(address),size=len(data),before=sha(data),after=sha(new),
                    changes=changes if name in ('dgroup','crt_thread_data') else None,count=len(changes),first=changes[0][0])
            rows.append(dict(routine=routine,origin=origin,writes=[[hex(ad),v.hex()] for ad,v in writes],
                returned=out['EIP']==RETORNO,registers=out,changed=changed,cursor_writer_hits=dict(writers),
                surface_sha256=sha(dd.pixels('offscreen'))))
            assert rows[-1]['returned']
            if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
        if len(rows)%40==0:print('native calls',len(rows),'last origin',origin,flush=True)
    result=dict(schema='rising-lands/native-view-origin-matrix/1',method=__doc__,probe_ref=REF,
        executable_sha256=__import__('emulador').HASH_ORIGINAL,source_sha256=sha(Path(__file__).read_bytes()),
        snapshot_sha256=sha(Path(a.snapshot).read_bytes()),code_sha256=b.sha256_codigo(),map=[64,64],viewport=[25,17],
        offset=a.offset,count=a.count,elapsed_seconds=time.monotonic()-t,
        host_observer_compaction=dict(discarded_events=discarded,logical_event_count=len(events),
            pickle_bytes_before=host_before,pickle_bytes_after=len(host),native_state_sha256=before_compaction),
        opening_dgroup_zlib=base64.b64encode(zlib.compress(image['dgroup'][1])).decode(),
        projectile_base=hex(int.from_bytes(image['dgroup'][1][0x5080f0-0x494000:0x5080f4-0x494000],'little')),
        opening_projectiles_zlib=base64.b64encode(zlib.compress(next(v for n,(ad,v) in image.items()
            if ad==int.from_bytes(image['dgroup'][1][0x5080f0-0x494000:0x5080f4-0x494000],'little')))).decode(),rows=rows)
    Path(a.output).write_bytes(lzma.compress(json.dumps(result).encode()));print('completed',len(rows),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--offset',type=int,required=True);p.add_argument('--count',type=int,required=True);p.add_argument('--output',required=True);main(p.parse_args())
