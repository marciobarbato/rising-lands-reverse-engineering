"""Join the economic bonus producer to the committed core capacity refresh."""
import importlib
from pathlib import Path
import sys

from bonus_unidades import capacidade_tipo


def _atualizador_core():
    pasta=Path(__file__).resolve().parents[2]/'ferramentas'
    atual=sys.modules.get('capacidades_unidades')
    if atual is not None and Path(atual.__file__).resolve()!=pasta/'capacidades_unidades.py':
        raise ImportError('Capacity refresh requires the committed core provider from this checkout')
    sys.path.insert(0,str(pasta))
    try:
        return importlib.import_module('capacidades_unidades').atualizar_capacidades_unidades
    finally:
        sys.path.remove(str(pasta))


def definir_bonus_no_mundo(bonus,mundo,jogador,tipo,seletor,valor):
    """Run the setter once, then the actual live-world callback for selector 1.

    No buffers are copied. The core provider loads only at the original refresh
    boundary, after bonus writes; import/guard/query errors retain those writes
    and any earlier unit capacity stores. Other selectors do not touch core.
    Queries must not mutate/reenter shared state. No allocation or Bag clearing.
    """
    def atualizar(dono):
        _atualizador_core()(mundo,dono,capacidade_tipo=capacidade_tipo,modificador=bonus.consultar)
    return bonus.definir(jogador,tipo,seletor,valor,recalcular_capacidades=atualizar)
