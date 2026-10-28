"""Selective structure-record lifecycle translated from original x86.

The startup entry is only BatimentAlloc's prefix, ending before economic bags
and characteristic loading. None of these operations places or reserves a
structure, releases terrain, charges resources, or selects a sprite.
"""
import struct

PASSO = 276
QUANTIDADE = 1000

# Ordered (offset, format, value) stores, relative to 0x49a0c8 + i*0x114.
# Unlisted bytes must survive: these routines are not memset operations.
INICIALIZACAO = (
    (5, 'B', 0), (0x0a, 'H', 0), (0x78, 'H', 0xffff),
    (0x86, 'H', 0xffff), (0x88, 'H', 0xffff), (6, 'H', 0),
    (0x90, 'B', 1), (0, 'B', 0xff), (0x74, 'B', 0),
    (0x75, 'B', 0), (0x76, 'B', 0), (0x7b, 'B', 0xff),
    (0x82, 'H', 0), (0x7c, 'H', 0), (0x7a, 'B', 0),
    (0x80, 'H', 0), (0x7e, 'H', 0), (0xc4, 'H', 0),
    (0xc6, 'H', 0), (0xc2, 'H', 0), (0x84, 'H', 200),
    (0xc8, 'H', 0xffff), (2, 'H', 0xffff), (0x104, 'B', 0),
    (0x8a, 'B', 1), (0x8b, 'B', 1), (0x100, 'I', 0xffffffff),
    (4, 'B', 0xff), (8, 'B', 0xff), (0x8c, 'I', 0),
    (0x108, 'I', 0),
)
RESET_TODAS = (
    (5, 'B', 0), (6, 'H', 0), (0x0a, 'H', 0), (0, 'B', 0xff),
    (0x74, 'B', 0), (0x75, 'B', 0), (0x76, 'B', 0),
    (0x7b, 'B', 0xff), (0x7c, 'H', 0), (0x90, 'B', 0),
    (0x7e, 'H', 0), (0x80, 'H', 0), (0x82, 'H', 0),
    (0x84, 'H', 200), (0x8c, 'I', 0), (0x78, 'H', 0xffff),
    (0x86, 'H', 0xffff), (0x8a, 'B', 1), (0x8b, 'B', 1),
    (4, 'B', 0xff),
)


def _buffer(memoria, tamanho, nome):
    if not isinstance(memoria, bytearray) or len(memoria) != tamanho:
        raise ValueError(f'{nome} must be a writable bytearray of {tamanho} bytes')


def _escrever(memoria, base, escritas):
    for offset, formato, valor in escritas:
        struct.pack_into('<' + formato, memoria, base + offset, valor)


def inicializar_registros_estruturas(registros, realizaveis):
    """BatimentAlloc 0x418e95..0x419004; stop before external effects.

    Zero 88 flag bytes, then selectively initialize records in index order.
    The four trailing bytes +0x110..+0x113 are zeroed after each record.
    """
    _buffer(registros, QUANTIDADE * PASSO, 'registros')
    _buffer(realizaveis, 4 * 22, 'realizaveis')
    realizaveis[:] = bytes(88)
    for indice in range(QUANTIDADE):
        base = indice * PASSO
        _escrever(registros, base, INICIALIZACAO)
        registros[base + 0x110:base + 0x114] = bytes(4)


def resetar_todas_estruturas(registros, realizaveis, selecoes):
    """Complete BatimentResetAll, 0x41a75c; no terrain/economic callbacks."""
    _buffer(registros, QUANTIDADE * PASSO, 'registros')
    _buffer(realizaveis, 88, 'realizaveis')
    _buffer(selecoes, 8, 'selecoes')
    selecoes[:] = b'\xff' * 8
    realizaveis[:] = bytes(88)
    for indice in range(QUANTIDADE):
        _escrever(registros, indice * PASSO, RESET_TODAS)


def resetar_estrutura(registros, indice):
    """Complete ResetBatiment, 0x41b9d6; EAX index is truncated to u16.

    Type 20 preserves +0x80/+0x82; state 3 remains 3, every other state becomes
    5. The gate counter +0x76 is retained. Terrain is untouched.
    """
    _buffer(registros, QUANTIDADE * PASSO, 'registros')
    indice &= 0xffff
    if indice >= QUANTIDADE:
        raise ValueError('Structure index outside modeled pool (0..999)')
    base = indice * PASSO
    _escrever(registros, base, ((0x78, 'H', 0xffff), (0x7b, 'B', 0xff),
                              (0x7c, 'H', 0), (0x7e, 'H', 0)))
    tipo = registros[base + 8]
    struct.pack_into('<H', registros, base + 0x86, 0xffff)
    if tipo != 20:
        _escrever(registros, base, ((0x80, 'H', 0), (0x82, 'H', 0)))
    registros[base + 0x74] = 0
    estado = registros[base + 5]
    struct.pack_into('<I', registros, base + 0x8c, 0)
    if estado != 3:
        registros[base + 5] = 5


def buscar_estrutura_livre(registros):
    """CreerBatiment's first-free scan; does not reserve or create a record.

    Only state byte +5 matters. Return the first index or the u16 sentinel
    0xffff. The success checkpoint is 0x41ff04, before economic validation.
    """
    _buffer(registros, QUANTIDADE * PASSO, 'registros')
    return next((i for i in range(QUANTIDADE) if registros[i * PASSO + 5] == 0), 0xffff)
