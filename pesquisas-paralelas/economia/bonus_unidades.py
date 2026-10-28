"""Original read-only unit capacity and BonusGetValEngin query providers.

State is the already-loaded bonus table; constructing zeros is a synthetic
fixture, not BonusReset/INI/mission loading. No ownership, allocation or unit
conversion effects are performed by these queries.
"""
import struct

BASE_BONUS_UNIDADES = 0x4dfba0
TAMANHO_BONUS_UNIDADES = 4 * 26 * 18

# Original selector dispatch 0x428c8c: (record offset, load width).
# None is a direct return of the caller's incoming ECX, not a table read.
CAMPOS_BONUS = ((0, 2), (11, 1), (2, 1), (4, 2), (6, 1), (8, 2),
                (10, 1), (12, 1), None, (14, 1), (17, 1), (15, 1), (16, 1))
CAPACIDADES_TIPOS = (0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 2,
                    5, 1, 3, 1, 6, 0, 0, 0, 0, 0, 0, 0, 0)


def capacidade_tipo(tipo):
    """EnginTypeGetCapacite 0x4475ac: low AL; all 256 byte values supported."""
    tipo &= 255
    return CAPACIDADES_TIPOS[tipo] if tipo < 26 else 0


class BonusUnidades:
    def __init__(self, memoria=None):
        self.memoria = bytearray(TAMANHO_BONUS_UNIDADES if memoria is None else memoria)
        if len(self.memoria) != TAMANHO_BONUS_UNIDADES:
            raise ValueError('Unit bonus table must contain four x 26 x 18 bytes')

    def consultar(self, jogador, tipo, seletor, *, ecx=0):
        """BonusGetValEngin 0x428cc0: AL=owner, BL=type, DL=selector.

        Owners 4/200 return 0 before dispatch or validation. Selector 8 or
        selector >12 returns incoming ECX as u32 before any table lookup.
        Otherwise protected owner/type ranges are 0..3/0..25 and unsigned
        fields return u8/u16. The original does not protect table indices.
        Default ecx=0 is an explicit caller input, not an original default.
        For conversion, selectors 1/12 return bytes +0x0b/+0x10.
        """
        jogador, tipo, seletor = jogador & 255, tipo & 255, seletor & 255
        if jogador in (4, 200):
            return 0
        if seletor > 12 or CAMPOS_BONUS[seletor] is None:
            return ecx & 0xffffffff
        if jogador >= 4 or tipo >= 26:
            raise ValueError('Protected unit bonus lookup requires owner 0..3 and type 0..25')
        offset, largura = CAMPOS_BONUS[seletor]
        pos = jogador * 468 + tipo * 18 + offset
        return self.memoria[pos] if largura == 1 else struct.unpack_from('<H', self.memoria, pos)[0]
