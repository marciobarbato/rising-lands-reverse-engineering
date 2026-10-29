"""M2.3 formal 9,200-frame equality proof (AI/runtime): the Python frame composition against Missions' original
capture in 10 self-contained parts (frames 0-9,200, 18,401 phases; first raid spawn at frame 9000, first path
search 9176-9179).

One command, on a clean tree (parts in parallel; ``--lease`` wraps each part in the machine's heavy lease):

    python3 -B pesquisas-paralelas/ia-runtime/provar_quadros_9200_ia.py tudo --paralelo 4 \
        [--lease <path>/heavy_lease.py] --saida pesquisas-paralelas/ia-runtime/validacao/m2-3-prova-9200-quadros.json

The same proof, step by step (the parts may run on any schedule or machine slot):

    python3 -B pesquisas-paralelas/ia-runtime/provar_quadros_9200_ia.py parte N      # N = 0..9, one report each
    python3 -B pesquisas-paralelas/ia-runtime/provar_quadros_9200_ia.py agregar --saida <proof.json>

Python only; the native side is the committed capture.

- **Reference:** the manifest ``captura-quadros9200-monde01-exibicao-v2.manifest.json`` (its SHA-256 is pinned
  here; it pins every part's xz and raw JSON hashes and the policy). ``agregar`` re-checks the hash chain between
  the parts (``partes_quadros_ia.verificar``).
- **Per part** (``comparar_quadros_ia.comparar_parte``): the opening full state is checked against its own
  summary, compared summary and masked hash; part 0 must open with the -v2 MissionLoad final state. Every phase is
  replayed from the deltas and checked against its summary, compared summary and masked hash, and the full states
  after frames 8999, 9000 and 9176. Python starts from the opening state with ONE map, in mode 'prova' (no
  crossing), and each phase is compared:
  - every state byte outside the cumulative mask (and Python's compared summary against the reference's);
  - both RNGs;
  - the bindings and boundaries outside display context;
  - the allocation-record count;
  - the between-frames exit registers and the carried entry registers.

  The first difference stops the part. Part 9 carries the final allocation records, compared in full.
- **Reports:** one JSON per part under ``.local/m2-3/prova-<revision>/``; ``agregar`` requires every report from
  the same clean revision, equal, covering its whole part, and writes the proof. A proof that is not accepted
  goes under ``.local/``.
"""
import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ambiente_ia_runtime import EXE, ORIGINAL_SHA256, ROOT, SBL

PASTA = 'pesquisas-paralelas/missoes/evidencias/m2-3'
MANIFESTO = f'{PASTA}/captura-quadros9200-monde01-exibicao-v2.manifest.json'
SHA_MANIFESTO = 'e88dc3fcaca11d03a774dad8bd9c768345f13c884cc2d8df493107ec9d180b09'
POLITICA = 'pesquisas-paralelas/missoes/validacao/m2-3-politica-comparacao-9200-quadros.json'
SCRIPT = 'pesquisas-paralelas/ia-runtime/provar_quadros_9200_ia.py'
FASES_TOTAIS = 18401
PARTES = 10
# Phases kept in full in the proof: the raid spawn, the first path search and the reference full states.
FASES_DETALHADAS = ('between_frames8999', 'frame8999', 'between_frames9000', 'frame9000', 'between_frames9176',
                    'frame9176', 'between_frames9177', 'frame9177', 'between_frames9178', 'frame9178',
                    'between_frames9179', 'frame9179', 'frame9200')


def sha(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True).stdout


def revisao():
    return git('rev-parse', 'HEAD').strip()


def sujos():
    return git('status', '--porcelain').splitlines()


def manifesto():
    caminho = ROOT / MANIFESTO
    if sha(caminho) != SHA_MANIFESTO:
        raise SystemExit('The M2.3 manifest is not the pinned one')
    m = json.loads(caminho.read_bytes())
    if m['policy']['path'] != POLITICA or sha(ROOT / POLITICA) != m['policy']['sha256']:
        raise SystemExit('The manifest policy is not the committed M2.3 policy')
    if len(m['parts']) != PARTES or sum(p['phases'] for p in m['parts']) != FASES_TOTAIS:
        raise SystemExit('The manifest does not hold 10 parts and 18,401 phases')
    return m


