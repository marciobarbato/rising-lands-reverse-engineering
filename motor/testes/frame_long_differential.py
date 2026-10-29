"""0..9200 Rust proof in bounded original-evidence shards (wrap each job in the heavy lease).

verify: package pins/hash chain; part: one independent opening or a serial continuation;
aggregate: all ten equal complete shards. --start-frame/--max-phases are diagnostics.
--serial runs one part per invocation, carrying actual Rust bytes/clock/registers in
an explicitly hashed checkpoint. It never substitutes a later original state.
"""
import argparse
import base64
import bisect
import copy
import ctypes as C
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import time
import zlib

from frame_long_evidence import *  # imports only reviewed offline helpers


def read_json(path):
    raw = Path(path).read_bytes()
    return json.loads(lzma.decompress(raw) if str(path).endswith('.xz') else raw)


def write_json(path, report):
    path = Path(path).resolve()
    if path.exists():
        raise ValueError('Refusing to overwrite ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(report, indent=1, sort_keys=True) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(lzma.compress(raw) if str(path).endswith('.xz') else raw)


def source_hashes():
    paths = list((ROOT / 'motor/crates').rglob('*.rs')) + list((ROOT / 'motor/include').glob('*'))
    paths += list((ROOT / 'motor/testes').glob('*.py'))
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(paths) if p.is_file()}


def metadata():
    return dict(source_revision=subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
                source_dirty_paths=subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True).splitlines())


def state_value(state, address, width):
    base, data = state['dgroup']
    if not base <= address < address + width <= base + len(data):
        raise ValueError('Expected DGROUP field is outside its declared block')
    return int.from_bytes(data[address - base:address - base + width], 'little')


def pack_state(state):
    return {name: dict(base=hex(a), zlib_base64=base64.b64encode(zlib.compress(b)).decode())
            for name, (a, b) in state.items()}


def unpack_state(state):
    return {name: (int(block['base'], 16), _decode(block)) for name, block in state.items()}


def _decode(block):
    return zlib.decompress(base64.b64decode(block['zlib_base64']))


def checkpoint(path, world, handle, inputs, names, static, records, part, library):
    raw = world.snapshot(handle)
    state = named_snapshot({a: b for a, b in raw.items() if a not in static}, names)
    tick, ms = world.clock(handle)
    data = dict(schema='rising-lands/rust-engine-long-serial-checkpoint/1', after_part=part,
                last_frame=load_manifest()['parts'][part]['frames'][1], library=library,
                full_state=pack_state(state), summary=resumo_estado(state), allocation_records=records,
                registers=inputs.registers.values(), saved=list(inputs.saved), msg=list(inputs.msg),
                cursor=[inputs.cursor_x, inputs.cursor_y], offscreen=inputs.offscreen, tick=tick, milliseconds=ms,
                immutable_inputs=[dict(base=hex(a), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b)) for a, b in static.items()])
    write_json(path, data)
    return dict(path=str(Path(path).resolve()), sha256=sha(Path(path)), after_frame=data['last_frame'])


