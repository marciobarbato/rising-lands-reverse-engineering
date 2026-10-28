"""Complete CalculPosition (0x420698), returning the caller-consumed AX cell.

The BL direction supplied by SortieTroupe is unused by the original body.
This arithmetic query neither checks passage nor converts or moves a unit.
"""
import struct
from pegadas_estruturas import tamanho_estrutura

# Per-type dispatch through 0x420640 and its ten subordinate tables.
# Entries: width subtraction, height subtraction, immediate correction, addback.
# None represents the original direct return of zero (types 9, 12, 17).
AJUSTES = (
    (3, 2, 0x201, 0x102), (1, 1, 0x300, 0xff),
    (4, 2, 0x101, 0x102), (4, 2, 0x202, 0x102),
    (4, 2, 0x100, 0x102), (1, 0, 0x202, 0x102),
    (4, 2, 0x100, 0x102), (4, 1, 0x300, 0x102),
    (6, 4, 0x202, 0x102), None,
    (3, 2, 0, 0x102), (3, 2, 0, 0x102), None,
    (4, 1, 0x200, 0x102), (6, 4, 0x300, 0x102),
    (4, 1, 0x100, 0x102), (4, 2, 0x100, 0x102), None,
    (1, 1, 0x201, 1), (4, 2, 0x100, 0x102),
    (4, 1, 0x100, 0x102), (4, 2, 0x100, 0x102),
)


def calcular_posicao_saida(mundo, indice, direcao=0, dimensoes=None):
    """Return a u16 cell from an existing structure's type and origin.

    The integer index truncates to AX and must address records 0..999; type
    must be 0..21. Optional width/height override the original u16 geometry
    words for this query and truncate to u16. No playable-map clipping or
    collision check is implied. Type 9/12/17 returns zero, not the origin.
    """
    indice &= 65535
    direcao &= 255  # accepted caller width; deliberately absent from arithmetic
    if not 0 <= indice < 1000 or len(mundo.estruturas) != 276000:
        raise ValueError('CalculPosition requires a 1000-record structure pool')
    p = indice * 276
    tipo = mundo.estruturas[p + 8]
    if tipo >= 22:
        raise ValueError('CalculPosition supports structure types 0..21')
    if dimensoes is None:
        largura, altura = tamanho_estrutura(tipo)
    else:
        if len(dimensoes) != 2:
            raise ValueError('CalculPosition requires width and height')
        largura, altura = (n & 65535 for n in dimensoes)
    ajuste = AJUSTES[tipo]
    if ajuste is None:
        return 0
    origem = struct.unpack_from('<H', mundo.estruturas, p + 2)[0]
    dx, dy, correcao, reposicao = ajuste
    # Only low 16 bits reach the caller's DX. All original intermediate 32-bit
    # overflows/underflows have the same low word under this expression.
    return (origem + ((altura - dy) << 8) + largura - dx - correcao + reposicao) & 65535
