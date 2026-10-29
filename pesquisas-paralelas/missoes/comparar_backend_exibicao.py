"""Display reference over Graphics' backend (v2) vs the Stage17 interim-backend artifacts, byte by byte.

CPU-free, from committed captures only.  Compared: the MissionLoad entry
snapshot, the MissionLoad final state, allocation records, the ordered
MissionLoad binding log, startup binding counts, and for load_tail /
between_frames / frame1 the state after the phase, the per-routine entry
trace, the declared boundaries, the Windows answers and the binding names in
order.  A differing state dword is classified ``backend_address`` only when
both values lie inside the two backends' declared object/surface regions
(0x3600000..0x3610000, 0x60000000..0x60400000): the program stored a pointer
the backend chose.  Anything else is reported as unexplained.

    python3 -B pesquisas-paralelas/missoes/comparar_backend_exibicao.py \
        --relatorio pesquisas-paralelas/missoes/validacao/m2-exibicao-v2-vs-interino.json
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys

import ambiente_missoes
import cenarios_oraculo as cen
import comparar_quadros_exibicao as cmp
from mapa_memoria_m1 import carregar_json, expandir_captura

REGIOES_BACKEND = ((0x3600000, 0x3610000), (0x60000000, 0x60400000))


def backend(valor):
    return any(a <= valor < z for a, z in REGIOES_BACKEND)


def diff_blocos(a, b):
    saida = dict(blocks_only_interim=sorted(set(a)-set(b)), blocks_only_v2=sorted(set(b)-set(a)), differing=[])
    for nome in sorted(set(a) & set(b)):
        base, x = a[nome]
        y = b[nome][1]
        if x == y:
            continue
        difs = [i for i in range(len(x)) if x[i] != y[i]]
        explicados = set()
        for i in difs:
            for k in range(max(0, i-3), min(i, len(x)-4)+1):
                va, vb = struct.unpack_from('<I', x, k)[0], struct.unpack_from('<I', y, k)[0]
                if va != vb and backend(va) and backend(vb):
                    explicados.update(range(k, k+4))
                    break
        for i in difs:
            saida['differing'].append(dict(block=nome, address=hex(base+i), interim=x[i], v2=y[i],
                                           cls='backend_address' if i in explicados else 'unexplained'))
    saida['unexplained'] = [d for d in saida['differing'] if d['cls'] == 'unexplained']
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--relatorio', required=True)
    args = ap.parse_args()
    saida = ambiente_missoes.ROOT/args.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    i1, _, aloc1, ent1 = cmp.imagens('exibicao_interino')
    i2, _, aloc2, ent2 = cmp.imagens('exibicao')
    m1 = [expandir_captura(carregar_json(cen.caminho(c, 'captura_m1')), e) for c, e in
          (('exibicao_interino', ent1), ('exibicao', ent2))]
    q = [carregar_json(cen.caminho(c, 'captura_quadro')) for c in ('exibicao_interino', 'exibicao')]
    estados = {e: diff_blocos(i1[e], i2[e]) for e in cmp.ESTADOS}
    nomes = lambda p: [ev['name'] for ev in p['bindings']]
    fases = {}
    for p1, p2 in zip(q[0]['phases'], q[1]['phases']):
        fases[p1['phase']] = dict(
            binding_names_equal=nomes(p1) == nomes(p2),
            binding_counts=[p1['binding_counts'], p2['binding_counts']] if p1['binding_counts'] != p2['binding_counts'] else 'equal',
            boundaries_equal=[(x['routine'], x['caller_return']) for x in p1['boundaries']]
            == [(x['routine'], x['caller_return']) for x in p2['boundaries']],
            windows_answers_equal=p1['windows_answers'] == p2['windows_answers'],
            directdraw_methods=[[c.get('method') for c in p1.get('directdraw_calls', [])],
                                [c.get('method') for c in p2.get('directdraw_calls', [])]])
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    rel = dict(
        schema='rising-lands/display-reference-backend-equivalence/1', source_revision=revisao, cpu_free=True,
        inputs={f'{c}_{k}': dict(path=str(cen.caminho(c, k).relative_to(ambiente_missoes.ROOT)),
                                 sha256=hashlib.sha256(cen.caminho(c, k).read_bytes()).hexdigest())
                for c in ('exibicao_interino', 'exibicao') for k in ('entrada', 'captura_m1', 'captura_quadro')},
        states=estados,
        allocation_records_equal=aloc1 == aloc2,
        missionload_binding_log_equal=m1[0]['oracle']['binding_events'] == m1[1]['oracle']['binding_events'],
        missionload_al=[m1[0]['oracle']['al'], m1[1]['oracle']['al']],
        startup_binding_counts_equal=m1[0]['startup']['binding_counts'] == m1[1]['startup']['binding_counts'],
        entry_trace_equal=q[0]['entry_trace'] == q[1]['entry_trace'],
        phases=fases, method=__doc__.split('\n\n')[1].replace('\n', ' '))
    rel['byte_for_byte'] = all(not v['differing'] for v in estados.values())
    rel['equal_except_backend_addresses'] = (
        all(not v['unexplained'] and not v['blocks_only_interim'] and not v['blocks_only_v2'] for v in estados.values())
        and rel['allocation_records_equal'] and rel['missionload_binding_log_equal'] and rel['entry_trace_equal']
        and all(f['binding_names_equal'] and f['boundaries_equal'] and f['windows_answers_equal'] for f in fases.values()))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1)
        f.write('\n')
    print(json.dumps(dict(byte_for_byte=rel['byte_for_byte'],
                          equal_except_backend_addresses=rel['equal_except_backend_addresses'],
                          differing={e: (len(v['differing']), len(v['unexplained'])) for e, v in estados.items()},
                          phases={k: {kk: vv for kk, vv in v.items() if kk != 'directdraw_methods'} for k, v in fases.items()}),
                     indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
