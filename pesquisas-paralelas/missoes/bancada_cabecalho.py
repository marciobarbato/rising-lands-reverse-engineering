"""Intact MissionLoad successful-open prelude, stopped before Chemin_Remap."""
import struct
import ambiente_missoes
from emulador import BancadaX86, x86

LAYERS = ((0x507da8, 0x1100000, 65536), (0x507d70, 0x1120000, 131072),
          (0x507d74, 0x1140000, 65536), (0x507dac, 0x1160000, 65536))
INTERVALS = [(0x46c396, 0x46c517), (0x46799c, 0x4679d0),
             (0x458475, 0x458476), (0x4584a2, 0x4584a3)]


class BancadaCabecalho(BancadaX86):
    def __init__(self):
        super().__init__()
        for pointer, base, size in LAYERS:
            self.cpu.mem_map(base, size)
            self.cpu.mem_write(pointer, struct.pack('<I', base))
        self.calls = 0

    def carregar(self, data, *, camera, resources, dimensions, view):
        self.calls += 1
        self.cpu.mem_write(0x508041, bytes([camera & 255]))
        self.cpu.mem_write(0x4e2ea8, bytes(resources))
        self.cpu.mem_write(0x497168, bytes(dimensions))
        self.cpu.mem_write(0x508720, bytes(view))
        self.io, self.resource_calls = [], []
        self.cursor = 0
        stops = {0x458461, 0x45848b, 0x42ee1c, 0x46799c}
        entry = 0x46c396
        regs = self.executar(entry, INTERVALS, parada=stops, limite_instrucoes=1000000)
        while regs['EIP'] != 0x42ee1c:
            pc = regs['EIP']
            if pc == 0x46799c:
                self.resource_calls.append((regs['EBX'] & 65535, regs['EAX'] & 255, regs['EDX'] & 65535))
                # Retain the actual setter; suppress only this entry checkpoint.
                regs = self.retomar(pc, INTERVALS, parada=stops-{pc}, limite_instrucoes=1000000)
                continue
            if pc == 0x458461:
                count = regs['EDX']
                end = self.cursor + count
                if end > len(data):
                    raise ValueError('Native successful-I/O prelude fixture truncated')
                self.io.append(('read', self.cursor, count))
                self.cpu.mem_write(regs['EAX'], bytes(data[self.cursor:end]))
                self.cursor = end
                self.cpu.reg_write(x86.UC_X86_REG_EAX, count)
                entry = 0x458475
            else:
                if regs['EDX'] & 255:
                    raise ValueError('Unexpected seek mode in mission prelude')
                self.io.append(('seek_absolute', self.cursor, regs['EAX']))
                self.cursor = regs['EAX']
                self.cpu.reg_write(x86.UC_X86_REG_EAX, self.cursor)
                entry = 0x4584a2
            regs = self.retomar(entry, INTERVALS, parada=stops, limite_instrucoes=1000000)
        return regs

    def estado(self):
        layers = tuple(bytes(self.cpu.mem_read(base, size)) for _, base, size in LAYERS)
        return layers + tuple(bytes(self.cpu.mem_read(address, size)) for address, size in
                              ((0x4e2ea8, 128), (0x497168, 4), (0x508720, 4)))
