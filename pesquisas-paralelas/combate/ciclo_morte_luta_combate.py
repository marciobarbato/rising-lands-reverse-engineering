"""Ordinary live unit death, corpse animation/removal and kill-level effects.

Core owns selection, collision, minimap and light mutations. This composition
preserves their original call order; no Core file or frozen evidence is edited.
The raw facade requires all seven registers. Private semantic calls pass only
the input registers the existing Core methods actually read; discarded saved
register results are never synthesized or exposed as known values.
"""
from abi_luta_fatal_combate import M32, DependenciaLutaFatal, registradores_exigidos, unidade
from chamadas_quadro_core import terreno_esta_descoberto
from entrada_estruturas import EntradaEstruturas
from experiencia_unidades import TIPOS_F7
from incursao_core import definir_minimapa
from selecao_ordens import chamar_som

ADDRESSES={'SetDyingEngin':0x444938,'EnginSetLevelExperience':0x44fb20,
           'EnginNextEtape:state4':0x45442c,'RetireEngin':0x457058}


class CicloMorteLuta:
    def __init__(self, memoria, combate, mensagens, *, som=None):
        self.m,self.combate,self.mensagens,self.som=memoria,combate,mensagens,som
        self.core=EntradaEstruturas(memoria,som=som,bonus=combate.bonus.consultar)

    def _release(self, unit):
        m=self.m
        if m.u16(0x496304)==unit:
            m.u8(0x4e0f36,0);m.u32(0x4e0f3c,0);m.u8(0x4e0f37,0);m.u16(0x496304,65535)

    def _deselect(self, unit):
        self.combate.ordens.deselection_engin({'EAX':unit,'EDX':0})

    def _collision_off(self, unit):
        m=self.m;r=unidade(m,unit);cell=m.u16(r+8)
        self.combate.mundo.ocupar(unit,cell,False)
        if cell!=m.u16(r+0x7c): self.combate.mundo.ocupar(unit,m.u16(r+0x7c),False)

    def _audio_stop(self, reference):
        if self.som is None: raise DependenciaLutaFatal('PlaySnd_StopSound',0x48aac0,(reference,))
        chamar_som(self.som,'PlaySnd_StopSound',dict(EAX=reference),[],0x4449c3)

    def dying(self, unit):
        m=self.m;unit&=65535;r=unidade(m,unit)
        if m.u8(r+0xdc)&4:
            raise DependenciaLutaFatal('SetDyingEngin spell/special branch',0x444c7e,(unit,))
        if m.u8(r+2) in (0,4): return 0
        self.mensagens.mensagem(unit,0x44,0)
        self._audio_stop(r+0x104)
        if terreno_esta_descoberto(m,m.u16(r+8),m.u8(0x508041))['EAX']&255:
            volume=self.combate._query('EnginGetVolume',(unit,))
            m.u8(r+0xf9,0)
            if m.u32(r+0x104)==M32:
                self.combate._efeito('PlaySnd_PostSound',(0x50,(m.u8(r+1)<<16)|0x500,0,volume,r+0x104),chamada=0x444a1b)
        if m.u8(r+2) not in (0,4):
            m.u8(r+2,4);self._release(unit)
        if m.u16(r+10): raise DependenciaLutaFatal('EnginRetire',0x443dfc,(unit,0))
        # The original repeats SetEtat after emptying Bag; state4 takes its guard.
        m.u8(r+0xa4,0);m.u16(r+0xc2,0)
        self._deselect(unit);self._collision_off(unit)
        if 11<=m.u8(r+1)<=17:
            raise DependenciaLutaFatal('SetDyingEngin vehicle explosion',0x444bd8,(unit,))
        return m.u32(0x4e19a0)&0xffffff00

    def level(self, unit, edx):
        m=self.m;unit&=65535;r=unidade(m,unit);level=edx&255
        out=dict(EAX=level,EDX=edx&M32)
        if level>=5: return out
        m.u8(r+0xaf,(m.u8(r+0xaf)&31)|((level<<5)&255))
        kind=m.u8(r+1)
        if kind>=26: raise ValueError('Protected kill level requires unit type0..25')
        if level==0: return out
        if level==1 and kind in TIPOS_F7:
            m.u8(r+0xf7,1);out['EAX']=(m.u32(0x4e19a0)&0xffffff00)|1;return out
        if level in (1,4):
            value=m.u16(0x4965dc+50*kind)
            if level==4 and kind not in TIPOS_F7: value*=2
            quotient,remainder=divmod(value,100)
            m.u8(r+0xf8,quotient)
            return dict(EAX=quotient,EDX=remainder)
        if level==2:
            m.u8(r+0xf6,1);return out
        if not m.u8(r+0x72):
            m.u8(r+0xf5,1);return out
        self.core.retire_engin({'EAX':unit})
        m.u8(r+0xf5,1)
        self.combate.mundo.ocupar(unit,m.u16(r+8),True)
        m.u8(r+0x72,1)
        owner=m.u8(r);cell=m.u16(r+8)
        if owner not in (200,4):
            self.core.decouvre_terrain(dict(EAX=cell,EDX=m.u8(r+0xbb)+m.u8(r+0xf5)+2,EBX=owner))
            self.core.illumine_terrain(dict(EAX=cell,EDX=m.u8(r+0xbb)+m.u8(r+0xf5),EBX=owner))
        result=definir_minimapa(m,owner,4,cell)
        return dict(EAX=result['EAX'],EDX=result['EDX'])

    def corpse(self, unit, *, preludio=True):
        """Full EnginNextEtape entry restricted to inactive/ordinary dying units."""
        m=self.m;unit&=65535;r=unidade(m,unit);status=m.u8(r+2)
        if status not in (0,4): raise DependenciaLutaFatal('EnginNextEtape live state',0x4544cd,(unit,status))
        if not status: return 0
        if preludio:
            if m.u32(r+0x104)!=M32:
                raise DependenciaLutaFatal('PlaySnd_PostVolume',0x48aacf,(r+0x104,))
            m.u8(r+0xf9,0)
        if 11<=m.u8(r+1)<=17 or m.u8(r+0xdc)&4:
            raise DependenciaLutaFatal('EnginNextEtape special corpse',0x456b2f,(unit,))
        if not m.u8(r+0xa4): self._deselect(unit);self._collision_off(unit)
        count=m.u8(r+0xdb);animation=m.u8(r+0xa4)
        if animation!=count-1:
            if not count: raise ZeroDivisionError('Original corpse animation IDIV by zero at0x456a71')
            m.u8(r+0xa4,(animation+1)%count)
        timer=(m.u16(r+0xc2)+1)&65535;m.u16(r+0xc2,timer)
        if timer<330: return timer
        self._deselect(unit)
        if m.u16(r+10): raise DependenciaLutaFatal('EnginRetire',0x443dfc,(unit,0))
        result=self.core.retire_engin({'EAX':unit})['EAX']
        m.u16(r+0x9a,0);m.u8(r+2,0)
        return result

    def corpo_estado4(self, unit):
        """Typed branch0x456ae5 after AI/runtime has executed the entry prelude."""
        return self.corpse(unit,preludio=False)

    def chamar(self,nome,regs,*,chamada=None):
        out=registradores_exigidos(nome,ADDRESSES[nome] if chamada is None else chamada,regs)
        if nome=='SetDyingEngin': out['EAX']=self.dying(out['EAX'])
        elif nome=='EnginSetLevelExperience': out.update(self.level(out['EAX'],out['EDX']))
        elif nome=='EnginNextEtape:state4': out['EAX']=self.corpse(out['EAX'])
        else: out=self.core.chamar('RetireEngin',out)
        return out
