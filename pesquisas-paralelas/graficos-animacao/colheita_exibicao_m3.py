"""Selected builder mining display, translated after exact native P5 evidence 2e24188."""
import json,struct
from pathlib import Path
import sobreposicoes_entrada_m3 as overlay
import corpo_tipos1_8 as raster

TABLES=json.loads(Path(__file__).with_name('camadas_colheita_m3.json').read_text())

def builder_work(c,r,x,y,index):
    spec=TABLES['builder_worker']
    if r[1]!=spec['type'] or r[2]!=spec['state']:return False
    if (r[0]!=spec['owner'] or c.camera!=spec['camera'] or r[0xdc] or r[0x99]
            or r[0xa5]!=spec['count'] or r[0xa4]>=spec['count'] or not 1<=r[0x91]<=16):
        c.parar(0x414a8a,'builder work outside captured owner/count/effect domain')
    # AffWorkEngin returns before the selected-target prefix for builder mining tasks 1/2.
    if r[0x89] in spec['return_before_overlays']:return True
    task=spec['tasks'].get(str(r[0x89]))
    if task is None:c.parar(0x414a8a,'uncaptured builder work task')
    active=bool(r[0xba] or r[0xbd] or c.tela.u('selecionada_unidade_u16')==index or c.tela.u('modo_selecao_u8'))
    dx,dy=struct.unpack_from('<bb',r,0x86);px,py=x+dx,y+dy
    if active:
        overlay.validar_unidade(c,r);overlay.quadro_selecao_unidade(c,r,px,py)
    from cave_scriptada_m3 import order_markers
    order_markers(c,r)
    base=task['empty_base'] if overlay.word(r,0xa)==0 else task['full_base']
    ident=base+((r[0x91]+1)//2)*task['stride']+r[0xa4]
    c.saida=raster.compor_sombra(c.saida,c.largura,c.altura,c.catalogo.quadro(10784),overlay.i16(px+2),overlay.i16(py+26),c.sombra,c.recorte())
    overlay.bob(c,px-spec['anchor'][0],py-spec['anchor'][1],ident)
    c._cauda_unidade_m3(r,x,y,index,active)
    return True
