"""Indexed ETA unit loading, with an explicit committed selection initializer.

The continuation covers 0x46acca through LoadEngin's return. The full entry
composes core SelectionInit before it. Neither is MissionLoad or a prepared
world. The caller supplies inherited memory and already-loaded types.
Combat owns the per-record postload body; this module only orders reads and
effects. Modifier callbacks must be read-only with respect to loader inputs.
"""
from dataclasses import dataclass
import struct
import ambiente_missoes
from formatos import Leitor
from inicializacao_ataque import CaracteristicasTipo, preparar_apos_carga_missao
from selecao_unidades import inicializar_selecoes_unidades


class DependenciaCargaUnidades(NotImplementedError):
    def __init__(self, endereco, detalhe):
        self.endereco = endereco
        super().__init__(f'Carga de unidades pendente em 0x{endereco:08x}: {detalhe}')


@dataclass(frozen=True)
class CargaUnidades:
    quantidade: int
    indices: tuple
    fim: int
    # This metadata describes a checkpoint, never world/mission readiness.
    rotina_seguinte: int = 0x47534a


def continuar_carga_unidades(leitor, unidades, valores_jogador, tipos_unidades, *, modificador12=None):
    """Continue after SelectionInit, mutating shared writable buffers in order.

    `leitor` is the committed Leitor at the indexed block header; `unidades`
    is 800*276 inherited bytes, `valores_jogador` the four bytes at 0x4e19bc,
    and `tipos_unidades` 26*50 already-loaded bytes. No zero pool/table is
    manufactured. Supported records have size 784, IDs 0..799, and active
    types 0..25. Active type 4 needs (owner,type)->modifier12 except 4/200.
    Earlier copies/stores persist when a read or dependency fails. Reentry
    after failure restarts this continuation and is not a resume token.
    """
    if not isinstance(leitor, Leitor):
        raise ValueError('Leitor ETA incompatível')
    pool = memoryview(unidades)
    flags = memoryview(valores_jogador)
    types = memoryview(tipos_unidades)
    if (pool.readonly or flags.readonly or not pool.c_contiguous or not flags.c_contiguous
            or not types.c_contiguous or pool.ndim != 1 or flags.ndim != 1 or types.ndim != 1
            or pool.format != 'B' or flags.format != 'B' or types.format != 'B'
            or len(pool) != 220800 or len(flags) != 4 or len(types) != 1300):
        raise ValueError('Buffers de carga de unidades incompatíveis')
    if modificador12 is not None and not callable(modificador12):
        raise ValueError('Consulta de modificador incompatível')
    flags[:] = b'\x32' * 4
    count, size = leitor.u16(), leitor.u16()
    if size != 784 or count > 800:
        raise ValueError('Bloco de unidades fora da variante suportada')
    indices = []
    for ordinal in range(count):
        index = leitor.u16()
        if index >= 800:
            raise ValueError('Índice de unidade fora da tabela')
        unit = pool[index*276:(index+1)*276]
        unit[:140] = leitor.ler(140)
        leitor.ler(512)  # Successful in-memory equivalent of FileSeek(+512,1).
        unit[140:272] = leitor.ler(size-652)
        pool[ordinal*276+0xbd] = 0  # Original uses BX ordinal, NOT the disk ID.
        if unit[2]:
            kind = unit[1]
            if kind >= 26:
                raise DependenciaCargaUnidades(0x457350, 'tipo ativo sem tabela carregada')
            params = CaracteristicasTipo(*(struct.unpack_from('<H', types, kind*50+off)[0]
                                          for off in (42, 44, 48)))

            def modifier(owner, unit_type):
                if modificador12 is None:
                    raise DependenciaCargaUnidades(0x428cc0, 'modificador 12 não fornecido')
                return modificador12(owner, unit_type)

            preparar_apos_carga_missao(unit, params, modifier)
        indices.append(index)
    return CargaUnidades(count, tuple(indices), leitor.posicao)


def carregar_unidades_missao(leitor, unidades, valores_jogador, tipos_unidades,
                             selecoes_unidades, *, modificador12=None):
    """Complete LoadEngin entry: original SelectionInit before the continuation.

    Selection memory must be the explicit inherited bytearray2048 accepted by
    the committed core provider. Its four word stores precede continuation
    input checks and all reads/copies. Therefore a later validation, read or
    modifier failure retains those selection stores. No unit flag is scanned
    or cleared by SelectionInit; only the subsequent original ordinal writes
    affect +bd. This is one loader body, not an initialized live world.
    """
    inicializar_selecoes_unidades(selecoes_unidades)
    return continuar_carga_unidades(leitor,unidades,valores_jogador,tipos_unidades,
                                     modificador12=modificador12)
