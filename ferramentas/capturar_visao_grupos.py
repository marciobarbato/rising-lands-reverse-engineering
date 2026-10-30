"""Original-only capture of the structure vision, group, minimap and exit-position routines (M3.1 round 2).

Runs every case of ``casos_visao_grupos`` natively through ``bancada_entrada_estruturas`` (MONDE01 display
reference, frame 1 paused at its first ProcessInputGame entry; the prepared CAVE of STRUCTURE_ENTRY built by
original routines; a few short windows of consecutive calls). No Python translation is
imported. Per measured step it records the entry/exit registers, every non-stack store in order, the changed bytes
of the whole mapped state (stack excluded), the nested routine entries and the frame-boundary events (PlaySnd_*).
The run must reproduce the committed load_tail, between_frames and frame1 state summaries and leave the code
section unchanged.

    python3 -B ferramentas/capturar_visao_grupos.py \
        --saida evidencias/visao-grupos/captura-visao-grupos-exibicao.json.xz
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import time

RAIZ = Path(__file__).resolve().parents[1]
FONTES = ('ferramentas/capturar_visao_grupos.py', 'ferramentas/bancada_entrada_estruturas.py',
          'ferramentas/bancada_selecao_ordens.py', 'ferramentas/casos_visao_grupos.py',
          'ferramentas/casos_entrada_estruturas.py', 'ferramentas/casos_selecao_ordens.py',
          'ferramentas/percurso_quadro1.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')


def chamada_compacta(c):
    """[depth, name, {EAX, EDX, EBX, ECX}, caller, exit EAX] -> 'depth|name|eax,edx,ebx,ecx|caller|exit'."""
    p, nome, r, chamador, saida = c
    return f"{p}|{nome}|{r['EAX']},{r['EDX']},{r['EBX']},{r['ECX']}|{chamador}|{saida}"


def casos_da_bancada(b):
    """The declared matrix, bound to this run's pause (checked against the documented facts)."""
    import casos_visao_grupos as cvg
    return cvg.casos(*cvg.verificar_pausa(lambda a, n: bytes(b.cpu.mem_read(a, n))))


def executar(cenario, observador=None, limite=None, leituras=False, nomes=None, progresso=False):
    """(bench, cases, results, reproduction, pause, seconds) of the declared matrix (first ``limite`` cases, or
    the cases named in ``nomes``)."""
    import bancada_entrada_estruturas as bee

    def escolher(b):
        c = casos_da_bancada(b)
        if nomes is not None:
            c = [x for x in c if x['case'] in nomes]
        return c[:limite]
    return bee.executar(cenario, escolher, observador, leituras=leituras, progresso=progresso)


def abrir(caminho, modo):
    return lzma.open(caminho, modo) if str(caminho).endswith('.xz') else open(caminho, modo)


def main():
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--casos', type=int, help='smoke run: first N cases only (output under .local/ only)')
    ap.add_argument('--nomes', nargs='*', help='smoke run: only these cases (output under .local/ only)')
    a = ap.parse_args()
    if (a.casos is not None or a.nomes) and not a.saida.startswith('.local/'):
        raise SystemExit('A smoke run writes under .local/ only')
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    b, casos, resultados, reproducao, pausa, segundos = executar('exibicao', limite=a.casos,
                                                                 nomes=set(a.nomes) if a.nomes else None,
                                                                 progresso=True)
    for r in resultados:
        r['calls'] = [chamada_compacta(c) for c in r['calls']]
        contagem = {}
        for c in r['calls']:
            nome = c.split('|')[1]
            contagem[nome] = contagem.get(nome, 0) + 1
        r['callee_counts'] = contagem
    alcancados = {}
    for r in resultados:
        alvo = alcancados.setdefault(r['routine'], {})
        for nome, n in r['callee_counts'].items():
            alvo[nome] = alvo.get(nome, 0) + n
    relatorio = dict(
        schema='rising-lands/monde01-vision-groups-capture/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='exibicao',
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        label='leaf calls and short windows at frame 1\'s first ProcessInputGame entry (accepted '
              'MONDE01 display path); a case adds only its native preparation, declared writes and argument registers',
        pause=pausa, path_reproduction=reproducao, declared_cases=len(casos),
        preparations={c['case']: c.get('_preparation_record', []) for c in casos if c.get('preparation')},
        cases=resultados, callees_reached=alcancados,
        encoding=dict(calls="'depth|name|EAX,EDX,EBX,ECX at entry|caller|EAX at return' (depth 0 = direct callee)",
                      stores='[routine, eip, address, width, value] in execution order (native stack excluded)',
                      changed_bytes='[address, old, new] over DGROUP+.bss, CRT thread page, active allocations',
                      names="'case' for a single measured call, 'case/step.repetition' inside a window"),
        seconds=round(time.monotonic() - t0, 3), pause_seconds=segundos)
    ok = all(reproducao.values()) and all(r['reached_return'] for r in resultados) and resultados
    if not ok:
        saida = RAIZ / '.local/visao-grupos' / ('captura-falha-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with abrir(saida, 'xt') as f:
        json.dump(relatorio, f, indent=None, sort_keys=True, separators=(',', ':'))
        f.write('\n')
    print(json.dumps(dict(output=str(saida), reproduction=reproducao, declared_cases=len(casos),
                          measured=len(resultados), returned=sum(r['reached_return'] for r in resultados),
                          boundaries=sum(len(r['boundaries']) for r in resultados),
                          callees_reached={k: sorted(v) for k, v in alcancados.items()},
                          seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida)


if __name__ == '__main__':
    main()
