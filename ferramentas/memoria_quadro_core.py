"""Flat 32-bit address space over the live original buffers, for Core frame callees.

The interface (``u8/u16/u32(endereco, valor=None)``) is the one ai-runtime's
``MemoriaDeclarada`` exposes, so either can be handed to the Core providers in
``chamadas_quadro_core``. Each segment is the caller's own writable buffer
(DGROUP+.bss, an allocation, the CRT thread page...), never a copy; an access
outside every segment raises ``AcessoForaDosSegmentos`` naming the address
instead of reading or writing invented bytes.
"""
from bisect import bisect_right
import struct

MASCARA = 0xffffffff
_FORMATOS = {1: '<B', 2: '<H', 4: '<I'}


class AcessoForaDosSegmentos(LookupError):
    def __init__(self, endereco, largura):
        self.endereco, self.largura = endereco, largura
        super().__init__(f'Access outside every live segment: 0x{endereco:08x} (width {largura})')


class MemoriaQuadro:
    def __init__(self, segmentos):
        """``segmentos``: iterable of (base address, writable contiguous byte buffer)."""
        self.segmentos = []
        for base, buffer in segmentos:
            view = memoryview(buffer)
            if view.readonly or view.ndim != 1 or not view.c_contiguous or view.itemsize != 1:
                raise ValueError(f'Segment at 0x{base:08x} must be a writable contiguous byte buffer')
            self.segmentos.append((base & MASCARA, (base & MASCARA) + len(view), view.cast('B')))
        self.segmentos.sort(key=lambda s: s[0])
        for (_, fim, _), (base, _, _) in zip(self.segmentos, self.segmentos[1:]):
            if base < fim:
                raise ValueError(f'Segments overlap at 0x{base:08x}')
        self._bases = [base for base, _, _ in self.segmentos]

    def _local(self, endereco, largura):
        endereco &= MASCARA
        i = bisect_right(self._bases, endereco) - 1
        if i >= 0:
            base, fim, view = self.segmentos[i]
            if endereco + largura <= fim:
                return view, endereco - base
        raise AcessoForaDosSegmentos(endereco, largura)

    def _acesso(self, largura, endereco, valor):
        view, o = self._local(endereco, largura)
        if valor is None:
            return struct.unpack_from(_FORMATOS[largura], view, o)[0]
        valor &= (1 << 8 * largura) - 1
        struct.pack_into(_FORMATOS[largura], view, o, valor)
        return valor

    def u8(self, endereco, valor=None):
        return self._acesso(1, endereco, valor)

    def u16(self, endereco, valor=None):
        return self._acesso(2, endereco, valor)

    def u32(self, endereco, valor=None):
        return self._acesso(4, endereco, valor)

    def vista(self, endereco, tamanho):
        """Writable live memoryview of ``tamanho`` bytes at ``endereco`` (no copy)."""
        view, o = self._local(endereco, tamanho)
        return view[o:o + tamanho]

    def ler(self, endereco, tamanho):
        view, o = self._local(endereco, tamanho)
        return bytes(view[o:o + tamanho])
