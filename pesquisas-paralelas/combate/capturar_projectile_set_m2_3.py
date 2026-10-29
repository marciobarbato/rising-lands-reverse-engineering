"""Original-only isolated ProjectileSet 0x46e208 at MONDE01's raid spawn (forced counter 9000).

Same forced input as `capturar_vida_incursao_m2_3.py` (Missions' v1 path, u32
0x508f7c = 9000 written at frame 1's CalculGame entry), run for that one
frame.  Missions' ``Isolamento`` pauses at ProjectileSet's entry inside
ConstruitGroupeMonstre -> ProjectileInit and runs it natively from the exact
saved state twice: the captured inputs (type 0x20, Random even) and a register
perturbation with DL = 0x1f (the odd-Random spawn effect, the only other value
ConstruitGroupeMonstre passes).  The observer keeps the entry pool and the six
stack argument words.  No Python translation is imported.

    python3 -B pesquisas-paralelas/combate/capturar_projectile_set_m2_3.py
"""
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

from capturar_isolados_combate_quadro1 import CAPTURA, CONTADOR, HASH, POOL, empacotar, ler, u32  # noqa: E402
from sondar_vida_incursao import BancadaVida  # noqa: E402

DESTINO = AQUI / 'evidencias/captura-projectile-set-m2-3-original.json'
CONTADOR_FORCADO = 9000


def executar():
    cap = json.loads(CAPTURA.read_bytes())
    ni = cap['named_inputs']['m1']
    b = BancadaVida(cq.entradas_quadro(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
    b.iniciar_relogio()
    b.executar_inicio()
    b.executar_mission_load(60)
    observadas = []
    perturbacoes = {'ProjectileSet': []}

    def observador(rotina, fase, caso, antes, resultado):
        esp = int(resultado['entry_registers']['ESP'], 16)
        observadas.append(dict(case=caso['case'], counter=u32(antes, CONTADOR),
                               pool=empacotar(ler(antes, u32(antes, POOL), 5600)),
                               stack_words=[hex(v) for v in struct.unpack('<7I', ler(antes, esp, 28))[1:]]))

    iso = Isolamento(b, ('ProjectileSet',), perturbacoes, observador)
    iso.instalar()
    original = iso.executar

    def executar_com_perturbacao(regs):
        # The perturbation needs the live EDX: only DL (the type) changes.
        perturbacoes['ProjectileSet'] = [dict(case='type-0x1f', writes=[],
                                              registers={'EDX': (regs['EDX'] & ~0xff) | 0x1f})]
        return original(regs)
    iso.executar = executar_com_perturbacao
    b.executar_cauda_carga(600)
    b.executar_entre_quadros(120)
    if u32(b.imagem(), CONTADOR) != 1:
        raise RuntimeError('Frame 1 must enter CalculGame with counter 1 before the forced write')
    b.cpu.mem_write(CONTADOR, struct.pack('<I', CONTADOR_FORCADO))
    b.executar_quadro(300, 1)
    casos = [c for r in iso.registros for c in r['cases']]
    if len(casos) != len(observadas):
        raise RuntimeError('Observer and isolated case records disagree')
    for c, obs in zip(casos, observadas):
        if c['case'] != obs['case']:
            raise RuntimeError('Observer order differs from isolated case order')
        c.update(counter=obs['counter'], pool_before=obs['pool'], stack_words=obs['stack_words'])
    return b, iso


def main():
    if DESTINO.exists():
        raise SystemExit(f'Refusing to overwrite existing evidence {DESTINO}')
    t0 = time.monotonic()
    b, iso = executar()
    relatorio = dict(
        schema='rising-lands/monde01-raid-projectile-set/1', original_sha256=HASH,
        label='forced input: v1 path, u32 0x508f7c = 9000 at frame 1\'s CalculGame entry; ProjectileSet isolated',
        translation_executed=False,
        frame_capture=dict(path=str(CAPTURA.relative_to(REPO)),
                           sha256=hashlib.sha256(CAPTURA.read_bytes()).hexdigest()),
        source_sha256={s: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for s, p in (
            ('capturar_projectile_set_m2_3.py', 'pesquisas-paralelas/combate/capturar_projectile_set_m2_3.py'),
            ('sondar_vida_incursao.py', 'pesquisas-paralelas/combate/sondar_vida_incursao.py'),
            ('oraculo_quadro_missao.py', 'pesquisas-paralelas/missoes/oraculo_quadro_missao.py'))},
        calls=iso.registros, code_sha256_after=b.sha256_codigo(),
        stack_format='six u32 words after the return address: mode, attacker, direction, dx, dy, flag',
        seconds=round(time.monotonic() - t0, 3))
    casos = [c['case'] for r in iso.registros for c in r['cases']]
    ok = casos == ['captured_inputs', 'type-0x1f'] and all(c['reached_return'] for r in iso.registros
                                                             for c in r['cases'])
    saida = DESTINO if ok else REPO / '.local' / ('combat-projectile-set-failed-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(relatorio, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(output=str(saida.relative_to(REPO)), cases=casos, seconds=relatorio['seconds'])), flush=True)
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