def pasta_relatorios(rev=None):
    return f'.local/m2-3/prova-{(rev or revisao())[:12]}'


def codigo_importado():
    """SHA-256 of every repository source file this process imported (the code the part ran)."""
    saida = {}
    for modulo in list(sys.modules.values()):
        f = getattr(modulo, '__file__', None)
        if not f:
            continue
        p = Path(f).resolve()
        if p.suffix == '.py' and p.is_relative_to(ROOT):
            saida[str(p.relative_to(ROOT))] = sha(p)
    return dict(sorted(saida.items()))


def cenario_v2():
    """SHA-256 of the -v2 display scenario files (MissionLoad input and capture, frame-1 capture): part 0's S0,
    the declared frame inputs and the allocation records at every part opening come from them."""
    sys.path.insert(0, str(ROOT / 'pesquisas-paralelas/missoes'))
    import cenarios_oraculo
    saida = {}
    for chave in ('entrada', 'captura_m1', 'captura_quadro'):
        caminho = cenarios_oraculo.caminho('exibicao', chave)
        saida[str(caminho.relative_to(ROOT))] = sha(caminho)
    return saida


def cadeia_fases(fases):
    """SHA-256 over 'phase compared_summary world_rng ai_rng allocations' lines, in phase order (Python values).

    Two runs of the same part on any machine give the same chain only if every phase's compared state is equal."""
    h = hashlib.sha256()
    for nome, r in fases.items():
        rng = r.get('rng', {}).get('python', {})
        h.update(f"{nome} {r.get('compared_summary', {}).get('python')} {rng.get('0x497164')} "
                 f"{rng.get('0x498db4')} {r.get('allocation_count', {}).get('python')}\n".encode())
    return h.hexdigest()


def rodar_parte(n, relatorios):
    from comparar_quadros_ia import comparar_parte
    m = manifesto()
    entrada = next(p for p in m['parts'] if p['part'] == n)
    saida = ROOT / relatorios / f'parte{n:02d}.json'
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    artefato = ROOT / entrada['artifact']
    if sha(artefato) != entrada['compressed_sha256']:
        raise SystemExit(f'part {n}: the xz file differs from the manifest')
    rev, sujo = revisao(), sujos()
    t0 = time.monotonic()
    corpo = comparar_parte(artefato, ROOT / POLITICA, entrada['raw_sha256'])
    segundos = round(time.monotonic() - t0, 1)
    pico = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rel = dict(schema='rising-lands/ai-runtime-m2.3-part-comparison/1', part_number=n, source_revision=rev,
               source_dirty_paths=sujo, manifest=dict(path=MANIFESTO, sha256=SHA_MANIFESTO),
               manifest_part=entrada, seconds=segundos,
               peak_rss_bytes=pico if sys.platform == 'darwin' else pico * 1024,
               machine=dict(system=platform.system(), release=platform.release(), machine=platform.machine(),
                            processor=platform.processor(), python=platform.python_version()),
               code_sha256=codigo_importado(), phase_chain_sha256=cadeia_fases(corpo['phases']), **corpo)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(part=n, output=str(saida), summary=rel['summary'], seconds=segundos,
                          peak_rss_mb=round(rel['peak_rss_bytes'] / 2**20)), indent=1), flush=True)
    return 0 if rel['summary']['result'] == 'equal' else 2


# ---------------------------------------------------------------------------------------------------- aggregation

COLUNAS = ('equal', 'compared_bytes', 'compared_summary', 'rng', 'bindings', 'boundaries', 'allocation_count',
           'registers', 'carried_registers', 'hud_flag', 'display_context_bindings_not_modeled',
           'display_context_boundaries_not_modeled', 'shared_issuers_matched', 'reference_integrity')


