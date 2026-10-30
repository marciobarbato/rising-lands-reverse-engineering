"""Compare live fight emitters with captured S1 requests and original leaves.

The Python sound callback is exactly the inherited scenario boundary: log the
request, preserve memory and return entry EAX. Native mode executes the actual
unopened sound bodies as well as every parent game body, with passive CALL
hooks, and compares whole non-stack state and consumed sound arguments/sites.
"""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import struct

from ambiente_combate_raid import ROOT
from delta_estado_missao import _decodificar, aplicar, resumo
from validar_combate_raid import memory, serialize, write_state
from validar_luta_fatal_combate import factory
from bancada_luta_fatal_combate import BancadaLutaFatal
from abi_luta_fatal_combate import REG7

HERE = Path(__file__).resolve().parent
CAPTURE = HERE/'evidencias/som-luta-s1-original-v2.json.xz'
REQUEST_REGS = {'PlaySnd_PostSound': ('EAX','EDX','EBX','ECX'), 'PlaySnd_StopSound': ('EAX',)}


def load(path=CAPTURE):
    data = json.loads(lzma.decompress(Path(path).read_bytes()))
    for case in data['cases']: case['_state_anchor'] = data['state_anchor']
    return data


def state_before(case):
    anchor = {n:(int(v['base'],16),_decodificar(v)) for n,v in case['_state_anchor'].items()}
    return aplicar(anchor,case['entry_delta'],'sound parent entry')


def request(name, regs, words, site):
    return dict(routine=name, call=hex(site),
                registers={k:hex(regs[k]) for k in REQUEST_REGS[name]}, stack_words=list(words))


def expected_requests(case):
    return [request(e['routine'],{k:int(v,16) for k,v in e['registers'].items()},
                    e['stack_words'],int(e['call'],16)) for e in case['sound_requests']]


def execute(case, *, callback=None):
    m, blocks = memory(state_before(case))
    calls = []
    def sound(name, regs, words, *, chamada):
        calls.append(request(name,regs,words,chamada))
        if callback is not None: return callback(name,regs,words,chamada=chamada)
        return regs['EAX']  # Exact declared S1 scenario boundary, no game-byte stores.
    live = factory(m)
    live.som = sound
    regs = {k:int(v,16) for k,v in case['entry_registers'].items()}
    # Explicit owner providers for the structure-hit parent cases. The typed
    # caller consumes only their semantic effects (no saved-register result).
    # Carry captured saved registers; replace exactly the three request inputs.
    from consultas_luta import ConsultasLuta
    from mensagem_cidade_ia import mensagem_cidade
    voice=ConsultasLuta(m,som=live._som)
    def provided(name,args):
        if name in ('VoixOffAsk','iagVilleSendMessage'):
            r=dict(regs,EAX=args[0],EDX=args[1],EBX=args[2])
            if name=='VoixOffAsk': return voice.chamar(name,r)
            return mensagem_cidade(m,r)
        if name=='BatimentGetCaseAdjacent':
            r=voice.chamar(name,dict(regs,EAX=args[0],EDX=args[1]))
            # The caller consumes AX only. Core explicitly marks stack-residue
            # upper EAX as unknown when no native stack is supplied.
            if r.get('_incertos',{}).get('EAX',0)&65535:
                raise ValueError('Unknown adjacent cell low word')
            return r['EAX']&65535
        if name=='BatimentAdjacent':
            return live.ciclo.core.batiment_adjacent(dict(EAX=args[0],EDX=args[1]))['EAX']&255
        from abi_luta_fatal_combate import DependenciaLutaFatal
        from combate_raid_vivo import DEPENDENCIAS_RAID
        raise DependenciaLutaFatal(name,DEPENDENCIAS_RAID[name],args)
    live.externo=provided
    n = case['routine']
    if n == 'CalculAttaqueEngin': live.combate.calcular_ataque(regs['EAX'])
    elif n == 'ProjectileCalcul': live.combate.calcular_projeteis()
    elif n == 'EnginInfligeDegat': live.combate.infligir_unidade(regs['EAX'],regs['EDX'],regs['EBX'],regs['ECX'])
    elif n == 'InfligeDegat': live.combate.infligir(regs['EAX'],regs['EDX'],regs['EBX'],regs['ECX'],int(case['stack_args'][0],16))
    elif n == 'SetDyingEngin': live.ciclo.dying(regs['EAX'])
    elif n == 'BatimentInfligeDegat': live.combate.infligir_estrutura_registradores(regs)
    else: raise ValueError(n)
    return serialize(blocks), calls


