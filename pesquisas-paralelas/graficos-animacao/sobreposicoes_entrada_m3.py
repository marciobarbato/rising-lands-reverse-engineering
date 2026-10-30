"""Input-time overlays, reconstructed after native evidence commits 5b05e41 and 5405033.

Only the captured normal field units and inhabited type-2 sanctuary are supported. Helpers operate on the frame
compositor's indexed surface and append actual drawing arguments. They never mutate simulation memory.
"""
import struct
from graficos import Quadro, compor_indices

i16=lambda v:(v+32768)%65536-32768
word=lambda r,o:struct.unpack_from('<H',r,o)[0]
TIPOS_ENTRADA=(0,1,5,7,8,9)


def bob(c,x,y,ident,owner=None):
    x,y=i16(x),i16(y)
    name='PasteBobCmp' if owner is None else 'PastePlayerCmp'
    c.chamadas.append([name,x,y,ident,1]+([] if owner is None else [owner]))
    q=c.catalogo.quadro(ident)
    if owner is not None:
        q=Quadro(q.largura,q.altura,q.pixels.translate(c.tabelas_jogador[owner]),q.opacidade,0,b'')
    c.saida=compor_indices(c.saida,c.largura,c.altura,q,x,y,c.recorte())


def filled(c,x0,y0,x1,y1,color):
    x0,y0,x1,y1=map(i16,(x0,y0,x1,y1))
    c.chamadas.append(['FilledBox',x0,y0,x1,y1,color,1])
    left,top,right,bottom=c.recorte()
    # FilledBox clips first and does not reorder endpoints. A zero-health fill has y0 > y1 and writes no row.
    if x0>right or y0>bottom or x1<left or y1<top:return
    x0,y0,x1,y1=max(x0,left),max(y0,top),min(x1,right),min(y1,bottom)
    if x1<x0 or y1<y0:return
    out=bytearray(c.saida)
    for y in range(y0,y1+1):out[y*c.largura+x0:y*c.largura+x1+1]=bytes([color])*(x1-x0+1)
    c.saida=bytes(out)


def drag(c):
    if c.leitura_entrada is None:c.parar(0x417ac8,'selection drag box (Box 0x45C912) is not composed')
    x0,y0,x1,y1=(c.leitura_entrada.i16(a) for a in (0x49a024,0x49a026,0x49a028,0x49a02a))
    w,h=c.tela.palavras('janela');x1,y1=min(x1,w*32),min(y1,h*32)
    c.chamadas.append(['Box',x0,y0,x1,y1,1,1])
    left,top,right,bottom=c.recorte()
    if x0>right or y0>bottom or x1<left or y1<top:return
    x0,y0,x1,y1=max(x0,left),max(y0,top),min(x1,right),min(y1,bottom)
    if x1<x0:x0,x1=x1,x0
    if y1<y0:y0,y1=y1,y0
    out=bytearray(c.saida)
    out[y0*c.largura+x0:y0*c.largura+x1+1]=bytes([1])*(x1-x0+1)
    out[y1*c.largura+x0:y1*c.largura+x1+1]=bytes([1])*(x1-x0+1)
    for y in range(y0,y1+1):out[y*c.largura+x0]=1;out[y*c.largura+x1]=1
    c.saida=bytes(out)


def validar_unidade(c,r):
    if r[1] not in TIPOS_ENTRADA or r[0]!=0 or c.camera!=0 or (r[2] not in (2,7) and not (r[1]==7 and r[2] in (5,11,15)) and not (r[1]==9 and r[2]==13) and not (r[1]==5 and r[2]==5)) or r[0x99] or r[0xdc]:
        c.parar(0x41591f,'input overlay outside captured owner-0 normal field-unit domain')
    if r[0xa5] != (10 if r[1] == 8 else 8):c.parar(0x41591f,'input-overlay body count differs from the initialized count')
    if word(r,4)!=4 or word(r,0x76)!=4:
        from camadas_exibicao_m3 import TABLES
        if ([word(r,4),word(r,0x76)] not in TABLES.get('fatigue_pairs',{}).get(str(r[1]),[])
                and not (r[1]==5 and (word(r,4),word(r,0x76))==(1,4))):
            c.parar(0x410be4,'fatigue words outside captured unit/material pairs')
    if r[0xbd] and r[0x82]>1 and not (r[1] in (5,7) and r[0x82]==2):
        c.parar(0x412923,'selected unit order marker outside captured modes')
    if r[0xaf]>>5 and r[1]!=7:c.parar(0x413696,'experience icon for a non-builder is not captured')


