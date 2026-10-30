"""The original count phase, composed with an explicit live per-unit body.

Counts are rebuilt before each unit's body, using the established AI loop.
Death never decrements them directly. A victim already visited this phase can
therefore remain counted until the following phase, exactly as in the game.
"""
from abi_luta_fatal_combate import registradores_exigidos
from laco_despachantes import calcular_proxima_etapa_unidades


def recontar_luta(memoria, etapa):
    def player_type(sitio,jogador):
        return memoria.u8(memoria.u32(0x5080a8)+20*jogador+1) if jogador<4 else 2
    return calcular_proxima_etapa_unidades(memoria,{
        'EnginNextEtape':lambda sitio,unidade:etapa(unidade),
        'PlayerGetType':player_type})


def recontar_registradores(memoria, etapa, regs, *, chamada=0x456db5):
    out=registradores_exigidos('CalculEnginNextEtape',chamada,regs)
    recontar_luta(memoria,etapa)
    out['EAX']=800
    return out
