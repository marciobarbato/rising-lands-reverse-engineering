"""Original-only capture of the hunger state's exits: EnginRestaureEtat, BatimentEnleveMatiere, the cave meal and the
"nothing found" branches of state 19, and SetDechargeCaveEnginSelect (tag 19), M3 S1.

Why. The S1 victory route enters EnginRestaureEtat 0x45315f (its only caller is the state-19 body, 0x45566a) with
saved state 5 at frame 8057; eating at a cave removes one food from the totals through BatimentEnleveMatiere
0x4235bd; ai-runtime and the Rust engine stop at SetDechargeCaveEnginSelect 0x473194 (ProcessInputGame tag 19,
0x45f085).

Bench: ``bancada_ciclo_trabalho.Ciclo`` with ``gravar_acoes`` (MONDE01 display reference; frames 0/1 reproduced; then
real frames with the reference's no-input answers), driven by the committed hunger scenario
(``capturar_alimentacao.ordens``: the work cycle plus the declared hunger of unit 12 at frame 1100 and unit 14 at
1150). No Python translation is imported.

Declared additions, all at CalculGame entries:
1. Frame 1150, before unit 14's declared hunger: every food sack on the map is removed (declared writes: object byte
   0x43 of grid [0x507d74] := 0 and its quantity byte of grid [0x507dac] := 0). Unit 12, already walking to a sack,
   finds none on arrival (state 19's "nothing found": ChercheVegetLibre again, none, EnginRestaureEtat); unit 14's
   EnginSetFatigue finds no sack and picks the own cave (food >= 3): the cave meal, BatimentEnleveMatiere(food, 1).
2. Restored cases (the whole state put back after each) while unit 12 or 14 walks to the cave (state 19, food
   structure +0xc2 set, within 2 cells of its destination +0x7e; at most ``CASOS_CAVE`` per unit): the player-0
   food words := 0, then the original EnginNextEtape(unit): at the cave TestRessource fails and the "nothing found"
   branch runs from the cave.
3. Frame ``QUADRO_CASOS`` restored cases: EnginRestaureEtat(unit) with declared saved states +0xa0 (every switch
   target, with declared types +1, targets +0xb7/+0xb8/+0xc0/+0xbe/+0xb2 and the path-search owner 0x496304 where a
   branch reads them); BatimentEnleveMatiere with declared AL/DX/BL; SetDechargeCaveEnginSelect(AL, DX = the cave)
   with declared player-0 selection lists.
4. The first frame at or after ``QUADRO_DESCARGA`` with unit 14 working (state 5, provisions refilled): the player-0
   selection := [14], then tag 19 as ProcessInputGame applies it: SetDechargeCaveEnginSelect(0, cave) and
   SetDepotEnginSelect(0, 2, cave, 1) (declared depot tuple). ``ATRASO_FOME`` frames later, with unit 14 in state 20,
   its declared hunger (provisions +4 := 1, fatigue +0x74 := 0xfffe): saved state 0x14 reaches EnginRestaureEtat
   from the real call site.

Recorded calls (``Ciclo`` isolation, also inside declared calls), by ``--modo``:
- ``rotinas``: every EnginRestaureEtat, BatimentEnleveMatiere and SetDechargeCaveEnginSelect not nested in another
  recorded call (the state-19 body is not recorded, so the real call sites 0x45566a / 0x4556d7 are recorded);
- ``corpo``: the same plus the state-19 body ``EnginNextEtape:19`` of every unit (entry 0x4554db, exit 0x454ccd);
  the bodies then hold EnginRestaureEtat / BatimentEnleveMatiere as nested calls.
The two modes run the same declared actions; the timeline is identical. Per frame: units 12/14/colonist with their
hunger fields, player-0 resources, the cave-count words, structures 0 and the cave.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/capturar_restauracao.py \\
        --modo rotinas --ate 2000 \\
        --saida pesquisas-paralelas/economia/evidencias/restauracao/captura-restauracao-rotinas.json.xz
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

FONTES = cal.FONTES + ('pesquisas-paralelas/economia/capturar_restauracao.py',)
ROTINAS = ('EnginRestaureEtat', 'BatimentEnleveMatiere', 'SetDechargeCaveEnginSelect')
GRADE_OBJETOS, GRADE_QUANTIDADES = 0x507d74, 0x507dac
BUSCA_UNIDADE = 0x496304
SACO_COMIDA = 0x43
QUADRO_LIMPEZA = 1150
QUADRO_CASOS = 1420
QUADRO_DESCARGA = 1500
ATRASO_FOME = 20
CASOS_CAVE = 6
COMIDA_P0 = cct.RECURSOS + 8          # player 0, resource 1 (food): u16 +0, u16 total +2


def _u16(v):
    return struct.pack('<H', v & 0xffff)


def registro(c, i):
    return c.u32(cct.UNIDADES_PTR) + cct.PASSO * i


def campos(c, i, rotulo, valores):
    """Declared writes into unit ``i``'s record: {offset: (size, value)}."""
    p = registro(c, i)
    return [cct.escrita(f'{rotulo}: unit {i} +{o:#x} := {v:#x}', p + o, v.to_bytes(n, 'little'))
            for o, (n, v) in sorted(valores.items())]


