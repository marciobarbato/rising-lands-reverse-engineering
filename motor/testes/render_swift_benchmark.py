"""Run the actual Swift/Metal buffer client under an outer exclusive heavy lease."""
import argparse,json,subprocess,sys
from pathlib import Path
from render_proof import renderer_pins
from frame_long_differential import source_hashes,metadata,write_json
from render_abi import ROOT
from render_matrix import sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--binary',required=True);p.add_argument('--inputs',required=True);p.add_argument('--library',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    if Path(a.output).exists():raise SystemExit('Refusing overwrite')
    renderer_pins();before=source_hashes()
    result=subprocess.run([a.binary,a.inputs],check=True,text=True,capture_output=True)
    report=json.loads(result.stdout);after=source_hashes()
    report.update(schema='rising-lands/rust-render-swift-metal-benchmark/1',**metadata(),source_sha256=before,sources_unchanged=before==after,library_sha256=sha(Path(a.library).read_bytes()),swift_binary_sha256=sha(Path(a.binary).read_bytes()),input_sha256=sha(Path(a.inputs).read_bytes()),reference_pins=renderer_pins(),target_fps=25,target_met=report['engine_render_metal_fps']>=25)
    write_json(a.output,report);print(result.stdout)
    return int(not report['target_met'] or before!=after or report['frames_equal']!=128)
if __name__=='__main__':sys.exit(main())
