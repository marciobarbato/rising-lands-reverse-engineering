"""Prepared type-2 normal body: exact raw count/phase and indexed layers."""
import struct
from graficos import localizar, QUANTIDADES, compor_indices
from composicao import compor_sombra


def _i16(value):return (value+32768)%65536-32768


def consultar_corpo_tipo2(registro,*,x,y):
    """276 runtime bytes, player 0, state 2/7, inactive effects/indicators.

    x/y are signed-i16 projected cell origins. The raw +A5 count and +A4
    phase are consumed directly; this function does not advance animation.
    """
    if len(registro)!=276:raise ValueError('Expected one 276-byte runtime unit record')
    if any(type(v) is not int or not -32768<=v<=32767 for v in (x,y)):
        raise ValueError('Projected coordinates must be signed i16')
    raw=bytes(registro)
    if raw[1]!=2:raise NotImplementedError('Only type 2 is verified by this API')
    if raw[0]!=0 or raw[2] not in (2,7):
        raise NotImplementedError('Only player 0 and normal states 2/7 are verified')
    if raw[0x99]!=0 or raw[0xdc]!=0 or raw[0xba]!=0 or struct.unpack_from('<H',raw,0x74)[0]<100:
        raise NotImplementedError('Oscillation, effects and auxiliary indicators must be inactive')
    direction,phase,count=raw[0x91],raw[0xa4],raw[0xa5]
    ident=(3202+((direction+1)//2-1)*count+phase)&65535
    if not 1<=ident<=sum(QUANTIDADES):
        raise NotImplementedError('Raw type-2 state selects an ID outside the verified catalog')
    dx,dy=struct.unpack_from('<bb',raw,0x86);xx,yy=x+dx,y+dy
    layers=[dict(**localizar(10784),x=_i16(xx+2),y=_i16(yy+26),operacao='sombra'),
        dict(**localizar(ident),x=_i16(xx-32),y=_i16(yy-16),operacao='copiar')]
    return dict(tipo=2,estado_u8=raw[2],direcao_u8=direction,fase_u8=phase,quantidade_u8=count,
        dx_i8=dx,dy_i8=dy,camadas=layers,evidencia='AffDeplaceEngin 0x412ece; anchor 0x410ff8')


def compor_corpo_tipo2(catalogo,destino,largura,altura,registro,*,x,y,tabela_sombra,recorte=None):
    """Return (new indexed bytes, plan); runtime record and inputs stay intact."""
    if any(type(v) is not int or v<=0 for v in (largura,altura)) or len(destino)!=largura*altura:
        raise ValueError('Invalid indexed surface')
    if len(tabela_sombra)!=256:raise ValueError('Expected an explicit 256-byte shadow table')
    plan=consultar_corpo_tipo2(registro,x=x,y=y);out=bytes(destino)
    for layer in plan['camadas']:
        frame=catalogo.quadro(layer['id_motor'])
        if layer['operacao']=='sombra':out=compor_sombra(out,largura,altura,frame,layer['x'],layer['y'],tabela_sombra,recorte)
        else:out=compor_indices(out,largura,altura,frame,layer['x'],layer['y'],recorte)
    return out,plan