def linha_fase(r, hud):
    integridade = r.get('reference_integrity', {})
    return dict(
        equal=r['equal'], compared_bytes=r.get('state', {}).get('compared_bytes'),
        compared_summary=r.get('compared_summary', {}).get('equal'), rng=r.get('rng', {}).get('equal'),
        bindings=r.get('bindings', {}).get('equal'), boundaries=r.get('boundaries', {}).get('equal'),
        allocation_count=r.get('allocation_count', {}).get('equal'),
        registers=all(v['equal'] for v in r['registers'].values()) if 'registers' in r else None,
        carried_registers=all(v['equal'] for v in r['carried_entry_registers'].values())
        if 'carried_entry_registers' in r else None,
        hud_flag=hud,
        display_context_bindings_not_modeled=r.get('bindings', {}).get('display_context_not_modeled'),
        display_context_boundaries_not_modeled=len(r.get('boundaries', {}).get('display_context_not_modeled', [])),
        shared_issuers_matched=len(r.get('bindings', {}).get('shared_issuers_matched', [])) +
        len(r.get('boundaries', {}).get('shared_issuers_matched', [])),
        reference_integrity='+'.join(sorted(k for k, v in integridade.items() if v is True)) + '/' +
        integridade.get('form', '?'))


def tabela_rle(fases, huds):
    """The phase table run-length encoded by frame: consecutive frames whose between-frames row and frame row are
    both identical share one run ``[first_frame, last_frame, frames, between_frames_row, frame_row]`` (rows follow
    ``columns``); ``load_tail`` is its own row."""
    linha = lambda nome: [linha_fase(fases[nome], huds.get(nome))[c] for c in COLUNAS]  # noqa: E731
    saida, corridas, entre = dict(columns=list(COLUNAS)), [], None
    for nome in fases:
        if nome == 'load_tail':
            saida['load_tail'] = linha(nome)
        elif nome.startswith('between_frames'):
            entre = linha(nome)
        else:
            k = int(nome[len('frame'):])
            par = [entre, linha(nome)]
            if corridas and corridas[-1][1] == k - 1 and corridas[-1][3:] == par:
                corridas[-1][1] = k
                corridas[-1][2] += 1
            else:
                corridas.append([k, k, 1] + par)
            entre = None
    saida['runs'] = corridas
    return saida


def contar(fases, chave, filtro=lambda nome: True):
    sel = [r for nome, r in fases.items() if filtro(nome) and chave(r) is not None]
    return dict(equal=sum(1 for r in sel if chave(r)), checked=len(sel))


