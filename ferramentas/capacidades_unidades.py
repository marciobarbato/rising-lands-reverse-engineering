"""Original EnginResetCapacite scan, retaining Bag contents and partial stores."""
import struct


def atualizar_capacidades_unidades(mundo, jogador, *, capacidade_tipo=None, modificador=None):
    """0x4475ef: scan 800 existing units; write only u16 Bag capacity +0x0c.

    AL owner truncates to u8. States 0/4 are skipped, then owner is tested.
    For each matching record query capacity(type), then bonus(owner,type,1),
    and store the sum's low word. Queries must be read-only. A missing/raising
    query leaves earlier records updated and this/later records untouched.
    No count clamp, inventory removal, navigation or allocation occurs.
    """
    jogador &= 255
    if not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800:
        raise ValueError('EnginResetCapacite requires a writable 800-record unit pool')
    for indice in range(800):
        p = indice * 276
        if mundo.unidades[p+2] in (0, 4) or mundo.unidades[p] != jogador:
            continue
        tipo = mundo.unidades[p+1]
        if capacidade_tipo is None:
            raise NotImplementedError('EnginTypeGetCapacite provider required')
        capacidade = capacidade_tipo(tipo) & 65535
        if modificador is None:
            raise NotImplementedError('BonusGetValEngin selector 1 provider required')
        bonus = modificador(jogador, tipo, 1) & 255
        struct.pack_into('<H', mundo.unidades, p+0xc, (capacidade + bonus) & 65535)
