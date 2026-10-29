"""Chemin_Remap first allocation/lock and two-pass temporary classification."""
import ctypes
from dataclasses import dataclass

from remapeamento_mundo import RemapeamentoPendente
from grade_u16 import GradeU16
from regioes_mapa import obstaculo_natural


class DependenciaClassificacaoRemapeamento(NotImplementedError):
    def __init__(self, checkpoint, importacao, argumentos):
        self.checkpoint, self.importacao, self.argumentos = checkpoint, importacao, argumentos
        super().__init__(f'Missing declared resource provider at 0x{checkpoint:x}, IAT 0x{importacao:x}; prior effects retained')


@dataclass(frozen=True)
class ClassificacaoRemapeamento:
    memoria: object
    alocacao_u32: int
    endereco_dependencia: int = 0x42ef8b


def _vista(dados, tamanho, *, gravavel=False):
    if not isinstance(dados, (bytes, bytearray, memoryview)):
        raise ValueError('Remap classification requires explicit byte buffers')
    v = memoryview(dados)
    if (v.ndim != 1 or not v.c_contiguous or v.format not in ('B', 'b')
            or v.nbytes != tamanho or (gravavel and v.readonly)):
        raise ValueError('Remap classification requires exact contiguous byte buffers and writable class memory')
    return v.cast('B')


def _sem_sobreposicao(destino, fontes):
    inicio = ctypes.addressof(ctypes.c_ubyte.from_buffer(destino))
    for fonte in fontes:
        if fonte.readonly:
            if fonte.obj is destino.obj:
                raise ValueError('Temporary class memory cannot alias a readonly terrain view')
            continue
        outro = ctypes.addressof(ctypes.c_ubyte.from_buffer(fonte))
        if inicio < outro+fonte.nbytes and outro < inicio+destino.nbytes:
            raise ValueError('Temporary class memory cannot overlap terrain inputs')


def retomar_classificacao_remapeamento(mundo, pedido, *, alocar=None, fixar=None):
    """Consume 0x42eebd without replaying reset; None lock -> False, else stop 0x42ef8b.

    Resource callbacks own actual allocation/lock effects. The returned live
    class buffer is not a labeled map or final successful remap result.
    """
    if (not isinstance(pedido, RemapeamentoPendente)
            or (pedido.flags, pedido.tamanho, pedido.endereco_dependencia, pedido.importacao)
            != (0, 65536, 0x42eebd, 0x5231c0)):
        raise ValueError('Expected the exact pre-allocation remap handoff')
    if alocar is None:
        raise DependenciaClassificacaoRemapeamento(0x42eebd, 0x5231c0, (0, 65536))
    handle = alocar(0, 65536) & 0xffffffff
    if fixar is None:
        raise DependenciaClassificacaoRemapeamento(0x42eec5, 0x5231d0, (handle,))
    memoria = fixar(handle)  # The original calls GlobalLock even for handle zero.
    if memoria is None:
        return False
    classes = _vista(memoria, 65536, gravavel=True)
    atributos = _vista(mundo.atributos, 65536)
    objetos = _vista(mundo.objetos, 65536)
    marcadores = _vista(mundo.marcadores_obstaculos_tiles, 702)
    vivo = isinstance(mundo.tiles, GradeU16)       # live grid: u16 by construction
    if not vivo and (not isinstance(mundo.tiles, (list, tuple)) or len(mundo.tiles) != 65536
                     or any(not isinstance(t, int) or not 0 <= t <= 65535 for t in mundo.tiles)):
        raise ValueError('Classification requires 65536 explicit u16 tiles')
    _sem_sobreposicao(classes, (atributos, objetos, marcadores) + ((_vista(memoryview(mundo.tiles.buffer).cast("B"), 131072),) if vivo else ()))
    for celula in range(65536):
        classes[celula] = atributos[celula] & 1
    for celula in range(65536):
        if not obstaculo_natural(mundo.tiles[celula], objetos[celula], marcadores):
            classes[celula] = 0
    return ClassificacaoRemapeamento(memoria, handle)
