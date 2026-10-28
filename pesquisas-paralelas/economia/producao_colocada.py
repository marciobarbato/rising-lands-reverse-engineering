"""Actual production update through committed physical exit and movement order."""
import importlib
from pathlib import Path
import sys

from producao_experiente import calcular_tropa_com_experiencia_no_mundo


def _colocacao_core():
    pasta=Path(__file__).resolve().parents[2]/'ferramentas'
    atual=sys.modules.get('colocacao_saida')
    if atual is not None and Path(atual.__file__).resolve()!=pasta/'colocacao_saida.py':
        raise ImportError('Production placement requires committed core provider from this checkout')
    sys.path.insert(0,str(pasta))
    try:
        return importlib.import_module('colocacao_saida').retomar_colocacao_saida
    finally:
        sys.path.remove(str(pasta))


def calcular_tropa_com_colocacao_no_mundo(producao,mundo,bonus,indice):
    """One actual update through experience, physical exit and movement order.

    Require the two original terrain-pointer aliases before progress, alongside
    prior unit/structure identity guards. No buffer is copied or reconnected.
    Core owns all placement, discovery/light/minimap and movement algorithms.
    Returns None if incomplete, else ColocacaoSaidaTropa at0x420f9e BEFORE the
    conditional owner/EnginAsk fragment. Failures retain preceding economic,
    conversion, recovery, queue and partial physical effects. Never replay.
    """
    terreno=producao.recrutamento.mundo.terreno
    if (terreno.tipos is not getattr(mundo,'objetos',None)
            or terreno.quantidades is not getattr(mundo,'donos_objetos',None)):
        raise ValueError('Production placement requires identical raw terrain/object buffers for507d74/507dac')
    pedido=calcular_tropa_com_experiencia_no_mundo(producao,mundo,bonus,indice)
    if pedido is None:
        return None
    return _colocacao_core()(mundo,pedido)