def fresh_native(case, before, inventory):
    b = BancadaLutaFatal(before)
    calls = []
    sites = {int(e['call'],16):e['routine'] for e in case['sound_requests']}
    # Hook every audited site, so an unexpected extra request cannot go unseen.
    for e in inventory: sites[int(e['call'],16)] = e['routine']
    def on_call(cpu, address, size, _):
        name = sites[address]
        regs = {r:cpu.reg_read(getattr(b.x86,'UC_X86_REG_'+r)) for r in REQUEST_REGS[name]}
        esp = cpu.reg_read(b.x86.UC_X86_REG_ESP)
        words = [struct.unpack('<I',cpu.mem_read(esp,4))[0]] if name=='PlaySnd_PostSound' else []
        calls.append(request(name,regs,words,address))
    hooks = [b.cpu.hook_add(b.unicorn.UC_HOOK_CODE,on_call,begin=a,end=a) for a in sites]
    try:
        result, _, after = b.call(case['routine'], {k:int(case['entry_registers'][k],16) for k in REG7},
                                  words=[int(w,16) for w in case['stack_args']], seconds=15)
    finally:
        for h in hooks: b.cpu.hook_del(h)
    if result['fault'] or result['limit'] or not result['reached_return'] or result['writes_outside_checkpoint']:
        raise RuntimeError(str(result))
    return after, calls


def compare(path=CAPTURE, *, native=False):
    capture = load(path)
    rows = []
    for i,case in enumerate(capture['cases']):
        before = state_before(case)
        if resumo(before)!=case['state_before']: raise ValueError('Captured parent entry differs')
        expected = write_state(before, [[a,bytes([v]).hex()] for a,_,v in case['changed_bytes']])
        actual, calls = execute(case)
        wanted = expected_requests(case)
        row = dict(case=i,frame=case['frame'],routine=case['routine'],
                   state_equal=actual==expected, requests_equal=calls==wanted,
                   native_state_equal=None, native_requests_equal=None,
                   requests=len(wanted))
        if not row['requests_equal']: row.update(actual_requests=calls,expected_requests=wanted)
        if not row['state_equal']:
            row['different_blocks']=[n for n in actual if actual[n]!=expected[n]]
        if native:
            original, original_calls = fresh_native(case,before,capture['inventory'])
            row.update(native_state_equal=original==expected, native_requests_equal=original_calls==wanted)
            if original_calls!=wanted: row['native_requests']=original_calls
        rows.append(row)
    return dict(schema='rising-lands/combat-s1-sound-differential/1',native=native,
                original_sha256=capture['original_sha256'],
                source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in (
                    'combate_raid_vivo.py','luta_fatal_viva_combate.py','ciclo_morte_luta_combate.py',
                    'validar_som_luta_s1_combate.py')},
                capture_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                summary=dict(cases=len(rows),requests=sum(r['requests'] for r in rows),
                             real_window_requests=len(capture['requests']),
                             mismatches=sum(any(r[k] is False for k in ('state_equal','requests_equal','native_state_equal','native_requests_equal')) for r in rows),
                             routines=dict(Counter(r['routine'] for r in rows))),cases=rows)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--capture',type=Path,default=CAPTURE)
    ap.add_argument('--emular',action='store_true')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args(); report=compare(args.capture,native=args.emular)
    if args.output: args.output.write_text(json.dumps(report,indent=1)+'\n')
    print(json.dumps(report,indent=1))
    raise SystemExit(bool(report['summary']['mismatches']))
