"""Original-only survey of the MONDE01 display-reference frames up to cycle counter 128.

Reruns Missions' committed display reference (``cenarios_oraculo`` 'exibicao':
startup, MissionLoad, frames 0/1 reproduced against the v2 capture) and then
keeps running the real loop - between_frames (AffGame, PlaySnd/MCI pumps,
PeekMessageA, ProgIteration) and the next CalculGame frame - with the same
declared inputs (no key pressed, cursor (0,0), display ticks), until the frame
whose cycle counter u32 0x508f7c is ``--ate`` (default 128, where UpdateChamp's
field growth starts). Per frame it records the routine entries (Missions' block
trace, per-frame deltas), the boundary events, the counter, the world RNG
0x497164, the AI RNG 0x498db4, the CRT seed (thread +0xc), the permutation
cursor 0x4e1d18, the view origin and the whole-state hash. Routines first entered
after frame 1, and the first frame entering combat/raid routines, are listed.
No Python translation is imported.

    python3 -B ferramentas/levantar_quadros_exibicao.py \
        --saida evidencias/fundacoes-quadro/levantamento-quadros-exibicao.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
# Routines whose entry marks a raid or combat beginning (Combat/AI owners).
ATAQUE = ('SetAttaqueEngin', 'EnginTrouveCible', 'iagWarNoyau', 'ConstruitGroupeMonstre', 'EnginAttaque',
          'CalculAttaque', 'ProjectileNew', 'EnginBlesse', 'BatimentBlesse')


def contagens(b):
    return {f: dict(r.get('counts', {})) for f, r in b.rastro.items()}


def delta(antes, depois):
    saida = {}
    for f, c in depois.items():
        a = antes.get(f, {})
        d = {n: k - a.get(n, 0) for n, k in c.items() if k != a.get(n, 0)}
        if d:
            saida[f] = d
    return saida


def amostra(b):
    u32 = lambda a: struct.unpack('<I', b.cpu.mem_read(a, 4))[0]
    u16 = lambda a: struct.unpack('<H', b.cpu.mem_read(a, 2))[0]
    return dict(counter=u32(0x508f7c), game_frame=u32(0x496d40), world_rng=hex(u32(0x497164)),
                ai_rng=hex(u32(0x498db4)), crt_seed=hex(u32(u32(0x522244) + 0xc)),
                cursor=b.cpu.mem_read(0x4e1d18, 1)[0], view_origin=[u16(0x508720), u16(0x508722)],
                state=b.resumo_imagem(b.imagem())['sha256'])


def main():
    import percurso_quadro1 as pq       # noqa: F401  (Missions path on sys.path)
    import cenarios_oraculo
    from emulador import HASH_ORIGINAL
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ate', type=int, default=128)
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    b, cap = pq._bancada('exibicao')
    quadros, vistos, primeiro, ataque = [], {}, {}, None
    referencia = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao = {}
    eventos = len(b.eventos_fronteira)
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(300)),
                         ('frame1', lambda: b.executar_quadro(600))):
        antes = contagens(b)
        correr()
        reproducao[nome] = b.resumo_imagem(b.imagem()) == referencia[nome]
        for f, d in delta(antes, contagens(b)).items():
            for n in d:
                vistos.setdefault(n, 0 if nome == 'load_tail' else 1)
    reproducao['entry_trace_equal'] = json.loads(json.dumps(b.rastro_json())) == cap['entry_trace']
    quadros.append(dict(frame=1, **amostra(b)))
    eventos = len(b.eventos_fronteira)
    while True:
        k = len(quadros) + 1
        antes = contagens(b)
        t = time.monotonic()
        b.executar_entre_quadros(300)
        b.executar_quadro(600)
        d = delta(antes, contagens(b))
        fronteiras = {}
        for e in b.eventos_fronteira[eventos:]:
            fronteiras[e['routine']] = fronteiras.get(e['routine'], 0) + 1
        eventos = len(b.eventos_fronteira)
        novos = sorted({n for f in d.values() for n in f} - set(vistos))
        for n in novos:
            vistos[n] = k
            primeiro[n] = k
        if ataque is None and any(n in ATAQUE for f in d.values() for n in f):
            ataque = k
        quadros.append(dict(frame=k, seconds=round(time.monotonic() - t, 3), new_routines=novos, entries=d,
                            boundaries=fronteiras, **amostra(b)))
        if quadros[-1]['counter'] >= a.ate:
            break
    relatorio = dict(
        schema='rising-lands/monde01-display-frames-survey/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='exibicao',
        reference=dict(path=str(cenarios_oraculo.caminho('exibicao', 'captura_quadro').relative_to(RAIZ)),
                       sha256=hashlib.sha256(cenarios_oraculo.caminho('exibicao', 'captura_quadro').read_bytes())
                       .hexdigest()),
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('ferramentas/levantar_quadros_exibicao.py', 'ferramentas/percurso_quadro1.py')},
        inputs='Missions display-reference named inputs; every later frame keeps the declared no-input answers '
               '(GetAsyncKeyState 0, PeekMessageA no message, GetCursorPos (0,0)) and the declared display ticks',
        reproduction_frames_0_1=reproducao, stop_counter=a.ate,
        routines_first_entered_after_frame1=primeiro, first_raid_frame=ataque, raid_markers=list(ATAQUE),
        code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'], frames=quadros,
        seconds=round(time.monotonic() - t0, 3))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), reproduction=reproducao, frames=len(quadros),
                          last=quadros[-1]['counter'], first_entered=primeiro, first_raid=ataque,
                          seconds=relatorio['seconds']), indent=1))
    return 0 if all(reproducao.values()) and relatorio['code_unchanged'] else 2


if __name__ == '__main__':
    sys.exit(main())
