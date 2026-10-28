"""Physical SetSortEngin using established core collision/vision primitives."""
from dataclasses import dataclass
import struct
from insercao_unidades import DependenciaInsercaoUnidade,_preparar_insercao,_aplicar_insercao


class DependenciaColocacaoSaida(DependenciaInsercaoUnidade):
    def __init__(self, unidade):
        super().__init__(unidade,0x446146)


def colocar_unidade_saida(mundo, indice, celula):
    """0x445fbc complete supported exit; does not remove previous occupancy.

    Uses a live physical world, known type/owner, in-map cell and 128x128
    minimap. BB+F5 >8 stops before discovery, after collision/+72 stores.
    """
    indice,celula,p=_preparar_insercao(mundo,indice,celula & 65535)
    u = mundo.unidades
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
    _aplicar_insercao(mundo,indice,celula,DependenciaColocacaoSaida)


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
