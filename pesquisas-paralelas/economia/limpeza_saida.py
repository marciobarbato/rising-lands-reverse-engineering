"""Isolated production cleanup prefix, before terrain and AI dependencies."""
from dataclasses import dataclass
import importlib
from pathlib import Path
import sys

from recrutamento import _word

# Exact negative cases in original BagVide's inlined type classification.
# All other u8 types, including unknown 26..255, satisfy this predicate.
_TIPOS_EXCLUIDOS_BAG_VIDE=frozenset((3,11,12,13,14,15,16,17,25))


def bag_vide(recrutamento, indice):
    """Complete 0x44724a: capacity scan, tag1, first accepted unit type.

    Despite its symbol this is not a count==0 test. Only read references are
    protected (0..799); a successful early return never reads later slots.
    Capacity must be 0..30. No mutation, activity, owner or count check occurs.
    """
    r=recrutamento
    o=r._offset(indice)
    s=r.mundo.estruturas
    capacidade=_word(s,o+0xe)
    if capacidade>30:
        raise ValueError('BagVide protected capacity is 0..30')
    for slot in range(capacidade):
        if s[o+0x4e+slot]!=1:
            continue
        unidade=_word(s,o+0x12+slot*2)
        if unidade>=800:
            raise ValueError('BagVide protected unit reference is 0..799')
        if r.unidades[unidade*276+1] not in _TIPOS_EXCLUIDOS_BAG_VIDE:
            return True
    return False


def _resetter_core():
    pasta=Path(__file__).resolve().parents[2]/'ferramentas'
    atual=sys.modules.get('ciclo_estruturas')
    if atual is not None and Path(atual.__file__).resolve()!=pasta/'ciclo_estruturas.py':
        raise ImportError('Production cleanup requires committed core reset from this checkout')
    sys.path.insert(0,str(pasta))
    try:
        return importlib.import_module('ciclo_estruturas').resetar_estrutura
    finally:
        sys.path.remove(str(pasta))


@dataclass(frozen=True)
class LimpezaSaidaTropa:
    indice:int
    unidade:int
    endereco_dependencia:int
    funcao_dependencia:int
    parametro:int


def retomar_limpeza_saida(producao,mundo,pedido):
    """Consume only a real 0x420fb7 handoff; missing preceding calls stay open.

    Protected indices truncate u16, buildings0..999, output units0..799 and
    production types1/2/13/16. Economy/core buffers must be identical. These
    guards precede mutation. Retention predicates use original capacity scans.
    True retention resets through actual core then stops before unit message70;
    false resets types1/2 only then stops before terrain query (10/8 parameter).
    Imports/errors retain earlier effects; no terrain/AI call is substituted.
    No complete cleanup, preceding unit calls, allocation or mission is claimed.
    """
    if pedido.endereco_dependencia!=0x420fb7:
        raise ValueError('Expected completed unit-caller handoff at 0x420fb7')
    r=producao.recrutamento
    if r.unidades is not mundo.unidades or r.mundo.estruturas is not mundo.estruturas:
        raise ValueError('Cleanup requires identical live unit and structure buffers')
    indice,unidade=pedido.indice&65535,pedido.unidade&65535
    o=r._offset(indice)
    tipo=mundo.estruturas[o+8]
    if unidade>=800 or tipo not in (1,2,13,16):
        raise ValueError('Cleanup requires unit0..799 and production building type1/2/13/16')
    reter=bag_vide(r,indice) if tipo==2 else False
    if not reter:
        reter=bool(producao.contar_unidades(indice,9))
    if reter:
        _resetter_core()(mundo.estruturas,indice)
        return LimpezaSaidaTropa(indice,unidade,0x4211d3,0x4829c8,70)
    if tipo in (1,2):
        _resetter_core()(mundo.estruturas,indice)
    return LimpezaSaidaTropa(indice,unidade,0x42110c,0x41aee2,10 if tipo==2 else 8)
