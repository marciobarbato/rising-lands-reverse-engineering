"""Recorded app -> unchanged Missions input -> native replays -> all-frame report.

Use `original` on the mini. Its only instrumentation is a read-only companion
observer around Missions' amostra; correr, validator and scripted bindings remain
unchanged. The app validation replay uses the same S0/128-prefix/C phase path as
Test A, audited execution policy 2, without rendering after frame 128.
"""
import argparse
import ctypes as C
import json
import importlib.util
import os
from pathlib import Path
import runpy
import signal
import subprocess
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from macos_scripted_input import ScriptedInput, FrameAnswerMapper, canonical, owner_contract
from macos_test_b import HashContract, compare, sha, order_coverage


def write(path, value):
    Path(path).write_bytes(canonical(value))


def app(a, script):
    from macos_native_driver import NativeDriver
    from macos_m22_playback import MacOSM22Playback
    # Only copied ABI diagnostics, not the engine's simulator/reference imports.
    sys.path.insert(0, str(a.root/'motor/testes'))
    from player_abi import Player, orders, inputs
    driver = NativeDriver(a.bundle/'librising_macos_live.dylib', a.bundle/'librising_engine.dylib', a.bundle/'native-inputs')
    engine = Player(a.bundle/'librising_engine.dylib')
    contract = HashContract(a.root)
    baseline = MacOSM22Playback.open(a.root)._s0
    names = {base: name for name, (base, data) in baseline.items() if name != 'native_stack'}
    stop = min(a.ate or script.stop_frame, script.stop_frame)
    manifest = dict(schema='rising-lands/macos-test-b-replay/1', input_sha256=sha(a.input),
                    hash_contract=contract.identity, stop_frame=stop, status='running',
                    mode='app validation: persistent audited policy 2, production C input phase; no post-prefix rendering',
                    source_revision=subprocess.check_output(['git','-C',str(a.root),'rev-parse','HEAD'], text=True).strip(),
                    bundle_snapshot_sha256=sha(a.bundle/'snapshot.json'),
                    driver_sha256=sha(a.bundle/'librising_macos_live.dylib'),
                    engine_sha256=sha(a.bundle/'librising_engine.dylib'),
                    initialization='Accepted S0 + four original static tables; real 128-frame prefix; no later state reload')
    tags = []
    order_rows = []
    started = time.monotonic()
    try:
        if driver.lib.macos_live_validation(driver.handle, 0): raise RuntimeError('Play policy refused')
        engine.check(engine.lib.rl_execucao_definir(driver.status().world, 2))
        for _ in range(129):
            if driver.advance(): raise RuntimeError(bytes(driver.status().message).decode())
        initial = engine.snapshot(driver.status().world)
        static = {base: data for base, data in initial.items() if base not in names}
        mapper = FrameAnswerMapper(script, hwnd=0)
        with (a.output/'states.jsonl').open('x') as f, (a.output/'orders.jsonl').open('x') as of:
            for frame in range(129, stop+1):
                mapper.begin_frame(frame)
                answers = mapper.declared_answers()
                for phase in (2, 3):
                    code = driver.input_phase(phase, answers)
                    consumed = engine.consumed(driver.status().world)
                    for event in consumed:
                        if event.kind not in range(1, 7): continue
                        kind = {1:'peek_message', 2:'get_message', 3:'translate_message', 4:'dispatch_message', 5:'cursor', 6:'key'}[event.kind]
                        phase_name = ('between_frames' if phase == 2 else 'frame')+str(frame)
                        mapped = mapper.poll(kind, phase=phase_name, site=event.site,
                                             vk=event.values[0] if event.kind == 6 else None)
                        actual = inputs([event])[0]
                        actual['phase'] = phase_name
                        if kind == 'dispatch_message':
                            actual.pop('wndproc_flags_after')
                            actual['hwnd'] = event.values[3]
                        if actual != mapped: raise RuntimeError(f'Frame {frame}: consumed answer differs from recorder: {actual} / {mapped}')
                    for order in orders(consumed):
                        order_rows.append(order)
                        of.write(json.dumps(order, sort_keys=True)+'\n')
                        if order.get('event', 'SetPlayerOrdre') == 'SetPlayerOrdre': tags.append(order['tag'])
                    if code: raise RuntimeError(f'Frame {frame} phase {phase}: '+bytes(driver.status().message).decode())
                snap = engine.snapshot(driver.status().world)
                if any(snap.get(base) != data for base, data in static.items()):
                    raise RuntimeError('Original static input mutated')
                state = {names.get(base, f'rust_extra_{base:08x}'): (base, data)
                         for base, data in snap.items() if base not in static}
                f.write(json.dumps(contract.sample(frame, state), sort_keys=True)+'\n')
                if frame % 500 == 0: print('App replay frame', frame, flush=True)
        mapper.finish()
        manifest['status'] = 'completed'
    except Exception as e:
        manifest.update(status='stopped', stop=str(e))
    finally:
        driver.close()
    manifest.update(seconds=time.monotonic()-started, order_tags=tags,
                    order_coverage=order_coverage(order_rows))
    manifest['full_session_ready'] = manifest['status'] == 'completed' and stop-128 >= 3000 and all(manifest['order_coverage'].values())
    write(a.output/'manifest.json', manifest)
    print(json.dumps(manifest, indent=1))
    return int(manifest['status'] != 'completed')


