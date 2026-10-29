"""Original-only capture of M3.1 round 2: state 11 and the construction-progress branch, the state-13 dispatch,
ProcessInputGame tags 0xb/0xc/0x10/0x21, WndProc key messages and InputGame's group-number/GoLastAttaque keys.

Runs every case of ``casos_construcao_teclas_ia`` natively through Core's ``bancada_selecao_ordens`` (the same
frame-1 ProcessInputGame pause and recording as ``capturar_entrada_ordens_ia``; its ``Teclas`` binding answers
each case's declared GetAsyncKeyState list). No Python translation is imported. The run must reproduce the
committed load_tail/between_frames/frame1 summaries and leave the code section unchanged.

    python3 -B pesquisas-paralelas/ia-runtime/capturar_construcao_teclas_ia.py \\
        --saida pesquisas-paralelas/ia-runtime/evidencias/captura-construcao-teclas-ia.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import time

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))
from ambiente_ia_runtime import ROOT  # noqa: E402

MISSOES = ROOT / 'pesquisas-paralelas/missoes'
if str(MISSOES) not in sys.path:
    sys.path.insert(0, str(MISSOES))
FONTES = ('pesquisas-paralelas/ia-runtime/capturar_construcao_teclas_ia.py',
          'pesquisas-paralelas/ia-runtime/casos_construcao_teclas_ia.py',
          'pesquisas-paralelas/ia-runtime/casos_entrada_ordens_ia.py',
          'pesquisas-paralelas/ia-runtime/capturar_entrada_ordens_ia.py', 'ferramentas/bancada_selecao_ordens.py',
          'ferramentas/percurso_quadro1.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')
CAPTURA = AQUI / 'evidencias/captura-construcao-teclas-ia.json'


def casos_da_bancada(b):
    """The declared matrix bound to this run (pause pointers checked; type limits read at the pause)."""
    import casos_construcao_teclas_ia as cc
    import casos_entrada_ordens_ia as ce
    ler = lambda a, n: bytes(b.cpu.mem_read(a, n))  # noqa: E731
    for endereco, esperado, nome in ((0x4e19a0, ce.UNIDADES, 'unit pool'), (0x4e2458, ce.PACOTE, 'player-0 packet')):
        valor = struct.unpack('<I', ler(endereco, 4))[0]
        if valor != esperado:
            raise RuntimeError(f'{nome} at 0x{valor:08x}, not the documented 0x{esperado:08x}')
    if ler(cc.ESTRUTURAS + cc.PASSO + 5, 1) != b'\0':
        raise RuntimeError('structure record 1 is not free at the pause')
    return cc.casos(cc.limites_da_memoria(ler))


def executar(observador=None, limite=None, leituras=False):
    import bancada_selecao_ordens as bso
    from capturar_entrada_ordens_ia import Teclas
    teclas = Teclas()

    def observar(caso, antes, resultado):
        resultado['declared_keys_consumed'] = teclas.depois(caso)
        if observador is not None:
            observador(caso, antes, resultado)
    return bso.executar('exibicao', lambda b: teclas.preparar(b, casos_da_bancada(b)[:limite]), observar,
                        leituras=leituras)


def main():
    from capturar_entrada_ordens_ia import chamada_compacta
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--casos', type=int, help='smoke run: first N cases only (output under .local/ only)')
    a = ap.parse_args()
    if a.casos is not None and not a.saida.startswith('.local/'):
        raise SystemExit('A --casos smoke run writes under .local/ only')
    saida = ROOT / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {saida}')
    revisao = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    b, casos, resultados, reproducao, pausa, segundos = executar(limite=a.casos)
    alcancados = {}
    for r in resultados:
        r['calls'] = [chamada_compacta(c) for c in r['calls']]
        alvo = alcancados.setdefault(r['routine'], {})
        for c in r['calls']:
            nome = c.split('|')[1]
            alvo[nome] = alvo.get(nome, 0) + 1
    import casos_construcao_teclas_ia as cc
    relatorio = dict(
        schema='rising-lands/monde01-construction-keys-capture/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='exibicao',
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FONTES},
        label='leaf calls at frame 1\'s first ProcessInputGame entry (accepted MONDE01 display path); each case '
              'adds only its declared writes, argument registers, pushed words and GetAsyncKeyState answers',
        structure_limits={hex(t): v for t, v in cc.limites_da_memoria(lambda x, n: bytes(b.cpu.mem_read(x, n))).items()},
        pause=pausa, path_reproduction=reproducao, cases=resultados, callees_reached=alcancados,
        encoding=dict(calls="'depth|name|EAX,EDX,EBX,ECX at entry|caller|EAX at return' (depth 0 = direct callee)",
                      stores='[routine, eip, address, width, value] in execution order (native stack excluded)',
                      changed_bytes='[address, old, new] over DGROUP+.bss, CRT thread page, active allocations',
                      declared_keys_consumed='[return site, vkey, answer] per GetAsyncKeyState call answered from '
                                             'the case\'s declared list'),
        seconds=round(time.monotonic() - t0, 3), pause_seconds=segundos)
    ok = (all(reproducao.values()) and len(resultados) == len(casos) and
          all(r['reached_return'] for r in resultados))
    if not ok:
        saida = ROOT / '.local/entrada' / ('captura-construcao-falha-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=None, sort_keys=True, separators=(',', ':'))
        f.write('\n')
    print(json.dumps(dict(output=str(saida), reproduction=reproducao, cases=len(resultados),
                          returned=sum(r['reached_return'] for r in resultados),
                          not_returned=[r['case'] for r in resultados if not r['reached_return']],
                          boundaries=sum(len(r['boundaries']) for r in resultados),
                          callees_reached={k: sorted(v) for k, v in alcancados.items()},
                          seconds=relatorio['seconds']), indent=1))
    encerrar_captura(0 if ok else 2, saida)


if __name__ == '__main__':
    main()
