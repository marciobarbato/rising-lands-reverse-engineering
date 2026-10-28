"""Original unit-selection initialization and owner/flag query."""
import struct


def inicializar_selecoes_unidades(selecoes):
    """0x472555; preserve list tails and every caller-owned unit flag."""
    if not isinstance(selecoes, bytearray) or len(selecoes) != 2048:
        raise ValueError('SelectionInit requires exactly 2048 writable selection bytes')
    for offset in (0, 512, 1024, 1536):
        struct.pack_into('<H', selecoes, offset, 0)


def unidade_selecionada(mundo, jogador, indice):
    """0x472174 consumed AL: owner match and nonzero live +bd, no list read."""
    jogador, indice = jogador & 255, indice & 65535
    if not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800 or indice >= 800:
        raise ValueError('Selection query requires live 800-record pool and unit 0..799')
    p = indice*276
    return mundo.unidades[p+0xbd] != 0 and mundo.unidades[p] == jogador
