"""Compare normal public rendering with glyph-enabled original AffGame full buffers."""
import argparse, base64, json, lzma, struct, zlib
from pathlib import Path
from validar_colheita_graficos import CapturaLimitada
from validar_entrada_m3 import AQUI, ArgumentosRasterM3, CatalogoRastreado, sha
from validar_janelas_s1_graficos import habitado
from render_quadro import renderizar_quadro


def validar(path):
    raw=Path(path).read_bytes(); native=json.loads(lzma.decompress(raw))
    assert native['source_sha256']==sha((AQUI/'capturar_affgame_glifos.py').read_bytes())
    assert native['executable_sha256']=='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
    catalog=CatalogoRastreado(); rows=[]; cap=None; name=None
    assert len(native['glyph_metrics'])==1344
    for glyph in native['glyph_metrics']:
        q=catalog.quadro(glyph['id'])
        assert (q.largura,q.altura)==(glyph['width'],glyph['height'])
    for row in native['rows']:
        if row['source'] != name:
            name=row['source']; cap=CapturaLimitada(AQUI/'evidencias'/name)
            assert cap.sha==native['inputs'][name]
        source=next(r for r in cap.d['rows'] if r['frame']==row['frame'])
        m=cap.memory(source)
        with ArgumentosRasterM3(catalog) as raster:
            result=renderizar_quadro(m, superficie_anterior=cap.blob(source['before']),
                cache=cap.cache_entry(source), catalogo=catalog, hud=True,
                habitado=lambda i: habitado(m,i),
                relogio=lambda:struct.unpack_from('<I',cap.blob(source['exit_dgroup']),0x4e17b4-0x494000)[0])
        expected=zlib.decompress(base64.b64decode(native['blobs'][row['after']]))
        assert sha(expected)==row['after'] and row['baseline_equal']
        dg=zlib.decompress(base64.b64decode(native['blobs'][row['exit_dgroup']]))
        assert sha(dg)==row['exit_dgroup']
        projected=bytearray(m.ler_mundo(0x494000,len(dg)))
        for _,address,old,new in result.efeitos:
            value=bytes.fromhex(new)
            if 0x494000<=address and address+len(value)<=0x523000:
                projected[address-0x494000:address-0x494000+len(value)]=value
        struct.pack_into('<H',projected,0x49a04e-0x494000,result.cache.proximo)
        ignored={a+i for a in (0x508f70,0x4e17a4) for i in range(4)}
        effects=[hex(0x494000+i) for i,(a,b) in enumerate(zip(projected,dg)) if a!=b and 0x494000+i not in ignored]
        item=dict(source=name,frame=row['frame'],stop=result.parada,text_calls=row['text_calls'],
            pixel_mismatches=sum(a!=b for a,b in zip(expected,result.pixels)),
            effect_mismatches=effects,raster_equal=raster.calls==row['blits'],sha256=sha(result.pixels),native_sha256=row['after'])
        item['equal']=result.parada is None and item['pixel_mismatches']==0 and item['raster_equal'] and not effects
        rows.append(item)
        if not item['equal']:
            print(item, 'raster counts',len(raster.calls),len(row['blits']),flush=True)
            print([(a,b) for a,b in zip(raster.calls,row['blits']) if a!=b][:3],flush=True)
            break
    return dict(schema='rising-lands/affgame-glyphs-comparison/1',capture_sha256=sha(raw),
        sources_sha256={n:sha((AQUI/n).read_bytes()) for n in ('render_quadro.py','hud_scriptado_m3.py',
            'texto_afftext_bitmap.py','validar_entrada_m3.py','validar_affgame_glifos.py')},
        expected=len(native['rows']),equal=sum(r['equal'] for r in rows),rows=rows)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capture',required=True);p.add_argument('--output',required=True)
    a=p.parse_args(); d=validar(a.capture);Path(a.output).write_text(json.dumps(d,indent=1)+'\n')
    print(d['equal'],'/',d['expected'],'full surfaces',flush=True)
    raise SystemExit(d['equal']!=d['expected'])
