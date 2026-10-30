"""Live research/result-screen Economy routines reached by S1.

All seven general registers are explicit, including preserved inputs; ESP is
optional control state. Flags are not modeled. RechercheGetEtat additionally
returns _x87_push=(unsigned significand64, sign/exponent16), one exact ST0 push,
without rounding a double through a host float. No native stack is mutated.
"""
from lacunas_economia_s1 import REG7, M32, exigir

ROTINAS = {
    'RechercheGetEtat':0x4717a2,'RechercheGetBranche':0x4717b1,'RechercheGetNiveau':0x4717c2,
    'RechercheGetNbInvention':0x470554,'InventionGetCout':0x470c3d,'SetBatimentRecrutable':0x418ad3,
    'SetTroupeRecrutable':0x44244d,'TypeBatimentEstRealisable':0x418a93,'TypeEnginEstRealisable':0x44228e,
    'SortilegeResetTechnologie':0x4749f2,'TechnologieReset':0x46b517,'BonusReset':0x428e71,
    'BatimentInitTechnologie':0x41cde0,'EnginSetTechnologie':0x4411e1,'InventionSetEffet':0x470f98,
    'RechercheCalculNew':0x47150f,'IaRechercheAjuste':0x47fa88,
}
PESQUISA,GUARDADA,TABELA=0x5080f4,0x508134,0x50817c
ESTRUTURAS,UNIDADES_REALIZAVEIS,ESTRUTURAS_REALIZAVEIS=0x49a0c8,0x4e1934,0x4dfad4


class DependenciaTecnologiaS1(NotImplementedError):
    def __init__(self,nome,chamada):
        self.rotina,self.chamada=nome,chamada
        super().__init__(f'{nome} called at {chamada:#x}: live provider required; earlier effects retained')


class ForaDoDominioTecnologiaS1(NotImplementedError):
    def __init__(self,nome,endereco,motivo):
        self.rotina,self.endereco=nome,endereco
        super().__init__(f'{nome} at {endereco:#x}: {motivo}')


def double_para_x87(bits):
    """Exact finite IEEE binary64 -> explicit-integer-bit x87 extended value."""
    sinal=bits>>63
    expoente=(bits>>52)&0x7ff
    fracao=bits&((1<<52)-1)
    if expoente==0x7ff:
        raise ForaDoDominioTecnologiaS1('RechercheGetEtat',0x4717aa,'nonfinite research value')
    if expoente:
        mantissa=((1<<52)|fracao)<<11
        expoente=expoente-1023+16383
    elif fracao:
        bit=fracao.bit_length()-1
        mantissa=fracao<<(63-bit)
        expoente=16383-1074+bit
    else:
        mantissa=0
    return (mantissa,expoente|(sinal<<15))


