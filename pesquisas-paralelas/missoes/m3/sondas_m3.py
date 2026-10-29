"""Write the M3 probe input files (schema rising-lands/monde01-scripted-input/1) from the Step 0 targets.

Each probe is a list of M3_PLAN §2 clicks (``entrada_roteirizada.clique``: move at k, button down at k+1, up at
k+3) placed on pixels from ``alvos-m3-monde01.json``. F0 = 129; the cursor stays at (0,0) through frame 129.
The files are written under ``entradas/`` and committed with their captures.

    python3 -B pesquisas-paralelas/missoes/m3/sondas_m3.py
"""
import json
from pathlib import Path
import sys

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from entrada_roteirizada import ESQUEMA, clique, juntar_quadros  # noqa: E402

ENTRADAS = AQUI / 'entradas'
F0 = 129

# Pixels (alvos-m3-monde01.json, view origin (0,0); cell (x,y) -> (32x+16, 32y+16)).
UNIDADE_12 = (560, 528)        # builder, cell (17,16)
ICONE_CAVE = (180, 573)        # bag slot 2
SITIO_CAVE = (688, 400)        # cell (21,12), BatimentGetCase (20,10)
DESTINO_MOVE = (624, 432)      # cell (19,13), free and discovered at frame 128


def sonda(nome, descricao, cliques, ate, extra=None):
    return dict(schema=ESQUEMA, name=nome, description=descricao, start=dict(frame=128, checkpoint='M2.2 frame128'),
                stop_frame=ate, frames=juntar_quadros(*cliques), **(extra or {}))


def sondas():
    p = {}
    p['P1'] = sonda('P1', 'Select builder unit 12: one left click on its cell (17,16).',
                    [clique(F0 + 1, *UNIDADE_12)], F0 + 500)
    p['P2'] = sonda('P2', 'Select unit 12, then a left click on the free discovered cell (19,13): a move order.',
                    [clique(F0 + 1, *UNIDADE_12), clique(F0 + 11, *DESTINO_MOVE)], F0 + 600)
    p['P3'] = sonda('P3', 'Select unit 12, press the CAVE icon (bag slot 2), press the proposed site (21,12); '
                          'follow the walk and the construction start.',
                    [clique(F0 + 1, *UNIDADE_12), clique(F0 + 11, *ICONE_CAVE), clique(F0 + 21, *SITIO_CAVE)],
                    F0 + 3000)
    return p


def main():
    ENTRADAS.mkdir(exist_ok=True)
    for nome, dados in sondas().items():
        caminho = ENTRADAS / f'{nome}.json'
        caminho.write_text(json.dumps(dados, indent=1, sort_keys=True) + '\n')
        print(caminho.relative_to(AQUI.parents[2]))


if __name__ == '__main__':
    main()
