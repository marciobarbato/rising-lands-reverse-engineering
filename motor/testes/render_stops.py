"""Perturbed-state Graphics 1.5 stop/prefix parity, separate from native cases."""
import argparse,json,struct,sys
from pathlib import Path
from render_matrix import cases,run as matrix_run,source_hashes,metadata,sha
from render_proof import renderer_pins
from render_abi import ROOT
from render_abi import Catalogo
from render_proof import inhabited
from render_quadro import renderizar_quadro
from validar_entrada_m3 import MemoriaEntradaM3

def stop_cases():
    original=next(c for c in cases() if c[0]=='selected_unit_12')
    name,blocks,surface,cache,tick,*_=original;m=MemoriaEntradaM3(blocks);unit=m.u32(0x4e19a0)+12*276;players=m.u32(0x5080a8)
    word=lambda x:struct.pack('<H',x)
    probes=[
      ('order_marker',[(unit+0x82,b'\1')],0x412923),
      ('capacity',[(unit+12,word(2))],0x410a2c),
      ('health',[(unit+0x9a,word(101))],0x410be4),
      ('fatigue',[(unit+4,word(5))],0x410be4),
      ('oscillation',[(unit+0x99,b'\1')],0x41591f),
      ('effects',[(unit+0xdc,b'\1')],0x41591f),
      ('direction',[(unit+0x91,b'\0')],0x41591f),
      ('phase',[(unit+0xa4,b'\xff')],0x41591f),
      ('nonbuilder_experience',[(unit+1,b'\0'),(unit+0xaf,b'\x20')],0x413696),
      ('action_kind',[(0x4e2410,word(0x29b7)+word(3))],0x417086),
      ('action_percent',[(0x4e2410,word(0x29b7)+word(0)+word(101))],0x417086),
      ('action_counter',[(0x4e2410,word(0x29b7)+word(2)+word(1000))],0x417086),
      ('counter',[(0x4e2eac,word(10000))],0x417f6e),
      ('placement',[(0x4e05ae,word(3)),(0x5099a8,word(100)+word(100))],0x41729b),
      ('target',[(0x496204,word(3000)),(0x4e05ac,word(1))],0x417ba2),
      ('market',[(0x4e2e7c,b'\1')],0x4667a7),
      ('minimap',[(0x497285,b'\1'),(0x496fe0,word(0))],0x46a70c),
      ('chrono',[(0x496ac4,word(1000))],0x401d18),
      ('cost',[(0x4e0618,word(10000))],0x40f77b),
      ('tooltip',[(0x4e060c,struct.pack('<I',1))],0x40f8c0),
      ('debug',[(0x4e17ac,b'\1')],0x417c7f),
      ('event',[(0x4e1b0e,b'\1')],0x417c8a),
      ('message',[(0x507d54,word(0)+word(1))],0x469c5f),
      ('alliance',[(players+6,b'\2')],0x417604),
      ('contact',[(0x5080b4,struct.pack('<I',1))],0x4175f2),
      ('second_cursor',[(0x4e062c,word(17))],0x417cfc),
    ]
    out=[];catalog=Catalogo()
    for name,patches,stop in probes:
        state=[(a,bytearray(b)) for a,b in blocks]
        for address,value in patches:
            for a,b in state:
                if a<=address and address+len(value)<=a+len(b):b[address-a:address-a+len(value)]=value;break
            else:raise ValueError('Patch outside declared memory')
        state=[(a,bytes(b)) for a,b in state];memory=MemoriaEntradaM3(state)
        py=renderizar_quadro(memory,superficie_anterior=surface,cache=cache,catalogo=catalog,habitado=lambda i:inhabited(memory,i),relogio=lambda:tick,hud=True)
        if not py.parada or int(py.parada['endereco'],16)!=stop:raise AssertionError((name,py.parada,hex(stop)))
        out.append((name,state,surface,cache,tick,py.pixels,stop))
    return out

def run(binary=None):
    report=matrix_run(binary,True,stop_cases())
    report.update(schema='rising-lands/rust-render-perturbed-stop-matrix/1',scope='26 declared perturbations of a captured entry; expected stops, prefixes, effects and cache come from read-only Python 1.5, not new original executions')
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument('--binary');p.add_argument('--output',required=True);a=p.parse_args()
    if Path(a.output).exists():raise SystemExit('Refusing overwrite')
    renderer_pins();before=source_hashes();report=run(a.binary);after=source_hashes()
    binary=Path(a.binary or ROOT/'motor/target/debug/render_fixtures')
    report.update(metadata(),source_sha256=before,sources_unchanged=before==after,binary_sha256=sha(binary.read_bytes()),reference_pins=renderer_pins())
    Path(a.output).write_text(json.dumps(report,indent=1)+'\n');print({k:v for k,v in report.items() if k not in ('rows','source_sha256','reference_pins')});return bool(report['mismatches'])
if __name__=='__main__':sys.exit(main())
