"""Original TerrainReset and MiniMapReset over explicit live world layers."""
import struct
from candidatos_rota import aleatorio_caminhos


def _gravavel(buffer, tamanho):
    if isinstance(buffer, bytearray):
        return len(buffer) == tamanho
    return (isinstance(buffer, memoryview) and not buffer.readonly and buffer.contiguous
            and buffer.format in ('B', 'b') and buffer.nbytes == tamanho)


def _distintos(buffers):
    """Protected aliasing check: identity of allocations and memoryview owners."""
    donos = [b.obj if isinstance(b, memoryview) else b for b in buffers]
    return len({id(d) for d in donos}) == len(donos)


def resetar_terreno(mundo, minas, aleatorio):
    """0x46b315..0x46b38f: clear terrain/vision layers, draw object aux, clear mine origins.

    For every cell 0..65535: objects 0, aux = Random() & 3, attributes 0,
    then per owner 0..3 light count 0, light edges 0x1f, discovery 0x1f.
    Random 0x4704dc advances the live u32 state at 0x497164 once per cell
    (EAX=0x28 is passed but unused). Afterwards the origin word of each of the
    20 mine records (0x509954, stride 4) is zeroed; reserve words remain.
    Tiles, regions, minimap layers, units and structures are untouched.
    Every allocation is checked before the first store; nothing can fail later.
    """
    grades = [list(getattr(mundo, nome)) for nome in ('contagem_luz', 'luz_bordas', 'descoberto')]
    camadas = [mundo.objetos, mundo.donos_objetos, mundo.atributos] + [g for grade in grades for g in grade]
    if (any(len(grade) != 4 for grade in grades) or not all(_gravavel(c, 65536) for c in camadas)
            or not _gravavel(minas, 80) or not _gravavel(aleatorio, 4)
            or not _distintos(camadas + [minas, aleatorio])):
        raise ValueError('TerrainReset requires distinct writable 65536-byte layers, four owner grids, '
                         '80-byte mines and a 4-byte Random state')
    semente = struct.unpack_from('<I', aleatorio, 0)[0]
    donos = mundo.donos_objetos
    # Distinct protected allocations make the per-cell interleaving unobservable:
    # each layer gets its final value and the draws stay in ascending cell order.
    for celula in range(65536):
        semente = aleatorio_caminhos(semente)
        donos[celula] = semente & 3
    zeros, bordas = bytes(65536), b'\x1f' * 65536
    mundo.objetos[:] = zeros
    mundo.atributos[:] = zeros
    for contagem, borda, descoberto in zip(*grades):
        contagem[:] = zeros
        borda[:] = bordas
        descoberto[:] = bordas
    struct.pack_into('<I', aleatorio, 0, semente)
    for registro in range(20):
        struct.pack_into('<H', minas, registro*4, 0)


def resetar_minimapa(mundo):
    """0x469f00..0x469f68: memset w*h bytes of final=2, units=0, structures=0.

    w/h are the u16 minimap dimensions (0x496fe0/0x496fe2); the product is
    32-bit and must fit the 65,536-byte layers. Bytes after w*h are retained.
    """
    largura, altura = mundo.tamanho_minimapa
    if not (isinstance(largura, int) and isinstance(altura, int) and 0 <= largura < 65536
            and 0 <= altura < 65536):
        raise ValueError('MiniMapReset requires u16 minimap dimensions')
    n = largura*altura
    camadas = (mundo.mini_final, mundo.mini_unidades, mundo.mini_estruturas)
    if n > 65536 or not all(_gravavel(c, 65536) for c in camadas) or not _distintos(list(camadas)):
        raise ValueError('MiniMapReset requires three distinct writable 65536-byte layers and w*h <= 65536')
    mundo.mini_final[:n] = b'\x02' * n
    mundo.mini_unidades[:n] = bytes(n)
    mundo.mini_estruturas[:n] = bytes(n)
