"""Batch Rust Graphics 1.5 leaves against frozen original input-time surfaces."""
import argparse,ast,hashlib,json,struct,subprocess,sys,tempfile
from pathlib import Path
from render_abi import original_assets,RAIZ,ROOT
from validar_entrada_m3 import CapturaEntradaM3,MemoriaEntradaM3
from render_quadro import renderizar_quadro,EstadoCache
from render_proof import inhabited,renderer_pins
from frame_long_differential import source_hashes,metadata
sha=lambda b:hashlib.sha256(b).hexdigest()
CAPTURES=['captura-entrada-m3.json','captura-entrada-m3-suplementar.json']
def cases():
    result=[]
    for name in CAPTURES:
        cap=CapturaEntradaM3(RAIZ/'evidencias'/name)
        for case in cap.d['cases']:
            tick=struct.unpack_from('<I',cap.blob(case['exit_dgroup']),0x4e17b4-0x494000)[0]
            result.append((case['name'],cap.memory(case).blocks,cap.blob(case['before']),EstadoCache(cap.blob(case['cache']['keys']),cap.blob(case['cache']['payloads']),case['cache']['cursor']),tick,cap.blob(case['after']),0x4085cb if case['name']=='sanctuary_health600_malus100' else 0,case['blits'],cap.blob(case['exit_dgroup'])))
    return result

def write_batch(path,rows):
    with Path(path).open('wb') as f:
        def u32(n):f.write(struct.pack('<I',n))
        def blob(b):u32(len(b));f.write(b)
        f.write(b'RLRF1500')
        for b in original_assets():blob(b)
        u32(len(rows))
        for name,blocks,surface,cache,tick,reference,stop,*extra in rows:
            u32(tick);u32(len(blocks))
            for a,b in blocks:u32(a);blob(b)
            blob(surface);blob(cache.registros);blob(cache.blocos_crus);u32(cache.proximo)

def run(binary=None,compare_python=False,rows=None):
    rows=cases() if rows is None else rows;binary=Path(binary or ROOT/'motor/target/debug/render_fixtures')
    with tempfile.TemporaryDirectory(prefix='rust-render-matrix-',dir=ROOT/'.local') as tmp:
        tmp=Path(tmp);write_batch(tmp/'input.bin',rows)
        done=subprocess.run([str(binary),str(tmp/'input.bin'),str(tmp/'out')],check=True,capture_output=True,text=True)
        print(done.stdout,flush=True)
        lines=done.stdout.splitlines();results=[]
        if compare_python:
            from graficos import Catalogo
            catalog=Catalogo()
        for i,(name,blocks,surface,cache,tick,expected,stop,*extra) in enumerate(rows):
            pixel=(tmp/f'out/{i}.pixels').read_bytes();raw=(tmp/f'out/{i}.cache').read_bytes();observations=(tmp/f'out/{i}.observations').read_text()
            actual_stop=0 if lines[i].endswith('None') else int(lines[i].split('Some((')[1].split(',')[0])
            row=dict(name=name,stop=actual_stop,expected_stop=stop,stop_equal=actual_stop==stop,sha256=sha(pixel),original_sha256=sha(expected),pixels_equal=pixel==expected if not stop else None)
            calls=[];effects=[]
            for line in observations.splitlines():
                if line.startswith('effect '):
                    _,effect_name,address,tail=line.split(' ',3);left,_,right=tail.partition('] ')
                    effects.append((effect_name,int(address),bytes(ast.literal_eval(left+']')),bytes(ast.literal_eval(right))))
                else:
                    routine,arguments=line.split(' ',1);calls.append([routine,*ast.literal_eval(arguments)])
            if extra:
                expected_calls,exit_dgroup=extra
                row['drawing_calls_equal']=calls==(expected_calls[:len(calls)] if stop else expected_calls)
                if not stop:
                    original=MemoriaEntradaM3(blocks);projected=bytearray(original.ler_mundo(0x494000,len(exit_dgroup)))
                    before_equal=True
                    for effect_name,address,old,new in effects:
                        offset=address-0x494000;before_equal &= projected[offset:offset+len(old)]==old;projected[offset:offset+len(new)]=new
                    struct.pack_into('<H',projected,0x49a04e-0x494000,struct.unpack_from('<I',raw,len(raw)-4)[0])
                    excluded={a+i for a in (0x508f70,0x4e17a4) for i in range(4)}
                    row['dgroup_equal']=all(a==b or 0x494000+i in excluded for i,(a,b) in enumerate(zip(projected,exit_dgroup)))
                    row['effect_old_bytes_equal']=before_equal
            if compare_python:
                py=renderizar_quadro(MemoriaEntradaM3(blocks),superficie_anterior=surface,cache=cache,catalogo=catalog,habitado=lambda i:inhabited(MemoriaEntradaM3(blocks),i),relogio=lambda:tick,hud=True)
                row.update(python_pixels_equal=pixel==py.pixels,python_cache_equal=raw==py.cache.registros+py.cache.blocos_crus+struct.pack('<I',py.cache.proximo),python_effects_equal=[(n,a,o.hex(),v.hex()) for n,a,o,v in effects]==list(py.efeitos))
            results.append(row)
        return dict(schema='rising-lands/rust-render-original-input-matrix/1',cases=len(rows),complete=sum(r['pixels_equal'] is True for r in results),stops=sum(r['stop']!=0 for r in results),mismatches=sum(not r['stop_equal'] or r['pixels_equal'] is False or r.get('python_pixels_equal',True) is False or any(r.get(k,True) is False for k in ('python_cache_equal','python_effects_equal','drawing_calls_equal','dgroup_equal','effect_old_bytes_equal')) for r in results),rows=results)
def main():
    p=argparse.ArgumentParser();p.add_argument('--binary');p.add_argument('--python',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
    if Path(a.output).exists():raise SystemExit('Refusing overwrite')
    renderer_pins();before=source_hashes();report=run(a.binary,a.python);after=source_hashes()
    binary=Path(a.binary or ROOT/'motor/target/debug/render_fixtures')
    report.update(metadata(),source_sha256=before,sources_unchanged=before==after,binary_sha256=sha(binary.read_bytes()),reference_pins=renderer_pins())
    Path(a.output).write_text(json.dumps(report,indent=1)+'\n');print({k:v for k,v in report.items() if k not in ('rows','source_sha256','reference_pins')});return bool(report['mismatches'])
if __name__=='__main__':sys.exit(main())
