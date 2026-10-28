"""Physical SetSortEngin using established core collision/vision primitives."""
from dataclasses import dataclass
import struct


class DependenciaColocacaoSaida(NotImplementedError):
    def __init__(self, unidade):
        self.unidade, self.endereco, self.checkpoint = unidade, 0x476851, 0x446146
        super().__init__('Vision radius above the validated 0..8 sum requires DecouvreTerrain; '
                         'prior record/collision effects retained')


def colocar_unidade_saida(mundo, indice, celula):
    """0x445fbc complete supported exit; does not remove previous occupancy.

    Uses a live physical world, known type/owner, in-map cell and 128x128
    minimap. BB+F5 >8 stops before discovery, after collision/+72 stores.
    """
    indice, celula = indice & 65535, celula & 65535
    u = mundo.unidades
    if (not isinstance(u, bytearray) or len(u) != 220800 or indice >= 800
            or not 1 <= mundo.largura <= 256 or not 1 <= mundo.altura <= 256
            or not 0 <= mundo.jogador_local < 4 or mundo.tamanho_minimapa != (128, 128)
            or (celula & 255) >= mundo.largura or (celula >> 8) >= mundo.altura):
        raise ValueError('Exit requires a live physical pool, valid index/cell/camera and 128x128 minimap')
    p = indice*276
    if u[p+1] >= 26 or u[p] not in (0, 1, 2, 3, 4, 200):
        raise ValueError('Exit requires known type 0..25 and owner 0..3/4/200')
    for off in (0x7e, 0x7c, 8, 0x7e):
        struct.pack_into('<H', u, p+off, celula)
    mundo._liberar_busca(indice)
    u[p+0x88] = 0
    if u[p+2] not in (0, 4):
        u[p+2] = 7
        mundo._liberar_busca(indice)
    struct.pack_into('<H', u, p+0xc0, 65535)
    struct.pack_into('<H', u, p+0xb8, 65535)
    u[p+0x87] = u[p+0x86] = 0
    mundo.ocupar(indice, celula, True)
    u[p+0x72] = 1
    dono = u[p]
    if dono not in (4, 200):
        raio = u[p+0xbb]+u[p+0xf5]
        if raio > 8:
            raise DependenciaColocacaoSaida(indice)
        mundo.descobrir_area(celula, raio+2, dono)
        raio = u[p+0xbb]+u[p+0xf5]
        mundo.iluminar_area(celula, raio, dono)
    mundo.minimapa(u[p], celula, 4)


@dataclass(frozen=True)
class ColocacaoSaidaTropa:
    indice: int
    unidade: int
    celula: int
    tipo_unidade: int
    destino_ordem: int
    endereco_dependencia: int = 0x420f9e


def retomar_colocacao_saida(mundo, pedido):
    """One-shot placement then original movement order; stop before request."""
    if pedido.endereco_dependencia != 0x420f8a:
        raise ValueError('Expected experience handoff at 0x420f8a')
    indice, unidade, celula = pedido.indice & 65535, pedido.unidade & 65535, pedido.celula & 65535
    if not isinstance(mundo.estruturas, bytearray) or len(mundo.estruturas) != 276000 or indice >= 1000:
        raise ValueError('Exit continuation requires building 0..999 and writable structure pool')
    colocar_unidade_saida(mundo, unidade, celula)
    destino = struct.unpack_from('<H', mundo.estruturas, indice*276+0x7c)[0]
    mundo.definir_movimento(unidade, destino)
    return ColocacaoSaidaTropa(indice, unidade, celula, mundo.unidades[unidade*276+1], destino)
