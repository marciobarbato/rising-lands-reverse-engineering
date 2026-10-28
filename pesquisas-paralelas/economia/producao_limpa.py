"""Actual economic producer through the bounded economic cleanup prefix."""
from producao_solicitada import calcular_tropa_com_solicitacao_no_mundo
from limpeza_saida import retomar_limpeza_saida


def calcular_tropa_com_limpeza_no_mundo(producao, mundo, bonus, indice, *, janela=None):
    """Advance once, then consume only the genuine supported420fb7 handoff.

    All loaded-state, shared-buffer and one-shot producer contracts apply.
    Return None before completion; otherwise return LimpezaSaidaTropa before
    the first terrain query or unit AI message. Core reset is reused by the
    existing cleanup provider only where the original reaches it. Errors and
    unresolved viewport/PostSound imports preserve prior effects. This is not
    complete cleanup; never replay a pending or failed update.
    """
    pedido = calcular_tropa_com_solicitacao_no_mundo(producao, mundo, bonus, indice, janela=janela)
    if pedido is None:
        return None
    return retomar_limpeza_saida(producao, mundo, pedido)
