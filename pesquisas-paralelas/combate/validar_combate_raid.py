"""Whole-checkpoint differential for Combat's real-raid live-memory API.

Local mode replays committed original evidence. --emular freshly reruns each
selected original leaf, including explicit foreign-provider entry stops.
Native windows remain original evidence, not Python frame-chain validation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

from ambiente_combate_raid import ROOT
from bancada_combate_raid import checkpoints, BancadaCombateRaid, DEPENDENCIES
from delta_estado_missao import aplicar, resumo
from memoria_quadro_core import MemoriaQuadro
from combate_raid_vivo import CombateRaidVivo, DependenciaCombateRaid

HERE = Path(__file__).resolve().parent
CAPTURE = HERE / 'evidencias/captura-combate-raid-original-v1.json'
PRESERVED = ('EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
GENERAL = ('EAX', *PRESERVED)


def write_state(state, writes):
    result = dict(state)
    for address, hexdata in writes:
        a, data = int(address, 16), bytes.fromhex(hexdata)
        name, (base, old) = next((n, b) for n, b in result.items() if b[0] <= a and a+len(data) <= b[0]+len(b[1]))
        buf = bytearray(old);buf[a-base:a-base+len(data)] = data
        result[name] = (base, bytes(buf))
    return result


def entry_states(capture, states):
    previous = None
    for case in capture['cases']:
        setup = list(case['declared_writes'])
        if '-window-' in case['case'] and '-t' in case['case']:
            import re
            tick = int(re.search(r'-t(\d+)-', case['case']).group(1))
            setup.append(['0x508f7c', (case['checkpoint']+tick).to_bytes(4, 'little').hex()])
        # Every input is one of the explicit checkpoint reset or the preceding
        # native state plus declared writes. Hashes resolve that choice exactly.
        candidates = [states[case['checkpoint']][0]]
        if previous is not None:
            candidates.insert(0, previous)
        before = None
        for candidate in candidates:
            proposed = write_state(candidate, setup)
            if resumo(proposed) == case['state_before']:
                before = proposed
                break
        if before is None:
            raise ValueError(f'Cannot reconstruct original input {case["case"]}')
        after = aplicar(before, case['delta'], case['case'])
        if resumo(after) != case['state_after']:
            raise ValueError(f'Original delta/hash mismatch: {case["case"]}')
        previous = after
        yield case, before, after


def memory(state):
    blocks = {n:(base,bytearray(data)) for n,(base,data) in state.items()}
    return MemoriaQuadro((base,data) for base,data in blocks.values()), blocks


def serialize(blocks):
    return {n:(base,bytes(data)) for n,(base,data) in blocks.items()}


def execute(case, state, audio=False, guarded=False):
    m, blocks = memory(state)
    sound=None
    if audio:
        from provedor_pedidos_m3_audio import SoundRequestProvider, LiveAudioMemory
        sound=SoundRequestProvider(LiveAudioMemory(m),domain='unopened-display')
    def known_guard(name,args):
        # Test-only original read-only returns, never a general AI/diplomacy bridge.
        # Both original bodies and full outcomes are present in the committed matrix.
        if name == 'iagVilleSendMessage' and args[1] in (2,4):
            owner=m.u8(0x49a0c8+276*(args[0]&65535)+4)
            if owner < 4 and m.u8(m.u32(0x5080a8)+20*owner+1) != 2:
                return None  # 0x484808 -> PlayerGetType != 2 -> original RET
        if name == 'iagUnitSendMessage' and args[1] == 0x48:
            owner=m.u8(m.u32(0x4e19a0)+276*(args[0]&65535))
            if owner < 4 and m.u8(m.u32(0x5080a8)+20*owner+1) != 2:
                return None  # 0x4829c8 -> PlayerGetType != 2 -> original RET
        if name == 'MAJSympathie':
            a,b,flag=args
            if a == b or a >= 4 or b >= 4:
                return dict(EAX=a,EDX=b,EBX=flag)  # 0x475121..0x475135 guard exits
        if name == 'PlayerAAttaqueSet' and (args[0] >= 4 or args[1] >= 4):
            return None  # 0x46d609/0x46d612 before any statistic store
        raise DependenciaCombateRaid(name,args)
    live = CombateRaidVivo(m,som=sound,efeito=known_guard if guarded else None)
    regs = {k:int(v,16) for k,v in case['entry_registers'].items()}
    name, output, checked, dependency = case['routine'], {}, (), None
    try:
        if name == 'SetAttaqueEngin':
            output = live.set_attaque_engin(regs); checked = GENERAL
        elif name == 'EnginTrouveCible':
            output = live.engin_trouve_cible(regs); checked = GENERAL
        elif name == 'CalculAttaqueEngin':
            live.calcular_ataque(regs['EAX']);output=regs;checked=PRESERVED
        elif name == 'InfligeDegat':
            live.infligir(regs['EAX'],regs['EDX'],regs['EBX'],regs['ECX'],case['stack_words'][0])
        elif name == 'EnginInfligeDegat':
            live.infligir_unidade(regs['EAX'],regs['EDX'],regs['EBX'],regs['ECX'])
        elif name == 'ProjectileInit':
            live.pool.iniciar(regs['EAX'],regs['EDX'],regs['EBX'],regs['ECX'],*case['stack_words'])
            output=regs;checked=('ESI','EDI','EBP')
        elif name == 'ProjectileAvance':
            if case.get('stop') == 'InfligeDegat checkpoint':
                def internal_checkpoint(name,args):
                    if name != 'InfligeDegat':
                        raise ValueError(f'Unexpected effect before impact checkpoint: {name}')
                    raise DependenciaCombateRaid(name,args)
                live.pool.efeito_externo=internal_checkpoint
            index, remainder = divmod(regs['EAX']-m.u32(0x5080f0),56)
            if remainder or not 0 <= index < 100:
                raise ValueError('ProjectileAvance needs an original record pointer')
            live.maquina.avancar(index)
            output=regs;checked=PRESERVED
        elif name == 'BatimentInfligeDegat':
            output=live.infligir_estrutura_registradores(regs);checked=GENERAL
        elif name in ('SetDyingEngin', 'RetireEngin'):
            (live.iniciar_morte if name=='SetDyingEngin' else live.retirar)(regs['EAX'])
        else:
            raise ValueError(f'Unselected routine {name}')
    except DependenciaCombateRaid as exc:
        dependency = dict(name=exc.nome, address=exc.endereco, arguments=list(exc.argumentos))
    return serialize(blocks), output, checked, dependency


def arguments_equal(dep, native_case):
    r={k:int(v,16) for k,v in native_case['exit_registers'].items()}
    name,args=dep['name'],dep['arguments']
    if name in ('iagUnitSendMessage','iagVilleSendMessage'):
        expected=[r['EAX']&65535,r['EDX']&255,r['EBX']&65535]
    elif name == 'PlaySnd_PostSound':
        expected=[r['EAX'],r['EDX'],r['ECX']&255,native_case['stop_stack_words'][0],r['EBX']]
    elif name in ('SetDyingEngin','RetireEngin'):
        expected=[r['EAX']&65535]
    elif name == 'EnginSetLevelExperience':
        expected=[r['EAX']&65535,r['EDX']&255]
    elif name in ('PlayerResetAllie','PlayerAAttaqueSet'):
        expected=[r['EAX']&255,r['EDX']&255]
    elif name in ('MAJSympathie','VoixOffAsk'):
        expected=[r['EAX'],r['EDX'],r['EBX']]
    elif name in ('BatimentGetCaseAdjacent','BatimentAdjacent'):
        expected=[r['EAX']&65535,r['EDX']&65535]
    elif name == 'InfligeDegat':
        expected=[r['EAX']&65535,r['EDX']&255,r['EBX']&65535,r['ECX']&255,
                  native_case['stop_stack_words'][0]&255]
    else:
        raise ValueError(f'No consumed-register comparison for {name}')
    return args == expected


def compare(capture=CAPTURE, native=False, output=None, audio=False, guarded=False):
    started=time.monotonic()
    hash_paths=(HERE/'combate_raid_vivo.py',HERE/'dano_estrutura_raid.py',HERE/'validar_combate_raid.py',
                HERE/'bancada_combate_raid.py')
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in hash_paths}
    capture = capture.resolve()
    data=json.loads(capture.read_bytes())
    states, provenance=checkpoints()
    bench=BancadaCombateRaid(states[9000][0]) if native else None
    rows=[]
    for case,before,after in entry_states(data,states):
        if '-window-' in case['case']:
            continue
        py,regs,checked,dep=execute(case,before,audio,guarded)
        row=dict(case=case['case'],routine=case['routine'],dependency=dep,
                 register_scope=list(checked), native=False, result=None)
        expected=after; native_case=case
        if dep:
            if not native:
                row['result']='dependency_not_compared';rows.append(row);continue
            bench.restore(before)
            stops=dict(DEPENDENCIES)
            if audio:stops.pop(0x48aa79,None)
            stops[dep['address']]=dep['name']
            native_case,_,expected=bench.call(case['routine'],
                {k:int(v,16) for k,v in case['entry_registers'].items() if k not in ('EIP','ESP')},
                words=tuple(case['stack_words']),stops=stops)
            row['native']=True
            row['stop_equal']=int(native_case['exit_registers']['EIP'],16)==dep['address']
            row['dependency_arguments_equal']=arguments_equal(dep,native_case)
        elif native:
            bench.restore(before)
            native_case,_,expected=bench.call(case['routine'],
                {k:int(v,16) for k,v in case['entry_registers'].items() if k not in ('EIP','ESP')},
                words=tuple(case['stack_words']),stops={a:n for a,n in DEPENDENCIES.items() if not audio or a!=0x48aa79})
            row['native']=True
            row['capture_reproduced']=(native_case['state_after']==case['state_after'] and
                 native_case['exit_registers']==case['exit_registers'])
        row['state_equal']=resumo(py)==resumo(expected)
        row['registers_equal']=all(regs[k]==int(native_case['exit_registers'][k],16) for k in checked)
        row['native_fault']=native_case['fault'];row['native_limit']=native_case['limit']
        row['unmodeled_native_writes']=native_case['writes_outside_checkpoint']
        row['result']='equal' if (row['state_equal'] and row['registers_equal'] and
            row.get('stop_equal',True) and row.get('dependency_arguments_equal',True) and row.get('capture_reproduced',True) and
            not row['native_fault'] and not row['native_limit'] and not row['unmodeled_native_writes']) else 'mismatch'
        if not row['state_equal']:
            row['different_blocks']=[n for n in expected if py[n]!=expected[n]]
            row['first_differences']=[]
            for n in row['different_blocks']:
                a,x=py[n];y=expected[n][1]
                row['first_differences'] += [[hex(a+i),xx,yy] for i,(xx,yy) in enumerate(zip(x,y)) if xx!=yy][:12]
        rows.append(row)
        print(json.dumps({k:row[k] for k in ('case','result','dependency')}),flush=True)
    report=dict(schema='rising-lands/combat-real-raid-differential/1',capture=str(capture.relative_to(ROOT)),
                capture_sha256=hashlib.sha256(capture.read_bytes()).hexdigest(),provenance=provenance,
                native=native,read_only_guard_fixture=guarded,audio_domain='unopened-display' if audio else None,cases=rows,seconds=round(time.monotonic()-started,3),
                summary=dict(cases=len(rows),equal=sum(r['result']=='equal' for r in rows),
                    mismatches=sum(r['result']=='mismatch' for r in rows),
                    dependency_not_compared=sum(r['result']=='dependency_not_compared' for r in rows),
                    dependency_stops=sum(bool(r['dependency']) for r in rows)))
    report['source_sha256']=source_hashes
    report['source_unchanged_during_run']=all(hashlib.sha256(p.read_bytes()).hexdigest()==source_hashes[p.name] for p in hash_paths)
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x') as f:json.dump(report,f,indent=1);f.write('\n')
    return report


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--captura',type=Path,default=CAPTURE)
    ap.add_argument('--emular',action='store_true');ap.add_argument('--audio',action='store_true');ap.add_argument('--guarded',action='store_true');ap.add_argument('--saida',type=Path,required=True)
    a=ap.parse_args()
    if a.saida.exists():raise SystemExit(f'Refusing to overwrite {a.saida}')
    r=compare(a.captura,a.emular,a.saida,a.audio,a.guarded);print(json.dumps(r['summary']),flush=True)
    return bool(r['summary']['mismatches'])


if __name__=='__main__':
    raise SystemExit(main())
