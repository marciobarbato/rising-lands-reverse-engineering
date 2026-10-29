"""Original-only whole-MissionLoad capture for MONDE01 from the original program start.

Runs only the intact executable (no Python game translation exists or is
used). Writes a new evidence file with exclusive creation; a failed or
interrupted attempt is preserved under .local/ and exits nonzero.

    python3 -B pesquisas-paralelas/missoes/capturar_carga_missao_original.py \
        --saida pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original.json
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time

import ambiente_missoes
from fronteiras_carga_missao import EntradasNomeadas, rotulo_volume_iso
from oraculo_carga_missao import (BancadaCargaMissaoOriginal, OraculoInterrompido, MISSION_LOAD,
                                  RETORNO_MISSION_LOAD, NAO_EXECUTADOS)
from emulador import HASH_ORIGINAL
from vinculos_declarados import ParadaVinculoDeclarado

ROOT = ambiente_missoes.ROOT
BIN = ROOT.parent/'source/RISING_LANDS_BR_.BIN'


def entradas(preenchimento, relogio, diretorio=b'C:\\RISING', unidade=b'D', id_thread=1,
             estado_memoria=bytes(32)):
    rotulo, pvd = rotulo_volume_iso(BIN)
    return EntradasNomeadas(
        diretorio_instalacao=diretorio, unidade_cd=unidade, rotulo_cd=rotulo,
        relogio_ms=(relogio,), preenchimento_alocacao=preenchimento, estado_memoria=estado_memoria,
        teclas=((0x0d, 0x8000), (0x0d, 0), (0x0d, 0x8000), (0x0d, 0), (0x0d, 0x8000)), id_thread=id_thread,
        proveniencia=dict(
            install_directory='WINSTALL.INF TemplateTargetDir=RISING under drive C: (installer default); '
                              'machine-specific, used only to build profile/data paths',
            cd_drive='first drive FindCD probes (index 3); machine-specific',
            cd_volume_label=pvd,
            clock_ms='declared timeGetTime value consumed by iaRandom(0) in IaAlloc; real value is '
                     'nondeterministic, every value is an original execution',
            allocation_fill='declared initial byte of non-ZEROINIT GlobalAlloc memory '
                            '(Windows leaves GMEM_FIXED contents unspecified)',
            memory_status='32 zero bytes; consumed only as the GlobalCompact argument',
            async_keys='Enter pressed/released on the default item of menus 2 and 3, then Enter '
                       'on the research screen (no research branch click)',
            thread_id='stored only in CRT thread data +0xda'))


def eventos_json(eventos):
    saida = []
    for ev in eventos:
        e = dict(ev)
        e['registers_before'] = {k: hex(v) for k, v in e['registers_before'].items()}
        e['arguments'] = [hex(a & 0xffffffff) for a in e['arguments']]
        if 'results' in e:
            e['results'] = {k: hex(v) for k, v in e['results'].items()}
        saida.append(e)
    return saida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--entrada', help='also write the first-class MissionLoad entry snapshot here')
    ap.add_argument('--preenchimento', type=lambda x: int(x, 0), default=0xa7)
    ap.add_argument('--relogio', type=lambda x: int(x, 0), default=0x00123456)
    ap.add_argument('--segundos-inicio', type=float, default=120.0)
    ap.add_argument('--segundos-oraculo', type=float, default=60.0)
    ap.add_argument('--cenario', default='v1', choices=('v1', 'exibicao'),
                    help='v1: accepted M1 bench; exibicao: display path executed (cenarios_oraculo)')
    a = ap.parse_args()
    saida = ROOT/a.saida if not a.saida.startswith('/') else __import__('pathlib').Path(a.saida)
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                             text=True).stdout.strip()
    sujo = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--',
                           'pesquisas-paralelas/missoes'], capture_output=True, text=True).stdout
    nomes = ('oraculo_carga_missao.py', 'fronteiras_carga_missao.py', 'capturar_carga_missao_original.py')
    if a.cenario != 'v1':
        nomes += ('oraculo_quadro_missao.py', 'oraculo_exibicao_missao.py', 'cenarios_oraculo.py',
                  '../graficos-animacao/fronteiras_exibicao.py')
    fontes = {n: hashlib.sha256((ambiente_missoes.OWNED/n).read_bytes()).hexdigest() for n in nomes}
    if a.cenario == 'v1':
        e = entradas(a.preenchimento, a.relogio)
        b = BancadaCargaMissaoOriginal(e, segundos=a.segundos_inicio)
        manifesto = e.manifesto()
    else:
        import cenarios_oraculo
        b, e, extra = cenarios_oraculo.bancada(a.cenario, a.preenchimento, a.relogio, segundos=a.segundos_inicio)
        manifesto = dict(e.manifesto(), frame=extra['frame'], display=extra['display'])
    relatorio = dict(schema='rising-lands/missionload-original-capture/1', original_sha256=HASH_ORIGINAL,
                     scenario=a.cenario,
                     translation_executed=False, python_composition=False, m1_accepted=False,
                     mission='MONDE01 (new campaign, mission byte 1)', source_revision=revisao,
                     source_dirty_paths=sujo.splitlines(), source_sha256=fontes,
                     named_inputs=manifesto, limits=dict(startup_seconds=a.segundos_inicio,
                     oracle_seconds=a.segundos_oraculo, instructions_per_segment=b.instrucoes_segmento,
                     segments=b.limite_segmentos, bindings=b.limite_vinculos_total,
                     allocations=b.arena.maximo))
    t0 = time.monotonic()
    fase = 'startup'
    try:
        b.iniciar_relogio()
        b.executar_inicio()
        relatorio['startup'] = dict(seconds=round(time.monotonic()-t0, 3), steps=b.passos,
                                    segments=b.execucoes, count_resumes=b.segmentos_retomados,
                                    bindings=len(b.vinculos_declarados.eventos),
                                    binding_counts=_contar(b.vinculos_declarados.eventos),
                                    events_sha256=_hash_eventos(b.vinculos_declarados.eventos),
                                    skipped_calls=b.eventos_pulados, profile_calls=len(b.perfil.chamadas),
                                    allocations=len(b.arena.ordem))
        vigiado = b.conjunto_vigiado()
        b.vigiar_leituras(vigiado)
        rotinas, extras = b._nao_executados()
        relatorio['watched_unexecuted_writes'] = dict(
            routines=list(rotinas)+(['ProgIteration'] if extras else []),
            ranges=[[hex(x), hex(z)] for x, z in b.intervalos_vigiados],
            sources=[dict(address=hex(k[0]), size=k[1], indexed=k[2], writers=v) for k, v in sorted(vigiado.items())])
        if a.entrada:
            entrada_snap = b.snapshot_entrada()
            entrada_doc = dict(schema='rising-lands/missionload-entry-state/1', original_sha256=HASH_ORIGINAL,
                               scenario=a.cenario, source_revision=revisao, named_inputs=manifesto,
                               summary=b.resumo_imagem(entrada_snap['blocks']),
                               blocks=b.serializar(entrada_snap['blocks']),
                               registers={k: hex(v) for k, v in entrada_snap['registers'].items()},
                               segment_registers={k: hex(v) for k, v in entrada_snap['segments'].items()},
                               **{k: v for k, v in entrada_snap.items()
                                  if k not in ('blocks', 'registers', 'segments')},
                               allocations=b.arena.manifesto(), skipped_startup_calls=b.eventos_pulados,
                               note='Python M1 composition starts from exactly these bytes; the startup '
                                    'emulation is provenance only')
            if hasattr(b, 'estado_exibicao'):
                entrada_doc['display_state'] = b.estado_exibicao()
        pre = b.imagem()
        if a.cenario == 'v1':
            relatorio['inherited_state'] = dict(summary=b.resumo_imagem(pre), blocks=b.serializar(pre),
                                                registers_at_entry={k: hex(v) for k, v in b._registros().items()})
        else:
            # The entry artifact holds every inherited byte; here only per-block hashes.
            relatorio['inherited_state'] = dict(summary=b.resumo_imagem(pre), encoding='hashes_only_see_entry',
                                                block_hashes=_hashes(pre),
                                                registers_at_entry={k: hex(v) for k, v in b._registros().items()})
        fase = 'oracle'
        regs = b.executar_mission_load(a.segundos_oraculo)
        post = b.imagem()
        relatorio['oracle'] = dict(
            entry=hex(MISSION_LOAD), real_return=hex(regs['EIP']), reached_real_return=regs['EIP'] == RETORNO_MISSION_LOAD,
            al=regs['EAX'] & 0xff, registers={k: hex(v) for k, v in regs.items()},
            seconds=round(b.segundos_oraculo, 3), segments=b.execucoes-b.segmentos_inicio_oraculo,
            binding_counts=_contar(b.vinculos_declarados.eventos[b.evento_inicio_oraculo:]),
            binding_events=eventos_json(b.vinculos_declarados.eventos[b.evento_inicio_oraculo:]),
            watched_reads=[dict(address=hex(k[0]), size=k[1], reader=k[2], count=v)
                           for k, v in sorted(b.leituras_vigiadas.items())],
            final_state=(dict(summary=b.resumo_imagem(post), blocks=b.serializar(post)) if a.cenario == 'v1' else
                         dict(summary=b.resumo_imagem(post), encoding='delta_from_entry', block_hashes=_hashes(post),
                              blocks=b.serializar({n: v for n, v in post.items() if pre.get(n) != v}))))
        if hasattr(b, 'estado_exibicao'):
            relatorio['display_state'] = b.estado_exibicao()
            relatorio['directdraw_calls'] = b.chamadas_exibicao()
        relatorio['code_integrity'] = dict(exe_code_sha256=b.sha256_codigo_exe, before=b.sha256_codigo_inicial,
                                           after=b.sha256_codigo(), protection='BEGTEXT R|X; headers/.reloc/.rsrc R; '
                                           'DGROUP/.bss/.idata RW; 0x52e000..0x600000 no access; stack/arena RW no exec')
        resultado = 0
    except (OraculoInterrompido, ParadaVinculoDeclarado, RuntimeError) as erro:
        detalhe = getattr(erro, 'detalhe', None)
        ultimo = b.vinculos_declarados.eventos[-1] if b.vinculos_declarados.eventos else None
        relatorio['stop'] = dict(phase=fase, type=type(erro).__name__, reason=str(erro)[:2000], detail=detalhe,
                                 last_binding=eventos_json([ultimo])[0] if ultimo else None,
                                 registers={k: hex(v) for k, v in b._registros().items()},
                                 stack_scan=b.pilha_provavel(b._registros()['ESP']),
                                 retained_state=b.serializar(b.imagem()))
        relatorio['partial_steps'] = b.passos
        relatorio['skipped_calls'] = b.eventos_pulados
        resultado = 2
    relatorio['media_read'] = sorted(b.midia.lidos.values(), key=lambda x: x['path'])
    relatorio['crt_files'] = b.arquivos.historico
    relatorio['win32_files'] = b.arquivos_win32.historico
    relatorio['profile_calls_sha256'] = hashlib.sha256(repr(b.perfil.chamadas).encode()).hexdigest()
    relatorio['declared_windows_answers'] = [list(x) for x in b.windows.consumidos]
    relatorio['allocations'] = b.arena.manifesto()
    relatorio['import_resolutions'] = b.importacoes_declaradas
    relatorio['total_seconds'] = round(time.monotonic()-t0, 3)
    if resultado:
        saida = ROOT/'.local'/(f'{a.cenario}-missionload-failed-'+time.strftime('%Y%m%dT%H%M%S')+'.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    if not resultado and a.entrada:
        caminho_entrada = ROOT/a.entrada
        with open(caminho_entrada, 'x') as f:
            json.dump(entrada_doc, f, indent=1, sort_keys=True)
            f.write('\n')
        print('entry', caminho_entrada, hashlib.sha256(caminho_entrada.read_bytes()).hexdigest())
    print(json.dumps(dict(output=str(saida), sha256=hashlib.sha256(saida.read_bytes()).hexdigest(),
                          result='real_return' if not resultado else 'stopped',
                          oracle={k: v for k, v in relatorio.get('oracle', {}).items()
                                  if k in ('real_return', 'al', 'seconds', 'segments', 'binding_counts')},
                          watched_reads=len(relatorio.get('oracle', {}).get('watched_reads', [])),
                          stop=relatorio.get('stop', {}).get('reason'),
                          total_seconds=relatorio['total_seconds']), indent=1))
    return resultado


def _hashes(blocos):
    return {n: dict(base=hex(base), bytes=len(d), sha256=hashlib.sha256(d).hexdigest()) for n, (base, d) in blocos.items()}


def _contar(eventos):
    c = {}
    for ev in eventos:
        c[ev['name']] = c.get(ev['name'], 0)+1
    return dict(sorted(c.items()))


def _hash_eventos(eventos):
    return hashlib.sha256(json.dumps(eventos_json(eventos), sort_keys=True).encode()).hexdigest()


if __name__ == '__main__':
    sys.exit(main())
