"""Compare the complete AffText provider with all original bitmap-call buffers and raster arguments."""
import argparse,base64,json,lzma,zlib
from pathlib import Path
from graficos import Catalogo
from texto_afftext_bitmap import compor_texto_afftext
from validar_objetivos_s1 import AQUI,sha

def validar():
    path=AQUI/'evidencias/glifos-afftext-nativos.json.xz';raw=path.read_bytes();d=json.loads(lzma.decompress(raw))
    assert len(d['rows'])==270 and d['language']==[0,0]
    assert d['executable_sha256']=='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
    assert d['source_sha256']==sha((AQUI/'capturar_glifos_afftext.py').read_bytes())
    baseline=bytes((x*7+y*11)%256 for y in range(600) for x in range(800));assert sha(baseline)==d['baseline_sha256']
    catalog=Catalogo();rows=[]
    for i,row in enumerate(d['rows']):
        assert row['returned'] and row['stack_balanced'] and not row['changed_blocks']
        request=dict(row['request']);request['text']=bytes.fromhex(request.pop('text_hex'))
        out,plan=compor_texto_afftext(catalog,baseline,request=request,recorte=row['clip'],idioma_u32=0,multibyte_u32=0)
        expected=zlib.decompress(base64.b64decode(row['pixels_zlib']));assert sha(expected)==row['surface_sha256']
        pixels=sum(a!=b for a,b in zip(out,expected))
        native=[['PasteBobCmp',*r[1:]] for r in row['blits']];assert all(r[0]=='0x45b247' for r in row['blits'])
        args=plan['chamadas']!=native
        assert not(pixels or args),(i,request,pixels,args,plan['chamadas'][:3],native[:3])
        rows.append(dict(case=i,font=request['font'],equal=True,pixel_mismatches=pixels,argument_mismatches=int(args),
            drawing_calls=len(native),sha256=sha(out)))
    return dict(schema='rising-lands/afftext-bitmap-comparison/1',cases=270,equal=270,mismatches=0,
        glyph_calls=sum(r['drawing_calls'] for r in rows),native_capture_sha256=sha(raw),
        sources_sha256={n:sha((AQUI/n).read_bytes()) for n in ('texto_afftext_bitmap.py','validar_glifos_afftext.py')},rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();d=validar()
    Path(a.output).write_text(json.dumps(d,indent=1)+'\n');print(d['equal'],'/',d['cases'],'buffers;',d['glyph_calls'],'glyph calls;0 mismatches')
