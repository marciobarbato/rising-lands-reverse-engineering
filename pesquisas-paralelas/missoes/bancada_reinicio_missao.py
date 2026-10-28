"""Intact MissionLoad/MissionLoadName reset prefixes and their three UI leaf resets.

Every engine body runs unpatched. TerrainReset/MiniMapReset (core) and the
MissionLoadName research/experience resets have no committed provider, so
entries stop before those CALLs; the tail is entered at its original
post-MiniMapReset instruction with the caller's frame. FileOpen 0x458420 is a
stop (the declared file binding), never executed.
"""
import struct
import ambiente_missoes
from emulador import BancadaX86,PILHA,RETORNO,UNIDADES,x86

DATA=(0x494000,0x523000)
POINTERS=0x1400000
BAGS=tuple(0x1410000+i*0x1000 for i in range(4))
PROJECTILES=0x1500000
PLAYERS=0x1600000
FRAME=PILHA+0x8000+0x100
LEAVES={'IconeReset':(0x45e88f,0x45e90b),'MessageBoxInit':(0x469908,0x46994b),'BallonInit':(0x441b6c,0x441baa)}
PROVIDERS=[(0x41a75c,0x41a860),(0x441659,0x441775),(0x46e00a,0x46e02c),(0x4749f2,0x474a38)]
NAME=[(0x46c1b8,0x46c2cf),(0x46dc6c,0x46dc90)]
ENTRIES={'MissionLoad':0x46c2cf,'MissionLoad_tail':0x46c369,
         'MissionLoadName':0x46c5e3,'MissionLoadName_tail':0x46c619}
CALLERS=[(0x46c2cf,0x46c396),(0x46c5e3,0x46c76c)]
FILE_OPEN=0x458420
# Original CALL sites whose callee has no committed provider.
TERRAIN={'MissionLoad':0x46c35f,'MissionLoadName':0x46c60f}
RESEARCH_RESET=0x46c68c


def ponteiros(image):
    """Point the original pool globals of a data image at the bench allocations."""
    for address,value in ((0x4e19a0,UNIDADES),(0x4e19b8,POINTERS),(0x5080f0,PROJECTILES),(0x5080a8,PLAYERS)):
        struct.pack_into('<I',image,address-DATA[0],value)
    return image


class BancadaReinicioMissao(BancadaX86):
    def __init__(self):
        super().__init__()
        for base in (POINTERS,PROJECTILES,PLAYERS)+BAGS:
            self.cpu.mem_map(base,0x2000 if base==PROJECTILES else 0x1000)
        self.intervals=CALLERS+NAME+PROVIDERS+list(LEAVES.values())
        self.entries={name:0 for name in list(ENTRIES)+list(LEAVES)}
        self.stops={}

    def carregar(self,image,units,bags,projectiles,players):
        if len(image)!=DATA[1]-DATA[0] or len(units)!=220800 or len(projectiles)!=5600:
            raise ValueError('Reset bench inputs have fixed original widths')
        if bytes(image)!=bytes(ponteiros(bytearray(image))):
            raise ValueError('Image must carry the bench pool pointers (use ponteiros)')
        self.cpu.mem_write(DATA[0],bytes(image))
        self.cpu.mem_write(POINTERS,struct.pack('<4I',*BAGS))
        self.cpu.mem_write(UNIDADES,bytes(units))
        for base,bag in zip(BAGS,bags):
            self.cpu.mem_write(base,bytes(bag))
        self.cpu.mem_write(PROJECTILES,bytes(projectiles))
        self.cpu.mem_write(PLAYERS,bytes(players))

    def estado(self):
        return dict(image=bytes(self.cpu.mem_read(DATA[0],DATA[1]-DATA[0])),
                    units=bytes(self.cpu.mem_read(UNIDADES,220800)),
                    bags=tuple(bytes(self.cpu.mem_read(b,2704)) for b in BAGS),
                    projectiles=bytes(self.cpu.mem_read(PROJECTILES,5600)),
                    players=bytes(self.cpu.mem_read(PLAYERS,80)))

    def texto(self,address,size=0x100):
        data=bytes(self.cpu.mem_read(address,size))
        return data[:data.index(b'\0')]

    def _stop(self,regs):
        self.stops[hex(regs['EIP'])]=self.stops.get(hex(regs['EIP']),0)+1
        return regs

    def folha(self,name):
        self.entries[name]+=1
        return self._stop(self.executar(LEAVES[name][0],self.intervals,parada=RETORNO))

    def prefixo(self,caller,*,number=None,name=None):
        """Prologue entry; stop at the TerrainReset CALL (no provider)."""
        self.entries[caller]+=1
        if caller=='MissionLoad':
            self.cpu.mem_write(0x496fe4,bytes([number&255]))
            regs=self.executar(ENTRIES[caller],self.intervals,parada=TERRAIN[caller],limite_instrucoes=200000)
            frame=regs['ESP']
            return self._stop(regs),dict(path=self.texto(frame),name=self.texto(frame+0x100))
        regs=self.executar(ENTRIES[caller],self.intervals,dict(EAX=PILHA+0x8000+0x800),
                           parada=TERRAIN[caller],pilha={0x800:name+b'\0'},limite_instrucoes=200000)
        return self._stop(regs),dict(name_argument=self.texto(struct.unpack('<I',self.cpu.mem_read(regs['ESP'],4))[0]))

    def continuacao(self,caller,*,path=None,name=None):
        """Enter at the original instruction after MiniMapReset, with the caller frame."""
        self.entries[caller+'_tail']+=1
        if caller=='MissionLoad':
            regs=self.executar(ENTRIES['MissionLoad_tail'],self.intervals,dict(ESP=FRAME),parada=FILE_OPEN,
                               pilha={0x100:path+b'\0'},limite_instrucoes=400000)
            return self._stop(regs),dict(path=self.texto(regs['EAX']),mode=self.texto(regs['EDX']))
        pointer=PILHA+0x8000+0x800
        regs=self.executar(ENTRIES['MissionLoadName_tail'],self.intervals,dict(ESP=FRAME),parada=RESEARCH_RESET,
                           pilha={0x100:struct.pack('<I',pointer),0x800:name+b'\0'},limite_instrucoes=400000)
        return self._stop(regs),{}
