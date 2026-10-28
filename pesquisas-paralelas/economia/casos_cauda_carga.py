"""Explicit Stage 16 fixtures: load-tail tables added to Stage 15 worlds.

Every table is an inherited input (synthetic unless stated); nothing is
computed here, so the same cases feed original-only captures and tests.
"""
import random

import casos_habitaveis as base

# Market buffers of MarcheResetAll; names follow mercado/ciclo_mercado.
MERCADO = {'bytes_2e7c': (0x4e2e7c, 4), 'indicadores': (0x4e2930, 8), 'contatos': (0x496f8c, 4),
           'bytes_292c': (0x4e292c, 4), 'bytes_2928': (0x4e2928, 4), 'words_2940': (0x4e2940, 8),
           'words_2938': (0x4e2938, 8)}


def estender(caso, *, semente=0, rede=None, pool_aleatorio=False, padrao_realizaveis=None):
    """Add order Bags, counts, player tables and market buffers to a case."""
    rng = random.Random(f'cauda:{caso.nome}:{semente}')
    m = caso.mundo
    # [0x4e19b8] owner pools, laid out contiguously as in the native bench
    # (legacy fixture form; the original uses four separate allocations).
    caso.ordens = bytearray(rng.randbytes(10816))
    m.realizaveis_estruturas[:] = rng.randbytes(88)         # 0x49a070, core's raw name
    caso.contagens_tipo18 = bytearray(rng.randbytes(4))     # 0x4dfb4c
    caso.jogadores = bytearray(rng.randbytes(80))           # live [0x5080a8]
    m.controle_jogadores[:] = caso.jogadores[1::20]         # core's view of byte +1
    caso.jogadores_guardados = bytearray(rng.randbytes(80))  # source [0x5080ac]
    caso.mercado = {nome: bytearray(rng.randbytes(n)) for nome, (_, n) in MERCADO.items()}
    if rede is not None:
        caso.rede = rede
    if padrao_realizaveis == 'zero':
        caso.estruturas_realizaveis[:] = bytes(88)
    elif padrao_realizaveis == 'um':
        caso.estruturas_realizaveis[:] = bytes([1]*88)
    if pool_aleatorio:
        s = m.estruturas
        for i in range(1000):
            o = i*276
            dono = rng.choice((0, 1, 2, 3, 0, 1, 2, 3, 4, 200, 255))
            s[o+4], s[o+5] = dono, rng.choice((0, 0, 1, 3, 5, 255))
            s[o+8] = rng.randrange(22) if dono < 4 else rng.randrange(256)
    return caso


def casos_monde01():
    for nome, padrao, rede, realizaveis in (('MONDE01 zero tables, network 0', 'zero', 0, 'zero'),
                                            ('MONDE01 one tables, network 0', 'um', 0, 'um'),
                                            ('MONDE01 one tables, network 1', 'um', 1, 'um'),
                                            ('MONDE01 random tables, network 0x80', 'aleatorio', 0x80, None)):
        yield estender(base.caso_monde01(nome, padrao=padrao), rede=rede, padrao_realizaveis=realizaveis)


def caso_pool(nome, *, semente, rede, padrao='aleatorio'):
    caso = base.caso_sintetico(nome, 2, 0, 0x4040, padrao=padrao, semente=semente)
    return estender(caso, semente=semente, rede=rede, pool_aleatorio=True)


def montar_cauda(caso, *, bolsas=None):
    """Compose existing economy classes over the case buffers, by identity.

    ``bolsas``: four separate per-owner unit-order pools (the original's
    [0x4e19b8] shape), used by identity. None uses the legacy contiguous
    fixture ``caso.ordens`` through ``ordens_contiguas``."""
    from mercado import Mercado
    from ciclo_mercado import CicloMercado
    from cauda_carga import CaudaCargaEconomia
    from proprietarios import ordens_contiguas
    h = base.montar_habitacao(caso, ordens=ordens_contiguas(caso.ordens) if bolsas is None else bolsas)
    c = h.construcoes
    c.contagens_por_tipo = caso.mundo.realizaveis_estruturas
    c.contagens_tipo18 = caso.contagens_tipo18
    mercado = Mercado(c.economia)
    mercado.jogadores, mercado.contatos, mercado.indicadores = (caso.jogadores, caso.mercado['contatos'],
                                                                caso.mercado['indicadores'])
    ciclo = CicloMercado(mercado)
    for nome in ('bytes_2e7c', 'bytes_292c', 'bytes_2928', 'words_2940', 'words_2938'):
        setattr(ciclo, nome, caso.mercado[nome])
    caso.rede_bytes = bytearray([caso.rede])
    return h, CaudaCargaEconomia(h, ciclo, rede=caso.rede_bytes, jogadores_guardados=caso.jogadores_guardados)
