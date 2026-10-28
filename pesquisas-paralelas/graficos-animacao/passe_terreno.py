"""Bounded interior AffTerrain plan, callbacks and un-clipped opaque blocks."""
import struct
from cache_terreno import CacheTerreno


def terreno_de_construcao(terreno_u16):
    """Read-only EstConstructionTerrain range union, not physical semantics."""
    if type(terreno_u16) is not int or not 0<=terreno_u16<=65535:raise ValueError('Expected raw u16 terrain word')
    return 702<=terreno_u16<=1081


def planejar_passe_terreno(terreno,iluminacao,*,origem,janela_celulas,margem_i8):
    """Stable raw terrain/light snapshot; origin u8, window1..32, inset>=0.

    Native width-word and pitch must both be window_width*32. Negative/wrapped
    views are explicitly outside this bounded interior contract.
    """
    if len(terreno)!=131072 or len(iluminacao)!=65536:raise ValueError('Expected full terrain-word and selected-light maps')
    terreno=bytes(terreno);iluminacao=bytes(iluminacao)
    if len(origem)!=2 or any(type(v) is not int or not 0<=v<=255 for v in origem):raise ValueError('Expected two u8 origin coordinates')
    if len(janela_celulas)!=2 or any(type(v) is not int or not 1<=v<=32 for v in janela_celulas):raise ValueError('Expected window dimensions1..32')
    if type(margem_i8) is not int or not -128<=margem_i8<=127:raise ValueError('Expected raw signed-i8 inset')
    ox,oy=origem;w,h=janela_celulas;m=margem_i8
    if m<0 or 2*m>min(w,h):raise NotImplementedError('Negative/excessive insets are outside the verified interior domain')
    if ox+w>256 or oy+h>256:raise NotImplementedError('Wrapped terrain viewports are not implemented')
    cells=[]
    for row in range(m,h-m):
        for column in range(m,w-m):
            cell=(oy+row)*256+ox+column;raw=struct.unpack_from('<H',terreno,cell*2)[0]
            replaced=terreno_de_construcao(raw) and bool(iluminacao[cell]&16)
            source=349+(cell%256)%8+8*((cell//256)%8) if replaced else raw
            cells.append(dict(celula=cell,x=column*32,y=row*32,id_original_u16=raw,id_terreno_u16=source,substituido=replaced))
    return dict(origem=list(origem),janela_celulas=list(janela_celulas),margem_i8=m,largura_px=w*32,altura_px=h*32,
        celulas=cells,evidencia='AffTerrain 0x41068e..0x41087e')


def executar_passe_terreno(plano,*,bloco,vegetacao):
    """Block(x,y,cell,source) then vegetation(x,y,cell); effects stay on errors."""
    if not callable(bloco) or not callable(vegetacao):raise ValueError('Both terrain callbacks must be callable')
    count=0
    for cell in plano['celulas']:
        bloco(cell['x'],cell['y'],cell['celula'],cell['id_terreno_u16']);count+=1
        vegetacao(cell['x'],cell['y'],cell['celula']);count+=1
    return count


def pixels_bloco_terreno(catalogo,cache,id_motor):
    """Read the original32x33 raw-block layout, not generic transparent RLE."""
    if type(id_motor) is not int:raise ValueError('Expected integer engine ID')
    if 1090<=id_motor<=1345:
        if not isinstance(cache,CacheTerreno):raise ValueError('Expected explicit terrain cache')
        return cache.pixels(id_motor-1090)
    if not 1<=id_motor<=1081:raise NotImplementedError('Engine ID is outside verified full-block sources/cache slots')
    frame=catalogo.quadro(id_motor);raw=frame.comprimido
    if (frame.largura,frame.altura,len(raw))!=(32,32,1056) or any(raw[row*33]!=224 for row in range(32)):
        raise NotImplementedError('Static engine ID is not a verified full-literal block')
    return b''.join(raw[row*33+1:row*33+33] for row in range(32))


def compor_bloco_terreno(destino,largura,altura,pixels,x,y):
    """AffBloc:32 opaque pixels per row, native pitch, no clip rectangle."""
    if any(type(v) is not int or v<=0 for v in (largura,altura)) or len(destino)!=largura*altura or len(pixels)!=1024:
        raise ValueError('Invalid surface or32x32 block')
    if type(x) is not int or type(y) is not int:raise ValueError('Expected integer block coordinates')
    if not 0<=x<=largura-32 or not 0<=y<=altura-32:
        raise NotImplementedError('Un-clipped block must fit entirely inside the destination')
    out=bytearray(destino)
    for row in range(32):out[(y+row)*largura+x:(y+row)*largura+x+32]=pixels[row*32:row*32+32]
    return bytes(out)
