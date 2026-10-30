"""ctypes additions for the deterministic ABI 1.1 frame-phase contract."""
import ctypes as C
import struct

from pilot_abi import Pilot

FRAME_VERSION = 0x00010005
REGISTERS = ('eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp')


class FrameRegisters(C.Structure):
    _fields_ = [(n, C.c_uint32) for n in REGISTERS]

    @classmethod
    def from_values(cls, values):
        return cls(**{n: values[n.upper()] for n in REGISTERS})

    def values(self):
        return {n.upper(): getattr(self, n) for n in REGISTERS}


class FrameInput(C.Structure):
    _fields_ = [('cursor_x', C.c_int32), ('cursor_y', C.c_int32),
                ('offscreen', C.c_uint32), ('registers', FrameRegisters),
                ('saved', C.c_uint32 * 3), ('msg', C.c_uint32 * 4)]


class FrameEvent(C.Structure):
    _fields_ = [('kind', C.c_uint32), ('id', C.c_uint32), ('site', C.c_uint32),
                ('args', C.c_uint32 * 5), ('result', C.c_uint32),
                ('registers', C.c_uint32 * 4), ('stack', C.c_uint32 * 4),
                ('stack_mask', C.c_uint32)]


def unpack_blocks(raw):
    """Strictly decode copied bulk snapshots, rejecting truncation/duplicates/tails."""
    if len(raw) < 4:
        raise ValueError('Truncated block count')
    count, = struct.unpack_from('<I', raw)
    blocks, offset = {}, 4
    for _ in range(count):
        if offset + 8 > len(raw):
            raise ValueError('Truncated block descriptor')
        address, length = struct.unpack_from('<II', raw, offset)
        offset += 8
        if not length or offset + length > len(raw) or address in blocks:
            raise ValueError('Invalid block size, duplicate address or truncated data')
        blocks[address] = raw[offset:offset + length]
        offset += length
    if offset != len(raw):
        raise ValueError('Trailing snapshot bytes')
    return blocks


class Frames(Pilot):
    def __init__(self, path=None):
        super().__init__(path)
        if self.lib.rl_versao() != FRAME_VERSION:
            raise RuntimeError('Frame C ABI version mismatch')
        u32, u64 = C.c_uint32, C.c_uint64
        self.lib.rl_passo_quadro.argtypes = [u64, u32, C.POINTER(FrameInput)]
        self.lib.rl_passo_quadro.restype = C.c_int32
        self.lib.rl_eventos_quadro.argtypes = [u64, C.POINTER(FrameEvent), u32, C.POINTER(u32)]
        self.lib.rl_eventos_quadro.restype = C.c_int32
        for name in ('rl_projetar_tudo', 'rl_projetar_liberados'):
            fn = getattr(self.lib, name)
            fn.argtypes = [u64, C.POINTER(C.c_uint8), u32, C.POINTER(u32)]
            fn.restype = C.c_int32

    def snapshot(self, handle, freed=False):
        fn = self.lib.rl_projetar_liberados if freed else self.lib.rl_projetar_tudo
        required = C.c_uint32()
        code = fn(handle, None, 0, C.byref(required))
        if code != 6:
            self.check(code)
            raise RuntimeError('Expected bulk snapshot size query')
        buf = (C.c_uint8 * required.value)()
        self.check(fn(handle, buf, len(buf), C.byref(required)))
        return unpack_blocks(bytes(buf))

    def frame(self, handle, phase, inputs):
        self.check(self.lib.rl_passo_quadro(handle, phase, C.byref(inputs)))

    def events(self, handle):
        required = C.c_uint32()
        code = self.lib.rl_eventos_quadro(handle, None, 0, C.byref(required))
        if code not in (0, 6):
            self.check(code)
        buf = (FrameEvent * required.value)()
        self.check(self.lib.rl_eventos_quadro(handle, buf, len(buf), C.byref(required)))
        return list(buf)
