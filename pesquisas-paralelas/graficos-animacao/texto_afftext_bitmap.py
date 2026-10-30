"""Pure AffText0x459454 bitmap provider, validated against270 complete original calls.

Original glyph banks, paired-font metrics, signed rectangle centring and clipped copies are preserved.
There is no host-font substitution, text-resource lookup, native execution or default probe boundary.
"""
from graficos import compor_indices
from texto_bitmap_nativo import DependenciaTextoBitmap

BASES=(0x23d5,0x24b5,0x2595,0x2675,0x2755,0x2835)

def _integer(value,lo,hi,name):
    if type(value) is not int or not lo<=value<=hi:raise ValueError(f'{name} outside {lo}..{hi}')
    return value

def _i16(value):return ((value+32768)&65535)-32768
def _half(value):return value//2 if value>=0 else -((-value)//2)

def planejar_texto_afftext(catalogo,request,*,idioma_u32,multibyte_u32):
    """Required request: original bytes, signed16-bit x/y/right/bottom, font u8, (colour,clip) u8 pair.

    Domain: fonts1..6, language/multibyte0/0, colour0, clip0/1, first NUL/newline-terminated printable
    line of at most127 bytes. Return original glyph calls and metrics; no inputs or world state mutate.
    """
    for name,value in (('language',idioma_u32),('multibyte',multibyte_u32)):_integer(value,0,0xffffffff,name)
    if (idioma_u32,multibyte_u32)!=(0,0):
        raise DependenciaTextoBitmap(0x459635,'External/multibyte font mode is not proved')
    required={'text','x','y','right','bottom','font','flags'}
    if not isinstance(request,dict) or not required<=request.keys():raise ValueError('Incomplete AffText request')
    if not isinstance(request['text'],bytes):
        raise DependenciaTextoBitmap(0x459454,'Actual text bytes are required; an opaque pointer is not empty text')
    line=request['text'].split(b'\0',1)[0].split(b'\n',1)[0]
    if len(line)>127 or any(c<32 for c in line):
        raise DependenciaTextoBitmap(0x459618,'Unproved control byte or signed-byte text-cursor overflow')
    font=_integer(request['font'],0,255,'font')
    if not 1<=font<=6:raise DependenciaTextoBitmap(0x459540,'Only the six captured bitmap fonts are proved')
    flags=request['flags']
    if not isinstance(flags,(tuple,list)) or len(flags)!=2:raise ValueError('AffText requires two flag bytes')
    colour,clip=(_integer(v,0,255,'flag') for v in flags)
    if colour:raise DependenciaTextoBitmap(0x459764,'Colour-substitution glyph blitter is not proved')
    if clip not in (0,1):raise DependenciaTextoBitmap(0x459788,'Only the captured clip bytes0/1 are proved')
    x,y,right,bottom=(_integer(request[n],-32768,32767,n) for n in ('x','y','right','bottom'))
    metrics_font=font if font&1 else font-1;metrics_base=BASES[metrics_font-1]
    height=catalogo.quadro(metrics_base+ord('j')-32).altura
    advances=[catalogo.quadro(metrics_base+(ord('l')-32 if c==32 else c-32)).largura for c in line]
    width=sum(advances)
    if x!=right:
        if _i16(width)<=right-x:x+=_half(right-x-_i16(width))
        y+=_half(bottom-y-_i16(height))
    x,y=_i16(x),_i16(y);calls=[]
    for c,advance in zip(line,advances):
        if c!=32:calls.append(['PasteBobCmp',x,y,BASES[font-1]+c-32,clip])
        x=_i16(x+advance)
    return dict(largura=width,altura=height,fonte_medidas=metrics_font,chamadas=calls)

def compor_texto_afftext(catalogo,superficie,*,request,recorte,idioma_u32,multibyte_u32):
    """Return(new800x600 indexed bytes,plan). Explicit clip words are(left,top,right,bottom), inclusive.

    Unclipped glyphs must fit the surface: invalid native out-of-buffer writes are named dependencies.
    Clipped positions retain original signed16-bit wrapping and the verified CMP opacity rules.
    """
    if len(superficie)!=480000:raise ValueError('Expected800x600 indexed surface')
    if not isinstance(recorte,(tuple,list)) or len(recorte)!=4:raise ValueError('Expected four inclusive clip words')
    for value in recorte:_integer(value,0,65535,'clip word')
    plan=planejar_texto_afftext(catalogo,request,idioma_u32=idioma_u32,multibyte_u32=multibyte_u32)
    # Validate all unclipped writes before changing even the local destination copy.
    for _,x,y,ident,clip in plan['chamadas']:
        q=catalogo.quadro(ident)
        if not clip and not(0<=x and 0<=y and x+q.largura<=800 and y+q.altura<=600):
            raise DependenciaTextoBitmap(0x45b247,'Unclipped glyph would write outside the supplied surface')
    out=bytes(superficie)
    for _,x,y,ident,clip in plan['chamadas']:
        out=compor_indices(out,800,600,catalogo.quadro(ident),x,y,recorte if clip else None)
    return out,plan

class TextoAffTextBitmap:
    """Explicit render_quadro texto(request,pixels) callback; construct with the actual clip/language inputs."""
    def __init__(self,catalogo,*,recorte,idioma_u32,multibyte_u32):
        self.catalogo,self.recorte=catalogo,tuple(recorte)
        self.idioma_u32,self.multibyte_u32=idioma_u32,multibyte_u32
    def __call__(self,request,superficie):
        return compor_texto_afftext(self.catalogo,superficie,request=request,recorte=self.recorte,
            idioma_u32=self.idioma_u32,multibyte_u32=self.multibyte_u32)[0]
