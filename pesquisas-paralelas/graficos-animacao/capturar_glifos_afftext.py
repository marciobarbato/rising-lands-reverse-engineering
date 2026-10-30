"""Prepared original AffText calls from the accepted MONDE01 frame128 snapshot.

AffText alone executes: remove only its declared non-execution boundary. Input text/arguments and clip words
are explicit prepared writes, never claims about a text-enabled mission trajectory. No translated renderer runs.
"""
import argparse,base64,json,lzma,struct,time,zlib
from pathlib import Path
from capturar_escritas_cave_m3 import original,REF,sha
from oraculo_quadro_missao import Isolamento,BancadaCargaMissaoOriginal
from emulador import RETORNO,PILHA


def main(a):
    original.REF=REF;m=original.modulo_entrada();b,_,k=m.abrir(a.start,None);assert k==128
    b.pulos.pop(b.sym['AffText'],None);b.fronteiras.pop(b.sym['AffText'],None)
    iso=Isolamento(b,());ctx,image=iso._salvar();cpu=b.cpu;x86=original.x86
    baseline=bytes((x*7+y*11)%256 for y in range(600) for x in range(800))
    surface=int.from_bytes(cpu.mem_read(0x508f70,4),'little')
    rows=[];blits=[];t=time.monotonic()
    def blit(c,pc,size,_):
        r=lambda n:c.reg_read(getattr(x86,'UC_X86_REG_'+n))&0xffffffff
        signed=lambda v:(v&65535)-65536 if v&32768 else v&65535
        blits.append([hex(pc),signed(r('EAX')),signed(r('EDX')),r('EBX')&65535,r('ECX')&255])
    cpu.hook_add(original.unicorn.UC_HOOK_CODE,blit,begin=0x45b247,end=0x45b247)
    cpu.hook_add(original.unicorn.UC_HOOK_CODE,b._parar_se_pedido,begin=RETORNO,end=RETORNO)
    # All six bitmap fonts, spaces, newline/NUL, PT-BR bytes, fixed and centred rectangles, clipping edges.
    texts=[b'',b'ABC xyz 019',b'SANTU\xc1RIO',b'FAZENDEIRO',b'A B\nignored',b'A\0ignored',
           bytes(range(33,128)),bytes(range(128,224)),bytes(range(224,256))]
    positions=[(12,15,12,15,0),(12,15,312,65,0),(-5,-3,-5,-3,0),(790,590,790,590,0),(12,15,312,65,1)]
    for font in range(1,7):
        for text in texts:
            for x,y,right,bottom,clip in positions:
                iso._restaurar(ctx,image);cpu.mem_write(surface,baseline);blits.clear()
                words=(16,18,240,50);cpu.mem_write(0x49a01c,struct.pack('<4H',words[1],words[3],words[0],words[2]))
                esp=PILHA+0x8000;ptr=PILHA+0xe000
                cpu.mem_write(ptr,text+b'\0');cpu.mem_write(esp,struct.pack('<5I',RETORNO,ptr,font,0,clip))
                for name,value in dict(EAX=x,EDX=y,EBX=right,ECX=bottom,ESP=esp).items():cpu.reg_write(getattr(x86,'UC_X86_REG_'+name),value&0xffffffff)
                before=b.imagem();cpu.ctl_flush_tb()
                out=BancadaCargaMissaoOriginal._correr(b,'prepared-AffText',b.sym['AffText'],{},(RETORNO,),retomar=True)
                assert out['EIP']==RETORNO and out['ESP']==esp+20
                after=b.imagem();changes={n:sha(v) for n,(ad,v) in after.items() if v!=before[n][1]}
                pixels=bytes(cpu.mem_read(surface,480000))
                rows.append(dict(request=dict(text_hex=text.hex(),x=x,y=y,right=right,bottom=bottom,font=font,flags=[0,clip]),
                    clip=list(words),returned=True,stack_balanced=True,blits=list(blits),changed_blocks=changes,
                    surface_sha256=sha(pixels),pixels_zlib=base64.b64encode(zlib.compress(pixels)).decode()))
                if time.monotonic()-t>1080:raise RuntimeError('18-minute native budget exhausted')
        print('native font',font,'calls',len(rows),flush=True)
    result=dict(schema='rising-lands/afftext-bitmap-native/1',method=__doc__,probe_ref=REF,
        executable_sha256=__import__('emulador').HASH_ORIGINAL,source_sha256=sha(Path(__file__).read_bytes()),
        snapshot_sha256=sha(Path(a.snapshot).read_bytes()),code_sha256=b.sha256_codigo(),
        afftext_bytes_sha256=sha(cpu.mem_read(0x459454,0x4598ad-0x459454)),
        language=[int.from_bytes(cpu.mem_read(p,4),'little') for p in (0x4e1d94,0x4e1d98)],
        baseline_sha256=sha(baseline),elapsed_seconds=time.monotonic()-t,rows=rows)
    Path(a.output).write_bytes(lzma.compress(json.dumps(result).encode()));print('native calls',len(rows),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--output',required=True);main(p.parse_args())
