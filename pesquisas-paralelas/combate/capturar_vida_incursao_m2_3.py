"""Original-only capture of the MONDE01 raid unit's first frames (M2.3, counters 9000..9000+N-1).

Forced input: Missions' committed v1 path (startup, MissionLoad, load_tail,
between_frames) is rerun with their read-only bench; at frame 1's CalculGame
entry u32 0x508f7c is written to 9000, and whole frames then run natively with
the real ProgIteration tail and window loop between them, so frame k runs
with counter 8999+k.  Every other byte is the original's own state; the
frame-1 caller frame and the no-input answers are Missions' declarations.

Combat entries are paused with Missions' ``Isolamento``: each call runs
natively in isolation from its exact saved entry state, the state is
restored, and the frame resumes.  An observer stores the inputs the Python
entries need; a block hook records every routine entry inside the isolated
calls (routine, caller, EAX EDX EBX ECX).  After every frame the raid unit's
276-byte record, the projectile pool hash and the boundary events are kept.
No Python translation is imported.

    python3 -B pesquisas-paralelas/combate/capturar_vida_incursao_m2_3.py [--quadros 101]
"""
import argparse
import hashlib
import json
import struct
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
sys.path.insert(0, str(REPO / 'pesquisas-paralelas/missoes'))
import ambiente_missoes  # noqa: E402,F401  (Missions bootstrap: ferramentas, inputs)
import capturar_quadro_missao_original as cq  # noqa: E402
from oraculo_quadro_missao import Isolamento  # noqa: E402
import unicorn  # noqa: E402
from unicorn import x86_const as x86  # noqa: E402

from capturar_isolados_combate_quadro1 import (CAPTURA, CONTADOR, HASH, POOL, UNIDADES, empacotar,  # noqa: E402
                                               entradas_python, u32)
from sondar_vida_incursao import BancadaVida  # noqa: E402

DESTINO = AQUI / 'evidencias/captura-vida-incursao-m2-3-original.json'
CONTADOR_FORCADO, UNIDADE, UNIDADE_INCURSAO = 9000, 0x114, 16
ROTINAS = ('PlayerAttaqueReset', 'ProjectileCalcul', 'EnginTrouveCible', 'PlayerEstAllie',
           'PlayerAttaqueCalculSympa')


def executar(n):
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaVida(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    simbolos = {b.sym[s]: s for s in b.sym}
    entradas_caso, observadas = [], []

    def bloco(cpu, endereco, _tamanho, _):
        if b.fase != 'isolated' or endereco not in simbolos:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        retorno = struct.unpack('<I', bytes(cpu.mem_read(esp, 4)))[0]
        regs = [cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in ('EAX', 'EDX', 'EBX', 'ECX')]
        entradas_caso.append([simbolos[endereco], b.nome(retorno), *(f'{v:x}' for v in regs)])

    b.cpu.hook_add(unicorn.UC_HOOK_BLOCK, bloco, begin=0x401000, end=0x493bff)
    b.cpu.ctl_flush_tb()

    def observador(rotina, fase, caso, antes, resultado):
        observadas.append(dict(routine=rotina, phase=fase, entries=list(entradas_caso),
                               inputs=entradas_python(rotina, antes)))
        entradas_caso.clear()

    iso = Isolamento(b, ROTINAS, None, observador)
    iso.instalar()

    def unidade():
        return bytes(b.cpu.mem_read(u32(b.imagem(), UNIDADES) + UNIDADE * UNIDADE_INCURSAO, UNIDADE))

    b.executar_cauda_carga(600)
    b.executar_entre_quadros(120)
    if u32(b.imagem(), CONTADOR) != 1:
        raise RuntimeError('Frame 1 must enter CalculGame with counter 1 before the forced write')
    b.cpu.mem_write(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))
    quadros, eventos = [], len(b.eventos_fronteira)
    for k in range(1, n + 1):
        if k > 1:
            b.executar_entre_quadros_k(120, k)
        contador = u32(b.imagem(), CONTADOR)
        b.executar_quadro(300, k)
        imagem = b.imagem()
        quadros.append(dict(frame=k, counter=contador, raid_unit=unidade().hex(),
                            pool_sha256=hashlib.sha256(bytes(b.cpu.mem_read(u32(imagem, POOL), 5600))).hexdigest(),
                            boundaries=[e['routine'] for e in b.eventos_fronteira[eventos:]]))
        eventos = len(b.eventos_fronteira)
    if len(observadas) != len(iso.registros):
        raise RuntimeError('Observer and isolated call records disagree')
    for registro, obs in zip(iso.registros, observadas):
        if (registro['routine'], registro['phase']) != (obs['routine'], obs['phase']):
            raise RuntimeError('Observer order differs from isolated call order')
        registro['python_inputs'] = obs['inputs']
        registro['cases'][0]['entries'] = obs['entries']
    return b, iso, quadros


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=101)
    args = ap.parse_args()
    if DESTINO.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {DESTINO}')
    t0 = time.monotonic()
    b, iso, quadros = executar(args.quadros)
    relatorio = dict(
        schema='rising-lands/monde01-raid-life-forced-capture/1', original_sha256=HASH,
        label=f'forced input: v1 path, u32 0x508f7c = {CONTADOR_FORCADO} at frame 1\'s CalculGame entry, '
              f'{args.quadros} whole native frames', translation_executed=False,
        frame_capture=dict(path=str(CAPTURA.relative_to(REPO)),
                           sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={s: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for s, p in (
            ('capturar_vida_incursao_m2_3.py', 'pesquisas-paralelas/combate/capturar_vida_incursao_m2_3.py'),
            ('sondar_vida_incursao.py', 'pesquisas-paralelas/combate/sondar_vida_incursao.py'),
            ('oraculo_quadro_missao.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py'))},
        routines=list(ROTINAS), frames=quadros, calls=iso.registros, code_unchanged_sha256=b.sha256_codigo(),
        entry_format='routine, caller, EAX, EDX, EBX, ECX (hex) of every routine entry inside the isolated call',
        method=('Missions Isolamento: native call from the exact saved entry state to its stack return with '
                'local read/write hooks, state restored afterwards; python_inputs are read from that saved '
                'entry state. Nested entries of listed routines inside an isolated call run natively; the '
                'resumed frame isolates them separately.'),
        seconds=round(time.monotonic() - t0, 3))
    ok = all(c['reached_return'] for r in iso.registros for c in r['cases']) and len(quadros) == args.quadros
    saida = DESTINO if ok else REPO / '.local' / ('combat-raid-life-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    contagem = {}
    for r in iso.registros:
        contagem[r['routine']] = contagem.get(r['routine'], 0) + 1
    print(json.dumps(dict(output=str(saida.relative_to(REPO)), calls=contagem, frames=len(quadros),
                          seconds=relatorio['seconds'])), flush=True)
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
