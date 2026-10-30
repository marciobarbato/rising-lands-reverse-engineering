"""Offline Rust frame proof against accepted intact-original M2.1/M2.2 evidence.

Run under the shared heavy lease. This script never executes x86 or repairs a
reference. Each phase advances ONE Rust world; reference deltas only reconstruct
the expected state, never become Rust inputs after S0. Output refuses overwrite.
"""
from pinned_reference import activate, reference_file, pinned_file, provenance
SOURCE_ROOT = activate()

import argparse
import copy
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

from frame_abi import Frames, FrameInput, FrameRegisters

ROOT = Path(__file__).resolve().parents[2]
IA = SOURCE_ROOT / 'pesquisas-paralelas/ia-runtime'
sys.path.insert(0, str(IA))
sys.path.insert(0, str(SOURCE_ROOT / 'pesquisas-paralelas/missoes'))
import ambiente_ia_runtime  # noqa: E402,F401
from frame_evidence import (VINCULO, FRONTEIRA, MascaraEnderecos, carregar_captura,
                            comparar_estado, comparar_eventos_fase, comparar_alocacoes,
                            fases_referencia, resumo_estado, ler_estado)
from contexto_exibicao_ia import ContextoExibicao  # noqa: E402
from inventario_ia_runtime import OriginalImage  # noqa: E402
from mapa_memoria_m1 import carregar_json, expandir_captura, carregar_blocos  # noqa: E402

MISSION = ROOT / 'pesquisas-paralelas/missoes'
EVIDENCE = MISSION / 'evidencias'
M1_ENTRY = EVIDENCE / 'entrada-carga-missao-exibicao-v2.json'
M1_CAPTURE = EVIDENCE / 'captura-carga-missao-exibicao-v2.json'
FIRST_CAPTURE = EVIDENCE / 'captura-quadro1-monde01-exibicao-v2.json'
LONG_CAPTURE = EVIDENCE / 'captura-quadros128-monde01-exibicao-v2.json.xz'
FIRST_POLICY = MISSION / 'validacao/m2-politica-comparacao-quadro1.json'
LONG_POLICY = MISSION / 'validacao/m2-2-politica-comparacao-128-quadros.json'
PINS = {
    M1_ENTRY: '0bfbe98a7fbdb73e3c1f0c8510095e259a127bcfb842edf161ae072cde13c03a',
    M1_CAPTURE: 'a71351ed3b74bf7f8327910f8d06459327c10e6a97dc4e272f9a95ee237bca7e',
    FIRST_CAPTURE: 'd800be5aee2cda363b6fca08fd162e5f7a1a61e849c1384e29fefe9e031e1d1d',
    FIRST_POLICY: '64c7fa739c76fc1f9a12bc4678181d0d8fa97c5887f5d8ced1b964d9e6cae73c',
    LONG_CAPTURE: '4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3',
    LONG_POLICY: 'bf36e6e8f6a38202fa3248256d3de9f768497caa835a563a3ef119be994127f0',
}
PINS.update({
    ROOT / 'pesquisas-paralelas/ia-runtime/comparar_quadro1_encadeado_ia.py': 'd1a268d35261c1f75afec9938c9c09b3bbc2bb371d9c81e17e3a8ff9374f82a6',
    ROOT / 'pesquisas-paralelas/ia-runtime/comparar_quadros_ia.py': 'aa81ee3b1b8514f76fb57ec44841b05289422fb4c177620b6cf571f96a30ac63',
    ROOT / 'pesquisas-paralelas/ia-runtime/composicao_quadros_ia.py': 'afdc8a396b254f5e65167b215c9a785d18cba530169c683ad5c35d63ed786e43',
    ROOT / 'pesquisas-paralelas/ia-runtime/composicao_encadeada_ia.py': '4d4f45ce5fc2c2599884d876f7c189554c61b71852115a83d4c96a6f4efc873b',
    ROOT / 'pesquisas-paralelas/ia-runtime/quadro_calcul_game.py': '1634bed75de495041871540bf33176e3aad607e1cf2c843f96453df623c540d7',
    ROOT / 'pesquisas-paralelas/ia-runtime/contexto_exibicao_ia.py': 'e8ba0fbbba0d0b8dd39511b3cca3df0a3a6737411992f488400e3e3b24b70d87',
    ROOT / 'pesquisas-paralelas/missoes/mapa_memoria_m1.py': '7507e065c20ff0c05d6d86972d0a11919cc59e484a6b4f306c122c309a2d74c9',
})
# Python references are loaded and checked at the fixed port revision.
LONG_RAW_SHA = '1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930'
BINDINGS = {1: ('USER32.ShowCursor', 1), 2: ('USER32.GetAsyncKeyState', 1),
            3: ('KERNEL32.GlobalHandle', 1), 4: ('KERNEL32.GlobalUnlock', 1),
            5: ('KERNEL32.GlobalFree', 1), 6: ('USER32.PeekMessageA', 5),
            7: ('USER32.GetCursorPos', 1), 8: ('USER32.SetCursorPos', 2)}
