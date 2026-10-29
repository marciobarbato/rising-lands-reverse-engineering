"""Original unit capacity/bonus queries and selective table producers.

State is the already-loaded bonus table; constructing zeros is a synthetic
fixture, not BonusReset/INI/mission loading. No ownership, allocation or unit
conversion effects are performed by these queries.
"""
import struct

from economia import _buffer_vivo, _i32

BASE_BONUS_UNIDADES = 0x4dfba0
TAMANHO_BONUS_UNIDADES = 4 * 26 * 18
BASE_TIPOS_UNIDADES = 0x4965ae
TAMANHO_TIPOS_UNIDADES = 26 * 50

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


class CapacidadeUnidadesPendente(RuntimeError):
    """Bonus writes are committed; original next call is EnginResetCapacite."""
    endereco = 0x4475ef

    def __init__(self, jogador):
        self.jogador = jogador
        super().__init__(f'Unit capacity refresh pending for player {jogador}')


# Original TypeEnginEstArmee 0x44230c, used only for selected BL=30 loops.
_TIPOS_ARMEE = frozenset((0, 1, 2, 3, 8, 11, 12, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25))
_CAMPOS_RESET = ((0, 2), (2, 1), (4, 2), (12, 1), (6, 1),
                 (11, 1), (8, 2), (10, 1), (13, 1), (14, 1))
_CAMPOS_SET = {0:(0,2), 1:(11,1), 2:(2,1), 3:(4,2), 4:(6,1),
               5:(8,2), 6:(10,1), 7:(11,1), 8:(13,1), 9:(14,1),
               10:(17,1), 11:(15,1), 12:(16,1)}


def _dividir_assinado(n, d):
    if not d:
        raise ZeroDivisionError('BonusSetEngin signed integer division by zero')
    return -(abs(n) // d) if n < 0 else n // d


class BonusUnidades:
    """Unit bonus table 0x4dfba0 (1,872 bytes) and runtime unit types 0x4965ae (1,300 bytes).

    ``BonusUnidades.vivo``/``da_memoria`` bind the live original ranges by
    identity: every query reads and every setter writes the caller's buffers.
    The constructor COPIES its arguments; it is the legacy/fixture form only.
    """
    @classmethod
    def vivo(cls, memoria, *, tipos_unidades):
        """Bind the live table and runtime types by identity (no copy).

        Both are writable ``bytearray``s or writable 1-D contiguous byte
        ``memoryview``s of exactly 1,872 and 1,300 bytes. Rejection happens
        before any binding; ``self.memoria``/``self.tipos_unidades`` are the
        given objects.
        """
        memoria = _buffer_vivo(memoria, TAMANHO_BONUS_UNIDADES, 'Live unit bonus table (0x4dfba0)')
        tipos_unidades = _buffer_vivo(tipos_unidades, TAMANHO_TIPOS_UNIDADES, 'Live runtime unit types (0x4965ae)')
        if memoria is tipos_unidades:
            raise ValueError('The bonus table and the runtime unit types are different original ranges')
        self = cls.__new__(cls)
        self.memoria, self.tipos_unidades = memoria, tipos_unidades
        return self

    @classmethod
    def da_memoria(cls, m):
        """``vivo`` over a live memory map: ``m.vista(0x4dfba0, 1872)`` and ``m.vista(0x4965ae, 1300)``."""
        return cls.vivo(m.vista(BASE_BONUS_UNIDADES, TAMANHO_BONUS_UNIDADES),
                        tipos_unidades=m.vista(BASE_TIPOS_UNIDADES, TAMANHO_TIPOS_UNIDADES))

    def __init__(self, memoria=None, *, tipos_unidades=None):
        # Legacy/fixture form: copies. Use BonusUnidades.vivo for the live original table.
        self.memoria = bytearray(TAMANHO_BONUS_UNIDADES if memoria is None else memoria)
        if len(self.memoria) != TAMANHO_BONUS_UNIDADES:
            raise ValueError('Unit bonus table must contain four x 26 x 18 bytes')
        self.tipos_unidades = bytearray(1300 if tipos_unidades is None else tipos_unidades)
        if len(self.tipos_unidades) != 1300:
            raise ValueError('Runtime unit types must contain 26 x 50 bytes')

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


    def reiniciar(self):
        """Complete BonusReset 0x428e71; selective writes in original order.

        Preserves record offsets 3, 7, 15, 16, 17. No unit refresh occurs.
        """
        for jogador in range(4):
            for tipo in range(26):
                base = jogador * 468 + tipo * 18
                for offset, largura in _CAMPOS_RESET:
                    if largura == 1:
                        self.memoria[base + offset] = 0
                    else:
                        struct.pack_into('<H', self.memoria, base + offset, 0)

    def definir(self, jogador, tipo, seletor, valor, *, recalcular_capacidades=None):
        """BonusSetEngin: AL owner, BL type, DL selector, CX value.

        Selector >12 is a no-op before protected owner/type validation. Active
        branches protect owners 0..3; normal type 0..25. BL=30 selects all types
        only for IDs 0/1/3/4/5/6, with original per-selector filtering.
        Selector 1 calls recalcular_capacidades(owner) AFTER table writes, or
        raises CapacidadeUnidadesPendente there. Caller failures retain writes.
        """
        jogador, tipo, seletor, valor = jogador & 255, tipo & 255, seletor & 255, valor & 65535
        if seletor > 12:
            return
        if jogador >= 4:
            raise ValueError('Protected bonus setter requires player 0..3')
        if tipo == 30 and seletor in (0, 1, 3, 4, 5, 6):
            tipos = (12, 13, 15) if seletor == 1 else range(26)
            if seletor in (3, 4, 5):
                tipos = (t for t in tipos if t in _TIPOS_ARMEE)
        elif tipo < 26:
            tipos = (tipo,)
        else:
            raise ValueError('Unit type outside this selector protected domain')
        offset, largura = _CAMPOS_SET[seletor]
        for alvo in tipos:
            resultado = valor
            if seletor == 0:
                base = struct.unpack_from('<H', self.tipos_unidades, alvo * 50 + 46)[0]
                resultado = _dividir_assinado(_i32(base * valor), 10)
            elif seletor == 3:
                base = struct.unpack_from('<H', self.tipos_unidades, alvo * 50 + 48)[0]
                resultado = base - _dividir_assinado(base * 10, valor)
            elif seletor == 12:
                resultado = valor - 10
            pos = jogador * 468 + alvo * 18 + offset
            if largura == 1:
                self.memoria[pos] = resultado & 255
            else:
                struct.pack_into('<H', self.memoria, pos, resultado & 65535)
        if seletor == 1:
            if recalcular_capacidades is None:
                raise CapacidadeUnidadesPendente(jogador)
            recalcular_capacidades(jogador)