def quadro_selecao_unidade(c,r,x,y):
    if r[0xbd] and r[0]==c.camera:bob(c,x,y,0x2a1e)


def experiencia(c,r,x,y,*,info=False):
    level=r[0xaf]>>5
    if level and (info or r[0xba]) and (not r[0xba] or c.tela.u('quadro_u32')%5==0):
        bob(c,x-8,y-2,0x1e46+level)


def info_unidade(c,r,x,y,index):
    m=c.leitura_entrada
    if m is None:c.parar(0x410be4,'AffInfoSelection requires the live type-table read view')
    if r[0]!=c.camera:return
    maximum=m.u16(0x4965b6+50*r[1]);hp=word(r,0x9a)
    if maximum!=100 or hp>maximum:c.parar(0x410be4,'unit health outside captured 0..100 / max 100')
    if word(r,0xc) not in (0,1):c.parar(0x410a2c,'AffContenanceEngin bag capacity outside captured 0/1')
    percent=100*hp//maximum;height=15*percent//100
    filled(c,x-11,y,x-8,y+15,2)
    filled(c,x-11,y+15-height,x-9,y+14,48 if percent>75 else 180 if percent>35 else 145)
    life=word(r,0x74)
    tired=word(r,4)==word(r,0x76) and life<100
    if not tired or (life//5)%2==0:bob(c,x-8,y-2,0x1e2b+word(r,4),r[0])
    experiencia(c,r,x,y,info=True)
    # AffContenanceEngin: capacity 0 has no iteration; capacity 1 exits before drawing.


def estrutura(c,r,cell,index,*,frame,gauge):
    if r[8]==3 or (r[8]==2 and (word(r,0xc) in (2,3,4,5,6,7) or r[5]==4)):
        from camadas_exibicao_m3 import selecao
        return selecao(c,r,cell,index,frame=frame,gauge=gauge)
    if r[8]!=2 or r[5]!=5 or r[4]!=0 or c.camera!=0:
        c.parar(0x4022c8 if frame else 0x4020ec,'selection overlay outside captured inhabited owner-0 mode-5 sanctuary')
    if c.leitura_entrada is None:c.parar(0x4020ec,'sanctuary gauge requires the live type-table read view')
    ox,oy=c.tela.palavras('origem')
    # Only the sanctuary facade trigger executes this prologue (0x4085CD..0x408603).
    x,y=(cell%256-ox)*32-150,(cell//256-oy)*32-93
    if frame:
        phase=c.relogios_extra[0]&7
        for ident,px,py in ((0x2a79,x+phase-20,y+phase),(0x2a78,x+phase-20,y+153-phase),
                            (0x2a7a,x+175-phase,y+phase),(0x2a77,x+175-phase,y+153-phase)):
            bob(c,px,py,ident,r[4])
    if not gauge:return
    denominator=c.leitura_entrada.u16(0x495d90+52*2)
    hp,damage=word(r,0xa),word(r,6)
    if denominator!=600 or not 0<=damage<=hp<=600:c.parar(0x4020ec,'sanctuary health/malus outside captured 0..600')
    if word(r,0xe)!=16 or word(r,0xc)!=8 or r[0x4e:0x5e] != bytes([1])*8+bytes(8):
        c.parar(0x401a70,'sanctuary contents outside captured 16-slot / 8-unit bag')
    gx,gy=i16(x-23),i16(y+90)
    if ox==0 and gx<0:gx=0
    bob(c,gx+9,gy,0x2a7b)
    height=((hp*200//denominator)-(damage*200//denominator))*60//200
    filled(c,gx+10,gy+61-height,gx+14,gy+60,145 if height<=20 else 180 if height<=40 else 48)
    for i in range(16):
        px,py=gx-(9 if i>=8 else 0),gy+8*(i%8)
        code=r[0x4e+i]
        bob(c,px,py,0x2a3c if code==1 else 0x2a3b,r[4] if code==1 else None)
