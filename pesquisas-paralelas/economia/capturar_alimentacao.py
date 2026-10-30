"""Original-only capture of the hunger state (unit state 19: a starving unit walks to food and eats).

S1 evidence that this path is on the victory route: the Mac mini's S1 development run (stages 6-7, frames
5300-18000) first enters ``EnginSetFatigue``'s ``ChercheVegetLibre`` at frame 7958 and the state-19 body's
``TerrainRetireMatiere`` (EnginNextEtape+0x11c2, return 0x4555ee) and ``EnginRestaureEtat`` at 8057. Neither
CalculTransporteEngin (state 18) nor CalculDechargeCaveEngin (state 20) is entered by S1, P6 or P7.

Bench: ``bancada_ciclo_trabalho.Ciclo`` (MONDE01 display reference; frames 0/1 reproduced; then real frames
with the reference's no-input answers), driven by the committed work-cycle scenario
(``capturar_ciclo_trabalho.ordens``: cave created and completed, unit 14 Ctrl tag 7 with depot structure 0, the
builder 12 Ctrl tag 6, the colonist lodged in the cave). No Python translation is imported.

Declared hunger (the only addition). At the CalculGame entry of the first frame at or after ``FOME`` where the
unit is in state 5 (work), a declared write sets its provisions word +4 := 1 and its fatigue counter +0x74 :=
0xfffe. The frame's own CalculFatigue then reaches its threshold natively (+0x74 = 0, +4 = 0), and the
EnginNextEtape prelude calls EnginSetFatigue (saved state +0xa0, saved target +0xa2, food search
ChercheVegetLibre(cell, 20, 0x43), else the nearest own cave within 40 when food >= 3 -> +0xc2; state 19).
Everything after it is native.

Recorded calls (``Ciclo`` isolation): those of the work-cycle capture, plus the inline state-19 body
``EnginNextEtape:19`` (entry 0x4554db with ESI = unit record, DI = unit, exit 0x454ccd with the entry ESP) of
units 12 and 14 on every frame. Per frame: units 12/13/14/colonist with their hunger fields, player-0 resources,
the cave-count words, structures 0 and the cave.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/capturar_alimentacao.py \\
        --ate 1500 --saida pesquisas-paralelas/economia/evidencias/alimentacao/captura-alimentacao-exibicao.json.xz
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import capturar_ciclo_trabalho as cct  # noqa: E402

FONTES = cct.FONTES + ('pesquisas-paralelas/economia/capturar_alimentacao.py',)
ENTRADA_19, SAIDA_19 = 0x4554db, 0x454ccd
PSEUDO = {ENTRADA_19: ('EnginNextEtape:19', SAIDA_19)}
FOME = {12: 1100, 14: 1150}         # unit -> first frame of its declared hunger (unit in state 5)
UNIDADES_19 = tuple(FOME)


def unidade(c, i):
    u = cct.unidade(c, i)
    p = c.u32(cct.UNIDADES_PTR) + cct.PASSO * i
    u.update(provisions=c.u16(p + 4), provisions_max=c.u16(p + 0x76), fatigue=c.u16(p + 0x74),
             saved_state=c.u16(p + 0xa0), saved_target=c.u16(p + 0xa2), food_structure=c.u16(p + 0xc2),
             f72=c.u8(p + 0x72))
    return u


def ordens(estado):
    base = cct.ordens(estado)

    def gerar(c, k):
        yield from base(c, k)
        for i, quadro in FOME.items():
            rotulo = f'hunger {i}'
            if rotulo in estado.feito or k < quadro or unidade(c, i)['state'] != 5:
                continue
            estado.feito.add(rotulo)
            p = c.u32(cct.UNIDADES_PTR) + cct.PASSO * i
            yield cct.escrita(f'unit {i} provisions +4 := 1', p + 4, struct.pack('<H', 1))
            yield cct.escrita(f'unit {i} fatigue counter +0x74 := 0xfffe', p + 0x74, struct.pack('<H', 0xfffe))
    return gerar


def escolher(estado):
    base = cct.escolher(estado)

    def f(nome, regs, c):
        if nome == 'EnginNextEtape:19':
            return regs['EDI'] & 0xffff in UNIDADES_19
        return base(nome, regs, c)
    return f


def amostra(estado):
    base = cct.amostra(estado)

    def f(c):
        r = base(c)
        r['units'] = {i: unidade(c, i) for i in r['units']}
        return r
    return f


def executar(ate, observador=None, progresso=None):
    from bancada_ciclo_trabalho import Ciclo
    estado = cct.Estado()
    c = Ciclo(cct.ROTINAS, escolher(estado), ordens(estado), observador=observador, amostra=amostra(estado),
              pseudo=PSEUDO)
    segundos = c.executar(ate, progresso)
    return c, estado, segundos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ate', type=int, required=True, help='last frame counter 0x508f7c')
    a = ap.parse_args()
    saida = RAIZ / a.saida
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    from emulador import HASH_ORIGINAL
    from encerramento_captura import encerrar_captura
    revisao = subprocess.run(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()

    def progresso(k, s):
        if k % 100 == 0:
            print(f'frame {k} {s:.0f}s', flush=True)

    c, estado, segundos = executar(a.ate, progresso=progresso)
    dados = dict(
        schema='rising-lands/economy-hunger-capture/1', original_sha256=HASH_ORIGINAL, translation_executed=False,
        scenario='exibicao', source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        reference=dict(path=str(c.cap_caminho.relative_to(RAIZ)), sha256=hashlib.sha256(c.cap_caminho.read_bytes()).hexdigest()),
        inputs='display-reference named inputs; later frames keep the declared no-input answers; display clock '
               '0x123456+40*k (the reference rule, extended)',
        reproduction=c.reproducao, last_counter=a.ate, seconds=segundos, hunger=FOME,
        pseudo={hex(e): dict(name=n, exit=hex(s)) for e, (n, s) in PSEUDO.items()},
        colonist=estado.colono, cave=estado.cave, routines=list(cct.ROTINAS) + ['EnginNextEtape:19'],
        always_recorded=list(cct.SEMPRE), actions=c.acoes, frames=c.quadros, calls=c.registros)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9) if saida.suffix == '.xz' else bruto)
    n19 = sum(1 for r in c.registros if r['routine'] == 'EnginNextEtape:19')
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(), seconds=segundos,
                          reproduction=c.reproducao, calls=len(c.registros), state19_calls=n19,
                          actions=len(c.acoes)), indent=1), flush=True)
    encerrar_captura(0, saida)


if __name__ == '__main__':
    main()