def run_part(number, library=None, executable=None, start_frame=None, max_phases=None,
             serial=False, resume=None, checkpoint_out=None):
    t0 = time.monotonic()
    manifest = load_manifest()
    policy = carregar_json(POLICY)
    mask = MascaraEnderecos(policy['cumulative']['exclusion_mask'])
    part = load_part(manifest, number)
    allocator = allocator_invariants(part)
    state = opening(part, mask)
    s0, m1_records, post_records, short = mission_inputs()
    if number == 0 and state != s0:
        raise ValueError('Part 0 opening differs from accepted MissionLoad S0')
    refs = fases_referencia(part, state, mask)
    skipped, replayed, full_checks = [], 0, []
    if start_frame is not None:
        if serial or not part['frames'][0] <= start_frame < part['frames'][1]:
            raise ValueError('--start-frame must be an in-part checkpoint and cannot be serial')
        if start_frame == 0:
            raise ValueError('Frame0 checkpoint must be selected after its load_tail, not before it')
        found = False
        while not found:
            ph, state, integrity = next(refs)
            skipped.append(ph['phase'])
            replayed += 1
            found = ph['phase'] == f'frame{start_frame}'
        first_index = len(skipped)
    else:
        first_index = 0
    selected = part['phases'][first_index:]
    if max_phases is not None:
        if max_phases <= 0:
            raise ValueError('--max-phases must be positive')
        selected = selected[:max_phases]
    first = selected[0]
    named = part.get('named_inputs') or short['named_inputs']
    cursor = tuple(named['frame']['cursor'])
    surface = next(s for s in short['phases'][0]['display_state']['surfaces'] if s['role'] == 'offscreen')
    original = Path(executable or os.environ.get('RL_ORIGINAL_EXE', str(ROOT.parent / 'source/cd/INSTALHD/RISING.EXE'))).resolve()
    image = OriginalImage(original, original.with_suffix('.SBL'))
    context = ContextoExibicao(image, policy['display_roots'])
    static = static_inputs(image, state)
    rust = Frames(library)
    lib = dict(path=str(rust.path), bytes=rust.path.stat().st_size, sha256=sha(rust.path),
               profile='release' if 'release' in rust.path.parts else 'debug_or_other')
    records = copy.deepcopy(m1_records if first['phase'] == 'load_tail' else post_records)
    regs = {k: int(first['entry']['registers'][k], 16) for k in ('EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP')}
    inp = FrameInput(cursor[0], cursor[1], int(surface['pixels'], 16), FrameRegisters.from_values(regs),
                     (C.c_uint32 * 3)(0,0,0), (C.c_uint32 * 4)(0x3000000,0,0,0))
    start_tick = 0 if first['phase'] == 'load_tail' else phase_frame(first['phase'])
    resume_identity = None
    if serial and number > 0 and resume is None:
        raise ValueError('A serial continuation requires the previous actual Rust checkpoint')
    if resume is not None:
        if not serial or number == 0 or start_frame is not None:
            raise ValueError('Resume is only valid for a later whole serial part')
        saved = read_json(resume)
        if (saved['schema'] != 'rising-lands/rust-engine-long-serial-checkpoint/1'
                or saved['after_part'] != number - 1 or saved['last_frame'] != part['frames'][0] - 1
                or saved['library']['sha256'] != lib['sha256']):
            raise ValueError('Serial checkpoint identity/library/bounds differ')
        actual_start = unpack_state(saved['full_state'])
        if resumo_estado(actual_start) != saved['summary'] or not comparar_estado(mask, actual_start, state)['equal']:
            raise ValueError('Serial checkpoint is corrupt or differs from expected compared opening state')
        state = actual_start
        records = saved['allocation_records']
        inp.registers = FrameRegisters.from_values(saved['registers'])
        inp.saved = (C.c_uint32 * 3)(*saved['saved'])
        inp.msg = (C.c_uint32 * 4)(*saved['msg'])
        if tuple(saved['cursor']) != cursor or saved['offscreen'] != inp.offscreen:
            raise ValueError('Serial declared host inputs differ')
        start_tick = saved['tick']
        resume_identity = dict(path=str(Path(resume).resolve()), sha256=sha(Path(resume)), after_frame=saved['last_frame'])
    names = {a: n for n, (a, _) in state.items()}
    handle = rust.create()
    results, runtime = [], 0.0
    checks = {}
    try:
        rust.load(handle, sorted(list(state.values()) + list(static.items())))
        if start_tick:
            rust.check(rust.lib.rl_avancar_ticks(handle, start_tick))
        raw = rust.snapshot(handle)
        initial = named_snapshot({a: b for a, b in raw.items() if a not in static}, names)
        if initial != state or any(raw.get(a) != b for a, b in static.items()):
            raise AssertionError('Checkpoint load/project identity differs')
        checks['projected_byte_mutation'] = check_mutation_detection(mask, initial)
        for index, wanted in enumerate(selected):
            ph, expected, integrity = next(refs)
            replayed += 1
            name = ph['phase']
            if name != wanted['phase']:
                raise ValueError('Reference replay phase order differs')
            if integrity.get('checkpoint_full_state_equal'):
                full_checks.append(name)
            phase_id = 1 if name == 'load_tail' else 2 if name.startswith('between_frames') else 3
            if number == 0 and name == 'between_frames' and not start_frame:
                inp.registers = FrameRegisters.from_values({k: int(ph['entry']['registers'][k], 16) for k in regs})
            carried = None
            if phase_id == 2 and (index > 0 or serial and number > 0):
                carried = {k: dict(rust=hex(v), reference=ph['entry']['registers'][k], equal=hex(v) == ph['entry']['registers'][k])
                           for k, v in inp.registers.values().items() if k != 'EAX'}
            before = rust.clock(handle)[0]
            t_step = time.perf_counter()
            try:
                rust.frame(handle, phase_id, inp)
            except RuntimeError as error:
                runtime += time.perf_counter() - t_step
                results.append(dict(phase=name, equal=False, result='dependency_stop', message=str(error), reference_integrity=integrity))
                break
            runtime += time.perf_counter() - t_step
            raw = rust.snapshot(handle)
            immutable = all(raw.get(a) == b for a, b in static.items())
            actual = named_snapshot({a: b for a, b in raw.items() if a not in static}, names)
            comparison = comparar_estado(mask, actual, expected)
            comparison['mismatched_bytes'] = mismatch_bytes(mask, actual, expected)
            compared, _ = resumos_mascarados(mask, actual)
            comparison['compared_summary_equal'] = compared == ph['state_after']['compared_summary']
            rng = {a: hex(state_value(actual, int(a, 16), 4)) for a in ('0x497164','0x498db4')}
            events = rust.events(handle)
            bindings, boundaries, _ = normalize_events(events, name, cursor)
            result = dict(phase=name, result='returned', state=comparison, reference_integrity=integrity,
                          immutable_tables_equal=immutable, rng=dict(rust=rng, reference=ph['exit']['rng'], equal=rng == ph['exit']['rng']),
                          bindings=comparar_eventos_fase(bindings, ph['bindings'], context.vinculo, VINCULO, 'bindings'),
                          boundaries=comparar_eventos_fase(boundaries, ph['boundaries'], context.fronteira, FRONTEIRA, 'boundaries'),
                          negative_controls=reject_mutated_events(bindings, boundaries, ph, context),
                          clock=dict(before=before, after=rust.clock(handle)[0], equal=rust.clock(handle)[0] == before + (phase_id != 2)))
            if any(e.kind == 3 or e.kind == 1 and e.id in (3,4,5) for e in events):
                update_allocations(records, events, rust.snapshot(handle, freed=True))
            elif rust.snapshot(handle, freed=True):
                raise AssertionError('Freed bytes were exposed without matching allocator events')
            result['allocation_count'] = dict(rust=len(records), reference=ph['exit']['allocations'], equal=len(records) == ph['exit']['allocations'])
            if phase_id == 2:
                result['registers'] = {k: dict(rust=hex(v), reference=ph['exit']['registers'][k], equal=hex(v) == ph['exit']['registers'][k])
                                       for k, v in inp.registers.values().items()}
            if carried is not None:
                result['carried_entry_registers'] = carried
            booleans = [immutable, comparison['equal'], comparison['compared_summary_equal']]
            booleans += [result[k]['equal'] for k in ('rng','bindings','boundaries','clock','allocation_count')]
            booleans += [v['equal'] for section in ('registers','carried_entry_registers') for v in result.get(section, {}).values()]
            result['equal'] = all(booleans)
            results.append(result)
            if not result['equal'] or index % 100 == 0 or index + 1 == len(selected):
                print(f'part{number:02d} {name}: ' + ('equal' if result['equal'] else 'DIFFERENT'), flush=True)
            if not result['equal']:
                break
        all_equal = len(results) == len(selected) and all(r['equal'] for r in results)
        allocation_expected = part.get('allocations') or post_records
        allocations = comparar_alocacoes(records, allocation_expected)
        all_equal = all_equal and allocations['equal']
        output_checkpoint = None
        complete_part = first_index == 0 and len(selected) == len(part['phases']) and all_equal
        if checkpoint_out is not None:
            if not serial or not complete_part:
                raise ValueError('Only a complete equal serial part may write a continuation checkpoint')
            output_checkpoint = checkpoint(checkpoint_out, rust, handle, inp, names, static, records, number, lib)
    finally:
        rust.free(handle)
    frames = sum(r.get('result') == 'returned' and r['phase'].startswith('frame') for r in results)
    return dict(schema='rising-lands/rust-engine-long-part-proof/1', library=lib,
                manifest=dict(path=str(MANIFEST.relative_to(ROOT)), sha256=PINS[MANIFEST]), policy=manifest['policy'],
                part=dict(number=number, artifact=manifest['parts'][number]['artifact'], raw_sha256=manifest['parts'][number]['raw_sha256'],
                          frames=part['frames'], first_phase=selected[0]['phase'], last_phase=selected[-1]['phase'],
                          expected_phases=len(part['phases']), opening={k:part['opening_state'][k] for k in HASH_FIELDS},
                          ending={k:part['phases'][-1]['state_after'][k] for k in HASH_FIELDS}),
                scope='serial_from_S0' if serial else 'declared_opening_checkpoint',
                diagnostic=dict(start_frame=start_frame, max_phases=max_phases),
                checkpoint_input=resume_identity, checkpoint_output=output_checkpoint,
                original_executable_input=str(original), original_sha256=part['original_sha256'],
                immutable_table_inputs=[dict(address=hex(a), bytes=len(b), sha256=hashlib.sha256(b).hexdigest()) for a,b in static.items()],
                phases=results, allocation_records=allocations, allocator_contract=allocator, mutation_checks=checks,
                capture_integrity=dict(phases_replayed=replayed, checkpoints_checked=full_checks, skipped_to_checkpoint=skipped),
                timing=dict(rust_phase_seconds=runtime, frames_completed=frames, frames_per_second=frames/runtime if runtime else None,
                            wall_seconds=time.monotonic()-t0,
                            scope='C ABI phase execution including private projection; excludes export/comparison/rendering'),
                summary=dict(result='equal' if all_equal else 'different_or_stopped', phases_compared=len(results),
                             phases_equal=sum(r['equal'] for r in results), complete_part=complete_part))


