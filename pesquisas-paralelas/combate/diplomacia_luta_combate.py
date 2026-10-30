"""Intact raid diplomacy and profile-message queue over live original memory."""
from abi_luta_fatal_combate import M32, DependenciaLutaFatal, registradores_exigidos, assinado
from entrada_estruturas import ArgumentoNaoPassado

ADDRESSES = {'MAJSympathie':0x475118, 'PlayerResetAllie':0x46d8cb,
             'PlayerAAttaqueSet':0x46d600, 'MessageBoxSet':0x46994b}


class PerfilTextoLuta:
    """The same media-backed Windows profile semantics used by Missions' oracle.

    Installation/CD identity comes from the caller's EntradasNomeadas, not game
    defaults. No Windows state is fabricated and an absent file raises.
    """
    def __init__(self, entradas):
        from fronteiras_carga_missao import MidiaOriginal, PerfilWindows
        self.perfil = PerfilWindows(MidiaOriginal(entradas))
        self.chamadas = []

    def __call__(self, section, key, default, size, filename):
        if not section or not key or size <= 0:
            raise ValueError('Profile enumeration and zero-size buffers are outside this contract')
        value = self.perfil._valor(section, key, filename)
        if value is None: value = default
        if len(value)>=2 and value[:1]==value[-1:] and value[:1] in (b'"',b"'"):
            value=value[1:-1]
        value=value[:size-1]
        self.chamadas.append(('string',section,key,filename,size,value))
        return value

    def importacao(self, memoria, regs, pilha, *, chamada=0x5231b0):
        """Declared stdcall boundary, six stack arguments; only EAX changes.

        The caller's memory must include its actual string/stack buffers. This
        models the established external answer, not execution of Windows code.
        Core's binding transport owns RET/stack cleanup (24 argument bytes).
        """
        out=registradores_exigidos('KERNEL32.GetPrivateProfileStringA',chamada,regs)
        if pilha is None or len(pilha)!=6:
            raise ArgumentoNaoPassado('KERNEL32.GetPrivateProfileStringA',chamada,('pilha[0..5]',))
        section,key,default,target,size,filename=(v&M32 for v in pilha)
        def string(address,limit):
            if not address:return b''
            data=bytearray()
            for i in range(limit):
                value=memoria.u8(address+i)
                if not value:return bytes(data)
                data.append(value)
            raise ValueError('Unterminated declared profile argument')
        data=self(string(section,512),string(key,512),string(default,4096),size,string(filename,512))
        memoria.vista(target,len(data)+1)[:]=data+b'\0'
        out['EAX']=len(data)
        return out


class DiplomaciaLuta:
    def __init__(self, memoria, *, perfil=None):
        self.m, self.perfil = memoria, perfil

    def _string(self, address, limit=4096):
        out=bytearray()
        for i in range(limit):
            v=self.m.u8(address+i)
            if not v: return bytes(out)
            out.append(v)
        raise ValueError('Unterminated original profile string')

    def _texto(self, section, key, default, size, filename, target):
        if self.perfil is None:
            raise DependenciaLutaFatal('KERNEL32.GetPrivateProfileStringA',0x5231b0,
                                      (section,key,default,size,filename,target))
        data=self.perfil(section,key,default,size,filename)
        if not isinstance(data,bytes) or len(data)>=size:
            raise ValueError('Profile provider must return bytes fitting nSize-1')
        self.m.vista(target,len(data)+1)[:]=data+b'\0'

    def message_box(self, eax, edx):
        """Semantic inputs with exact clobbered EAX/EDX; other registers saved."""
        m=self.m
        if m.u8(0x507d58): return dict(EAX=edx & M32,EDX=edx & M32)
        tail=m.u16(0x507d56)
        if tail>=256: raise ValueError('Protected message queue index requires 0..255')
        record=0x4e7754+518*tail
        m.u8(record,eax);m.u16(record+2,edx)
        code=edx&65535
        key=(f'{code:03d}' if code<1000 else f'{code%10000:04d}').encode('ascii')
        filename=self._string(0x509094)
        self._texto(self._string(0x494aed),key,self._string(0x494aec),250,filename,record+0x106)
        self._texto(self._string(0x494af8),key,self._string(0x494af7),250,filename,record+4)
        text=self._string(record+4,250)
        star=text.find(b'*')
        if star<0: m.u16(record+0x102,0xffff)
        else:
            m.u16(record+0x102,star+1);m.u8(record+4+star,0)
        m.u16(record+0x104,400)
        next_tail=(tail+1)%256
        m.u16(0x507d56,next_tail)
        if next_tail==m.u16(0x507d54): m.u8(0x507d58,1)
        return dict(EAX=(tail+1)//256,EDX=next_tail)

    def reset_allie(self, eax, edx):
        m=self.m; a,b=eax&255,edx&255
        if a==b: return dict(EAX=eax&M32,EDX=edx&M32)
        if a>4 or b>4: return dict(EAX=a,EDX=edx&M32)
        rec=m.u32(0x5080a8)+20*a
        mask=m.u8(rec+6)&~(1<<b)&255
        m.u8(rec+6,mask)
        out=dict(EAX=5*a,EDX=(edx&0xffff00ff)|(mask<<8))
        if a==m.u8(0x508041): out=self.message_box(10,b+402)
        return out

    def attaque_set(self, eax, edx):
        a,b=eax&255,edx&255
        if a>=4 or b>=4: return dict(EAX=a,EDX=edx&M32)
        address=0x508044+20*a+4*b
        self.m.u32(address,self.m.u32(address)+1)
        return dict(EAX=b,EDX=20*a)

    def maj_sympathie(self, eax, edx, ebx):
        m=self.m;a,b=eax&M32,edx&M32;action=ebx&M32
        out=dict(EAX=a,EDX=b,EBX=action)
        if a==b or a>=4 or b>=4: return out
        out['EAX']=16*a
        if m.u8(0x51a990+16*a): return out
        out['EAX']=16*b
        if m.u8(0x51a990+16*b): return out
        if action>=11: raise ValueError('Protected sympathy action requires 0..10')
        offset=16*action;rec=0x497288+offset
        count=(m.u32(rec+8)+1)&M32
        out.update(EAX=offset,EBX=count)
        m.u32(rec+8,count)
        if count<m.u32(rec+12): return out
        mode=m.u8(rec+4);out['EBX']=mode;m.u32(rec+8,0)
        pairs=((x,y) for x in range(4) for y in range(4) if x!=y) if mode==1 else ((a,b),)
        for x,y in pairs:
            player=m.u32(0x5080a8)+20*x
            value=assinado(m.u16(player+12+2*y),16)
            change=assinado(m.u32(rec))
            total=assinado((value+change)&M32)
            total=max(-50,min(50,total))
            m.u16(player+12+2*y,total)
            out.update(EAX=y,EBX=total&M32,EDX=player)
        return out

    def efeito(self, nome, argumentos):
        return {'MAJSympathie':self.maj_sympathie,'PlayerResetAllie':self.reset_allie,
                'PlayerAAttaqueSet':self.attaque_set,'MessageBoxSet':self.message_box}[nome](*argumentos)

    def chamar(self, nome, regs, *, chamada=None):
        out=registradores_exigidos(nome,ADDRESSES[nome] if chamada is None else chamada,regs)
        args=(out['EAX'],out['EDX'],out['EBX']) if nome=='MAJSympathie' else (out['EAX'],out['EDX'])
        out.update(self.efeito(nome,args))
        return out

    def provedores(self):
        return {name:(lambda regs,n=name:self.chamar(n,regs)) for name in ADDRESSES}