def casos_restauracao(c, cave):
    """EnginRestaureEtat restored cases: (label, unit, record writes, other writes)."""
    u14, u12 = 14, 12
    cel14 = c.u16(registro(c, u14) + 8)
    s = []
    for v in (0, 2, 3, 4, 5, 6, 7, 8, 9, 0xa, 0xb, 0xc, 0xe, 0xf, 0x10, 0x11, 0x12, 0x13, 0x15, 0x16, 0x17, 0x19,
              0x30):
        s.append((f'saved state {v:#x}', u14, {0xa0: (2, v)}, []))
    s += [
        ('saved state 1 (attack a cell)', u14, {0xa0: (2, 1), 0xb7: (1, 5), 0xb8: (2, cel14 + 1)}, []),
        ('saved state 0xd, structure', u14, {0xa0: (2, 0xd), 0xc0: (2, cave)}, []),
        ('saved state 0xd, no target', u14, {0xa0: (2, 0xd), 0xc0: (2, 0xffff), 0xb8: (2, 0xffff)}, []),
        ('saved state 0xd, follow unit 12', u14, {0xa0: (2, 0xd), 0xc0: (2, 0xffff), 0xb8: (2, u12)}, []),
        ('saved state 0x14, the cave', u14, {0xa0: (2, 0x14), 0xc0: (2, cave)}, []),
        ('saved state 5, builder', u12, {0xa0: (2, 5)}, []),
        ('saved state 5, declared builder', u14, {0xa0: (2, 5), 1: (1, 7)}, []),
        ('saved state 0xb, builder, structure', u12, {0xa0: (2, 0xb), 0xc0: (2, cave)}, []),
        ('saved state 0xf, builder, structure', u12, {0xa0: (2, 0xf), 0xc0: (2, 0)}, []),
        ('saved state 0xf, builder, new cave', u12, {0xa0: (2, 0xf), 0xc0: (2, 0xffff), 0xbe: (1, 3),
                                                       0xb2: (2, cct.celula(30, 20))}, []),
        ('saved state 0xb, builder, new type 1', u12, {0xa0: (2, 0xb), 0xc0: (2, 0xffff), 0xbe: (1, 1),
                                                         0xb2: (2, cct.celula(31, 24))}, []),
        ('saved state 0xf, type 6, unit 12', u14, {0xa0: (2, 0xf), 1: (1, 6), 0xc0: (2, u12)}, []),
        ('saved state 0xb, type 6, unit 12', u14, {0xa0: (2, 0xb), 1: (1, 6), 0xc0: (2, u12)}, []),
        ('saved state 0x18, type 4, unit 12', u14, {0xa0: (2, 0x18), 1: (1, 4), 0xb7: (1, 1), 0xb8: (2, u12),
                                                      0xf4: (1, 0x5a)}, []),
        ('saved state 0x18, type 4, itself', u14, {0xa0: (2, 0x18), 1: (1, 4), 0xb7: (1, 1), 0xb8: (2, u14)}, []),
        ('saved state 0x18, type 4, mode 5', u14, {0xa0: (2, 0x18), 1: (1, 4), 0xb7: (1, 5), 0xb8: (2, cel14)}, []),
        ('saved state 0x18, type 4, mode 3', u14, {0xa0: (2, 0x18), 1: (1, 4), 0xb7: (1, 3), 0xb8: (2, cave)}, []),
        ('saved state 0x18, type 4, mode 0', u14, {0xa0: (2, 0x18), 1: (1, 4), 0xb7: (1, 0), 0xb8: (2, u12)}, []),
        ('saved state 0x18, type 5', u14, {0xa0: (2, 0x18), 0xb7: (1, 1), 0xb8: (2, u12)}, []),
    ]
    busca = [cct.escrita('path-search owner 0x496304 := 14', BUSCA_UNIDADE, _u16(u14))]
    for v, extra in ((2, {}), (5, {}), (0x10, {}), (0x12, {}), (0x14, {0xc0: (2, cave)}),
                     (0xd, {0xc0: (2, 0xffff), 0xb8: (2, u12)}), (0xf, {1: (1, 6), 0xc0: (2, u12)}),
                     (5, {1: (1, 7)}), (0xb, {1: (1, 7), 0xc0: (2, cave)})):
        s.append((f'saved state {v:#x} {sorted(extra)} owning the path search', u14, dict({0xa0: (2, v)}, **extra), busca))
    return s


