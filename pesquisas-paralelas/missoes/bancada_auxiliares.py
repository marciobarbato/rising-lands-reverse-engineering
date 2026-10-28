"""Intact post-unit LoadMine/IALoadAttaqueIni caller prefixes."""
import ambiente_missoes
from emulador import BancadaX86,x86

MINES=0x509954
ATTACKS=0x50d5b4
CALLERS={'MissionLoad':(0x46c57d,0x46c587),'MissionLoadName':(0x46c946,0x46c950)}
INTERVALS=list(CALLERS.values())+[(0x47534a,0x47539c),(0x47c24d,0x47c2ec),(0x458475,0x458476)]


class BancadaAuxiliares(BancadaX86):
    def __init__(self):
        super().__init__()
        self.calls={name:0 for name in CALLERS}

    def carregar(self,data,offset,mines,attacks,caller='MissionLoad'):
        entry,stop=CALLERS[caller];self.calls[caller]+=1
        self.cpu.mem_write(MINES,bytes(mines));self.cpu.mem_write(ATTACKS,bytes(attacks))
        self.cursor,self.reads=offset,[]
        regs=self.executar(entry,INTERVALS,parada={stop,0x458461})
        while regs['EIP']!=stop:
            size=regs['EDX'];end=self.cursor+size
            if end>len(data):
                raise ValueError('Truncated successful-I/O auxiliary fixture')
            self.reads.append((self.cursor,size))
            self.cpu.mem_write(regs['EAX'],bytes(data[self.cursor:end]))
            self.cursor=end;self.cpu.reg_write(x86.UC_X86_REG_EAX,size)
            regs=self.retomar(0x458475,INTERVALS,parada={stop,0x458461})
        return regs

    def estado(self):
        return bytes(self.cpu.mem_read(MINES,80)),bytes(self.cpu.mem_read(ATTACKS,1004))