def agregar(relatorios):
    from partes_quadros_ia import verificar
    from provar_quadros_ia import bytes_mistos
    m = manifesto()
    rev, sujo = revisao(), sujos()
    cadeia = verificar(ROOT / MANIFESTO)
    politica = json.loads((ROOT / POLITICA).read_bytes())
    partes, fases, huds, problemas, codigo = [], {}, {}, [], {}
    alocacoes_finais = None
    for p in m['parts']:
        n = p['part']
        rel = json.loads((ROOT / relatorios / f'parte{n:02d}.json').read_bytes())
        erros = []
        if rel['part']['raw_json_sha256'] != p['raw_sha256'] or rel['part']['sha256'] != p['compressed_sha256']:
            erros.append('report is not for the manifest part')
        if rel['policy']['sha256'] != m['policy']['sha256']:
            erros.append('report used another policy')
        if (rel['part']['first_phase'], rel['part']['last_phase']) != (p['first_phase'], p['last_phase']):
            erros.append('report does not cover the whole part')
        if rel['summary']['result'] != 'equal' or rel['summary']['phases_equal'] != p['phases']:
            erros.append(f"result {rel['summary']['result']} ({rel['summary']['phases_equal']}/{p['phases']})")
        if rel['source_revision'] != rev or rel['source_dirty_paths']:
            erros.append(f"report from revision {rel['source_revision'][:12]} (dirty: {bool(rel['source_dirty_paths'])})")
        if rel['crossings']['count'] or rel['crossings']['writing_compared_bytes']:
            erros.append(f"crossings {rel['crossings']}")
        conflitos = sorted(f for f, h in rel['code_sha256'].items() if codigo.get(f, h) != h)
        if conflitos:
            erros.append(f'imported code differs from an earlier part: {conflitos}')
        codigo.update(rel['code_sha256'])
        if n == PARTES - 1:
            alocacoes_finais = rel['allocation_records']
            if not (alocacoes_finais or {}).get('equal'):
                erros.append('final allocation records not equal')
        if erros:
            problemas.append(dict(part=n, problems=erros))
        for h in rel['hud_flag']:
            huds[h['phase']] = h['equal']
        fases.update(rel['phases'])
        partes.append(dict(
            part=n, frames=rel['part']['frames'], first_phase=rel['part']['first_phase'],
            last_phase=rel['part']['last_phase'], phases=rel['summary']['phases_compared'],
            phases_equal=rel['summary']['phases_equal'], result=rel['summary']['result'],
            opening_state=rel['part']['opening_state'], reference_full_states=rel['part']['full_states'],
            crossings=rel['crossings'], phase_chain_sha256=rel['phase_chain_sha256'], seconds=rel['seconds'],
            peak_rss_mb=round(rel['peak_rss_bytes'] / 2**20), machine=rel['machine'],
            report_sha256=sha(ROOT / relatorios / f'parte{n:02d}.json')))
    # Part reports are written with sorted keys: restore the run's phase order (load_tail, then each frame).
    from composicao_quadros_ia import fases_quadros
    ordem = fases_quadros(9200)
    if set(ordem) != set(fases):
        problemas.append(dict(part=None, problems=['the part reports do not hold exactly the 18,401 run phases']))
    fases = {n: fases[n] for n in ordem if n in fases}
    nomes = list(fases)
    entre = lambda nome: nome.startswith('between_frames')  # noqa: E731
    byte_fases = {r['state']['compared_bytes'] for r in fases.values() if 'state' in r}
    ultima = fases[nomes[-1]]
    resultado = 'equal' if not problemas and len(nomes) == FASES_TOTAIS and \
        all(r['equal'] for r in fases.values()) else 'not_accepted'
    tempos = json.loads((ROOT / relatorios / 'tempo.json').read_bytes()) if (ROOT / relatorios / 'tempo.json').exists() \
        else None
    return dict(
        schema='rising-lands/ai-runtime-m2.3-9200-frame-proof/1', source_revision=rev, source_dirty_paths=sujo,
        reproduction=dict(
            one_command=f'python3 -B {SCRIPT} tudo --paralelo 4 [--lease <heavy_lease.py>] --saida <proof.json>',
            per_part=f'python3 -B {SCRIPT} parte N  (N = 0..9)', aggregate=f'python3 -B {SCRIPT} agregar --saida '
                                                                         '<proof.json>',
            reports=relatorios),
        capture=dict(manifest=dict(path=MANIFESTO, sha256=SHA_MANIFESTO), chain=cadeia,
                     parts=[{k: p[k] for k in ('part', 'artifact', 'compressed_sha256', 'raw_sha256', 'frames',
                                               'first_phase', 'last_phase', 'phases')} for p in m['parts']]),
        policy=dict(path=POLITICA, sha256=m['policy']['sha256'], frames=politica['frames'],
                    phases=politica['phases'], totals=politica['cumulative']['totals'],
                    exclusion_ranges=len(politica['cumulative']['exclusion_mask']), passed=politica['passed']),
        evidence_sha256={MANIFESTO: SHA_MANIFESTO, POLITICA: m['policy']['sha256'],
                         **{p['artifact']: p['compressed_sha256'] for p in m['parts']},
                         str(EXE.relative_to(ROOT)) if EXE.is_relative_to(ROOT) else 'RISING.EXE': ORIGINAL_SHA256,
                         'RISING.SBL': sha(SBL), **cenario_v2()},
        code_sha256=dict(sorted(codigo.items())),
        crossings=dict(count=sum(p['crossings']['count'] for p in partes),
                       writing_compared_bytes=sum(p['crossings']['writing_compared_bytes'] for p in partes),
                       note='measured: the composition runs in mode \'prova\' with no crossing data, so any crossing '
                            'would stop the part; every routine is a Python provider or a display root whose state '
                            'writes are masked or modeled'),
        compared_bytes_with_display_writers=dict(
            bytes=bytes_mistos(politica),
            handling={'0x4e05a2': 'AffGame store modeled (affgame_hud_ia); CalculMatiere is Economy\'s provider',
                      'clip words 0x49a01e/1f, 0x49a022/23': 'RestaureClipping (display) writes back the values '
                                                                'SaveClipping saved; SetClipping (logic) is Core\'s '
                                                                'provider; equal at every phase end'}),
        equality=dict(
            state=contar(fases, lambda r: r.get('state', {}).get('equal')),
            compared_summary=contar(fases, lambda r: r.get('compared_summary', {}).get('equal')),
            compared_bytes_per_phase=sorted(byte_fases),
            compared_byte_phase_total=sum(r['state']['compared_bytes'] for r in fases.values() if 'state' in r),
            rng=contar(fases, lambda r: r.get('rng', {}).get('equal')),
            bindings_outside_display=contar(fases, lambda r: r.get('bindings', {}).get('equal')),
            boundaries_outside_display=contar(fases, lambda r: r.get('boundaries', {}).get('equal')),
            allocation_count=contar(fases, lambda r: r.get('allocation_count', {}).get('equal')),
            between_frames_exit_registers=contar(fases, lambda r: all(v['equal'] for v in r['registers'].values())
                                                 if 'registers' in r else None, entre),
            carried_entry_registers=contar(
                fases, lambda r: all(v['equal'] for v in r['carried_entry_registers'].values())
                if 'carried_entry_registers' in r else None, entre),
            hud_flag=dict(equal=sum(1 for v in huds.values() if v), checked=len(huds)),
            reference_integrity=dict(
                summary=sum(1 for r in fases.values() if r['reference_integrity'].get('summary_equal')),
                compared_summary=sum(1 for r in fases.values()
                                     if r['reference_integrity'].get('compared_summary_equal')),
                masked_sha256=sum(1 for r in fases.values() if r['reference_integrity'].get('masked_sha256_equal')),
                full_states=[n for n, r in fases.items() if r['reference_integrity'].get('checkpoint_full_state_equal')])),
        bindings_boundaries=dict(
            bindings_compared=sum(r['bindings']['original'] for r in fases.values() if 'bindings' in r),
            boundaries_compared=sum(r['boundaries']['original'] for r in fases.values() if 'boundaries' in r),
            display_context_bindings_not_modeled=sum(r['bindings']['display_context_not_modeled']
                                                     for r in fases.values() if 'bindings' in r),
            display_context_boundaries_not_modeled=sum(len(r['boundaries']['display_context_not_modeled'])
                                                       for r in fases.values() if 'boundaries' in r),
            shared_issuers_matched=sum(len(r['bindings']['shared_issuers_matched']) +
                                       len(r['boundaries']['shared_issuers_matched'])
                                       for r in fases.values() if 'bindings' in r)),
        allocation_records=dict(
            opening=[dict(part=p['part'], **p['opening_state']['allocation_records']) for p in partes],
            final=alocacoes_finais),
        final_indicators=dict(phase=nomes[-1], rng=ultima.get('rng'), indicators=ultima.get('indicators')),
        parts=partes, problems=problemas,
        timing=dict(per_part_seconds={p['part']: p['seconds'] for p in partes},
                    sum_of_parts_seconds=round(sum(p['seconds'] for p in partes), 1), run=tempos),
        phase_table=tabela_rle(fases, huds),
        phases={n: fases[n] for n in FASES_DETALHADAS if n in fases},
        unmodeled=[
            'stack words of MCICD_Play in the CalculGame frame bodies (uninitialized caller locals)',
            'EFLAGS and EIP',
            'bindings and boundaries issued inside policy display roots (DirectDraw COM calls, display ticks, '
            'palette, LoadPie inside RestoreAll), counted per phase in phase_table',
            'masked display-only state (cumulative exclusion_mask, 153,060 bytes) and the surfaces (outside the '
            'state; the policy proves no logic access to them)',
            'ProgIteration frame words: saved EDX/ECX/EBX = 0 and the MSG buffer [0x3000000, 0, 0, 0] (declared; '
            'checked through the between-frames exit registers)',
            'at each part opening after part 0: the opening full state, the -v2 allocation records (no phase of '
            'the run allocates or releases a block, and part 9\'s final records are compared in full) and the '
            'between_frames entry registers are declared inputs from the capture',
            'allocation-record metadata caller_return, stack and freed_caller_return (bench call-site metadata)',
            'the CalculGame return EAX (overwritten by AffGame before any use)'],
        summary=dict(result=resultado, phases=len(nomes), phases_equal=sum(1 for r in fases.values() if r['equal']),
                     parts_equal=sum(1 for p in partes if p['result'] == 'equal'),
                     crossings=sum(p['crossings']['count'] for p in partes),
                     crossings_writing_compared_bytes=sum(p['crossings']['writing_compared_bytes'] for p in partes),
                     hud_flag_equal=all(huds.values()), final_allocation_records_equal=bool(
                         (alocacoes_finais or {}).get('equal'))))


