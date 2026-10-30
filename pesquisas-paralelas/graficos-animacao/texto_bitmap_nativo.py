"""Original single-byte bitmap line (AffString 0x4591c8), independent of the AffText boundary.

Font1's glyphs execute natively in the committed real S1 objectives captures. No translated text or host font
is used. The prepared AffText matrix will separately establish its alignment and additional font domains.
"""
from graficos import compor_indices

BASE_FONTE1=0x23d5

class DependenciaTextoBitmap(Exception):
    def __init__(self,endereco,detalhe):
        self.endereco,self.detalhe=endereco,detalhe
        super().__init__(f'Bitmap text @0x{endereco:x}: {detalhe}')

def bytes_linha(texto):
    if not isinstance(texto,bytes):raise ValueError('Text must be original bytes')
    texto=texto.split(b'\0',1)[0].split(b'\n',1)[0]
    if len(texto)>127 or any(c<32 for c in texto):
        raise DependenciaTextoBitmap(0x4591c8,'Only bounded single-byte lines of at most127 printable bytes are proved')
    return texto

def largura_linha_bitmap(catalogo,texto,*,fonte_u8,idioma_u32,multibyte_u32):
    if any(type(v) is not int for v in (fonte_u8,idioma_u32,multibyte_u32)) or (fonte_u8,idioma_u32,multibyte_u32)!=(1,0,0):
        raise DependenciaTextoBitmap(0x458f5c,'Only font1 and captured single-byte language mode0 are proved')
    return sum(catalogo.quadro(BASE_FONTE1+(0x4c if c==32 else c-32)).largura for c in bytes_linha(texto))

def compor_linha_bitmap(catalogo,superficie,*,texto,x,y,fonte_u8,idioma_u32,multibyte_u32,recorte):
    """Return new800x600 indexed bytes and ordered PasteBobCmp calls; inputs never mutate.

    Explicit inclusive clip corresponds to the original CL=1 branch. Unsupported language/font/control
    paths raise at the original routine; no glyph callback or missing-text default is installed.
    """
    if len(superficie)!=800*600:raise ValueError('Expected800x600 indexed surface')
    if any(type(v) is not int or not -32768<=v<=32767 for v in (x,y)):
        raise ValueError('Text coordinates must be signed16-bit integers')
    if len(recorte)!=4 or any(type(v) is not int or not 0<=v<=65535 for v in recorte):
        raise ValueError('Clip must have four unsigned16-bit words')
    largura_linha_bitmap(catalogo,texto,fonte_u8=fonte_u8,idioma_u32=idioma_u32,multibyte_u32=multibyte_u32)
    out=bytes(superficie);calls=[]
    for c in bytes_linha(texto):
        q=catalogo.quadro(BASE_FONTE1+(0x4c if c==32 else c-32))
        if c!=32:
            ident=BASE_FONTE1+c-32
            out=compor_indices(out,800,600,q,x,y,recorte)
            calls.append(['PasteBobCmp',x,y,ident,1])
        x=((x+q.largura+32768)&65535)-32768
    return out,calls
