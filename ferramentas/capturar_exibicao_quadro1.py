"""Original-only isolated captures of Core frame callees in the display scenario (M2 reference).

Runs ``percurso_quadro1.executar(cenario='exibicao')``: Missions' committed
display-executing path (real _WinMain@16 loop, DDInit's 25x17 viewport), then
frames 0/1, pausing at SetClipping, InitGameZone and the routines it calls,
NextAnimTerrain/NextAnimVegetFullMap/NextAnimVeget, GameNextFrame, Random and
the CRT random generator (LongRand 0x45841b -> rand 0x48c51d). The 425-per-frame
LongRand/rand calls and the Random/MouseSetZone calls are isolated only for the
first calls of each phase; NextAnimTerrain is isolated whole, so its record holds
the effect of all 425 draws on the CRT seed. Each record keeps registers,
changed bytes, bytes read before written and the executed native blocks. No
Python translation is imported.

    python3 -B ferramentas/capturar_exibicao_quadro1.py \
        --saida evidencias/fundacoes-quadro/captura-exibicao-quadro1.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
ROTINAS = ('SetClipping', 'InitGameZone', 'MouseSetZone', 'MouseTestZone', 'MiniMapGetPos', 'MiniMapGetTaille',
           'MarcheGetPos', 'MarcheGetTaille', 'ChercheContacteur', 'MessageBoxExiste',
           'PlayerEstContacterPourAlliance', 'NextAnimTerrain', 'NextAnimVegetFullMap', 'NextAnimVeget',
           'GameNextFrame', 'Random', 'LongRand', 'rand')
LIMITES = {'LongRand': 6, 'rand': 6, 'Random': 4, 'MouseSetZone': 6}


def main():
    import percurso_quadro1 as pq
    from emulador import HASH_ORIGINAL
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    blocos, estado = [], {}

    def observador(nome, fase, caso, antes, resultado):
        blocos.append(estado['recorder'].drenar())

    b, iso, cap, reproducao, _ = pq.executar(ROTINAS, observador=observador, cobertura=estado, cenario='exibicao',
                                             limites=LIMITES)
    chamadas = []
    for registro, cobertos in zip(iso.registros, blocos):
        c, = registro['cases']
        chamadas.append(dict(routine=registro['routine'], phase=registro['phase'], caller=registro['caller'],
                             caller_return=registro['caller_return'], entry_registers=c['entry_registers'],
                             exit_registers=c['exit_registers'], reached_return=c['reached_return'],
                             changed_bytes=c['changed_bytes'], read_before_write=c['read_before_write'],
                             native_blocks=[hex(x) for x in cobertos]))
    entradas = {f'{n}:{f}': k for (n, f, _), k in sorted(iso.vistos.items())}
    contagem = {}
    for c in chamadas:
        contagem[f"{c['phase']}:{c['routine']}"] = contagem.get(f"{c['phase']}:{c['routine']}", 0) + 1
    import cenarios_oraculo
    caminho = cenarios_oraculo.caminho('exibicao', 'captura_quadro')
    relatorio = dict(
        schema='rising-lands/monde01-frame1-display-isolated-core-calls/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='exibicao',
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('ferramentas/capturar_exibicao_quadro1.py', 'ferramentas/percurso_quadro1.py',
                                 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py',
                                 'pesquisas-paralelas/missoes/oraculo_exibicao_missao.py')},
        frame_capture=dict(path=str(caminho.relative_to(RAIZ)), sha256=hashlib.sha256(caminho.read_bytes()).hexdigest()),
        input='exact display-scenario MONDE01 frame inputs: load_tail is frame 0, frame1 the second pass',
        routines={n: hex(b.sym[n]) for n in ROTINAS}, isolation_limits_per_phase=LIMITES,
        routine_entries=entradas, isolated_counts=contagem, path_reproduction=reproducao,
        not_reached=[n for n in ROTINAS if not any(k.startswith(n + ':') for k in entradas)],
        method='Native call from the exact saved entry state to its stack return (Missions Isolamento over the '
               'display bench); read/write hooks and a basic-block hook, translation cache flushed after each '
               'hook_add; native_blocks are the block starts executed by that isolated call including nested '
               'routines; calls beyond the per-phase limit run natively without a pause',
        calls=chamadas, seconds=round(time.monotonic() - t0, 3))
    ok = reproducao['passed'] and all(c['reached_return'] for c in chamadas) and len(blocos) == len(iso.registros)
    if not ok:
        saida = RAIZ / '.local/frame' / ('exibicao-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao, entries=entradas, isolated=contagem,
                          not_reached=relatorio['not_reached'], seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2, saida


if __name__ == '__main__':
    # Durable fast exit: fsync the output, skip uc_close at shutdown (docs/core/UNICORN_TEARDOWN.md).
    from encerramento_captura import encerrar_captura
    encerrar_captura(*main())
