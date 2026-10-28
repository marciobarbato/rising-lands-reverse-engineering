"""MissionLoad successful-open continuation, ending before natural remapping."""
from dataclasses import dataclass
import struct
import ambiente_missoes
from formatos import Leitor
from economia import Economia
from sequenciais import normalizar_inicio


@dataclass(frozen=True)
class CabecalhoCarregado:
    largura: int
    altura: int
    jogador_visualizacao: int
    fim: int
    rotina_seguinte: int = 0x42ee1c


def continuar_cabecalho(leitor, atributos, terreno, objetos, auxiliares, economia,
                        dimensoes, visualizacao, jogador_visualizacao):
    """0x46c396..0x46c512: caller supplies every inherited buffer/provider.

    Leitor must start at file position0 after successful open. Four layer
    byte buffers have lengths65536/131072/65536/65536. Dimensions and view
    are separate four-byte buffers; the selected-player byte truncates to u8.
    Economia is an explicitly inherited128-byte provider, not a default world.
    Global reset/open failure, remap and later record loading are outside scope.
    Strict read failures retain earlier stores; Win32 short reads are excluded.
    """
    if not isinstance(leitor, Leitor) or leitor.posicao != 0 or not isinstance(economia, Economia):
        raise ValueError('Entradas do cabeçalho de missão incompatíveis')
    views = []
    for buffer, size in zip((atributos, terreno, objetos, auxiliares, dimensoes, visualizacao),
                            (65536, 131072, 65536, 65536, 4, 4)):
        view = memoryview(buffer)
        if view.readonly or not view.c_contiguous or view.ndim != 1 or view.format != 'B' or len(view) != size:
            raise ValueError('Buffer do cabeçalho de missão incompatível')
        views.append(view)
    resource_memory = memoryview(economia.memoria)
    if (resource_memory.readonly or not resource_memory.c_contiguous or resource_memory.ndim != 1
            or resource_memory.format != 'B' or len(resource_memory) != 128):
        raise ValueError('Tabela de recursos incompatível')
    attributes, tiles, objects, auxiliary, dimensions, camera_view = views
    camera = jogador_visualizacao & 255
    buscar = getattr(leitor, 'buscar', None)
    if callable(buscar):
        buscar(4, 0)  # FileSeek 0x45848b(4, SEEK_SET) request, for a recording reader.
    else:
        leitor.ler(4)  # Original seeks absolute4; it does not validate the version.
    for layer in (attributes, tiles, objects, auxiliary):
        layer[:] = leitor.ler(len(layer))
    normalized = normalizar_inicio(objects, auxiliary)
    objects[:] = normalized['objetos']
    auxiliary[:] = normalized['auxiliares']
    for resource in (1, 2, 0):
        for player in range(4):
            amount = leitor.u16()
            economia.atribuir(player, resource, amount)
    dimensions[:2] = leitor.ler(2)
    dimensions[2:] = leitor.ler(2)
    for player in range(4):
        for part in (0, 2):
            raw = leitor.ler(2)
            if camera == player:
                camera_view[part:part+2] = raw
    width, height = struct.unpack('<HH', dimensions)
    return CabecalhoCarregado(width, height, camera, leitor.posicao)