BOUNDARIES = {101: 'LoadPie', 102: 'MCICD_Play', 103: 'PlaySnd_Manage', 104: 'MCICD_Manage'}
BOUNDARY_CALLERS = {0x46847b: ('MenuInit+0x1c0', 'MenuInit'),
                    0x4684bd: ('MenuInit+0x202', 'MenuInit'),
                    0x42d32d: ('CalculGame+0xac5', 'MCICD_Play'),
                    0x460220: ('_WinMain@16+0xb0', 'PlaySnd_Manage'),
                    0x460225: ('_WinMain@16+0xb5', 'MCICD_Manage')}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_pins(paths):
    for path in paths:
        if sha(pinned_file(path)) != PINS[path]:
            raise ValueError('Frozen reference SHA mismatch: ' + str(path.relative_to(ROOT)))


def named_snapshot(snapshot, names):
    return {names.get(a, f'rust_extra_{a:08x}'): (a, data) for a, data in snapshot.items()}


def mismatch_bytes(mask, actual, expected):
    """Count exact compared-byte mismatches when block identities agree."""
    if actual.keys() != expected.keys():
        return None
    mismatches = 0
    for name, (base, reference) in expected.items():
        ab, data = actual[name]
        if ab != base or len(data) != len(reference):
            return None
        if data == reference:
            continue
        a, _ = mask.aplicar(base, data)
        b, _ = mask.aplicar(base, reference)
        if a != b:
            mismatches += sum(x != y for x, y in zip(a, b))
    return mismatches


def normalize_events(events, phase, cursor):
    """Map ABI observations onto precisely the fields compared by accepted policy."""
    bindings, boundaries, frees = [], [], []
    for e in events:
        if e.kind == 1:
            name, argc = BINDINGS[e.id]
            writes = []
            if e.id == 7:
                data = struct.pack('<ii', *cursor)
                writes = [dict(address=hex(e.args[0]), size=len(data), sha256=hashlib.sha256(data).hexdigest())]
            bindings.append(dict(name=name, arguments=[hex(a) for a in e.args[:argc]],
                                 caller_return=hex(e.site), results=dict(EAX=hex(e.result)), memory_writes=writes))
        elif e.kind == 2:
            name = BOUNDARIES[e.id]
            caller, top = BOUNDARY_CALLERS[e.site]
            guards = {'0x4e2f28': e.args[0], '0x4e2f29': e.args[1]} if e.id in (102, 104) else {}
            boundaries.append(dict(phase=phase, routine=name, caller_return=hex(e.site), caller=caller,
                                   top_callee=top, registers={n: hex(v) for n, v in
                                   zip(('EAX', 'EDX', 'EBX', 'ECX'), e.registers)}, declared_eax=None,
                                   stack_cleanup=0, guards=guards,
                                   stack_words=[hex(e.stack[i]) if e.stack_mask & (1 << i) else None
                                                for i in range(4)]))
        elif e.kind == 3:
            frees.append((e.args[0], e.result))
        else:
            raise ValueError(f'Unknown frame event kind {e.kind}')
    return bindings, boundaries, frees


def reject_mutated_events(bindings, boundaries, phase, context):
    """Mutate observations actually returned by Rust, then require rejection."""
    results = {}
    if bindings:
        changed = copy.deepcopy(bindings)
        changed[0]['results']['EAX'] = hex(int(changed[0]['results']['EAX'], 16) ^ 1)
        rejected = not comparar_eventos_fase(changed, phase['bindings'], context.vinculo,
                                             VINCULO, 'bindings')['equal']
        if not rejected:
            raise AssertionError('An altered actual Rust binding return was accepted')
        results['binding_return_mutation_detected'] = True
    if boundaries:
        changed = copy.deepcopy(boundaries)
        changed[0]['registers']['EAX'] = hex(int(changed[0]['registers']['EAX'], 16) ^ 1)
        rejected = not comparar_eventos_fase(changed, phase['boundaries'], context.fronteira,
                                             FRONTEIRA, 'boundaries')['equal']
        if not rejected:
            raise AssertionError('An altered actual Rust boundary register was accepted')
        results['boundary_register_mutation_detected'] = True
    return results


