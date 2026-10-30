"""App-order C ABI benchmark: render, between_frames, CalculGame, generation.

No per-frame hashes, world exports, cache exports, Python render or phase audit
queries. Initialization is separate. The optional macOS sample process profiles
the same ABI loop, and its overhead is declared in the report.
"""
import argparse
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import signal
import statistics
import subprocess
import time
from render_proof import live
from render_abi import Render, initial, ROOT


def distribution(values):
    ordered = sorted(values)
    return dict(count=len(values), seconds=sum(values),
                mean_ms=1000 * statistics.mean(values),
                p50_ms=1000 * statistics.median(values),
                p95_ms=1000 * ordered[min(len(values)-1, int(len(values)*.95))],
                p99_ms=1000 * ordered[min(len(values)-1, int(len(values)*.99))],
                max_ms=1000 * max(values))


def run(library, frames, mode, sample_path=None):
    # This comparative harness deliberately supports the preserved ABI1.5 baseline
    # and the new additive ABI1.6 library; ordinary proof loaders stay strict.
    import frame_abi, pilot_abi
    probe = C.CDLL(str(Path(library).resolve()))
    probe.rl_versao.restype = C.c_uint32
    version = probe.rl_versao()
    if version not in (0x10005, 0x10006): raise ValueError('Unsupported benchmark ABI')
    frame_abi.FRAME_VERSION = pilot_abi.VERSION = version
    started = time.monotonic()
    f, world, inp = live(library)
    r = Render(f)
    surface, cache = initial()
    renderer = r.create(world, surface, cache)
    if mode is not None:
        f.lib.rl_execucao_definir.argtypes = [C.c_uint64, C.c_uint32]
        f.lib.rl_execucao_definir.restype = C.c_int32
        f.check(f.lib.rl_execucao_definir(world, mode))
    initialization = time.monotonic() - started
    sampler = None
    if sample_path:
        sampler = subprocess.Popen(['/usr/bin/sample', str(os.getpid()), '3', '1',
                                    '-file', str(Path(sample_path).resolve())],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('ABI play loop ready: pid', os.getpid(), 'frames', frames, flush=True)
    phase2, phase3, render, generation, total = [], [], [], [], []
    try:
        for index in range(frames):
            begin = time.perf_counter()
            t = time.perf_counter(); gen, _, _ = r.generation(world); gt = time.perf_counter()-t
            t = time.perf_counter(); out = r.draw(renderer, gen); render.append(time.perf_counter()-t)
            if out.disposition != 0 or out.abi_status:
                raise ValueError(('Render stop', index, out.disposition, hex(out.stop_address)))
            t = time.perf_counter(); f.frame(world, 2, inp); phase2.append(time.perf_counter()-t)
            t = time.perf_counter(); f.frame(world, 3, inp); phase3.append(time.perf_counter()-t)
            t = time.perf_counter(); last = r.generation(world); gt += time.perf_counter()-t
            generation.append(gt); total.append(time.perf_counter()-begin)
        final_surface_sha256 = hashlib.sha256(bytes(r.pixels)).hexdigest()
        final_projection = f.snapshot(world)
        state_hash = hashlib.sha256()
        import struct
        for address,data in sorted(final_projection.items()):
            state_hash.update(struct.pack('<II',address,len(data)));state_hash.update(data)
        final_state_sha256 = state_hash.hexdigest()
        final_clock = f.clock(world)
    finally:
        if sampler is not None:
            sampler.wait(timeout=30)
        r.free(renderer); f.free(world)
    logic = [a+b for a,b in zip(phase2, phase3)]
    pipeline = [a+b for a,b in zip(logic, render)]
    return dict(schema='rising-lands/native-abi-play-benchmark/1',
                frames=frames, mode='legacy audit' if mode is None else mode,
                initialization_seconds=initialization,
                abi=f.lib.rl_versao(), sample=sample_path,
                phases=dict(between_frames=distribution(phase2), CalculGame=distribution(phase3),
                            logic=distribution(logic), render=distribution(render),
                            generation=distribution(generation),
                            logic_render=distribution(pipeline), loop=distribution(total)),
                fps=dict(logic=frames/sum(logic), render=frames/sum(render),
                         logic_render=frames/sum(pipeline), loop=frames/sum(total)),
                final_generation=last[0], final_phase=last[1], final_counter=last[2],
                final_surface_sha256=final_surface_sha256,final_state_sha256=final_state_sha256,final_clock=final_clock,
                scope='Release C ABI in app play order, reused caller buffers, hud=True; '
                      'excludes initialization, audit/export/hash work and presentation. '
                      'Phase timers include ctypes call overhead. Optional sampling overhead is included.')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--library', required=True)
    ap.add_argument('--frames', type=int, default=9200)
    ap.add_argument('--mode', type=int, choices=(0, 1, 2)); ap.add_argument('--sample')
    ap.add_argument('--output', required=True); a = ap.parse_args()
    if a.frames < 9200: raise ValueError('Sustained benchmark requires at least 9200 frames')
    output = Path(a.output)
    if output.exists(): raise ValueError('Refusing overwrite')
    signal.alarm(1140)
    library = Path(a.library).resolve(); before = hashlib.sha256(library.read_bytes()).hexdigest()
    report = run(str(library), a.frames, a.mode, a.sample)
    after = hashlib.sha256(library.read_bytes()).hexdigest()
    if before != after: raise ValueError('Benchmark library changed during execution')
    report.update(library_sha256=before, source_revision=subprocess.check_output(
        ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(fps=report['fps'], means_ms={k:v['mean_ms'] for k,v in report['phases'].items()}), indent=2))


if __name__ == '__main__': main()
