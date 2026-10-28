"""Actual production update through committed recruitment experience queue."""
import importlib
from pathlib import Path
import sys

from producao_compartilhada import calcular_tropa_no_mundo


def _experiencia_core():
    pasta=Path(__file__).resolve().parents[2]/'ferramentas'
    atual=sys.modules.get('experiencia_unidades')
    if atual is not None and Path(atual.__file__).resolve()!=pasta/'experiencia_unidades.py':
        raise ImportError('Production experience requires committed core provider from this checkout')
    sys.path.insert(0,str(pasta))
    try:
        return importlib.import_module('experiencia_unidades').retomar_experiencia_saida
    finally:
        sys.path.remove(str(pasta))


def calcular_tropa_com_experiencia_no_mundo(producao,mundo,bonus,indice):
    """Run one update through recovery, then consume the loaded raw queue.

    All Stage8 shared-buffer/domains/partial-effect contracts apply. Core's
    40-byte writable experience queue must be supplied as live inherited state;
    synthetic constructor zeros are not a mission-load default. Queue/import
    failures occur after recovery and retain preceding effects. No replay or
    extra progress update is performed. Returns None before completion, else
    actual ExperienciaSaidaTropa at0x420f8a before physical placement.
    """
    pedido=calcular_tropa_no_mundo(producao,mundo,bonus,indice)
    if pedido is None:
        return None
    return _experiencia_core()(mundo,pedido,producao.recrutamento.tipos_unidades)
