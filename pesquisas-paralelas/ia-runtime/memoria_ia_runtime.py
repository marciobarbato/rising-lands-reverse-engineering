"""Flat 32-bit address space over explicit inherited buffers, with declared regions.

Translated routines address memory exactly as the original does (absolute
addresses, pointer arithmetic modulo 2**32, little-endian widths). Every
access they make must fall inside a declared region; anything else raises
``AcessoNaoDeclarado`` naming the address, so an unsupported footprint is never
silently read or written. World providers (other owners' routines) write
through ``escrever_mundo``, which only requires a mapped segment.
"""
import struct

MASCARA = 0xffffffff
_FORMATOS = {1: '<B', 2: '<H', 4: '<I'}


class AcessoNaoDeclarado(LookupError):
    def __init__(self, endereco, largura, motivo):
        self.endereco, self.largura = endereco, largura
        super().__init__(f'{motivo}: 0x{endereco:08x} (width {largura})')


class MemoriaDeclarada:
    def __init__(self, segmentos, regioes):
        """``segmentos``: (base, writable buffer); ``regioes``: (start, end_exclusive, name)."""
        self.segmentos = []
        for base, buffer in segmentos:
            view = memoryview(buffer)
            if view.readonly or view.ndim != 1 or view.format != 'B':
                raise ValueError(f'Segment at 0x{base:08x} must be a writable byte buffer')
            self.segmentos.append((base, base + len(view), view))
        self.regioes = tuple(regioes)

    def _local(self, endereco, largura, declarado=True):
        endereco &= MASCARA
        if declarado and not any(a <= endereco and endereco + largura <= b for a, b, _ in self.regioes):
            raise AcessoNaoDeclarado(endereco, largura, 'Access outside the declared AI regions')
        for base, fim, view in self.segmentos:
            if base <= endereco and endereco + largura <= fim:
                return view, endereco - base
        raise AcessoNaoDeclarado(endereco, largura, 'Address outside every inherited buffer')

    def _acesso(self, largura, endereco, valor):
        view, offset = self._local(endereco, largura)
        if valor is None:
            return struct.unpack_from(_FORMATOS[largura], view, offset)[0]
        struct.pack_into(_FORMATOS[largura], view, offset, valor & ((1 << (8 * largura)) - 1))
        return valor & ((1 << (8 * largura)) - 1)

    def u8(self, endereco, valor=None):
        return self._acesso(1, endereco, valor)

    def u16(self, endereco, valor=None):
        return self._acesso(2, endereco, valor)

    def u32(self, endereco, valor=None):
        return self._acesso(4, endereco, valor)

    def s8(self, endereco):
        valor = self.u8(endereco)
        return valor - 0x100 if valor & 0x80 else valor

    def escrever_mundo(self, endereco, dados):
        """Effect of another owner's routine (mapped segment required, no region check)."""
        view, offset = self._local(endereco, len(dados), declarado=False)
        view[offset:offset + len(dados)] = bytes(dados)

    def ler_mundo(self, endereco, largura):
        view, offset = self._local(endereco, largura, declarado=False)
        return bytes(view[offset:offset + largura])


def u32(valor):
    return valor & MASCARA


def s32(valor):
    valor &= MASCARA
    return valor - 0x100000000 if valor & 0x80000000 else valor
