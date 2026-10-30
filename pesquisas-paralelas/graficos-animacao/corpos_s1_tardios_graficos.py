"""Original late-S1 normal/attack/death bodies, read-only display records.

Finite native windows include owner-4 soldiers, owner-0 hunger state19 and the
thief's attack branch. Animation/life/death counters are consumed, never advanced.
"""
import struct
import composicao
from sobreposicoes_entrada_m3 import bob,word,i16


def shadow(c,x,y,ident):
    c.saida=composicao.compor_sombra(c.saida,c.largura,c.altura,c.catalogo.quadro(ident),i16(x),i16(y),c.sombra,c.recorte())


def copy_body(c,owner,x,y,ident):
    # Owner4 first draws at0x411C9F, then rejoins0x41118A and draws again at
    # 0x41121B. These two real calls have identical pixels, but both are retained.
    for _ in range(2 if owner==4 else 1):bob(c,x,y,ident,owner if owner else None)


def body(c,r,x,y,index):
    owner,kind,state=r[0],r[1],r[2]
    dying=state==4 and (owner==0 and kind in (0,5) or owner==4 and kind==0)
    routed=(owner==4 and kind==0 and state in (1,2,7) or
            owner==0 and kind==0 and state==1 or
            owner==0 and kind in (0,1,5,8) and state==19 or
            owner==0 and kind==8 and state==1)
    if not(dying or routed):return False
    if c.camera!=0 or r[0xdc] or r[0x99]:c.parar(0x411147,'Late-S1 body effect/camera mode is not proved')
    dx,dy=struct.unpack_from('<bb',r,0x86);px,py=x+dx,y+dy
    if dying:
        counter=word(r,0xc2);phase,direction,count=r[0xa4],r[0x91],r[0xdb]
        if counter<330 and (count!=8 or not 1<=direction<=16 or phase>=count):
            c.parar(0x41591f,'Late-S1 corpse direction/count/phase outside native records')
        base,ax,ay=(0x8b2,40,22) if kind==0 else (0x6e2,11,11)
        ident=(base+((direction+1)//2-1)*count+phase)&65535
        if counter<=315:copy_body(c,owner,px-ax,py-ay,ident)
        passes=(counter-300)//5 if 300<=counter<315 else max(0,3-(counter-315)//5) if counter>=315 else 0
        for _ in range(passes):shadow(c,px-ax,py-ay,ident)
        return True
    if r[0xbd] or c.tela.u('selecionada_unidade_u16')==index or c.tela.u('modo_selecao_u8'):
        c.parar(0x410be4,'Late-S1 army/raider selection overlay is not proved')
    attack=state==1 and 1<=r[0x8a]<=3
    if state==1 and r[0x8a]>3:return True
    base,ax,ay={0:(2146 if attack else 2082,40,22),1:(2290,23,9),
        5:(1698 if word(r,0xa) else 1602,11,11),8:(2530 if attack else 2450,32,30)}[kind]
    count=r[0xa6] if attack else r[0xa5]
    if not 1<=r[0x91]<=16 or count!=(10 if attack or kind==8 else 8) or r[0xa4]>=count:
        c.parar(0x41374c if attack else 0x412390,'Late-S1 direction/animation count outside native records')
    ident=(base+((r[0x91]+1)//2-1)*count+r[0xa4])&65535
    shadow(c,px+2,py+26,10784)
    copy_body(c,owner,px-ax,py-ay,ident)
    c._cauda_unidade_m3(r,x,y,index,bool(r[0xba]))
    return True
