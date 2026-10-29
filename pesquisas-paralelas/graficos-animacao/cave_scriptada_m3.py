"""CAVE/sanctuary construction and builder orders, native evidence 9a05e69/9a1f846.

The new facade domain is uninhabited types 2/3, modes 0..7, progress 0..200. Inhabited sanctuary's existing provider
is retained by the caller. Fire, inhabited CAVE and queued/foreign builder bodies remain explicit dependencies.
"""
import struct
from graficos import compor_indices
from objetos import compor_sombra
from sobreposicoes_entrada_m3 import bob, i16, word

PARTES={2:((7032,0,0),(7049,74,5),(7033,89,95),(7041,151,131),(7057,18,63)),
        3:((7094,0,0),(7095,3,10),(7103,43,0),(7111,60,23),(7119,64,41),(7127,12,46),(7135,21,16))}

def clip(c,left,top,right,bottom):
    c.tela.gravar('recorte',struct.pack('<4H',*(v&65535 for v in (top,bottom,left,right))))

def gray(c,x,y,ident):
    m=c.leitura_entrada
    if m is None:c.parar(0x40892d,'uninhabited facade requires the grayscale read view')
    c.chamadas.append(['PasteGrisCmp',i16(x),i16(y),ident,1])
    table=m.ler(m.u32(0x4e24c4),256)
    c.saida=compor_sombra(c.saida,c.largura,c.altura,c.catalogo.quadro(ident),i16(x),i16(y),table,c.recorte())

def facade(c,x,y,cell,index,*,habitacao=None):
    if index==0xffff:return
    r=c._estrutura(index,0x4085cb);kind,mode=r[8],r[5]
    if kind not in (2,3) or mode>7:c.parar(0x40f23b,'facade outside types 2/3 modes 0..7')
    if c.mundo.palavra('terreno',cell)!={2:0x2ed,3:0x30d}[kind]:c.parar(0x40f23b,'facade trigger and structure type disagree')
    if word(r,6):c.parar(0x4085cb,'structure damage/fire (+0x06 nonzero)')
    inhabited=c._consulta_habitada(index,0x4087aa) if habitacao is None else habitacao
    if inhabited:c.parar(0x40958e if kind==3 else 0x408ac8,'construction facade outside captured uninhabited domain')
    m=c.leitura_entrada
    if m is None:c.parar(0x408ac8,'construction facade requires the live type-table read view')
    maximum=m.u16(0x495d90+52*kind)
    if maximum!={2:600,3:100}[kind] or word(r,0xa)>maximum:c.parar(0x408ac8,'construction health outside captured maximum')
    height,scaffold,dx,dy={2:(153,7031,150,93),3:(97,7093,57,47)}[kind]
    x,y=i16(x-dx),i16(y-dy);w,h=c.tela.palavras('janela')
    state=200*word(r,0xa)//maximum
    if mode in (0,1,2,6,7):
        if state<100:
            clip(c,max(0,x),max(0,i16(y+(100-state)*height//100)),w*32-1,h*32-1)
            bob(c,x,y,scaffold);return
        offset=(200-state)*height//100
        clip(c,0,0,w*32-1,min(i16(y+offset),h*32-1));bob(c,x,y,scaffold)
        clip(c,max(0,x),max(0,i16(y+offset)),w*32-1,h*32-1)
    elif mode==3:
        def jitter():
            cursor=c.tela.u('rng_u8');value=m.u8(0x4e1c18+cursor)%3
            c.tela.gravar('rng_u8',(cursor+1)&255);return value
        bottom=min(i16(y+height+jitter()),h*32-1)
        y=max(0,i16(y+200+jitter()-word(r,0x84)))
        clip(c,0,y,w*32,bottom);x=i16(x+jitter())
    for ident,ox,oy in PARTES[kind]:bob(c,x+ox,y+oy,ident)
    for ident,ox,oy in PARTES[kind]:gray(c,x+ox,y+(38 if kind==3 and ident==7119 else oy),ident)

def construction_builder(c,r,x,y,index):
    if (r[0]!=0 or c.camera!=0 or r[1]!=7 or r[2] not in (11,15) or r[0x89] not in (0,1)
            or r[0xbe]==9 or r[0xdc] or r[0x99] or r[0xa5]!=8 or r[0xa4]>=8 or not 1<=r[0x91]<=16):
        c.parar(0x414495,'builder construction body outside captured owner-0 task 0/1 domain')
    dx,dy=struct.unpack_from('<bb',r,0x86);px,py=x+dx,y+dy
    base=0x57a if r[0x89] else 0x53a if word(r,0xa)==0 else 0x5ba
    # AffConstruireBatiment indexes the direction group without AffDeplaceEngin's -1.
    ident=base+((r[0x91]+1)//2)*8+r[0xa4]
    c.saida=compor_sombra(c.saida,c.largura,c.altura,c.catalogo.quadro(10784),i16(px+2),i16(py+26),c.sombra,c.recorte())
    c.saida=compor_indices(c.saida,c.largura,c.altura,c.catalogo.quadro(ident),i16(px-26),i16(py-26),c.recorte())
    c._cauda_unidade_m3(r,x,y,index,True)

def order_markers(c,r):
    if not r[0xbd] or not r[0x82] or r[2]==17:return
    if r[0x82]!=1:c.parar(0x412923,'selected order marker outside captured cell-target mode 1')
    ox,oy=c.tela.palavras('origem');w,h=c.tela.palavras('janela');phase=(c.tela.u('quadro_u32')//5)&1
    for offset,base in ((0xb2,0x1e43),(0x80,0x1e45)):
        cell=word(r,offset);cx,cy=cell%256,cell//256
        if ox<=cx<ox+w and oy<=cy<oy+h:bob(c,(cx-ox)*32,(cy-oy)*32,base+phase)
