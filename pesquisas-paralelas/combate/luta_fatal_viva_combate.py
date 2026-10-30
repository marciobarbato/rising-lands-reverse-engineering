"""Live composition of Combat with synchronous raid-message/diplomacy effects."""
from abi_luta_fatal_combate import DependenciaLutaFatal, registradores_exigidos, unidade, assinado, M32
from entrada_estruturas import ArgumentoNaoPassado
from combate_raid_vivo import CombateRaidVivo, DEPENDENCIAS_RAID
from diplomacia_luta_combate import DiplomaciaLuta, ADDRESSES as DIPLOMACY
from mensagens_luta_combate import MensagensLuta
from movimento import direcao_entre_celulas, celula_vizinha
from ciclo_morte_luta_combate import CicloMorteLuta, ADDRESSES as LIFECYCLE
from recontagem_luta_combate import recontar_registradores
from etapa_viva_luta_combate import etapa_viva_luta
from refugio_luta_combate import buscar_refugio, refugio_registradores
from chamadas_quadro_core import terreno_esta_descoberto
from selecao_ordens import chamar_som


class LutaFatalViva:
    def __init__(self, memoria, *, perfil=None, som=None, externo=None, etapa=None):
        self.m,self.perfil,self.som,self.externo,self.etapa=memoria,perfil,som,externo,etapa
        self.ultimo_som=None;self.ultima_diplomacia=None
        self.diplomacia=DiplomaciaLuta(memoria,perfil=perfil)
        self.combate=CombateRaidVivo(memoria,consulta=self.consulta,efeito=self.efeito,som=self._som if som is not None else None)
        self.mensagens=MensagensLuta(memoria,self.combate)
        self.ciclo=CicloMorteLuta(memoria,self.combate,self.mensagens,som=self._som if som is not None else None)

    def _som(self,nome,regs,pilha,*,chamada=None):
        result=chamar_som(self.som,nome,regs,pilha,chamada)
        # Original unopened-library prefix: PostSound dispatches through the
        # fixed private object, returns0, and leaves EBX=object, ECX=flags,
        # EDX=0. Audio's provider checks that exact inherited private image.
        raw=None
        if nome=='PlaySnd_PostSound' and getattr(self.som,'domain',None)=='unopened-display':
            if result!=0: raise ValueError('Unopened original PostSound must return0')
            raw=dict(EAX=0,EBX=0x522000,ECX=regs['ECX']&M32,EDX=0)
        self.ultimo_som=dict(name=nome,entry=dict(regs),pilha=list(pilha),result=result,raw=raw)
        return result

    def consulta(self, nome, args):
        if nome=='CalculDirection': return direcao_entre_celulas(*args)
        if nome=='CalculDirCase': return celula_vizinha(*args,self.m.u16(0x497168),self.m.u16(0x49716a))
        if nome=='ChercheBatimentProximiteCaveOuSanctuaire': return buscar_refugio(self.m,*args)
        return self._externo(nome,args)

    def _externo(self,nome,args):
        if self.externo is None:
            raise DependenciaLutaFatal(nome,DEPENDENCIAS_RAID[nome],args)
        return self.externo(nome,tuple(args))

    def efeito(self,nome,args):
        if nome in DIPLOMACY:
            result=self.diplomacia.efeito(nome,args)
            self.ultima_diplomacia=dict(name=nome,arguments=tuple(args),result=result)
            return result
        if nome=='iagUnitSendMessage': return self.mensagens.mensagem(*args)
        if nome=='SetDyingEngin': return self.ciclo.dying(*args)
        if nome=='EnginSetLevelExperience': return self.ciclo.level(*args)
        if nome=='RetireEngin': return self.ciclo.core.retire_engin({'EAX':args[0]})
        return self._externo(nome,args)

    def _dano_registradores(self,regs):
        m=self.m;out=registradores_exigidos('EnginInfligeDegat',0x4502f0,regs)
        victim=out['EAX']&65535;source=out['EBX']&65535;mode=out['EDX']&255
        if mode!=1: raise DependenciaLutaFatal('EnginInfligeDegat raw mode',0x450588,(victim,mode,source))
        record=unidade(m,victim);before=m.u16(record+0x9a)
        self._raw_presentation_domain(record,0x4502f0)
        self.ultimo_som=self.ultima_diplomacia=None
        self.combate.infligir_unidade(victim,mode,source,out['ECX']&255)
        if self.ultima_diplomacia is not None and self.ultima_diplomacia['name']=='MAJSympathie':
            last=self.ultima_diplomacia
            out.update(last['result']);out['ECX']=last['arguments'][1]&255
        else:
            damage=assinado((before-m.u16(record+0x9a))&65535,16)
            sound=self.ultimo_som
            if sound is None or sound['raw'] is None:
                raise RuntimeError('Prevalidated nonlethal presentation prefix did not execute')
            out.update(EAX=damage&M32,EDX=(before-damage)&M32,
                       EBX=sound['raw']['EBX'],ECX=sound['raw']['ECX'])
        return out

    def _raw_presentation_domain(self,record,entry):
        m=self.m
        if getattr(self.som,'domain',None)!='unopened-display' or m.u32(record+0x104)!=M32 or not (
            terreno_esta_descoberto(m,m.u16(record+8),m.u8(0x508041))['EAX']&255):
            raise DependenciaLutaFatal('Raw fight return outside visible/unopened domain',entry,(record,))

    def _impact_registradores(self,regs,pilha):
        out=registradores_exigidos('InfligeDegat',0x450874,regs)
        if pilha is None or len(pilha)!=1:
            raise ArgumentoNaoPassado('InfligeDegat',0x450874,('pilha[0]',))
        m=self.m;cell=out['EAX']&65535;mode=out['EDX']&255;source=out['EBX']&65535;flag=pilha[0]&255
        if mode!=1: raise DependenciaLutaFatal('InfligeDegat raw non-unit source',0x4508af,(cell,mode,source))
        if not flag and self.combate._query('ChercheIndiceBatiment',(cell,))!=65535:
            raise DependenciaLutaFatal('InfligeDegat raw structure target',0x4508af,(cell,mode,source))
        victim=self.combate._query('ChercheIndiceEnginCible',(cell,65535,flag))
        if victim==65535: raise DependenciaLutaFatal('InfligeDegat raw empty impact',0x450a9d,(cell,))
        self._raw_presentation_domain(unidade(m,victim),0x450874)
        previous_alert=m.u32(0x4e19c0)
        self.ultimo_som=self.ultima_diplomacia=None
        self.combate.infligir(cell,mode,source,out['ECX']&255,flag)
        last=self.ultima_diplomacia
        if last is None or last['name']!='PlayerAAttaqueSet':
            raise ValueError('Expected original mode1 diplomacy suffix')
        source_owner=last['arguments'][0]&255
        record=unidade(m,victim);victim_owner=m.u8(record);offset=276*victim
        out.update(EAX=record,EBX=offset,ECX=source_owner,EDX=victim_owner)
        if victim_owner==source_owner: return out
        out.update(EBX=record,ECX=m.u8(0x508041))
        if victim_owner!=out['ECX']: return out
        now=m.u32(0x508f7c)
        if previous_alert<=now and now-previous_alert<200:
            out.update(EAX=now-previous_alert,ECX=now)
            return out
        sound=self.ultimo_som
        if sound is None or sound['raw'] is None or sound['entry'].get('EBX')!=0x496ac8:
            raise DependenciaLutaFatal('InfligeDegat raw alert sound registers',0x48aa79,(victim,))
        out.update(sound['raw'])
        return out

    def chamar(self,nome,regs,*,chamada=None,pilha=None):
        if nome=='KERNEL32.GetPrivateProfileStringA':
            registradores_exigidos(nome,0x5231b0 if chamada is None else chamada,regs)
            if self.perfil is None or not hasattr(self.perfil,'importacao'):
                raise DependenciaLutaFatal(nome,0x5231b0,())
            return self.perfil.importacao(self.m,regs,pilha,chamada=0x5231b0 if chamada is None else chamada)
        if nome in DIPLOMACY: return self.diplomacia.chamar(nome,regs,chamada=chamada)
        if nome=='iagUnitSendMessage': return self.mensagens.chamar(nome,regs,chamada=chamada)
        if nome in LIFECYCLE: return self.ciclo.chamar(nome,regs,chamada=chamada)
        if nome=='EnginNextEtape': return self.ciclo.chamar('EnginNextEtape:state4',regs,chamada=chamada)
        if nome=='EnginInfligeDegat': return self._dano_registradores(regs)
        if nome=='InfligeDegat': return self._impact_registradores(regs,pilha)
        if nome=='ChercheBatimentProximiteCaveOuSanctuaire':
            return refugio_registradores(self.m,regs,chamada=0x4539f3 if chamada is None else chamada)
        if nome=='CalculEnginNextEtape':
            def body(unit):
                if self.m.u8(self.m.u32(0x4e19a0)+276*unit+2) in (0,4): return self.ciclo.corpse(unit)
                return self.etapa(unit) if self.etapa is not None else etapa_viva_luta(self,unit)
            return recontar_registradores(self.m,body,regs,chamada=0x456db5 if chamada is None else chamada)
        raise KeyError(nome)

    def provedores(self):
        names=(*DIPLOMACY,*LIFECYCLE,'iagUnitSendMessage','EnginNextEtape','CalculEnginNextEtape','EnginInfligeDegat','InfligeDegat','KERNEL32.GetPrivateProfileStringA','ChercheBatimentProximiteCaveOuSanctuaire')
        return {n:(lambda regs,pilha=None,name=n:self.chamar(name,regs,pilha=pilha)) for n in names}
