"""Original SelectionInit: clear four count words without scanning units."""
import struct


def inicializar_selecoes_unidades(selecoes):
    """0x472555; preserve list tails and every caller-owned unit flag."""
    if not isinstance(selecoes, bytearray) or len(selecoes) != 2048:
        raise ValueError('SelectionInit requires exactly 2048 writable selection bytes')
    for offset in (0, 512, 1024, 1536):
        struct.pack_into('<H', selecoes, offset, 0)
