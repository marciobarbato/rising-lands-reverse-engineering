"""Native differential of influencia_missao against the intact queries at the frame-1 inputs.

Reruns the committed first-frame path, pauses at the frame-1 TestFinDeMission
entry and, for each declared table below written over 0x50c614, sweeps
CaseGetZoneInfluence over all 65,536 cells (plus 256 high-EAX calls) and
GetTopLeftCaseZoneInfluence over zones 0..399 natively; the Python
translation computes the same arrays from that case's exact table bytes.

    python3 -B pesquisas-paralelas/missoes/diferencial_influencia.py \
        --relatorio pesquisas-paralelas/missoes/validacao/m2-influencia-differential-x86.json
"""
import argparse
import hashlib
import json
import random
import struct
import subprocess
import sys
import time

import ambiente_missoes
import capturar_influencia_quadro1 as cinf
from influencia_missao import canto_zona_influencia, zona_influencia

TABELA = cinf.TABELA


def registro(z, x0, y0, x1, y1):
    return (TABELA+10*z, struct.pack('<4H', x0, y0, x1, y1))


def tabelas():
    gerador = random.Random(0x4d4f4e44)   # declared deterministic seed
    aleatoria = []
    for z in range(400):
        if gerador.random() < 0.25:
            aleatoria.append(registro(z, 0xffff, 0xffff, 0xffff, 0xffff))
        else:
            x0, y0 = gerador.randrange(256), gerador.randrange(256)
            aleatoria.append(registro(z, x0, y0, min(0xffff, x0+gerador.randrange(-8, 64)),
                                      min(0xffff, y0+gerador.randrange(-8, 64))))
    return [
        dict(case='overlap_skip255_inverted_point', writes=[
            registro(1, 10, 10, 20, 20), registro(2, 15, 15, 30, 30), registro(255, 0, 0, 255, 255),
            registro(5, 50, 50, 40, 40), registro(6, 100, 100, 100, 100), registro(399, 200, 200, 255, 255)]),
        dict(case='zone0_cleared_whole_map_record7', writes=[registro(0, 0xffff, 0xffff, 0xffff, 0xffff),
                                                             registro(7, 0, 0, 0xffff, 0xffff)]),
        dict(case='upper_word_bounds', writes=[registro(3, 0x100, 0, 0xffff, 0xffff), registro(4, 0, 0x100, 0xffff, 0xffff),
                                               registro(8, 254, 254, 0x1ff, 0x1ff)]),
        dict(case='seeded_random_400', writes=aleatoria),
    ]


class Comparador:
    def __init__(self):
        self.linhas = []

    def __call__(self, linha, tabela, zonas, altos, cantos):
        t = bytearray(tabela)
        pz = [zona_influencia(t, c) for c in range(65536)]
        pa = [[c, hex(zona_influencia(t, 0xabcd0000 | int(c, 16)))] for c, _ in altos]
        pc = [canto_zona_influencia(t, z) for z in range(400)]
        dif_z = [c for c in range(65536) if pz[c] != zonas[c]]
        dif_c = [z for z in range(400) if pc[z] != cantos[z]]
        self.linhas.append(dict(case=linha['case'], table_sha256=linha['table_sha256'],
                                zone_counts=linha['zone_counts'], registers_preserved=linha['registers_preserved'],
                                cells_differing=dif_z[:50], cells_differing_count=len(dif_z),
                                high_eax_equal=pa == altos, zones_differing=dif_c,
                                equal=not dif_z and not dif_c and pa == altos))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--relatorio', required=True)
    a = ap.parse_args()
    saida = ambiente_missoes.ROOT/a.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    t0 = time.monotonic()
    comparador = Comparador()
    casos = [dict(case='captured_inputs', writes=[])] + tabelas()
    v = cinf.Varredura(casos, observador=comparador)
    b, iso, cap, reproducao = cinf.executar(v)
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'status', '--porcelain', '--',
                           'pesquisas-paralelas/missoes'], capture_output=True, text=True).stdout
    linhas = comparador.linhas
    relatorio = dict(
        schema='rising-lands/monde01-influence-native-differential/1', source_revision=revisao,
        source_dirty_paths=sujo.splitlines(),
        source_sha256={n: hashlib.sha256((ambiente_missoes.OWNED/n).read_bytes()).hexdigest()
                       for n in ('influencia_missao.py', 'diferencial_influencia.py', 'capturar_influencia_quadro1.py',
                                 'oraculo_quadro_missao.py')},
        path_reproduction=reproducao, tables=len(linhas),
        native_calls_per_table=65536+256+400, differing=[x for x in linhas if not x['equal']], rows=linhas,
        seconds=round(time.monotonic()-t0, 3))
    relatorio['passed'] = (reproducao['passed'] and len(linhas) == len(casos) and not relatorio['differing']
                           and all(x['registers_preserved'] for x in linhas))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({k: v for k, v in relatorio.items() if k != 'rows'}, indent=1)[:4000])
    print([(x['case'], x['zone_counts'] if len(x['zone_counts']) < 8 else len(x['zone_counts']), x['equal']) for x in linhas])
    return 0 if relatorio['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
