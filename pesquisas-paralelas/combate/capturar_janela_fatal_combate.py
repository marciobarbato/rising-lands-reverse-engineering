"""Original-only phase/leaf evidence from an existing S1 or D1 native snapshot.

Resume the exact Missions scripted-input bench, with all its already-declared
external/display boundaries. Every hook below only records. This tool neither
injects an order nor alters a game byte. Runs are bounded to 250 frames/1100s.
The output includes an exact resumable end snapshot for the following segment.
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import signal
import struct
import sys
import time

from ambiente_combate_raid import ROOT
sys.path.append(str(ROOT / 'pesquisas-paralelas/missoes/m3'))
import entrada_roteirizada as er
import segmentos_quadros_missao as seg
from delta_estado_missao import delta, estado_completo, resumo
from emulador import x86, unicorn
from oraculo_quadro_missao import nomes_fases

HOOKS = {'InfligeDegat': (0x450874, 4), 'EnginInfligeDegat': (0x4502f0, 0),
         'iagUnitSendMessage': (0x4829c8, 0), 'MAJSympathie': (0x475118, 0),
         'PlayerResetAllie': (0x46d8cb, 0), 'MessageBoxSet': (0x46994b, 0),
         'EnginSetLevelExperience': (0x44fb20, 0), 'SetDyingEngin': (0x444938, 0),
         'RetireEngin': (0x457058, 0), 'CalculEnginNextEtape': (0x456db5, 0),
         'EnginNextEtape': (0x45442c, 0)}
REGS = ('EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP','EIP','EFLAGS')


def identidade_registrada(path, frame):
    """Read the unique published end-of-frame identity, never a pickle digest."""
    raw = path.read_bytes()
    opener = lzma.open if path.suffix == '.xz' else open
    matches = []
    with opener(path, 'rt') as stream:
        for line in stream:
            if line.strip():
                row = json.loads(line)
                if row['frame'] == frame:
                    matches.append(row)
    if len(matches) != 1:
        raise RuntimeError(f'Require one published record at frame {frame}, found {len(matches)}')
    row = matches[0]
    expected = {k: row[k] for k in ('dgroup_sha256', 'state_sha256')}
    if any(len(v) != 64 or any(c not in '0123456789abcdef' for c in v) for v in expected.values()):
        raise RuntimeError('Invalid published state identity')
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), frame=frame, **expected)


def abrir_snapshot(inicio, candidates, frame, *, digest=None, identity=None):
    """Restore trusted project files; verify before any native phase or sound change."""
    mismatches = []
    for path in candidates:
        if not path.is_file():
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest is not None and actual != digest:
            continue
        b, _, restored = er.abrir(inicio, path)
        if restored != frame:
            mismatches.append(f'{path}: frame {restored} differs from {frame}')
            continue
        if identity is not None:
            observed = er.amostra(b)
            different = [k for k in ('dgroup_sha256', 'state_sha256') if observed[k] != identity[k]]
            if different:
                mismatches.append(f'{path}: mismatched {", ".join(different)}')
                continue
        return b, path, actual
    raise RuntimeError('No verified snapshot found; no execution started. ' + '; '.join(mismatches))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inicio', type=Path, default=ROOT/'.local/m3/quadro128')
    p.add_argument('--snapshot', type=Path)
    p.add_argument('--snapshot-root', type=Path, default=ROOT/'.local')
    p.add_argument('--snapshot-frame', type=int, required=True)
    p.add_argument('--snapshot-sha256')
    p.add_argument('--snapshot-manifest', type=Path,
                   help='Missions resumo.json; pins pickle SHA only when --snapshot-records is absent')
    p.add_argument('--snapshot-records', type=Path,
                   help='Published quadros.jsonl[.xz]; require restored DGROUP AND whole-state identity')
    p.add_argument('--entrada', type=Path, required=True)
    p.add_argument('--ate', type=int, required=True)
    p.add_argument('--saida', type=Path, required=True)
    p.add_argument('--leaf-limit', type=int, default=24)
    p.add_argument('--execute-sound-bodies', action='store_true',
                   help='Execute original unopened sound-library bodies instead of inherited display boundaries')
    a = p.parse_args()
    if not 1 <= a.ate-a.snapshot_frame <= 250 or not 1 <= a.leaf_limit <= 64:
        p.error('Require 1..250 frames and 1..64 isolated leaf records')
    if a.saida.exists(): p.error('Output directory already exists')
    manifest_pin=None
    if a.snapshot_manifest:
        manifest_raw=a.snapshot_manifest.read_bytes();manifest=json.loads(manifest_raw)
        expected=manifest['snapshots'][str(a.snapshot_frame)]['sha256']
        if not a.snapshot_records and a.snapshot_sha256 is not None and a.snapshot_sha256!=expected:
            p.error('Explicit snapshot SHA differs from the Missions manifest')
        if not a.snapshot_records:
            a.snapshot_sha256=expected
        manifest_pin=dict(path=str(a.snapshot_manifest),sha256=hashlib.sha256(manifest_raw).hexdigest())
        if hashlib.sha256(a.entrada.read_bytes()).hexdigest()!=manifest['input_sha256']:
            p.error('Scenario input hash differs from the Missions manifest')
    identity = identidade_registrada(a.snapshot_records, a.snapshot_frame) if a.snapshot_records else None
    if a.snapshot_sha256 is None and identity is None:
        p.error('Supply --snapshot-records, --snapshot-sha256 or --snapshot-manifest')
    candidates = [a.snapshot] if a.snapshot else sorted(a.snapshot_root.rglob(f'instantaneo-{a.snapshot_frame:05d}.pickle'))
    # Trusted project snapshots only. Restore after the scripted bindings exist.
    b, snapshot, snapshot_sha = abrir_snapshot(a.inicio, candidates, a.snapshot_frame,
                                              digest=a.snapshot_sha256, identity=identity)
    frame = a.snapshot_frame
    raw = a.entrada.read_bytes()
    declared, stop_frame = er.carregar_entrada(json.loads(raw))
    if a.ate > stop_frame: raise RuntimeError('Requested end exceeds the input stop frame')
    if {k:v for k,v in b.roteiro.quadros.items() if k<=frame} != {k:v for k,v in declared.items() if k<=frame}:
        raise RuntimeError('Input prefix differs from the restored original run')
    b.roteiro.quadros = declared
    executed_sounds=[]
    if a.execute_sound_bodies:
        for name in ('PlaySnd_Manage','PlaySnd_PostSound','PlaySnd_StopSound','PlaySnd_StopAllSound',
                     'PlaySnd_PostVolume','PlaySnd_SetGameVolume'):
            address=b.sym[name]
            for attr in ('fronteiras','pulos'):getattr(b,attr).pop(address,None)
            executed_sounds.append(name)
    a.saida.mkdir(parents=True)
    opened = b.imagem()
    opening = dict(summary=resumo(opened), full_state=estado_completo(opened))
    with lzma.open(a.saida/'abertura.json.xz','wt',preset=3) as f: json.dump(opening,f)
    cases=[]; pending=[]; counts={n:0 for n in HOOKS}; phase='opening'; baseline=opened
    sampled=set(); return_hooks={}; failures=[]; completed=frame
    by_address={address:(name,cleanup) for name,(address,cleanup) in HOOKS.items()}
    def regs(): return {k:b.cpu.reg_read(getattr(x86,'UC_X86_REG_'+k)) for k in REGS}
    def word(address): return struct.unpack('<I',b.cpu.mem_read(address,4))[0]
    def on_return(cpu,address,size,_):
        current=regs()
        for item in pending[:]:
            if address!=item['return_address'] or current['ESP']!=item['return_esp']: continue
            after=b.imagem()
            item['record'].update(exit_registers={k:hex(v) for k,v in current.items()},
                                 reached_return=True,state_after=resumo(after),delta=delta(item['before'],after))
            pending.remove(item)
    def on_entry(cpu,address,size,_):
        name,cleanup=by_address[address]; counts[name]+=1
        corpse_timer=None
        if name=='EnginNextEtape':
            u=b.cpu.reg_read(x86.UC_X86_REG_EAX)&65535
            if u>=800:return
            rec=word(0x4e19a0)+276*u
            if bytes(b.cpu.mem_read(rec+2,1))!=b'\4':return
            corpse_timer=struct.unpack('<H',b.cpu.mem_read(rec+0xc2,2))[0]
            if corpse_timer not in (0,329):return
        r=regs()
        # Each routine/AX/DL pair is sampled once; all calls remain counted.
        # Recount is captured only after a death/removal has actually occurred.
        if name=='CalculEnginNextEtape' and not any(c['routine']=='SetDyingEngin' for c in cases): return
        key=(name,r['EAX']&65535,corpse_timer if corpse_timer is not None else r['EDX']&255) if name!='CalculEnginNextEtape' else (name,0,0)
        priority=name in ('SetDyingEngin','RetireEngin','CalculEnginNextEtape','EnginNextEtape')
        if key in sampled or len(cases)>=a.leaf_limit and not priority: return
        if len(cases)>=a.leaf_limit+32: raise RuntimeError('Fatal leaf capture reserve exhausted')
        sampled.add(key); before=b.imagem(); ret=word(r['ESP'])
        record=dict(routine=name,phase=phase,frame=frame,
                    entry_registers={k:hex(v) for k,v in r.items()},
                    stack_words=[word(r['ESP']+4)] if cleanup else [],
                    state_before=resumo(before),entry_delta=delta(baseline,before),
                    reached_return=False,return_address=hex(ret))
        if corpse_timer is not None:record['corpse_timer_before']=corpse_timer
        cases.append(record)
        pending.append(dict(record=record,before=before,return_address=ret,return_esp=r['ESP']+4+cleanup))
        if ret not in return_hooks:
            return_hooks[ret]=b.cpu.hook_add(unicorn.UC_HOOK_CODE,on_return,begin=ret,end=ret)
    handles=[b.cpu.hook_add(unicorn.UC_HOOK_CODE,on_entry,begin=address,end=address) for address in by_address]
    started=time.monotonic()
    def budget(*_): raise TimeoutError('1100-second native window budget')
    signal.signal(signal.SIGALRM,budget);signal.alarm(1100)
    try:
        with lzma.open(a.saida/'fases.jsonl.xz','wt',preset=3) as out:
            for frame in range(completed+1,a.ate+1):
                b.roteiro.iniciar_quadro(frame)
                for phase,method in zip(nomes_fases(frame),(b.executar_entre_quadros,b.executar_quadro)):
                    baseline=b.imagem(); before_regs=regs()
                    method(60,frame)
                    after=b.imagem()
                    record=dict(phase=phase,frame=frame,state_before=resumo(baseline),
                                entry_registers={k:hex(v) for k,v in before_regs.items()},
                                state_after=resumo(after),delta=delta(baseline,after),
                                exit_registers={k:hex(v) for k,v in regs().items()})
                    out.write(json.dumps(record)+'\n')
                completed=frame
    except Exception as exc:
        failures.append(f'{type(exc).__name__}: {exc}')
    finally:
        signal.alarm(0)
        for h in handles+list(return_hooks.values()): b.cpu.hook_del(h)
        with lzma.open(a.saida/'folhas.json.xz','wt',preset=3) as f: json.dump(cases,f)
        snapshot_out=None
        if completed==frame and not failures:
            path=a.saida/f'instantaneo-{completed:05d}.pickle'
            snapshot_out=dict(path=str(path),sha256=seg.salvar(b,path,completed))
        report=dict(schema='rising-lands/combat-scripted-fatal-window/1',translation_executed=False,
                    original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    snapshot=dict(path=str(snapshot),sha256=snapshot_sha,frame=a.snapshot_frame,
                                  verification='published-state' if identity else 'pickle-sha256'),
                    snapshot_identity=identity,
                    snapshot_manifest=manifest_pin,original_sound_bodies=executed_sounds,
                    input=dict(path=str(a.entrada),sha256=hashlib.sha256(raw).hexdigest()),
                    completed_frame=completed,requested_end=a.ate,failures=failures,counts=counts,
                    leaf_cases=len(cases),incomplete_leaves=len(pending),end_snapshot=snapshot_out,
                    hooks={n:hex(v[0]) for n,v in HOOKS.items()},seconds=round(time.monotonic()-started,3))
        (a.saida/'manifest.json').write_text(json.dumps(report,indent=1)+'\n')
        print(json.dumps(report),flush=True)
    return bool(failures or pending)


if __name__=='__main__': raise SystemExit(main())
