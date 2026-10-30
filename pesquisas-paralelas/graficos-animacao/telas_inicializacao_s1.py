"""Prepared pixel plans for S1's two real MenuInit transitions, with explicit picture/text dependencies.

Missions supplies mission number/message lookup and Economy supplies resolved research levels, colour and
percentage text. This module reconstructs drawing only; it neither loads mission state nor computes research.
LoadPie and AffText are required callbacks, including when a benchmark deliberately declares non-execution.
"""
from texto_bitmap_nativo import DependenciaTextoBitmap

class DependenciaInicializacaoS1(DependenciaTextoBitmap):
    def __init__(self,endereco,detalhe,pixels,chamadas):
        super().__init__(endereco,detalhe);self.pixels=bytes(pixels);self.chamadas=list(chamadas)

def compor_inicializacao_s1(memoria,superficie,*,jogador_u8,modo_destino_u8,carregar_pie=None,texto=None,
        numero_missao_u16=None,niveis_pesquisa=None,cor_jogador_u8=None,percentual_texto=None,mensagem=None):
    """Return indexed pixels and raster/external drawing calls for the captured0x12→0x13→0x11 transitions.

    All query results are required explicit prepared inputs at their original use. Unknown values stop;
    callback outputs must be full480000-byte surfaces. An opaque message remains a pointer token, never an
    empty byte string. No default picture/text callback is installed, and memory/surface inputs do not mutate.
    """
    if len(superficie)!=480000:raise ValueError('Expected800x600 indexed surface')
    out=bytes(superficie);calls=[];external=[]
    def stop(pc,why):raise DependenciaInicializacaoS1(pc,why,out,calls)
    mode=memoria.u8(0x4e2f78)
    if (type(jogador_u8) is not int or jogador_u8!=0 or type(modo_destino_u8) is not int
        or (mode,modo_destino_u8) not in ((0x12,0x13),(0x13,0x11))
        or memoria.u8(0x508041)!=0 or (memoria.u16(0x49a018),memoria.u16(0x49a01a))!=(800,600)):
        stop(0x4682bb,'Menu initialization outside the two captured owner/camera0 S1 transitions')
    prefix=bytearray()
    for i in range(1024):
        value=memoria.u8(0x509494+i)
        if not value:break
        prefix.append(value)
    else:stop(0x468ad4,'File prefix has no bounded terminator')
    if modo_destino_u8==0x11:
        if type(numero_missao_u16) is not int or numero_missao_u16!=2:
            stop(0x46c11a,'The actual captured next-mission number2 must be supplied')
        filename=bytes(prefix)+b'\\pagemis2.pie'
    else:filename=bytes(prefix)+b'\\ecranfin.lzs'
    request=dict(arquivo=filename)
    if not callable(carregar_pie):stop(0x4799c4,'LoadPie picture provider is missing')
    external.append(['LoadPie',filename.hex()]);out=carregar_pie(request,out)
    if not isinstance(out,bytes) or len(out)!=480000:raise ValueError('LoadPie must return full indexed surface bytes')
    if modo_destino_u8==0x13:
        if mensagem is None:stop(0x478a3b,'Actual TextGetMessage(0x74) result must be supplied')
        if not isinstance(mensagem,dict) or set(mensagem)!={'pointer','text'}:raise ValueError('Message requires pointer and text')
        ptr=mensagem['pointer'];raw=mensagem['text']
        if type(ptr) is not int or not 0<=ptr<=0xffffffff or raw is not None and not isinstance(raw,bytes):
            raise ValueError('Message pointer/text has invalid type')
        request=dict(text=raw,text_pointer=ptr,x=0,y=145,right=450,bottom=215,font=3,flags=(0,0))
    else:
        if (not isinstance(niveis_pesquisa,tuple) or len(niveis_pesquisa)!=4
                or any(type(v) is not int or not 0<=v<=255 for v in niveis_pesquisa)):
            stop(0x4717c2,'Four actual unsigned-byte research levels must be supplied')
        if niveis_pesquisa!=(2,2,4,0) or type(cor_jogador_u8) is not int or cor_jogador_u8!=160:
            stop(0x4717c2,'Actual research levels(2,2,4,0) and player colour160 must be supplied')
        surface=bytearray(out)
        for column,branch in enumerate((0,2,1,3)):
            for index in range(niveis_pesquisa[branch]):
                left=442+103*column;top=425-15*index;right=446+103*column;bottom=435-15*index
                calls.append(['FilledBox',left,top,right,bottom,cor_jogador_u8,0])
                for y in range(top,bottom+1):surface[y*800+left:y*800+right+1]=bytes([cor_jogador_u8])*(right-left+1)
        out=bytes(surface)
        if percentual_texto!=b'0%':stop(0x4687fa,'Actual captured percentage text0% must be supplied')
        request=dict(text=percentual_texto,x=680,y=51,right=735,bottom=87,font=1,flags=(0,0))
    if not callable(texto):stop(0x459454,'AffText provider or explicitly attested probe boundary is missing')
    external.append(['AffText',request]);out=texto(request,out)
    if not isinstance(out,bytes) or len(out)!=480000:raise ValueError('AffText must return full indexed surface bytes')
    return dict(pixels=out,chamadas=calls,externas=external)
