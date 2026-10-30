"""Original-only inhabited CAVE layer/selection matrix, restored from native P3 frame 220.

Declared writes finish the existing CAVE and lodge one troop-code bag entry. Every native call first verifies
BatimentEstHabiter; no reconstructed provider is imported. Animation/door/store flags are exhaustive byte-domain slices.
"""
import argparse,json,lzma,struct,time
from pathlib import Path
import capturar_sondas_graficos_m3 as original
from capturar_janelas_graficas_m3 import REF,sha,AQUI
import ambiente_missoes
from oraculo_quadro_missao import Isolamento

def main(a):
    original.REF=REF;m=original.modulo_entrada();b,_,frame=m.abrir(a.start,Path(a.snapshot));t=time.monotonic()
    if frame!=220:raise ValueError('Requires the reproduced P3 frame-220 checkpoint')
    iso=Isolamento(b,());ctx,image=iso._salvar();dd=b.directdraw;surface=bytes(b.cpu.mem_read(dd.base_superficies,dd.tamanho_superficies))
    cap=original.CapturadorSondasGraficos(b);cases=[];record=0x49a0c8+276
    # Native capacity is retained (2). Bag base is +0x0C: slot values start at record +0x12; codes at +0x4E.
    resident=[(record+4,b'\0\5'),(record+0xa,struct.pack('<H',100)),(record+0xc,b'\1\0'),
              (record+0x12,b'\3\0'),(record+0x4e,b'\1'+bytes(15))]
    for variant in range(16):
        for busy in (0,1):
            for flag in (0,1):
                for clock in range(8):
                    writes=resident+[(record+0x74,bytes([busy,flag,variant])),(0x508f80,struct.pack('<I',clock)),
                                      (0x496ac4,b'\xff\xff'),(0x495be0,b'\xff\xff')]
                    cases.append(dict(name=f'cave_variant{variant}_busy{busy}_flag{flag}_clock{clock}',index=1,tile=0x30d,writes=writes))
    for index,count,tile in ((0,7,0x2ed),(0,8,0x2ed),(1,1,0x30d)):
        r=0x49a0c8+276*index
        writes=(resident if index else [])+[(r+0xc,struct.pack('<H',count)),(r+0x4e,bytes([1])*count+bytes(16-count)),
                    (0x496ac4,struct.pack('<H',index)),(0x495be0,struct.pack('<H',index))]
        cases.append(dict(name=f'selected_type{2 if index==0 else 3}_bag{count}',index=index,tile=tile,writes=writes))
    rows=[]
    for case in cases:
        iso._restaurar(ctx,image);b.cpu.mem_write(dd.base_superficies,surface)
        for addr,value in case['writes']:b.cpu.mem_write(addr,value)
        u=lambda addr,size:int.from_bytes(b.cpu.mem_read(addr,size),'little')
        terrain=bytes(b.cpu.mem_read(u(0x507d70,4),131072));regions=bytes(b.cpu.mem_read(u(0x4e0f38,4),131072))
        cells=[c for c in range(65536) if struct.unpack_from('<H',terrain,2*c)[0]==case['tile'] and
               struct.unpack_from('<H',regions,2*c)[0]&0xffe0==0x8000+(case['index']<<5)]
        if len(cells)!=1:raise RuntimeError('Facade trigger is not unique')
        cell=cells[0];regs=dict(EAX=((cell%256-u(0x508720,2))*32)&0xffffffff,
                              EDX=((cell//256-u(0x508722,2))*32)&0xffffffff,EBX=cell)
        esp=b.cpu.reg_read(original.x86.UC_X86_REG_ESP)
        inhabited=iso.chamar_folha(0x41a5b8,dict(EAX=case['index']),esp)['EAX']&255
        if inhabited!=1:raise RuntimeError('Declared resident did not create native habitation')
        cap.phase_frame=220;cap.entry(b.cpu,0,0,None);cap.phase_frame=None
        iso.chamar_folha(b.sym['AffBatiments'],regs,esp);cap.end(b.cpu,0,0,None)
        row=cap.rows.pop();row.update(name=case['name'],index=case['index'],cell=cell,kind=2 if case['index']==0 else 3,
            registers=regs,habitado_native=inhabited,writes=[[hex(addr),value.hex()] for addr,value in case['writes']])
        rows.append(row)
        if len(rows)%100==0:print('native inhabited cases',len(rows),flush=True)
        if time.monotonic()-t>1080:raise RuntimeError('18-minute budget exhausted')
    iso._restaurar(ctx,image);b.cpu.mem_write(dd.base_superficies,surface);cap.detach()
    result=dict(schema='rising-lands/m3-inhabited-layers-native/1',method=__doc__,probe_ref=REF,
        executable_sha256=__import__('emulador').HASH_ORIGINAL,source_sha256=sha(Path(__file__).read_bytes()),
        snapshot_sha256=sha(Path(a.snapshot).read_bytes()),cases=len(rows),rows=rows,blobs=cap.blobs,
        elapsed_seconds=round(time.monotonic()-t,3),code_sha256=b.sha256_codigo())
    raw=json.dumps(result).encode();z=lzma.compress(raw,preset=6);Path(a.output).write_bytes(z)
    Path(a.output+'.manifest.json').write_text(json.dumps(dict(cases=len(rows),raw_sha256=sha(raw),compressed_sha256=sha(z),
        elapsed_seconds=result['elapsed_seconds'],source_sha256=result['source_sha256']),indent=1)+'\n')
    print(json.dumps(dict(cases=len(rows),seconds=result['elapsed_seconds'])),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--output',required=True)
    main(p.parse_args())
