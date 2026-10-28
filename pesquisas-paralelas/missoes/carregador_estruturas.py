"""Inline mission structure-copy continuation, after explicit natural remap."""
from dataclasses import dataclass
import ambiente_missoes
from formatos import Leitor


@dataclass(frozen=True)
class CargaEstruturas:
    quantidade:int
    indices:tuple
    fim:int
    rotina_seguinte:int=0x46acbf


def carregar_estruturas_missao(leitor,estruturas):
    """0x46c517..0x46c578 and0x46c8e0..0x46c941: identical copy effects.

    Supply an inherited writable276000-byte pool and the committed Leitor at
    the u16 count,size header. Size204 is the studied domain. File indices
    are u16 protected to0..999; count is independent of slot capacity because
    repeated indices overwrite in file order. Retain all72 unpopulated bytes
    per slot, all unloaded records and prior effects on strict-reader failure.
    Reset/remap, placement and the following LoadEngin call are not executed.
    """
    if not isinstance(leitor,Leitor):
        raise ValueError('Leitor de estruturas incompatível')
    pool=memoryview(estruturas)
    if pool.readonly or not pool.c_contiguous or pool.ndim!=1 or pool.format!='B' or len(pool)!=276000:
        raise ValueError('Tabela de estruturas incompatível')
    count,size=leitor.u16(),leitor.u16()
    if size!=204:
        raise ValueError('Tamanho de estrutura fora da variante suportada')
    indices=[]
    for _ in range(count):
        index=leitor.u16()
        if index>=1000:
            raise ValueError('Índice de estrutura fora da tabela')
        pool[index*276:index*276+204]=leitor.ler(size)
        indices.append(index)
    return CargaEstruturas(count,tuple(indices),leitor.posicao)
