"""Original-only capture of the work, deposit and lodging cycles that move goods to the player totals.

Bench: ``bancada_ciclo_trabalho.Ciclo`` (MONDE01 display reference; frames 0/1 reproduced; then real
frames with the reference's no-input answers). No Python translation is imported.

Declared actions at frame 2's CalculGame entry, all by ORIGINAL routines called natively, unless a
write is named:
1. DecouvreTerrain(field (26,32), radius 3, player 0) and DecouvreTerrain(mine 0 (43,8), 3, 0): the
   targets discovered by the original discovery routine.
2. CreerBatiment(cell (23,14), type 3 CAVE, player 0): the click (21,12) of M3_ALVOS plus offset 0x202.
3. Cave completion: declared write of the cave's progress word +0xa := target - 2, then the original
   BatimentConstruction(cave) once, which adds 2 and completes it (+5 = 5, BatimentModifyMap).
4. Orders as ProcessInputGame applies them (setter pairs of tags 6/7; depot tuple from the packet):
   - unit 13 (type 5): SetRecolteEngin(13, (26,32)) + SetDepotEngin(13, 0, 0, 0)   (plain tag 7)
   - unit 14 (type 5): SetRecolteEngin(14, (27,32)) + SetDepotEngin(14, 2, 0, 1)   (Ctrl tag 7, depot = structure 0)
   - unit 12 (type 7): SetMineEngin(12, (43,8))   + SetDepotEngin(12, 2, 0, 2)   (Ctrl tag 6, depot = structure 0)
5. BatimentRetireColon(0) (tag 33: double-click on the selected sanctuary) releases a colonist.
6. Restored probes (state put back after each): EnginSelectPeutEntrer(AL=0, DL=3, BX=structure) with
   the player-0 selection list declared as [13] or [colonist], on the sanctuary and on the 0xc8 cave
   (and on the cave declared owned by player 0); BatimentConstruit on both.
Conditional actions at later CalculGame entries (first frame the condition holds):
7. colonist idle (state 0/7): SetEnginRentreBatiment(colonist, cave, BL = 9)  (tag 0x10 sub 3)
8. unit 13 idle (state 7) with a carried entry: SetEnginRentreBatiment(13, 0, BL = 5)  (tag 0x10 on the sanctuary)

Recorded calls (``Ciclo`` isolation): every BatimentLogeEngin, BatimentAjouteMatiere, InitBatimentPlayer,
TerrainRecolte, MineRecolte, MineSetWork, MineEndWork call that is not nested in another recorded call;
CalculWorkEngin of units 12/13/14 when its timer is about to expire (type 5 phases 1/3, type 7 phases 1/4),
in the builder's mine-exit and return phases (7: 2/5), or otherwise within 3 cells of its destination;
CalculEntreBatiment of units 13/colonist within 3 cells of their destination; and both every 50th frame. Per frame: units 12/13/14/colonist,
player-0 resources, the cave-count words, structures 0 and 1.

    python3 -B pesquisas-paralelas/economia/capturar_ciclo_trabalho.py --ate 1600 \
        --saida pesquisas-paralelas/economia/evidencias/ciclo-trabalho/captura-ciclo-trabalho-exibicao.json.xz
"""
import argparse
import hashlib
import json
import lzma
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

FONTES = ('pesquisas-paralelas/economia/capturar_ciclo_trabalho.py',
          'pesquisas-paralelas/economia/bancada_ciclo_trabalho.py',
          'pesquisas-paralelas/economia/bancada_ordens_economia.py',
          'ferramentas/bancada_selecao_ordens.py', 'ferramentas/percurso_quadro1.py',
          'pesquisas-paralelas/missoes/oraculo_quadro_missao.py', 'pesquisas-paralelas/missoes/oraculo_exibicao_missao.py')
UNIDADES_PTR, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
RECURSOS, CAVES = 0x4e2ea8, 0x4dfb2c
SELECAO = 0x508728
TIPOS = 0x495d8c


def celula(x, y):
    return y * 256 + x


CAMPO, CAMPO2, MINA, CAVE_CLIQUE = celula(26, 32), celula(27, 32), celula(43, 8), celula(23, 14)
SEMPRE = ('BatimentLogeEngin', 'BatimentAjouteMatiere', 'InitBatimentPlayer', 'TerrainRecolte', 'MineRecolte',
          'MineSetWork', 'MineEndWork')
ROTINAS = SEMPRE + ('CalculWorkEngin', 'CalculEntreBatiment')


