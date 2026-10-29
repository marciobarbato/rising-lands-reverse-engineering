"""Original-only checks of the committed whole-MissionLoad capture (no translation).

Runs, all on the intact executable with the declared fixture:
  A  capture inputs, oracle read-before-write footprint tracking enabled;
  B  capture inputs, oracle phase with 77,777-instruction segments;
  C  allocation fill 0x5a (fill mask + fill sensitivity);
  D  every skipped startup call returns a distinct marker EAX (skip-derived mask);
  E  different clock, install directory, CD drive letter, thread id and
     memory-status bytes (declared-Windows-input mask).
Checks: replay equality with the committed capture and code-section integrity
(A), segmentation invariance (B), fill independence (C), and a provenance-
classified list of every inherited byte MissionLoad reads before writing (A
with masks from C/D/E and the static skipped-store set).

    python3 -B pesquisas-paralelas/missoes/validar_carga_missao_original.py \
        --captura pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json \
        --relatorio pesquisas-paralelas/missoes/validacao/stage12-missionload-original-x86.json
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

import ambiente_missoes
import capturar_carga_missao_original as c
from oraculo_carga_missao import (BancadaCargaMissaoOriginal, PULOS_INICIO, PILHA, RETORNO_MISSION_LOAD)


CENARIO = 'v1'


def entradas_cenario(fill, clock, **kw):
    if CENARIO == 'v1':
        return c.entradas(fill, clock, **kw)
    import cenarios_oraculo
    return cenarios_oraculo.entradas_exibicao(fill, clock, **kw)


def rodar(entradas, *, pulos=None, segmento=None, pegada=False):
    t = time.monotonic()
    if CENARIO == 'v1':
        b = BancadaCargaMissaoOriginal(entradas, segundos=120, pulos=pulos or PULOS_INICIO)
    else:
        from oraculo_exibicao_missao import BancadaExibicaoOriginal
        b = BancadaExibicaoOriginal(entradas, segundos=300, pulos=pulos)
    b.iniciar_relogio()
    b.executar_inicio()
    pre = b.snapshot_entrada()['blocks']
    if pegada:
        b.iniciar_pegada()
    regs = b.executar_mission_load(300, instrucoes_segmento=segmento)
    return dict(bench=b, pre=pre, post=b.imagem(), regs=regs, seconds=round(time.monotonic()-t, 3),
                events=c.eventos_json(b.vinculos_declarados.eventos[b.evento_inicio_oraculo:]),
                code_after=b.sha256_codigo(), pegada=b.pegada() if pegada else None)


def mascara(x, y):
    """Byte addresses whose entry values differ between two runs (same layout required)."""
    if [(n, v[0], len(v[1])) for n, v in x.items()] != [(n, v[0], len(v[1])) for n, v in y.items()]:
        return None
    m = set()
    for n, (base, a) in x.items():
        b = y[n][1]
        if a != b:
            m.update(base+i for i in range(len(a)) if a[i] != b[i])
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--captura', required=True)
    ap.add_argument('--relatorio', required=True)
    ap.add_argument('--cenario', default='v1', choices=('v1', 'exibicao'))
    a = ap.parse_args()
    global CENARIO
    CENARIO = a.cenario
    if CENARIO == 'v1':
        pulos_base = PULOS_INICIO
    else:
        from oraculo_exibicao_missao import PULOS_EXIBICAO as pulos_base
    saida = ambiente_missoes.ROOT/a.relatorio
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    caminho = ambiente_missoes.ROOT/a.captura
    bruto = caminho.read_bytes()
    cap = json.loads(bruto)
    ni = cap['named_inputs']
    fill, clock = ni['allocation_fill'], ni['clock_ms'][0]

    A = rodar(entradas_cenario(fill, clock), pegada=True)
    bA = A['bench']
    replay = dict(seconds=A['seconds'], real_return=A['regs']['EIP'] == RETORNO_MISSION_LOAD,
                  al=A['regs']['EAX'] & 0xff,
                  inherited_equal=bA.resumo_imagem({k: v for k, v in A['pre'].items() if k != 'native_stack'})
                  == cap['inherited_state']['summary'],
                  final_equal=bA.resumo_imagem(A['post']) == cap['oracle']['final_state']['summary'],
                  binding_log_equal=A['events'] == cap['oracle']['binding_events'],
                  note='footprint hooks were active in this replay')
    codigo = dict(exe_code_sha256=bA.sha256_codigo_exe, before=bA.sha256_codigo_inicial, after=A['code_after'],
                  capture_before=cap['code_integrity']['before'], capture_after=cap['code_integrity']['after'],
                  unchanged=len({bA.sha256_codigo_exe, bA.sha256_codigo_inicial, A['code_after'],
                                 cap['code_integrity']['before'], cap['code_integrity']['after']}) == 1)

    B = rodar(entradas_cenario(fill, clock), segmento=77777)
    segmentacao = dict(oracle_instructions_per_segment=[cap['limits']['instructions_per_segment'], 77777],
                       oracle_segments=[cap['oracle']['segments'], B['bench'].execucoes-B['bench'].segmentos_inicio_oraculo],
                       entry_equal=B['pre'] == A['pre'], final_equal=B['post'] == A['post'],
                       binding_log_equal=B['events'] == A['events'],
                       al_equal=(B['regs']['EAX'] & 0xff) == (A['regs']['EAX'] & 0xff),
                       real_return=B['regs']['EIP'] == RETORNO_MISSION_LOAD, seconds=B['seconds'])

    C = rodar(entradas_cenario(0x5a if fill != 0x5a else 0x3c, clock))
    preench, outros, copiados = 0, 0, 0
    for n, (base, x) in A['post'].items():
        y = C['post'][n][1]
        p, q = A['pre'][n][1], C['pre'][n][1]
        for i in range(len(x)) if x != y else ():
            if x[i] != y[i]:
                if x[i] == fill:
                    preench += 1
                    copiados += p[i] == q[i]
                else:
                    outros += 1
    sensibilidade = dict(fills=[hex(fill), hex(C['bench'].arena.preenchimento)],
                         final_bytes_still_holding_fill=preench, final_bytes_differing_otherwise=outros,
                         fill_bytes_copied_by_missionload=copiados, binding_log_equal=C['events'] == A['events'],
                         real_return=C['regs']['EIP'] == RETORNO_MISSION_LOAD, seconds=C['seconds'])

    marcadores = {n: (0x7d000000+0x1000*i, limpeza) for i, (n, (_, limpeza)) in enumerate(sorted(pulos_base.items()))}
    D = rodar(entradas_cenario(fill, clock), pulos=marcadores)
    E = rodar(entradas_cenario(fill, clock ^ 0x00777777, diretorio=b'C:\\JOGOS\\RISINGBR', unidade=b'E', id_thread=7,
                         estado_memoria=bytes(range(32))))
    mascaras = {'untouched_allocation_fill': mascara(A['pre'], C['pre']),
                'skip_derived_value': mascara(A['pre'], D['pre']),
                'declared_windows_input': mascara(A['pre'], E['pre'])}
    estaticos = set()
    for (ad, tam, _), _ in bA.conjunto_vigiado().items():
        estaticos.update(range(ad, ad+tam))

    classes, faixas = {}, []
    for inicio, fim, leitor in A['pegada']:
        atual = None
        for endereco in range(inicio, fim+1):
            if endereco < fim:
                rot = []
                for nome, m in mascaras.items():
                    if m is None:
                        rot.append(nome+'_layout_mismatch')
                    elif endereco in m:
                        rot.append(nome)
                if endereco in estaticos:
                    rot.append('skipped_routine_static_store')
                if PILHA <= endereco < PILHA+0x10000:
                    rot.append('native_stack_entry_frame_or_stale')
                rot = tuple(rot) or ('startup_executed_original_code_or_pe_image',)
            else:
                rot = None
            if atual and rot == atual[2] and endereco == atual[1]:
                atual[1] += 1
                continue
            if atual:
                faixas.append(dict(start=hex(atual[0]), end=hex(atual[1]), bytes=atual[1]-atual[0],
                                   classes=list(atual[2]), first_reader=leitor))
                for k in atual[2]:
                    classes[k] = classes.get(k, 0)+atual[1]-atual[0]
            atual = [endereco, endereco+1, rot] if rot else None
    def propagado(R, mascara_entrada):
        diff = mascara(A['post'], R['post'])
        return None if diff is None or mascara_entrada is None else len(diff-mascara_entrada)
    leitores = {}
    for f in faixas:
        for k in f['classes']:
            leitores.setdefault(k, {})
            leitores[k][f['first_reader']] = leitores[k].get(f['first_reader'], 0)+f['bytes']
    pegada = dict(read_before_write_bytes=sum(f['bytes'] for f in faixas), ranges=len(faixas),
                  bytes_by_class=dict(sorted(classes.items())), mask_sizes={k: (None if m is None else len(m))
                                                                           for k, m in mascaras.items()},
                  first_readers_by_class={k: dict(sorted(v.items())) for k, v in sorted(leitores.items())},
                  perturbation_runs=dict(
                      D=dict(real_return=D['regs']['EIP'] == RETORNO_MISSION_LOAD, seconds=D['seconds'],
                             final_bytes_differing_outside_entry_skip_mask=propagado(D, mascaras['skip_derived_value']),
                             binding_log_equal=D['events'] == A['events']),
                      E=dict(real_return=E['regs']['EIP'] == RETORNO_MISSION_LOAD, seconds=E['seconds'],
                             final_bytes_differing_outside_entry_input_mask=propagado(E, mascaras['declared_windows_input']))),
                  read_ranges=faixas,
                  method='Unicorn read/write hooks over DGROUP+.bss, CRT thread page, native stack and all '
                         'pre-entry arena bytes during the oracle only; binding writes mark destinations '
                         'written; host-side fixture reads (e.g. fopen path strings) are not counted')
    criticos = {'skip_derived_value', 'untouched_allocation_fill', 'skipped_routine_static_store'}
    aprovado = (replay['real_return'] and replay['inherited_equal'] and replay['final_equal']
                and replay['binding_log_equal'] and codigo['unchanged']
                and all(segmentacao[k] for k in ('entry_equal', 'final_equal', 'binding_log_equal', 'al_equal',
                                                 'real_return'))
                and sensibilidade['final_bytes_differing_otherwise'] == 0
                and sensibilidade['fill_bytes_copied_by_missionload'] == 0 and sensibilidade['binding_log_equal']
                and None not in mascaras.values())
    revisao = subprocess.run(['git', '-C', str(ambiente_missoes.ROOT), 'rev-parse', 'HEAD'],
                             capture_output=True, text=True).stdout.strip()
    relatorio = dict(schema='rising-lands/missionload-original-validation/1', source_revision=revisao,
                     scenario=CENARIO,
                     capture=a.captura, capture_sha256=hashlib.sha256(bruto).hexdigest(),
                     translation_executed=False, m1_accepted=False, replay=replay, code_integrity=codigo,
                     segmentation_invariance=segmentacao, allocation_fill_sensitivity=sensibilidade,
                     input_footprint=pegada,
                     critical_class_reads={k: classes.get(k, 0) for k in sorted(criticos)}, passed=aprovado)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    resumo = {k: v for k, v in relatorio.items() if k != 'input_footprint'}
    resumo['input_footprint'] = {k: v for k, v in pegada.items() if k != 'read_ranges'}
    print(json.dumps(resumo, indent=1))
    return 0 if aprovado else 1


if __name__ == '__main__':
    sys.exit(main())
