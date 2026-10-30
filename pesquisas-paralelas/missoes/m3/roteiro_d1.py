"""The D1 input (schema rising-lands/monde01-scripted-input/1): the M4.2 defeat, written from development runs.

Defeat in the original is only `TestFinDeMission 0x458735` with player unit count 0x4e1a3a = 0 (dead units are in
state 4, `CalculEnginNextEtape`); MONDE01 has no trap cells, so every unit must fall to the raiders. A grouped force
wins against a raid; marched into the raiders it loses. Each stage was run natively, resumed from the previous
stage's snapshot (`.local/m3/d1`, runs D1-b, D1-c, D1-d). See SONDAS_M3.md "D1".

    python3 -B pesquisas-paralelas/missoes/m3/roteiro_d1.py 15700
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrada_roteirizada import clique, lparam
from roteiro_s1 import dbl, escrever, seta
SANT = (528, 400); C = (400, 272)


def arrasto(k, a, b):
    """Selection box: move to A at k, DOWN at k+1, moves toward B at k+3/k+4 (button held), UP at B at k+6."""
    m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
    return [dict(frame=k, cursor=list(a), messages=[[0x200, 0, lparam(*a)]]),
            dict(frame=k + 1, messages=[[0x201, 1, lparam(*a)]]),
            dict(frame=k + 3, cursor=list(m), messages=[[0x200, 1, lparam(*m)]]),
            dict(frame=k + 4, cursor=list(b), messages=[[0x200, 1, lparam(*b)]]),
            dict(frame=k + 6, messages=[[0x202, 0, lparam(*b)]])]


def etapa1():
    # Sanctuary select; 8 double clicks release its 8 colonists (tag 33); deselect; view down 5 rows to (0,5);
    # box-select the 16 units; minimap press (7,92): move the group to (3,46) (tag 5, 11779), on the raid path.
    return [clique(140, *SANT), [dbl(160 + 30 * i, SANT) for i in range(8)], clique(420, *C, 'right'),
            seta(0x28, 0x50, 430, 5), arrasto(450, (100, 150), (700, 540)), clique(470, 7, 92)]


def etapa2():
    # The group (still selected) is sent toward the raid spawn corner (63,63): it meets the two raiders on the
    # way and loses 14 units (16 -> 2 between 11429 and 13687).
    return [clique(11010, 127, 126)]


def etapa3():
    # The two survivors (units 0 and 9, still selected) are sent onto the raiders resting at (22..23,36):
    # count 0 at 15555, MenuInit(0x13) at 15654, PartieGetResultat 0 and the failure branch at 15655.
    return [clique(15010, 45, 72)]


if __name__ == '__main__':
    escrever('D1', [etapa1(), etapa2(), etapa3()], int(sys.argv[1]))
