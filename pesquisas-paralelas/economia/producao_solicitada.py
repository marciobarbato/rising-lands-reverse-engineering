"""Actual economic producer through the committed conditional unit request."""
import importlib
from pathlib import Path
import sys

from producao_colocada import calcular_tropa_com_colocacao_no_mundo


def _voz_core():
    pasta = Path(__file__).resolve().parents[2] / 'ferramentas'
    for nome in ('voz_unidades', 'selecao_unidades', 'movimento'):
        atual = sys.modules.get(nome)
        if atual is not None and Path(atual.__file__).resolve() != pasta / (nome + '.py'):
            raise ImportError('Production request requires committed core providers from this checkout')
    sys.path.insert(0, str(pasta))
    try:
        return importlib.import_module('voz_unidades').retomar_solicitacao_saida
    finally:
        sys.path.remove(str(pasta))


def calcular_tropa_com_solicitacao_no_mundo(producao, mundo, bonus, indice, *, janela=None):
    """Run one update through actual placement and bounded original request.

    Prior shared-state/domain contracts apply. Loaded viewport words are
    forwarded only to the core request provider, after placement. Foreign or
    hidden paths may return without them; visible paths require them even for
    an active handle. Pending volume/PostSound dependencies retain prior live
    effects and exact core request data. No backend or handle is fabricated.
    Return None if incomplete, else actual SolicitacaoSaidaTropa at0x420fb7,
    ready for the separate economic cleanup. Never replay a pending/error call.
    """
    pedido = calcular_tropa_com_colocacao_no_mundo(producao, mundo, bonus, indice)
    if pedido is None:
        return None
    return _voz_core()(mundo, pedido, janela=janela)
