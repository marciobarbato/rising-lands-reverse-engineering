"""Exercise the exact Swift frame driver: serial S0 chain, Rust pixels, native stops."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import argparse,ctypes as C,hashlib,json,time
from macos_native_driver import NativeDriver
from macos_rust_abi import Frames
from macos_render_diagnostics import RenderDiagnostics
from macos_fast_projection import MacOSBulkProjection,MacOSGraphicsView
from macos_projection_codec import ProjectionCodec
from macos_graphics_inspection import GraphicsInspectionRenderer


def main():
    p=argparse.ArgumentParser()
    for name in ('root','library','driver','codec','inputs','graphics-sources','output'):p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--frames',type=int,default=128);p.add_argument('--until-stop',action='store_true');p.add_argument('--seconds',type=float,default=1100)
    p.add_argument('--python-oracle',action='store_true')
    a=p.parse_args()
    if a.output.exists():p.error('Refusing to overwrite native proof')
    driver=NativeDriver(a.driver,a.library,a.inputs)
    f=Frames(a.library);bulk=MacOSBulkProjection(f,(a.inputs/'s0.bin').stat().st_size,ProjectionCodec(a.codec))
    oracle=GraphicsInspectionRenderer(a.root,a.graphics_sources) if a.python_oracle else None
    views=[MacOSGraphicsView('actual-native'),MacOSGraphicsView('actual-native')]
    diagnostics=RenderDiagnostics(f) if oracle else None
    rows=[];failures=[];previous=None;python_equal=0
    driver.lib.macos_live_audit_window(driver.handle,18401 if a.frames>=9200 else 257)
    def observer(ctx,world,index,phase):
        nonlocal previous,python_equal
        try:
            if index>256:return 0
            bulk.update(world)
            if oracle:
                image=views[index%2].capture(bulk,oracle.api,index,'load_tail' if index==0 else ('between_frames' if index==1 else f'between_frames{(index+1)//2}') if phase==2 else f'frame{index//2}','actual-native',index%2==0)
                record=oracle.consume(image,previous if phase==2 else None)
                if driver.pixels()!=oracle.pixels:raise AssertionError('Rust/Python surface mismatch')
                if phase==2:
                    if driver.palette()!=oracle.palette:raise AssertionError('Rust/Python palette mismatch')
                    diagnostics.compare(driver.lib.macos_live_renderer(driver.handle),oracle.last)
                    python_equal+=1
                previous=image
            rows.append(dict(index=index,phase=phase,state_sha256=bytes(driver.status().state_sha).hex(),surface_sha256=hashlib.sha256(driver.pixels()).hexdigest()))
            return 0
        except Exception as e:failures.append(str(e));return 1
    t0=time.perf_counter();stop=None
    try:
        code=driver.advance(observer)
        while not code:
            s=driver.status()
            if s.frames>=a.frames and not a.until_stop:break
            if time.perf_counter()-t0>=a.seconds:break
            code=driver.advance(observer)
            if driver.status().frames%1000==0:print('Native frames',driver.status().frames,flush=True)
        s=driver.status()
        if s.stopped:stop=bytes(s.message).split(b'\0')[0].decode()
        report=dict(schema='rising-lands/macos-native-render-proof/1',engine_sha256=hashlib.sha256(a.library.read_bytes()).hexdigest(),
                    driver_sha256=hashlib.sha256(a.driver.read_bytes()).hexdigest(),inputs_manifest_sha256=hashlib.sha256((a.inputs/'manifest.json').read_bytes()).hexdigest(),
                    frames_requested=a.frames,frames_completed=s.frames,states_equal=s.phases_equal,checkpoints_equal=s.checkpoints_equal,
                    surfaces_equal=s.surfaces_equal,python_surfaces_equal=python_equal,first_named_stop=stop,observer_failures=failures,
                    horizon_pending=a.until_stop and not s.stopped,
                    timing=dict(logic_seconds=s.logic_ns/1e9,render_seconds=s.render_ns/1e9,proof_seconds=s.proof_ns/1e9,wall_seconds=time.perf_counter()-t0),prefix_phases=rows)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(report,indent=1)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='prefix_phases'},indent=1))
        return int(bool(failures) or s.frames<a.frames or s.surfaces_equal<min(a.frames,9200) or s.phases_equal<(18401 if a.frames>=9200 else 257) or (a.python_oracle and python_equal!=128))
    finally:driver.close()
if __name__=='__main__':sys.exit(main())
