"""Intact MakeMissionName and real PlayerGetSympathie, without file opening."""
import struct
import ambiente_missoes
from emulador import BancadaX86,RETORNO,x86,unicorn

DEST=0x1100000
PLAYERS=0x1120000
INTERVALS=[(0x46c1b8,0x46c2cf),(0x46dc6c,0x46dc90)]


class BancadaNomeMissao(BancadaX86):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(DEST,0x1000)
        self.cpu.mem_map(PLAYERS,0x1000)
        self.cpu.mem_write(0x5080a8,struct.pack('<I',PLAYERS))
        self.calls=self.returned=self.dependency_stops=0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE,self._query)

    def _query(self,cpu,address,size,_):
        if address==0x46dc6c:
            self.queries.append((cpu.reg_read(x86.UC_X86_REG_EAX)&255,
                                 cpu.reg_read(x86.UC_X86_REG_EDX)&255))
            if self.stop_query==len(self.queries):
                self.paradas.add(address)
                cpu.emu_stop()

    def nome(self,number,variant,players,output,*,stop_query=None):
        self.calls+=1
        self.queries=[];self.stop_query=stop_query
        self.cpu.mem_write(PLAYERS,bytes(players))
        self.cpu.mem_write(DEST,bytes(output))
        self.cpu.mem_write(0x4e1d85,bytes([variant&255]))
        regs=self.executar(0x46c1b8,INTERVALS,dict(EAX=number,EDX=DEST,ECX=0x12345678))
        if regs['EIP']==RETORNO:
            self.returned+=1
        else:
            self.dependency_stops+=1
        return regs

    def estado(self):
        return bytes(self.cpu.mem_read(DEST,64)),bytes(self.cpu.mem_read(PLAYERS,80))