def update_allocations(records, events, freed):
    by_pointer = {int(r['pointer'], 16): r for r in records}
    observed_free = []
    for e in events:
        if e.kind != 1 or e.id not in (3, 4, 5):
            continue
        ptr = e.args[0]
        r = by_pointer[ptr]
        if not r['active']:
            raise ValueError(f'Allocator request on inactive pointer 0x{ptr:x}')
        if e.id == 3:
            if e.result != ptr:
                raise ValueError('GlobalHandle result differs from adopted GMEM_FIXED contract')
            r['events'] += ' handle'
        elif e.id == 4:
            if not r['locks'] or e.result != 0:
                raise ValueError('Invalid GlobalUnlock transition')
            r['locks'] -= 1
            r['events'] += ' unlock'
        else:
            if r['locks'] or e.result != 0 or ptr not in freed:
                raise ValueError('Invalid GlobalFree transition or missing freed byte snapshot')
            if len(freed[ptr]) != r['size']:
                raise ValueError('Freed byte count differs from allocation size')
            r.update(active=False, freed_sha256=hashlib.sha256(freed[ptr]).hexdigest())
            r['events'] += ' free'
            observed_free.append(ptr)
    announced = [(e.args[0], e.result) for e in events if e.kind == 3]
    if announced != [(p, len(freed[p])) for p in observed_free] or set(freed) != set(observed_free):
        raise ValueError('Free observations, binding transitions and freed snapshots differ')


def check_mutation_detection(mask, state):
    """Mutating an actual projected compared byte must fail the same comparator."""
    for name, (base, data) in state.items():
        if name == 'native_stack':
            continue
        for i, byte in enumerate(data):
            if not mask.mascarado(base + i):
                changed = dict(state)
                b = bytearray(data)
                b[i] = byte ^ 1
                changed[name] = (base, bytes(b))
                if comparar_estado(mask, changed, state)['equal']:
                    raise AssertionError('Compared-byte corruption was accepted')
                return dict(address=hex(base + i), detected=True)
    raise AssertionError('No compared byte available for mutation test')


STATIC_TABLES = ((0x45ed20, 40 * 4), (0x454344, 26 * 4), (0x4543c8, 25 * 4), (0x426880, 21 * 4))


def static_inputs(image, state):
    """Declare only original table bytes not already supplied by the captured state.

    Captured overlaps must agree with the intact image. Added regions remain
    immutable, are checked after every phase, and are excluded from state counts.
    """
    blocks = sorted(state.values())
    inputs = {}
    for address, length in STATIC_TABLES:
        data = image.read(address, address + length)
        missing = bytearray()
        start = address
        for i, byte in enumerate(data):
            at = address + i
            captured = next((b[at - a] for a, b in blocks if a <= at < a + len(b)), None)
            if captured is not None:
                if captured != byte:
                    raise ValueError(f'Captured/static table input disagreement at 0x{at:x}')
                if missing:
                    inputs[start] = bytes(missing)
                    missing.clear()
            else:
                if not missing:
                    start = at
                missing.append(byte)
        if missing:
            inputs[start] = bytes(missing)
    return inputs


