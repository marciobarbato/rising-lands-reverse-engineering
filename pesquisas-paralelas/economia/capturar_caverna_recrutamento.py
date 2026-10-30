"""Original-only capture of the cave structure body, cave habitation and sanctuary recruitment in MONDE01.

Bench: ``bancada_ciclo_trabalho.Ciclo`` with ``gravar_acoes`` (MONDE01 display reference; frames 0/1 reproduced;
then real frames with the reference's no-input answers). No Python translation is imported.

Declared actions at CalculGame entries, all by ORIGINAL routines called natively, unless a write is named:
1. frame 2: CreerBatiment(cell (23,14), type 3 CAVE, player 0) (M3_ALVOS click (21,12) + 0x202, as P3), and
   BatimentRetireColon(sanctuary) (tag 33) releases a colonist.
2. frame 12: declared write of the cave's progress word +0xa := target - 2, then BatimentConstruction(cave) once
   (+5 = 5). Frames 2..11 run the cave body under construction (owner 0xc8), as P3's frame 220.
3. first frame with the colonist idle: SetEnginRentreBatiment(colonist, cave, BL = 9) (tag 0x10 sub 3, P6).
   The colonist walks in and lodges natively (BatimentLogeEngin -> BatimentHabitable -> InitBatimentPlayer).
4. frame 30: BatimentSelection(sanctuary) (the press that selects it, 0x495be0[0] = 0), then
   InitRecruteTroupe(AL = 5, DL = 0) (tag 17, icon slot 0). Frame 40: InitRecruteTroupe(7, 0) while that request
   is pending (P6: charges nothing).
5. each later frame where the sanctuary has no pending request (+0x74 = 0) after a completion: the next request
   of the plan [7 (slot 2), 6 (slot 1), 5 (slot 0), 5] (the last one finds 0 food).
6. restored cases (the whole state is put back after each):
   - frame 150 (cave inhabited): BatimentNextEtape(cave) with declared +0x75/+0x76 in (1,0) (1,14) (1,15)
     (0,5) (0,1) (0,0) and with the 0x508f80 bit 0 forced to 0 and 1; BatimentRetireColon(cave) (the colonist
     leaves: the cave is abandoned -> InitBatimentNeutre); BatimentHabitable / InitBatimentPlayer /
     InitBatimentNeutre on the sanctuary (type 2); InitBatimentPlayer on the cave once more.
   - frame 50 (request pending): InitRecruteTroupe for slots 5/6/7 with +0x74 := 0 declared; with the food
     total declared 3 (short); BatimentSelection(cave) then InitRecruteTroupe(5, 0) (a structure that does not
     recruit).

Recorded calls (``Ciclo`` isolation, also inside declared calls): every InitRecruteTroupe, BatimentLogeEngin,
BatimentHabitable, BatimentSetTechnologie, InitBatimentPlayer, InitBatimentNeutre; BatimentNextEtape of the cave
on frames 2..20, 118..135, every 20th frame and in the cases; CalculTroupe and SortieTroupe of the sanctuary in
the action frames, every 20th frame, and while a pending request is within 1,500 of its threshold.
Per frame: sanctuary and cave records, player-0 resources, cave-count words, the colonist and the recruits.

    python3 -B pesquisas-paralelas/economia/capturar_caverna_recrutamento.py --ate 1000 \\
        --saida pesquisas-paralelas/economia/evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz
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

FONTES = ('pesquisas-paralelas/economia/capturar_caverna_recrutamento.py',
          'pesquisas-paralelas/economia/bancada_ciclo_trabalho.py',
          'pesquisas-paralelas/economia/bancada_ordens_economia.py',
          'ferramentas/bancada_selecao_ordens.py', 'ferramentas/percurso_quadro1.py',
          'pesquisas-paralelas/missoes/oraculo_quadro_missao.py', 'pesquisas-paralelas/missoes/oraculo_exibicao_missao.py')
UNIDADES_PTR, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
RECURSOS, CAVES = 0x4e2ea8, 0x4dfb2c
TIPOS = 0x495d8c
TEMPOS = 0x4965ae            # u16 recruit time of each 50-byte unit-type record (EnginGetTimeRecrute)
SELECOES_ESTRUTURA = 0x495be0
ANIM = 0x508f80
SANTUARIO = 0


def celula(x, y):
    return y * 256 + x


CAVE_CLIQUE = celula(23, 14)
SEMPRE = ('InitRecruteTroupe', 'BatimentLogeEngin', 'BatimentHabitable', 'BatimentSetTechnologie',
          'InitBatimentPlayer', 'InitBatimentNeutre')
ROTINAS = SEMPRE + ('BatimentNextEtape', 'CalculTroupe', 'SortieTroupe')
PLANO = (7, 6, 5, 5)          # requests after the first (type 5) completes: icon slots 2, 1, 0, 0
QUADROS_ACOES = (2, 12, 30, 40, 50, 150)


class Estado:
    def __init__(self):
        self.colono = None
        self.cave = None
        self.feito = set()
        self.plano = list(PLANO)
        self.pendente = False
        self.quadros_acao = set(QUADROS_ACOES)
        self.recrutas = []


def unidade(c, i):
    p = c.u32(UNIDADES_PTR) + PASSO * i
    return dict(owner=c.u8(p), type=c.u8(p + 1), state=c.u8(p + 2), cell=c.u16(p + 8), dest=c.u16(p + 0x7e))


def estrutura(c, i):
    p = ESTRUTURAS + PASSO * i
    bag = p + 0xc
    n = c.u16(bag)
    return dict(owner=c.u8(p + 4), exists=c.u8(p + 5), type=c.u8(p + 8), progress=c.u16(p + 0xa), origin=c.u16(p + 2),
                pending=c.u8(p + 0x74), b75=c.u8(p + 0x75), b76=c.u8(p + 0x76), requested=c.u8(p + 0x7b),
                rally=c.u16(p + 0x7c), production=c.u32(p + 0x8c), bag_count=n,
                bag=[[c.u8(bag + 0x42 + j), c.u16(bag + 6 + 2 * j)] for j in range(min(n, 30))])


def colonos(c, s):
    pool = c.u32(UNIDADES_PTR)
    return [v for t, v in estrutura(c, s)['bag'] if t == 1 and c.u8(pool + PASSO * v + 1) == 9]


def limiar(c, s):
    """SortieTroupe's threshold: u16 time of the requested type (EnginGetTimeRecrute) * 100."""
    tipo = c.u8(ESTRUTURAS + PASSO * s + 0x7b)
    return c.u16(TEMPOS + 50 * tipo) * 100 if tipo < 26 else None


