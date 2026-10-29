"""Economy providers for ai-runtime's MONDE01 frame composition (M2.1).

``provedores_economia_quadro(memoria, *, bonus, producao, recursos=None, calcular_tropa=None)``
returns ``{original name: provider}`` in ai-runtime's convention
``provider(sitio=..., **keywords) -> EAX`` (None when the caller does not
consume EAX), like Core's ``provedores_core(memoria, bonus)``. Every routine
covered by the 102 isolated native calls of frames 0/1
(``evidencias/captura-quadro1-economia-original-v2.json``) is here, plus
RechercheGetNbInvention for Missions' TestFinDeMission. Round 4 adds the
queries the display-scenario frames reach outside those calls
(``evidencias/captura-consultas-economia-exibicao.json``): PlayerGetType,
PlayerEstAllie, TestRessource, BatimentGetType, BatimentEstHabiter,
IntToBCD, BCDToInt and BagVide. PlayerEstAllie and TestRessource are the live
functions (original index handling, player 4 included), never the 0..3-protected
class forms. ``recursos`` should be live (round 5):
``extracao.RecursosTerreno.do_mundo(mundo, minas=m.vista(0x509954, 80))`` over
Core's ``MundoFisico.vincular_grades`` world, or
``RecursosTerreno.da_memoria(m, mosaicos=mundo.tiles.buffer)``.

``memoria`` is the declared live memory: either an object with
``ler(endereco, tamanho)`` and ``vista(endereco, tamanho)`` (Missions'
``MapaMemoriaM1``), or one with ``u8/u16/u32(endereco, valor=None)``
(ai-runtime's ``MemoriaDeclarada``, Core's ``MemoriaQuadro``), adapted
byte by byte with no copy. ``bonus`` must be ``BonusUnidades.vivo``/
``da_memoria`` (the live 0x4dfba0/0x4965ae ranges). ``producao`` is the
economy ``Producao`` whose structure pool and unit pool are the live
buffers (the M1 composition binds them, Bag pools included, by identity).
``recursos`` is ``extracao.RecursosTerreno`` with its grids bound live; it is
needed for UpdateChamp only. ``calcular_tropa(indice)`` is the world-joined
CalculTroupe (``producao_limpa.calcular_tropa_com_limpeza_no_mundo``); when
omitted, CalculTroupe runs the economy-only update and raises
``DependenciaQuadro`` before any store for an ACTIVE structure, the case
MONDE01 frames 0/1 do not reach.

``REGIOES_ECONOMIA_QUADRO`` lists the fixed address ranges these providers
may touch, for a region-checked memory; the unit pool ``[0x4e19a0]`` is the
only dynamic range.
"""
import struct

import quadro_economia as q

REGIOES_ECONOMIA_QUADRO = (
    (0x494cbb, 0x494cc3, 'research constant f64'), (0x495d8c, 0x495d8c + 22 * 52, 'structure type table'),
    (0x4965ae, 0x4965ae + 1300, 'runtime unit types'), (0x496f8c, 0x496f90, 'market partners'),
    (0x4973e8, 0x4973ec, 'field row and period'), (0x496fe4, 0x496fe5, 'mission number'),
    (0x497164, 0x497168, 'RNG'), (0x49a0c8, 0x49a0c8 + 276000, 'structures'),
    (0x4dfba0, 0x4dfba0 + 1872, 'unit bonus table'), (0x4e05a2, 0x4e05a3, 'resource redraw flag'),
    (0x4e2928, 0x4e292c, 'market contact'), (0x4e296c, 0x4e296c + 80, 'hangar table'),
    (0x4e2e7c, 0x4e2e7c + 256, 'market state (indexed by partner byte, up to 0xff)'),
    (0x4e2ea8, 0x4e2ea8 + 128, 'resources'), (0x508041, 0x508042, 'local player'),
    (0x508044, 0x508044 + 80, 'attack flags'), (0x5080b0, 0x5080b0 + 64, 'alliance counters'),
    (0x5080f4, 0x5080f4 + 64, 'research players'), (0x508174, 0x50817c, 'scientists'),
    (0x50817c, 0x50817c + 4 * 0x168, 'research table'), (0x50871c, 0x50871c + 256, 'invention counts (AL index)'),
    (0x508f7c, 0x508f80, 'frame counter'), (0x509952, 0x509953, 'field update flag'),
    (0x509954, 0x509954 + 80, 'mines'), (0x51a990, 0x51a990 + 64, 'AI contexts (+0 inactive byte)'),
    (0x4e19a0, 0x4e19a4, 'unit pool pointer'), (0x5080a8, 0x5080ac, 'player records pointer'),
)
# Dynamic ranges besides the unit pool: the player records [0x5080a8] (PlayerGetType/PlayerEstAllie),
# any Bag count word BagVide is given, and the IntToBCD/BCDToInt destinations and sources.
BOLSAS_ESTRUTURAS = 0x49a0c8 + 0x0c


class _MemoriaPalavras:
    """``ler``/``vista`` over a ``u8``-addressable memory; writes go straight through ``u8``."""
    def __init__(self, memoria):
        self.memoria = memoria

    def ler(self, endereco, tamanho):
        return bytes(self.memoria.u8(endereco + i) for i in range(tamanho))

    def vista(self, endereco, tamanho):
        return _Escrita(self.memoria, endereco, tamanho)