def escrever_prova(relatorios, saida_nome):
    saida = ROOT / saida_nome
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    prova = agregar(relatorios)
    ok = prova['summary']['result'] == 'equal' and not prova['source_dirty_paths']
    if not ok:
        saida = ROOT / '.local' / ('m2-3-proof-not-accepted-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(prova, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), summary=prova['summary'], problems=prova['problems'],
                          timing=prova['timing']), indent=1))
    return 0 if ok else 2


def tudo(paralelo, lease, relatorios, saida):
    """Every part in parallel (each a separate process, optionally under the heavy lease), then the proof."""
    if sujos():
        raise SystemExit('The one-command proof runs on a clean tree only')
    manifesto()
    t0 = time.monotonic()
    logs = ROOT / relatorios
    logs.mkdir(parents=True, exist_ok=True)

    def uma(n):
        cmd = [sys.executable, '-B', str(ROOT / SCRIPT), 'parte', str(n), '--relatorios', relatorios]
        if lease:
            cmd = [sys.executable, lease, f'ai-m23-p{n}', '--'] + cmd
        inicio = time.monotonic()
        with open(logs / f'parte{n:02d}.log', 'x') as log:
            codigo = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT).returncode
        return n, codigo, round(time.monotonic() - inicio, 1)

    # Part 9 (the raid, the longest) first, then the others in order.
    ordem = [PARTES - 1] + list(range(PARTES - 1))
    with ThreadPoolExecutor(max_workers=paralelo) as ex:
        resultados = list(ex.map(uma, ordem))
    for n, codigo, segundos in sorted(resultados):
        print(f'part {n}: exit {codigo}, {segundos} s wall', flush=True)
    with open(logs / 'tempo.json', 'x') as f:
        json.dump(dict(parallel=paralelo, lease=bool(lease), wall_seconds=round(time.monotonic() - t0, 1),
                       part_wall_seconds={n: s for n, _, s in sorted(resultados)},
                       part_exit_codes={n: c for n, c, _ in sorted(resultados)}), f, indent=1)
    return escrever_prova(relatorios, saida)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='comando', required=True)
    p = sub.add_parser('parte', help='compare one part (0..9) and write its report')
    p.add_argument('n', type=int, choices=range(PARTES))
    p.add_argument('--relatorios', help='repo-relative report folder (default .local/m2-3/prova-<revision>)')
    g = sub.add_parser('agregar', help='the proof from the 10 part reports')
    g.add_argument('--relatorios')
    g.add_argument('--saida', required=True)
    t = sub.add_parser('tudo', help='every part in parallel, then the proof')
    t.add_argument('--paralelo', type=int, default=4)
    t.add_argument('--lease', help="path of the machine's heavy_lease.py (each part takes one slot)")
    t.add_argument('--relatorios')
    t.add_argument('--saida', required=True)
    a = ap.parse_args()
    relatorios = a.relatorios or pasta_relatorios()
    if a.comando == 'parte':
        return rodar_parte(a.n, relatorios)
    if a.comando == 'agregar':
        return escrever_prova(relatorios, a.saida)
    return tudo(a.paralelo, os.path.abspath(a.lease) if a.lease else None, relatorios, a.saida)


if __name__ == '__main__':
    sys.exit(main())
