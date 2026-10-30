"""Read-only AffObjectif 0x47c6d3 composition from the real S1 transition to the next objectives page.

The mission loader owns the text/pointer table; this renderer consumes it after loading. No mission/menu state
is fabricated or updated. Full MenuInit/LoadPie/AffText transition composition remains a separate dependency.
"""
from texto_bitmap_nativo import compor_linha_bitmap,largura_linha_bitmap,DependenciaTextoBitmap

DGROUP=0x494000

def compor_objetivos_s1(memoria,superficie,*,catalogo):
    """Return dict(pixels,chamadas,efeitos), preserving memory and reporting ordered clip stores.

    Captured domain:800x600, language0/single-byte mode, first page offset0, last-line index36.
    A zero draw flag returns immediately. Unknown pages/geometry/languages are named dependencies.
    """
    if len(superficie)!=480000:raise ValueError('Expected800x600 indexed surface')
    if memoria.u8(0x511ffa)==0:return dict(pixels=bytes(superficie),chamadas=[],efeitos=[])
    if ((memoria.u16(0x49a018),memoria.u16(0x49a01a))!=(800,600)
            or memoria.u16(0x511ff8)!=0 or memoria.u16(0x511824)!=36):
        raise DependenciaTextoBitmap(0x47c6d3,'Objectives outside the captured S1 first-page domain')
    idioma,multi=memoria.u32(0x4e1d94),memoria.u32(0x4e1d98)
    if (idioma,multi)!=(0,0):raise DependenciaTextoBitmap(0x4591c8,'Unproved objectives language/font mode')
    line_height=memoria.u16(0x498408)
    if line_height!=15:raise DependenciaTextoBitmap(0x47c738,'Uncaptured objectives line-height table')
    incoming={a:memoria.u16(a) for a in (0x49a01c,0x49a01e,0x49a020,0x49a022,0x49a02c,0x49a02e,0x49a030,0x49a032)}
    current=dict(incoming);effects=[]
    def store(name,address,value):
        effects.append((name,address,current[address].to_bytes(2,'little').hex(),value.to_bytes(2,'little').hex()))
        current[address]=value
    for dst,src in ((0x49a02c,0x49a020),(0x49a02e,0x49a022),(0x49a030,0x49a01c),(0x49a032,0x49a01e)):
        store('SaveCurrentClipping',dst,current[src])
    for a,v in ((0x49a020,55),(0x49a022,310),(0x49a01c,212),(0x49a01e,486)):
        store('SetClipping',a,v)
    out=bytearray(superficie)
    for y in range(212,487):out[y*800+55:y*800+311]=bytes([42])*256
    calls=[['FilledBox',55,212,310,486,42,0]]
    for i in range(18):
        ptr=memoria.u32(0x511828+4*i);text=bytearray()
        for j in range(128):
            c=memoria.u8(ptr+j)
            if c in (0,10):break
            text.append(c)
        else:raise DependenciaTextoBitmap(0x4591c8,'Objectives line has no bounded terminator')
        text=bytes(text)
        width=largura_linha_bitmap(catalogo,text,fonte_u8=1,idioma_u32=idioma,multibyte_u32=multi)&65535
        # Original signed IDIV-style halving truncates toward zero, then negative centring clamps to0.
        delta=255-width;centre=max(0,delta//2 if delta>=0 else -((-delta)//2))
        out,draws=compor_linha_bitmap(catalogo,out,texto=text,x=55+centre,y=212+line_height*i,
            fonte_u8=1,idioma_u32=idioma,multibyte_u32=multi,recorte=(55,212,310,486))
        calls.extend(draws)
    for dst,src in ((0x49a020,0x49a02c),(0x49a022,0x49a02e),(0x49a01c,0x49a030),(0x49a01e,0x49a032)):
        store('RestaureClipping',dst,current[src])
    return dict(pixels=bytes(out),chamadas=calls,efeitos=effects)
