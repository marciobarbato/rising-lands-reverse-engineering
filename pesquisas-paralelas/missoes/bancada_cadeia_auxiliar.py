"""Intact L7 auxiliary chain in both MissionLoad callers.

Engine code (loaders, InitEntrerMonstre, Random and the Watcom CRT) runs
unpatched. Only two declared external bindings replace work: the game's file
read wrapper 0x458461 (fixture bytes) and the five KERNEL32 profile CALL sites
of InitEntrerMonstre, answered by the caller-supplied profile binding.
"""
import struct
import ambiente_missoes
from emulador import BancadaX86,RETORNO,x86

DATA=(0x494000,0x523000)  # DGROUP plus .bss: every global the chain can reach
CALLERS={'MissionLoad':(0x46c57d,0x46c5a5),'MissionLoadName':(0x46c946,0x46c96e)}
ROUTINES=[(0x47534a,0x47539c),(0x47c24d,0x47c2ec),(0x47bcc7,0x47bd40),(0x47c04a,0x47c0c3),
          (0x458b05,0x458b72),(0x47c30f,0x47c359),(0x47c404,0x47c4b7),(0x47ac30,0x47ad6a),
          (0x47a601,0x47a81d),(0x4704dc,0x470520),(0x458475,0x458476)]
# Complete Watcom CRT bodies (SBL symbol bounds) reached by memset/sprintf/sscanf in a
# permissive discovery run; 0x48cfa8 is sprintf's unnamed buffer-putc callback.
CRT=[(0x48c341,0x48c38b),(0x48c38b,0x48c3b0),(0x48c3b0,0x48c3f5),(0x48c3f5,0x48c41c),
     (0x48c41c,0x48c43e),(0x48cfa8,0x48cfbb),(0x48cfbb,0x48cfeb),(0x48d890,0x48d8c7),
     (0x48d8c7,0x48d942),(0x48d942,0x48e564),(0x48e940,0x48e94e),(0x48efe8,0x48fb01)]
PROFILE_INT={0x47a665,0x47a688,0x47a6a5,0x47a6c7}
PROFILE_STRING=0x47a74d
READ=0x458461


class BancadaCadeiaAuxiliar(BancadaX86):
    def __init__(self,crt=None):
        super().__init__()
        self.intervals=list(CALLERS.values())+ROUTINES+list(CRT if crt is None else crt)
        self.calls={name:0 for name in CALLERS}
        self.returned=self.read_stops=self.profile_stops=0

    def imagem(self):
        return bytes(self.cpu.mem_read(DATA[0],DATA[1]-DATA[0]))

    def _texto(self,address):
        data=bytes(self.cpu.mem_read(address,256))
        end=data.find(b'\0')
        if end<0:
            raise ValueError('Unterminated profile argument string')
        return data[:end]

    def _perfil(self,regs,perfil):
        esp=regs['ESP']
        if regs['EIP']==PROFILE_STRING:
            app,key,default,buffer,size,name=struct.unpack('<6I',self.cpu.mem_read(esp,24))
            value=perfil.texto(self._texto(app),self._texto(key),self._texto(default),size,self._texto(name))
            self.cpu.mem_write(buffer,bytes(value)+b'\0')
            result,args=len(value),24
        else:
            app,key,default,name=struct.unpack('<4I',self.cpu.mem_read(esp,16))
            result=perfil.inteiro(self._texto(app),self._texto(key),default,self._texto(name))
            args=16
        # stdcall: callee pops its arguments; execution resumes after the CALL.
        self.cpu.reg_write(x86.UC_X86_REG_EAX,result&0xffffffff)
        self.cpu.reg_write(x86.UC_X86_REG_ESP,esp+args)
        self.profile_stops+=1
        return regs['EIP']+7

    def _registradores(self):
        return {name:self.cpu.reg_read(getattr(x86,'UC_X86_REG_'+name))
                for name in ('EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP','EIP')}

    def carregar(self,data,offset,image,perfil,caller='MissionLoad',stop=None):
        """Run the caller chain over a full data/.bss image; return the stop EIP.

        stop=(address,predicate) halts before the first execution of address whose
        predicate(bench,registers) is true; other visits are single-stepped.
        """
        entry,end=CALLERS[caller];self.calls[caller]+=1
        if len(image)!=DATA[1]-DATA[0]:
            raise ValueError('Data image must cover 0x494000..0x523000')
        self.cpu.mem_write(DATA[0],bytes(image))
        self.cursor,self.reads=offset,[]
        stops={end,READ,PROFILE_STRING}|PROFILE_INT|({stop[0]} if stop else set())
        regs=self.executar(entry,self.intervals,parada=stops,limite_instrucoes=200000)
        while regs['EIP']!=end:
            eip=regs['EIP']
            if stop and eip==stop[0]:
                if stop[1](self,regs):
                    return eip
                self.paradas.discard(eip)
                self.cpu.emu_start(eip,RETORNO,timeout=1_000_000,count=1)
                regs=self._registradores()
                if regs['EIP'] in stops:
                    continue
                resume=regs['EIP']
            elif eip==READ:
                size=regs['EDX'];last=self.cursor+size
                if last>len(data):
                    raise ValueError('Truncated successful-I/O auxiliary fixture')
                self.reads.append((self.cursor,size))
                self.cpu.mem_write(regs['EAX'],bytes(data[self.cursor:last]))
                self.cursor=last;self.cpu.reg_write(x86.UC_X86_REG_EAX,size)
                self.read_stops+=1;resume=0x458475
            else:
                resume=self._perfil(regs,perfil)
            regs=self.retomar(resume,self.intervals,parada=stops,limite_instrucoes=200000)
        self.returned+=1
        return regs['EIP']
