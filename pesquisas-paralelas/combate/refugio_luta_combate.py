"""The original civilian refuge query: prefer CAVE, then sanctuary, at any range."""
from abi_luta_fatal_combate import registradores_exigidos
from chamadas_quadro_core import caso_estrutura
from alvos_alcance import distancia2


def buscar_refugio(memoria, cell, player):
    cell&=65535;player&=255;m=memoria
    best={2:(0xffffffff,65535),3:(0xffffffff,65535)}
    for index in range(1000):
        rec=0x49a0c8+276*index;kind=m.u8(rec+8)
        if not m.u8(rec+5) or m.u8(rec+4)!=player or kind not in (2,3):continue
        centre=caso_estrutura(m,index)['EAX']&65535
        distance=distancia2(cell,centre)
        if distance<best[kind][0]:best[kind]=(distance,index)
    return best[3][1] if best[3][1]!=65535 else best[2][1]


def refugio_registradores(memoria, regs, *, chamada=0x4539f3):
    out=registradores_exigidos('ChercheBatimentProximiteCaveOuSanctuaire',chamada,regs)
    out.update(EAX=buscar_refugio(memoria,out['EAX'],out['EDX']),EDX=1000)
    return out
