"""Prepare explicit pinned original inputs for the standalone Swift/Metal client."""
import argparse,ctypes as C,json,struct
from pathlib import Path
from render_abi import *
from frame_long_evidence import mission_inputs,load_manifest,load_part
from frame_differential import OriginalImage,static_inputs,FrameInput,FrameRegisters

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output)
    if out.exists():raise SystemExit('Refusing overwrite')
    s0,_,_,short=mission_inputs();part=load_part(load_manifest(),0);original=ROOT.parent/'source/cd/INSTALHD/RISING.EXE';image=OriginalImage(original,original.with_suffix('.SBL'));static=static_inputs(image,s0)
    surface=next(s for s in short['phases'][0]['display_state']['surfaces'] if s['role']=='offscreen')
    def registers(i):return FrameRegisters.from_values({k:int(v,16) for k,v in part['phases'][i]['entry']['registers'].items()})
    inp=FrameInput(*part['named_inputs']['frame']['cursor'],int(surface['pixels'],16),registers(0),(C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
    pixels,cache=initial();native=json.loads((RAIZ/'evidencias/verificacao-cadeia-m22-v2-api15-128.json').read_text())
    with out.open('xb') as f:
        def u32(n):f.write(struct.pack('<I',n))
        def b(v):u32(len(v));f.write(v)
        f.write(b'RLSW1300')
        for v in original_assets():b(v)
        blocks=sorted(list(s0.values())+list(static.items()));u32(len(blocks))
        for base,data in blocks:u32(base);b(data)
        b(bytes(inp));b(bytes(registers(1)));b(pixels);b(cache.registros);b(cache.blocos_crus);u32(cache.proximo)
        b('\n'.join(row['recorded_sha256'] for row in native['rows']).encode())
    print(out)
if __name__=='__main__':main()
