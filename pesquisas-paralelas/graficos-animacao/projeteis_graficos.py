"""Read-only AffProjectile mapping and indexed copy/shadow/Eclair composition."""
import struct
from graficos import localizar, compor_indices, QUANTIDADES
from composicao import compor_sombra
from eclairage import compor_eclairage


# Original single-copy branches: engine base, x/y offsets, displacement use.
SIMPLES={
    1:(0x2a7c,-9,-7,False),2:(0x2a80,-9,-7,True),
    3:(0x2a84,-9,-7,True),4:(0x2a88,-9,-7,True),5:(0x2a8c,-9,-7,True),
    6:(0x2075,0,0,False),7:(0x2095,-20,0,False),8:(0x20b5,-24,-16,False),
    14:(0x2a9a,0,0,False),15:(0x2aba,0,0,False),16:(0x2aca,0,0,False),
    17:(0x2a80,-9,-7,False),18:(0x2115,-37,-38,False),19:(0x2135,-33,-31,False),
    20:(0x235d,-5,-5,False),21:(0x2355,-6,-6,False),22:(0x2365,-3,-3,False),
    23:(0x236d,-4,-4,False),26:(0x2ada,0,0,False),34:(0x20d5,-81,-54,False)}


def _i16(value):return (value+32768)%65536-32768


def consultar_projetil_grafico(registro,*,origem,iluminacao_u8):
    """One immutable 56-byte runtime record; origin contains two raw u16 words.

    The illumination byte must come from the selected camera at the low word
    of (pixel_y//32)*256+pixel_x//32. Discovery is not queried by AffProjectile.
    All phase/direction bytes are consumed exactly; catalog overflow is refused.
    """
    if len(registro)!=56:raise ValueError('Expected one 56-byte projectile record')
    if len(origem)!=2 or any(type(v) is not int or not 0<=v<=65535 for v in origem):
        raise ValueError('Expected two u16 viewport origin words')
    if type(iluminacao_u8) is not int or not 0<=iluminacao_u8<=255:
        raise ValueError('iluminacao_u8 must be an integer in 0..255')
    registro=bytes(registro);kind=registro[0];phase=registro[0x18];direction=registro[0x22]
    px,py=struct.unpack_from('<HH',registro,0xc);displacement=struct.unpack_from('<I',registro,0x24)[0]
    plan=dict(tipo_u8=kind,fase_u8=phase,direcao_u8=direction,deslocamento_vertical_u32=displacement,
        celula_u16=((py//32)*256+px//32)&65535,camadas=[],evidencia='AffProjectile 0x46ff70..0x4704d9')
    if registro[2]==0:plan['motivo']='inactive';return plan
    if iluminacao_u8&31:plan['motivo']='unlit';return plan
    if kind in (0,28,33) or kind>34:plan['motivo']='no_visible_handler';return plan
    x,y=px-origem[0]*32,py-origem[1]*32
    layers=[]
    if kind in SIMPLES:
        base,dx,dy,raised=SIMPLES[kind]
        layers=[(base+phase,x+dx,y+dy-(displacement>>8 if raised else 0),'copiar')]
    elif 9<=kind<=13:
        layers=[(0x2a87+kind,x-1,y-1,'sombra'),
            (0x2a87+kind,x-1,y-1-(displacement>>8),'copiar')]
    elif kind in (24,25):
        # Original signed division truncates -1/2 to zero when direction is 0.
        group=(direction-1)//2 if direction else 0
        base,dx,dy=(0x2155,-75,-52) if kind==24 else (0x2255,-91,-59)
        layers=[(base+phase+group*32,x+dx,y+dy,'copiar')]
    elif kind==27:
        layers=[(0x1eb5+phase+(direction-1)*8,x-68,y-49,'copiar')]
    elif kind in (29,30):
        base,offset=(0x2c1d,8) if kind==29 else (0x2bbd,33)
        layers=[(base+phase+step,x-offset,y-offset,'eclairage') for step in (0,32,64)]
    elif kind in (31,32):
        operation='sombra' if kind==31 else 'eclairage'
        layers=[(0x20b5+phase,x-24,y-16,operation),(0x2075+phase,x,y,operation)]
    for order,(ident,xx,yy,operation) in enumerate(layers):
        ident&=65535
        if not 1<=ident<=sum(QUANTIDADES):
            raise NotImplementedError('Raw projectile state selects an ID outside the verified catalog')
        plan['camadas'].append(dict(**localizar(ident),x=_i16(xx),y=_i16(yy),operacao=operation,ordem=order))
    plan['motivo']='draw'
    return plan


def compor_projetil(catalogo,destino,largura,altura,registro,*,origem,iluminacao_u8,
                    tabela_sombra,tabela_eclairage,recorte=None):
    """Return (new indexed bytes, plan); records, inputs and tables stay intact."""
    if any(type(v) is not int or v<=0 for v in (largura,altura)) or len(destino)!=largura*altura:
        raise ValueError('Invalid indexed surface')
    if len(tabela_sombra)!=256 or len(tabela_eclairage)!=256:
        raise ValueError('Expected explicit 256-byte shadow and lighting tables')
    plan=consultar_projetil_grafico(registro,origem=origem,iluminacao_u8=iluminacao_u8);out=bytes(destino)
    for layer in plan['camadas']:
        frame=catalogo.quadro(layer['id_motor']);xx,yy=layer['x'],layer['y']
        if layer['operacao']=='copiar':out=compor_indices(out,largura,altura,frame,xx,yy,recorte)
        elif layer['operacao']=='sombra':out=compor_sombra(out,largura,altura,frame,xx,yy,tabela_sombra,recorte)
        else:out=compor_eclairage(out,largura,altura,frame,xx,yy,tabela_eclairage,recorte)
    return out,plan
