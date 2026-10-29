"""Original-only checks of the committed MONDE01 first-frame capture (no translation).

Runs, all on the intact executable with the declared fixture:
  A  capture inputs, read-before-write footprint over load_tail/between_frames/
     frame1 relative to the MissionLoad return state S0;
  B  capture inputs, 77,777-instruction segments from MissionLoad on;
  C  allocation fills 0x5a and 0x00 (fill mask + fill sensitivity);
  D  every non-executed routine (startup skips and frame boundaries) returns a
     distinct marker EAX (boundary-derived mask and propagation);
  E  different clock, install directory, CD drive, thread id, memory status
     (M1 declared-Windows-input mask);
  F  different frame inputs: cursor and declared caller registers.
Checks: replay equality with the committed capture, code-section integrity,
segmentation invariance, determinism (A vs capture vs B), fill independence,
boundary-EAX harmlessness, and a provenance-classified list of every byte the
three phases read before writing.

    python3 -B pesquisas-paralelas/missoes/validar_quadro_missao_original.py \
        --captura pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json \
        --relatorio pesquisas-paralelas/missoes/validacao/m2-frame1-original-x86.json
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

import ambiente_missoes
import capturar_carga_missao_original as c
import capturar_quadro_missao_original as cq
from emulador import PILHA
from oraculo_carga_missao import PULOS_INICIO
from oraculo_quadro_missao import (BancadaQuadroMissaoOriginal, FRONTEIRAS_QUADRO, FASES_QUADRO,
                                   RETORNO_CALCUL_GAME)

FASES = ('s0',) + FASES_QUADRO
QUADRO_CHAMADOR = (PILHA+0x8004, PILHA+0x8040)


CENARIO = 'v1'


def entradas(fill, clock, **kw):
    """Scenario inputs: EntradasQuadro (v1) or EntradasExibicao (display executed)."""
    if CENARIO == 'v1':
        return cq.entradas_quadro(fill, clock, **kw)
    import cenarios_oraculo
    return cenarios_oraculo.entradas_exibicao(fill, clock, **kw)


def rodar(q, *, pulos=None, fronteiras=None, segmento=None, pegada=False):
    t = time.monotonic()
    if CENARIO == 'v1':
        b = BancadaQuadroMissaoOriginal(q, segundos=120, pulos=pulos or PULOS_INICIO,
                                        fronteiras=fronteiras or FRONTEIRAS_QUADRO)
    else:
        from oraculo_exibicao_missao import BancadaExibicaoOriginal
        b = BancadaExibicaoOriginal(q, segundos=300, pulos=pulos, fronteiras=fronteiras)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(300, instrucoes_segmento=segmento)
    imagens = dict(s0=b.imagem())
    eventos = dict(s0=len(b.vinculos_declarados.eventos))
    if pegada:
        b.iniciar_pegada()
    for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                         ('between_frames', lambda: b.executar_entre_quadros(120)),
                         ('frame1', lambda: b.executar_quadro(600))):
        regs = correr()
        imagens[nome] = b.imagem()
        eventos[nome] = len(b.vinculos_declarados.eventos)
        if pegada:
            b.marcar_escritas_fase()
    todos = c.eventos_json(b.vinculos_declarados.eventos)
    logs = {f: todos[eventos[FASES[i-1]]:eventos[f]] for i, f in enumerate(FASES) if i}
    return dict(bench=b, images=imagens, logs=logs, regs=regs, seconds=round(time.monotonic()-t, 3),
                reached=regs['EIP'] == RETORNO_CALCUL_GAME, code_after=b.sha256_codigo(),
                boundaries=b.eventos_fronteira, windows=[list(x) for x in b.windows.consumidos],
                trace=b.rastro_json(), pegada=b.pegada() if pegada else None,
                writes=getattr(b, 'escritas_por_fase', None))


def mascara(x, y):
    if [(n, v[0], len(v[1])) for n, v in x.items()] != [(n, v[0], len(v[1])) for n, v in y.items()]:
        return None
    m = set()
    for n, (base, a) in x.items():
        b = y[n][1]
        if a != b:
            m.update(base+i for i in range(len(a)) if a[i] != b[i])
    return m


def faixas(enderecos, limite=200):
    saida, ordem = [], sorted(enderecos)
    for a in ordem:
        if saida and a == saida[-1][1]:
            saida[-1][1] += 1
        else:
            saida.append([a, a+1])
    return dict(bytes=len(ordem), ranges=len(saida), first_ranges=[[hex(a), hex(z)] for a, z in saida[:limite]])


def diferenca_rastro(x, y):
    """Per phase: routines whose entry counts differ between two entry traces."""
    saida = {}
    for fase in sorted(set(x) | set(y)):
        cx = {r['routine']: r['entries'] for r in x.get(fase, {}).get('routines_in_first_entry_order', [])}
        cy = {r['routine']: r['entries'] for r in y.get(fase, {}).get('routines_in_first_entry_order', [])}
        d = {n: [cx.get(n, 0), cy.get(n, 0)] for n in sorted(set(cx) | set(cy)) if cx.get(n, 0) != cy.get(n, 0)}
        if d:
            saida[fase] = d
    return saida


def diferenca_fronteiras(x, y):
    from collections import Counter
    cx = Counter((e['phase'], e['routine'], e['caller']) for e in x)
    cy = Counter((e['phase'], e['routine'], e['caller']) for e in y)
    return [dict(phase=k[0], routine=k[1], caller=k[2], counts=[cx.get(k, 0), cy.get(k, 0)])
            for k in sorted(set(cx) | set(cy)) if cx.get(k, 0) != cy.get(k, 0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', required=True)
    ap.add_argument('--relatorio', required=True)
    ap.add_argument('--cenario', default='v1', choices=('v1', 'exibicao'))
    a = ap.parse_args()
    global CENARIO
    CENARIO = a.cenario
    global QUADRO_CHAMADOR
    if CENARIO == 'v1':
        pulos_base, fronteiras_base = PULOS_INICIO, FRONTEIRAS_QUADRO
    else:
        from oraculo_exibicao_missao import PULOS_EXIBICAO as pulos_base, FRONTEIRAS_EXIBICAO as fronteiras_base
        QUADRO_CHAMADOR = (PILHA+0x8000, PILHA+0x8020)   # _WinMain@16 MSG buffer and saved EBX
    saida = ambiente_missoes.ROOT/a.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    bruto = (ambiente_missoes.ROOT/a.captura).read_bytes()
    cap = json.loads(bruto)
    ni = cap['named_inputs']['m1']
    fill, clock = ni['allocation_fill'], ni['clock_ms'][0]
    q = entradas(fill, clock)

    A = rodar(q, pegada=True)
    bA = A['bench']
    fases_cap = {p['phase']: p for p in cap['phases']}
    replay = dict(seconds=A['seconds'], frame1_return=A['reached'],
                  s0_equal=bA.resumo_imagem(A['images']['s0']) == cap['state_s0']['summary'],
                  phase_states_equal={f: bA.resumo_imagem(A['images'][f]) == fases_cap[f]['state_after']['summary']
                                      for f in FASES_QUADRO},
                  binding_logs_equal={f: A['logs'][f] == fases_cap[f]['bindings'] for f in FASES_QUADRO},
                  boundaries_equal=A['boundaries'] == [e for f in FASES_QUADRO for e in fases_cap[f]['boundaries']],
                  windows_answers_equal=A['windows'] == cap['declared_windows_answers'],
                  entry_trace_equal=json.loads(json.dumps(A['trace'])) == cap['entry_trace'],
                  note='footprint hooks were active in this replay')
    replay['passed'] = (replay['frame1_return'] and replay['s0_equal'] and all(replay['phase_states_equal'].values())
                        and all(replay['binding_logs_equal'].values()) and replay['boundaries_equal']
                        and replay['windows_answers_equal'] and replay['entry_trace_equal'])
    codigo = dict(exe_code_sha256=bA.sha256_codigo_exe, before=bA.sha256_codigo_inicial, after=A['code_after'],
                  capture_after=cap['code_integrity']['after'],
                  unchanged=len({bA.sha256_codigo_exe, bA.sha256_codigo_inicial, A['code_after'],
                                 cap['code_integrity']['after']}) == 1)

    B = rodar(q, segmento=77777)
    segmentacao = dict(instructions_per_segment=[cap['limits']['instructions_per_segment'], 77777],
                       states_equal={f: B['images'][f] == A['images'][f] for f in FASES},
                       binding_logs_equal={f: B['logs'][f] == A['logs'][f] for f in FASES_QUADRO},
                       boundaries_equal=B['boundaries'] == A['boundaries'], trace_equal=B['trace'] == A['trace'],
                       frame1_return=B['reached'], seconds=B['seconds'])
    segmentacao['passed'] = (B['reached'] and all(segmentacao['states_equal'].values())
                             and all(segmentacao['binding_logs_equal'].values()) and segmentacao['boundaries_equal']
                             and segmentacao['trace_equal'])

    sensibilidade = {}
    for alternativo in [x for x in (0x5a, 0x00, 0x3c) if x != fill][:2]:
        C = rodar(entradas(alternativo, clock))
        fases = {}
        for f in FASES_QUADRO:
            preench, outros = 0, set()
            for n, (base, x) in A['images'][f].items():
                y = C['images'][f][n][1]
                if x != y:
                    for i in range(len(x)):
                        if x[i] != y[i]:
                            if x[i] == fill and y[i] == alternativo:
                                preench += 1
                            else:
                                outros.add(base+i)
            fases[f] = dict(bytes_still_holding_fill=preench, bytes_differing_otherwise=faixas(outros, 60))
        sensibilidade[hex(alternativo)] = dict(
            phases=fases, binding_logs_equal=all(C['logs'][f] == A['logs'][f] for f in FASES_QUADRO),
            boundary_differences=diferenca_fronteiras(A['boundaries'], C['boundaries']),
            entry_trace_differences=diferenca_rastro(A['trace'], C['trace']),
            frame1_return=C['reached'], seconds=C['seconds'])
        sensibilidade[hex(alternativo)]['independent'] = (
            C['reached'] and sensibilidade[hex(alternativo)]['binding_logs_equal']
            and all(v['bytes_differing_otherwise']['bytes'] == 0 for v in fases.values()))
    sensibilidade = dict(capture_fill=hex(fill), runs=sensibilidade,
                         independent=all(v['independent'] for v in sensibilidade.values()))

    marcadores = {n: (0x7d000000+0x1000*i, l) for i, (n, (_, l)) in enumerate(sorted(pulos_base.items()))}
    marcadores_quadro = {n: (0x7e000000+0x1000*i, l, r) for i, (n, (_, l, r)) in enumerate(sorted(fronteiras_base.items()))}
    D = rodar(q, pulos=marcadores, fronteiras=marcadores_quadro)
    E = rodar(entradas(fill, clock ^ 0x00777777, diretorio=b'C:\\JOGOS\\RISINGBR', unidade=b'E',
                       id_thread=7, estado_memoria=bytes(range(32))))
    F = rodar(entradas(fill, clock, cursor=(320, 240),
                       registradores=dict(ECX=0x11111111, EDX=0x22222222, ESI=0x33333333,
                                          EDI=0x44444444, EBP=0x55555555)))
    G = None
    if CENARIO != 'v1':
        G = rodar(entradas(fill, clock, ticks=tuple(0x00500000+17*k for k in range(1, 4097)), superficie=0x5a))
    mascaras = {'untouched_allocation_fill': mascara(A['images']['s0'], C['images']['s0']),
                'skip_derived_value': mascara(A['images']['s0'], D['images']['s0']),
                'declared_windows_input': mascara(A['images']['s0'], E['images']['s0'])}
    propagacao = {}
    for rotulo, R, chave in (('D_boundary_markers', D, 'skip_derived_value'),
                             ('E_m1_windows_inputs', E, 'declared_windows_input'),
                             ('F_frame_inputs', F, None)) + ((('G_display_inputs', G, None),) if G else ()):
        base_mask = mascaras[chave] if chave else set()
        propagacao[rotulo] = dict(
            frame1_return=R['reached'], seconds=R['seconds'],
            binding_logs_equal={f: R['logs'][f] == A['logs'][f] for f in FASES_QUADRO},
            boundary_sequence_equal=[(e['routine'], e['caller_return']) for e in R['boundaries']]
            == [(e['routine'], e['caller_return']) for e in A['boundaries']],
            boundary_differences=diferenca_fronteiras(A['boundaries'], R['boundaries']),
            trace_equal=R['trace'] == A['trace'], entry_trace_differences=diferenca_rastro(A['trace'], R['trace']),
            differing_outside_s0_mask={f: (None if mascara(A['images'][f], R['images'][f]) is None or base_mask is None
                                           else faixas(mascara(A['images'][f], R['images'][f])-base_mask, 60))
                                       for f in FASES_QUADRO})

    estaticos = set()
    for (ad, tam, _), _ in bA.conjunto_vigiado_quadro().items():
        estaticos.update(range(ad, ad+tam))
    m1_estaticos = set()
    for (ad, tam, _), _ in bA.conjunto_vigiado().items():
        m1_estaticos.update(range(ad, ad+tam))
    classes, lista = {}, []
    for inicio, fim, leitor, fase in A['pegada']:
        atual = None
        for endereco in range(inicio, fim+1):
            if endereco < fim:
                rot = [n if m is not None else n+'_layout_mismatch' for n, m in mascaras.items()
                       if m is None or endereco in m]
                if endereco in estaticos:
                    rot.append('frame_unexecuted_routine_static_store')
                if endereco in m1_estaticos:
                    rot.append('m1_unexecuted_routine_static_store')
                if QUADRO_CHAMADOR[0] <= endereco < QUADRO_CHAMADOR[1]:
                    rot.append('declared_caller_frame' if CENARIO == 'v1' else 'declared_window_loop_frame')
                elif PILHA <= endereco < PILHA+0x10000:
                    rot.append('native_stack_bench_or_stale')
                rot = tuple(rot) or ('executed_original_code_or_pe_image',)
            else:
                rot = None
            if atual and rot == atual[2] and endereco == atual[1]:
                atual[1] += 1
                continue
            if atual:
                lista.append(dict(start=hex(atual[0]), end=hex(atual[1]), bytes=atual[1]-atual[0],
                                  classes=list(atual[2]), first_reader=leitor, phase=fase))
                for k in atual[2]:
                    classes[k] = classes.get(k, 0)+atual[1]-atual[0]
            atual = [endereco, endereco+1, rot] if rot else None
    leitores = {}
    for f in lista:
        for k in f['classes']:
            chave = f"{f['phase']}:{f['first_reader']}"
            leitores.setdefault(k, {})
            leitores[k][chave] = leitores[k].get(chave, 0)+f['bytes']
    por_fase = {}
    for f in lista:
        por_fase[f['phase']] = por_fase.get(f['phase'], 0)+f['bytes']
    pegada = dict(read_before_write_bytes=sum(f['bytes'] for f in lista), ranges=len(lista),
                  bytes_by_phase=por_fase, bytes_by_class=dict(sorted(classes.items())),
                  mask_sizes={k: (None if m is None else len(m)) for k, m in mascaras.items()},
                  first_readers_by_class={k: dict(sorted(v.items())) for k, v in sorted(leitores.items())},
                  written_bytes_cumulative_by_phase=A['writes'], read_ranges=lista,
                  method='Unicorn read/write hooks (translation cache flushed after adding them) over DGROUP+.bss, '
                         'the CRT thread page, the native stack and every arena byte allocated before the load '
                         'tail, from the MissionLoad return through frame1; binding writes mark destinations '
                         'written; a byte is attributed to the phase of its first read')
    criticos = ('skip_derived_value', 'untouched_allocation_fill', 'frame_unexecuted_routine_static_store',
                'm1_unexecuted_routine_static_store')
    d = propagacao['D_boundary_markers']
    # Bench integrity and boundary harmlessness gate the capture.  Fill
    # sensitivity is a property of the original program (it reads GlobalAlloc
    # bytes it never wrote) and is reported, not gated.
    aprovado = (replay['passed'] and codigo['unchanged'] and segmentacao['passed']
                and d['frame1_return'] and all(d['binding_logs_equal'].values())
                and all(v is not None and v['bytes'] == 0 for v in d['differing_outside_s0_mask'].values())
                and None not in mascaras.values())
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    relatorio = dict(schema='rising-lands/monde01-frame1-original-validation/1', source_revision=revisao,
                     scenario=CENARIO,
                     capture=a.captura, capture_sha256=hashlib.sha256(bruto).hexdigest(),
                     translation_executed=False, m2_accepted=False, replay=replay, code_integrity=codigo,
                     segmentation_invariance=segmentacao, allocation_fill_sensitivity=sensibilidade,
                     sensitivity_runs=propagacao, input_footprint=pegada,
                     critical_class_reads={k: classes.get(k, 0) for k in criticos}, passed=aprovado)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    resumo = {k: v for k, v in relatorio.items() if k != 'input_footprint'}
    resumo['input_footprint'] = {k: v for k, v in pegada.items() if k not in ('read_ranges', 'first_readers_by_class')}
    print(json.dumps(resumo, indent=1)[:20000])
    return 0 if aprovado else 1


if __name__ == '__main__':
    sys.exit(main())
