"""Compare normal public rendering with glyph-enabled original AffGame full buffers."""
import argparse, base64, json, lzma, struct, zlib, subprocess
from pathlib import Path
from validar_colheita_graficos import CapturaLimitada
from validar_entrada_m3 import AQUI, ArgumentosRasterM3, CatalogoRastreado, sha
from validar_janelas_s1_graficos import habitado
from render_quadro import renderizar_quadro
from validar_entrada_m3 import MemoriaEntradaM3
from efeitos_logicos_exibicao import desenhar_jogo,DependenciaExibicao


def validar(path):
    raw=Path(path).read_bytes(); native=json.loads(lzma.decompress(raw))
    producer=(AQUI/'capturar_affgame_glifos.py').read_bytes()
    if native['source_sha256']!=sha(producer):
        producer=subprocess.check_output(['git','show','bc38477:pesquisas-paralelas/graficos-animacao/capturar_affgame_glifos.py'],cwd=AQUI)
    assert native['source_sha256']==sha(producer)
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
        if row.get('declared_writes'):
            blocks=[];applied=set()
            for base,data in m.blocks:
                data=bytearray(data)
                for index,write in enumerate(row['declared_writes']):
                    address=int(write['address'],16);value=bytes.fromhex(write['bytes'])
                    if base<=address and address+len(value)<=base+len(data):
                        data[address-base:address-base+len(value)]=value;applied.add(index)
                blocks.append((base,bytes(data)))
            assert len(applied)==len(row['declared_writes'])
            m=MemoriaEntradaM3(blocks)
        logic_stop=None;logic_effects=()
        if 'world_unchanged' in row:
            assert all(row['world_unchanged'].values())
            try:logic_effects=desenhar_jogo(m,habitado=lambda i:habitado(m,i)).escritas
            except DependenciaExibicao as error:logic_stop=dict(address=hex(error.sitio),reason=error.motivo)
        with ArgumentosRasterM3(catalog) as raster:
            result=renderizar_quadro(m, superficie_anterior=cap.blob(source['before']),
                cache=cap.cache_entry(source), catalogo=catalog, hud=True,
                habitado=lambda i: habitado(m,i),
                relogio=lambda:struct.unpack_from('<I',cap.blob(source['exit_dgroup']),0x4e17b4-0x494000)[0])
        expected=zlib.decompress(base64.b64decode(native['blobs'][row['after']]))
        assert sha(expected)==row['after'] and row['baseline_equal']
        dg=zlib.decompress(base64.b64decode(native['blobs'][row['exit_dgroup']]))
        assert sha(dg)==row['exit_dgroup']
        logic_bad=[hex(a) for a,n,v in logic_effects if dg[a-0x494000:a-0x494000+n]!=v.to_bytes(n,'little')]
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
        if 'case' in row:item['case']=row['case']
        if 'world_unchanged' in row:item.update(logic_stop=logic_stop,logic_write_mismatches=logic_bad)
        item['equal']=result.parada is None and item['pixel_mismatches']==0 and item['raster_equal'] and not(effects or logic_stop or logic_bad)
        rows.append(item)
        if not item['equal']:
            print(item, 'raster counts',len(raster.calls),len(row['blits']),flush=True)
            print([(a,b) for a,b in zip(raster.calls,row['blits']) if a!=b][:3],flush=True)
            break
    return dict(schema='rising-lands/affgame-glyphs-comparison/1',capture_sha256=sha(raw),
        capture_file=Path(path).name,native_parent=native.get('derived_partition'),
        sources_sha256={n:sha((AQUI/n).read_bytes()) for n in ('render_quadro.py','hud_scriptado_m3.py',
            'texto_afftext_bitmap.py','validar_entrada_m3.py','validar_affgame_glifos.py',
            'quadro_jogo.py','hud_quadro.py','camadas_exibicao_m3.py','cave_scriptada_m3.py',
            'sobreposicoes_entrada_m3.py','alertas_s1_graficos.py','corpos_s1_tardios_graficos.py',
            'ambiente_graficos_core.py',
            'efeitos_logicos_exibicao.py')},
        expected=len(native['rows']),equal=sum(r['equal'] for r in rows),rows=rows)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--capture',action='append',required=True);p.add_argument('--output',required=True)
    a=p.parse_args(); results=[validar(path) for path in a.capture]
    d=results[0]
    if len(results)>1:
        assert all(r['sources_sha256']==d['sources_sha256'] for r in results)
        d=dict(schema='rising-lands/affgame-glyphs-set-comparison/1',sources_sha256=d['sources_sha256'],
            parts=[{k:v for k,v in r.items() if k not in ('rows','sources_sha256')} for r in results],
            expected=sum(r['expected'] for r in results),equal=sum(r['equal'] for r in results),
            rows=[row for r in results for row in r['rows']])
    Path(a.output).write_text(json.dumps(d,indent=1)+'\n')
    print(d['equal'],'/',d['expected'],'full surfaces',flush=True)
    raise SystemExit(d['equal']!=d['expected'])