def casos_matiere():
    """BatimentEnleveMatiere restored cases: (AL resource, DX quantity, BL player) with upper bits."""
    return ((1, 1, 0), (2, 3, 0), (0, 2, 0), (3, 1, 0), (1, 0, 0), (1, 500, 0), (2, 0xffff, 0), (1, 1, 1),
            (1, 1, 2), (2, 1, 3), (0xabcd0101, 0x12340002, 0x77665500))


def casos_selecao():
    """SetDechargeCaveEnginSelect restored cases: (label, player AL, player-0 selection list or None)."""
    return (('selection [14]', 0, [14]), ('selection [12, 14]', 0, [12, 14]), ('selection [14, 12]', 0, [14, 12]),
            ('selection [20, 14] (slot 20 not alive)', 0, [20, 14]), ('empty selection', 0, []),
            ('player 1 (not local)', 1, None))


class Estado(cct.Estado):
    def __init__(self, modo):
        super().__init__()
        self.modo = modo
        self.sacos = []
        self.casos_cave = {}
        self.descarga = None
        self.fome_descarga = None


def sacos_comida(c):
    objetos = c.ler(c.u32(GRADE_OBJETOS), 0x10000)
    return [i for i, b in enumerate(objetos) if b == SACO_COMIDA]


def ordens(estado):
    base = cal.ordens(estado)

    def gerar(c, k):
        if k == QUADRO_LIMPEZA and 'sacks' not in estado.feito:
            estado.feito.add('sacks')
            po, pq = c.u32(GRADE_OBJETOS), c.u32(GRADE_QUANTIDADES)
            estado.sacos = [dict(cell=i, quantity=c.u8(pq + i)) for i in sacos_comida(c)]
            for s in estado.sacos:
                yield cct.escrita(f'food sack at cell {s["cell"]}: object := 0', po + s['cell'], [0])
                yield cct.escrita(f'food sack at cell {s["cell"]}: quantity := 0', pq + s['cell'], [0])
        yield from base(c, k)
        cave = estado.cave
        for i in (12, 14):
            p = registro(c, i)
            if c.u8(p + 2) != 0x13 or c.u16(p + 0xc2) == 0xffff or estado.casos_cave.get(i, 0) >= CASOS_CAVE:
                continue
            cel, dest = c.u16(p + 8), c.u16(p + 0x7e)
            if max(abs((cel & 0xff) - (dest & 0xff)), abs((cel >> 8) - (dest >> 8))) > 2:
                continue
            estado.casos_cave[i] = estado.casos_cave.get(i, 0) + 1
            yield dict(kind='case', label=f'unit {i} at the cave with no food: EnginNextEtape', steps=[
                cct.escrita('player-0 food words := 0', COMIDA_P0, bytes(4)),
                cct.chamada(f'EnginNextEtape({i})', 'EnginNextEtape', EAX=i)])
        if k == QUADRO_CASOS:
            for rotulo, u, valores, outras in casos_restauracao(c, cave):
                yield dict(kind='case', label=f'EnginRestaureEtat unit {u}, {rotulo}', steps=outras + campos(
                    c, u, rotulo, valores) + [cct.chamada(f'EnginRestaureEtat({u})', 'EnginRestaureEtat', EAX=u)])
            for al, dx, bl in casos_matiere():
                yield dict(kind='case', label=f'BatimentEnleveMatiere({al:#x}, {dx:#x}, {bl:#x})', steps=[
                    cct.chamada('BatimentEnleveMatiere', 'BatimentEnleveMatiere', EAX=al, EDX=dx, EBX=bl, ECX=0)])
            for rotulo, jogador, sel in casos_selecao():
                passos = [] if sel is None else [cct.selecao(sel)]
                passos.append(cct.chamada(f'SetDechargeCaveEnginSelect({jogador}, cave {cave})',
                                          'SetDechargeCaveEnginSelect', EAX=jogador, EDX=cave, EBX=jogador << 2))
                yield dict(kind='case', label=f'tag 19, {rotulo}', steps=passos)
        p14 = registro(c, 14)
        if estado.descarga is None and k >= QUADRO_DESCARGA and c.u8(p14 + 2) == 5 and c.u16(p14 + 4):
            estado.descarga = k
            yield cct.selecao([14])
            yield cct.chamada('tag 19: SetDechargeCaveEnginSelect(0, cave)', 'SetDechargeCaveEnginSelect',
                              EAX=0, EDX=cave, EBX=0)
            yield cct.chamada('tag 19 depot tuple (2, cave, 1)', 'SetDepotEnginSelect', EAX=0, EDX=2, EBX=cave, ECX=1)
        if (estado.descarga is not None and estado.fome_descarga is None and k >= estado.descarga + ATRASO_FOME
                and c.u8(p14 + 2) == 0x14):
            estado.fome_descarga = k
            yield cct.escrita('unit 14 provisions +4 := 1', p14 + 4, _u16(1))
            yield cct.escrita('unit 14 fatigue counter +0x74 := 0xfffe', p14 + 0x74, _u16(0xfffe))
    return gerar


