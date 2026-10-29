"""Original-only AffBatiments matrix restored from P3's native frame-220 checkpoint.

Declared writes exercise CAVE/sanctuary construction modes, progression clips and uninhabited/RNG states.
No translation is imported; every call reaches its native return. The frame-220 state is matched to the published
scripted probe before the checkpoint is saved by capturar_sondas_graficos_m3.py.
"""
import argparse, json, struct, time
from pathlib import Path
from capturar_sondas_graficos_m3 import (AQUI,ROOT,REF,sha,modulo_entrada,CapturadorSondasGraficos)
import ambiente_missoes
from oraculo_quadro_missao import Isolamento


def cases(b):
    m=lambda a,n:bytes(b.cpu.mem_read(a,n));u=lambda a,n:int.from_bytes(m(a,n),'little')
    terrain=m(u(0x507d70,4),131072);regions=m(u(0x4e0f38,4),131072)
    out=[]
    for index,tile in ((0,0x2ed),(1,0x30d)):
        record=0x49a0c8+276*index;kind=u(record+8,1)
        cells=[c for c in range(65536) if struct.unpack_from('<H',terrain,2*c)[0]==tile
               and struct.unpack_from('<H',regions,2*c)[0]&0xffe0==0x8000+(index<<5)]
        if len(cells)!=1:raise RuntimeError((index,tile,cells))
        cell=cells[0];ox,oy=u(0x508720,2),u(0x508722,2)
        regs=dict(EAX=((cell%256-ox)*32)&0xffffffff,EDX=((cell//256-oy)*32)&0xffffffff,EBX=cell)
        maximum=u(0x495d90+52*kind,2)
        base_writes=[(0x496ac4,b'\xff\xff'),(0x495be0,b'\xff\xff')]
        # The sanctuary's initial bag is emptied explicitly for uninhabited branches.
        empty=[(record+0xc,b'\0\0'),(record+0x4e,bytes(16))] if index==0 else []
        for mode in (0,1,2,6,7):
            for state in (0,1,25,50,75,99,100,101,125,150,175,199,200):
                hp=(maximum*state+199)//200
                writes=base_writes+[(record+5,bytes([mode])),(record+0xa,struct.pack('<H',hp))]+empty
                out.append(dict(name=f'type{kind}_mode{mode}_state{state}',index=index,kind=kind,cell=cell,regs=regs,writes=writes))
        for mode in (3,4,5):
            for seed in (0,1,254):
                for height in ((0,35,255) if mode==3 else (0,)):
                    writes=base_writes+empty+[(record+5,bytes([mode])),(record+0xa,struct.pack('<H',maximum)),
                                              (record+0x84,struct.pack('<H',height)),(0x4e1d18,bytes([seed]))]
                    out.append(dict(name=f'type{kind}_mode{mode}_rng{seed}_height{height}',index=index,kind=kind,cell=cell,regs=regs,writes=writes))
    return out


def main(args):
    t=time.monotonic();m=modulo_entrada();b,_,frame=m.abrir(args.start,Path(args.snapshot))
    if frame!=220:raise RuntimeError('Matrix requires the P3 frame-220 checkpoint')
    iso=Isolamento(b,());ctx,image=iso._salvar();dd=b.directdraw
    surfaces=bytes(b.cpu.mem_read(dd.base_superficies,dd.tamanho_superficies))
    cap=CapturadorSondasGraficos(b);rows=[]
    for case in cases(b):
        iso._restaurar(ctx,image);b.cpu.mem_write(dd.base_superficies,surfaces)
        for a,value in case['writes']:b.cpu.mem_write(a,bytes(value))
        cap.phase_frame=220;cap.entry(b.cpu,0,0,None);cap.phase_frame=None
        result=iso.chamar_folha(b.sym['AffBatiments'],case['regs'],b.cpu.reg_read(__import__('emulador').x86.UC_X86_REG_ESP))
        cap.end(b.cpu,0,0,None);row=cap.rows.pop()
        row.update(name=case['name'],index=case['index'],kind=case['kind'],cell=case['cell'],registers=case['regs'],
                   writes=[[hex(a),bytes(v).hex()] for a,v in case['writes']],returned=True)
        rows.append(row)
        if len(rows)%20==0:print('matrix',len(rows),'native calls returned',flush=True)
        if time.monotonic()-t>1080:raise RuntimeError('18-minute matrix budget exhausted')
    iso._restaurar(ctx,image);b.cpu.mem_write(dd.base_superficies,surfaces);cap.detach()
    out=dict(schema='rising-lands/m3-cave-facade-matrix/1',method=__doc__,probe_ref=REF,source_snapshot_sha256=sha(Path(args.snapshot).read_bytes()),
             cases=len(rows),rows=rows,blobs=cap.blobs,elapsed_seconds=round(time.monotonic()-t,3),code_sha256=b.sha256_codigo())
    Path(args.output).write_text(json.dumps(out));print(json.dumps({k:v for k,v in out.items() if k not in ('rows','blobs','method')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--snapshot',required=True);p.add_argument('--output',required=True)
    main(p.parse_args())
