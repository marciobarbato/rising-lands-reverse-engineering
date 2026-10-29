"""Coverage-only long run of the MONDE01 display reference (output is NOT evidence).

The long-run form of ``levantar_quadros_exibicao`` (the 0..128 survey, f426e30)
for M2.3 planning: it says which original routines frames 129..9,200 reach.
It builds Missions' display bench (scenario 'exibicao': startup, MissionLoad),
checks frames 0/1 against the v2 frame capture's state summaries, then keeps
running the real loop (between_frames, frame) with the declared no-input
answers until the cycle counter u32 0x508f7c reaches ``--ate``.

Lightest hooks: Missions' per-block entry trace (which reads the stack on each
symbol entry) is turned off (``rastrear=False``). One UC_HOOK_BLOCK over the code
section counts every original symbol entry inside each executed block: calls,
jumps back to a routine's first instruction, and fall-through entries. There
are no read/write hooks. Declared boundaries (bound I/O, skips and the frame
boundaries) are counted when their address block runs, and are also listed as
``declared_boundaries``. (One UC_HOOK_CODE per entry, 1,952 of them, was
measured about four times slower per frame.)

Inputs: the display reference's named inputs. Its declared display clock
(0x123456 + 40*k, one answer per call, k = 1..4096) is extended by the same
rule to k = 1..``--ticks``, so a long run does not stop on the clock budget.
Frames 0/1 consume the same first answers, so their states are unchanged.

Outputs:
* ``SAIDA.frames.jsonl``: one line per frame, flushed every frame and fsynced
  every ``--checkpoint`` frames. Each line holds:
  - the counter, game frame, world RNG 0x497164, AI RNG 0x498db4, CRT seed,
    permutation cursor 0x4e1d18 and view origin;
  - the DGROUP SHA-256 (every frame) and the whole-state SHA-256 (every
    ``--hash-cada`` frames);
  - the routines entered for the first time, the raid-marker entries, the
    boundary events and the display ticks consumed.
* ``SAIDA``: a summary (each routine's first/last entry frame and total
  entries, first raid-marker frame, status). It is rewritten atomically at
  every checkpoint and at the end.

A stop of the original (declared-boundary stop, time limit, fault) is recorded
in the summary with its traceback, and the tool exits with status 2. The
process ends with ``encerramento_captura.encerrar_captura`` (fsync, os._exit).

    python3 -B ferramentas/cobrir_quadros_exibicao.py --ate 9200 \
        --saida relatorios/cobertura-quadros-exibicao-9200.json
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time
import traceback

RAIZ = Path(__file__).resolve().parents[1]
CODIGO = (0x401000, 0x493c00)
CONTADOR = 0x508f7c
# Routine entries that mark a raid or combat beginning (Combat/AI owners), as in the 0..128 survey.
ATAQUE = ('SetAttaqueEngin', 'EnginTrouveCible', 'iagWarNoyau', 'ConstruitGroupeMonstre', 'EnginAttaque',
          'CalculAttaque', 'ProjectileNew', 'EnginBlesse', 'BatimentBlesse')


def _fsync(caminho):
    fd = os.open(caminho, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def escrever_atomico(caminho, dados):
    """Write JSON to ``caminho`` via a fsynced temporary file and rename."""
    tmp = caminho.with_name(caminho.name + '.tmp')
    with open(tmp, 'w') as f:
        json.dump(dados, f, indent=1, sort_keys=True)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, caminho)
    _fsync(caminho.parent)


class ContadorEntradas:
    """One UC_HOOK_BLOCK over the code section counting every original symbol entry inside each executed block.

    A block that starts at an entry, or runs through one by falling into it, counts that entry once; a block
    holds no branch before its end, so each count is one execution of the routine's first instruction.
    """
    def __init__(self, bancada):
        import unicorn
        from bisect import bisect_left
        self.nomes = {a: n for a, n in bancada.nomes.items() if CODIGO[0] <= a < CODIGO[1]}
        self.fronteiras = sorted(bancada.nomes[a] for a in (set(bancada.vinculos_declarados.vinculos) |
                                                            set(bancada.fronteiras) | set(bancada.pulos))
                                 if a in self.nomes)
        self.quadro = {}
        entradas, quadro, n = sorted(self.nomes), self.quadro, len(self.nomes)

        def bloco(cpu, endereco, tamanho, _):
            i = bisect_left(entradas, endereco)
            fim = endereco + tamanho
            while i < n and entradas[i] < fim:
                a = entradas[i]
                quadro[a] = quadro.get(a, 0) + 1
                i += 1
        self._bloco = bloco
        bancada.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=CODIGO[0], end=CODIGO[1] - 1)
        # Hooks are instrumented at translation time: flush blocks cached during startup/MissionLoad.
        bancada.cpu.ctl_flush_tb()

    def drenar(self):
        d = {self.nomes[a]: k for a, k in self.quadro.items()}
        self.quadro.clear()
        return d


def amostra(b, completo):
    u32 = lambda a: struct.unpack('<I', b.cpu.mem_read(a, 4))[0]
    u16 = lambda a: struct.unpack('<H', b.cpu.mem_read(a, 2))[0]
    from oraculo_carga_missao import DGROUP
    r = dict(counter=u32(CONTADOR), game_frame=u32(0x496d40), world_rng=hex(u32(0x497164)),
             ai_rng=hex(u32(0x498db4)), crt_seed=hex(u32(u32(0x522244) + 0xc)),
             cursor=b.cpu.mem_read(0x4e1d18, 1)[0], view_origin=[u16(0x508720), u16(0x508722)],
             dgroup_sha256=hashlib.sha256(bytes(b.cpu.mem_read(DGROUP[0], DGROUP[1] - DGROUP[0]))).hexdigest())
    if completo:
        r['state'] = b.resumo_imagem(b.imagem())['sha256']
    return r


def main():
    import percurso_quadro1  # noqa: F401  (puts Missions on sys.path)
    import cenarios_oraculo
    from oraculo_exibicao_missao import BancadaExibicaoOriginal
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ate', type=int, required=True, help='stop at the frame whose counter 0x508f7c reaches this')
    ap.add_argument('--max-quadros', type=int, help='safety bound on frames run (default: ate + 100)')
    ap.add_argument('--ticks', type=int, default=200000, help='declared display clock answers k = 1..TICKS')
    ap.add_argument('--hash-cada', type=int, default=1, help='whole-state SHA-256 every N frames')
    ap.add_argument('--checkpoint', type=int, default=100, help='fsync and rewrite the summary every N frames')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    linhas = saida.with_name(saida.name.removesuffix('.json') + '.frames.jsonl')
    for p in (saida, linhas):
        if p.exists():
            raise SystemExit(f'Refusing to overwrite {p}')
    saida.parent.mkdir(parents=True, exist_ok=True)
    if a.ticks < len(cenarios_oraculo.TICKS_EXIBICAO):
        raise SystemExit('--ticks must extend, not shorten, the declared display clock')
    maximo = a.max_quadros or a.ate + 100
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    t0 = time.monotonic()
    caminho_cap = cenarios_oraculo.caminho('exibicao', 'captura_quadro')
    cap = json.loads(caminho_cap.read_bytes())
    ni = cap['named_inputs']['m1']
    ticks = tuple(0x123456 + 40 * k for k in range(1, a.ticks + 1))
    if ticks[:len(cenarios_oraculo.TICKS_EXIBICAO)] != cenarios_oraculo.TICKS_EXIBICAO:
        raise SystemExit('Display clock rule differs from cenarios_oraculo.TICKS_EXIBICAO')
    entradas = cenarios_oraculo.entradas_exibicao(ni['allocation_fill'], ni['clock_ms'][0], ticks=ticks)
    b = BancadaExibicaoOriginal(entradas, segundos=300, rastrear=False)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    contador = ContadorEntradas(b)
    resumo = dict(
        schema='rising-lands/monde01-display-frames-coverage/1', evidence=False, original_sha256=HASH_ORIGINAL,
        translation_executed=False, source_revision=revisao, scenario='exibicao',
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest()
                       for p in ('ferramentas/cobrir_quadros_exibicao.py',
                                 'pesquisas-paralelas/missoes/oraculo_exibicao_missao.py',
                                 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py')},
        reference=dict(path=str(caminho_cap.relative_to(RAIZ)), sha256=hashlib.sha256(caminho_cap.read_bytes()).hexdigest()),
        inputs='display-reference named inputs; every later frame keeps the declared no-input answers '
               '(GetAsyncKeyState 0, PeekMessageA no message, GetCursorPos (0,0)); display clock '
               f'0x123456+40*k for k=1..{a.ticks} (the reference rule, extended)',
        hooks=f'one UC_HOOK_BLOCK over 0x401000..0x493c00 counting each of {len(contador.nomes)} original '
              'symbol entries inside every executed block; Missions block trace off; no read/write hooks',
        declared_boundaries=contador.fronteiras,
        frames_file=linhas.name, stop_counter=a.ate, max_frames=maximo, hash_every=a.hash_cada,
        raid_markers=list(ATAQUE), status='running')
    rotinas, marcadores = {}, {}
    tick0 = len(b.windows.ticks)
    referencia = {p['phase']: p['state_after']['summary'] for p in cap['phases']}
    reproducao, estado = {}, None
    f = open(linhas, 'x')

    def registrar(k, completo):
        nonlocal tick0
        entradas_q = contador.drenar()
        novos = sorted(n for n in entradas_q if n not in rotinas)
        for n, c in entradas_q.items():
            r = rotinas.setdefault(n, dict(first_frame=k, last_frame=k, entries=0))
            r['last_frame'], r['entries'] = k, r['entries'] + c
        for n in ATAQUE:
            if n in entradas_q:
                marcadores.setdefault(n, k)
        fronteiras = {}
        for e in b.eventos_fronteira[registrar.eventos:]:
            fronteiras[e['routine']] = fronteiras.get(e['routine'], 0) + 1
        registrar.eventos = len(b.eventos_fronteira)
        linha = dict(frame=k, seconds=round(time.monotonic() - registrar.t, 3), new_routines=novos,
                     raid_entries={n: entradas_q[n] for n in ATAQUE if n in entradas_q},
                     boundaries=fronteiras, routines_entered=len(entradas_q), **amostra(b, completo))
        linha['display_ticks'] = tick0 - len(b.windows.ticks)
        tick0 = len(b.windows.ticks)
        registrar.t = time.monotonic()
        f.write(json.dumps(linha, sort_keys=True) + '\n')
        f.flush()
        return linha

    registrar.eventos, registrar.t = len(b.eventos_fronteira), time.monotonic()

    def checkpoint(status, **extra):
        f.flush()
        os.fsync(f.fileno())
        resumo.update(status=status, routines=dict(sorted(rotinas.items())),
                      first_raid_marker_frames=marcadores, seconds=round(time.monotonic() - t0, 3), **extra)
        escrever_atomico(saida, resumo)

    k, codigo = 0, 0
    try:
        for nome, correr in (('load_tail', lambda: b.executar_cauda_carga(600)),
                             ('between_frames', lambda: b.executar_entre_quadros(300)),
                             ('frame1', lambda: b.executar_quadro(600))):
            correr()
            reproducao[nome] = b.resumo_imagem(b.imagem()) == referencia[nome]
            if nome != 'between_frames':
                registrar(k, True)
                k += 1
        resumo['reproduction_frames_0_1'] = reproducao
        if not all(reproducao.values()):
            raise RuntimeError(f'Frames 0/1 do not reproduce the display reference: {reproducao}')
        while True:
            b.executar_entre_quadros(300)
            b.executar_quadro(600)
            estado = registrar(k, k % a.hash_cada == 0)
            if k % a.checkpoint == 0:
                checkpoint('running', frames_run=k, last=estado)
            if estado['counter'] >= a.ate:
                break
            if k >= maximo:
                raise RuntimeError(f'Frame bound {maximo} reached at counter {estado["counter"]}')
            k += 1
        checkpoint('completed', frames_run=k, last=estado, code_unchanged=b.sha256_codigo() == cap['code_integrity']['after'])
    except Exception as erro:
        codigo = 2
        checkpoint('stopped', frames_run=k, last=estado, stop=dict(frame=k, error=repr(erro),
                                                                   traceback=traceback.format_exc()))
    f.close()
    print(json.dumps(dict(output=str(saida), status=resumo['status'], frames=k, routines=len(rotinas),
                          first_raid_marker_frames=marcadores, seconds=resumo['seconds']), indent=1))
    encerrar_captura(codigo, saida, linhas)


if __name__ == '__main__':
    main()