class Estado:
    def __init__(self):
        self.colono = None
        self.cave = None
        self.feito = set()


def unidade(c, i):
    p = c.u32(UNIDADES_PTR) + PASSO * i
    bag = p + 0xa
    n = c.u16(bag)
    return dict(owner=c.u8(p), type=c.u8(p + 1), state=c.u8(p + 2), cell=c.u16(p + 8), dest=c.u16(p + 0x7e),
                depot_target=c.u16(p + 0x80), depot_mode=c.u8(p + 0x82), depot_kind=c.u16(p + 0x84),
                phase=c.u8(p + 0x89), timer=c.u8(p + 0x8b), b2=c.u16(p + 0xb2), c0=c.u16(p + 0xc0),
                bag_count=n, bag_capacity=c.u16(bag + 2), bag_counter=c.u16(bag + 0x66),
                bag=[[c.u8(bag + 0x42 + j), c.u16(bag + 6 + 2 * j)] for j in range(min(n, 30))])


def estrutura(c, i):
    p = ESTRUTURAS + PASSO * i
    bag = p + 0xc
    n = c.u16(bag)
    return dict(owner=c.u8(p + 4), exists=c.u8(p + 5), type=c.u8(p + 8), progress=c.u16(p + 0xa), origin=c.u16(p + 2),
                bag_count=n, bag=[[c.u8(bag + 0x42 + j), c.u16(bag + 6 + 2 * j)] for j in range(min(n, 30))])


def colonos_no_santuario(c):
    pool = c.u32(UNIDADES_PTR)
    return [v for t, v in estrutura(c, 0)['bag'] if t == 1 and c.u8(pool + PASSO * v + 1) == 9]


def chamada(rotulo, rotina, **regs):
    return dict(kind='call', label=rotulo, routine=rotina, registers=regs)


def escrita(rotulo, endereco, dados):
    return dict(kind='write', label=rotulo, address=endereco, bytes=bytes(dados))


def selecao(unidades):
    return escrita(f'player-0 selection = {list(unidades)}', SELECAO,
                   struct.pack(f'<H{len(unidades)}H', len(unidades), *unidades))


def ordens(estado):
    def gerar(c, k):
        if k == 2:
            yield chamada('discover field (26,32)', 'DecouvreTerrain', EAX=CAMPO, EDX=3, EBX=0)
            yield chamada('discover mine 0 (43,8)', 'DecouvreTerrain', EAX=MINA, EDX=3, EBX=0)
            r = c._acao(k, chamada('CreerBatiment cave (23,14) player 0', 'CreerBatiment', EAX=CAVE_CLIQUE, EDX=3, EBX=0))
            estado.cave = int(c.acoes[-1]['exit_registers']['EAX'], 16) & 0xffff
            if estado.cave == 0xffff:
                raise RuntimeError('CreerBatiment refused the declared cave')
            alvo = c.u16(TIPOS + 52 * 3 + 4)
            yield escrita(f'cave {estado.cave} progress +0xa := {alvo - 2} (target {alvo} - 2)',
                          ESTRUTURAS + PASSO * estado.cave + 0xa, struct.pack('<H', alvo - 2))
            yield chamada('BatimentConstruction(cave) completes it', 'BatimentConstruction', EAX=estado.cave)
            yield chamada('unit 13 tag 7: SetRecolteEngin', 'SetRecolteEngin', EAX=13, EDX=CAMPO)
            yield chamada('unit 13 tag 7 depot tuple (0,0,0)', 'SetDepotEngin', EAX=13, EDX=0, EBX=0, ECX=0)
            yield chamada('unit 14 tag 7: SetRecolteEngin', 'SetRecolteEngin', EAX=14, EDX=CAMPO2)
            yield chamada('unit 14 Ctrl tag 7 depot tuple (2, structure 0, food)', 'SetDepotEngin', EAX=14, EDX=2, EBX=0, ECX=1)
            yield chamada('unit 12 tag 6: SetMineEngin', 'SetMineEngin', EAX=12, EDX=MINA)
            yield chamada('unit 12 Ctrl tag 6 depot tuple (2, structure 0, stone)', 'SetDepotEngin', EAX=12, EDX=2, EBX=0, ECX=2)
            antes = colonos_no_santuario(c)
            yield chamada('tag 33: BatimentRetireColon(sanctuary)', 'BatimentRetireColon', EAX=0)
            saiu = [v for v in antes if v not in colonos_no_santuario(c)]
            if len(saiu) != 1:
                raise RuntimeError(f'BatimentRetireColon released {saiu} (sanctuary colonists before: {antes})')
            estado.colono = saiu[0]
            cave = estado.cave
            for sel, alvo_b, dono in (([13], 0, None), ([13], cave, None), ([estado.colono], cave, None),
                                      ([13], cave, 0), ([estado.colono], 0, None)):
                passos = [selecao(sel)]
                if dono is not None:
                    passos.append(escrita(f'cave owner := {dono}', ESTRUTURAS + PASSO * cave + 4, [dono]))
                passos += [chamada(f'EnginSelectPeutEntrer(0, 3, {alvo_b})', 'EnginSelectPeutEntrer', EAX=0, EDX=3, EBX=alvo_b),
                           chamada(f'BatimentConstruit({alvo_b})', 'BatimentConstruit', EAX=alvo_b)]
                yield dict(kind='case', label=f'selection {sel} enters structure {alvo_b}'
                           + ('' if dono is None else f' (owner declared {dono})'), steps=passos)
            return
        if estado.colono is not None and 'colono' not in estado.feito and unidade(c, estado.colono)['state'] in (0, 7):
            estado.feito.add('colono')
            yield chamada('tag 0x10: SetEnginRentreBatiment(colonist, cave)', 'SetEnginRentreBatiment',
                          EAX=estado.colono, EDX=estado.cave, EBX=9)
        u = unidade(c, 13)
        if 'u13' not in estado.feito and u['state'] == 7 and u['bag_count']:
            estado.feito.add('u13')
            yield chamada('tag 0x10: SetEnginRentreBatiment(13, sanctuary)', 'SetEnginRentreBatiment', EAX=13, EDX=0, EBX=5)
    return gerar


