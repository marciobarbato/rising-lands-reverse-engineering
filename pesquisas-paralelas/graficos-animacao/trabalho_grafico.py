"""Prepared worker display; raw task branches and local overlay bypasses."""
import struct
from graficos import localizar, compor_indices
from composicao import compor_sombra


def _i16(value):return (value+32768)%65536-32768


def consultar_trabalho_grafico(registro,*,x,y,indice_u16,camera_u8,indice_selecionado_u16,modo_selecao_u8):
    """Prepared owner0/effects0/state5 records of types5/6/7; no task update."""
    if len(registro)!=276:raise ValueError('Expected one 276-byte runtime record')
    if any(type(v) is not int or not -32768<=v<=32767 for v in (x,y)):
        raise ValueError('Projected origins must be signed i16')
    if type(indice_u16) is not int or not 0<=indice_u16<800:raise ValueError('Expected pool index0..799')
    if type(indice_selecionado_u16) is not int or not 0<=indice_selecionado_u16<=65535:
        raise ValueError('Expected raw u16 selected index')
    if any(type(v) is not int or not 0<=v<=255 for v in (camera_u8,modo_selecao_u8)):
        raise ValueError('Camera and mode must be raw u8')
    raw=bytes(registro);kind,task=raw[1],raw[0x89]
    if raw[0]!=0 or kind not in (5,6,7) or raw[2]!=5 or raw[0xdc]!=0:
        raise NotImplementedError('Only owner0/effects0/state5 types5/6/7 are verified')
    if raw[0xbd]!=0 and camera_u8==raw[0]:raise NotImplementedError('Selected-target prefix is not implemented')
    bypass=(kind==7 and task in (1,2)) or (kind==6 and task==3)
    if not bypass:
        if indice_u16==indice_selecionado_u16 or modo_selecao_u8!=0:
            raise NotImplementedError('Work selection overlay is not implemented')
        if raw[0xba]!=0 or struct.unpack_from('<H',raw,0x74)[0]<100:
            raise NotImplementedError('Post-body indicators must be inactive')
    bag=struct.unpack_from('<H',raw,0xa)[0];direction,phase=raw[0x91],raw[0xa4]
    plan=dict(tipo=kind,tarefa_89_u8=task,bolsa_u16=bag,direcao_u8=direction,fase_u8=phase,
        pular_pos_corpo=bypass,camadas=[],evidencia='AffWorkEngin 0x414a8a..0x415496')
    if kind==5:
        ax,ay=11,11
        if task in (0,2,3):base,stride=(0x63a if bag==0 else 0x69a),8
        elif task==1:base,stride=0x67e,4
        else:plan['motivo']='no_body';return plan
    elif kind==6:
        ax,ay=16,20
        if task in (0,1):base,stride=(0xb9a if bag==0 else 0xbda),8
        elif task==2:base,stride=0xbda,8
        else:plan['motivo']='no_body';return plan
    else:
        ax,ay=26,26
        if task in (0,3,4,5):base,stride=(0x53a if bag==0 else 0x5ba),8
        elif task==12:base,stride=0x57a,8
        else:plan['motivo']='no_body';return plan
    ident=(base+((direction+1)//2)*stride+phase)&65535
    dx,dy=struct.unpack_from('<bb',raw,0x86);xx,yy=x+dx,y+dy
    plan['camadas']=[dict(**localizar(10784),x=_i16(xx+2),y=_i16(yy+26),operacao='sombra'),
        dict(**localizar(ident),x=_i16(xx-ax),y=_i16(yy-ay),operacao='copiar')]
    plan['motivo']='draw';return plan


def compor_trabalho_grafico(catalogo,destino,largura,altura,registro,*,x,y,tabela_sombra,
        indice_u16,camera_u8,indice_selecionado_u16,modo_selecao_u8,recorte=None):
    """Return(new indexed bytes,plan); no callbacks/economy/world changes."""
    if any(type(v) is not int or v<=0 for v in (largura,altura)) or len(destino)!=largura*altura:
        raise ValueError('Invalid indexed surface')
    if len(tabela_sombra)!=256:raise ValueError('Expected an explicit256-byte shadow table')
    plan=consultar_trabalho_grafico(registro,x=x,y=y,indice_u16=indice_u16,camera_u8=camera_u8,
        indice_selecionado_u16=indice_selecionado_u16,modo_selecao_u8=modo_selecao_u8);out=bytes(destino)
    for layer in plan['camadas']:
        frame=catalogo.quadro(layer['id_motor'])
        if layer['operacao']=='sombra':out=compor_sombra(out,largura,altura,frame,layer['x'],layer['y'],tabela_sombra,recorte)
        else:out=compor_indices(out,largura,altura,frame,layer['x'],layer['y'],recorte)
    return out,plan
