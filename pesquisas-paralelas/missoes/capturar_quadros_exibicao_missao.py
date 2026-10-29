"""Original-only MONDE01 N-frame capture of the display reference (M2.2), in delta form.

Runs only the intact executable (no Python game translation is imported or
executed): the ``-v2`` display scenario (``cenarios_oraculo`` 'exibicao') from
program start through MissionLoad, then load_tail and N frames, each frame k as
between_frames(k) and frame(k) (``BancadaExibicaoOriginal.executar_quadros``).

Each phase records what the M2.1 capture records (entry/exit registers, RNGs
and counts, bindings, boundaries, Windows and clock answers, DirectDraw calls
and display state) plus an exact ``state_delta`` against the previous phase's
state, ``state_after.summary`` and, at the checkpoint frames, the full state
(``delta_estado_missao``).  ``observed`` lists the few words the scenario
decisions are about: the CD-audio flag 0x4e2f28 (no CD track plays, so it must
stay 0), the shared permutation cursor 0x4e1d18, the HUD flag 0x4e05a2, the
cycle counter 0x508f7c and the view origin 0x508720/22.

The first three phases must equal the committed ``-v2`` frame-1 capture
(state summaries, bindings, boundaries, Windows answers); a difference stops the
run.  The raw JSON is written under ``.local/``; the committed artifact is its
xz encoding plus a manifest that pins both hashes and the result of the replay
check (s0 + deltas rebuild every summary and checkpoint).  A failed attempt is
preserved under ``.local/`` and exits nonzero.  The process ends with
``encerramento_captura.encerrar_captura`` (fsync, ``os._exit``).

    python3 -B pesquisas-paralelas/missoes/capturar_quadros_exibicao_missao.py --quadros 128 \
        --saida pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz
"""
import argparse
import hashlib
import json
import lzma
import struct
import subprocess
import sys
import time

import ambiente_missoes
import capturar_carga_missao_original as c
import delta_estado_missao as delta
from emulador import HASH_ORIGINAL, PILHA, RETORNO
from oraculo_carga_missao import OraculoInterrompido
from oraculo_quadro_missao import RETORNO_CALCUL_GAME, CALCUL_GAME, nomes_fases
from vinculos_declarados import ParadaVinculoDeclarado

ROOT = ambiente_missoes.ROOT
OWNED = ambiente_missoes.OWNED
CHECKPOINTS = (1, 31, 32, 45, 50, 51, 52, 64, 100, 101, 128)
FASES_M21 = ('load_tail', 'between_frames', 'frame1')
FONTES = ('oraculo_carga_missao.py', 'fronteiras_carga_missao.py', 'capturar_carga_missao_original.py',
          'oraculo_quadro_missao.py', 'capturar_quadro_missao_original.py', 'oraculo_exibicao_missao.py',
          'cenarios_oraculo.py', 'mapa_memoria_m1.py', 'delta_estado_missao.py',
          'capturar_quadros_exibicao_missao.py', '../graficos-animacao/fronteiras_exibicao.py')
PALAVRAS = (('cd_audio_flag_0x4e2f28', 0x4e2f28, 1), ('permutation_cursor_0x4e1d18', 0x4e1d18, 4),
            ('hud_flag_0x4e05a2', 0x4e05a2, 1), ('cycle_counter_0x508f7c', 0x508f7c, 4),
            ('view_origin_x_0x508720', 0x508720, 2), ('view_origin_y_0x508722', 0x508722, 2))
AUDIO_CD = dict(
    cd_track_playing=False, flag=hex(0x4e2f28), flag_value=0,
    provenance='declared input: no CD audio track plays (MCICD_Init is never executed, so [0x4e2f28] stays 0). '
               'CalculGame then takes its CD branch every frame: it reads the permutation table '
               '0x4e1c18[0x4e1d18], advances the shared cursor 0x4e1d18 and calls the MCICD_Play boundary. '
               'Game logic shares that cursor (NextAnimVeget, NextAnimTerrain), so this input changes logic '
               'state over long runs; a CD-playing scenario is a different declared input')
DECISOES = dict(
    hud_flag_0x4e05a2='compared: AffGame and CalculMatiere write it (coordinator decision, M2.2)',
    menuinit_freed_records='the 146 MenuInit bank allocation records freed in load_tail are compared',
    cd_audio='no CD track playing, declared in named_inputs.cd_audio',
    comparison_mask='only the cumulative mask of politica_comparacao_quadros.py --quadros N may exclude bytes')


