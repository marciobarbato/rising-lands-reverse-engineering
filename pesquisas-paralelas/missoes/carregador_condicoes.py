"""Original condition/objective table loading, without mission evaluation."""
from dataclasses import dataclass
import ambiente_missoes
from formatos import Leitor


@dataclass(frozen=True)
class TabelaMissaoCarregada:
    quantidade: int
    fim: int
    rotina_seguinte: int


def _entrada(leitor,memoria,tamanho):
    if not isinstance(leitor,Leitor):
        raise ValueError('Leitor de tabela de missão incompatível')
    view = memoryview(memoria)
    if view.readonly or not view.c_contiguous or view.ndim != 1 or view.format != 'B' or len(view) != tamanho:
        raise ValueError('Buffer de tabela de missão incompatível')
    return view


def carregar_condicoes_fim(leitor,memoria):
    """LoadFinMission0x458b05: inherited114 bytes at0x4e1d20.

    Ten10-byte records are followed by four retained result/global bytes,
    then ten status bytes at+104. Only the first byte of each record is reset
    before reading. The protected header domain is N0..10,S10. Prior effects
    persist on strict read failure. No code is interpreted or evaluated.
    """
    view = _entrada(leitor,memoria,114)
    for index in range(10):
        view[index*10] = 255
    count,size = leitor.u16(),leitor.u16()
    if count > 10 or size != 10:
        raise ValueError('Tabela de condições fora da variante suportada')
    for index in range(count):
        view[index*10:index*10+10] = leitor.ler(size)
        view[104+index] = 0
    return TabelaMissaoCarregada(count,leitor.posicao,0x47c30f)


def carregar_objetivos(leitor,memoria):
    """LoadObjectif0x47c404: inherited804 bytes at0x511ffc.

    Four players*100u16 words (800 bytes), followed by four retained cursor
    bytes at0x51231c. Disk data is400(word,flag) pairs; flags go to original
    stack scratch only. This load does not reset cursors or read text files.
    """
    view = _entrada(leitor,memoria,804)
    view[:800] = b'\xff'*800
    for player in range(4):
        for ordinal in range(100):
            offset = player*200+ordinal*2
            view[offset:offset+2] = leitor.ler(2)
            leitor.ler(1)
    return TabelaMissaoCarregada(400,leitor.posicao,0x47ac30)
