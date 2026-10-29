"""Ordered Chemin_Remap reset up to the first external allocation request."""
from dataclasses import dataclass

from grade_u16 import GradeU16
from ordens_unidades import ContextoBusca


@dataclass(frozen=True)
class RemapeamentoPendente:
    flags: int = 0
    tamanho: int = 65536
    endereco_dependencia: int = 0x42eebd
    importacao: int = 0x5231c0


def iniciar_remapeamento(mundo):
    """0x42ee1c..0x42eebd: reset in place, then expose pending GlobalAlloc.

    Does not read/reclassify terrain or reinsert occupants. Repeating this
    prefix clears its pools again; the returned request is not remap success.
    """
    cores = mundo.cores_estruturas
    if (not isinstance(mundo.busca,ContextoBusca)
            or not isinstance(mundo.regioes,(list,GradeU16)) or len(mundo.regioes) != 65536
            or not isinstance(cores.grade,bytearray) or len(cores.grade) != 65536
            or not isinstance(cores.livres,bytearray) or len(cores.livres) != 256
            or not isinstance(cores.liberadas,bytearray) or len(cores.liberadas) != 256
            or cores.livres is cores.liberadas):
        raise ValueError('Remap reset requires mutable search, regions and distinct exact-size color pools')
    mundo.busca.ocupada = 0
    mundo.busca.sucesso = 0
    mundo.busca.ponteiro_rota = 0
    mundo.busca.unidade = 65535
    cores.grade[:] = bytes(65536)
    cores.liberadas[:] = b'\x01'*256
    cores.livres[0] = 255
    for i in range(1,256):
        cores.livres[i] = i
    mundo.regioes[:] = [0]*65536
    return RemapeamentoPendente()
