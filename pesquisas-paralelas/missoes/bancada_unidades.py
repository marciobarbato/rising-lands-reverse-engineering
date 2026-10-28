"""Execute intact LoadEngin with declared successful in-memory file I/O only.

SelectionInit and every native postload/type/bonus subcall execute unchanged.
The translated scope begins at the checkpoint after SelectionInit. No Win32
runtime, short-read behavior, or complete mission execution is provided here.
"""
import ambiente_missoes
from emulador import BancadaX86, UNIDADES, RETORNO, x86

INTERVALS = [(0x46acbf, 0x46b01e), (0x46b112, 0x46b119),
             (0x472555, 0x472576), (0x457350, 0x457b87),
             (0x428cc0, 0x428e71), (0x441fff, 0x442045),
             (0x4422da, 0x4422eb), (0x458475, 0x458476),
             (0x4584a2, 0x4584a3)]


class BancadaCargaUnidades(BancadaX86):
    def __init__(self):
        super().__init__()
        self.loads = 0
        self.returned = 0
        self.dependency_stops = 0

    def carregar(self, data, offset, pool, flags, types, bonuses, *, parar_bonus=False):
        self.loads += 1
        self.cpu.mem_write(UNIDADES, bytes(pool))
        self.cpu.mem_write(0x4e19bc, bytes(flags))
        self.cpu.mem_write(0x4965ae, bytes(types))
        self.cpu.mem_write(0x4dfba0, bytes(bonuses))
        # Execute the real prologue and SelectionInit before the public boundary.
        self.executar(0x46acbf, INTERVALS, parada=0x46acca)
        self.cursor, self.io = offset, []
        stops = {RETORNO, 0x458461, 0x45848b}
        if parar_bonus:
            stops.add(0x428cc0)
        entry = 0x46acca
        while True:
            regs = self.retomar(entry, INTERVALS, parada=stops, limite_instrucoes=1000000)
            pc = regs['EIP']
            if pc == RETORNO:
                self.returned += 1
                return regs
            if pc == 0x428cc0:
                self.dependency_stops += 1
                return regs
            if pc == 0x458461:
                count, dest = regs['EDX'], regs['EAX']
                end = self.cursor + count
                if end > len(data):
                    raise ValueError('Native successful-I/O fixture is truncated')
                self.io.append(('read', self.cursor, count))
                self.cpu.mem_write(dest, data[self.cursor:end])
                self.cursor = end
                self.cpu.reg_write(x86.UC_X86_REG_EAX, count)
                entry = 0x458475  # Execute the original RET, preserving native stack.
            else:
                amount, mode = regs['EAX'], regs['EDX'] & 255
                if mode != 1:
                    raise ValueError('Unsupported file seek mode in fixture')
                self.io.append(('seek', self.cursor, amount))
                self.cursor += amount
                if self.cursor > len(data):
                    raise ValueError('Native seek beyond supplied fixture')
                self.cpu.reg_write(x86.UC_X86_REG_EAX, self.cursor)
                self.cpu.reg_write(x86.UC_X86_REG_EDX, amount)
                entry = 0x4584a2

    def estado(self):
        return bytes(self.cpu.mem_read(UNIDADES, 800*276)), bytes(self.cpu.mem_read(0x4e19bc, 4))