def chamada(rotulo, rotina, **regs):
    return dict(kind='call', label=rotulo, routine=rotina, registers=regs)


def escrita(rotulo, endereco, dados):
    return dict(kind='write', label=rotulo, address=endereco, bytes=bytes(dados))


def recrutar(tipo):
    slot = {5: 0, 6: 1, 7: 2}[tipo]
    return chamada(f'tag 17 slot {slot}: InitRecruteTroupe(type {tipo}, player 0)', 'InitRecruteTroupe', EAX=tipo, EDX=0)


def ordens(estado):
    def gerar(c, k):
        e0 = ESTRUTURAS + PASSO * SANTUARIO
        if k == 2:
            c._acao(k, chamada('CreerBatiment cave (23,14) player 0', 'CreerBatiment', EAX=CAVE_CLIQUE, EDX=3, EBX=0))
            estado.cave = int(c.acoes[-1]['exit_registers']['EAX'], 16) & 0xffff
            if estado.cave == 0xffff:
                raise RuntimeError('CreerBatiment refused the declared cave')
            antes = colonos(c, SANTUARIO)
            yield chamada('tag 33: BatimentRetireColon(sanctuary)', 'BatimentRetireColon', EAX=SANTUARIO)
            saiu = [v for v in antes if v not in colonos(c, SANTUARIO)]
            if len(saiu) != 1:
                raise RuntimeError(f'BatimentRetireColon released {saiu} (sanctuary colonists before: {antes})')
            estado.colono = saiu[0]
            return
        cave = estado.cave
        ec = ESTRUTURAS + PASSO * cave
        if k == 12:
            alvo = c.u16(TIPOS + 52 * 3 + 4)
            yield escrita(f'cave {cave} progress +0xa := {alvo - 2} (target {alvo} - 2)', ec + 0xa,
                          struct.pack('<H', alvo - 2))
            yield chamada('BatimentConstruction(cave) completes it', 'BatimentConstruction', EAX=cave)
            return
        if k > 12 and 'colono' not in estado.feito and unidade(c, estado.colono)['state'] in (0, 7):
            estado.feito.add('colono')
            yield chamada('tag 0x10: SetEnginRentreBatiment(colonist, cave)', 'SetEnginRentreBatiment',
                          EAX=estado.colono, EDX=cave, EBX=9)
        if k == 30:
            yield chamada('select the sanctuary: BatimentSelection(0)', 'BatimentSelection', EAX=SANTUARIO)
            yield recrutar(5)
            estado.pendente = True
            return
        if k == 40:
            yield recrutar(7)
            return
        if k == 50:
            for tipo in (5, 6, 7):
                yield dict(kind='case', label=f'idle sanctuary (+0x74 := 0): recruit type {tipo}',
                           steps=[escrita('sanctuary +0x74 := 0', e0 + 0x74, [0]), recrutar(tipo)])
            yield dict(kind='case', label='food total 3: recruit type 5 (short)',
                       steps=[escrita('sanctuary +0x74 := 0', e0 + 0x74, [0]),
                              escrita('player 0 food total := 3', RECURSOS + 8 + 2, struct.pack('<H', 3)),
                              recrutar(5)])
            yield dict(kind='case', label='cave selected: recruit type 5 (structure does not recruit)',
                       steps=[chamada('BatimentSelection(cave)', 'BatimentSelection', EAX=cave), recrutar(5)])
            return
        if k == 150:
            if c.u8(ec + 4) != 0:
                raise RuntimeError(f'The cave is not owned by player 0 at frame 150 (owner {c.u8(ec + 4)})')
            for b75, b76 in ((1, 0), (1, 14), (1, 15), (0, 5), (0, 1), (0, 0)):
                for bit in (0, 1):
                    anim = c.u32(ANIM)
                    yield dict(kind='case', label=f'cave body: +0x75={b75} +0x76={b76}, 0x508f80 bit0={bit}',
                               steps=[escrita('cave +0x75/+0x76', ec + 0x75, [b75, b76]),
                                      escrita('0x508f80 bit 0', ANIM, struct.pack('<I', (anim & ~1) | bit)),
                                      chamada('BatimentNextEtape(cave)', 'BatimentNextEtape', EAX=cave)])
            yield dict(kind='case', label='double click on the cave: BatimentRetireColon(cave)',
                       steps=[chamada('BatimentRetireColon(cave)', 'BatimentRetireColon', EAX=cave)])
            yield dict(kind='case', label='BatimentHabitable(sanctuary)',
                       steps=[chamada('BatimentHabitable(0)', 'BatimentHabitable', EAX=SANTUARIO, EDX=1)])
            yield dict(kind='case', label='InitBatimentPlayer(sanctuary, 0)',
                       steps=[chamada('InitBatimentPlayer(0, 0)', 'InitBatimentPlayer', EAX=SANTUARIO, EDX=0)])
            yield dict(kind='case', label='InitBatimentNeutre(sanctuary, 0)',
                       steps=[chamada('InitBatimentNeutre(0, 0)', 'InitBatimentNeutre', EAX=SANTUARIO, EDX=0)])
            yield dict(kind='case', label='InitBatimentPlayer(cave, 0) again',
                       steps=[chamada('InitBatimentPlayer(cave, 0)', 'InitBatimentPlayer', EAX=cave, EDX=0)])
            yield dict(kind='case', label='InitBatimentNeutre(cave, 0)',
                       steps=[chamada('InitBatimentNeutre(cave, 0)', 'InitBatimentNeutre', EAX=cave, EDX=0)])
            return
        pendente = c.u8(e0 + 0x74) != 0
        if estado.pendente and not pendente:
            estado.recrutas.append(k)
            estado.pendente = False
        if not pendente and k > 50 and estado.plano and estado.recrutas:
            tipo = estado.plano.pop(0)
            estado.quadros_acao.add(k)
            yield recrutar(tipo)
            estado.pendente = c.u8(e0 + 0x74) != 0
    return gerar


