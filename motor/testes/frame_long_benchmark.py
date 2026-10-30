"""Supplemental serial S0->9200 benchmark; this is not the 18,401-phase proof.

No snapshot/export/reference comparison runs during the 9200 timed phase pairs.
Run under an exclusive heavy lease. Every reference remains read-only.
"""
import argparse
import copy
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import sys
import time

from frame_long_evidence import *
from frame_long_differential import source_hashes, metadata, write_json, state_value


def benchmark(library=None, executable=None, frames=9200):
    if frames != 9200:
        raise ValueError('This supplement has the exact original 9200-frame endpoint')
    manifest = load_manifest()
    policy = carregar_json(POLICY)
    mask = MascaraEnderecos(policy['cumulative']['exclusion_mask'])
    part0 = load_part(manifest, 0)
    part9 = load_part(manifest, 9)
    reference = opening(part9, mask)
    replayed = 0
    for phase, reference, integrity in fases_referencia(part9, reference, mask):
        replayed += 1
    if phase['phase'] != 'frame9200':
        raise ValueError('Final reference phase differs')
    s0, records, _, short = mission_inputs()
    records = copy.deepcopy(records)
    if opening(part0, mask) != s0:
        raise ValueError('Long opening differs from accepted M1')
    original = Path(executable or os.environ.get('RL_ORIGINAL_EXE',str(ROOT.parent/'source/cd/INSTALHD/RISING.EXE'))).resolve()
    image = OriginalImage(original, original.with_suffix('.SBL'))
    static = static_inputs(image,s0)
    rust = Frames(library)
    lib = dict(path=str(rust.path),bytes=rust.path.stat().st_size,sha256=sha(rust.path),
               profile='release' if 'release' in rust.path.parts else 'debug_or_other')
    cursor = tuple(part0['named_inputs']['frame']['cursor'])
    surface = next(s for s in short['phases'][0]['display_state']['surfaces'] if s['role']=='offscreen')
    keys = ('EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP')
    regs = {k:int(part0['phases'][0]['entry']['registers'][k],16) for k in keys}
    inp = FrameInput(cursor[0],cursor[1],int(surface['pixels'],16),FrameRegisters.from_values(regs),
                     (C.c_uint32*3)(0,0,0),(C.c_uint32*4)(0x3000000,0,0,0))
    handle = rust.create()
    seconds, completed, error = 0.0, 0, None
    try:
        rust.load(handle,sorted(list(s0.values())+list(static.items())))
        t0 = time.perf_counter()
        try:
            rust.frame(handle,1,inp)
        except RuntimeError as failure:
            error = dict(phase='load_tail',message=str(failure))
        seconds += time.perf_counter()-t0
        if error is None:
            # Capture original-order bank frees without charging export/hashing
            # to Rust frame throughput. This happens before the timed loop.
            update_allocations(records,rust.events(handle),rust.snapshot(handle,freed=True))
            inp.registers = FrameRegisters.from_values({k:int(part0['phases'][1]['entry']['registers'][k],16) for k in keys})
            t0 = time.perf_counter()
            try:
                for frame in range(1,frames+1):
                    current_phase = 'between_frames' if frame==1 else f'between_frames{frame}'
                    rust.frame(handle,2,inp)
                    current_phase = f'frame{frame}'
                    rust.frame(handle,3,inp)
                    completed = frame
            except RuntimeError as failure:
                error = dict(phase=current_phase,message=str(failure))
            seconds += time.perf_counter()-t0
        raw = rust.snapshot(handle)
        names = {a:n for n,(a,_) in s0.items()}
        actual = named_snapshot({a:b for a,b in raw.items() if a not in static},names)
        clock = rust.clock(handle)
        state = comparar_estado(mask,actual,reference) if error is None else None
        if state is not None:
            state['mismatched_bytes'] = mismatch_bytes(mask,actual,reference)
            compared,_ = resumos_mascarados(mask,actual)
            state['compared_summary_equal'] = compared == phase['state_after']['compared_summary']
        allocations = comparar_alocacoes(records,part9['allocations'])
        rng = {a:hex(state_value(actual,int(a,16),4)) for a in ('0x497164','0x498db4')}
        immutable = all(raw.get(a)==b for a,b in static.items())
    finally:
        rust.free(handle)
    equal = (error is None and completed==9200 and clock[0]==9201 and state['equal']
             and state['compared_summary_equal'] and allocations['equal'] and immutable
             and rng==phase['exit']['rng'])
    return dict(schema='rising-lands/rust-engine-long-serial-benchmark/1',
                claim='Supplemental serial throughput and endpoint equality; not per-phase proof',
                manifest=dict(path=str(MANIFEST.relative_to(ROOT)),sha256=PINS[MANIFEST]),policy=manifest['policy'],
                original_executable_input=str(original),original_sha256=part0['original_sha256'],library=lib,
                inputs=dict(source='accepted display MissionLoad S0; only first between-frame registers are declared',
                            no_reference_checkpoint_reload=True,cursor=list(cursor),offscreen=surface['pixels'],
                            saved=[0,0,0],msg=[0x3000000,0,0,0]),
                capture_integrity=dict(final_part_phases_replayed=replayed,all_equal=True),
                state=state,allocation_records=allocations,immutable_tables_equal=immutable,
                rng=dict(rust=rng,reference=phase['exit']['rng'],equal=rng==phase['exit']['rng']),
                clock=dict(tick=clock[0],milliseconds=clock[1],expected_tick=9201,equal=clock[0]==9201),
                first_stop=error,
                timing=dict(frames_completed=completed,rust_phase_seconds=seconds,frames_per_second=completed/seconds if seconds else None,
                            scope='C ABI phase1 and9200 phase2/3pairs including Python call overhead; no timed exports/comparisons/rendering'),
                summary=dict(result='equal' if equal else 'different_or_stopped',complete_endpoint=equal,complete_phase_proof=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--library');ap.add_argument('--executable');ap.add_argument('--output',required=True)
    a = ap.parse_args()
    if Path(a.output).exists():
        raise SystemExit('Refusing to overwrite '+a.output)
    before = source_hashes()
    report = benchmark(a.library,a.executable)
    after = source_hashes()
    report.update(metadata(),engine_source_sha256=before,engine_sources_unchanged_during_run=before==after)
    if before != after:
        report['summary'].update(result='source_changed_during_run',complete_endpoint=False)
    write_json(a.output,report)
    print(json.dumps(dict(output=a.output,summary=report['summary'],timing=report['timing'],first_stop=report['first_stop']),indent=1))
    return 0 if report['summary']['complete_endpoint'] else 2


if __name__=='__main__':
    sys.exit(main())
