"""Original-only capture of the economy order setters and construction gates (M3 groundwork).

Runs every case of ``casos_ordens_economia`` natively through ``bancada_ordens_economia``
(Core's selection-orders pause: MONDE01 display reference, frame 1 paused at its first
ProcessInputGame entry). No Python translation is imported. Per case it records the entry/exit
registers, every non-stack store in order (with the nested call it happened in), the changed
bytes of the whole mapped state (stack excluded), every nested routine entry with its exit
registers and the frame-boundary events (PlaySnd_*). The run must reproduce the committed
load_tail, between_frames and frame1 summaries and leave the code section unchanged.

    python3 -B pesquisas-paralelas/economia/capturar_ordens_economia.py \
        --saida pesquisas-paralelas/economia/evidencias/ordens-economia/captura-ordens-economia-exibicao.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
FONTES = ('pesquisas-paralelas/economia/capturar_ordens_economia.py',
          'pesquisas-paralelas/economia/bancada_ordens_economia.py',
          'pesquisas-paralelas/economia/casos_ordens_economia.py',
          'ferramentas/bancada_selecao_ordens.py', 'ferramentas/casos_selecao_ordens.py',
          'ferramentas/percurso_quadro1.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')
REGS7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')


def chamada_compacta(c):
    """[depth, name, {EAX, EDX, EBX, ECX}, caller, exit EAX, {exit EAX..EBP}] ->
    'depth|name|eax,edx,ebx,ecx|caller|exit EAX|exit EAX,EBX,ECX,EDX,ESI,EDI,EBP'."""
    p, nome, r, chamador, saida = c[:5]
    fim = ','.join(c[5][k] for k in REGS7) if len(c) > 5 else ''
    return f"{p}|{nome}|{r['EAX']},{r['EDX']},{r['EBX']},{r['ECX']}|{chamador}|{saida}|{fim}"


def casos_da_bancada(b):
    """The declared matrix, bound to this run's pointers after checking the documented pause facts."""
    import casos_ordens_economia as coe
    grade = coe.verificar_pausa(lambda a, n: bytes(b.cpu.mem_read(a, n)))
    return coe.casos(grade)


def executar(cenario, observador=None, limite=None, leituras=False):
    """(bench, cases, results, reproduction, pause, seconds) of the declared matrix (first ``limite`` cases)."""
    import bancada_ordens_economia as boe
    return boe.executar(cenario, lambda b: casos_da_bancada(b)[:limite], observador, leituras=leituras)


def compactar(resultados):
    for r in resultados:
        r['calls'] = [chamada_compacta(c) for c in r['calls']]
        contagem = {}
        for c in r['calls']:
            nome = c.split('|')[1]
            contagem[nome] = contagem.get(nome, 0) + 1
        r['callee_counts'] = contagem
    return resultados


def main():
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--cenario', choices=('exibicao',), default='exibicao')
    ap.add_argument('--saida', required=True)
    ap.add_argument('--casos', type=int, help='smoke run: first N cases only (output under .local/ only)')
    a = ap.parse_args()
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    b, casos, resultados, reproducao, pausa, segundos = executar(a.cenario, limite=a.casos)
    compactar(resultados)
    alcancados = {}
    for r in resultados:
        alvo = alcancados.setdefault(r['routine'], {})
        for nome, n in r['callee_counts'].items():
            alvo[nome] = alvo.get(nome, 0) + n
    relatorio = dict(
        schema='rising-lands/monde01-economy-orders-capture/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario=a.cenario,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        label='economy leaf calls at frame 1\'s first ProcessInputGame entry (Core\'s accepted pause on the '
              'MONDE01 display path); each case adds only its declared writes and argument registers',
        pause=pausa, path_reproduction=reproducao, cases=resultados, callees_reached=alcancados,
        encoding=dict(calls="'depth|name|EAX,EDX,EBX,ECX at entry|caller|EAX at return|EAX,EBX,ECX,EDX,ESI,EDI,"
                            "EBP at return' (depth 0 = direct callee)",
                      stores='[routine, eip, address, width, value, index of the innermost open nested call or -1] '
                             'in execution order (native stack excluded)',
                      changed_bytes='[address, old, new] over DGROUP+.bss, CRT thread page, active allocations'),
        seconds=round(time.monotonic() - t0, 3), pause_seconds=segundos)
    ok = (all(reproducao.values()) and len(resultados) == len(casos) and
          all(r['reached_return'] for r in resultados))
    if not ok:
        saida = RAIZ / '.local/ordens-economia' / ('captura-falha-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=None, sort_keys=True, separators=(',', ':'))
        f.write('\n')
    print(json.dumps(dict(output=str(saida), reproduction=reproducao, cases=len(resultados),
                          returned=sum(r['reached_return'] for r in resultados),
                          boundaries=sum(len(r['boundaries']) for r in resultados),
                          callees_reached={k: sorted(v) for k, v in alcancados.items()},
                          seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida)


if __name__ == '__main__':
    main()
