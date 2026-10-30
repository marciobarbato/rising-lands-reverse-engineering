"""Prepare provenance-bound native initialization/proof data; never live replay."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import argparse,ctypes as C,hashlib,json,lzma,struct
from macos_m22_playback import MacOSM22Playback,PINS,CAPTURE
from macos_live_session import MacOSLiveSession
from macos_graphics_inspection import GraphicsInspectionRenderer,RENDER_PINS
from macos_fast_projection import MacOSBulkProjection
from macos_projection_codec import ProjectionCodec


def prepare(root,library,executable,graphics_sources,output,codec_library=None):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    renderer=GraphicsInspectionRenderer(root,graphics_sources)
    session=MacOSLiveSession(root,library,executable)
    def write(name,data):
        p=output/name
        if p.exists() and p.read_bytes()!=data:raise ValueError('Native input changed: '+name)
        p.write_bytes(data)
    try:
        blocks=sorted(list(session.s0.values())+list(session.static.items()))
        write('s0.bin',struct.pack('<I',len(blocks))+b''.join(struct.pack('<II',a,len(b))+b for a,b in blocks))
        write('input1.bin',bytes(session.inputs))
        session.inputs.registers=__import__('macos_rust_abi').FrameRegisters.from_values(session.phase2_registers)
        write('input2.bin',bytes(session.inputs))
        write('surface.bin',renderer.initial_pixels);write('keys.bin',renderer.initial_cache.registros)
        write('cache.bin',renderer.initial_cache.blocos_crus);write('cursor.bin',struct.pack('<I',renderer.initial_cache.proximo))
        write('palette.bin',renderer.palette)
        graphics=sys.modules['graficos']
        assets=[renderer.catalog._ler('cd/INSTALHD/GRAPHICS/'+name) for name in graphics.ORDEM]
        assets+=[renderer.catalog._ler('cd/INSTALHD/PLATGAME.PIE'),*sys.modules['test_quadro_jogo'].tabelas()]
        assert len(assets)==9
        for i,data in enumerate(assets):write(f'asset{i}.bin',data)
        session.inputs.registers=__import__('macos_rust_abi').FrameRegisters.from_values(session.phase1_registers)
        session.abi.frame(session.handle,1,session.inputs)
        bulk=MacOSBulkProjection(session.abi,len((output/'s0.bin').read_bytes()),ProjectionCodec(codec_library)).update(session.handle)
        if bulk.masked_summary(session.names,session.static,session.ranges)!=session.expected[0]:raise AssertionError('Native input load-tail proof mismatch')
        write('entries.bin',bytes(bulk.native_entries));write('spans.bin',bytes(bulk.native_spans))
        expected_prefix=session.expected
        # Hash-checked M2.3 packages provide surfaces only, never later world inputs.
        manifest_path=Path(root)/'pesquisas-paralelas/missoes/evidencias/m2-3/captura-quadros9200-monde01-exibicao-v2.manifest.json'
        if hashlib.sha256(manifest_path.read_bytes()).hexdigest()!='e88dc3fcaca11d03a774dad8bd9c768345f13c884cc2d8df493107ec9d180b09':raise ValueError('M2.3 manifest pin mismatch')
        manifest=json.loads(manifest_path.read_bytes());surfaces={};states=[]
        policy=json.loads((Path(root)/manifest['policy']['path']).read_bytes())
        if sorted((int(a,16),int(z,16)) for a,z in policy['cumulative']['exclusion_mask'])!=session.ranges:raise ValueError('M2.2/M2.3 mask differs')
        for part in manifest['parts']:
            data=(Path(root)/part['artifact']).read_bytes()
            if hashlib.sha256(data).hexdigest()!=part['compressed_sha256']:raise ValueError('M2.3 compressed pin mismatch')
            raw=lzma.decompress(data)
            if hashlib.sha256(raw).hexdigest()!=part['raw_sha256']:raise ValueError('M2.3 raw pin mismatch')
            cap=json.loads(raw)
            for phase in cap['phases']:
                name=phase['phase']
                states.append(phase['state_after']['compared_summary']['sha256'])
                if name.startswith('between_frames'):
                    frame=int(name[len('between_frames'):] or '1')
                    surfaces[frame]=next(s['sha256'] for s in phase['display_state']['surfaces'] if s['role']=='offscreen')
            print('Native inputs: M2.3 part',part['part'],flush=True)
        if len(states)!=18401 or tuple(states[:257])!=expected_prefix:raise ValueError('M2.3 state prefix differs')
        write('states.bin',b''.join(bytes.fromhex(h) for h in states))
        if sorted(surfaces)!=list(range(1,9201)):raise ValueError('M2.3 surface domain incomplete')
        for i in range(1,129):
            if surfaces[i]!=renderer.references[i]['native_full_surface_sha256']:raise ValueError('M2.2/M2.3 surface mismatch')
        write('surfaces.bin',b''.join(bytes.fromhex(surfaces[i]) for i in range(1,9201)))
        report=dict(schema='rising-lands/macos-native-inputs/1',evidence=PINS,graphics=RENDER_PINS,
                    library_sha256=hashlib.sha256(Path(library).read_bytes()).hexdigest(),
                    m23_manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                    surfaces=9200,states=18401,source='Accepted S0 + four original static tables; later states are proof hashes only',
                    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file() and p.name!='manifest.json'})
        (output/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
        return report
    finally:session.close()

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('root','library','executable','graphics-sources','output'):p.add_argument('--'+k,required=True,type=Path)
    p.add_argument('--codec-library',type=Path)
    a=p.parse_args();prepare(a.root,a.library,a.executable,a.graphics_sources,a.output,a.codec_library)
