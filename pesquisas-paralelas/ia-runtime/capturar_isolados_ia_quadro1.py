"""Original-only isolated captures of the AI/runtime frame callees at the exact MONDE01 frame-0/1 inputs.

    python3 -B pesquisas-paralelas/ia-runtime/capturar_isolados_ia_quadro1.py \
        --saida pesquisas-paralelas/ia-runtime/evidencias/captura-isolada-ia-quadro1.json

This replays Missions' committed first-frame path (``bancada_quadro1_ia``):
accepted M1 startup and MissionLoad, then load_tail ("frame 0"), between_frames
and frame1. Each listed routine is executed natively in isolation at every
entry, on the exact saved state. The record holds AL, the registers, the
changed bytes and the bytes read before written, with their entry values.
Snapshot-only pauses record the state summary and registers at the entries of
RestoreAll and InputGame, the first calls that have no Python provider.
The run must reproduce every committed phase state, the entry trace and the
boundaries. No Python translation is imported.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

from ambiente_ia_runtime import OWNED, ROOT
from bancada_quadro1_ia import CAPTURA_QUADRO, MISSOES, executar_caminho
from emulador import HASH_ORIGINAL

EXECUTADAS = ('CalculNextReflect', 'ProcessInputGame', 'MessageBoxCalcul', 'GameNextFrame',
              'CalculEnginNextEtape', 'CalculBatimentNextEtape')
INSTANTANEOS = ('RestoreAll', 'InputGame')
LABEL = 'exact MONDE01 frame-0/1 input (Missions first-frame path)'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/ia-runtime',
                           'pesquisas-paralelas/missoes'], capture_output=True, text=True).stdout
    t0 = time.monotonic()
    b, pausa, cap, reproducao = executar_caminho(EXECUTADAS, INSTANTANEOS)
    relatorio = dict(
        schema='rising-lands/ai-runtime-frame1-isolated-calls/1', label=LABEL, original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, source_dirty_paths=sujo.splitlines(),
        source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (
            OWNED / 'bancada_quadro1_ia.py', OWNED / 'capturar_isolados_ia_quadro1.py',
            MISSOES / 'oraculo_quadro_missao.py', MISSOES / 'capturar_quadro_missao_original.py')},
        frame_capture=dict(path=str(CAPTURA_QUADRO.relative_to(ROOT)),
                           sha256=hashlib.sha256(CAPTURA_QUADRO.read_bytes()).hexdigest()),
        executed=list(EXECUTADAS), snapshots=list(INSTANTANEOS), path_reproduction=reproducao,
        calls=pausa.registros, pauses=pausa.pausas,
        method="Missions' Isolamento: native call from the exact saved entry state to its stack return under "
               'local read/write hooks (translation cache flushed); state restored after each call. Snapshot '
               'pauses record the entry state summary without executing anything',
        seconds=round(time.monotonic() - t0, 3))
    resultado = 0 if reproducao['passed'] and all(c['reached_return'] for r in pausa.registros for c in r['cases']) else 2
    if resultado:
        saida = ROOT / '.local' / ('ai-frame1-isolated-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao,
                          calls=[dict(routine=r['routine'], phase=r['phase'], al=r['cases'][0]['al'],
                                      changed=len(r['cases'][0]['changed_bytes']),
                                      reads=len(r['cases'][0]['read_before_write'])) for r in pausa.registros],
                          pauses=[(p['routine'], p['phase'], p['caller']) for p in pausa.pausas],
                          seconds=relatorio['seconds']), indent=1))
    return resultado


if __name__ == '__main__':
    sys.exit(main())
