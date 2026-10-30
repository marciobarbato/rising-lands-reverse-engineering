"""Original-only capture of SortieTroupe's abandonment path: the recruit takes the sanctuary's last colonist.

Bench: ``bancada_ciclo_trabalho.Ciclo`` with ``gravar_acoes`` (MONDE01 display reference; frames 0/1 reproduced;
then real frames with the reference's no-input answers). No Python translation is imported.

Declared actions at CalculGame entries, all by ORIGINAL routines called natively:
1. frames 2, 3, ...: BatimentRetireColon(sanctuary) (tag 33, the double click on the selected sanctuary), one per
   frame, until a single colonist remains in it.
2. the next frame: BatimentSelection(sanctuary) (0x495be0[0] = 0), then InitRecruteTroupe(AL = 5, DL = 0) (tag 17,
   icon slot 0: 4 food).
Then the recruit completes natively: SortieTroupe's BagRetire takes the last colonist, BagContient(Bag, 1, 9)
finds none, and the original runs 0x42101d..0x42114e (request cleared, BatimentGetCase + EteintTerrain with the
type's radius, the owner's structure selection reset, owner := 0xc8, BatimentModifyMap) before the common tail.

Recorded calls (``Ciclo`` isolation, also inside declared calls): every InitRecruteTroupe, BatimentHabitable,
InitBatimentNeutre, InitBatimentPlayer; CalculTroupe and SortieTroupe of the sanctuary in the action frames, every
20th frame and while the pending request is within 1,500 of its threshold, and every call once the sanctuary has
no colonist left. Per frame: the sanctuary record, player-0 resources and selection.

    python3 "…/heavy_lease.py" economy -- python3 -B pesquisas-paralelas/economia/capturar_abandono_santuario.py \\
        --ate 700 --saida pesquisas-paralelas/economia/evidencias/abandono-santuario/captura-abandono-santuario-exibicao.json.xz
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
for _p in (RAIZ / 'ferramentas', PASTA):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import capturar_caverna_recrutamento as ccr  # noqa: E402

FONTES = ccr.FONTES + ('pesquisas-paralelas/economia/capturar_abandono_santuario.py',)
SANTUARIO = ccr.SANTUARIO
SEMPRE = ('InitRecruteTroupe', 'BatimentHabitable', 'InitBatimentNeutre', 'InitBatimentPlayer')
ROTINAS = SEMPRE + ('CalculTroupe', 'SortieTroupe')


class Estado:
    def __init__(self):
        self.liberados = []
        self.recrutado = None
        self.quadros_acao = set()


def ordens(estado):
    def gerar(c, k):
        if estado.recrutado is not None:
            return
        restantes = ccr.colonos(c, SANTUARIO)
        estado.quadros_acao.add(k)
        if len(restantes) > 1:
            yield ccr.chamada('tag 33: BatimentRetireColon(sanctuary)', 'BatimentRetireColon', EAX=SANTUARIO)
            saiu = [v for v in restantes if v not in ccr.colonos(c, SANTUARIO)]
            if len(saiu) != 1:
                raise RuntimeError(f'BatimentRetireColon released {saiu} (sanctuary colonists before: {restantes})')
            estado.liberados.append(dict(frame=k, unit=saiu[0]))
            return
        yield ccr.chamada('select the sanctuary: BatimentSelection(0)', 'BatimentSelection', EAX=SANTUARIO)
        yield ccr.recrutar(5)
        if not c.u8(ccr.ESTRUTURAS + ccr.PASSO * SANTUARIO + 0x74):
            raise RuntimeError('InitRecruteTroupe(5, 0) was refused')
        estado.recrutado = k
    return gerar


def escolher(estado):
    def f(nome, regs, c):
        if nome in SEMPRE or c.acao_atual is not None:
            return True
        if regs['EAX'] & 0xffff != SANTUARIO:
            return False
        if c.k in estado.quadros_acao or c.k % 20 == 0 or not ccr.colonos(c, SANTUARIO):
            return True
        e0 = ccr.ESTRUTURAS + ccr.PASSO * SANTUARIO
        if not c.u8(e0 + 0x74):
            return False
        t = ccr.limiar(c, SANTUARIO)
        return t is not None and t - c.u32(e0 + 0x8c) <= 1500
    return f


def amostra(c):
    return dict(resources_p0=c.ler(ccr.RECURSOS, 32).hex(), selection_p0=c.u16(ccr.SELECOES_ESTRUTURA),
                structures={SANTUARIO: ccr.estrutura(c, SANTUARIO)})


def executar(ate, observador=None, progresso=None):
    from bancada_ciclo_trabalho import Ciclo
    estado = Estado()
    c = Ciclo(ROTINAS, escolher(estado), ordens(estado), observador=observador, amostra=amostra, gravar_acoes=True)
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
    abandono = next((f['frame'] for f in c.quadros if f['structures'][SANTUARIO]['owner'] == 0xc8), None)
    dados = dict(
        schema='rising-lands/economy-sanctuary-abandonment-capture/1', original_sha256=HASH_ORIGINAL,
        translation_executed=False, scenario='exibicao', source_revision=revisao,
        source_sha256={p: hashlib.sha256((RAIZ / p).read_bytes()).hexdigest() for p in FONTES},
        reference=dict(path=str(c.cap_caminho.relative_to(RAIZ)), sha256=hashlib.sha256(c.cap_caminho.read_bytes()).hexdigest()),
        inputs='display-reference named inputs; later frames keep the declared no-input answers; display clock '
               '0x123456+40*k (the reference rule, extended)',
        reproduction=c.reproducao, last_counter=a.ate, seconds=segundos, released=estado.liberados,
        recruit_frame=estado.recrutado, abandoned_frame=abandono, routines=list(ROTINAS), always_recorded=list(SEMPRE),
        actions=c.acoes, frames=c.quadros, calls=c.registros)
    saida.parent.mkdir(parents=True, exist_ok=True)
    bruto = (json.dumps(dados, sort_keys=True) + '\n').encode()
    saida.write_bytes(lzma.compress(bruto, preset=9) if saida.suffix == '.xz' else bruto)
    print(json.dumps(dict(output=str(saida), raw_sha256=hashlib.sha256(bruto).hexdigest(), seconds=segundos,
                          reproduction=c.reproducao, calls=len(c.registros), recruit_frame=estado.recrutado,
                          abandoned_frame=abandono, released=len(estado.liberados)), indent=1), flush=True)
    encerrar_captura(0 if abandono is not None else 1, saida)


if __name__ == '__main__':
    main()
