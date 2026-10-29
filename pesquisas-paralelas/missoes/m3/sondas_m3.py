"""Write the M3 probe input files (schema rising-lands/monde01-scripted-input/1) from the Step 0 targets.

Each mouse probe is a list of M3_PLAN §2 clicks (``entrada_roteirizada.clique``: move at k, button down at k+1, up at
k+3) placed on pixels from ``alvos-m3-monde01.json``. F0 = 129; the cursor stays at (0,0) through frame 129.
The files are written under ``entradas/`` and committed with their captures.

    python3 -B pesquisas-paralelas/missoes/m3/sondas_m3.py
"""
import json
from pathlib import Path
import sys

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from entrada_roteirizada import ESQUEMA, clique, juntar_quadros, lparam  # noqa: E402

ENTRADAS = AQUI / 'entradas'
F0 = 129

# Pixels (alvos-m3-monde01.json, view origin (0,0); cell (x,y) -> (32x+16, 32y+16)).
UNIDADE_12 = (560, 528)        # builder, cell (17,16)
UNIDADE_13 = (464, 528)        # type 5, cell (14,16)
ICONE_CAVE = (180, 573)        # bag slot 2
SITIO_CAVE = (688, 400)        # cell (21,12), BatimentGetCase (20,10)
DESTINO_MOVE = (624, 432)      # cell (19,13), free and discovered at frame 128
CENTRO = (400, 272)            # playfield centre, cell (12,8)
SANTUARIO = (528, 400)         # sanctuary grid cell (16,12)
CELULA_CAVE = (656, 336)       # cave grid cell (20,10)


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
    # P4/P5 coordinates are read from their own exploration runs (deterministic prefixes): unit 13 stops on
    # field (26,32) at frame 402; the builder stops at (42,9) at frame 548.
    p['P4'] = sonda('P4', 'Select unit 13 (14,16); minimap press (53,64) with it selected (move to field (26,32)); '
                          'right click deselects; minimap press (46,49) sets view (10,16); select unit 13 at (26,32); '
                          'press field (27,32): harvest order. No cave exists.',
                    [clique(F0 + 1, *UNIDADE_13), clique(F0 + 11, 53, 64), clique(410, *CENTRO, 'right'),
                     clique(420, 46, 49), clique(430, 528, 528), clique(440, 560, 528)], F0 + 3000)
    p['P5'] = sonda('P5', 'Select builder 12; minimap press (86,17) with it selected (move to mine (43,8)); right click '
                          'deselects; minimap press (87,18) sets view (31,0); select unit 12 at (42,9); press mine '
                          '(43,8): mine order. No cave exists.',
                    [clique(F0 + 1, *UNIDADE_12), clique(F0 + 11, 86, 17), clique(560, *CENTRO, 'right'),
                     clique(570, 87, 18), clique(580, 368, 304), clique(590, 400, 272)], F0 + 3000)
    # P6 continues P3 once the cave is complete (frame 1812): read from P3 and from development runs resumed
    # from its frame-2000 snapshot. The sanctuary's grid cells include (16,12); the cave's are (19..21, 10..11).
    duplo = [dict(frame=2030, messages=[[0x203, 1, lparam(*SANTUARIO)]]),
             dict(frame=2032, messages=[[0x202, 0, lparam(*SANTUARIO)]])]
    p['P6'] = sonda('P6', 'P3, then: right click deselects; click the sanctuary (16,12) (structure selection); '
                          'double click it (WM_LBUTTONDBLCLK: one colonist leaves); select that colonist at (14,14); '
                          'click the cave cell (20,10): the colonist enters and lodges.',
                    [clique(F0 + 1, *UNIDADE_12), clique(F0 + 11, *ICONE_CAVE), clique(F0 + 21, *SITIO_CAVE),
                     clique(2005, *CENTRO, 'right'), clique(2015, *SANTUARIO), duplo, clique(2060, 464, 464),
                     clique(2070, *CELULA_CAVE)], 2400)
    teclas = [dict(frame=F0 + 1, cursor=list(CENTRO))]   # off every edge: no edge scroll fights the keys
    for vk, sc, ext, de, ate in ((0x27, 0x4d, 1, F0 + 11, F0 + 30), (0x28, 0x50, 1, F0 + 41, F0 + 60),
                                 (0x20, 0x39, 0, F0 + 81, F0 + 83), (0x58, 0x2d, 0, F0 + 91, F0 + 93)):
        teclas += tecla(vk, sc, ext, de, ate)
    teclas += tecla(0x31, 0x02, 0, F0 + 71, F0 + 73, assincrona=False)
    p['K1'] = sonda('K1', 'Keys: arrows right then down held 20 frames, digit 1 (WM_KEYDOWN only; WndProc 0x418313), '
                          'Space and X held 3 frames; cursor at the playfield centre from F0+1. Coverage only; nothing selected.', [teclas], F0 + 500)
    return p


def tecla(vk, sc, ext, de, ate, assincrona=True):
    """WM_KEYDOWN at ``de``, WM_KEYUP at ``ate``; GetAsyncKeyState(vk) answers 0x8000 (as i16) on frames
    de..ate-1 (a key held down) when ``assincrona``."""
    lp = 1 | sc << 16 | ext << 24
    quadros = [dict(frame=de, messages=[[0x100, vk, lp]]), dict(frame=ate, messages=[[0x101, vk, lp | 0xc0000000]])]
    if assincrona:
        quadros += [dict(frame=k, keys={hex(vk): -0x8000}) for k in range(de, ate)]
    return quadros


def main():
    ENTRADAS.mkdir(exist_ok=True)
    for nome, dados in sondas().items():
        caminho = ENTRADAS / f'{nome}.json'
        caminho.write_text(json.dumps(dados, indent=1, sort_keys=True) + '\n')
        print(caminho.relative_to(AQUI.parents[2]))


if __name__ == '__main__':
    main()