def compare(library=None, frames=1, long_policy=False, state_only=False, executable=None):
    policy_path = LONG_POLICY if long_policy else FIRST_POLICY
    capture_path = LONG_CAPTURE if long_policy else FIRST_CAPTURE
    assert_pins([p for p in PINS if long_policy or p not in (LONG_CAPTURE, LONG_POLICY)])
    entry = carregar_json(M1_ENTRY)
    m1 = expandir_captura(carregar_json(M1_CAPTURE), entry)
    short_cap = carregar_json(FIRST_CAPTURE)
    s0 = carregar_blocos(m1['oracle']['final_state']['blocks'])
    s0 = {n: v for n, v in s0.items() if n != 'native_stack'}
    cap, raw_sha = carregar_captura(capture_path, LONG_RAW_SHA if long_policy else None)
    policy = carregar_json(policy_path)
    ranges = policy.get('cumulative', policy)['exclusion_mask']
    roots = policy['display_roots']
    if cap['state_s0']['summary'] != resumo_estado(s0):
        raise ValueError('Capture S0 differs from accepted display MissionLoad state')
    if not 1 <= frames <= (128 if long_policy else 1):
        raise ValueError('Frame count outside selected evidence domain')
    # Replay every phase/checkpoint before exercising Rust. This checks compressed
    # corpus integrity even when only an early subset is requested.
    integrity = [dict(phase=f['phase'], **record) for f, _, record in fases_referencia(cap, s0)]
    records = copy.deepcopy(m1['allocations'])
    names = {a: n for n, (a, _) in s0.items()}
    cursor = tuple(cap['named_inputs']['frame']['cursor'])
    surface = next(s for s in short_cap['phases'][0]['display_state']['surfaces'] if s['role'] == 'offscreen')
    mask = MascaraEnderecos(ranges)
    original = Path(executable or os.environ.get('RL_ORIGINAL_EXE', str(ambiente_ia_runtime.EXE))).resolve()
    image = OriginalImage(original, original.with_suffix('.SBL'))
    context = None if state_only else ContextoExibicao(image, roots)
    static = static_inputs(image, s0)
    rust = Frames(library)
    library_identity = dict(path=str(rust.path), bytes=rust.path.stat().st_size, sha256=sha(rust.path))
    handle = rust.create()
    results, runtime, checks = [], 0.0, {}
    try:
        rust.load(handle, sorted(list(s0.values()) + list(static.items())))
        initial_snapshot = rust.snapshot(handle)
        if any(initial_snapshot.get(a) != b for a, b in static.items()):
            raise AssertionError('Immutable table input projection differs')
        projected = named_snapshot({a: b for a, b in initial_snapshot.items() if a not in static}, names)
        if projected != s0:
            raise AssertionError('Initial memory -> state -> projection differs')
        checks['projected_byte_mutation'] = check_mutation_detection(mask, projected)
        inp = FrameInput(cursor[0], cursor[1], int(surface['pixels'], 16),
                         FrameRegisters.from_values({k: int(v, 16) for k, v in
                                                     cap['phases'][0]['entry']['registers'].items()}),
                         (C.c_uint32 * 3)(0, 0, 0), (C.c_uint32 * 4)(0x3000000, 0, 0, 0))
        reference = fases_referencia(cap, s0)
        for index in range(1 + 2 * frames):
            phase, expected, phase_integrity = next(reference)
            name = phase['phase']
            phase_id = 1 if index == 0 else 2 if index % 2 else 3
            if index == 1:
                inp.registers = FrameRegisters.from_values({k: int(v, 16) for k, v in phase['entry']['registers'].items()})
            carried_check = None
            if index > 2 and phase_id == 2:
                carried_check = {k: dict(rust=hex(v), reference=phase['entry']['registers'][k],
                                         equal=hex(v) == phase['entry']['registers'][k])
                                 for k, v in inp.registers.values().items() if k != 'EAX'}
            tick_before = rust.clock(handle)[0]
            t0 = time.perf_counter()
            try:
                rust.frame(handle, phase_id, inp)
            except RuntimeError as error:
                runtime += time.perf_counter() - t0
                results.append(dict(phase=name, equal=False, result='dependency_stop', message=str(error)))
                break
            runtime += time.perf_counter() - t0
            raw_projection = rust.snapshot(handle)
            static_equal = all(raw_projection.get(a) == b for a, b in static.items())
            actual = named_snapshot({a: b for a, b in raw_projection.items() if a not in static}, names)
            events = rust.events(handle)
            bindings, boundaries, frees = normalize_events(events, name, cursor)
            state = comparar_estado(mask, actual, expected)
            state['mismatched_bytes'] = mismatch_bytes(mask, actual, expected)
            tick_after = rust.clock(handle)[0]
            result = dict(phase=name, result='returned', state=state, immutable_tables_equal=static_equal, reference_integrity=phase_integrity,
                          clock=dict(before=tick_before, after=tick_after,
                                     equal=tick_after == tick_before + (phase_id in (1, 3))))
            rng = {a: hex(ler_estado(actual, int(a, 16), 4)) for a in ('0x497164', '0x498db4')}
            result['rng'] = dict(rust=rng, reference=phase['exit']['rng'], equal=rng == phase['exit']['rng'])
            if phase_id == 2:
                result['registers'] = {k: dict(rust=hex(v), reference=phase['exit']['registers'][k],
                                              equal=hex(v) == phase['exit']['registers'][k])
                                       for k, v in inp.registers.values().items()}
            if carried_check is not None:
                result['carried_entry_registers'] = carried_check
            if not state_only:
                result['bindings'] = comparar_eventos_fase(bindings, phase['bindings'], context.vinculo,
                                                            VINCULO, 'bindings')
                result['boundaries'] = comparar_eventos_fase(boundaries, phase['boundaries'], context.fronteira,
                                                              FRONTEIRA, 'boundaries')
                result['negative_controls'] = reject_mutated_events(bindings, boundaries, phase, context)
                update_allocations(records, events, rust.snapshot(handle, freed=True))
                result['allocation_count'] = dict(rust=len(records), reference=phase['exit']['allocations'],
                                                  equal=len(records) == phase['exit']['allocations'])
            bools = [static_equal, state['equal'], result['rng']['equal'], result['clock']['equal']]
            bools += [v['equal'] for v in result.get('registers', {}).values()]
            bools += [v['equal'] for v in result.get('carried_entry_registers', {}).values()]
            if not state_only:
                bools += [result[k]['equal'] for k in ('bindings', 'boundaries', 'allocation_count')]
            result['equal'] = all(bools)
            results.append(result)
            print(name, 'equal' if result['equal'] else 'DIFFERENT', flush=True)
            if not result['equal']:
                break
        allocation_result = comparar_alocacoes(records, cap['allocations']) if not state_only else None
    finally:
        rust.free(handle)
    frames_completed = sum(1 for r in results if r['result'] == 'returned' and r['phase'].startswith('frame'))
    equal = len(results) == 1 + 2 * frames and all(r['equal'] for r in results)
    equal = equal and (state_only or allocation_result['equal'])
    return dict(schema='rising-lands/rust-engine-frame-differential/1', reference_snapshot=provenance(),
                original_sha256=ambiente_ia_runtime.ORIGINAL_SHA256,
                library=library_identity,
                original_executable_input=str(original),
                immutable_table_inputs=[dict(address=hex(a), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
                                        for a, b in static.items()],
                references={str(p.relative_to(ROOT)): sha(p) for p in
                            (M1_ENTRY, M1_CAPTURE, capture_path, policy_path)}, raw_capture_sha256=raw_sha,
                policy=dict(path=str(policy_path.relative_to(ROOT)), masked_bytes=mask.bytes, ranges=len(ranges)),
                capture_integrity=dict(phases_replayed=len(integrity), all_equal=True),
                comparison_scope='state_only_diagnostic' if state_only else 'state_events_registers_allocations',
                phases=results, allocation_records=allocation_result, mutation_checks=checks,
                timing=dict(rust_phase_seconds=runtime, frames_completed=frames_completed,
                            frames_per_second=(frames_completed / runtime if runtime else None),
                            scope='C ABI phase execution only; excludes corpus replay, projection and comparison'),
                summary=dict(result='equal' if equal else 'different_or_stopped', phases_equal=sum(r['equal'] for r in results),
                             phases_compared=len(results), phases_requested=1 + 2 * frames,
                             complete_proof=equal and not state_only))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--library')
    ap.add_argument('--executable', help='read-only intact RISING.EXE (or RL_ORIGINAL_EXE)')
    ap.add_argument('--frames', type=int, default=1)
    ap.add_argument('--m22', action='store_true', help='use 128-frame corpus and cumulative published mask')
    ap.add_argument('--state-only', action='store_true', help='diagnostic: do not claim event/allocation proof')
    ap.add_argument('--output', required=True)
    a = ap.parse_args()
    output = Path(a.output).resolve()
    if output.exists():
        raise SystemExit('Refusing to overwrite evidence: ' + str(output))
    t0 = time.monotonic()
    sources = sorted(list((ROOT / 'motor/crates').rglob('*.rs')) +
                     list((ROOT / 'motor/include').glob('*')) +
                     list((ROOT / 'motor/testes').glob('frame_*.py')) +
                     list((ROOT / 'motor/testes').glob('test_frame*.py')))
    before = {str(p.relative_to(ROOT)): sha(p) for p in sources if p.is_file()}
    report = compare(a.library, a.frames, a.m22, a.state_only, a.executable)
    after = {str(p.relative_to(ROOT)): sha(p) for p in sources if p.is_file()}
    report['engine_source_sha256'] = before
    report['engine_sources_unchanged_during_run'] = before == after
    if before != after:
        report['summary'].update(result='source_changed_during_run', complete_proof=False)
    report['source_revision'] = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    report['source_dirty_paths'] = subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True).splitlines()
    report['wall_seconds'] = time.monotonic() - t0
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        json.dump(report, stream, indent=1, sort_keys=True)
        stream.write('\n')
    print(json.dumps(dict(output=str(output), **report['summary'], timing=report['timing']), indent=1))
    return 0 if report['summary']['complete_proof'] else 2


if __name__ == '__main__':
    sys.exit(main())
