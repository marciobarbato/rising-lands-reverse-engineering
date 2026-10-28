"""Two exact auxiliary readers after unit loading, before the Ghost reader."""
from dataclasses import dataclass
import ambiente_missoes
from formatos import Leitor


def _entrada(leitor,memoria,tamanho):
    if not isinstance(leitor,Leitor):
        raise ValueError('Leitor auxiliar incompatível')
    view=memoryview(memoria)
    if view.readonly or not view.c_contiguous or view.ndim!=1 or view.format!='B' or len(view)!=tamanho:
        raise ValueError('Buffer auxiliar incompatível')
    return view


def carregar_minas_missao(leitor,minas):
    """LoadMine47534a: N records of4 bytes; trailing origin words only clear."""
    view=_entrada(leitor,minas,80)
    count=leitor.u16()
    if count>20:
        raise ValueError('Quantidade de minas fora de0..20')
    for index in range(count):
        view[index*4:index*4+4]=leitor.ler(4)
    for index in range(count,20):
        view[index*4:index*4+2]=b'\0\0'
    return count


def carregar_ataques_missao(leitor,ataques):
    """IALoadAttaqueIni47c24d:100x10 inherited bytes plus a4-byte counter.

    Reset exact fields before the header; byte9 survives in every record.
    Supported disk records have size8 and count0..100. No AI is executed.
    """
    view=_entrada(leitor,ataques,1004)
    view[1000:1004]=bytes(4)
    for index in range(100):
        p=index*10
        view[p]=200;view[p+1]=255
        view[p+2:p+4]=b'\xff\xff'
        view[p+4]=view[p+5]=255
        view[p+6:p+8]=b'\xff\xff'
        view[p+8]=0
    count,size=leitor.u16(),leitor.u16()
    if count>100 or size!=8:
        raise ValueError('Configuração de ataque fora da variante suportada')
    for index in range(count):
        view[index*10:index*10+8]=leitor.ler(size)
    return count


@dataclass(frozen=True)
class AuxiliaresIniciais:
    minas:int
    ataques:int
    fim:int
    rotina_seguinte:int=0x47bcc7


def carregar_minas_e_ataques(leitor,minas,ataques):
    """Original post-unit call order, with a declared stop before Ghost loading."""
    count_mines=carregar_minas_missao(leitor,minas)
    count_attacks=carregar_ataques_missao(leitor,ataques)
    return AuxiliaresIniciais(count_mines,count_attacks,leitor.posicao)
