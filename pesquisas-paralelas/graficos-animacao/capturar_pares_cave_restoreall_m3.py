"""Original RestoreAll matrix: sanctuary modes0..7 paired with constructing/uninhabited/inhabited CAVE.

Prepared cases restore native P3 frame220 and apply only listed record writes. Natural two-pass captures separately
prove the actual P3/P6/P7/S1 states and outside-display readers. This matrix checks that other already-supported
sanctuary modes introduce no additional AffBatiments writer sites when a CAVE is present.
"""
import argparse,base64,json,lzma,pickle,struct,time,zlib
from pathlib import Path
from capturar_escritas_cave_m3 import original,REF,sha,EscritasBatiments
from oraculo_quadro_missao import Isolamento,BancadaCargaMissaoOriginal
from oraculo_carga_missao import DADOS_THREAD_CRT
from emulador import RETORNO

def main(a):
    original.REF=REF;m=original.modulo_entrada();b,_,k=m.abrir(a.start,Path(a.snapshot));assert k==220
    iso=Isolamento(b,());ctx,image=iso._salvar();host=pickle.dumps(original.seg._python(b));dd=b.directdraw
    surfaces=bytes(b.cpu.mem_read(dd.base_superficies,dd.tamanho_superficies));rows=[];t=time.monotonic()
    for sanctuary in range(8):
        for cave in ('construction','uninhabited','inhabited'):
            iso._restaurar(ctx,image);b.cpu.mem_write(dd.base_superficies,surfaces)
            for name,value in pickle.loads(host).items():
                if name in original.seg.COM_CPU:
                    target=getattr(b,name)
                    for key,item in value.items():vars(target)[key]=original.seg._no_lugar(vars(target).get(key),item)
                else:vars(b)[name]=original.seg._no_lugar(vars(b).get(name),value)
            r=0x49a0c8+276;writes=[(0x49a0c8+5,bytes([sanctuary])),(r+5,bytes([2 if cave=='construction' else 5])),
                (r+0xa,struct.pack('<H',50 if cave=='construction' else 100))]
            if cave=='inhabited':writes += [(r+4,b'\0'),(r+0xc,b'\1\0'),(r+0x12,b'\3\0'),(r+0x4e,b'\1'+bytes(15))]
            for address,data in writes:b.cpu.mem_write(address,data)
            before_image=b.imagem();before=bytes(b.cpu.mem_read(0x494000,0x8f000));crt=bytes(b.cpu.mem_read(DADOS_THREAD_CRT,4096))
            obs=EscritasBatiments(b);obs.start(220)
            esp=b.cpu.reg_read(original.x86.UC_X86_REG_ESP)-0x100;b.cpu.mem_write(esp,struct.pack('<I',RETORNO))
            b.cpu.reg_write(original.x86.UC_X86_REG_ESP,esp)
            hook=b.cpu.hook_add(original.unicorn.UC_HOOK_CODE,b._parar_se_pedido,begin=RETORNO,end=RETORNO);b.cpu.ctl_flush_tb()
            try:out=BancadaCargaMissaoOriginal._correr(b,'prepared-cave-pair',b.sym['RestoreAll'],{},(RETORNO,),retomar=True)
            finally:b.cpu.hook_del(hook);obs.stop()
            after=bytes(b.cpu.mem_read(0x494000,0x8f000));observation=obs.finish()
            rows.append(dict(sanctuary=sanctuary,cave=cave,writes=[[hex(ad),d.hex()] for ad,d in writes],returned=out['EIP']==RETORNO,
                eax=out['EAX'],before_dgroup_zlib=base64.b64encode(zlib.compress(before)).decode(),
                changed_allocations={n:dict(base=hex(ad),before_sha256=sha(before_image[n][1]),after_sha256=sha(v),
                    changed_bytes=sum(x!=y for x,y in zip(before_image[n][1],v)))
                    for n,(ad,v) in b.imagem().items() if n.startswith('alloc') and v!=before_image[n][1]},
                net_dgroup=[[hex(0x494000+i),x,y] for i,(x,y) in enumerate(zip(before,after)) if x!=y],
                crt_unchanged=crt==bytes(b.cpu.mem_read(DADOS_THREAD_CRT,4096)),observation=observation,
                surface_sha256=sha(b.directdraw.pixels('offscreen'))))
            assert rows[-1]['returned'];print(sanctuary,cave,'native pair returned',flush=True)
            if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
    raw=json.dumps(dict(schema='rising-lands/cave-pair-native-matrix/1',method=__doc__,probe_ref=REF,
        executable_sha256=__import__('emulador').HASH_ORIGINAL,source_sha256=sha(Path(__file__).read_bytes()),
        snapshot_sha256=sha(Path(a.snapshot).read_bytes()),code_sha256=b.sha256_codigo(),elapsed_seconds=time.monotonic()-t,rows=rows)).encode()
    Path(a.output).write_bytes(lzma.compress(raw));print('original cases',len(rows),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--output',required=True);main(p.parse_args())
