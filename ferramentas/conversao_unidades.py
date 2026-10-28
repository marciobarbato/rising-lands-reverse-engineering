"""Bridge the committed local EnginSetType provider into shared core state.

The provider remains combat-owned. This adapter supplies live memory and search
release; explicit read-only query providers supply capacity/modifiers. It does
not occupy terrain, heal, run economic preparation, or finish SortieTroupe.
"""
from dataclasses import dataclass
import importlib
from pathlib import Path
import struct
import sys


def _provedor():
    caminho = str(Path(__file__).resolve().parents[1] / 'pesquisas-paralelas/combate')
    # The committed provider uses local absolute imports. Do not accidentally
    # reuse another checkout/snapshot's same-named modules in this process.
    for nome in ('inicializacao_ataque', 'animacao_disparo', 'alvos_alcance', 'mira_angular'):
        modulo = sys.modules.get(nome)
        if modulo is not None and Path(modulo.__file__).resolve().parent != Path(caminho):
            raise ImportError('Conversion requires the committed combat provider from this checkout')
    sys.path.insert(0, caminho)
    try:
        return importlib.import_module('inicializacao_ataque')
    finally:
        sys.path.remove(caminho)


class _BuscaCompartilhada:
    def __init__(self, mundo):
        self.mundo = mundo

    def liberar(self, indice):
        self.mundo._liberar_busca(indice)


def converter_unidade(mundo, indice, celula, direcao, tipo, tipos_unidades,
                     *, capacidade_tipo=None, modificador=None):
    """Mutate the existing live record through original local conversion.

    Integer inputs truncate to u16/u16/u8/u8. Supported unit indices 0..799,
    types 0..25, and a preloaded 26*50-byte type table. Missing query providers
    raise NotImplementedError at their original call boundary, retaining prior
    record/search mutations. Query providers must not mutate shared state.
    """
    indice, celula = indice & 65535, celula & 65535
    direcao, tipo = direcao & 255, tipo & 255
    if (not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800
            or indice >= 800 or tipo >= 26 or len(tipos_unidades) != 1300
            or not callable(getattr(mundo, '_liberar_busca', None))):
        raise ValueError('Conversion requires live core state, unit 0..799, type 0..25, and 1300 type bytes')
    provedor = _provedor()
    base = tipo * 50
    caracteristicas = provedor.CaracteristicasTipo(*(struct.unpack_from('<H', tipos_unidades, base + off)[0]
                                                    for off in (0x2a, 0x2c, 0x30)))

    def capacidade(t):
        if capacidade_tipo is None:
            raise NotImplementedError('EnginTypeGetCapacite provider required after characterization')
        return capacidade_tipo(t) & 65535

    def bonus(dono, t, seletor):
        if modificador is None:
            raise NotImplementedError(f'BonusGetValEngin provider required for selector {seletor}')
        return modificador(dono, t, seletor) & 255

    # A copied bytearray followed by writeback would discard partial effects on
    # a query failure. This view exposes every prior store immediately.
    with memoryview(mundo.unidades)[indice * 276:(indice + 1) * 276] as registro:
        provedor.definir_tipo(registro, indice, celula, direcao, tipo, caracteristicas,
                             capacidade, bonus, _BuscaCompartilhada(mundo))


@dataclass(frozen=True)
class ConversaoSaidaTropa:
    indice: int
    unidade: int
    celula: int
    tipo_unidade: int
    endereco_dependencia: int = 0x420f6e


def retomar_conversao_saida(mundo, pedido, tipos_unidades, *, capacidade_tipo=None,
                           modificador=None, dimensoes=None):
    """Resume a prepared economy handoff through 0x420f5a..0x420f6e.

    Do not rerun the economic prefix or retry after partial conversion failure.
    The pending type snapshot is deliberately ignored: original +7b is read
    after the complete position query. The result still requires healing and
    the remaining original production caller; it is not a spawned-unit claim.
    """
    if pedido.endereco_dependencia != 0x420698:
        raise ValueError('Expected an economy handoff stopped before CalculPosition')
    from posicao_saida import calcular_posicao_saida
    indice = pedido.indice & 65535
    celula = calcular_posicao_saida(mundo, indice, pedido.direcao, dimensoes)
    tipo = mundo.estruturas[indice * 276 + 0x7b]
    converter_unidade(mundo, pedido.unidade, celula, pedido.direcao, tipo, tipos_unidades,
                     capacidade_tipo=capacidade_tipo, modificador=modificador)
    return ConversaoSaidaTropa(indice, pedido.unidade & 65535, celula, tipo)
