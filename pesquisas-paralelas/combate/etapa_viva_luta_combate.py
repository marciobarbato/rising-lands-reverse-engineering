"""Typed per-unit composition for ordinary raid fights and the recount proof.

This closes the reload advance and state1/24 calls around Combat's existing
attack API, retaining the AI prelude order and Core fatigue/collision/movement.
It returns no invented path-dependent EAX. The count loop consumes no unit
return register; its separately published raw ABI is exact. Work/construction,
special unit/spell and starvation bodies remain original named dependencies.
"""
from abi_luta_fatal_combate import DependenciaLutaFatal, unidade, assinado
from chamadas_quadro_core import calcular_fadiga
from incursao_core import unidade_em_arret
from proxima_etapa_quadro import TIPOS_VARREDURA
from quadro_economia import estado_parado_unidade


def etapa_viva_luta(live, unit):
    m=live.m;unit&=65535;r=unidade(m,unit)
    status=m.u8(r+2)
    if status in (0,4): return live.ciclo.corpse(unit)
    owner,kind=m.u8(r),m.u8(r+1)
    if m.u32(r+0x104)!=0xffffffff:
        raise DependenciaLutaFatal('PlaySnd_PostVolume',0x48aacf,(r+0x104,))
    m.u8(r+0xf9,0)
    if kind>=11: raise DependenciaLutaFatal('EnginNextEtape special live type',0x4544d7,(unit,kind))
    current_type=m.u8(r+1)
    maximum=m.u16(0x4965de+50*current_type)
    bonus=live.combate.bonus.consultar(m.u8(r),current_type,3,ecx=r)&65535
    if m.u16(r+0x102)<assinado((maximum-bonus)&0xffffffff):
        m.u16(r+0x102,m.u16(r+0x102)+1)
    if m.u8(r+2)!=14 and (m.u32(0x508f7c)+unit)&31==0 and owner!=200 and m.u8(r+1) in TIPOS_VARREDURA:
        player_type=live.combate._query('PlayerGetType',(owner,))&255
        if m.u8(r+2) not in (1,19):
            target=live.combate.encontrar_alvo(unit)
            if target!=65535:
                if player_type==2: live.mensagens.mensagem(unit,0x49,target)
                elif m.u8(r+2)==7: live.combate.definir_ataque(unit,1,target)
    if m.u8(r+0xdc)&4: raise DependenciaLutaFatal('EnginNextEtape spell timer',0x454811,(unit,))
    calcular_fadiga(m,unit,lambda a,b,c:live.combate.bonus.consultar(a,b,c))
    if m.u8(r+2) in (0,4): return
    if m.u16(r+4)!=4 and m.u8(r+0x72) and not m.u16(r+4) and not m.u8(r+0x86) and not m.u8(r+0x87):
        raise DependenciaLutaFatal('EnginNextEtape hunger reaction',0x45496e,(unit,))
    if m.u8(r+0x72) and m.u8(r+2)!=4: live.combate.mundo.ocupar(unit,m.u16(r+8),True)
    if m.u8(r+0xdc)&2: raise DependenciaLutaFatal('EnginNextEtape bit1',0x454ba5,(unit,))
    if m.u8(r+0xdc)&8: raise DependenciaLutaFatal('EnginNextEtape bit3',0x454c0e,(unit,))
    status=m.u8(r+2)
    if status in (1,24): return live.combate.ramo(unit)
    if status==7: return estado_parado_unidade(m,unit)
    if status==14 or status==0: return
    if status==4: return live.ciclo.corpse(unit)
    if status==2:
        if m.u16(r+0x7e)!=m.u16(r+8): return live.combate.mundo.deslocar(unit)
        if m.u8(r+0x91)!=m.u8(r+0x90):
            raise DependenciaLutaFatal('EnginNextEtape arrival facing',0x455a6f,(unit,))
        if not unidade_em_arret(m,unit)['EAX']&255:
            raise DependenciaLutaFatal('EnginNextEtape arrival animation',0x456408,(unit,))
        m.u8(r+2,7);live.ciclo._release(unit);return
    raise DependenciaLutaFatal(f'EnginNextEtape state{status}',0x456c1c,(unit,))
