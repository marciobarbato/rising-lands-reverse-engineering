"""Event probe over N frames of the display scenario (M2.2 planning; output is not evidence).

Runs the original (scenario ``exibicao`` or ``exibicao_v3``) through load_tail
and N frames and records, per phase: the declared boundaries reached (routine,
caller), routines entered for the first time in the run, the DirectDraw call
count, clock answers, both RNG states, the frame counters, the game state byte
and the UpdateChamp row.  It answers "what new happens at frame k" so that
reference frame sequences can be declared.  Writes under .local/ by default.

    python3 -B pesquisas-paralelas/missoes/varrer_eventos_quadros.py --quadros 130 \
        --relatorio .local/m2-eventos-130.json
"""
import argparse
import json
import struct
import subprocess
import sys
import time

import ambiente_missoes
import cenarios_oraculo as cen
from mapa_memoria_m1 import carregar_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, required=True)
    ap.add_argument('--relatorio', required=True)
    ap.add_argument('--cenario', default='exibicao', choices=('exibicao', 'exibicao_v3'))
    args = ap.parse_args()
    saida = ambiente_missoes.ROOT/args.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    t0 = time.monotonic()
    ni = carregar_json(cen.caminho('exibicao', 'captura_m1'))['named_inputs']
    b, _, _ = cen.bancada(args.cenario, ni['allocation_fill'], ni['clock_ms'][0])
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    u = lambda a, n: bytes(b.cpu.mem_read(a, n))
    vistos, linhas = set(), []
    fronteiras0, janelas0, dd0 = len(b.eventos_fronteira), len(b.windows.consumidos), len(b.chamadas_exibicao())
    for fase, regs in b.executar_quadros(args.quadros):
        r = b.rastro.get(fase, {})
        novas = [n for n in r.get('order', []) if n not in vistos]
        vistos.update(r.get('order', []))
        fr = b.eventos_fronteira[fronteiras0:]
        linhas.append(dict(
            phase=fase, stop=hex(regs['EIP']),
            boundaries=sorted({f"{e['routine']}@{e['caller']}" for e in fr}),
            boundary_calls=len(fr), new_routines=novas,
            directdraw_calls=len(b.chamadas_exibicao())-dd0,
            clock=[x for x in b.windows.consumidos[janelas0:] if 'clock' in x[0]],
            rng=hex(struct.unpack('<I', u(0x497164, 4))[0]), crt_seed=hex(struct.unpack('<I', u(0x340000c, 4))[0]),
            counters=list(struct.unpack('<III', u(0x508f7c, 12))), game_state=u(0x4e2f78, 1)[0],
            field_row=struct.unpack('<H', u(0x4973e8, 2))[0], event=u(0x4e1b0e, 1)[0],
            message_index=list(u(0x507d54, 4)), cursor_shift=u(0x4e1d18, 1)[0]))
        fronteiras0, janelas0, dd0 = len(b.eventos_fronteira), len(b.windows.consumidos), len(b.chamadas_exibicao())
        b.rastro = {}
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    rel = dict(schema='rising-lands/monde01-n-frame-event-probe/1', source_revision=revisao, evidence=False,
               scenario=args.cenario, frames=args.quadros, phases=linhas, seconds=round(time.monotonic()-t0, 1))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1)
        f.write('\n')
    resumo = [dict(phase=l['phase'], new=l['new_routines'][:8], boundaries=l['boundaries'][:6])
              for l in linhas if l['new_routines']]
    print(json.dumps(dict(seconds=rel['seconds'], phases_with_new_routines=resumo[:60]), indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