def sem_caminho_host(valor):
    """Provenance strings naming a host path to the read-only media become workspace-relative ('source/...').

    Only provenance metadata carries these paths; no host path reaches emulated memory or a hashed input."""
    if isinstance(valor, dict):
        return {k: sem_caminho_host(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [sem_caminho_host(v) for v in valor]
    if isinstance(valor, str) and valor.startswith('/') and '/source/' in valor:
        return 'source/' + valor.split('/source/', 1)[1]
    return valor


def ler(b, endereco, largura):
    return int.from_bytes(bytes(b.cpu.mem_read(endereco, largura)), 'little')


def observar(b):
    return {nome: hex(ler(b, a, n)) for nome, a, n in PALAVRAS}


def registrar_fase(b, nome, regs, antes, depois, anterior, imagem, ddcalls, checkpoints, segundos):
    """One phase record of the capture (shared with the segmented runs of segmentos_quadros_missao)."""
    registro = dict(
        phase=nome, seconds=segundos, entry=antes, exit=depois,
        stop=hex(regs['EIP']),
        stop_routine='bench caller trampoline (load-state CalculGame called by the bench, as in M1)'
        if regs['EIP'] == RETORNO else b.nome(regs['EIP']),
        bindings=c.eventos_json(b.vinculos_declarados.eventos[antes['bindings']:depois['bindings']]),
        binding_counts=c._contar(b.vinculos_declarados.eventos[antes['bindings']:depois['bindings']]),
        boundaries=b.eventos_fronteira[antes['boundaries']:depois['boundaries']],
        windows_answers=[list(x) for x in b.windows.consumidos[antes['windows_answers']:depois['windows_answers']]],
        clock_answers=[list(x) for x in b.windows.consumidos[antes['windows_answers']:depois['windows_answers']]
                       if x[0] == 'clock'],
        allocations_created=depois['allocations']-antes['allocations'],
        display_state=b.estado_exibicao(), directdraw_calls=b.chamadas_exibicao()[ddcalls:],
        observed=observar(b),
        state_delta=delta.delta(anterior, imagem),
        state_after=dict(summary=b.resumo_imagem(imagem)))
    if nome == 'between_frames':
        registro['declared_caller_frame'] = b.declaracao_chamador
    if nome.startswith('frame') and int(nome[5:]) in checkpoints:
        registro['state_after']['full_state'] = delta.estado_completo(imagem)
    if registro['observed']['cd_audio_flag_0x4e2f28'] != '0x0':
        raise RuntimeError(f'{nome}: [0x4e2f28] left the declared no-CD-audio value')
    return registro


def comparar_m21(fase, registro, referencia):
    """Differences of an M2.1 phase against the committed -v2 frame-1 capture (empty when equal).

    The live record is compared in its JSON form (tuples become lists), as it will be written."""
    registro = json.loads(json.dumps(registro, sort_keys=True))
    diferencas = []
    if registro['state_after']['summary'] != referencia['state_after']['summary']:
        diferencas.append('state_after.summary')
    for chave in ('bindings', 'boundaries', 'windows_answers', 'clock_answers', 'stop', 'directdraw_calls',
                  'display_state', 'allocations_created'):
        if registro.get(chave) != referencia.get(chave):
            diferencas.append(chave)
    for chave in ('registers', 'rng'):
        for lado in ('entry', 'exit'):
            if registro[lado][chave] != referencia[lado][chave]:
                diferencas.append(f'{lado}.{chave}')
    return diferencas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, required=True)
    ap.add_argument('--saida', required=True, help='repo-relative .json.xz artifact')
    ap.add_argument('--segundos-quadro', type=float, default=600.0)
    a = ap.parse_args()
    if not a.saida.endswith('.json.xz'):
        raise SystemExit('--saida must name a .json.xz artifact')
    saida = ROOT/a.saida
    manifesto_caminho = saida.with_name(saida.name[:-len('.json.xz')]+'.manifest.json')
    bruto = ROOT/'.local'/'m2-2'/saida.name[:-len('.xz')]
    for p in (saida, manifesto_caminho, bruto):
        if p.exists():
            raise SystemExit(f'Refusing to overwrite existing evidence {p}')
    checkpoints = tuple(k for k in CHECKPOINTS if k <= a.quadros)
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'pesquisas-paralelas/missoes'],
                          capture_output=True, text=True).stdout
    import cenarios_oraculo
    from mapa_memoria_m1 import carregar_json, expandir_captura
    caminho_m1, caminho_entrada = cenarios_oraculo.caminho('exibicao', 'captura_m1'), cenarios_oraculo.caminho('exibicao', 'entrada')
    caminho_q1 = cenarios_oraculo.caminho('exibicao', 'captura_quadro')
    entrada_m1 = json.loads(caminho_entrada.read_bytes())
    m1 = expandir_captura(json.loads(caminho_m1.read_bytes()), entrada_m1)
    q1 = carregar_json(caminho_q1)
    referencia_m21 = {f['phase']: f for f in q1['phases']}
    fill, clock = m1['named_inputs']['allocation_fill'], m1['named_inputs']['clock_ms'][0]
    b, _, named = cenarios_oraculo.bancada('exibicao', fill, clock, segundos=300)
    named = sem_caminho_host(named)
    named['cd_audio'] = AUDIO_CD
    relatorio = dict(
        schema='rising-lands/monde01-n-frame-original-capture-delta/1', original_sha256=HASH_ORIGINAL,
        scenario='exibicao', translation_executed=False, python_composition=False, m2_accepted=False,
        mission='MONDE01 (new campaign, mission byte 1)', frames=a.quadros, checkpoint_frames=list(checkpoints),
        state_form='delta', source_revision=revisao, source_dirty_paths=sujo.splitlines(),
        source_sha256={n: hashlib.sha256((OWNED/n).read_bytes()).hexdigest() for n in FONTES},
        references=dict(
            m1_capture=dict(path=str(caminho_m1.relative_to(ROOT)), sha256=hashlib.sha256(caminho_m1.read_bytes()).hexdigest()),
            m1_entry=dict(path=str(caminho_entrada.relative_to(ROOT)),
                          sha256=hashlib.sha256(caminho_entrada.read_bytes()).hexdigest()),
            frame1_capture=dict(path=str(caminho_q1.relative_to(ROOT)), sha256=hashlib.sha256(caminho_q1.read_bytes()).hexdigest())),
        named_inputs=named, decisions=DECISOES,
        limits=dict(frame_seconds=a.segundos_quadro, instructions_per_segment=b.instrucoes_segmento,
                    segments=b.limite_segmentos, bindings=b.limite_vinculos_total, allocations=b.arena.maximo),
        boundary_policy=b.politica_fronteiras(),
        display_context_per_event='not recorded: events carry no display-root flag in this capture')
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
        relatorio['m1_path'].update(
            missionload_return=hex(regs['EIP']), al=regs['EAX'] & 0xff,
            final_equal_capture_v2=b.resumo_imagem(s0) == m1['oracle']['final_state']['summary'],
            code_sha256=b.sha256_codigo())
        relatorio['state_s0'] = dict(summary=b.resumo_imagem(s0), equals=f'{caminho_m1.name} oracle.final_state',
                                     native_stack_sha256=hashlib.sha256(bytes(b.cpu.mem_read(PILHA, 0x10000))).hexdigest())
        if not relatorio['m1_path']['final_equal_capture_v2']:
            raise RuntimeError('MissionLoad final state differs from the committed -v2 capture')
        anterior, fases, m21 = s0, [], {}
        relatorio['phases'] = fases
        ddcalls = len(b.chamadas_exibicao())
        antes = b._estado_fase()
        t = time.monotonic()
        for nome, regs in b.executar_quadros(a.quadros, a.segundos_quadro):
            fase = nome
            depois = b._estado_fase()
            imagem = b.imagem()
            registro = registrar_fase(b, nome, regs, antes, depois, anterior, imagem, ddcalls, checkpoints,
                                      round(time.monotonic()-t, 3))
            ddcalls = len(b.chamadas_exibicao())
            if nome in referencia_m21:
                m21[nome] = comparar_m21(nome, registro, referencia_m21[nome])
                if m21[nome]:
                    relatorio['m21_reference'] = m21
                    relatorio['m21_first_difference'] = {
                        k: dict(capture=registro.get(k), reference=referencia_m21[nome].get(k))
                        for k in m21[nome] if '.' not in k}
                    raise RuntimeError(f'{nome} differs from the committed -v2 frame-1 capture in {m21[nome]}')
            fases.append(registro)
            anterior, antes, t = imagem, depois, time.monotonic()
        relatorio['m21_reference'] = dict(
            phases={k: 'equal' for k in m21},
            compared=['state_after.summary', 'bindings', 'boundaries', 'windows_answers', 'clock_answers', 'stop',
                      'directdraw_calls', 'display_state', 'allocations_created', 'entry/exit registers and rng'])
        relatorio['last_frame_return'] = dict(reached=regs['EIP'] == RETORNO_CALCUL_GAME, eip=hex(regs['EIP']),
                                              eax=hex(regs['EAX']), calculgame_entry=hex(CALCUL_GAME))
        relatorio['code_integrity'] = dict(exe_code_sha256=b.sha256_codigo_exe, before=b.sha256_codigo_inicial,
                                           after=b.sha256_codigo())
        ok_codigo = relatorio['code_integrity']['before'] == relatorio['code_integrity']['after']
        resultado = 0 if relatorio['last_frame_return']['reached'] and ok_codigo and len(fases) == 1+2*a.quadros else 2
    except (OraculoInterrompido, ParadaVinculoDeclarado, RuntimeError) as erro:
        relatorio['stop'] = dict(phase=fase, type=type(erro).__name__, reason=str(erro)[:4000],
                                 detail=getattr(erro, 'detalhe', None),
                                 registers={k: hex(v) for k, v in b._registros().items()},
                                 boundaries=b.eventos_fronteira[-40:],
                                 last_bindings=c.eventos_json(b.vinculos_declarados.eventos[-5:]))
    relatorio['entry_trace'] = b.rastro_json()
    relatorio['allocations'] = b.arena.manifesto()
    relatorio['declared_windows_answers'] = [list(x) for x in b.windows.consumidos]
    relatorio['import_resolutions'] = b.importacoes_declaradas
    relatorio['total_seconds'] = round(time.monotonic()-t0, 3)
    from encerramento_captura import encerrar_captura
    if resultado:
        falha = ROOT/'.local'/('m2-2-capture-failed-'+time.strftime('%Y%m%dT%H%M%S')+'.json')
        falha.parent.mkdir(parents=True, exist_ok=True)
        with open(falha, 'x') as f:
            json.dump(relatorio, f, indent=1, sort_keys=True)
            f.write('\n')
        print(json.dumps(dict(output=str(falha), stop=relatorio.get('stop', {}).get('reason'),
                              phases=len(relatorio.get('phases', ()))), indent=1))
        encerrar_captura(resultado, falha)
    bruto.parent.mkdir(parents=True, exist_ok=True)
    texto = (json.dumps(relatorio, indent=1, sort_keys=True)+'\n').encode()
    with open(bruto, 'xb') as f:
        f.write(texto)
    sha_bruto = hashlib.sha256(texto).hexdigest()
    filtro = [dict(id=lzma.FILTER_LZMA2, preset=9 | lzma.PRESET_EXTREME)]
    comprimido = lzma.compress(texto, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, filters=filtro)
    del texto, relatorio
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'xb') as f:
        f.write(comprimido)
    # Replay check from the written artifact: s0 + deltas must rebuild every summary and checkpoint.
    captura, sha_lido = delta.carregar(saida)
    try:
        replay = delta.verificar_replay(captura, delta.s0_exibicao())
        verificacao = dict(result='equal', phases=len(replay),
                           checkpoints=[r['phase'] for r in replay if r.get('checkpoint_full_state_equal')])
    except delta.ReplayDivergente as erro:
        verificacao, resultado = dict(result='diverged', reason=str(erro)), 3
    manifesto = dict(
        schema='rising-lands/compressed-evidence-manifest/1', artifact=str(saida.relative_to(ROOT)),
        encoding=dict(format='xz', check='crc64', filter='lzma2', preset='9e'),
        compressed=dict(sha256=hashlib.sha256(comprimido).hexdigest(), bytes=len(comprimido)),
        raw_json=dict(sha256=sha_bruto, bytes=bruto.stat().st_size, local_copy=str(bruto.relative_to(ROOT)),
                      decompressed_sha256_equal=sha_lido == sha_bruto),
        capture_schema=captura['schema'], frames=captura['frames'], phases=len(captura['phases']),
        checkpoint_frames=captura['checkpoint_frames'], source_revision=captura['source_revision'],
        source_dirty_paths=captura['source_dirty_paths'], replay_check=verificacao,
        command='python3 -B pesquisas-paralelas/missoes/capturar_quadros_exibicao_missao.py --quadros '
                f'{a.quadros} --saida {a.saida}')
    if sha_lido != sha_bruto:
        resultado = 3
    with open(manifesto_caminho, 'x') as f:
        json.dump(manifesto, f, indent=1)
        f.write('\n')
    print(json.dumps(dict(manifest=str(manifesto_caminho), replay=verificacao, raw=manifesto['raw_json'],
                          compressed=manifesto['compressed'], total_seconds=captura['total_seconds']), indent=1))
    encerrar_captura(resultado, bruto, saida, manifesto_caminho)


if __name__ == '__main__':
    sys.exit(main())
