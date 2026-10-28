"""Prepared type-0/type-2 attack bodies; no simulation or phase production."""
import struct
from graficos import localizar, QUANTIDADES, compor_indices
from composicao import compor_sombra


def _i16(value):return (value+32768)%65536-32768


def consultar_ataque_grafico(registro,*,x,y,indice_u16,camera_u8,indice_selecionado_u16,modo_selecao_u8):
    """Read one 276-byte record plus the exact native selection inputs.

    Only player 0, type 0/2, inactive effects/indicators and attack-routed
    states 1/22/24 are supported. Raw +8A values do not imply their producer.
    """
    if len(registro)!=276:raise ValueError('Expected one 276-byte unit record')
    if any(type(v) is not int or not -32768<=v<=32767 for v in (x,y)):
        raise ValueError('Projected origins must be signed i16')
    if type(indice_u16) is not int or not 0<=indice_u16<800:
        raise ValueError('Expected a pool index in 0..799')
    if type(indice_selecionado_u16) is not int or not 0<=indice_selecionado_u16<=65535:
        raise ValueError('Expected a raw u16 selected index')
    if any(type(v) is not int or not 0<=v<=255 for v in (camera_u8,modo_selecao_u8)):
        raise ValueError('Camera and selection mode must be raw u8')
    raw=bytes(registro);kind,state,aux=raw[1],raw[2],raw[0x8a]
    if kind not in (0,2) or raw[0]!=0:raise NotImplementedError('Only player-0 types 0/2 are verified')
    if not ((state in (1,24) and 1<=aux<=3) or (state==22 and aux==1)):
        raise NotImplementedError('Record does not select the supported attack display handler')
    if raw[0xdc]!=0 or raw[0xba]!=0 or struct.unpack_from('<H',raw,0x74)[0]<100:
        raise NotImplementedError('Effects and auxiliary indicators must be inactive')
    if (raw[0xbd]!=0 and camera_u8==raw[0]) or indice_selecionado_u16==indice_u16 or modo_selecao_u8!=0:
        raise NotImplementedError('Selection overlays are not implemented')
    direction,phase,count=raw[0x91],raw[0xa4],raw[0xa6]
    base,ax,ay=(2146,40,22) if kind==0 else (3266,32,16)
    ident=(base+((direction+1)//2-1)*count+phase)&65535
    if not 1<=ident<=sum(QUANTIDADES):raise NotImplementedError('Raw attack state selects an out-of-catalog ID')
    dx,dy=struct.unpack_from('<bb',raw,0x86);xx,yy=x+dx,y+dy
    layers=[dict(**localizar(10784),x=_i16(xx+2),y=_i16(yy+26),operacao='sombra'),
        dict(**localizar(ident),x=_i16(xx-ax),y=_i16(yy-ay),operacao='copiar')]
    return dict(tipo=kind,estado_u8=state,auxiliar_8a_u8=aux,direcao_u8=direction,fase_u8=phase,
        quantidade_ataque_u8=count,camadas=layers,evidencia='AffAttaqueEngin 0x413a04/0x413bc7')


def compor_ataque_grafico(catalogo,destino,largura,altura,registro,*,x,y,tabela_sombra,
        indice_u16,camera_u8,indice_selecionado_u16,modo_selecao_u8,recorte=None):
    """Return (new indexed bytes, plan); all runtime inputs stay unchanged."""
    if any(type(v) is not int or v<=0 for v in (largura,altura)) or len(destino)!=largura*altura:
        raise ValueError('Invalid indexed surface')
    if len(tabela_sombra)!=256:raise ValueError('Expected an explicit 256-byte shadow table')
    plan=consultar_ataque_grafico(registro,x=x,y=y,indice_u16=indice_u16,camera_u8=camera_u8,
        indice_selecionado_u16=indice_selecionado_u16,modo_selecao_u8=modo_selecao_u8);out=bytes(destino)
    for layer in plan['camadas']:
        frame=catalogo.quadro(layer['id_motor'])
        if layer['operacao']=='sombra':out=compor_sombra(out,largura,altura,frame,layer['x'],layer['y'],tabela_sombra,recorte)
        else:out=compor_indices(out,largura,altura,frame,layer['x'],layer['y'],recorte)
    return out,plan
