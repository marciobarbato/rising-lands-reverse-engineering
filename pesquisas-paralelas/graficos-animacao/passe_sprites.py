"""Exact AffSprite callback order for stable interior runtime snapshots."""
import struct
from ordem_unidades import selecionar_ordem_unidades
from ordem_projeteis import selecionar_ordem_projeteis, consultar_celula_projetil


def planejar_passe_sprites(unidades,projeteis,objetos,descoberta,iluminacao,*,origem,janela_celulas):
    """Two scene passes; callback implementations and terrain pass are external.

    The origin is also the projectile viewport origin. Interior windows have
    1..32 cells per dimension and all +8/+10 margin cells inside the 256 map.
    Inputs are an immutable frame snapshot, not changing callback-owned state.
    """
    if len(objetos)!=65536:raise ValueError('Expected 65536 object-code bytes')
    if len(origem)!=2 or len(janela_celulas)!=2:
        raise ValueError('Expected origin and window cell pairs')
    if any(type(v) is not int or not 0<=v<=255 for v in origem):raise ValueError('Invalid map origin')
    if any(type(v) is not int or not 1<=v<=32 for v in janela_celulas):raise ValueError('Window must be 1..32 cells')
    ox,oy=origem;w,h=janela_celulas
    if ox+w+8>256 or oy+h+10>256:raise NotImplementedError('Viewport margin wraparound is outside this stage')
    units=selecionar_ordem_unidades(unidades,descoberta,iluminacao,origem=origem,janela_celulas=janela_celulas)['ordenadas']
    projectiles=selecionar_ordem_projeteis(projeteis,descoberta,iluminacao,bytes(200),
        origem=origem,janela_celulas=janela_celulas)['ordenadas']
    cells={index:struct.unpack_from('<H',unidades,index*276+8)[0] for index in units}
    priority={index:unidades[index*276+0xab] for index in units}
    projectile_cells={index:consultar_celula_projetil(projeteis,index)['celula_u16'] for index in projectiles}
    events=[];cursor=0
    for row in range(h+5):
        for column in range(w+8):
            cell=(oy+row)*256+ox+column;x=column*32;y=row*32
            if objetos[cell] and descoberta[cell]&31==0:
                events.append(dict(funcao='AffVeget',x=x,y=y,celula=cell,passe=1))
            events.append(dict(funcao='AffBatiments',x=x,y=y,celula=cell,passe=1))
            events.append(dict(funcao='AffBatimentOmbre',x=x,y=y,celula=cell,passe=1))
            while cursor<len(units) and priority[units[cursor]]!=0:cursor+=1
            while cursor<len(units) and cells[units[cursor]]==cell and priority[units[cursor]]==0:
                events.append(dict(funcao='AffEngin',x=x,y=y,indice=units[cursor],passe=1));cursor+=1
    cursor=0;projectile_cursor=0
    for row in range(h+10):
        for column in range(w+8):
            cell=(oy+row)*256+ox+column;x=column*32;y=row*32
            while projectile_cursor<len(projectiles) and projectile_cells[projectiles[projectile_cursor]]==cell:
                events.append(dict(funcao='AffProjectile',indice=projectiles[projectile_cursor],passe=2));projectile_cursor+=1
            while cursor<len(units) and priority[units[cursor]]==0:cursor+=1
            while cursor<len(units) and cells[units[cursor]]==cell and priority[units[cursor]]!=0:
                events.append(dict(funcao='AffEngin',x=x,y=y,indice=units[cursor],passe=2));cursor+=1
    return dict(origem=list(origem),janela_celulas=list(janela_celulas),unidades_ordenadas=units,
        projeteis_ordenados=projectiles,eventos=events)


def executar_passe_sprites(plano,*,vegetacao,construcao,unidade,projetil):
    """Run callbacks in original order; exceptions propagate without rollback.

    Vegetation/building: (x,y,cell); unit: (x,y,index); projectile: (index).
    Original AffBatimentOmbre is a literal RET and requires no callback.
    Callbacks must preserve the snapshot's selection/cell/priority fields.
    """
    callbacks=dict(AffVeget=vegetacao,AffBatiments=construcao,AffEngin=unidade,AffProjectile=projetil)
    if not all(callable(callback) for callback in callbacks.values()):raise ValueError('Four callable renderers required')
    count=0
    for event in plano['eventos']:
        name=event['funcao']
        if name=='AffBatimentOmbre':continue
        if name=='AffProjectile':callbacks[name](event['indice'])
        else:callbacks[name](event['x'],event['y'],event['indice'] if name=='AffEngin' else event['celula'])
        count+=1
    return count
