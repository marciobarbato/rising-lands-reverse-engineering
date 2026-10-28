"""AffSprite's read-only unit selection and exact unstable swap order."""
import struct

POOL_SIZE=800
RECORD_SIZE=276


def selecionar_ordem_unidades(unidades,descoberta,iluminacao,*,origem,janela_celulas):
    """Consume the 800 runtime records and two already selected camera maps.

    Only state +2, cell u16 +8 and priority u8 +0xab affect this prefix.
    Origin is a map-cell pair 0..255; window dimensions are u16 restricted to
    1..256. No unit/world bytes are mutated. No draw or projectile call occurs.
    """
    if len(unidades)!=POOL_SIZE*RECORD_SIZE or len(descoberta)!=65536 or len(iluminacao)!=65536:
        raise ValueError('Expected 800 runtime records and two 65536-byte camera maps')
    for pair,low,high,name in ((origem,0,255,'origin'),(janela_celulas,1,256,'window')):
        if len(pair)!=2 or any(type(value) is not int or not low<=value<=high for value in pair):
            raise ValueError(f'Invalid {name} cell pair')
    ox,oy=origem;w,h=janela_celulas
    selected=[];cells={};priorities={}
    for index in range(POOL_SIZE):
        offset=index*RECORD_SIZE
        if unidades[offset+2]==0:continue
        cell=struct.unpack_from('<H',unidades,offset+8)[0]
        if descoberta[cell]&31 or iluminacao[cell]&16:continue
        x,y=cell%256,cell//256
        if x<ox or y<oy or x>=ox+w+2 or y>=oy+h+10:continue
        selected.append(index);cells[index]=cell;priorities[index]=unidades[offset+0xab]
    ordered=list(selected)
    # Selection swaps intentionally retain the original equal-key instability.
    for position in range(len(ordered)):
        candidate=position
        for other in range(position+1,len(ordered)):
            current,new=ordered[candidate],ordered[other]
            if cells[new]<cells[current] or (cells[new]==cells[current] and priorities[new]<priorities[current]):
                candidate=other
        ordered[position],ordered[candidate]=ordered[candidate],ordered[position]
    return dict(selecionadas=selected,ordenadas=ordered,
        evidencia='AffSprite 0x416864..0x416a6c; before ProjectileTrierAffichage')