def escolher(estado):
    def f(nome, regs, c):
        if nome == 'EnginNextEtape:19':
            return estado.modo == 'corpo'
        return nome in ROTINAS
    return f


def amostra(estado):
    def f(c):
        r = dict(units={i: cal.unidade(c, i) for i in (12, 14) + ((estado.colono,) if estado.colono is not None else ())},
                 resources_p0=c.ler(cct.RECURSOS, 32).hex(), cave_words_p0=c.ler(cct.CAVES, 6).hex(),
                 structures={0: cct.estrutura(c, 0)})
        if estado.cave is not None:
            r['structures'][estado.cave] = cct.estrutura(c, estado.cave)
        return r
    return f


def executar(ate, modo, observador=None, progresso=None):
    from bancada_ciclo_trabalho import Ciclo
    estado = Estado(modo)
    c = Ciclo(ROTINAS, escolher(estado), ordens(estado), observador=observador, amostra=amostra(estado),
              pseudo=cal.PSEUDO, gravar_acoes=True)
    segundos = c.executar(ate, progresso)
    return c, estado, segundos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ate', type=int, required=True, help='last frame counter 0x508f7c')
    ap.add_argument('--modo', choices=('rotinas', 'corpo'), required=True)
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

    c, estado, segundos = executar(a.ate, a.modo, progresso=progresso)
    dados = dict(
        schema='rising-lands/economy-restore-capture/1', original_sha256=HASH_ORIGINAL, translation_executed=False,
        scenario='exibicao', mode=a.modo, source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        reference=dict(path=str(c.cap_caminho.relative_to(RAIZ)), sha256=hashlib.sha256(c.cap_caminho.read_bytes()).hexdigest()),
        inputs='display-reference named inputs; later frames keep the declared no-input answers; display clock '
               '0x123456+40*k (the reference rule, extended)',
        reproduction=c.reproducao, last_counter=a.ate, seconds=segundos, hunger=cal.FOME,
        sacks_removed=estado.sacos, cave_cases=estado.casos_cave, unload_frame=estado.descarga,
        unload_hunger_frame=estado.fome_descarga,
        pseudo={hex(e): dict(name=n, exit=hex(s)) for e, (n, s) in cal.PSEUDO.items()},
        colonist=estado.colono, cave=estado.cave, routines=list(ROTINAS) + ['EnginNextEtape:19'],
        actions=c.acoes, frames=c.quadros, calls=c.registros)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9) if saida.suffix == '.xz' else bruto)
    from collections import Counter
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(), seconds=segundos,
                          reproduction=c.reproducao, calls=dict(Counter(r['routine'] for r in c.registros)),
                          actions=len(c.acoes), sacks=len(estado.sacos), unload=estado.descarga,
                          unload_hunger=estado.fome_descarga), indent=1), flush=True)
    encerrar_captura(0, saida)


if __name__ == '__main__':
    main()