def original(a, script):
    if a.minutes: signal.alarm(int(a.minutes*60))
    owner = a.root/'pesquisas-paralelas/missoes/m3/entrada_roteirizada.py'
    spec = importlib.util.spec_from_file_location('entrada_roteirizada', owner)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    ns = vars(module)
    # The complete owner module validates the exact exported file unchanged.
    ns['carregar_entrada'](json.loads(a.input.read_bytes()))
    contract = HashContract(a.root)
    correr = ns['correr']
    globals_ = correr.__globals__
    old_sample = globals_['amostra']
    output = a.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    companion = output.with_name(output.name+'.states.tmp')
    manifest = dict(schema='rising-lands/macos-test-b-replay/1', input_sha256=sha(a.input),
                    hash_contract=contract.identity, stop_frame=min(a.ate or script.stop_frame, script.stop_frame),
                    status='running', owner_source_sha256=sha(owner), mode='intact executable; unchanged Missions correr')
    started = time.monotonic()
    if not a.worker:
        command = [sys.executable, '-B', str(Path(__file__).resolve()), '--root', str(a.root.resolve()),
                   'original', '--input', str(a.input.resolve()), '--output', str(output),
                   '--inicio', str(a.inicio.resolve()), '--worker']
        if a.ate: command += ['--ate', str(a.ate)]
        result = subprocess.run(command, timeout=a.minutes*60-10 if a.minutes else None)
        companion.rename(output/'states.jsonl')
        with (output/'states.jsonl').open('rb') as saved: os.fsync(saved.fileno())
        summary = json.loads((output/'resumo.json').read_text())
        if summary['original_sha256'] != contract.identity['original_sha256'] or not summary['code_unchanged']:
            raise ValueError('Original executable identity/code integrity failed')
        manifest.update(status=summary['status'], seconds=time.monotonic()-started,
                        original_summary_sha256=sha(output/'resumo.json'), original_summary=summary,
                        child_exit=result.returncode)
        write(output/'manifest.json', manifest)
        return int(manifest['status'] != 'completed' or result.returncode != 0)
    with companion.open('x') as f:
        def sample(bench):
            row = old_sample(bench)
            frame = bench.roteiro.quadro
            f.write(json.dumps(contract.sample(frame, bench.imagem()), sort_keys=True)+'\n')
            f.flush()
            return row
        globals_['amostra'] = sample
        args = argparse.Namespace(entrada=str(a.input.resolve()), inicio=str(a.inicio.resolve()),
                                  saida=str(output), ate=a.ate, retomar=None, instantaneo_cada=1000)
        try:
            correr(args)
        except SystemExit as e:
            if e.code not in (None, 0): manifest['stop'] = f'Missions exit {e.code}'
    companion.rename(output/'states.jsonl')
    summary = json.loads((output/'resumo.json').read_text())
    manifest.update(status=summary['status'], seconds=time.monotonic()-started,
                    original_summary_sha256=sha(output/'resumo.json'), original_summary=summary)
    write(output/'manifest.json', manifest)
    return int(manifest['status'] != 'completed')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('record', help='Drive the actual app UI; produces synthetic evidence, never human acceptance')
    q.add_argument('--app', type=Path, required=True)
    q.add_argument('--output', type=Path, required=True)
    q.add_argument('--plan', type=Path, default=Path(__file__).resolve().parents[1]/'test-b-ui-plan.json')
    for command in ('validate', 'app', 'original'):
        q = sub.add_parser(command)
        q.add_argument('--input', type=Path, required=True)
        if command != 'validate':
            q.add_argument('--output', type=Path, required=True)
            q.add_argument('--ate', type=int)
        if command == 'app': q.add_argument('--bundle', type=Path, required=True, help='Contents/Resources/preview')
        if command == 'original':
            q.add_argument('--inicio', type=Path, default=Path('.local/m3/quadro128'))
            q.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
            q.add_argument('--minutes', type=float, help='Hard wall-clock bound for MacBook prefixes (max 20)')
    q = sub.add_parser('compare')
    for name in ('app', 'original', 'output'): q.add_argument('--'+name, type=Path, required=True)
    q.add_argument('--ate', type=int)
    a = p.parse_args()
    if a.command == 'record':
        if a.output.exists() or a.output.with_suffix('.input.json').exists(): p.error('Refusing to overwrite UI evidence')
        a.output.parent.mkdir(parents=True, exist_ok=True)
        command = ['open', '-W', '-n', str(a.app.resolve()), '--args', '--inspection',
                   '--test-b-session', str(a.output.resolve()), '--test-b-plan', str(a.plan.resolve())]
        result = subprocess.run(command, timeout=900, capture_output=True, text=True)
        a.output.with_suffix('.launch.log').write_text(result.stdout+result.stderr)
        report = json.loads(a.output.read_text())
        script = ScriptedInput(a.root, a.output.with_suffix('.input.json').read_bytes())
        if result.returncode or not report['passed'] or script.stop_frame-128 < 3000:
            print(json.dumps(dict(passed=False, error=report.get('error'), phase=report.get('phase')), indent=1))
            return 1
        print(json.dumps(dict(passed=True, synthetic=True, frames=script.stop_frame-128,
                              input_sha256=sha(a.output.with_suffix('.input.json')))))
        return 0
    if a.command == 'compare':
        if a.output.exists(): p.error('Refusing to overwrite report')
        report = compare(a.app, a.original, a.ate)
        write(a.output, report)
        md = a.output.with_suffix('.md')
        md.write_text('# Test B per-frame divergence report\n\n'+
                      f"{report['frames_equal']}/{report['frames_requested']} frames equal.\n\n"+
                      ('No divergences.\n' if not report['differences'] else '\n'.join(
                          f"- Frame {r['frame']}: {', '.join(r['differences'])}" for r in report['differences'])+'\n'))
        print(json.dumps({k:v for k,v in report.items() if k not in ('results','differences','replay_manifests')}, indent=1))
        return int(not report['passed'])
    script = ScriptedInput(a.root, a.input.read_bytes())
    if a.command == 'validate':
        ns = runpy.run_path(str(a.root/'pesquisas-paralelas/missoes/m3/entrada_roteirizada.py'), run_name='macos_test_b_validator')
        ns['carregar_entrada'](json.loads(a.input.read_bytes()))
        print(json.dumps(dict(input_sha256=sha(a.input), stop_frame=script.stop_frame,
                              frames_after_prefix=script.stop_frame-128, full_owner_validator=True,
                              canonical_roundtrip=ScriptedInput(a.root, script.export_bytes()).export_bytes()==script.export_bytes())))
        return 0
    if a.ate is not None and not 129 <= a.ate <= script.stop_frame: p.error('Invalid replay end')
    if a.output.exists(): p.error('Refusing to overwrite replay')
    if a.command == 'app':
        a.output.mkdir(parents=True)
        return app(a, script)
    if a.minutes is not None and not 0 < a.minutes <= 20: p.error('MacBook bound must be <=20 min')
    return original(a, script)


if __name__ == '__main__': raise SystemExit(main())
