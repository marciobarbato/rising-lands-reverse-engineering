"""Native placement grid, tooltip frame and saved-background copy (evidence 9a1f846).

AffText is an explicit external dependency. A supplied text renderer receives bytes, rectangle and font arguments;
without it, rendering stops at 0x459454 after producing the native tooltip background.
"""
import struct
from quadro_jogo import DependenciaQuadro
from sobreposicoes_entrada_m3 import i16

def write(h,name,address,value,width=2):
    old=h.m.ler(address,width);new=value.to_bytes(width,'little')
    if old!=new:h.efeitos.append((name,address,old.hex(),new.hex()))
    h.m.sobrepostos.update({address+i:v for i,v in enumerate(new)})

def shaded_box(h,x0,y0,x1,y1,*,shadow=False,clipped=True):
    routine='FilledBoxOmbre' if shadow else 'FilledBoxGris'
    h.chamadas.append([routine,x0,y0,x1,y1,int(clipped)])
    if clipped:
        left,top,right,bottom=(h.m.u16(a) for a in (0x49a020,0x49a01c,0x49a022,0x49a01e))
    else:left,top,right,bottom=0,0,h.m.u16(0x49a018)-1,h.m.u16(0x49a01a)-1
    if x0>right or y0>bottom or x1<left or y1<top:return
    x0,y0,x1,y1=max(x0,left),max(y0,top),min(x1,right),min(y1,bottom)
    table=h.m.ler(h.m.u32(0x4e24b4 if shadow else 0x4e24c4),256)
    for y in range(y0,y1+1):
        at=y*h.largura+x0;h.saida[at:at+x1-x0+1]=bytes(h.saida[at:at+x1-x0+1]).translate(table)

def placement(h):
    m=h.m;kind=m.u8(0x496207)
    if kind!=3:h.parar(0x41729b,'placement outside captured type-3 CAVE')
    w,hh=m.u16(0x495d8c+52*kind),m.u16(0x495d8e+52*kind)
    if kind!=3 or (w,hh)!=(5,5):h.parar(0x41729b,'placement outside captured type-3 5 x 5 CAVE')
    x=(m.u16(0x5099a8)//32-w//2)*32;y=(m.u16(0x5099aa)//32-hh//2)*32
    h.caixa(x,y,x+w*32,y+hh*32,0x1f,True)
    shaded_box(h,x,y,x+w*32,y+hh*32)
    for row in range(hh):
        for col in range(w):
            if not m.u8(0x4e05b9+row*w+col):h.caixa(x+col*32,y+row*32,x+(col+1)*32,y+(row+1)*32,0x94,True)

def restore_background(c):
    m=c.leitura_entrada
    if m is None:c.parar(0x4179e1,'saved-background restore requires the live read view')
    if c.tela.u('largura_tela_u16')!=800:c.parar(0x4179e1,'saved-background restore outside captured 800-pixel screen mode')
    x,y,w,h=(m.u16(a) for a in (0x49a046,0x49a048,0x49a04a,0x49a04c));x,y=i16(x),i16(y)
    ptr=m.u32(0x49a03c);data=m.ler(ptr,w*h)
    c.chamadas.append(['PasteBob',x,y,w,h,ptr]);out=bytearray(c.saida)
    for row in range(h):
        if 0<=y+row<600:
            left,right=max(0,x),min(800,x+w)
            if right>left:out[(y+row)*c.largura+left:(y+row)*c.largura+right]=data[row*w+left-x:row*w+right-x]
    c.saida=bytes(out)
    c.tela.gravar('restaurar_fundo_u8',0);c.tela.gravar('forcar_desenho_u8',1)
    old=m.ler(0x49a040,1)
    if old!=b'\0':c.tela.efeitos.append(('fond_u8',0x49a040,old.hex(),'00'))

def save_background(h,x,y,width,height,ptr):
    saved=b''.join(bytes(h.saida[(y+r)*h.largura+x:(y+r)*h.largura+x+width]) for r in range(height))
    h.chamadas.append(['GetBob',x,y,width,height,ptr])
    # GetBob overwrites a scratch output buffer without reading its previous bytes. Empty old hex denotes write-only.
    h.efeitos.append(('saved_background_pixels',ptr,'',saved.hex()))

def tooltip(h):
    m=h.m;ptr=m.u32(0x4e060c)
    if not ptr:return
    if not 0x494000<=ptr<0x523000:h.parar(0x40f8c0,'tooltip pointer outside captured DGROUP strings')
    if m.u16(0x4e0610)<m.u16(0x49620a):return
    if m.u16(0x5099a8)>800 or m.u16(0x5099aa)>600:h.parar(0x40f8c0,'tooltip mouse outside captured screen coordinates')
    text=bytearray()
    for i in range(128):
        b=m.u8(ptr+i)
        if not b:break
        text.append(b)
    else:h.parar(0x40f8c0,'tooltip string exceeds captured bounded length')
    if bytes(text) not in (b'CONSTRUTOR',b'ARMAZ\xc9M') or m.u16(0x49620c)!=0xffff or m.u32(0x4e1d94) or m.u32(0x4e1d98):
        h.parar(0x40f8c0,'tooltip outside captured builder/CAVE strings and single-byte font mode')
    write(h,'restaurar_fundo_u8',0x49a041,1,1)
    width=sum(h.catalogo.quadro(0x23d5+b-32).largura for b in text)+2
    height=h.catalogo.quadro(0x23d5+0x6a-32).altura
    x=max(0,m.u16(0x5099a8)+24);y=max(0,m.u16(0x5099aa)+(120 if m.u16(0x5099aa)>=m.u16(0x508726)*32 else 0)+16)
    if y+height+6>592:y=591-height-6
    if x+width+6>800:x=800-width-6
    width+=6-(width%2==0);height+=6
    old_width,old_height=m.u16(0x49a018),m.u16(0x49a01a)
    write(h,'largura_tela_u16',0x49a018,800);write(h,'altura_tela_u16',0x49a01a,600)
    for name,a,value in (('tooltip_x',0x49a046,x),('tooltip_y',0x49a048,y),('tooltip_w',0x49a04a,width),('tooltip_h',0x49a04c,height)):
        write(h,name,a,value)
    save_background(h,x,y,width,height,m.u32(0x49a03c))
    h.caixa(x,y,x+width-1,y+height-1,1,False)
    shaded_box(h,x+1,y+1,x+width-2,y+height-2,shadow=True,clipped=False)
    request=dict(text=bytes(text),x=x+3,y=y+1,right=x+width-2,bottom=y+height-2,font=1,flags=(0,0))
    h.chamadas.append(['AffText',request['x'],request['y'],request['right'],request['bottom'],bytes(text).hex(),1,0,0])
    if h.texto is None:
        raise DependenciaQuadro(0x459454,'AffText glyph renderer is not supplied (probes declare this boundary non-executed)',
            superficie=bytes(h.saida),chamadas=h.chamadas,efeitos=h.efeitos)
    rendered=h.texto(request,bytes(h.saida))
    if not isinstance(rendered,bytes) or len(rendered)!=len(h.saida):raise ValueError('Text renderer must return the complete indexed surface')
    h.saida[:]=rendered
    write(h,'largura_tela_u16',0x49a018,old_width);write(h,'altura_tela_u16',0x49a01a,old_height)
