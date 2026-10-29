"""Render API: live memory view -> one AffGame frame (indexed pixels and RGBA), pure Python.

``renderizar_quadro(memoria, ...)`` reads the in-game state through ``memoria`` (``u8/u16/u32`` and ``ler_mundo``,
the ``MemoriaDeclarada`` contract) and runs the reconstructed AffGame mode-0x12 composition (CalculFrame, AffTerrain,
AffSprite with vegetation, structure facade of the type-2 Santuario, units and projectiles inside their validated
domains).  It never writes to ``memoria``.  Every pass outside the validated domain stops at its original address:
the result then carries the partial frame and ``parada`` (address and reason), never a guess.

Reads (declare these regions on the MemoriaDeclarada): DGROUP+.bss ``0x494000..0x523000`` and the buffers addressed
by the slots in ``BLOCOS`` (``regioes_necessarias``).  The previous surface is an input (the original draws over it).
"""
import struct
from dataclasses import dataclass
from graficos import Catalogo
from ciclo_cache_terreno import CicloCacheTerreno, MemoriaMotor
from vinculos_graficos import ArenaGlobalFixa, RegistroVinculos
from quadro_jogo import compor_quadro, EstadoTela, MundoQuadro, DependenciaQuadro, GLOBAIS_QUADRO
from test_quadro_jogo import DD, tabelas
from graficos import RAIZ
import json

DGROUP, DGROUP_FIM = 0x494000, 0x523000
ESTRUTURAS, PASSO_ESTRUTURA = 0x49a0c8, 276
# (name, pointer slot, size): world buffers addressed through DGROUP slots
BLOCOS = (('terreno', 0x507d70, 131072), ('objetos', 0x507d74, 65536), ('auxiliares', 0x507dac, 65536),
          ('regioes', 0x4e0f38, 131072), ('unidades', 0x4e19a0, 220800), ('projeteis', 0x5080f0, 5600),
          *((f'descoberta{i}', 0x507d78+4*i, 65536) for i in range(4)),
          *((f'iluminacao{i}', 0x507d88+4*i, 65536) for i in range(4)))
SELECAO_ESTRUTURAS = 0x495be0     # five u16: per-owner selected structure
RELOGIOS = (0x508f80, 0x508f84)   # with 0x508f7c (quadro_u32 in the frame globals)


@dataclass(frozen=True)
class QuadroRenderizado:
    pixels: bytes        # 800 x 600 palette indices (the offscreen surface after the composed passes)
    rgba: bytes          # pixels through the palette (800 x 600 x 4)
    parada: object       # None, or dict(endereco, detalhe): the first unreconstructed original branch
    chamadas: tuple      # ordered original calls the composition made
    efeitos: tuple       # (name, address, old hex, new hex) writes to the frame globals


def regioes_necessarias(memoria):
    """(start, end_exclusive, name) regions a MemoriaDeclarada must declare to render from its current pointers."""
    regioes = [(DGROUP, DGROUP_FIM, 'dgroup')]
    for nome, slot, tamanho in BLOCOS:
        base = memoria.u32(slot)
        regioes.append((base, base+tamanho, nome))
    return regioes


def renderizar_quadro(memoria, *, superficie_anterior, catalogo=None, paleta=None, habitado=None, relogio=None):
    """Compose the frame.  ``superficie_anterior``: 800*600 bytes (the surface the game draws over).

    habitado(indice) -> bool is BatimentEstHabiter (economy's result); required as soon as a structure is occupied.
    relogio() -> GetTickCount; defaults to the tick copy at 0x4E17B4 in memory.
    """
    if len(superficie_anterior) != 800*600: raise ValueError('The previous surface must be 800 x 600 bytes')
    lido = lambda a, n: bytes(memoria.ler_mundo(a, n))
    globais = {n: lido(a, w) for n, a, w in GLOBAIS_QUADRO}
    blocos = {n: lido(memoria.u32(slot), tam) for n, slot, tam in BLOCOS}
    mundo = MundoQuadro(terreno=blocos['terreno'], objetos=blocos['objetos'], auxiliares=blocos['auxiliares'],
        regioes=blocos['regioes'], unidades=blocos['unidades'], projeteis=blocos['projeteis'],
        descoberta=[blocos[f'descoberta{i}'] for i in range(4)], iluminacao=[blocos[f'iluminacao{i}'] for i in range(4)],
        estruturas=lido(ESTRUTURAS, 1000*PASSO_ESTRUTURA))
    tela = EstadoTela(globais)
    catalogo = catalogo or Catalogo(); sombra, ecl = tabelas()
    f = json.loads((RAIZ/'validacao/x86-quadro-jogo.json').read_text())['cache_alloc_fixture']
    mem = MemoriaMotor(contador_u32=f['counter_u32'], vinculos=ArenaGlobalFixa(inicio_u32=f['arena_next'],
        tamanho_u32=f['arena_end']-f['arena_next'], registro=RegistroVinculos()))
    ciclo = CicloCacheTerreno.apos_carregar_banco(catalogo); ciclo.alocar(mem); ciclo.iniciar()
    parada = None
    try:
        q = compor_quadro(mundo, tela, ciclo_cache=ciclo, catalogo=catalogo, tabela_sombra=sombra, tabela_eclairage=ecl,
            superficie=bytes(superficie_anterior), relogio=relogio or (lambda: memoria.u32(0x4e17b4) or 1500), directdraw=DD(),
            habitado=habitado, relogios_extra=tuple(memoria.u32(a) for a in RELOGIOS),
            selecao_estruturas=struct.unpack('<5H', lido(SELECAO_ESTRUTURAS, 10)))
        pixels, chamadas, efeitos = q['superficie'], q['chamadas'], q['efeitos']
    except DependenciaQuadro as e:
        parada = dict(endereco=f'0x{e.endereco:08x}', detalhe=e.detalhe)
        pixels, chamadas, efeitos = e.superficie, e.chamadas, e.efeitos
    pal = paleta or catalogo.paleta()
    rgba = b''.join(pal[p*3:p*3+3]+b'\xff' for p in pixels)
    return QuadroRenderizado(bytes(pixels), rgba, parada, tuple(map(tuple, chamadas)), tuple(efeitos))
