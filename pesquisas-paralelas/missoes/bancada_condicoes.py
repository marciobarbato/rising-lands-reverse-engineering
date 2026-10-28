"""Intact LoadFinMission/LoadObjectif, with successful FileRead input only."""
import ambiente_missoes
from emulador import BancadaX86, RETORNO, x86

FIN = 0x4e1d20
OBJECTIVES = 0x511ffc
INTERVALS = [(0x458b05,0x458b72),(0x47c404,0x47c4b7),(0x458475,0x458476)]


class BancadaCondicoes(BancadaX86):
    def __init__(self):
        super().__init__()
        self.calls = {0x458b05:0,0x47c404:0}

    def carregar(self,entry,data,offset,fin,objectives):
        self.calls[entry] += 1
        self.cpu.mem_write(FIN,bytes(fin))
        self.cpu.mem_write(OBJECTIVES,bytes(objectives))
        self.cursor,self.reads = offset,[]
        regs = self.executar(entry,INTERVALS,parada={RETORNO,0x458461},limite_instrucoes=20000)
        while regs['EIP'] != RETORNO:
            size = regs['EDX']
            end = self.cursor+size
            if end > len(data):
                raise ValueError('Truncated successful-I/O condition fixture')
            self.reads.append((self.cursor,size))
            self.cpu.mem_write(regs['EAX'],bytes(data[self.cursor:end]))
            self.cursor = end
            self.cpu.reg_write(x86.UC_X86_REG_EAX,size)
            regs = self.retomar(0x458475,INTERVALS,parada={RETORNO,0x458461},limite_instrucoes=20000)
        return regs

    def estado(self):
        return bytes(self.cpu.mem_read(FIN,114)),bytes(self.cpu.mem_read(OBJECTIVES,804))