class TecnologiaEconomiaS1:
    def __init__(self,memoria,*,externo=None):
        self.m,self.externo=memoria,externo

    def chamar(self,nome,regs):
        if nome not in ROTINAS:
            raise KeyError(nome)
        r=exigir(nome,ROTINAS[nome],regs)
        saida=getattr(self,'_'+nome)(r)
        if 'ESP' in r:saida['ESP']=(r['ESP']+4)&M32
        return saida

    def _RechercheGetEtat(self,r):
        jogador=r['EAX']&255
        a=0x5080fc+16*jogador
        bits=self.m.u32(a)|(self.m.u32(a+4)<<32)
        return dict(r,EAX=jogador*16,_x87_push=double_para_x87(bits))

    @staticmethod
    def _sair(entrada,r,salvos):
        return {k:(entrada[k] if k in salvos else r[k])&M32 for k in REG7}

    def _call(self,nome,chamada,r,deslocamento):
        entrada={k:r[k]&M32 for k in REG7}
        if 'ESP' in r:entrada['ESP']=(r['ESP']-deslocamento)&M32
        if nome in ROTINAS:
            saida=self.chamar(nome,entrada)
        elif self.externo is not None:
            saida=self.externo(nome,chamada,entrada)
        else:
            raise DependenciaTecnologiaS1(nome,chamada)
        exigir(nome,chamada,saida)
        return dict(r,**{k:saida[k]&M32 for k in REG7})

    def _RechercheGetBranche(self,r):
        return dict(r,EAX=self.m.u8(PESQUISA+16*(r['EAX']&255)+4))

    def _RechercheGetNiveau(self,r):
        return dict(r,EAX=self.m.u8(PESQUISA+16*(r['EAX']&255)+(r['EDX']&65535)))

    def _RechercheGetNbInvention(self,r):
        return dict(r,EAX=self.m.u8(0x50871c+(r['EAX']&255)))

    def _InventionGetCout(self,r):
        item,branche=r['EAX']&65535,r['EDX']&65535
        return dict(r,EAX=self.m.u32(TABELA+360*branche+12*item),EDX=item)

    def _SetBatimentRecrutable(self,r):
        p,t=r['EAX']&255,r['EDX']&255
        self.m.u8(ESTRUTURAS_REALIZAVEIS+22*p+t,1)
        return dict(r,EAX=11*p,EDX=t)

    def _SetTroupeRecrutable(self,r):
        p,t=r['EAX']&255,r['EDX']&255
        self.m.u8(UNIDADES_REALIZAVEIS+26*p+t,1)
        return dict(r,EAX=13*p,EDX=t)

    def _TypeEnginEstRealisable(self,r):
        p,t=r['EAX']&255,r['EDX']&255
        return dict(r,EAX=self.m.u8(UNIDADES_REALIZAVEIS+26*p+t),EDX=26*p)

    def _TypeBatimentEstRealisable(self,r):
        p,t=r['EAX']&255,r['EDX']&255
        if self.m.u8(0x4e0730) and t in (8,12):return dict(r,EAX=0)
        return dict(r,EAX=self.m.u8(ESTRUTURAS_REALIZAVEIS+22*p+t),EDX=22*p)

    def _SortilegeResetTechnologie(self,r):
        # Reuse the established eight interleaved columns, not broad zero fills.
        for i in range(5):
            for a in (0x508f30,0x508f44,0x508f35,0x508f49,0x508f3a,0x508f4e,0x508f3f,0x508f53):
                self.m.u8(a+i,0)
        return dict(r,EAX=5)

    def _TechnologieReset(self,r):
        original=dict(r)
        for p in range(4):
            for t in range(26):self.m.u8(UNIDADES_REALIZAVEIS+26*p+t,0)
        for p in range(4):
            for t in range(22):self.m.u8(ESTRUTURAS_REALIZAVEIS+22*p+t,0)
        r.update(EAX=22,EBX=66,ECX=4,EDX=4)
        r=self._call('SortilegeResetTechnologie',0x46b576,r,16)
        return self._sair(original,r,('EBX','ECX','EDX'))

    def _BonusReset(self,r):
        from bonus_unidades import _CAMPOS_RESET
        for p in range(4):
            for t in range(26):
                a=0x4dfba0+468*p+18*t
                for o,n in _CAMPOS_RESET:getattr(self.m,f'u{8*n}')(a+o,0)
        return dict(r,EAX=4)

    def _bag_inline(self,a,capacidade):
        # EnginSetTechnologie's inline reset: +0x60..+0x65 remain intact.
        for o in (0x66,4,2,0):self.m.u16(a+o,0)
        for i in range(30):
            self.m.u16(a+6+2*i,0);self.m.u8(a+0x42+i,0)
        self.m.u16(a+2,capacidade)

    def _prend(self,a,etiqueta,valor):
        n=self.m.u16(a)
        if n>=30:raise ForaDoDominioTecnologiaS1('BagPrend',0x447483,'protected Bag count exceeds 29')
        self.m.u16(a+0x66,self.m.u16(a+0x66)+1)
        self.m.u8(a+0x42+n,etiqueta)
        self.m.u16(a+6+2*n,valor)
        self.m.u16(a,n+1)
        return n

    def _EnginSetTechnologie(self,r):
        p=r['EAX']&255
        if p>=4:raise ForaDoDominioTecnologiaS1('EnginSetTechnologie',0x4411f9,'protected player is 0..3')
        pool=self.m.u32(self.m.u32(0x4e19b8)+4*p)
        self._bag_inline(pool+7*104,22)
        for t in range(22):
            q=self._TypeBatimentEstRealisable(dict(r,EAX=p,EDX=t))
            if q['EAX']&255 and t!=20:self._prend(pool+7*104,3,t)
        self._bag_inline(pool+14*104,1);self._prend(pool+14*104,7,6)
        self._bag_inline(pool+8*104,4)
        for t in range(4):self._prend(pool+8*104,2,t)
        return dict(r,EAX=(pool+8*104)&M32)

    def _batiment_set_technologie(self,r):
        # Existing cave/recruitment implementation: preserve its arithmetic
        # and BagInit implementation, supplying the BagPrend primitive here.
        from caverna_recrutamento import CavernaRecrutamento
        def bag_prend(nome,chamada,args):
            if nome!='BagPrend':raise DependenciaTecnologiaS1(nome,chamada)
            n=self._prend(args['EAX'],args['EDX']&255,args['EBX']&65535)
            # Caverna's leaf composer consumes precisely these three outputs;
            # its own epilogue restores all other entry registers.
            return dict(EAX=args['EAX'],EDX=n,EBX=n)
        return CavernaRecrutamento(self.m,externo=bag_prend).chamar('BatimentSetTechnologie',r)

    def _BatimentInitTechnologie(self,r):
        original=dict(r)
        for i in range(1000):
            a=ESTRUTURAS+276*i
            if not self.m.u8(a+5):continue
            t=self.m.u8(a+8)
            if t==3:
                p=self.m.u8(a+4)
                if p<4:
                    indicateur=0x4dfb2c+6*p
                    n=self.m.u16(indicateur)
                    if n:
                        base=0x4e2ea8+32*p
                        food=(self.m.u16(base+10)-self.m.u16(base+8))&65535
                        stone=(self.m.u16(base+18)-self.m.u16(base+16))&65535
                        q=((food+stone)&65535)//n
                        if q>65535:raise OverflowError('BatimentInitTechnologie DIV BX overflow')
                        cap=self.m.u16(indicateur+2)
                        if not cap:raise ZeroDivisionError('BatimentInitTechnologie IDIV at 0x41ce92')
                        self.m.u8(indicateur+4,(q*7)//cap)
            r.update(EAX=self.m.u8(a+4),EDX=t,ESI=a,EDI=i)
            r=self._batiment_set_technologie(r)
        return self._sair(original,dict(r,EAX=1000),REG7[1:])

    def _InventionSetEffet(self,r):
        original=dict(r)
        p,item,branche=r['EAX']&255,r['EDX'],r['EBX']
        offset=360*(branche&65535)+12*(item&65535)
        a=TABELA+offset
        kind=self.m.u8(a+6)
        valide=kind!=255 and self.m.u8(a+4)!=100
        if not valide and r['ECX']&255==1 and p==self.m.u8(0x508041):
            raise ForaDoDominioTecnologiaS1('InventionSetEffet',0x471017,'MessageBoxSet notification path')
        kind=self.m.u8(a+6)
        if kind!=0:
            raise ForaDoDominioTecnologiaS1('InventionSetEffet',0x471054,'only unlock effects (kind 0) are validated')
        sous_type=self.m.u8(a+7)
        if sous_type not in (1,3):
            raise ForaDoDominioTecnologiaS1('InventionSetEffet',0x471232,'only troop/building unlocks are validated')
        cible=self.m.u8(a+8)
        r.update(ESI=item,EDI=branche)
        if sous_type==3:
            if cible in (13,16,18,20):
                raise ForaDoDominioTecnologiaS1('InventionSetEffet',0x471126,'unlock also rebuilds special recruitment')
            r.update(EAX=p,EDX=cible,ECX=p,EBX=offset)
            r=self._call('SetBatimentRecrutable',0x471135,r,16)
            r['EAX']=r['ECX'];r=self._call('EnginSetTechnologie',0x47113c,r,16)
            r['EAX']=(r['EAX']&0xffff0000)|(cible<<8)|cible
        else:
            if cible in (11,13,15):
                raise ForaDoDominioTecnologiaS1('InventionSetEffet',0x471188,'unlock also enables building 5')
            r.update(EAX=p,EDX=cible,EBX=3*(item&65535))
            r=self._call('SetTroupeRecrutable',0x4711be,r,16)
            r=self._call('BatimentInitTechnologie',0x4711c3,r,16)
            r.update(EAX=(cible<<8)|cible,EDX=360*(branche&65535),EBX=3*(item&65535))
        return self._sair(original,r,('ESI','EDI'))

    def _RechercheCalculNew(self,r):
        original=dict(r)
        r=self._call('TechnologieReset',0x471518,r,36)
        r['EDX']=0;r=self._call('BonusReset',0x47151f,r,36)
        for p in range(4):
            for o in range(0,16,4):self.m.u32(PESQUISA+16*p+o,self.m.u32(GUARDADA+16*p+o))
        r.update(ECX=4,EBX=0,EBP=0)
        for p in range(4):
            for branche in range(4):
                item=0
                while item<self.m.u8(PESQUISA+16*p+branche):
                    if item>=30:raise ForaDoDominioTecnologiaS1('RechercheCalculNew',0x4715a7,'stored level exceeds 30 entries')
                    a=TABELA+360*branche+12*item
                    if self.m.u8(a+6)!=255:
                        r.update(EAX=p,EDX=item,EBX=branche,ECX=0,ESI=item,EDI=branche,EBP=0)
                        r=self._call('InventionSetEffet',0x4715df,r,36)
                    item+=1
        for p in range(4):
            self.m.u8(0x50871c+p,0)
            r.update(EDX=0,EDI=0)
            for branche in range(4):
                ebp=PESQUISA+16*p
                r.update(EDI=branche,EBP=ebp)
                for item in range(30):
                    offset=360*branche+12*item
                    kind=self.m.u8(TABELA+offset+6)
                    r.update(EAX=kind,ESI=offset)
                    if kind==255:break
                    r['EDX']=self.m.u8(TABELA+offset+5)
                    r=self._call('MissionGetNum',0x47165f,r,36)
                    if r['EDX']>r['EAX']&65535:break
                    niveau=self.m.u8(ebp+branche)
                    r.update(EAX=branche,EDX=niveau,ESI=item)
                    if niveau>item:continue
                    kind=self.m.u8(TABELA+offset+6)
                    r.update(EAX=kind,ESI=offset)
                    if kind==255:continue
                    r['EDX']=self.m.u8(TABELA+offset+4)
                    r=self._call('MissionGetNum',0x4716b0,r,36)
                    if r['EDX']<=r['EAX']&65535:
                        r.update(EAX=p,EDX=item,EBX=branche,ECX=1,ESI=branche)
                        r=self._call('InventionSetEffet',0x4716df,r,36)
                        r['EAX']=(r['EAX']&0xffffff00)|((item+1)&255)
                        self.m.u8(ebp+branche,r['EAX'])
                else:
                    raise ForaDoDominioTecnologiaS1('RechercheCalculNew',0x471632,
                                                  'branch exceeds the protected 30-entry table')
        return self._sair(original,dict(r,EAX=4),REG7[1:])

    def _IaRechercheAjuste(self,r):
        original=dict(r)
        r.update(EAX=0,EDX=1)
        r=self._call('RechercheGetNbInvention',0x47fa98,r,32)
        r['EBP']=r['EAX']&255
        for p in range(1,4):
            r.update(EAX=p,EDX=p,EBX=0)
            r=self._call('PlayerGetType',0x47fabe,r,32)
            r['EBX']=r['EAX']&255
            if r['EBX']!=2:continue
            r['EBX']=0;r=self._call('MissionGetNum',0x47facc,r,32)
            r['EBX']=r['EAX']&65535
            if r['EBX']>=3:
                raise ForaDoDominioTecnologiaS1('IaRechercheAjuste',0x47fad9,'AI research catch-up from mission 3')
        return self._sair(original,r,REG7[1:])


def provedor_tecnologia_economia_s1(tecnologia,outros=None):
    """Strict exact-register external provider; x87 push metadata is preserved."""
    def externo(nome,chamada,regs):
        if nome not in ROTINAS:
            if outros is None:raise DependenciaTecnologiaS1(nome,chamada)
            return outros(nome,chamada,regs)
        r=exigir(nome,chamada,regs)
        if regs.get('_pilha'):raise ValueError(f'{nome} takes no pushed words')
        saida=tecnologia.chamar(nome,r)
        return {k:v for k,v in saida.items() if k!='ESP'}
    return externo
