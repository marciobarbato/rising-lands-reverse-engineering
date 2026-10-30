"""Exact checkpoint/register comparisons for the original fatal-fight matrix.

Sequential corpse inputs keep the same Python buffers/providers: no native
state is copied back into a translated chain. A reset occurs only where the
original matrix declares state_ref=contact. Original fault cases are outside
the protected domain and listed separately, never counted as equal returns.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from bancada_luta_fatal_combate import estado_contato, BancadaLutaFatal, json_bytes
from delta_estado_missao import aplicar, resumo
from diplomacia_luta_combate import DiplomaciaLuta, PerfilTextoLuta, ADDRESSES
from capturar_carga_missao_original import entradas
from validar_combate_raid import memory, serialize, write_state
from abi_luta_fatal_combate import REG7
from luta_fatal_viva_combate import LutaFatalViva

HERE=Path(__file__).resolve().parent
CAPTURE=HERE/'evidencias/captura-folhas-luta-fatal-original-v1.json'


def factory(m):
    from provedor_pedidos_m3_audio import SoundRequestProvider, LiveAudioMemory
    profile=PerfilTextoLuta(entradas(0xa7,0x123456))
    sound=SoundRequestProvider(LiveAudioMemory(m),domain='unopened-display')
    return LutaFatalViva(m,perfil=profile,som=sound)


def compare(capture=CAPTURE, *, native=False, routines=None):
    captured=json.loads(Path(capture).read_bytes())
    state,pin=estado_contato()
    if pin!=captured['provenance']: raise ValueError('Contact source provenance mismatch')
    selected=set((*ADDRESSES,'iagUnitSendMessage','SetDyingEngin','EnginSetLevelExperience','EnginNextEtape','CalculEnginNextEtape','EnginInfligeDegat','InfligeDegat','ChercheBatimentProximiteCaveOuSanctuaire') if routines is None else routines)
    b=BancadaLutaFatal(state) if native else None
    previous_name=None; previous_native=None; previous_python=None
    output=[]; outside=[]; live=None; m=None; blocks=None
    for case in captured['cases']:
        if case['state_ref']=='contact':
            before=write_state(state,case['declared_writes'])
            chained=False
        else:
            if previous_name!=case['state_ref']: raise ValueError('Original sequential parent mismatch')
            before=write_state(previous_native,case['declared_writes'])
            chained=previous_python==case['state_ref']
        if case['routine'] not in selected:
            # Reconstruct only chains needed by a selected routine, without
            # running any unselected translation or pretending it succeeded.
            after=aplicar(before,case['delta'],case['case'])
            previous_name,previous_native=case['case'],after
            previous_python=None
            continue
        if resumo(before)!=case['state_before']: raise ValueError('Original input hash mismatch '+case['case'])
        after=aplicar(before,case['delta'],case['case'])
        if resumo(after)!=case['state_after']: raise ValueError('Original output hash mismatch '+case['case'])
        if case['fault'] or case['limit'] or not case['reached_return']:
            outside.append(dict(case=case['case'],fault=case['fault'],limit=case['limit'],stop=case['stop']))
            previous_name,previous_native=case['case'],after;previous_python=None
            continue
        if not chained:
            m,blocks=memory(before); live=factory(m)
        else:
            for address,data in case['declared_writes']:
                data=bytes.fromhex(data);m.vista(int(address,16),len(data))[:]=data
            if resumo(serialize(blocks))!=case['state_before']: raise ValueError('Python chain input diverged '+case['case'])
        regs={k:int(v,16) for k,v in case['entry_registers'].items() if k in REG7}
        profile=getattr(live,'perfil',None)
        p0=len(profile.chamadas) if profile is not None else 0
        actual=live.chamar(case['routine'],regs,pilha=case['stack_words'])
        differences={k:[hex(actual[k]),case['exit_registers'][k]] for k in REG7 if actual[k]!=int(case['exit_registers'][k],16)}
        state_equal=serialize(blocks)==after
        profile_equal=True
        if profile is not None:
            calls=json.loads(json.dumps(profile.chamadas[p0:],default=json_bytes))
            profile_equal=calls==case['profile_calls']
        native_errors=[]
        if native:
            b.restore(before)
            fresh,_,fresh_state=b.call(case['routine'],regs,words=case['stack_words'])
            for key in ('exit_registers','state_after','stores','profile_calls'):
                value=json.loads(json.dumps(fresh[key],default=json_bytes))
                if value!=case[key]: native_errors.append(key)
            if fresh_state!=after or fresh['fault'] or not fresh['reached_return']: native_errors.append('completion/state')
        output.append(dict(case=case['case'],routine=case['routine'],register_differences=differences,
                           whole_state_equal=state_equal,profile_calls_equal=profile_equal,
                           python_chain=chained,native_errors=native_errors))
        previous_name,previous_native,previous_python=case['case'],after,case['case']
    return dict(schema='rising-lands/combat-fatal-differential/1',native=native,
                capture_sha256=hashlib.sha256(Path(capture).read_bytes()).hexdigest(),
                summary=dict(cases=len(output),mismatches=sum(bool(c['register_differences'] or not c['whole_state_equal'] or not c['profile_calls_equal'] or c['native_errors']) for c in output),
                             routines=dict(Counter(c['routine'] for c in output)),outside_protected_domain=len(outside)),
                outside_protected_domain=outside,cases=output)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular',action='store_true');p.add_argument('--capture',type=Path,default=CAPTURE)
    p.add_argument('--routines',help='Comma-separated original names');p.add_argument('--output',type=Path)
    a=p.parse_args();report=compare(a.capture,native=a.emular,routines=a.routines.split(',') if a.routines else None)
    if a.output:
        a.output.parent.mkdir(exist_ok=True,parents=True);a.output.write_text(json.dumps(report,indent=1)+'\n')
    print(json.dumps(report['summary']))
    for c in report['cases']:
        if c['register_differences'] or not c['whole_state_equal'] or not c['profile_calls_equal'] or c['native_errors']: print(json.dumps(c))
    raise SystemExit(bool(report['summary']['mismatches']))
