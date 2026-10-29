"""App-owned copied-buffer ABI 1.3 binding. Serialized worker use only.

Layouts follow motor/include/rising_engine.h; no Rust pointers escape.
"""
import ctypes as C
import struct
import os
from pathlib import Path
import sys

VERSION = 0x00010003
NAMES = ('eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp')
ROUTINES = {'Random': 1, 'LongRand': 2, 'rand': 3, 'IntToBCD': 4, 'BCDToInt': 5}


class Registers(C.Structure):
    _fields_ = [(name, C.c_uint32) for name in NAMES]

    def values(self):
        return {name.upper(): getattr(self, name) for name in NAMES}

    @classmethod
    def from_values(cls, values):
        return cls(**{name: values[name.upper()] for name in NAMES})


class Block(C.Structure):
    _fields_ = [('address', C.c_uint32), ('length', C.c_uint32), ('data', C.POINTER(C.c_uint8))]


def library_path():
    suffix = 'dylib' if sys.platform == 'darwin' else 'so'
    return Path(__file__).resolve().parent / ('librising_engine.' + suffix)


class Pilot:
    def __init__(self, path=None):
        self.path = Path(path or library_path()).resolve()
        self.lib = C.CDLL(str(self.path))
        u32, u64 = C.c_uint32, C.c_uint64
        signatures = {
            'rl_versao': ([], u32),
            'rl_criar_mundo': ([u32, u32, u32, C.POINTER(u64)], C.c_int32),
            'rl_liberar_mundo': ([u64], C.c_int32),
            'rl_carregar_blocos': ([u64, C.POINTER(Block), u32], C.c_int32),
            'rl_executar_rotina': ([u64, u32, C.POINTER(Registers)], C.c_int32),
            'rl_quantidade_blocos': ([u64, C.POINTER(u32)], C.c_int32),
            'rl_projetar_bloco': ([u64, u32, C.POINTER(u32), C.POINTER(C.c_uint8), u32, C.POINTER(u32)], C.c_int32),
            'rl_avancar_ticks': ([u64, u64], C.c_int32),
            'rl_relogio': ([u64, C.POINTER(u64), C.POINTER(u32)], C.c_int32),
            'rl_erro_mensagem': ([C.POINTER(C.c_uint8), u32, C.POINTER(u32)], C.c_int32),
        }
        for name, (arguments, result) in signatures.items():
            fn = getattr(self.lib, name)
            fn.argtypes, fn.restype = arguments, result
        if self.lib.rl_versao() != VERSION:
            raise RuntimeError('Pilot C ABI version mismatch')

    def error(self):
        required = C.c_uint32()
        self.lib.rl_erro_mensagem(None, 0, C.byref(required))
        output = (C.c_uint8 * required.value)()
        code = self.lib.rl_erro_mensagem(output, len(output), C.byref(required))
        if code:
            raise RuntimeError('Error-message query failed: ' + str(code))
        return bytes(output).rstrip(b'\0').decode('utf-8')

    def check(self, code):
        if code:
            raise RuntimeError('Rust ABI status ' + str(code) + ': ' + self.error())

    def create(self, rate=20, epoch=0):
        handle = C.c_uint64()
        self.check(self.lib.rl_criar_mundo(VERSION, rate, epoch, C.byref(handle)))
        return handle.value

    def load(self, handle, blocks):
        # Keep all temporary input buffers alive until the synchronous copy ends.
        buffers = [(C.c_uint8 * len(data)).from_buffer_copy(data) for _, data in blocks]
        descriptors = (Block * len(blocks))(*(Block(base, len(data), buffer)
                         for (base, data), buffer in zip(blocks, buffers)))
        self.check(self.lib.rl_carregar_blocos(handle, descriptors, len(descriptors)))

    def project(self, handle):
        count = C.c_uint32()
        self.check(self.lib.rl_quantidade_blocos(handle, C.byref(count)))
        blocks = []
        for index in range(count.value):
            address, size = C.c_uint32(), C.c_uint32()
            code = self.lib.rl_projetar_bloco(handle, index, C.byref(address), None, 0, C.byref(size))
            if code != 6:
                self.check(code)
                raise RuntimeError('Expected bounded projection size query')
            buffer = (C.c_uint8 * size.value)()
            self.check(self.lib.rl_projetar_bloco(handle, index, C.byref(address), buffer, len(buffer), C.byref(size)))
            blocks.append((address.value, bytes(buffer)))
        return blocks

    def clock(self, handle):
        tick, ms = C.c_uint64(), C.c_uint32()
        self.check(self.lib.rl_relogio(handle, C.byref(tick), C.byref(ms)))
        return tick.value, ms.value

    def free(self, handle):
        self.check(self.lib.rl_liberar_mundo(handle))

FRAME_VERSION = 0x00010003
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
    if count > 65536: raise ValueError('Snapshot block limit exceeded')
    blocks, offset, end, total = {}, 4, 0, 0
    for _ in range(count):
        if offset + 8 > len(raw):
            raise ValueError('Truncated block descriptor')
        address, length = struct.unpack_from('<II', raw, offset)
        offset += 8
        if not length or offset + length > len(raw) or address in blocks:
            raise ValueError('Invalid block size, duplicate address or truncated data')
        if address < end or address + length > 2**32 or total + length > 64*1024*1024:
            raise ValueError('Overlapping, unordered, overflowing or oversized snapshot')
        end, total = address + length, total + length
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
