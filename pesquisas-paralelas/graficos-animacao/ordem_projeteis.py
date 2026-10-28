"""Read-only projectile display queries; no projectile simulation."""
import struct


def _pool(pool):
    if len(pool)!=5600:raise ValueError('Expected 100 projectile records of 56 bytes')


def consultar_celula_projetil(pool,indice_u16):
    """ProjectileGetCase: full derived dword and its caller-consumed low word."""
    _pool(pool)
    if type(indice_u16) is not int or not 0<=indice_u16<100:
        raise ValueError('indice_u16 must be in 0..99')
    x,y=struct.unpack_from('<HH',pool,indice_u16*56+0xc)
    cx,cy=x//32,y//32;key=cy*256+cx
    return dict(x_celula=cx,y_celula=cy,chave_u32=key,celula_u16=key&65535)


def selecionar_ordem_projeteis(pool,descoberta,iluminacao,indices_entrada,*,origem,janela_celulas):
    """Select/swap the original display index array, preserving its unused tail.

    Origin is restricted to nonnegative map coordinates 0..255, window 1..256
    cells. Coordinate words remain u16 even outside the physical map. Both
    visibility predicates consume the low packed-cell word with mask 31.
    """
    _pool(pool)
    if len(descoberta)!=65536 or len(iluminacao)!=65536 or len(indices_entrada)!=200:
        raise ValueError('Expected two camera maps and a 200-byte index array')
    for pair,low,high in ((origem,0,255),(janela_celulas,1,256)):
        if len(pair)!=2 or any(type(value) is not int or not low<=value<=high for value in pair):
            raise ValueError('Invalid origin or window cell pair')
    ox,oy=origem;w,h=janela_celulas;selected=[];keys={}
    for index in range(100):
        if pool[index*56+2]==0:continue
        cell=consultar_celula_projetil(pool,index);key=cell['celula_u16']
        if descoberta[key]&31 or iluminacao[key]&31:continue
        if not ox<=cell['x_celula']<ox+w+2 or not oy<=cell['y_celula']<oy+h+10:continue
        selected.append(index);keys[index]=key
    ordered=list(selected)
    for position in range(len(ordered)):
        candidate=position
        for other in range(position+1,len(ordered)):
            if keys[ordered[other]]<=keys[ordered[candidate]]:candidate=other
        ordered[position],ordered[candidate]=ordered[candidate],ordered[position]
    output=bytearray(indices_entrada)
    for position,index in enumerate(ordered):struct.pack_into('<H',output,position*2,index)
    return dict(quantidade=len(ordered),selecionadas=selected,ordenadas=ordered,indices_saida=bytes(output))