def escolher(estado):
    def f(nome, regs, c):
        if nome in SEMPRE or c.acao_atual is not None:
            return True
        s = regs['EAX'] & 0xffff
        k = c.k
        if nome == 'BatimentNextEtape':
            if estado.cave is None or s != estado.cave:
                return False
            return k <= 20 or 118 <= k <= 135 or k % 20 == 0
        if s != SANTUARIO:
            return False
        if k in estado.quadros_acao or k % 20 == 0:
            return True
        e0 = ESTRUTURAS + PASSO * SANTUARIO
        if not c.u8(e0 + 0x74):
            return False
        t = limiar(c, SANTUARIO)
        return t is not None and t - c.u32(e0 + 0x8c) <= 1500
    return f


def amostra(estado):
    def f(c):
        r = dict(resources_p0=c.ler(RECURSOS, 32).hex(), cave_words_p0=c.ler(CAVES, 6).hex(),
                 selection_p0=c.u16(SELECOES_ESTRUTURA), anim=c.u32(ANIM), structures={0: estrutura(c, 0)})
        if estado.cave is not None:
            r['structures'][estado.cave] = estrutura(c, estado.cave)
        if estado.colono is not None:
            r['colonist'] = unidade(c, estado.colono)
        return r
    return f


def executar(ate, observador=None, progresso=None):
    from bancada_ciclo_trabalho import Ciclo
    estado = Estado()
    c = Ciclo(ROTINAS, escolher(estado), ordens(estado), observador=observador, amostra=amostra(estado),
              gravar_acoes=True)
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
        schema='rising-lands/economy-cave-recruitment-capture/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, scenario='exibicao', source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        reference=dict(path=str(c.cap_caminho.relative_to(RAIZ)), sha256=hashlib.sha256(c.cap_caminho.read_bytes()).hexdigest()),
        inputs='display-reference named inputs; later frames keep the declared no-input answers; display clock '
               '0x123456+40*k (the reference rule, extended)',
        reproduction=c.reproducao, last_counter=a.ate, seconds=segundos,
        colonist=estado.colono, cave=estado.cave, recruit_completions=estado.recrutas,
        routines=list(ROTINAS), always_recorded=list(SEMPRE),
        actions=c.acoes, frames=c.quadros, calls=c.registros)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9) if saida.suffix == '.xz' else bruto)
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(), seconds=segundos,
                          reproduction=c.reproducao, calls=len(c.registros), actions=len(c.acoes),
                          colonist=estado.colono, cave=estado.cave, recruits=estado.recrutas), indent=1), flush=True)
    encerrar_captura(0, saida)


if __name__ == '__main__':
    main()
