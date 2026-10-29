"""Locate the first default-renderer stop in each scripted probe, without a text boundary adapter."""
import json
from pathlib import Path
from validar_sondas_graficos_m3 import CapturaSondaGrafica,CatalogoRastreado,ArgumentosRasterM3,AQUI,sha

def validar_prefixos():
    probes=[];catalog=CatalogoRastreado()
    for name in ('P1','P2','P3'):
        cap=CapturaSondaGrafica(AQUI/f'evidencias/sonda-render-{name}-api17.json.xz');previous=cache=None;count=0
        for row in cap.d['rows']:
            with ArgumentosRasterM3(catalog) as raster:result=cap.render(row,catalog,previous,cache)
            if result.parada:
                boundary=row['text_boundaries'][0]
                assert result.parada['endereco']=='0x00459454'
                assert sha(result.pixels)==boundary['surface_before']
                assert raster.calls==row['blits'][:boundary['blits_before']]
                probes.append(dict(probe=name,captured_frames=cap.d['frames'],chained_equal_prefix=count,first_stop_frame=row['frame'],
                    stop=result.parada,native_partial_surface_equal=True,native_partial_arguments_equal=True))
                break
            assert result.pixels==cap.blob(row['after'])
            assert raster.calls==row['blits']
            count+=1;previous,cache=result.pixels,result.cache
        else:raise AssertionError('Expected the recorded AffText dependency')
    return dict(schema='rising-lands/m3-default-render-prefixes/1',probes=probes)

if __name__=='__main__':
    output=AQUI/'validacao/prefixos-sondas-api17.json';result=validar_prefixos();output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
