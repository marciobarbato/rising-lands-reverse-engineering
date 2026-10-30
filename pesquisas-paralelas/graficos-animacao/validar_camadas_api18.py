"""Compare inhabited CAVE plans and structure gauges with the committed original leaf matrix."""
import json,struct,time
from pathlib import Path
from validar_sondas_graficos_m3 import CapturaSondaGrafica,CatalogoRastreado,AQUI
from validar_entrada_m3 import ArgumentosRasterM3
from quadro_jogo import _Composicao,EstadoTela,MundoQuadro,GLOBAIS_QUADRO
from render_quadro import BLOCOS
from hud_quadro import LeituraHud
from test_quadro_jogo import tabelas
from construcoes import tabelas_jogador

def validar():
    cap=CapturaSondaGrafica(AQUI/'evidencias/camadas-habitadas-api18.json.xz');catalog=CatalogoRastreado();rows=[];start=time.monotonic()
    for row in cap.d['rows']:
        m=cap.memory(row);l=m.ler_mundo;blocks={n:l(m.u32(slot),size) for n,slot,size in BLOCOS}
        world=MundoQuadro(**{n:blocks[n] for n in ('terreno','objetos','auxiliares','regioes','unidades','projeteis')},
            descoberta=[blocks[f'descoberta{i}'] for i in range(4)],iluminacao=[blocks[f'iluminacao{i}'] for i in range(4)],estruturas=l(0x49a0c8,276000))
        tela=EstadoTela({n:l(a,w) for n,a,w in GLOBAIS_QUADRO});sombra,ecl=tabelas()
        c=_Composicao(world,tela,cap.blob(row['before']),catalog,None,sombra,ecl)
        c.habitado=lambda i:True;c.leitura_entrada=LeituraHud(m);c.tabelas_jogador=tabelas_jogador()
        c.relogios_extra=(m.u32(0x508f80),m.u32(0x508f84));c.selecao_estruturas=struct.unpack('<5H',l(0x495be0,10))
        with ArgumentosRasterM3(catalog) as raster:c.batiments(row['registers']['EAX'],row['registers']['EDX'],row['cell'])
        pixels=sum(a!=b for a,b in zip(c.saida,cap.blob(row['after'])))
        dg=cap.blob(row['exit_dgroup']);projected=bytearray(l(0x494000,len(dg)))
        for _,a,old,new in tela.efeitos:projected[a-0x494000:a-0x494000+len(bytes.fromhex(new))]=bytes.fromhex(new)
        effects=[hex(0x494000+i) for i,(a,b) in enumerate(zip(projected,dg)) if a!=b]
        args=[] if raster.calls==row['blits'] else dict(python=raster.calls,native=row['blits'])
        item=dict(case=row['name'],pixels=pixels,arguments=args,effects=effects);rows.append(item)
        if pixels or args or effects:print(item,flush=True)
    return dict(cases=len(rows),mismatches=sum(bool(r['pixels'] or r['arguments'] or r['effects']) for r in rows),
        elapsed_seconds=round(time.monotonic()-start,3),rows=rows)

if __name__=='__main__':
    result=validar();(AQUI/'validacao/camadas-api18.json').write_text(json.dumps(result,indent=1)+'\n');print(result['cases'],result['mismatches'])
