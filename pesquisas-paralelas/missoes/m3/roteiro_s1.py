"""The S1 input (schema rising-lands/monde01-scripted-input/1), built in stages verified natively one by one.

Each stage was written from a run resumed from the previous stage's snapshot, because unit positions and
recruit exit frames must be read from the deterministic prefix. See SONDAS_M3.md "S1 script". The file
``entradas/S1.json`` holds stages 1-6 (no confirmation click yet); stop_frame bounds the continuation.

    python3 -B pesquisas-paralelas/missoes/m3/roteiro_s1.py 6 18000
"""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrada_roteirizada import clique, juntar_quadros, ESQUEMA, lparam
from sondas_m3 import tecla
SANT=(528,400); CAVE=(656,336); C=(400,272); UP=1|0x48<<16|1<<24

def dbl(k, p):
    return [dict(frame=k,messages=[[0x203,1,lparam(*p)]]), dict(frame=k+2,messages=[[0x202,0,lparam(*p)]])]

def seta(vk, sc, de, n):
    lp=1|sc<<16|1<<24
    return [dict(frame=k, keys={hex(vk): -0x8000}) for k in range(de,de+n)] + [dict(frame=de,messages=[[0x100,vk,lp]]), dict(frame=de+n,messages=[[0x101,vk,lp|0xc0000000]])]

def rota(k, origem, destino, rolagem=None):
    """Ctrl held from k to k+28: source press at k+1, optional arrow scroll from k+7, destination press at k+16."""
    r = [tecla(0x11,0x1d,0,k,k+28), clique(k+1,*origem), clique(k+16,*destino)]
    if rolagem: r.append(seta(*rolagem))
    return r

def etapa1():
    return [clique(130,560,528), clique(140,180,573), clique(150,688,400),
            clique(170,464,528), clique(180,53,64), clique(190,400,528), clique(200,55,64),
            clique(1820,*C,'right'), clique(1830,*SANT), dbl(1845,SANT)]

def etapa2():
    return [clique(1860,464,464), clique(1870,*CAVE),
            clique(2000,*SANT), clique(2010,180,573),
            clique(2020,*C,'right'), clique(2030,46,49), clique(2040,528,528),
            rota(2050,(592,528),(336,16),(0x26,0x48,2057,6)),
            clique(2090,*C,'right'), clique(2100,46,49), clique(2110,560,528),
            rota(2120,(528,528),(336,16),(0x26,0x48,2127,6)),
            clique(2160,*C,'right'), clique(2170,368,80), clique(2180,86,17),
            ]

def etapa3():
    return [clique(2400,*C,'right'), clique(2560,208,80), clique(2570,180,573),
            clique(2580,*C,'right'), clique(2590,144,144), clique(2600,86,17),
            clique(2620,*C,'right'), clique(2630,63,17), clique(2640,752,304),
            rota(2650,(784,272),(48,336))]

def rota_rolando(k, alvo_rec=None):
    """Ctrl held k..k+45; arrows right 9 and up 10 frames from k+1 (view (10,10) -> (19,0)); mine at k+15, cave at k+25."""
    return [tecla(0x11,0x1d,0,k,k+45), seta(0x27,0x4d,k+1,9), seta(0x26,0x48,k+1,10),
            clique(k+15,784,272), clique(k+25,48,336)]

def etapa4():
    return [clique(3110,*C,'right'), clique(3120,45,37), clique(3170,208,80), clique(3180,60,573),
            clique(3190,*C,'right'), clique(3200,208,144), rota_rolando(3210),
            clique(3260,*C,'right'), clique(3270,784,304), rota(3280,(784,272),(48,336))]

def rota_campo(k, campo):
    """Ctrl held k..k+50: arrow down 7 frames from k+1 (view (10,10) -> (10,17)); field press at k+12;
    arrow up 7 frames from k+20 (back to (10,10)); cave press at k+32."""
    return [tecla(0x11,0x1d,0,k,k+50), seta(0x28,0x50,k+1,7), clique(k+12,*campo), seta(0x26,0x48,k+20,7),
            clique(k+32,336,16)]

def etapa5():
    return [clique(3730,*C,'right'), clique(3740,45,37), clique(3750,208,80), clique(3760,60,573),
            clique(3810,*C,'right'), clique(3820,144,144), rota_campo(3830,(464,528)),
            clique(4170,*C,'right'), clique(4180,208,144), rota_campo(4190,(432,528)),
            clique(4400,*C,'right'), clique(4410,208,80), clique(4420,60,573)]

def etapa6():
    return [clique(4820,*C,'right'), clique(4830,144,144), rota_campo(4840,(368,528))]

def escrever(nome, etapas, ate):
    def planos(x):
        if isinstance(x, dict):
            yield x
        else:
            for y in x:
                yield from planos(y)
    fr = juntar_quadros(list(planos(etapas)))
    caminho = Path(__file__).resolve().parent / 'entradas' / f'{nome}.json'
    caminho.write_text(json.dumps(dict(schema=ESQUEMA, name=nome, start=dict(frame=128), stop_frame=ate, frames=fr),
                                  indent=1, sort_keys=True) + '\n')

if __name__ == '__main__':
    n = int(sys.argv[1]); ate = int(sys.argv[2])
    escrever('S1', [globals()[f'etapa{i}']() for i in range(1, n+1)], ate)
