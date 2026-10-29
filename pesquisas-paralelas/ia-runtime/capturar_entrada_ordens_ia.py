"""Original-only capture of the M3.1 input path: InputGame, SetPlayerOrdre, ProcessInputGame and their leaves.

Runs every case of ``casos_entrada_ordens_ia`` natively through Core's ``bancada_selecao_ordens`` (MONDE01
display reference, frame 1 paused at its first ProcessInputGame entry; the same bench and pause as Core's
selection/order capture). No Python translation is imported. Per case it records the entry/exit registers,
every non-stack store in order, the changed bytes of the whole mapped state (stack excluded), the nested
routine entries, the frame-boundary events (PlaySnd_*) and the declared GetAsyncKeyState answers consumed.
The run must reproduce the committed load_tail, between_frames and frame1 state summaries and leave the code
section unchanged.

Declared key answers: before each case the bench's Windows binding receives the case's ordered ``keys``
[(vkey, result)]; a case with none answers 0 to every call (the frame phases' no-input answer). Every declared
answer must be consumed by its own case.

Allocation bookkeeping: InitInputPlayer allocates five packets through MemAlloc (GlobalAlloc on the bench
arena). The bench restores every memory block after a case but not its Python arena allocator, so the arena's
next pointer and records are saved before that case and put back after it; otherwise the resumed frame 1 would
allocate at other addresses and its committed summary would not reproduce.

    python3 -B pesquisas-paralelas/ia-runtime/capturar_entrada_ordens_ia.py \\
        --saida pesquisas-paralelas/ia-runtime/evidencias/captura-entrada-ordens-ia.json
"""
import argparse
import copy
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
FONTES = ('pesquisas-paralelas/ia-runtime/capturar_entrada_ordens_ia.py',
          'pesquisas-paralelas/ia-runtime/casos_entrada_ordens_ia.py', 'ferramentas/bancada_selecao_ordens.py',
          'ferramentas/percurso_quadro1.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')
CAPTURA = AQUI / 'evidencias/captura-entrada-ordens-ia.json'


def chamada_compacta(c):
    """[depth, name, {EAX, EDX, EBX, ECX}, caller, exit EAX] -> 'depth|name|eax,edx,ebx,ecx|caller|exit'."""
    p, nome, r, chamador, saida = c
    return f"{p}|{nome}|{r['EAX']},{r['EDX']},{r['EBX']},{r['ECX']}|{chamador}|{saida}"


def _u32(b, endereco):
    return struct.unpack('<I', bytes(b.cpu.mem_read(endereco, 4)))[0]


def casos_da_bancada(b):
    """The declared matrix, bound to this run's grids (pointers checked against the documented pause state)."""
    import casos_entrada_ordens_ia as ce
    for endereco, esperado, nome in ((0x4e19a0, ce.UNIDADES, 'unit pool'), (0x4e2458, ce.PACOTE, 'player-0 packet')):
        if _u32(b, endereco) != esperado:
            raise RuntimeError(f'{nome} at 0x{_u32(b, endereco):08x}, not the documented 0x{esperado:08x}')
    grades = dict(descoberta=_u32(b, ce.DESCOBERTA_0), iluminacao=_u32(b, ce.ILUMINACAO_0),
                  objetos=_u32(b, ce.OBJETOS))
    return ce.casos(grades)


class Teclas:
    """Installs each case's declared GetAsyncKeyState answers on the bench's Windows binding, in case order, and
    saves/restores the bench arena allocator around a case that allocates (InitInputPlayer)."""

    def __init__(self):
        self.b, self.casos, self.i, self.consumo, self.arena = None, [], 0, [], None

    def preparar(self, b, casos):
        self.b, self.casos, self.i = b, casos, 0
        self._instalar()
        return casos

    def _instalar(self):
        w = self.b.windows
        w.teclas = [tuple(k) for k in self.casos[self.i]['keys']] if self.i < len(self.casos) else []
        self.inicio = len(w.consumidos)
        if self.i < len(self.casos) and self.casos[self.i]['routine'] == 'InitInputPlayer':
            a = self.b.arena
            self.arena = (a.proximo, copy.deepcopy(a.recursos), list(a.ordem))

    def depois(self, caso):
        w = self.b.windows
        consumidas = [list(e[1:4]) for e in w.consumidos[self.inicio:] if e[0] == 'key' and len(e) == 4]
        if w.teclas:
            raise RuntimeError(f'{caso["case"]}: declared key answers left unconsumed: {w.teclas}')
        self.consumo.append(consumidas)
        if self.arena is not None:
            a = self.b.arena
            a.proximo, a.recursos, a.ordem = self.arena[0], self.arena[1], self.arena[2]
            self.arena = None
        self.i += 1
        self._instalar()
        return consumidas


def executar(observador=None, limite=None, leituras=False):
    """(bench, cases, results, reproduction, pause, seconds, key answers) of the declared matrix."""
    import bancada_selecao_ordens as bso
    teclas = Teclas()

    def observar(caso, antes, resultado):
        resultado['declared_keys_consumed'] = teclas.depois(caso)
        if observador is not None:
            observador(caso, antes, resultado)
    saida = bso.executar('exibicao', lambda b: teclas.preparar(b, casos_da_bancada(b)[:limite]), observar,
                         leituras=leituras)
    return saida


def main():
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
    relatorio = dict(
        schema='rising-lands/monde01-input-orders-capture/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='exibicao',
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FONTES},
        label='leaf calls at frame 1\'s first ProcessInputGame entry (accepted MONDE01 display path); each case '
              'adds only its declared writes, argument registers, pushed words and GetAsyncKeyState answers',
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
        saida = ROOT / '.local/entrada' / ('captura-falha-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
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
