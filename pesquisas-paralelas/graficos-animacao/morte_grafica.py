"""Prepared corpse rendering with original counter-dependent copy/mask passes."""
import struct
from graficos import localizar, QUANTIDADES, compor_indices
from composicao import compor_sombra


SPEC={0:(0x8b2,40,22),2:(0xd12,32,16),5:(0x6e2,11,11),
      6:(0xc22,16,20),7:(0x602,26,26),9:(0x762,19,14)}


def _i16(value):return (value+32768)%65536-32768


def consultar_morte_grafica(registro,*,x,y):
    """One prepared276 record, owner0/effects0, state4, six verified types.

    CounterC2 and phaseA4 are raw inputs. This function neither advances death
    nor removes the unit. The original death handler reads no selection globals.
    """
    if len(registro)!=276:raise ValueError('Expected one 276-byte runtime record')
    if any(type(v) is not int or not -32768<=v<=32767 for v in (x,y)):
        raise ValueError('Projected origins must be signed i16')
    raw=bytes(registro);kind=raw[1]
    if kind not in SPEC or raw[0]!=0 or raw[2]!=4 or raw[0xdc]!=0:
        raise NotImplementedError('Only prepared owner-0/effects-0 state-4 bodies of types0/2/5/6/7/9 are verified')
    counter=struct.unpack_from('<H',raw,0xc2)[0];phase,direction,count=raw[0xa4],raw[0x91],raw[0xdb]
    operations=['copiar'] if counter<=315 else []
    shadows=(counter-300)//5 if 300<=counter<315 else max(0,3-(counter-315)//5) if counter>=315 else 0
    operations+=['sombra']*shadows
    plan=dict(tipo=kind,contador_c2_u16=counter,fase_u8=phase,direcao_u8=direction,quantidade_db_u8=count,
        camadas=[],evidencia='AffDyingEngin 0x41559a..0x41591f')
    if not operations:return plan
    base,ax,ay=SPEC[kind];ident=(base+((direction+1)//2-1)*count+phase)&65535
    if not 1<=ident<=sum(QUANTIDADES):raise NotImplementedError('Raw corpse state selects an out-of-catalog ID')
    dx,dy=struct.unpack_from('<bb',raw,0x86)
    for operation in operations:
        plan['camadas'].append(dict(**localizar(ident),x=_i16(x+dx-ax),y=_i16(y+dy-ay),operacao=operation))
    return plan


def compor_morte_grafica(catalogo,destino,largura,altura,registro,*,x,y,tabela_sombra,recorte=None):
    """Return(new indexed bytes,plan), preserving all runtime inputs/tables."""
    if any(type(v) is not int or v<=0 for v in (largura,altura)) or len(destino)!=largura*altura:
        raise ValueError('Invalid indexed surface')
    if len(tabela_sombra)!=256:raise ValueError('Expected an explicit 256-byte shadow table')
    plan=consultar_morte_grafica(registro,x=x,y=y);out=bytes(destino)
    for layer in plan['camadas']:
        frame=catalogo.quadro(layer['id_motor'])
        if layer['operacao']=='copiar':out=compor_indices(out,largura,altura,frame,layer['x'],layer['y'],recorte)
        else:out=compor_sombra(out,largura,altura,frame,layer['x'],layer['y'],tabela_sombra,recorte)
    return out,plan
