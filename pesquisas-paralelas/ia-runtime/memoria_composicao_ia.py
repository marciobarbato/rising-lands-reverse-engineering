"""Flat original-address access over Missions' ``MapaMemoriaM1`` for the frame composition.

Most segments of the map are provider byte buffers. A few are canonical Python
lists that Core keeps as u16 grids (tiles ``[0x507d70]``, regions ``[0x4e0f38]``,
the structure-colour stack ``0x4e0732``). Core's ``chamadas_quadro_core`` and this
front's routines address memory as u8/u16/u32. This facade serves those widths on
both kinds of segment: a list element is read and written in place, so a
byte-width access touches the element it belongs to. ``vista``/``ler`` (used by
Economy) are the map's own and stay byte-segment only. Nothing is copied or
defaulted; an address outside the map raises the map's error.
"""
import struct

_FORMATOS = {1: '<B', 2: '<H', 4: '<I'}


class MemoriaMapaM1:
    def __init__(self, mapa):
        self.mapa = mapa

    def vista(self, endereco, tamanho):
        return self.mapa.vista(endereco, tamanho)

    def ler(self, endereco, tamanho):
        return self.mapa.ler(endereco, tamanho)

    def _acesso(self, largura, endereco, valor):
        endereco &= 0xffffffff
        s = self.mapa._segmento(endereco, largura)
        if s.tipo == 'bytes':
            o = endereco - s.base
            if valor is None:
                return struct.unpack_from(_FORMATOS[largura], s.vista, o)[0]
            valor &= (1 << 8 * largura) - 1
            struct.pack_into(_FORMATOS[largura], s.vista, o, valor)
            return valor
        if s.formato != 'H':
            raise ValueError(f'{s.dono}: list format {s.formato} is not served')
        o = endereco - s.base
        primeiro, ultimo = o // 2, (o + largura - 1) // 2
        dados = bytearray(b''.join(struct.pack('<H', s.lista[i]) for i in range(primeiro, ultimo + 1)))
        d = o - 2 * primeiro
        if valor is None:
            return struct.unpack_from(_FORMATOS[largura], dados, d)[0]
        valor &= (1 << 8 * largura) - 1
        struct.pack_into(_FORMATOS[largura], dados, d, valor)
        for k, i in enumerate(range(primeiro, ultimo + 1)):
            s.lista[i] = struct.unpack_from('<H', dados, 2 * k)[0]
        return valor

    def u8(self, endereco, valor=None):
        return self._acesso(1, endereco, valor)

    def u16(self, endereco, valor=None):
        return self._acesso(2, endereco, valor)

    def u32(self, endereco, valor=None):
        return self._acesso(4, endereco, valor)

    def s8(self, endereco):
        v = self.u8(endereco)
        return v - 0x100 if v & 0x80 else v