def escolher(estado):
    def f(nome, regs, c):
        if nome in SEMPRE:
            return True
        i = regs['EAX'] & 0xffff
        if nome == 'CalculWorkEngin' and i not in (12, 13, 14):
            return False
        if nome == 'CalculEntreBatiment' and i not in (13, estado.colono):
            return False
        if c.k % 50 == 0:
            return True
        u = unidade(c, i)
        perto = max(abs((u['cell'] & 0xff) - (u['dest'] & 0xff)), abs((u['cell'] >> 8) - (u['dest'] >> 8))) <= 3
        if nome == 'CalculEntreBatiment':
            return perto
        temporizada = (u['type'], u['phase']) in ((5, 1), (5, 3), (7, 1), (7, 4))
        if temporizada:
            return u['timer'] <= 1
        return perto or (u['type'], u['phase']) in ((7, 2), (7, 5))
    return f


def amostra(estado):
    def f(c):
        r = dict(units={i: unidade(c, i) for i in (12, 13, 14) + ((estado.colono,) if estado.colono is not None else ())},
                 resources_p0=c.ler(RECURSOS, 32).hex(), cave_words_p0=c.ler(CAVES, 6).hex(),
                 structures={0: estrutura(c, 0)})
        if estado.cave is not None:
            r['structures'][estado.cave] = estrutura(c, estado.cave)
        return r
    return f


def executar(ate, observador=None, progresso=None):
    from bancada_ciclo_trabalho import Ciclo
    estado = Estado()
    c = Ciclo(ROTINAS, escolher(estado), ordens(estado), observador=observador, amostra=amostra(estado))
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
        schema='rising-lands/economy-work-cycle-capture/1', original_sha256=HASH_ORIGINAL, translation_executed=False,
        scenario='exibicao', source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        reference=dict(path=str(c.cap_caminho.relative_to(RAIZ)), sha256=hashlib.sha256(c.cap_caminho.read_bytes()).hexdigest()),
        inputs='display-reference named inputs; later frames keep the declared no-input answers; display clock '
               '0x123456+40*k (the reference rule, extended)',
        reproduction=c.reproducao, last_counter=a.ate, seconds=segundos,
        colonist=estado.colono, cave=estado.cave, routines=list(ROTINAS), always_recorded=list(SEMPRE),
        actions=c.acoes, frames=c.quadros, calls=c.registros)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9) if saida.suffix == '.xz' else bruto)
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(), seconds=segundos,
                          reproduction=c.reproducao, calls=len(c.registros), actions=len(c.acoes),
                          colonist=estado.colono, cave=estado.cave), indent=1), flush=True)
    encerrar_captura(0, saida)


if __name__ == '__main__':
    main()
