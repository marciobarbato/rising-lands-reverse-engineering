"""Bounded original-only S1 render-entry evidence, before any new render translation.

Restore a native checkpoint, compare its opening state and every following state and
both phase surfaces with published S1, and record complete AffGame entry inputs.
No translated renderer executes. All eight hundred unit records are retained.
"""
import argparse
import hashlib
import json
import lzma
import signal
import subprocess
import time
from pathlib import Path

import capturar_sondas_graficos_m3 as original
from inventariar_janelas_s1_graficos import S1_REF, S1_ROOT, arquivo, registros


def main(a):
    signal.alarm(1140)  # Whole invocation, including serialization, remains below 20 minutes.
    output = Path(a.output)
    if output.exists():
        raise FileExistsError(output)
    started = time.monotonic()
    ref = subprocess.check_output(['git', 'rev-parse', a.ref], text=True).strip()
    original.REF = ref
    module = original.modulo_entrada()
    b, _, start = module.abrir(a.start, Path(a.resume) if a.resume else None)
    if not 0 < a.to - start <= 750 or a.to > 17031:
        raise ValueError('Require 1..750 gameplay frames, ending before MenuInit(0x13)')
    refs = registros(ref)
    schedule = arquivo(ref, S1_ROOT + 'entradas/S1.json')
    b.roteiro.quadros = module.carregar_entrada(json.loads(schedule))[0]
    opening = b.resumo_imagem(b.imagem())['sha256']
    if start != 128 and opening != refs[start]['state_sha256']:
        raise RuntimeError('Opening checkpoint is not the published S1 state')
    if start == 128:
        manifest = json.loads((Path(a.start) / 'manifesto.json').read_text())
        if original.sha((Path(a.start) / manifest['snapshot']).read_bytes()) != manifest['snapshot_sha256']:
            raise RuntimeError('Frame-128 checkpoint differs from its manifest')
    checkpoint_input = Path(a.resume) if a.resume else Path(a.start) / manifest['snapshot']
    cap = original.CapturadorSondasGraficos(b)
    checks = []
    status = 'complete'
    for k in range(start + 1, a.to + 1):
        b.roteiro.iniciar_quadro(k)
        cap.phase_frame = k
        b.executar_entre_quadros(300, k)
        between = original.sha(b.directdraw.pixels('offscreen'))
        drawn = cap.rows[-1] if cap.rows and cap.rows[-1]['frame'] == k else None
        if drawn is None or drawn['after'] != between or between != refs[k]['surfaces_between']['offscreen']:
            raise RuntimeError(f'S1 {k}: AffGame/phase-end native surface differs')
        b.executar_quadro(600, k)
        after = original.sha(b.directdraw.pixels('offscreen'))
        state = b.resumo_imagem(b.imagem())['sha256']
        if after != refs[k]['surfaces_frame']['offscreen'] or state != refs[k]['state_sha256']:
            raise RuntimeError(f'S1 {k}: end-frame surface or complete native state differs')
        checks.append(dict(frame=k, surface_equal=True, state_equal=True))
        b.roteiro.eventos.clear()
        if k % 50 == 0:
            print('S1', k, 'original state and both phase surfaces equal', flush=True)
        if time.monotonic() - started > 840:
            status = 'budget_stop'
            break
    cap.phase_frame = None
    cap.detach()
    end = checks[-1]['frame']
    checkpoint = Path(a.start) / f'S1-render-{end:05d}.pickle'
    if checkpoint.exists():
        raise FileExistsError(checkpoint)
    digest = original.seg.salvar(b, checkpoint, end)
    result = dict(schema='rising-lands/m3-probe-render-native/1', method=__doc__, probe='S1', probe_ref=ref,
        frames=[start + 1, end], requested_stop=a.to, status=status,
        original_opening_state_sha256=opening, opening_checkpoint_sha256=original.sha(checkpoint_input.read_bytes()),
        executable_sha256=__import__('emulador').HASH_ORIGINAL, code_sha256=b.sha256_codigo(),
        source_sha256=original.sha(Path(__file__).read_bytes()),
        recording_helper_sha256=original.sha(Path(original.__file__).read_bytes()),
        producing_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        snapshot=dict(path=str(checkpoint), sha256=digest), checks=checks, rows=cap.rows, blobs=cap.blobs,
        boundary_contract='Original Missions display-v2: AffText/TextGetMessage declared non-execution; no glyph substitution.',
        elapsed_seconds=round(time.monotonic() - started, 3))
    raw = json.dumps(result).encode()
    output.write_bytes(lzma.compress(raw, preset=3))
    manifest = {k: v for k, v in result.items() if k not in ('rows', 'blobs', 'checks', 'method')}
    manifest.update(raw_sha256=original.sha(raw), compressed_sha256=original.sha(output.read_bytes()),
                    invocation_seconds=round(time.monotonic() - started, 3))
    Path(str(output) + '.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('S1 original capture', result['frames'], status, 'surfaces', len(cap.rows), 'seconds', manifest['invocation_seconds'], flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--start', required=True)
    p.add_argument('--resume')
    p.add_argument('--ref', default=S1_REF)
    p.add_argument('--to', type=int, required=True)
    p.add_argument('--output', required=True)
    main(p.parse_args())
