"""Join the actual production update to committed live core continuations."""
import importlib
from pathlib import Path
import struct
import sys

from bonus_unidades import capacidade_tipo
from saida_tropa import SaidaTropa


def _continuacoes_core():
    pasta = Path(__file__).resolve().parents[2] / 'ferramentas'
    nomes = ('conversao_unidades', 'posicao_saida', 'recuperacao_unidades', 'unidades')
    for nome in nomes:
        modulo = sys.modules.get(nome)
        if modulo is not None and Path(modulo.__file__).resolve() != pasta / (nome + '.py'):
            raise ImportError('Production requires committed core providers from this checkout')
    sys.path.insert(0, str(pasta))
    try:
        # The conversion provider imports position lazily when invoked, after
        # this scoped path is removed. Resolve that committed dependency now.
        importlib.import_module('posicao_saida')
        conversao = importlib.import_module('conversao_unidades').retomar_conversao_saida
        recuperacao = importlib.import_module('recuperacao_unidades').retomar_recuperacao_saida
        return conversao, recuperacao
    finally:
        sys.path.remove(str(pasta))


def calcular_tropa_no_mundo(producao, mundo, bonus, indice):
    """Run one real update through preparation, conversion, healing and fatigue.

    The economy/core unit and structure buffers must be the SAME objects;
    mismatches fail before progress. Existing input widths/domains otherwise
    apply at their original stage boundaries. Core imports occur only after
    successful economic preparation. Read-only loaded bonus queries are used
    directly, and position reads runtime dimensions from the production table.

    Return None when inactive/below threshold; otherwise return core's frozen
    RecuperacaoSaidaTropa at 0x420f81 before experience. Later errors preserve
    earlier progress, removals, credits, conversion/search effects and healing.
    This is one-shot: do not run another tick/replay after pending output or
    failure. It performs no experience, placement, cleanup or completion event.
    """
    r = producao.recrutamento
    if r.unidades is not mundo.unidades or r.mundo.estruturas is not mundo.estruturas:
        raise ValueError('Production requires identical live economy/core unit and structure buffers')

    def saida(i, direcao):
        pedido = SaidaTropa(r).preparar(i, direcao)
        if pedido is None:
            return None
        converter, recuperar = _continuacoes_core()
        tipo = mundo.estruturas[pedido.indice * 276 + 8]
        dimensoes = struct.unpack_from('<HH', producao.tipos_construcoes, tipo * 52)
        convertido = converter(mundo, pedido, r.tipos_unidades,
                               capacidade_tipo=capacidade_tipo, modificador=bonus.consultar,
                               dimensoes=dimensoes)
        return recuperar(mundo, convertido, r.tipos_unidades)

    return producao.calcular_tropa(indice, saida_tropa=saida)
