"""Original-only capture of the transport and cave-unload unit states (18 and 20) and of the hunger state's saved-state
checks, M3 (a human player's ordinary orders beyond the S1 script).

Why. A player reaches unit state 18 with tag 8 (a press on a sack: SetTransporteEnginSelect 0x473212 + the depot
tuple, ProcessInputGame 0x45f05f) and unit state 20 with tag 19 (SetDechargeCaveEnginSelect 0x473194 + the depot
tuple, 0x45f07d). Their per-frame bodies are CalculTransporteEngin 0x44f2d4 (EnginNextEtape 0x455e28; non-vehicles
go to EnginCalculTransporte 0x44ea78) and CalculDechargeCaveEngin 0x44e35c (0x455d1c). A unit that starves in any
state reaches the state-19 body, whose saved-state checks (+0xa0 = 1, 0xb, 0xd, 0xf, 0x12, 0x15, 0x17, 0x18) and
aborts (0x455107, 0x454ddd, 0x454ef8) were still outside the translated domain.

Bench: ``bancada_ciclo_trabalho.Ciclo`` with ``gravar_acoes`` (MONDE01 display reference; frames 0/1 reproduced; then
real frames with the reference's no-input answers), driven by the committed work-cycle scenario
(``capturar_ciclo_trabalho.ordens``: cave created and completed at frame 12, units 13/14 harvest, the builder 12
mines, the colonist lodges in the cave at frame 125). No Python translation is imported.

Declared orders, each as ProcessInputGame applies its tag (selection list, then the setter pair):
1. Frame ``QUADRO_ORDENS``: unit 13, tag 8 on the food sack nearest to it, Ctrl depot (2, cave, food);
   unit 12, tag 8 on the sack nearest to it of the kind present (stone when any stone sack exists, else food),
   Ctrl ground depot (1, its own cell, kind); unit 14, tag 19 on the cave, Ctrl depot (2, sanctuary 0, food).
2. Frame ``QUADRO_SEGUNDAS``: unit 14, tag 19 on the cave with a ground depot (1, the cell next to the sanctuary
   BatimentGetCase(0) gives, food); unit 13, plain tag 8 (depot (0, 0, 0)) on the food sack nearest to it.
3. The first frame at or after ``QUADRO_FOME`` with unit 12 or 13 in state 18: its declared hunger (provisions +4 := 1,
   fatigue +0x74 := 0xfffe): EnginSetFatigue saves state 0x12 natively and the state-19 body runs its check.
4. From frame ``QUADRO_CASOS`` (built from that frame's state, ``CASOS_POR_QUADRO`` per frame): restored cases (the
   whole state put back after each), every one with the fields its
   branch reads declared: CalculDechargeCaveEngin and CalculTransporteEngin over every phase, depot mode, bag
   content, timer and target (unit 14 and unit 13; vehicles: unit 14 declared type 0xd); EnginNextEtape(unit) in
   state 19 with each checked saved state and the targets its check reads, and the aborts of saved states 5 and 0x14.
   Cases that drop a sack (EnginRetireType) stand the unit on unit 12's ground-depot cell, where the natural flow
   drops its sacks.

Recorded calls (``Ciclo`` isolation, also inside declared calls): CalculTransporteEngin and CalculDechargeCaveEngin
(every declared one; a frame's own when the unit's timer is about to expire in a timed phase, within 2 cells of its
destination, within 3 frames of an order, or every 25th frame); the state-19 body ``EnginNextEtape:19`` (entry
0x4554db, exit 0x454ccd) inside declared calls and whenever its saved state is one of the checked ones. Per frame:
units 12/13/14, player-0 resources, the cave-count words, structures 0 and the cave.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/capturar_transporte.py --ate 1800 \\
        --saida pesquisas-paralelas/economia/evidencias/transporte/captura-transporte.json.xz
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

import capturar_alimentacao as cal  # noqa: E402
import capturar_ciclo_trabalho as cct  # noqa: E402

FONTES = cal.FONTES + ('pesquisas-paralelas/economia/capturar_transporte.py',)
ROTINAS = ('CalculTransporteEngin', 'CalculDechargeCaveEngin')
GRADE_OBJETOS, GRADE_QUANTIDADES = 0x507d74, 0x507dac
BUSCA_UNIDADE = 0x496304
COMIDA_P0 = cct.RECURSOS + 8
QUADRO_ORDENS = 200
QUADRO_CASOS = 400
CASOS_POR_QUADRO = 25
QUADRO_FOME = 600
QUADRO_SEGUNDAS = 1000
VERIFICADOS = (1, 0xb, 0xd, 0xf, 0x12, 0x15, 0x17, 0x18)


def _u16(v):
    return struct.pack('<H', v & 0xffff)


def registro(c, i):
    return c.u32(cct.UNIDADES_PTR) + cct.PASSO * i


def campos(c, i, rotulo, valores):
    p = registro(c, i)
    # No original instruction runs between these declared field writes. Merge
    # adjacent fields without touching a gap; each action otherwise snapshots
    # the entire native image before and after a single byte/word assignment.
    trechos = []
    for o, (n, v) in sorted(valores.items()):
        bruto = v.to_bytes(n, 'little')
        nome = f'+{o:#x} := {v:#x}'
        if trechos and trechos[-1][0] + len(trechos[-1][1]) == p + o:
            trechos[-1][1].extend(bruto)
            trechos[-1][2].append(nome)
        else:
            trechos.append((p + o, bytearray(bruto), [nome]))
    return [cct.escrita(f'{rotulo}: unit {i} ' + ', '.join(nomes), a, bruto)
            for a, bruto, nomes in trechos]


def estrutura(c, s, deslocamento, valor, rotulo):
    return cct.escrita(f'{rotulo}: structure {s} +{deslocamento:#x} := {valor:#x}',
                       cct.ESTRUTURAS + cct.PASSO * s + deslocamento, [valor])


def saco(c, celula, tipo, quantidade, rotulo):
    return [cct.escrita(f'{rotulo}: object at {celula} := {0x42 + tipo:#x}', c.u32(GRADE_OBJETOS) + celula,
                        [(0x42 + tipo) if quantidade else 0]),
            cct.escrita(f'{rotulo}: quantity at {celula} := {quantidade}', c.u32(GRADE_QUANTIDADES) + celula,
                        [quantidade])]


def busca(i):
    return [cct.escrita(f'path-search owner 0x496304 := {i}', BUSCA_UNIDADE, _u16(i))]


def sacos(c, tipo):
    objetos = c.ler(c.u32(GRADE_OBJETOS), 0x10000)
    return [i for i, b in enumerate(objetos) if b == 0x42 + tipo]


def distancia(a, b):
    return max(abs((a & 0xff) - (b & 0xff)), abs((a >> 8) - (b >> 8)))


def mais_proximo(c, celula, tipo):
    s = sacos(c, tipo)
    return min(s, key=lambda x: (distancia(x, celula), x)) if s else None


# Bags (+0xa): u16 count, u16 capacity, u16 values from +6, u8 tags from +0x42, u16 goods counter +0x66.
def bolsa_vazia():
    # BagContient scans capacity, not live count. Clear both slots used by this
    # matrix (one case widens capacity to 2), including stale values and tags.
    # Leaving a tag with count 0 makes EnginRetireType loop after BagRetire fails.
    return {0xa: (2, 0), 0xc: (2, 1), 0x10: (4, 0), 0x4c: (2, 0), 0x70: (2, 0)}


def bolsa_cheia():
    return bolsa_com(1)


def bolsa_com(tipo):
    return {0xa: (2, 1), 0xc: (2, 1), 0x10: (2, tipo), 0x4c: (1, 2), 0x70: (2, 1)}


class Estado(cct.Estado):
    def __init__(self):
        super().__init__()
        self.ordens = {}
        self.ultima = {}
        self.fome = None
        self.sanctuary_cell = None
        self.cases = 0
        self.cases_planned = 0
        self.pendentes = []
        self.chao = None


def casos_descarga(c, e, celula_s0):
    """CalculDechargeCaveEngin restored cases on unit 14 (state 20, cave unload)."""
    u, cave = 14, e.cave
    p = registro(c, u)
    caixa = c.u16(p + 0xb2)
    longe = cct.MINA
    base = {2: (1, 0x14), 1: (1, 5), 0xc0: (2, cave), 0xb2: (2, caixa), 0x84: (2, 1), 0x86: (1, 0), 0x87: (1, 0)}
    s = []

    def k(rotulo, valores, outras=()):
        s.append((rotulo, u, 'CalculDechargeCaveEngin', {**base, **valores}, list(outras)))

    k('phase 0, walking', {0x89: (1, 0), 8: (2, longe), 0x7e: (2, caixa), **bolsa_vazia()})
    k('phase 0, bag full', {0x89: (1, 0), **bolsa_cheia()})
    k('phase 0, at +0x7e far from the cave', {0x89: (1, 0), 8: (2, longe), 0x7e: (2, longe), **bolsa_vazia()})
    k('phase 0, at +0x7e far from the cave, owning the search', {0x89: (1, 0), 8: (2, longe), 0x7e: (2, longe),
                                                                 **bolsa_vazia()}, busca(u))
    k('phase 0, next to the cave', {0x89: (1, 0), 8: (2, caixa), 0x7e: (2, caixa), **bolsa_vazia()})
    k('phase 1, timer 5', {0x89: (1, 1), 0x8b: (1, 5), **bolsa_vazia()})
    k('phase 1, timer 0', {0x89: (1, 1), 0x8b: (1, 0), **bolsa_vazia()})
    k('phase 1, timer 1, food taken', {0x89: (1, 1), 0x8b: (1, 1), **bolsa_vazia()})
    k('phase 1, timer 1, no food', {0x89: (1, 1), 0x8b: (1, 1), **bolsa_vazia()},
      [cct.escrita('player-0 food words := 0', COMIDA_P0, bytes(4))])
    for tipo in (0, 2, 3):
        k(f'phase 1, timer 1, kind {tipo}', {0x89: (1, 1), 0x8b: (1, 1), 0x84: (2, tipo), **bolsa_vazia()})
    for modo, alvo, rot in ((2, 0, 'sanctuary'), (2, 0xffff, 'no structure'), (1, celula_s0, 'a cell'),
                            (0, 0, 'mode 0')):
        k(f'phase 1, bag full, depot {modo} {rot}', {0x89: (1, 1), 0x82: (1, modo), 0x80: (2, alvo), **bolsa_cheia()})
        if modo:
            k(f'phase 1, bag full, depot {modo} {rot}, owning the search',
              {0x89: (1, 1), 0x82: (1, modo), 0x80: (2, alvo), **bolsa_cheia()}, busca(u))
    k('phase 1, bag full, depot 2 no structure, state 4', {2: (1, 4), 0x89: (1, 1), 0x82: (1, 2), 0x80: (2, 0xffff),
                                                          **bolsa_cheia()})
    k('phase 1, bag full, depot 2 no structure, state 0', {2: (1, 0), 0x89: (1, 1), 0x82: (1, 2),
                                                          0x80: (2, 0xffff), **bolsa_cheia()})
    k('phase 2, depot 2, byte +0x86', {0x89: (1, 2), 0x82: (1, 2), 0x80: (2, 0), 0x86: (1, 1), **bolsa_com(1)})
    k('phase 2, depot 2, byte +0x87', {0x89: (1, 2), 0x82: (1, 2), 0x80: (2, 0), 0x87: (1, 0x80), **bolsa_com(1)})
    k('phase 2, depot 2, far', {0x89: (1, 2), 0x82: (1, 2), 0x80: (2, 0), 8: (2, longe), **bolsa_com(1)})
    k('phase 2, depot 2, next to it', {0x89: (1, 2), 0x82: (1, 2), 0x80: (2, 0), 8: (2, celula_s0), **bolsa_com(1)})
    k('phase 2, depot 2 the cave, next to it', {0x89: (1, 2), 0x82: (1, 2), 0x80: (2, cave), 8: (2, caixa),
                                                **bolsa_com(1)})
    k('phase 2, depot 1, walking', {0x89: (1, 2), 0x82: (1, 1), 0x80: (2, celula_s0), 8: (2, longe),
                                    0x7e: (2, celula_s0), **bolsa_com(1)})
    k('phase 2, depot 1, there', {0x89: (1, 2), 0x82: (1, 1), 0x80: (2, celula_s0), 8: (2, celula_s0),
                                  0x7e: (2, celula_s0), **bolsa_com(1)})
    k('phase 2, depot 1, there, on the cave cell', {0x89: (1, 2), 0x82: (1, 1), 0x80: (2, caixa), 8: (2, caixa),
                                                    0x7e: (2, caixa), **bolsa_com(1)})
    k('phase 2, depot 1, there, owning the search', {0x89: (1, 2), 0x82: (1, 1), 0x80: (2, caixa), 8: (2, caixa),
                                                     0x7e: (2, caixa), **bolsa_com(1)}, busca(u))
    k('phase 2, depot 1, far target', {0x89: (1, 2), 0x82: (1, 1), 0x80: (2, longe), 8: (2, celula_s0),
                                       0x7e: (2, celula_s0), **bolsa_com(1)})
    k('phase 2, depot 1, far target, owning the search', {0x89: (1, 2), 0x82: (1, 1), 0x80: (2, longe),
                                                          8: (2, celula_s0), 0x7e: (2, celula_s0), **bolsa_com(1)},
      busca(u))
    k('phase 2, depot 0', {0x89: (1, 2), 0x82: (1, 0), **bolsa_com(1)})
    for modo, alvo in ((2, 0), (2, cave), (1, e.chao), (0, 0)):
        k(f'phase 3, timer 1, food carried, depot {modo} {alvo:#x}', {0x89: (1, 3), 0x8b: (1, 1), 0x82: (1, modo),
                                                                     0x80: (2, alvo), 8: (2, e.chao),
                                                                     **bolsa_com(1)})
    k('phase 3, timer 1, stone carried, depot 2', {0x89: (1, 3), 0x8b: (1, 1), 0x82: (1, 2), 0x80: (2, 0),
                                                   0x84: (2, 2), **bolsa_com(2)})
    k('phase 3, timer 4', {0x89: (1, 3), 0x8b: (1, 4), 0x82: (1, 2), 0x80: (2, 0), **bolsa_com(1)})
    k('phase 3, timer 1, empty', {0x89: (1, 3), 0x8b: (1, 1), 0x82: (1, 2), 0x80: (2, 0), **bolsa_vazia()})
    k('phase 3, timer 1, empty, owning the search', {0x89: (1, 3), 0x8b: (1, 1), 0x82: (1, 2), 0x80: (2, 0),
                                                     **bolsa_vazia()}, busca(u))
    k('phase 3, timer 1, empty, no cave cell', {0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, 0xffff), **bolsa_vazia()})
    k('phase 3, timer 1, empty, no cave cell, owning the search', {0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, 0xffff),
                                                                   **bolsa_vazia()}, busca(u))
    k('phase 3, timer 1, empty, no cave cell, state 4', {2: (1, 4), 0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, 0xffff),
                                                        **bolsa_vazia()})
    k('phase 4', {0x89: (1, 4)})
    k('phase 0xff', {0x89: (1, 0xff)})
    return s


def casos_transporte(c, e, celula_s0):
    """CalculTransporteEngin restored cases: unit 13 (type 5, EnginCalculTransporte) and unit 14 declared a vehicle
    (type 0xd)."""
    cave = e.cave
    s = []
    longe = cct.MINA
    for u, tipo in ((13, 5), (14, 0xd)):
        p = registro(c, u)
        cel = c.u16(p + 8)
        alvo_saco = mais_proximo(c, cel, 1)
        perto = alvo_saco if alvo_saco is not None else cel
        base = {1: (1, tipo), 2: (1, 0x12), 0x84: (2, 1), 0x86: (1, 0), 0x87: (1, 0), 0xb2: (2, perto),
                0x7c: (2, cel), 0xc0: (2, 0xffff)}
        rot = f'type {tipo:#x}'

        def k(rotulo, valores, outras=(), u=u, base=base, rot=rot):
            s.append((f'{rot}, {rotulo}', u, 'CalculTransporteEngin', {**base, **valores}, list(outras)))

        modos = ((2, cave), (0, 0)) if tipo == 0xd else ((2, cave), (1, celula_s0), (0, 0))
        for modo, alvo in modos:
            m = {0x82: (1, modo), 0x80: (2, alvo)}
            k(f'depot {modo}, phase 0, walking', {**m, 0x89: (1, 0), 8: (2, cel), 0x7e: (2, longe), **bolsa_vazia()})
            k(f'depot {modo}, phase 0, on the sack', {**m, 0x89: (1, 0), 8: (2, cel), 0x7e: (2, cel),
                                                      **bolsa_vazia()}, saco(c, cel, 1, 3, 'sack'))
            k(f'depot {modo}, phase 0, on a sack of another kind', {**m, 0x89: (1, 0), 8: (2, cel), 0x7e: (2, cel),
                                                                    **bolsa_vazia()}, saco(c, cel, 2, 3, 'sack'))
            k(f'depot {modo}, phase 0, no sack, one near +0xb2', {**m, 0x89: (1, 0), 8: (2, cel), 0x7e: (2, cel),
                                                                  **bolsa_vazia()}, saco(c, cel, 1, 0, 'no sack'))
            k(f'depot {modo}, phase 0, no sack, one near +0xb2, owning the search',
              {**m, 0x89: (1, 0), 8: (2, cel), 0x7e: (2, cel), **bolsa_vazia()},
              saco(c, cel, 1, 0, 'no sack') + busca(u))
            k(f'depot {modo}, phase 0, no sack near +0xb2', {**m, 0x89: (1, 0), 8: (2, cel), 0x7e: (2, cel),
                                                            0xb2: (2, longe), **bolsa_vazia()},
              saco(c, cel, 1, 0, 'no sack'))
            k(f'depot {modo}, phase 0, bag full', {**m, 0x89: (1, 0), **bolsa_cheia()})
            k(f'depot {modo}, phase 1, timer 3', {**m, 0x89: (1, 1), 0x8b: (1, 3), **bolsa_vazia()})
            for q in (3, 1):
                k(f'depot {modo}, phase 1, timer 1, sack of {q}', {**m, 0x89: (1, 1), 0x8b: (1, 1), 8: (2, cel),
                                                                   **bolsa_vazia()}, saco(c, cel, 1, q, 'sack'))
            k(f'depot {modo}, phase 1, timer 1, sack of 3, owning the search',
              {**m, 0x89: (1, 1), 0x8b: (1, 1), 8: (2, cel), **bolsa_vazia()}, saco(c, cel, 1, 3, 'sack') + busca(u))
            k(f'depot {modo}, phase 1, timer 1, sack of 1, far from sacks',
              {**m, 0x89: (1, 1), 0x8b: (1, 1), 8: (2, longe), **bolsa_vazia()}, saco(c, longe, 1, 1, 'sack'))
            k(f'depot {modo}, phase 1, timer 1, sack of 1, bag of 2',
              {**m, 0x89: (1, 1), 0x8b: (1, 1), 8: (2, cel), **bolsa_vazia(), 0xc: (2, 2)},
              saco(c, cel, 1, 1, 'sack'))
            k(f'depot {modo}, phase 1, bag full', {**m, 0x89: (1, 1), **bolsa_cheia()})
            k(f'depot {modo}, phase 1, bag full, owning the search', {**m, 0x89: (1, 1), **bolsa_cheia()}, busca(u))
            if modo == 2:
                k('depot 2 no structure, phase 1, bag full', {0x82: (1, 2), 0x80: (2, 0xffff), 0x89: (1, 1),
                                                              **bolsa_cheia()})
                k('depot 2 no structure, phase 1, bag full, owning the search',
                  {0x82: (1, 2), 0x80: (2, 0xffff), 0x89: (1, 1), **bolsa_cheia()}, busca(u))
                k('depot 2 sanctuary, phase 1, bag full', {0x82: (1, 2), 0x80: (2, 0), 0x89: (1, 1),
                                                           **bolsa_cheia()})
        if tipo == 5:
            m2 = {0x82: (1, 2), 0x80: (2, 0), 0xc0: (2, 0)}
            k('phase 2, depot 2, destroyed', {**m2, 0x89: (1, 2), 0x7e: (2, celula_s0), **bolsa_com(1)},
              [estrutura(c, 0, 5, 3, 'destroyed')])
            k('phase 2, depot 2, byte +0x86', {**m2, 0x89: (1, 2), 0x86: (1, 1), **bolsa_com(1)})
            k('phase 2, depot 2, byte +0x87', {**m2, 0x89: (1, 2), 0x87: (1, 1), **bolsa_com(1)})
            k('phase 2, depot 2, far', {**m2, 0x89: (1, 2), 8: (2, longe), **bolsa_com(1)})
            k('phase 2, depot 2, next to it', {**m2, 0x89: (1, 2), 8: (2, celula_s0), **bolsa_com(1)})
            m1 = {0x82: (1, 1), 0x80: (2, celula_s0)}
            k('phase 2, depot 1, walking', {**m1, 0x89: (1, 2), 8: (2, longe), 0x7e: (2, celula_s0), **bolsa_com(1)})
            k('phase 2, depot 1, there', {**m1, 0x89: (1, 2), 8: (2, celula_s0), 0x7e: (2, celula_s0),
                                          **bolsa_com(1)})
            k('phase 2, depot 1, there, the cave cell', {0x82: (1, 1), 0x80: (2, c.u16(registro(c, 14) + 0xb2)),
                                                         0x89: (1, 2), 8: (2, c.u16(registro(c, 14) + 0xb2)),
                                                         0x7e: (2, c.u16(registro(c, 14) + 0xb2)), **bolsa_com(1)})
            k('phase 2, depot 1, there, the cave cell, owning the search',
              {0x82: (1, 1), 0x80: (2, c.u16(registro(c, 14) + 0xb2)), 0x89: (1, 2),
               8: (2, c.u16(registro(c, 14) + 0xb2)), 0x7e: (2, c.u16(registro(c, 14) + 0xb2)), **bolsa_com(1)},
              busca(u))
            k('phase 2, depot 1, far target', {0x82: (1, 1), 0x80: (2, longe), 0x89: (1, 2), 8: (2, celula_s0),
                                               0x7e: (2, celula_s0), **bolsa_com(1)})
            k('phase 2, depot 1, far target, owning the search', {0x82: (1, 1), 0x80: (2, longe), 0x89: (1, 2),
                                                                  8: (2, celula_s0), 0x7e: (2, celula_s0),
                                                                  **bolsa_com(1)}, busca(u))
            k('phase 2, depot 0', {0x82: (1, 0), 0x89: (1, 2), **bolsa_com(1)})
            for modo, alvo in ((2, 0), (2, cave), (1, e.chao), (0, 0)):
                k(f'phase 3, timer 1, food carried, depot {modo} {alvo:#x}',
                  {0x82: (1, modo), 0x80: (2, alvo), 0xc0: (2, alvo if modo == 2 else 0), 0x89: (1, 3),
                   0x8b: (1, 1), 8: (2, e.chao), **bolsa_com(1)})
            k('phase 3, structure destroyed, timer 4', {**m2, 0x89: (1, 3), 0x8b: (1, 4), 0x7e: (2, celula_s0),
                                                        **bolsa_com(1)}, [estrutura(c, 0, 5, 3, 'destroyed')])
            k('phase 3, timer 4', {**m2, 0x89: (1, 3), 0x8b: (1, 4), **bolsa_com(1)})
            k('phase 3, timer 1, empty, a sack near +0xb2', {**m2, 0x89: (1, 3), 0x8b: (1, 1), **bolsa_vazia()})
            k('phase 3, timer 1, empty, a sack near +0xb2, owning the search',
              {**m2, 0x89: (1, 3), 0x8b: (1, 1), **bolsa_vazia()}, busca(u))
            k('phase 3, timer 1, empty, the sack is the depot cell',
              {0x82: (1, 1), 0x80: (2, perto), 0xc0: (2, 0), 0x89: (1, 3), 0x8b: (1, 1), **bolsa_vazia()})
            k('phase 3, timer 1, empty, no sack near +0xb2', {**m2, 0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, longe),
                                                              **bolsa_vazia()})
            k('phase 3, timer 1, empty, no sack near +0xb2, owning the search',
              {**m2, 0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, longe), **bolsa_vazia()}, busca(u))
            k('phase 3, timer 1, empty, no sack near +0xb2, state 4',
              {**m2, 2: (1, 4), 0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, longe), **bolsa_vazia()})
            k('phase 3, timer 1, empty, no +0xb2', {**m2, 0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, 0xffff),
                                                    **bolsa_vazia()})
            k('phase 3, timer 1, empty, no +0xb2, owning the search',
              {**m2, 0x89: (1, 3), 0x8b: (1, 1), 0xb2: (2, 0xffff), **bolsa_vazia()}, busca(u))
            k('phase 3, timer 1, empty, no +0xb2, state 0', {**m2, 2: (1, 0), 0x89: (1, 3), 0x8b: (1, 1),
                                                             0xb2: (2, 0xffff), **bolsa_vazia()})
            k('phase 4', {0x89: (1, 4)})
        else:
            caixa = c.u16(registro(c, 14) + 0xb2)
            for modo, alvo in ((2, cave), (0, 0)):
                m = {0x82: (1, modo), 0x80: (2, alvo), 0xc0: (2, alvo if modo == 2 else 0xffff)}
                k(f'depot {modo}, phase 2, walking', {**m, 0x89: (1, 2), 8: (2, cel), 0x7e: (2, longe),
                                                      **bolsa_com(1)})
                k(f'depot {modo}, phase 2, there', {**m, 0x89: (1, 2), 8: (2, caixa), 0x7e: (2, caixa),
                                                    **bolsa_com(1)})
                k(f'depot {modo}, phase 3, turning', {**m, 0x89: (1, 3), 0x90: (1, 9), 0x91: (1, 3),
                                                      **bolsa_com(1)})
                k(f'depot {modo}, phase 3, facing', {**m, 0x89: (1, 3), 0x90: (1, 9), 0x91: (1, 9), 8: (2, caixa),
                                                     **bolsa_com(1)})
                k(f'depot {modo}, phase 4, timer 1, carried', {**m, 0x89: (1, 4), 0x8b: (1, 1), 8: (2, e.chao),
                                                               **bolsa_com(1)})
                k(f'depot {modo}, phase 4, timer 3, carried', {**m, 0x89: (1, 4), 0x8b: (1, 3), **bolsa_com(1)})
                k(f'depot {modo}, phase 4, empty', {**m, 0x89: (1, 4), 0x8b: (1, 1), **bolsa_vazia()})
                k(f'depot {modo}, phase 4, empty, owning the search', {**m, 0x89: (1, 4), 0x8b: (1, 1),
                                                                       **bolsa_vazia()}, busca(u))
            k('depot 1 (EnginCalculTransporte), phase 1, bag full', {0x82: (1, 1), 0x80: (2, celula_s0),
                                                                     0x89: (1, 1), **bolsa_cheia()})
            k('depot 1 (EnginCalculTransporte), phase 3, timer 1, carried',
              {0x82: (1, 1), 0x80: (2, e.chao), 0x89: (1, 3), 0x8b: (1, 1), 8: (2, e.chao), **bolsa_com(1)})
            k('depot 2, phase 5', {0x82: (1, 2), 0x80: (2, cave), 0x89: (1, 5)})
            for t in (0xb, 0x11, 0xa, 0x12):
                s.append((f'type {t:#x}, depot 2, phase 1, bag full', u, 'CalculTransporteEngin',
                          {**base, **{1: (1, t), 0x82: (1, 2), 0x80: (2, cave), 0x89: (1, 1), **bolsa_cheia()}}, []))
    return s


def casos_fome(c, e):
    """State-19 bodies through EnginNextEtape(unit) with each checked saved state +0xa0 and the targets it reads;
    the meal afterwards is the one already translated (food structure +0xc2 = the cave)."""
    cave = e.cave
    u12, u14 = 12, 14
    p = registro(c, u14)
    caixa = c.u16(p + 0xb2) if c.u16(p + 0xb2) != 0xffff else c.u16(p + 8)
    # Provisions 2 and fatigue counter 0 keep the prelude's CalculFatigue/EnginSetFatigue from saving a new state;
    # state 19 towards the cave (+0xc2).
    base = {2: (1, 0x13), 1: (1, 5), 4: (2, 2), 0x74: (2, 0), 0xc2: (2, cave), 0x7e: (2, caixa), 0x86: (1, 0),
            0x87: (1, 0), 0x72: (1, 0)}
    s = []

    def k(rotulo, valores, outras=(), u=u14):
        s.append((f'state 19, {rotulo}', u, 'EnginNextEtape', {**base, **valores}, list(outras)))

    for v in (1, 0x18):
        for b7 in (0, 2, 4):
            k(f'saved {v:#x}, mode {b7}', {0xa0: (2, v), 0xb7: (1, b7)})
        k(f'saved {v:#x}, unit target 12', {0xa0: (2, v), 0xb7: (1, 1), 0xb8: (2, u12)})
        k(f'saved {v:#x}, unit target none', {0xa0: (2, v), 0xb7: (1, 1), 0xb8: (2, 0xffff)})
        k(f'saved {v:#x}, unit target 12 gone', {0xa0: (2, v), 0xb7: (1, 1), 0xb8: (2, u12)},
          campos(c, u12, 'gone', {2: (1, 0)}))
        k(f'saved {v:#x}, unit target 12 state 4', {0xa0: (2, v), 0xb7: (1, 1), 0xb8: (2, u12)},
          campos(c, u12, 'state 4', {2: (1, 4)}))
        k(f'saved {v:#x}, unit target 12 neutral', {0xa0: (2, v), 0xb7: (1, 1), 0xb8: (2, u12)},
          campos(c, u12, 'neutral', {0: (1, 0xc8)}))
        k(f'saved {v:#x}, unit target 12 collided', {0xa0: (2, v), 0xb7: (1, 1), 0xb8: (2, u12)},
          campos(c, u12, 'collided', {0x72: (1, 1)}))
        k(f'saved {v:#x}, structure target none', {0xa0: (2, v), 0xb7: (1, 3), 0xb8: (2, 0xffff)})
        k(f'saved {v:#x}, structure target 0', {0xa0: (2, v), 0xb7: (1, 3), 0xb8: (2, 0)})
        k(f'saved {v:#x}, structure target 0 destroyed', {0xa0: (2, v), 0xb7: (1, 3), 0xb8: (2, 0)},
          [estrutura(c, 0, 5, 3, 'destroyed')])
        k(f'saved {v:#x}, structure target 0 neutral', {0xa0: (2, v), 0xb7: (1, 3), 0xb8: (2, 0)},
          [estrutura(c, 0, 4, 0xc8, 'neutral')])
    for v in (0xb, 0x15):
        k(f'saved {v:#x}, no structure', {0xa0: (2, v), 0xc0: (2, 0xffff)})
        k(f'saved {v:#x}, structure 0', {0xa0: (2, v), 0xc0: (2, 0)})
        k(f'saved {v:#x}, structure 0 destroyed', {0xa0: (2, v), 0xc0: (2, 0)}, [estrutura(c, 0, 5, 3, 'destroyed')])
    for tipo in (5, 6, 7):
        k(f'saved 0xf, type {tipo}, structure 0', {0xa0: (2, 0xf), 1: (1, tipo), 0xc0: (2, 0)})
        k(f'saved 0xf, type {tipo}, structure 0 destroyed', {0xa0: (2, 0xf), 1: (1, tipo), 0xc0: (2, 0)},
          [estrutura(c, 0, 5, 3, 'destroyed')])
    k('saved 0xf, type 6, unit 12', {0xa0: (2, 0xf), 1: (1, 6), 0xc0: (2, u12)})
    k('saved 0xf, type 6, unit 12 gone', {0xa0: (2, 0xf), 1: (1, 6), 0xc0: (2, u12)},
      campos(c, u12, 'gone', {2: (1, 0)}))
    k('saved 0xf, type 6, unit 12 state 4', {0xa0: (2, 0xf), 1: (1, 6), 0xc0: (2, u12)},
      campos(c, u12, 'state 4', {2: (1, 4)}))
    k('saved 0xd, nothing', {0xa0: (2, 0xd), 0xc0: (2, 0xffff), 0xb8: (2, 0xffff)})
    k('saved 0xd, structure 0', {0xa0: (2, 0xd), 0xc0: (2, 0)})
    k('saved 0xd, structure 0 destroyed', {0xa0: (2, 0xd), 0xc0: (2, 0)}, [estrutura(c, 0, 5, 3, 'destroyed')])
    k('saved 0xd, structure 0 other owner', {0xa0: (2, 0xd), 0xc0: (2, 0)}, [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0xd, structure 0 neutral', {0xa0: (2, 0xd), 0xc0: (2, 0)}, [estrutura(c, 0, 4, 0xc8, 'neutral')])
    k('saved 0xd, structure 0 neutral, colonist', {0xa0: (2, 0xd), 1: (1, 9), 0xc0: (2, 0)},
      [estrutura(c, 0, 4, 0xc8, 'neutral')])
    k('saved 0xd, type 10, structure 0', {0xa0: (2, 0xd), 1: (1, 10), 0xc0: (2, 0)})
    k('saved 0xd, type 10, structure 0 neutral', {0xa0: (2, 0xd), 1: (1, 10), 0xc0: (2, 0)},
      [estrutura(c, 0, 4, 0xc8, 'neutral')])
    k('saved 0xd, type 10, structure 0 other owner', {0xa0: (2, 0xd), 1: (1, 10), 0xc0: (2, 0)},
      [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0xd, unit 12', {0xa0: (2, 0xd), 0xc0: (2, 0xffff), 0xb8: (2, u12)})
    k('saved 0xd, unit 12 gone', {0xa0: (2, 0xd), 0xc0: (2, 0xffff), 0xb8: (2, u12)},
      campos(c, u12, 'gone', {2: (1, 0)}))
    k('saved 0xd, unit 12 other owner', {0xa0: (2, 0xd), 0xc0: (2, 0xffff), 0xb8: (2, u12)},
      campos(c, u12, 'owner 1', {0: (1, 1)}))
    k('saved 0xd, unit 12 neutral', {0xa0: (2, 0xd), 0xc0: (2, 0xffff), 0xb8: (2, u12)},
      campos(c, u12, 'neutral', {0: (1, 0xc8)}))
    for v in (0x12,):
        for modo in (0, 2):
            k(f'saved {v:#x}, depot {modo} sanctuary', {0xa0: (2, v), 0x82: (1, modo), 0x80: (2, 0)})
        k(f'saved {v:#x}, depot 2 destroyed', {0xa0: (2, v), 0x82: (1, 2), 0x80: (2, 0)},
          [estrutura(c, 0, 5, 3, 'destroyed')])
        k(f'saved {v:#x}, depot 2 other owner', {0xa0: (2, v), 0x82: (1, 2), 0x80: (2, 0)},
          [estrutura(c, 0, 4, 1, 'owner 1')])
        k(f'saved {v:#x}, depot 2 other owner, collided', {0xa0: (2, v), 0x82: (1, 2), 0x80: (2, 0), 0x72: (1, 1)},
          [estrutura(c, 0, 4, 1, 'owner 1')])
        k(f'saved {v:#x}, depot 2 other owner, unit neutral', {0xa0: (2, v), 0x82: (1, 2), 0x80: (2, 0),
                                                               0: (1, 0xc8)}, [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0x17, structure 0', {0xa0: (2, 0x17), 0xc0: (2, 0)})
    k('saved 0x17, structure 0 destroyed', {0xa0: (2, 0x17), 0xc0: (2, 0)}, [estrutura(c, 0, 5, 3, 'destroyed')])
    k('saved 0x17, structure 0 neutral', {0xa0: (2, 0x17), 0xc0: (2, 0)}, [estrutura(c, 0, 4, 0xc8, 'neutral')])
    k('saved 0x17, structure 0 other owner', {0xa0: (2, 0x17), 0xc0: (2, 0)}, [estrutura(c, 0, 4, 1, 'owner 1')])
    for tipo in (5, 7):
        k(f'saved 5, type {tipo}, depot destroyed', {0xa0: (2, 5), 1: (1, tipo), 0x82: (1, 2), 0x80: (2, 0)},
          [estrutura(c, 0, 5, 3, 'destroyed')])
    k('saved 5, depot other owner', {0xa0: (2, 5), 0x82: (1, 2), 0x80: (2, 0)}, [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 5, depot other owner, collided', {0xa0: (2, 5), 0x82: (1, 2), 0x80: (2, 0), 0x72: (1, 1)},
      [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0x14, unload structure destroyed', {0xa0: (2, 0x14), 0xc0: (2, 0)}, [estrutura(c, 0, 5, 3, 'destroyed')])
    k('saved 0x14, unload structure other owner', {0xa0: (2, 0x14), 0xc0: (2, 0)}, [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0x14, unload structure lost, collided', {0xa0: (2, 0x14), 0xc0: (2, 0), 0x72: (1, 1)},
      [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0x14, depot destroyed', {0xa0: (2, 0x14), 0xc0: (2, cave), 0x82: (1, 2), 0x80: (2, 0)},
      [estrutura(c, 0, 5, 3, 'destroyed')])
    k('saved 0x14, depot other owner', {0xa0: (2, 0x14), 0xc0: (2, cave), 0x82: (1, 2), 0x80: (2, 0)},
      [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0x14, depot lost, collided', {0xa0: (2, 0x14), 0xc0: (2, cave), 0x82: (1, 2), 0x80: (2, 0),
                                           0x72: (1, 1)}, [estrutura(c, 0, 4, 1, 'owner 1')])
    k('saved 0x14, depot lost, unit neutral', {0xa0: (2, 0x14), 0xc0: (2, cave), 0x82: (1, 2), 0x80: (2, 0),
                                               0: (1, 0xc8)}, [estrutura(c, 0, 4, 1, 'owner 1')])
    return s


def ordens(estado):
    base = cct.ordens(estado)

    def ordem(c, k, u, rotulo, passos):
        estado.ultima[u] = k
        estado.ordens.setdefault(str(u), []).append(dict(frame=k, label=rotulo))
        yield cct.selecao([u])
        yield from passos

    def gerar(c, k):
        yield from base(c, k)
        cave = estado.cave
        if k == QUADRO_ORDENS:
            r = c._acao(k, cct.chamada('BatimentGetCase(sanctuary 0)', 'BatimentGetCase', EAX=0, EBX=0, EDX=0))
            estado.sanctuary_cell = int(c.acoes[-1]['exit_registers']['EAX'], 16) & 0xffff
            del r
            c13 = c.u16(registro(c, 13) + 8)
            s13 = mais_proximo(c, c13, 1)
            if s13 is not None:
                yield from ordem(c, k, 13, f'tag 8 sack {s13}, Ctrl depot (2, cave, food)', [
                    cct.chamada(f'tag 8: SetTransporteEnginSelect(0, {s13})', 'SetTransporteEnginSelect', EAX=0, EDX=s13),
                    cct.chamada('tag 8 depot tuple (2, cave, 1)', 'SetDepotEnginSelect', EAX=0, EDX=2, EBX=cave, ECX=1)])
            c12 = c.u16(registro(c, 12) + 8)
            estado.chao = c12
            tipo12 = 2 if sacos(c, 2) else 1
            s12 = mais_proximo(c, c12, tipo12)
            if s12 is not None:
                yield from ordem(c, k, 12, f'tag 8 sack {s12} kind {tipo12}, Ctrl ground depot (1, {c12})', [
                    cct.chamada(f'tag 8: SetTransporteEnginSelect(0, {s12})', 'SetTransporteEnginSelect', EAX=0, EDX=s12),
                    cct.chamada(f'tag 8 depot tuple (1, {c12}, {tipo12})', 'SetDepotEnginSelect', EAX=0, EDX=1,
                                EBX=c12, ECX=tipo12)])
            yield from ordem(c, k, 14, 'tag 19 cave, Ctrl depot (2, sanctuary, food)', [
                cct.chamada('tag 19: SetDechargeCaveEnginSelect(0, cave)', 'SetDechargeCaveEnginSelect', EAX=0,
                            EDX=cave, EBX=0),
                cct.chamada('tag 19 depot tuple (2, 0, 1)', 'SetDepotEnginSelect', EAX=0, EDX=2, EBX=0, ECX=1)])
        if k == QUADRO_CASOS:
            cel0 = estado.sanctuary_cell
            for rotulo, u, rotina, valores, outras in (casos_descarga(c, estado, cel0) + casos_transporte(c, estado, cel0)
                                                       + casos_fome(c, estado)):
                estado.pendentes.append(dict(kind='case', label=f'{rotina} unit {u}, {rotulo}', steps=outras + campos(
                    c, u, rotulo, valores) + [cct.chamada(f'{rotina}({u})', rotina, EAX=u)]))
            estado.cases_planned = len(estado.pendentes)
        # The cases are built from frame QUADRO_CASOS's state and run CASOS_POR_QUADRO per frame (each declares the
        # fields its branch reads); the bench's per-phase wall budget bounds one frame's declared work.
        for caso in estado.pendentes[:CASOS_POR_QUADRO]:
            estado.cases += 1
            if getattr(c, 'progresso_casos', False):
                print(f'case {estado.cases} frame {k}: {caso["label"]}', flush=True)
            yield caso
        del estado.pendentes[:CASOS_POR_QUADRO]
        for i in (12, 13):
            pi = registro(c, i)
            if estado.fome is None and k >= QUADRO_FOME and c.u8(pi + 2) == 0x12:
                estado.fome = dict(frame=k, unit=i)
                yield cct.escrita(f'unit {i} provisions +4 := 1', pi + 4, _u16(1))
                yield cct.escrita(f'unit {i} fatigue counter +0x74 := 0xfffe', pi + 0x74, _u16(0xfffe))
        if k == QUADRO_SEGUNDAS:
            cel0 = estado.sanctuary_cell
            yield from ordem(c, k, 14, f'tag 19 cave, Ctrl ground depot (1, {cel0}, food)', [
                cct.chamada('tag 19: SetDechargeCaveEnginSelect(0, cave)', 'SetDechargeCaveEnginSelect', EAX=0,
                            EDX=cave, EBX=0),
                cct.chamada(f'tag 19 depot tuple (1, {cel0}, 1)', 'SetDepotEnginSelect', EAX=0, EDX=1, EBX=cel0, ECX=1)])
            c13 = c.u16(registro(c, 13) + 8)
            s13 = mais_proximo(c, c13, 1)
            if s13 is not None:
                yield from ordem(c, k, 13, f'plain tag 8 sack {s13}, depot (0, 0, 0)', [
                    cct.chamada(f'tag 8: SetTransporteEnginSelect(0, {s13})', 'SetTransporteEnginSelect', EAX=0, EDX=s13),
                    cct.chamada('tag 8 depot tuple (0, 0, 0)', 'SetDepotEnginSelect', EAX=0, EDX=0, EBX=0, ECX=0)])
    return gerar


def escolher(estado):
    def f(nome, regs, c):
        if c.acao_atual is not None:
            return nome in ROTINAS or nome == 'EnginNextEtape:19'
        if nome == 'EnginNextEtape:19':
            return c.u16((regs['ESI'] + 0xa0) & 0xffffffff) in VERIFICADOS
        if nome not in ROTINAS:
            return False
        i = regs['EAX'] & 0xffff
        p = registro(c, i)
        if c.k - estado.ultima.get(i, -100) <= 3 or c.k % 25 == 0:
            return True
        fase, tempo = c.u8(p + 0x89), c.u8(p + 0x8b)
        veiculo = 0xb <= c.u8(p + 1) <= 0x11 and c.u8(p + 0x82) != 1
        temporizadas = (1, 4) if veiculo else (1, 3)
        if fase in temporizadas:
            return tempo <= 1
        return distancia(c.u16(p + 8), c.u16(p + 0x7e)) <= 2 or fase > (4 if veiculo else 3)
    return f


def unidade(c, i):
    u = cal.unidade(c, i)
    p = registro(c, i)
    u.update(f86=c.u8(p + 0x86), f87=c.u8(p + 0x87), f90=c.u8(p + 0x90), f91=c.u8(p + 0x91), a4=c.u8(p + 0xa4),
             counter66=c.u16(p + 0x70), b7=c.u8(p + 0xb7), b8=c.u16(p + 0xb8))
    return u


def amostra(estado):
    def f(c):
        r = dict(units={i: unidade(c, i) for i in (12, 13, 14)}, resources_p0=c.ler(cct.RECURSOS, 32).hex(),
                 cave_words_p0=c.ler(cct.CAVES, 6).hex(), structures={0: cct.estrutura(c, 0)})
        if estado.cave is not None:
            r['structures'][estado.cave] = cct.estrutura(c, estado.cave)
        return r
    return f


def executar(ate, observador=None, progresso=None):
    from bancada_ciclo_trabalho import Ciclo
    estado = Estado()
    c = Ciclo(ROTINAS, escolher(estado), ordens(estado), observador=observador, amostra=amostra(estado),
              pseudo=cal.PSEUDO, gravar_acoes=True)
    c.progresso_casos = progresso is not None
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
        schema='rising-lands/economy-transport-capture/1', original_sha256=HASH_ORIGINAL, translation_executed=False,
        scenario='exibicao', source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        reference=dict(path=str(c.cap_caminho.relative_to(RAIZ)), sha256=hashlib.sha256(c.cap_caminho.read_bytes()).hexdigest()),
        inputs='display-reference named inputs; later frames keep the declared no-input answers; display clock '
               '0x123456+40*k (the reference rule, extended)',
        reproduction=c.reproducao, last_counter=a.ate, seconds=segundos, orders=estado.ordens,
        hunger_frame=estado.fome, sanctuary_cell=estado.sanctuary_cell, cases=estado.cases,
        cases_planned=estado.cases_planned, cases_pending=len(estado.pendentes),
        pseudo={hex(e): dict(name=n, exit=hex(s)) for e, (n, s) in cal.PSEUDO.items()},
        colonist=estado.colono, cave=estado.cave, routines=list(ROTINAS) + ['EnginNextEtape:19'],
        actions=c.acoes, frames=c.quadros, calls=c.registros)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9) if saida.suffix == '.xz' else bruto)
    from collections import Counter
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(), seconds=segundos,
                          reproduction=c.reproducao, calls=dict(Counter(r['routine'] for r in c.registros)),
                          actions=len(c.acoes), cases=estado.cases, hunger=estado.fome, orders=estado.ordens),
                     indent=1), flush=True)
    encerrar_captura(0, saida)


if __name__ == '__main__':
    main()