def aggregate(paths, plan, serial=False):
    manifest = load_manifest()
    if plan['manifest']['sha256'] != PINS[MANIFEST] or plan['summary']['result'] != 'verified':
        raise ValueError('Package verification plan identity/result differs')
    reports = sorted((read_json(p) for p in paths), key=lambda r:r['part']['number'])
    if [r['part']['number'] for r in reports] != list(range(10)):
        raise ValueError('Exactly one complete report for each of ten parts is required')
    identity = reports[0]['library']['sha256']
    sources = reports[0].get('engine_source_sha256')
    rows, total, equal, seconds, frames = [], 0, 0, 0.0, 0
    previous = None
    for r, expected in zip(reports, manifest['parts']):
        problems = []
        n = expected['part']
        if r['manifest']['sha256'] != PINS[MANIFEST] or r['policy'] != manifest['policy'] or r['part']['raw_sha256'] != expected['raw_sha256']:
            problems.append('input identity differs')
        if not r['summary']['complete_part'] or r['summary']['phases_equal'] != expected['phases'] or len(r['phases']) != expected['phases']:
            problems.append('part is incomplete or differs')
        if (r['part']['first_phase'],r['part']['last_phase']) != (expected['first_phase'],expected['last_phase']):
            problems.append('part phase coverage differs')
        if r['library']['sha256'] != identity or r.get('engine_source_sha256') != sources or not r.get('engine_sources_unchanged_during_run'):
            problems.append('library/source identity differs or changed')
        if r.get('source_dirty_paths'):
            problems.append('part was run from a dirty checkout')
        if not r['allocation_records']['equal']:
            problems.append('full allocation records differ')
        if serial:
            if r['scope'] != 'serial_from_S0' or n == 0 and r['checkpoint_input'] is not None:
                problems.append('not a serial S0 chain')
            if previous is not None and (not previous['checkpoint_output'] or not r['checkpoint_input'] or
                                        previous['checkpoint_output']['sha256'] != r['checkpoint_input']['sha256']):
                problems.append('actual Rust continuation checkpoint chain differs')
        if previous is not None and any(r['part']['opening'][k] != previous['part']['ending'][k] for k in HASH_FIELDS):
            problems.append('original opening/final hash chain differs')
        total += r['summary']['phases_compared']
        equal += r['summary']['phases_equal']
        seconds += r['timing']['rust_phase_seconds']
        frames += r['timing']['frames_completed']
        rows.append(dict(part=n, equal=not problems, problems=problems, phases=r['summary']['phases_compared']))
        previous = r
    passed = all(row['equal'] for row in rows) and total == equal == 18401 and frames == 9200
    return dict(schema='rising-lands/rust-engine-long-aggregate-proof/1', manifest=plan['manifest'], policy=manifest['policy'],
                scope='serial_from_S0' if serial else 'ten_declared_opening_checkpoints', parts=rows, library_sha256=identity,
                input_reports=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p))) for p in paths],
                timing=dict(rust_phase_seconds=seconds, frames_completed=frames, frames_per_second=frames/seconds if seconds else None),
                summary=dict(result='equal' if passed else 'incomplete_or_different', phases=total, phases_equal=equal, complete_proof=passed))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    v = sub.add_parser('verify'); v.add_argument('--output', required=True)
    p = sub.add_parser('part')
    p.add_argument('--part', type=int, choices=range(10), required=True)
    p.add_argument('--library'); p.add_argument('--executable'); p.add_argument('--start-frame', type=int)
    p.add_argument('--max-phases', type=int); p.add_argument('--serial', action='store_true')
    p.add_argument('--resume'); p.add_argument('--checkpoint-out'); p.add_argument('--output', required=True)
    g = sub.add_parser('aggregate'); g.add_argument('--reports', nargs=10, required=True)
    g.add_argument('--plan', required=True); g.add_argument('--serial', action='store_true'); g.add_argument('--output', required=True)
    a = ap.parse_args()
    if Path(a.output).exists():
        raise SystemExit('Refusing to overwrite ' + a.output)
    before = source_hashes()
    if a.command == 'verify':
        report = verify_packages()
    elif a.command == 'part':
        report = run_part(a.part,a.library,a.executable,a.start_frame,a.max_phases,a.serial,a.resume,a.checkpoint_out)
    else:
        report = aggregate(a.reports,read_json(a.plan),a.serial)
    after = source_hashes()
    report.update(metadata(),engine_source_sha256=before,engine_sources_unchanged_during_run=before==after)
    if before != after and a.command == 'part':
        report['summary'].update(result='source_changed_during_run',complete_proof=False,complete_part=False)
    write_json(a.output,report)
    print(json.dumps(dict(output=a.output,summary=report['summary'],timing=report.get('timing')),indent=1))
    return 0 if report['summary']['result'] in ('equal','verified') else 2


if __name__ == '__main__':
    sys.exit(main())
