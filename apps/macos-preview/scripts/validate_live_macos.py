"""Bounded live proof and timing, without reloading later expected states."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from macos_live_session import MacOSLiveSession
from macos_graphics_inspection import GraphicsInspectionRenderer, RENDER_PINS


def source_revision(root):
    root=root.resolve()
    manifest=root.parent/'snapshot.json'
    if manifest.is_file():
        data=json.loads(manifest.read_bytes())
        if (root.parent/data['snapshot']).resolve()!=root:
            raise ValueError('Source archive differs from declared snapshot')
        return data['commit']
    top=Path(subprocess.check_output(['git','-C',str(root),'rev-parse','--show-toplevel'],text=True).strip()).resolve()
    if top!=root: raise ValueError('Source root is neither a checkout nor a declared archive')
    return subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--library',type=Path,required=True)
    p.add_argument('--executable',type=Path,required=True)
    p.add_argument('--graphics-sources',type=Path)
    p.add_argument('--frames',type=int,default=128)
    p.add_argument('--logic-only',action='store_true')
    p.add_argument('--png-output',type=Path)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists(): p.error('Refusing to overwrite a live report')
    renderer=None if a.logic_only else GraphicsInspectionRenderer(a.source_root,a.graphics_sources)
    live=MacOSLiveSession(a.source_root,a.library,a.executable,renderer)
    t0=time.perf_counter()
    try:
        presentation_seconds=0.0
        transfer_bytes=0
        transferred_surfaces_equal=0
        horizon_seconds=0.0
        horizon_frames=0
        horizon_last=None
        for i in range(1+2*a.frames):
            if a.logic_only and i>256:
                phase=2 if i%2 else 3
                n=(i+1)//2
                name=f"between_frames{n}" if phase==2 else f"frame{n}"
                t=time.perf_counter()
                try: live.abi.frame(live.handle,phase,live.inputs)
                except RuntimeError as exc:
                    live.stop=dict(type=type(exc).__name__,phase=name,detail=str(exc));break
                horizon_seconds+=time.perf_counter()-t
                horizon_frames+=int(phase==3)
                horizon_last=name
                if i%2000==0:print(name,flush=True)
                continue
            live.apply_frame()
            if live.stop: break
            if renderer and i>0 and i%2==0:
                t=time.perf_counter()
                # Same raw indexed packet as the production worker. Exercise JSON
                # and decoding too; native smoke measures actual JS/canvas handoff.
                packet=renderer.present(raw=True)
                wire=json.dumps(packet,separators=(',',':'))
                decoded=json.loads(wire)['frame']
                pixels=base64.b64decode(decoded['pixels'],validate=True)
                palette=base64.b64decode(decoded['palette'],validate=True)
                if len(pixels)!=480000 or len(palette)!=768 or hashlib.sha256(pixels).hexdigest()!=packet['pixels_sha256']:
                    raise AssertionError('Raw frame transfer changed pixels/palette shape')
                transferred_surfaces_equal+=int(packet['equals_native_phase_end'] is True)
                transfer_bytes+=len(wire)
                presentation_seconds+=time.perf_counter()-t
            if i%128==0: print(live.current.phase_name,flush=True)
        records=live.records
        frames=sum(r['phase'].startswith('frame') for r in records)
        totals={k:sum(r[k] for r in records) for k in ('rust_seconds','projection_seconds','render_seconds','total_seconds')}
        if a.png_output:
            if a.png_output.exists():p.error('Refusing to overwrite PNG evidence')
            a.png_output.write_bytes(base64.b64decode(renderer.present()['image'].split(',',1)[1]))
        report=dict(schema='rising-lands/macos-live-proof/1',
                    source_revision=source_revision(a.source_root),
                    library_sha256=live.library_sha256,graphics_pins=RENDER_PINS,
                    logic_only=a.logic_only,frames_requested=a.frames,frames_completed=frames,
                    last_phase=horizon_last or live.current.phase_name,first_stop=live.stop,
                    engine_only_extension=dict(frames=horizon_frames,seconds=horizon_seconds,last_phase=horizon_last,scope="ABI only beyond 128; no snapshots/render/equality claim"),
                    phases_equal=sum(r['state_equal'] is True for r in records),
                    checkpoints_equal=sum(r['checkpoint'] for r in records),
                    full_surfaces_equal=sum(bool((r['render'] or {}).get('equals_native_full_surface')) for r in records),
                    transfer=dict(format='indexed8-rgb24/1',bytes=transfer_bytes,accepted_surfaces_equal=transferred_surfaces_equal),
                    projection=dict(path='persistent-graphics-regions' if renderer else 'full-diagnostic',
                                    bulk_calls=sum(b.calls for b in live.bulks),bulk_buffer_allocations=sum(b.allocations for b in live.bulks),
                                    region_buffer_allocations=sum(v.allocations for v in live.views),
                                    retained_graphics_bytes=sum(len(b) for a,b,n in live.views[0].regions),
                                    abi_limitation='ABI 1.1 bulk snapshot has no region filter'),
                    phase_surfaces_equal=sum(bool((r['render'] or {}).get('equals_native_phase_end')) for r in records),
                    timing=dict(**totals,transfer_seconds=presentation_seconds,
                                frames_per_second=frames/(totals['total_seconds']+presentation_seconds),
                                rust_projection_render_transfer_fps=frames/(totals['rust_seconds']+totals['projection_seconds']+totals['render_seconds']+presentation_seconds),
                                rust_frames_per_second=frames/totals['rust_seconds'],
                                render_frames_per_second=frames/totals['render_seconds'] if renderer else None,
                                wall_seconds=time.perf_counter()-t0,
                                scope='Phase calls + bulk projection/hash/oracle comparison + render + raw indexed JSON encode/decode/hash; initialization/IPC/native canvas excluded'),
                    phases=records)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open('x') as f: json.dump(report,f,indent=1); f.write('\n')
        print(json.dumps({k:v for k,v in report.items() if k not in ('phases','graphics_pins')},indent=1))
        if report['phases_equal'] != min(257,1+2*a.frames): return 2
        if renderer and (report['full_surfaces_equal'] != min(128,a.frames) or transferred_surfaces_equal!=min(128,a.frames)): return 2
        return 0
    finally: live.close()

if __name__=='__main__': sys.exit(main())
