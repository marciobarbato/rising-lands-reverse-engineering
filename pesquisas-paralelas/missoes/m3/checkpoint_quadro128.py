"""The M3 starting point: an exact resumable snapshot of the accepted M2.2 display reference after frame 128.

Builds Missions' -v2 display bench (``segmentos_quadros_missao.bancada_nova``), runs startup, MissionLoad and
frames 1..128 with the declared no-input answers, and requires the frame-128 state summary (and the frame-1
summary) to equal the committed M2.2 capture ``captura-quadros128-monde01-exibicao-v2.json.xz`` before it saves
the snapshot with ``segmentos_quadros_missao.salvar``. The display clock is extended by its own rule to
``--ticks`` answers so the scripted-input runs can continue for long from this snapshot.

Not evidence: the snapshot (about 40 MB) and its manifest stay under ``.local/``. The manifest records the
snapshot SHA-256, the reproduced summaries and the source revision.

    python3 -B pesquisas-paralelas/missoes/m3/checkpoint_quadro128.py --saida .local/m3/quadro128
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys
import time

MISSOES = Path(__file__).resolve().parents[1]
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
import ambiente_missoes  # noqa: E402

ROOT = ambiente_missoes.ROOT
CAPTURA_128 = MISSOES / 'evidencias/captura-quadros128-monde01-exibicao-v2.json.xz'
TICKS = 1_000_000
QUADRO = 128


def resumos_aceitos(caminho=CAPTURA_128):
    captura = json.loads(lzma.decompress(Path(caminho).read_bytes()))
    return {p['phase']: p['state_after']['summary'] for p in captura['phases']}


def main():
    import segmentos_quadros_missao as seg
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', required=True, help='directory (created) for the snapshot and its manifest')
    ap.add_argument('--ticks', type=int, default=TICKS)
    a = ap.parse_args()
    pasta = ROOT / a.saida
    pasta.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic()
    aceitos = resumos_aceitos()
    b = seg.bancada_nova(a.ticks)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    reproduzidos = {}
    for nome, _ in b.executar_quadros(QUADRO, 600):
        if nome in ('frame1', f'frame{QUADRO}'):
            reproduzidos[nome] = b.resumo_imagem(b.imagem()) == aceitos[nome]
    if not all(reproduzidos.values()):
        raise SystemExit(f'Frame summaries differ from the accepted M2.2 capture: {reproduzidos}')
    instantaneo = pasta / f'instantaneo-{QUADRO:05d}.pickle'
    sha = seg.salvar(b, instantaneo, QUADRO)
    manifesto = dict(
        schema='rising-lands/m3-frame128-snapshot/1', evidence=False, frame=QUADRO, ticks=a.ticks,
        snapshot=instantaneo.name, snapshot_sha256=sha,
        accepted_capture=dict(path=str(CAPTURA_128.relative_to(ROOT)),
                              xz_sha256=hashlib.sha256(CAPTURA_128.read_bytes()).hexdigest()),
        reproduced_summaries=reproduzidos, frame128_summary=aceitos[f'frame{QUADRO}'],
        source_revision=subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                                       text=True).stdout.strip(),
        seconds=round(time.monotonic() - t0, 1))
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=1, sort_keys=True) + '\n')
    print(json.dumps(manifesto, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
