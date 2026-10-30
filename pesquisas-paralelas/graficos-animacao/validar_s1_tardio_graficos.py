"""Chained full-surface/raster/effect proof of the bounded original late-S1 interval.

Historical S1 surfaces retain their explicitly recorded text boundaries. Separate
AffText-enabled original calls compare the normal default, with actual glyphs.
This is a render proof; no whole-state reconstructed mission acceptance is claimed.
"""
import argparse,json,time
from pathlib import Path
from validar_colheita_graficos import CapturaLimitada
from validar_janelas_s1_graficos import comparar,registros,AQUI,sha

CAPTURES=(
    's1-render-part-11251-11378.json.xz','s1-render-part-11379-11506.json.xz',
    's1-render-part-11507-11634.json.xz','s1-render-part-11635-11750.json.xz',
    's1-render-11751-11900.json.xz','s1-render-11901-12000.json.xz',
    's1-render-12001-12220.json.xz','s1-render-12221-12500.json.xz')
SOURCES=('render_quadro.py','quadro_jogo.py','hud_quadro.py','camadas_exibicao_m3.py',
    'cave_scriptada_m3.py','sobreposicoes_entrada_m3.py','hud_scriptado_m3.py',
    'corpos_s1_tardios_graficos.py','alertas_s1_graficos.py','texto_afftext_bitmap.py',
    'ambiente_graficos_core.py',
    'efeitos_logicos_exibicao.py','validar_entrada_m3.py','validar_janelas_s1_graficos.py',
    'validar_s1_tardio_graficos.py')


def validar(names=CAPTURES):
    started=time.monotonic();refs=registros();captures=[];previous=None;end=None;changes=set();world=0
    for name in names:
        cap=CapturaLimitada(AQUI/'evidencias'/name)
        assert cap.d['world_audit_observer']['source_sha256']==sha((AQUI/'capturar_s1_tardio_graficos.py').read_bytes())
        for row in cap.d['rows']:
            assert all(v['equal'] and v['before']==v['after'] for v in row['world_effect_audit'].values())
            changes.update(row['changing_dgroup_bytes']);world+=1
        result=comparar(AQUI/'evidencias'/name,refs,previous if end==cap.d['frames'][0]-1 else None,cap)
        previous=result.pop('_exit');end=result['native_frames'][1] if result['first_difference'] is None else None
        captures.append(result)
    rows=[r for c in captures for r in c['rows']]
    return dict(schema='rising-lands/late-s1-render-comparison/1',method=__doc__,render_api=[1,12],
        sources_sha256={n:sha((AQUI/n).read_bytes()) for n in SOURCES},
        frames=[11251,12500],expected=1250,equal=sum(r['equal'] for r in rows),compared=len(rows),
        world_unchanged_native_calls=world,changing_dgroup_bytes=sorted(changes,key=lambda x:int(x,16)),
        shared_rng_cursor_changed='0x4e1d18' in changes,captures=captures,
        elapsed_seconds=round(time.monotonic()-started,3))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',action='append');p.add_argument('--output',required=True)
    a=p.parse_args();d=validar(a.capture or CAPTURES);Path(a.output).write_text(json.dumps(d,indent=1)+'\n')
    print(d['equal'],'/',d['expected'],'full S1 surfaces',flush=True)
    raise SystemExit(d['equal']!=d['expected'])
