"""Intact inline indexed structure readers, before either LoadEngin call."""
import ambiente_missoes
from emulador import BancadaX86,x86

POOL=0x49a0c8
CALLERS={'MissionLoad':(0x46c517,0x46c578),'MissionLoadName':(0x46c8e0,0x46c941)}
INTERVALS=list(CALLERS.values())+[(0x458475,0x458476)]


class BancadaCargaEstruturas(BancadaX86):
    def __init__(self):
        super().__init__()
        self.calls={name:0 for name in CALLERS}

    def carregar(self,data,offset,pool,caller='MissionLoad'):
        entry,stop=CALLERS[caller]
        self.calls[caller]+=1
        self.cpu.mem_write(POOL,bytes(pool))
        self.cursor,self.reads=offset,[]
        regs=self.executar(entry,INTERVALS,parada={stop,0x458461})
        while regs['EIP']!=stop:
            size=regs['EDX'];end=self.cursor+size
            if end>len(data):
                raise ValueError('Truncated successful-I/O structure fixture')
            self.reads.append((self.cursor,size))
            self.cpu.mem_write(regs['EAX'],bytes(data[self.cursor:end]))
            self.cursor=end
            self.cpu.reg_write(x86.UC_X86_REG_EAX,size)
            regs=self.retomar(0x458475,INTERVALS,parada={stop,0x458461})
        return regs

    def estado(self):
        return bytes(self.cpu.mem_read(POOL,276000))
