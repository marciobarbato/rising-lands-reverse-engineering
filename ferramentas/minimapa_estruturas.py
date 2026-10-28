"""Original BatimentModifyMap: minimap footprint of one existing structure."""
import struct
from pegadas_estruturas import tamanho_estrutura


def modificar_minimapa_estrutura(mundo, indice, ativo):
    """0x419e97..0x419fc8 plus shared epilogue 0x42399a.

    AX index truncates to u16 (0..999); DL truncates to u8: nonzero calls
    SetMiniMap mode 6 (MissionPlaceTerrain and five other callers pass 1),
    zero calls mode 7 (DemonteBatiment). Rows ascend in y from the u16 origin
    +2 over the type's u16 width/height (0x495d8c/+2, stride 52), row-major,
    each cell skipped only when x or y reaches 256 (not the map size). The
    owner byte +4 is passed unchanged. No structure byte is written here.
    """
    indice &= 65535
    e = mundo.estruturas
    if not isinstance(e, (bytes, bytearray)) or len(e) != 276000 or indice >= 1000:
        raise ValueError('BatimentModifyMap requires a 1000-record structure pool and index 0..999')
    p = indice*276
    tipo, dono = e[p+8], e[p+4]
    modo = 6 if ativo & 255 else 7
    if (tipo >= 22 or not 1 <= mundo.largura <= 256 or not 1 <= mundo.altura <= 256
            or not 0 <= mundo.jogador_local < 4 or mundo.tamanho_minimapa != (128, 128)
            or (modo == 6 and dono != 200 and dono >= len(mundo.cores_jogadores))):
        raise ValueError('BatimentModifyMap requires type 0..21, camera 0..3, 128x128 minimap '
                         'and a colored owner for mode 6')
    origem = struct.unpack_from('<H', e, p+2)[0]
    largura, altura = tamanho_estrutura(tipo)
    x, y = origem & 255, origem >> 8
    for dy in range(altura):
        if y+dy >= 256:
            continue
        for dx in range(largura):
            if x+dx < 256:
                mundo.minimapa(dono, (origem + (dy << 8) + dx) & 65535, modo)
