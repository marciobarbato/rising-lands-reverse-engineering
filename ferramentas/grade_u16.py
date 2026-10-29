"""Fixed-size little-endian u16 grid over a caller-owned live byte buffer (by identity).

The original keeps the 256x256 terrain tile grid at [0x507d70] as 65,536 u16
words (131,072 bytes). ``GradeU16`` lets the list-based Core world use that
live allocation directly: reads and stores go to ``grade.buffer`` (the very
object the caller passed, a bytearray or writable memoryview), so Economy,
Missions and AI/runtime see the same bytes without a copy or bridge.

It behaves like the 65,536-item list it replaces for every operation the Core
code uses: ``g[i]`` (negative indexes too), ``g[i] = v``, ``g[a:b]`` (a new
list), ``g[:] = values`` (same length only), ``len``, iteration, ``list(g)``
and equality with any sequence. It cannot change size, and a store outside
0..65535 raises ``ValueError`` before writing, since a u16 cannot hold it.
"""
import struct

_U16 = struct.Struct('<H')


class GradeU16:
    __slots__ = ('buffer', '_v', '_n')

    def __init__(self, buffer, quantidade=65536):
        view = memoryview(buffer)
        if view.readonly or view.ndim != 1 or not view.c_contiguous or view.nbytes != 2 * quantidade:
            raise ValueError(f'A live u16 grid needs a writable contiguous {2 * quantidade}-byte buffer')
        self.buffer = buffer
        self._v = view.cast('B')
        self._n = quantidade

    def __len__(self):
        return self._n

    def _indice(self, i):
        if not isinstance(i, int):
            raise TypeError('grid indices must be integers or slices')
        if i < 0:
            i += self._n
        if not 0 <= i < self._n:
            raise IndexError('grid index out of range')
        return i

    def __getitem__(self, i):
        if isinstance(i, slice):
            inicio, fim, passo = i.indices(self._n)
            if passo == 1:
                return list(struct.unpack_from(f'<{max(fim - inicio, 0)}H', self._v, 2 * inicio))
            return [self[k] for k in range(inicio, fim, passo)]
        return _U16.unpack_from(self._v, 2 * self._indice(i))[0]

    def __setitem__(self, i, valor):
        if isinstance(i, slice):
            indices = range(*i.indices(self._n))
            valores = list(valor)
            if len(valores) != len(indices):
                raise ValueError('a live grid cannot change size')
            if any(not isinstance(v, int) or not 0 <= v <= 0xffff for v in valores):
                raise ValueError('grid values must be u16 integers')
            if indices.step == 1:
                struct.pack_into(f'<{len(valores)}H', self._v, 2 * indices.start if valores else 0, *valores)
            else:
                for k, v in zip(indices, valores):
                    _U16.pack_into(self._v, 2 * k, v)
            return
        if not isinstance(valor, int) or not 0 <= valor <= 0xffff:
            raise ValueError('grid values must be u16 integers')
        _U16.pack_into(self._v, 2 * self._indice(i), valor)

    def __iter__(self):
        return (v for (v,) in _U16.iter_unpack(self._v))

    def __eq__(self, outro):
        try:
            return len(outro) == self._n and list(self) == list(outro)
        except TypeError:
            return NotImplemented

    def __repr__(self):
        return f'GradeU16({self._n} live u16)'
