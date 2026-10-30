"""ctypes binding for the copied-buffer pilot ABI, independent of app workers."""
import ctypes as C
import os
from pathlib import Path
import sys
from pinned_reference import activate, reference_file, pinned_file
SOURCE_ROOT = activate()

ENGINE = Path(__file__).resolve().parents[1]
ROOT = ENGINE.parent
VERSION = 0x00010005
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
    return Path(os.environ.get('RL_LIBRARY', str(ENGINE / 'target/debug' / ('librising_engine.' + suffix))))


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

    def step(self, handle, name, values):
        registers = Registers.from_values(values)
        self.check(self.lib.rl_executar_rotina(handle, ROUTINES[name], C.byref(registers)))
        return registers.values()

    def clock(self, handle):
        tick, ms = C.c_uint64(), C.c_uint32()
        self.check(self.lib.rl_relogio(handle, C.byref(tick), C.byref(ms)))
        return tick.value, ms.value

    def free(self, handle):
        self.check(self.lib.rl_liberar_mundo(handle))
