"""Original full-surface renderer proofs over Rust's own chained engine state."""
import argparse,ctypes as C,hashlib,json,struct,sys,time
from pathlib import Path
from render_abi import *
from pinned_reference import reference_file,provenance
from frame_long_evidence import mission_inputs,load_manifest,load_part
from frame_long_differential import source_hashes,metadata,write_json
from frame_differential import OriginalImage,static_inputs,FrameInput,FrameRegisters
from validar_entrada_m3 import MemoriaEntradaM3
from render_quadro import renderizar_quadro
from quadro_jogo import GLOBAIS_QUADRO
sha=lambda b:hashlib.sha256(b).hexdigest()
def live(library=None):
    f=Frames(library);s0,_,_,short=mission_inputs();part=load_part(load_manifest(),0)
    original=ROOT.parent/'source/cd/INSTALHD/RISING.EXE';image=OriginalImage(original,original.with_suffix('.SBL'));static=static_inputs(image,s0)
    handle=f.create();f.load(handle,sorted(list(s0.values())+list(static.items())))
    surface=next(s for s in short['phases'][0]['display_state']['surfaces'] if s['role']=='offscreen')
    inp=FrameInput(*part['named_inputs']['frame']['cursor'],int(surface['pixels'],16),FrameRegisters.from_values({k:int(v,16) for k,v in part['phases'][0]['entry']['registers'].items()}),(C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
    f.frame(handle,1,inp)
    inp.registers=FrameRegisters.from_values({k:int(v,16) for k,v in part['phases'][1]['entry']['registers'].items()})
    return f,handle,inp

def renderer_pins():
    path=ROOT/'motor/testes/render-reference-pins.json';pins=json.loads(path.read_text())
    for name,digest in pins['sources'].items():
        if sha(reference_file(ROOT/name).read_bytes())!=digest:raise ValueError('Pinned Graphics reference hash mismatch: '+name)
        if '/evidencias/' in name and sha((ROOT/name).read_bytes())!=digest:raise ValueError('Immutable Graphics evidence changed: '+name)
    return {**pins,'snapshot':provenance()}

def surface_hashes(frames):
    if frames<=128:
        native=json.loads((RAIZ/'evidencias/verificacao-cadeia-m22-v2-api15-128.json').read_text())
        return {row['frame']:row['recorded_sha256'] for row in native['rows']}
    hashes={}
    manifest=load_manifest()
    for number in range(10):
        part=load_part(manifest,number)
        for phase in part['phases']:
            if phase['phase'].startswith('between_frames'):
                n=int(phase['phase'].removeprefix('between_frames') or '1')
                hashes[n]=next(s['sha256'] for s in phase['display_state']['surfaces'] if s['role']=='offscreen')
        del part
    if len(hashes)!=9200:raise ValueError('M2.3 surface phase count')
    return hashes

def prove(frames=128,library=None,python_compare=True):
    renderer_pins();recorded=surface_hashes(frames)
    f,world,inp=live(library);r=Render(f);surface,cache=initial();renderer=r.create(world,surface,cache)
    catalog=Catalogo();rows=[];render_seconds=0;engine_seconds=0;first_stop=None
    try:
        for frame in range(1,frames+1):
            t=time.perf_counter();gen,phase,counter=r.generation(world);render_seconds+=time.perf_counter()-t
            before=f.snapshot(world) if python_compare else None
            t=time.perf_counter();out=r.draw(renderer,gen);render_seconds+=time.perf_counter()-t
            pixels=bytes(r.pixels);digest=sha(pixels)
            row=dict(frame=frame,generation=gen,phase=phase,counter=counter,disposition=out.disposition,stop=hex(out.stop_address) if out.stop_address else None,sha256=digest)
            row['original_equal']=digest==recorded[frame] if out.disposition!=2 else None
            if python_compare or out.disposition==2:
                if not python_compare:
                    before=f.snapshot(world)
                mem=MemoriaEntradaM3(list(before.items()));py=renderizar_quadro(mem,superficie_anterior=surface,catalogo=catalog,cache=cache,habitado=lambda i:inhabited(mem,i),hud=True)
                row['python_equal']=pixels==py.pixels
                actual_cache=r.cache(renderer);row['cache_equal']=actual_cache==py.cache
                row['stop_equal']=out.stop_address==(int(py.parada['endereco'],16) if py.parada else 0)
                row['world_read_only']=before==f.snapshot(world)
                row['palette_equal']=bytes(r.palette)==catalog.paleta()
                row['effects_equal']=effects(r.observations(renderer))==list(py.efeitos)
                surface,cache=py.pixels,py.cache
            rows.append(row)
            print(frame,row,flush=True)
            if out.disposition==2:first_stop=row;break
            if not python_compare:
                surface=pixels;cache=r.cache(renderer)
            t=time.perf_counter();f.frame(world,2,inp);f.frame(world,3,inp);engine_seconds+=time.perf_counter()-t
    finally:r.free(renderer);f.free(world)
    return dict(schema='rising-lands/rust-render-own-world-proof/1',requested_frames=frames,full_frames=sum(x['disposition']==0 for x in rows),first_stop=first_stop,original_equal=sum(bool(x.get('original_equal',False)) for x in rows),python_equal=sum(x.get('python_equal',False) for x in rows),rows=rows,timing=dict(render_seconds=render_seconds,engine_seconds=engine_seconds,render_fps=len(rows)/render_seconds,end_to_end_fps=len(rows)/(render_seconds+engine_seconds),scope='C ABI engine phases + world generation + render + caller buffer copies; timing excludes proof snapshots/Python/exports/presentation; initialization excluded'))
def inhabited(m,index):
    a=0x49a0c8+index*276;kind=m.u8(a+8);colonist=False
    for slot in range(m.u16(a+14)):
        if m.u8(a+0x4e+slot)!=1:continue
        t=m.u8(m.u32(0x4e19a0)+276*m.u16(a+0x12+slot*2)+1)
        if kind in (2,21) and t not in (3,11,12,13,14,15,16,17,25):return True
        colonist|=t==9
    return kind!=21 and colonist

def effects(obs):
    return [(bytes(x.name).split(b'\0')[0].decode(),x.address,bytes(x.before[:x.count]).hex(),bytes(x.after[:x.count]).hex()) for x in obs if x.kind==1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--frames',type=int,default=128);p.add_argument('--library');p.add_argument('--no-python',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
    if Path(a.output).exists():raise SystemExit('Refusing overwrite')
    before=source_hashes();report=prove(a.frames,a.library,not a.no_python);after=source_hashes()
    library=Path(a.library or ROOT/'motor/target/debug/librising_engine.dylib')
    report.update(metadata(),source_sha256=before,sources_unchanged=before==after,library_sha256=sha(library.read_bytes()),reference_pins=renderer_pins())
    write_json(a.output,report)
    bad=any(any(row.get(k,True) is False for k in ('original_equal','python_equal','cache_equal','stop_equal','world_read_only','palette_equal','effects_equal')) for row in report['rows'])
    if before!=after:raise AssertionError('Renderer sources changed during proof')
    return int(bad)
if __name__=='__main__':sys.exit(main())
