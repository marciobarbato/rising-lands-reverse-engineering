"""Original-only MONDE01 first-frame capture (M2.1), continuing the accepted M1 path.

Runs only the intact executable (no Python game translation is imported or
executed).  Phases: accepted M1 startup and MissionLoad, then (a) load_tail,
(b) between_frames, (c) frame1 (see oraculo_quadro_missao).  Writes the capture
and the readable entry trace with exclusive creation; a failed or interrupted
attempt is preserved under .local/ and exits nonzero.

    python3 -B pesquisas-paralelas/missoes/capturar_quadro_missao_original.py \
        --saida pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json \
        --rastro pesquisas-paralelas/missoes/evidencias/rastro-quadro1-monde01.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import ambiente_missoes
import capturar_carga_missao_original as c
from emulador import HASH_ORIGINAL, PILHA, RETORNO
from oraculo_carga_missao import OraculoInterrompido, RETORNO_MISSION_LOAD
from oraculo_quadro_missao import (BancadaQuadroMissaoOriginal, EntradasQuadro, FASES_QUADRO,
                                   NAO_EXECUTADOS_QUADRO, RETORNO_CALCUL_GAME, CALCUL_GAME)
from vinculos_declarados import ParadaVinculoDeclarado

ROOT = ambiente_missoes.ROOT
OWNED = ambiente_missoes.OWNED
CAPTURA_M1 = OWNED/'evidencias/captura-carga-missao-original-v2.json'
ENTRADA_M1 = OWNED/'evidencias/entrada-carga-missao-original.json'
FONTES = ('oraculo_carga_missao.py', 'fronteiras_carga_missao.py', 'capturar_carga_missao_original.py',
          'oraculo_quadro_missao.py', 'capturar_quadro_missao_original.py')


def entradas_quadro(preenchimento=0xa7, relogio=0x00123456, cursor=(0, 0), registradores=None, **base):
    regs = registradores or dict(ECX=0, EDX=0, ESI=0, EDI=0, EBP=0)
    return EntradasQuadro(
        base=c.entradas(preenchimento, relogio, **base), cursor=tuple(cursor), registradores_chamador=regs,
        proveniencia=dict(
            cursor='GetCursorPos answer. Equals the last SetCursorPos target of the accepted path (CalculGame '
                   '0x42c89e passes the words at 0x5099a8/0x5099aa, which ProgIteration fills from GetCursorPos); '
                   'Windows keeps the cursor there when the mouse does not move',
            caller_registers='declared saved ECX/EDX in ProgIteration\'s frame and carried ESI/EDI/EBP of '
                             '_WinMain@16 (never executed by the bench); influence measured by the sensitivity run',
            async_keys='no human input: every frame-phase GetAsyncKeyState answers 0',
            peek_message='no human input and no window message: PeekMessageA answers 0, so _WinMain@16 takes '
                         'the active-flag branch to ProgIteration'))


def eventos_json(eventos):
    return c.eventos_json(eventos)


def blocos_alterados(antes, depois):
    """Per-block change summary between two images (same names → byte diffs; new/removed blocks)."""
    saida = dict(changed={}, added=[], removed=[])
    for nome, (base, dados) in depois.items():
        if nome not in antes:
            saida['added'].append(nome)
            continue
        velho = antes[nome][1]
        if velho == dados:
            continue
        faixas, i, n = [], 0, len(dados)
        while i < n:
            if dados[i] != velho[i]:
                j = i
                while j < n and (dados[j] != velho[j] or (j+8 < n and dados[j+1:j+9] != velho[j+1:j+9])):
                    j += 1
                faixas.append((base+i, base+j+1))
                i = j+1
            else:
                i += 1
        saida['changed'][nome] = dict(base=hex(base), bytes_differing=sum(a != b for a, b in zip(dados, velho)),
                                      ranges=len(faixas),
                                      first_ranges=[[hex(a), hex(z)] for a, z in faixas[:400]])
    saida['removed'] = sorted(set(antes)-set(depois))
    return saida


def instantaneo(b, blocos, anterior):
    """Full snapshot: summary + per-block hashes; bytes of blocks changed since ``anterior``."""
    resumo = b.resumo_imagem(blocos)
    hashes = {n: dict(base=hex(base), bytes=len(d), sha256=hashlib.sha256(d).hexdigest())
              for n, (base, d) in blocos.items()}
    novos = {n: v for n, v in blocos.items() if anterior is None or anterior.get(n) != v}
    return dict(summary=resumo, block_hashes=hashes, blocks_changed_since_previous=b.serializar(novos),
                native_stack_sha256=hashlib.sha256(bytes(b.cpu.mem_read(PILHA, 0x10000))).hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--rastro', required=True)
    ap.add_argument('--segundos-quadro', type=float, default=600.0)
    ap.add_argument('--cenario', default='v1', choices=('v1', 'exibicao'))
    a = ap.parse_args()
    saida, caminho_rastro = ROOT/a.saida, ROOT/a.rastro
    for p in (saida, caminho_rastro):
        if p.exists():
            raise SystemExit(f'Refusing to overwrite existing evidence {p}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/missoes'],
                          capture_output=True, text=True).stdout
    import cenarios_oraculo
    from mapa_memoria_m1 import expandir_captura
    caminho_m1, caminho_entrada = (cenarios_oraculo.caminho(a.cenario, 'captura_m1'),
                                   cenarios_oraculo.caminho(a.cenario, 'entrada'))
    entrada_m1 = json.loads(caminho_entrada.read_bytes())
    m1 = expandir_captura(json.loads(caminho_m1.read_bytes()), entrada_m1)
    fill, clock = m1['named_inputs']['allocation_fill'], m1['named_inputs']['clock_ms'][0]
    if a.cenario == 'v1':
        q = entradas_quadro(fill, clock)
        b = BancadaQuadroMissaoOriginal(q, segundos=120)
        named = dict(m1=q.base.manifesto(), frame=q.manifesto())
    else:
        b, _, named = cenarios_oraculo.bancada(a.cenario, fill, clock, segundos=300)
    fontes = FONTES + (() if a.cenario == 'v1' else ('oraculo_exibicao_missao.py', 'cenarios_oraculo.py',
                                                       'mapa_memoria_m1.py', '../graficos-animacao/fronteiras_exibicao.py'))
    relatorio = dict(
        schema='rising-lands/monde01-frame1-original-capture/1', original_sha256=HASH_ORIGINAL, scenario=a.cenario,
        translation_executed=False, python_composition=False, m2_accepted=False,
        mission='MONDE01 (new campaign, mission byte 1)', source_revision=revisao,
        source_dirty_paths=sujo.splitlines(),
        source_sha256={n: hashlib.sha256((OWNED/n).read_bytes()).hexdigest() for n in fontes},
        m1_references=dict(capture=dict(path=str(caminho_m1.relative_to(ROOT)),
                                        sha256=hashlib.sha256(caminho_m1.read_bytes()).hexdigest()),
                           entry=dict(path=str(caminho_entrada.relative_to(ROOT)),
                                      sha256=hashlib.sha256(caminho_entrada.read_bytes()).hexdigest())),
        named_inputs=named,
        limits=dict(frame_seconds=a.segundos_quadro, instructions_per_segment=b.instrucoes_segmento,
                    segments=b.limite_segmentos, bindings=b.limite_vinculos_total, allocations=b.arena.maximo),
        boundary_policy=b.politica_fronteiras())
    t0, fase, resultado = time.monotonic(), 'startup', 2
    try:
        b.iniciar_relogio()
        b.executar_inicio()
        entrada = b.snapshot_entrada()
        relatorio['m1_path'] = dict(entry_summary=b.resumo_imagem(entrada['blocks']),
                                    entry_equal_committed=b.resumo_imagem(entrada['blocks']) == entrada_m1['summary'],
                                    startup_seconds=round(time.monotonic()-t0, 3))
        fase = 'oracle'
        regs = b.executar_mission_load(60)
        s0 = b.imagem()
        eventos_ml = eventos_json(b.vinculos_declarados.eventos[b.evento_inicio_oraculo:])
        relatorio['m1_path'].update(
            missionload_return=hex(regs['EIP']), al=regs['EAX'] & 0xff,
            final_equal_capture_v2=b.resumo_imagem(s0) == m1['oracle']['final_state']['summary'],
            binding_log_equal_capture_v2=eventos_ml == m1['oracle']['binding_events'],
            code_sha256=b.sha256_codigo())
        vigiado = b.conjunto_vigiado_quadro()
        b.vigiar_leituras(vigiado)
        relatorio['watched_unexecuted_writes'] = dict(
            routines=list(NAO_EXECUTADOS_QUADRO), ranges=[[hex(x), hex(z)] for x, z in b.intervalos_vigiados],
            sources=[dict(address=hex(k[0]), size=k[1], indexed=k[2], writers=v) for k, v in sorted(vigiado.items())])
        relatorio['state_s0'] = dict(summary=b.resumo_imagem(s0), equals=f'{caminho_m1.name} oracle.final_state',
                                     native_stack_sha256=hashlib.sha256(bytes(b.cpu.mem_read(PILHA, 0x10000))).hexdigest())
        anterior, fases = s0, []
        ddcalls = len(b.chamadas_exibicao()) if hasattr(b, 'chamadas_exibicao') else 0
        etapas = (('load_tail', lambda: b.executar_cauda_carga(a.segundos_quadro)),
                  ('between_frames', lambda: b.executar_entre_quadros(120)),
                  ('frame1', lambda: b.executar_quadro(a.segundos_quadro)))
        for nome, correr in etapas:
            fase = nome
            antes = b._estado_fase()
            t = time.monotonic()
            regs = correr()
            depois = b._estado_fase()
            imagem = b.imagem()
            fases.append(dict(
                phase=nome, seconds=round(time.monotonic()-t, 3), entry=antes, exit=depois,
                stop=hex(regs['EIP']),
                stop_routine='bench caller trampoline (load-state CalculGame called by the bench, as in M1)'
                if regs['EIP'] == RETORNO else b.nome(regs['EIP']),
                bindings=eventos_json(b.vinculos_declarados.eventos[antes['bindings']:depois['bindings']]),
                binding_counts=c._contar(b.vinculos_declarados.eventos[antes['bindings']:depois['bindings']]),
                boundaries=b.eventos_fronteira[antes['boundaries']:depois['boundaries']],
                windows_answers=[list(x) for x in b.windows.consumidos[antes['windows_answers']:depois['windows_answers']]],
                clock_answers=[list(x) for x in b.windows.consumidos[antes['windows_answers']:depois['windows_answers']]
                               if x[0] == 'clock'],
                allocations_created=depois['allocations']-antes['allocations'],
                memory_changes=blocos_alterados(anterior, imagem),
                state_after=instantaneo(b, imagem, anterior)))
            if nome == 'between_frames':
                fases[-1]['declared_caller_frame'] = b.declaracao_chamador
            if hasattr(b, 'estado_exibicao'):
                fases[-1]['display_state'] = b.estado_exibicao()
                fases[-1]['directdraw_calls'] = b.chamadas_exibicao()[ddcalls:]
                ddcalls = len(b.chamadas_exibicao())
            anterior = imagem
            relatorio['phases'] = fases
        relatorio['frame1_return'] = dict(reached=regs['EIP'] == RETORNO_CALCUL_GAME, eip=hex(regs['EIP']),
                                          eax=hex(regs['EAX']), calculgame_entry=hex(CALCUL_GAME))
        relatorio['watched_reads'] = [dict(address=hex(k[0]), size=k[1], reader=k[2], phase=k[3], count=v)
                                      for k, v in sorted(b.leituras_vigiadas.items())]
        sitios = b.sitios_escrita({(int(w['address'], 16), w['size']) for w in relatorio['watched_reads']})
        relatorio['watched_read_writer_sites'] = [
            dict(address=hex(a), size=n, sites=[dict(root=r, routine=rot, instruction=i, indexed=x) for r, rot, i, x in v])
            for (a, n), v in sorted(sitios.items())]
        relatorio['caller_eax_use_after_boundaries'] = b.uso_eax_retorno()
        relatorio['code_integrity'] = dict(exe_code_sha256=b.sha256_codigo_exe, before=b.sha256_codigo_inicial,
                                           after=b.sha256_codigo())
        resultado = 0 if relatorio['frame1_return']['reached'] else 2
    except (OraculoInterrompido, ParadaVinculoDeclarado, RuntimeError) as erro:
        relatorio['stop'] = dict(phase=fase, type=type(erro).__name__, reason=str(erro)[:4000],
                                 detail=getattr(erro, 'detalhe', None),
                                 registers={k: hex(v) for k, v in b._registros().items()},
                                 stack_scan=b.pilha_provavel(b._registros()['ESP']),
                                 boundaries=b.eventos_fronteira[-40:],
                                 last_bindings=eventos_json(b.vinculos_declarados.eventos[-5:]))
    relatorio['entry_trace'] = b.rastro_json()
    relatorio['allocations'] = b.arena.manifesto()
    relatorio['declared_windows_answers'] = [list(x) for x in b.windows.consumidos]
    relatorio['import_resolutions'] = b.importacoes_declaradas
    relatorio['total_seconds'] = round(time.monotonic()-t0, 3)
    if resultado:
        saida = ROOT/'.local'/(f'm2-frame1-{a.cenario}-failed-'+time.strftime('%Y%m%dT%H%M%S')+'.json')
        caminho_rastro = saida.with_suffix('.trace.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    rastro = dict(schema='rising-lands/monde01-frame1-entry-trace/1', original_sha256=HASH_ORIGINAL,
                  capture=str(saida.relative_to(ROOT)), capture_sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                  complete=not resultado,
                  method='Unicorn block hook over BEGTEXT: a routine is entered when a basic block starts at its '
                         'symbol address (relatorios/simbolos-originais.tsv); a top-level callee is a routine '
                         'whose stack return address lies in CalculGame (load_tail, frame1) or in ProgIteration/'
                         '_WinMain@16 (between_frames). Non-executed boundaries are listed under boundaries.',
                  phases=relatorio['entry_trace'],
                  boundaries=[dict(phase=e['phase'], routine=e['routine'], caller=e['caller'],
                                   top_callee=e['top_callee']) for p in relatorio.get('phases', ())
                              for e in p['boundaries']])
    with open(caminho_rastro, 'x') as f:
        json.dump(rastro, f, indent=1)
        f.write('\n')
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          trace=str(caminho_rastro), result='frame1_return' if not resultado else 'stopped',
                          m1_path=relatorio.get('m1_path'), stop=relatorio.get('stop', {}).get('reason'),
                          phases=[dict(phase=p['phase'], seconds=p['seconds'], stop=p['stop_routine'],
                                       bindings=p['binding_counts'], boundaries=len(p['boundaries']))
                                  for p in relatorio.get('phases', ())],
                          watched_reads=len(relatorio.get('watched_reads', [])),
                          total_seconds=relatorio['total_seconds']), indent=1))
    return resultado


if __name__ == '__main__':
    sys.exit(main())
