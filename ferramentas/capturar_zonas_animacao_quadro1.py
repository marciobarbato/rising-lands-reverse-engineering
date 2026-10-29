"""Original-only isolated captures of SetClipping, InitGameZone and NextAnim* at the frame inputs.

Runs ``percurso_quadro1.executar`` (the committed Missions first-frame path)
pausing at SetClipping, InitGameZone (and the routines it calls), NextAnimTerrain,
NextAnimVegetFullMap and NextAnimVeget. Each call runs natively in isolation at its
exact entry state; the record keeps registers, changed bytes, the bytes read
before written and the native basic blocks the call executed. No Python
translation is imported.

    python3 -B ferramentas/capturar_zonas_animacao_quadro1.py \
        --saida evidencias/fundacoes-quadro/captura-zonas-animacao-quadro1.json
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
           'PlayerEstContacterPourAlliance', 'NextAnimTerrain', 'NextAnimVegetFullMap', 'NextAnimVeget')


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

    b, iso, cap, reproducao, _ = pq.executar(ROTINAS, observador=observador, cobertura=estado)
    chamadas = []
    for registro, cobertos in zip(iso.registros, blocos):
        c, = registro['cases']
        chamadas.append(dict(routine=registro['routine'], phase=registro['phase'], caller=registro['caller'],
                             caller_return=registro['caller_return'], entry_registers=c['entry_registers'],
                             exit_registers=c['exit_registers'], reached_return=c['reached_return'],
                             changed_bytes=c['changed_bytes'], read_before_write=c['read_before_write'],
                             native_blocks=[hex(x) for x in cobertos]))
    contagem = {}
    for c in chamadas:
        contagem[f"{c['phase']}:{c['routine']}"] = contagem.get(f"{c['phase']}:{c['routine']}", 0) + 1
    relatorio = dict(
        schema='rising-lands/monde01-frame1-isolated-core-zone-anim-calls/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('ferramentas/capturar_zonas_animacao_quadro1.py', 'ferramentas/percurso_quadro1.py',
                                 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        input='exact MONDE01 frame inputs: load_tail is frame 0, frame1 the second pass',
        routines={n: hex(b.sym[n]) for n in ROTINAS}, path_reproduction=reproducao, call_counts=contagem,
        not_reached=[n for n in ROTINAS if not any(c['routine'] == n for c in chamadas)],
        method='Native call from the exact saved entry state to its stack return (Missions Isolamento); read/write '
               'hooks and a basic-block hook, translation cache flushed after each hook_add; native_blocks are the '
               'block starts executed by that isolated call including nested routines',
        calls=chamadas, seconds=round(time.monotonic() - t0, 3))
    ok = reproducao['passed'] and all(c['reached_return'] for c in chamadas) and len(blocos) == len(iso.registros)
    if not ok:
        saida = RAIZ / '.local/frame' / ('zonas-animacao-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          reproduction=reproducao, call_counts=contagem, not_reached=relatorio['not_reached'],
                          seconds=relatorio['seconds']), indent=1))
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
