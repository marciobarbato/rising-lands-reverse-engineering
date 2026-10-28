"""Prepared mechanic/builder construction display with fixed branch strides."""
import struct
from graficos import localizar, compor_indices
from composicao import compor_sombra


def _i16(value):return (value+32768)%65536-32768


def consultar_construcao_grafica(registro,*,x,y,indice_u16,indice_selecionado_u16,modo_selecao_u8):
    """Read-only owner0/type6or7/state11or15 display; explicit selection inputs.

    BD must be zero irrespective of camera. Task89 is prepared, not advanced.
    A5/A6/A8 counts do not replace the fixed original construction strides.
    """
    if len(registro)!=276:raise ValueError('Expected one 276-byte unit record')
    if any(type(v) is not int or not -32768<=v<=32767 for v in (x,y)):
        raise ValueError('Projected origins must be signed i16')
    if type(indice_u16) is not int or not 0<=indice_u16<800:raise ValueError('Expected pool index0..799')
    if type(indice_selecionado_u16) is not int or not 0<=indice_selecionado_u16<=65535:
        raise ValueError('Expected raw u16 selected index')
    if type(modo_selecao_u8) is not int or not 0<=modo_selecao_u8<=255:raise ValueError('Expected raw u8 selection mode')
    raw=bytes(registro);kind,state=raw[1],raw[2]
    if raw[0]!=0 or kind not in (6,7) or state not in (11,15):
        raise NotImplementedError('Only owner0/types6or7/states11or15 are verified')
    if raw[0xbd]!=0 or indice_u16==indice_selecionado_u16 or modo_selecao_u8!=0:
        raise NotImplementedError('Construction selection overlays are not implemented')
    if raw[0xdc]!=0 or raw[0xba]!=0 or struct.unpack_from('<H',raw,0x74)[0]<100:
        raise NotImplementedError('Effects and auxiliary indicators must be inactive')
    task,direction,phase=raw[0x89],raw[0x91],raw[0xa4];bag=struct.unpack_from('<H',raw,0xa)[0]
    plan=dict(tipo=kind,estado_u8=state,tarefa_89_u8=task,direcao_u8=direction,fase_u8=phase,
        bolsa_u16=bag,camadas=[],evidencia='AffConstruireBatiment 0x414495..0x414a8a')
    if task>1:plan['motivo']='no_body';return plan
    if kind==7:base,stride,ax,ay=((0x53a if bag==0 else 0x5ba),8,26,26) if task==0 else (0x57a,8,26,26)
    else:base,stride,ax,ay=((0xb9a if bag==0 else 0xbda),8,16,20) if task==0 else (0xc5e,4,16,20)
    ident=(base+((direction+1)//2)*stride+phase)&65535
    dx,dy=struct.unpack_from('<bb',raw,0x86);xx,yy=x+dx,y+dy
    plan['camadas']=[dict(**localizar(10784),x=_i16(xx+2),y=_i16(yy+26),operacao='sombra'),
        dict(**localizar(ident),x=_i16(xx-ax),y=_i16(yy-ay),operacao='copiar')]
    plan['motivo']='draw';return plan


def compor_construcao_grafica(catalogo,destino,largura,altura,registro,*,x,y,tabela_sombra,
        indice_u16,indice_selecionado_u16,modo_selecao_u8,recorte=None):
    """Return(new indexed bytes,plan); no tasks/economy/world state is changed."""
    if any(type(v) is not int or v<=0 for v in (largura,altura)) or len(destino)!=largura*altura:
        raise ValueError('Invalid indexed surface')
    if len(tabela_sombra)!=256:raise ValueError('Expected an explicit256-byte shadow table')
    plan=consultar_construcao_grafica(registro,x=x,y=y,indice_u16=indice_u16,
        indice_selecionado_u16=indice_selecionado_u16,modo_selecao_u8=modo_selecao_u8);out=bytes(destino)
    for layer in plan['camadas']:
        frame=catalogo.quadro(layer['id_motor'])
        if layer['operacao']=='sombra':out=compor_sombra(out,largura,altura,frame,layer['x'],layer['y'],tabela_sombra,recorte)
        else:out=compor_indices(out,largura,altura,frame,layer['x'],layer['y'],recorte)
    return out,plan