class _Escrita:
    def __init__(self, memoria, endereco, tamanho):
        self.memoria, self.endereco, self.tamanho = memoria, endereco, tamanho

    def __setitem__(self, indice, valor):
        if isinstance(indice, int):
            self.memoria.u8(self.endereco + indice, valor)
            return
        if indice != slice(None) or len(valor) != self.tamanho:
            raise TypeError('Only [i] = byte and [:] = bytes of the full width are written')
        for i, b in enumerate(bytes(valor)):
            self.memoria.u8(self.endereco + i, b)


def memoria_economia(memoria):
    """The ``ler``/``vista`` interface quadro_economia uses, over either declared memory form."""
    if hasattr(memoria, 'ler') and hasattr(memoria, 'vista'):
        return memoria
    if hasattr(memoria, 'u8'):
        return _MemoriaPalavras(memoria)
    raise TypeError('Declared memory needs ler/vista or u8/u16/u32')


def provedores_economia_quadro(memoria, *, bonus, producao, recursos=None, calcular_tropa=None):
    from bonus_unidades import BonusUnidades
    from construcoes_habitaveis import celula_central_estrutura, estrutura_habitada
    from extracao import RecursosTerreno
    from limpeza_saida import bag_contient_troupe
    m = memoria_economia(memoria)
    if not isinstance(bonus, BonusUnidades) or not isinstance(bonus.memoria, (bytearray, memoryview)):
        raise TypeError('bonus must be BonusUnidades.vivo/da_memoria over the live table')
    estruturas = producao.recrutamento.mundo.estruturas

    def tropa(indice):
        indice &= 0xffff
        if calcular_tropa is not None:
            return calcular_tropa(indice)
        o = indice * 276
        if struct.unpack_from('<I', estruturas, o + 0x8c)[0] and estruturas[o + 0x74]:
            raise q.DependenciaQuadro('CalculTroupe', 0x4259e6, 'active structure needs the world-joined producer',
                                      dict(EAX=indice))
        return producao.calcular_tropa(indice)

    def bolsa_para_estrutura(bolsa):
        indice, resto = divmod((bolsa & 0xffffffff) - BOLSAS_ESTRUTURAS, 276)
        if resto or not 0 <= indice < 1000:
            raise q.DependenciaQuadro('BagContientTroupe', 0x44724a, 'Bag outside the structure pool',
                                      dict(EAX=bolsa & 0xffffffff))
        return indice

    # SetUpdateChamp touches only scalars; a fresh provider object holds them between pull and push.
    agenda = recursos if recursos is not None else RecursosTerreno()
    p = {
        'RechercheCalcul': lambda sitio: q.calcular_pesquisa(m),
        'PlayerInitAllianceCompteur': lambda sitio: q.contar_aliancas(m),
        'SetUpdateChamp': lambda sitio: q.agendar_campos(m, agenda),
        'CalculMatiere': lambda sitio: q.calcular_materia(m),
        'CalculCompteurMarche': lambda sitio, jogador: q.calcular_contador_mercado(m, jogador),
        'CalculCompteurProposition': lambda sitio, jogador, edx=0: q.calcular_contador_proposicao(m, jogador, edx),
        'PlayerAttaqueCalculSympa': lambda sitio: q.calcular_simpatia_ataques(m),
        'MAJSympathie': lambda sitio, jogador, outro, evento: q.atualizar_simpatia(m, jogador, outro, evento),
        'ResetTableauHangar': lambda sitio: q.resetar_tabela_hangar(m),
        'BatimentNextEtape:tipo1_2_13_16': lambda sitio, estrutura: q.ramo_producao_estrutura(producao, estrutura,
                                                                                               tropa),
        'BagContientTroupe': lambda sitio, bolsa: int(bag_contient_troupe(producao.recrutamento,
                                                                          bolsa_para_estrutura(bolsa))),
        'CalculTroupe': lambda sitio, estrutura: tropa(estrutura),
        'BatimentGetCase': lambda sitio, estrutura: celula_central_estrutura(estruturas, estrutura),
        'BonusGetValEngin': lambda sitio, jogador, tipo, seletor, ecx: bonus.consultar(jogador, tipo, seletor, ecx=ecx),
        'EnginNextEtape:estado7': lambda sitio, unidade: q.estado_parado_unidade(m, unidade),
        'RechercheGetNbInvention': lambda sitio, jogador: q.numero_invencoes(m, jogador),
        'PlayerGetType': lambda sitio, jogador: q.tipo_jogador(m, jogador),
        'PlayerEstAllie': lambda sitio, jogador, outro: q.aliado(m, jogador, outro),
        'TestRessource': lambda sitio, jogador, comida, pedra, pecas: q.recursos_suficientes(m, jogador, comida,
                                                                                             pedra, pecas),
        'BatimentGetType': lambda sitio, estrutura: q.tipo_estrutura_viva(m, estrutura),
        'BatimentEstHabiter': lambda sitio, estrutura: estrutura_habitada(producao, estrutura),
        'IntToBCD': lambda sitio, destino, valor: q.escrever_bcd(m, destino, valor),
        'BCDToInt': lambda sitio, destino, origem: q.ler_bcd(m, destino, origem),
        'BagVide': lambda sitio, bolsa: q.bolsa_vazia(m, bolsa),
    }
    if recursos is not None:
        p['UpdateChamp'] = lambda sitio: q.atualizar_campos(m, recursos)
    return p
