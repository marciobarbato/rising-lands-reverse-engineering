"""Data-driven API-1.8 layer plans, translated after native evidence cbe2604.

Only the inhabited owner-0 mode-5 CAVE and the captured sanctuary/CAVE bag slices are accepted. Plans contain
original raster operation, engine bob ID, signed position and owner. No emulator or simulated-state update is used.
"""
import json
from pathlib import Path
from sobreposicoes_entrada_m3 import bob,word,i16
import sobreposicoes_entrada_m3 as overlay
import corpo_tipos1_8 as raster
from graficos import TIPOS
import struct

TABLES=json.loads((Path(__file__).with_name('camadas_m3_api18.json')).read_text())

def work(c,r,x,y,index,overlay_active):
    spec=TABLES['worker']
    if r[1]!=spec['type'] or r[2]!=spec['state']:return False
    if r[0]!=0 or c.camera!=0 or r[0xdc] or r[0x99] or r[0xa5]!=spec['count'] or r[0xa4]>=8 or not 1<=r[0x91]<=16:
        c.parar(0x414a8a,'worker outside captured owner/count/effect bounds')
    task=spec['tasks'].get(str(r[0x89]))
    if task is None:c.parar(0x414a8a,'uncaptured worker task')
    from cave_scriptada_m3 import order_markers
    order_markers(c,r)
    dx,dy=struct.unpack_from('<bb',r,0x86);px,py=x+dx,y+dy
    base=task.get('base')
    if base is None:base=task['empty_base'] if word(r,0xa)==0 else task['full_base']
    ident=base+((r[0x91]+1)//2)*task['stride']+r[0xa4]
    c.saida=raster.compor_sombra(c.saida,c.largura,c.altura,c.catalogo.quadro(10784),i16(px+2),i16(py+26),c.sombra,c.recorte())
    bob(c,px-spec['anchor'][0],py-spec['anchor'][1],ident)
    c._cauda_unidade_m3(r,x,y,index,overlay_active)
    return True

def normal_extension(c,r,x,y,index,overlay_active):
    if r[2] not in TABLES['normal_extensions'].get(str(r[1]),[]):return False
    if r[0]!=0 or c.camera!=0 or r[0x99] or r[0xdc] or r[0xa5]!=8 or r[0xa4]>=8 or not 1<=r[0x91]<=16:
        c.parar(0x41591f,'normal state extension outside captured owner/count/effect bounds')
    spec=TIPOS[r[1]];dx,dy=struct.unpack_from('<bb',r,0x86);px,py=x+dx,y+dy
    base=spec['bases'][int(word(r,0xa)!=0)] if len(spec['bases'])==2 else spec['bases'][0]
    ident=base+((r[0x91]+1)//2-1)*r[0xa5]+r[0xa4]
    c.saida=raster.compor_sombra(c.saida,c.largura,c.altura,c.catalogo.quadro(10784),i16(px+2),i16(py+26),c.sombra,c.recorte())
    bob(c,px-spec['ancora'][0],py-spec['ancora'][1],ident)
    c._cauda_unidade_m3(r,x,y,index,overlay_active)
    return True

def plano_cave(c,r,x,y,cell):
    spec=TABLES['cave'];m=c.leitura_entrada
    if r[4]!=spec['owner'] or c.camera!=0 or r[5]!=spec['mode'] or word(r,6):
        c.parar(0x40958e,'inhabited CAVE outside captured owner-0 mode-5 no-fire domain')
    if m is None or c.relogios_extra is None:c.parar(0x40958e,'inhabited CAVE requires live table reads and clocks')
    level=m.u8(0x4dfb30+6*r[4])
    if level!=0 or r[0x74] not in (0,1) or r[0x75] not in (0,1) or r[0x76]>15:
        c.parar(0x40958e,'CAVE flags/player level outside the native matrix')
    x,y=i16(x-spec['anchor'][0]),i16(y-spec['anchor'][1]);clocks=(c.tela.u('quadro_u32'),*c.relogios_extra)
    layers=[]
    for definition in spec['layers']:
        if definition.get('when_full') and not (r[0x76]==15 and r[0x75]):continue
        ident=definition['base'];dx,dy=definition['offset']
        if 'clock' in definition and ('animate_if_byte' not in definition or r[definition['animate_if_byte']]):
            ident+=(clocks[definition['clock']]+(cell if definition.get('cell_phase') else 0))&definition['mask']
        if definition.get('player_level'):ident+=level
        if 'variant_byte' in definition:
            variant=r[definition['variant_byte']]
            if variant>=definition['split']:ident=definition['upper_base'];dy=definition['upper_y']
            ident+=variant
        layers.append(dict(op=definition['op'],id=ident,x=i16(x+dx),y=i16(y+dy),owner=r[4] if definition['op']=='player' else None))
    return layers

def cave(c,r,x,y,cell):
    for layer in plano_cave(c,r,x,y,cell):bob(c,layer['x'],layer['y'],layer['id'],layer['owner'])

def selecao(c,r,cell,index,*,frame,gauge):
    # S1 original frame2014: the selected sanctuary continues drawing while
    # SortieTroupe holds mode4. The caller still excludes mode3 before this tail.
    if r[8] not in (2,3) or not (r[5]==5 or r[8]==2 and r[5]==4) or r[4]!=0 or c.camera!=0 or c.leitura_entrada is None:
        c.parar(0x4022c8 if frame else 0x4020ec,'structure selection outside captured API-1.8 domain')
    spec=TABLES['selection'][str(r[8])];ox,oy=c.tela.palavras('origem')
    x,y=(cell%256-ox)*32-spec['anchor'][0],(cell//256-oy)*32-spec['anchor'][1]
    if frame:
        phase=c.relogios_extra[0]&7
        for ident,px,py in ((0x2a79,x+phase-20,y+phase),(0x2a78,x+phase-20,y+spec['height']-phase),
                           (0x2a7a,x+spec['frame_right']-phase,y+phase),(0x2a77,x+spec['frame_right']-phase,y+spec['height']-phase)):
            bob(c,px,py,ident,r[4])
    if not gauge:return
    maximum=c.leitura_entrada.u16(0x495d90+52*r[8]);hp,damage=word(r,0xa),word(r,6);capacity,count=word(r,0xe),word(r,0xc)
    # Native S1 pools through5090 include full-health sanctuary bags2..8.
    counts=spec['counts'] + ([2,3,4,5,6] if r[8]==2 else [])
    if maximum!=spec['maximum'] or hp!=maximum or damage or capacity!=spec['capacity'] or count not in counts:
        c.parar(0x4020ec,'structure gauge health/capacity outside API-1.8 matrix')
    if r[0x4e:0x4e+capacity]!=bytes([1])*count+bytes(capacity-count):c.parar(0x401a70,'structure bag codes outside captured compact troop slots')
    gx,gy=i16(x-23),i16(y+spec['gauge_y'])
    if ox==0 and gx<0:gx=0
    bob(c,gx+9,gy,0x2a7b);overlay.filled(c,gx+10,gy+1,gx+14,gy+60,48)
    for i in range(capacity):
        px,py=gx-(9 if i>=8 else 0),gy+8*(i%8)
        bob(c,px,py,0x2a3c if r[0x4e+i]==1 else 0x2a3b,r[4] if r[0x4e+i]==1 else None)
    if r[8]==3:
        if c.leitura_entrada.u8(0x4dfb30+6*r[4])!=0:c.parar(0x401a70,'CAVE technology markers above captured level zero')
        for i in range(7):bob(c,gx+63+8*i,gy+48,0x2a3b)
