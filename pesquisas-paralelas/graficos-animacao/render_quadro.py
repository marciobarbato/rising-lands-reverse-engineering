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
from pathlib import Path
from graficos import Catalogo
from ciclo_cache_terreno import CicloCacheTerreno, MemoriaMotor
from vinculos_graficos import ArenaGlobalFixa, RegistroVinculos
from quadro_jogo import compor_quadro, EstadoTela, MundoQuadro, DependenciaQuadro, GLOBAIS_QUADRO
from test_quadro_jogo import DD, tabelas
from hud_quadro import compor_hud, LeituraHud
from graficos import RAIZ
import json

# Contract version: major for breaking changes; minor for optional inputs and newly evidenced branches.
VERSAO_RENDER_QUADRO = (1, 8)
LARGURA, ALTURA = 800, 600
DGROUP, DGROUP_FIM = 0x494000, 0x523000
ESTRUTURAS, PASSO_ESTRUTURA = 0x49a0c8, 276
# (name, pointer slot, size): world buffers addressed through DGROUP slots
BLOCOS = (('terreno', 0x507d70, 131072), ('objetos', 0x507d74, 65536), ('auxiliares', 0x507dac, 65536),
          ('regioes', 0x4e0f38, 131072), ('unidades', 0x4e19a0, 220800), ('projeteis', 0x5080f0, 5600),
          *((f'descoberta{i}', 0x507d78+4*i, 65536) for i in range(4)),
          *((f'iluminacao{i}', 0x507d88+4*i, 65536) for i in range(4)))
SELECAO_ESTRUTURAS = 0x495be0     # five u16: per-owner selected structure
# HUD tail: minimap/player buffers (1.4); grayscale lookup for disabled action icons (1.5).
MINIMAPA = (0x507d5c, 0x496fe0, 0x496fe2)   # buffer pointer, width word, height word
JOGADORES, PASSO_JOGADOR = 0x5080a8, 20     # player table pointer; 5 records of 20 bytes
RELOGIOS = (0x508f80, 0x508f84)   # with 0x508f7c (quadro_u32 in the frame globals)


@dataclass(frozen=True)
class EstadoCache:
    """GetNumBob's terrain cache (original: keys at [0x49A050], cursor 0x49A04E, bank payloads 1090..1345).

    A cache hit reuses the stored pixels (lighting/discovery changes do not invalidate it), so a frame sequence is
    exact only when the cache is carried from frame to frame: pass ``resultado.cache`` into the next call.
    """
    registros: bytes     # 256 keys x 4 bytes
    blocos_crus: bytes   # 256 raw 1056-byte payloads
    proximo: int         # replacement cursor 0..255


@dataclass(frozen=True)
class QuadroRenderizado:
    versao: tuple        # VERSAO_RENDER_QUADRO of the producer
    largura: int         # 800
    altura: int          # 600
    pixels: bytes        # 800 x 600 palette indices (the offscreen surface after the composed passes)
    rgba: bytes          # pixels through the palette (800 x 600 x 4)
    parada: object       # None, or dict(endereco, detalhe): the first unreconstructed original branch
    chamadas: tuple      # ordered original calls the composition made
    efeitos: tuple       # (name, address, old hex, new hex) writes to the frame globals
    cache: object = None # EstadoCache after the frame: feed it to the next frame's call


def _ler_comprimido(entrada_b64, sha256_esperado):
    import base64, zlib, hashlib
    dados = zlib.decompress(base64.b64decode(entrada_b64))
    if hashlib.sha256(dados).hexdigest() != sha256_esperado: raise ValueError('Artifact hash mismatch')
    return dados


def carregar_superficie_inicial(caminho):
    """The M2.2 initial surface artifact -> 800*600 palette indices (hash-verified)."""
    d = json.loads(Path(caminho).read_text())
    return _ler_comprimido(d['pixels_zlib_base64'], d['sha256'])


def carregar_cache_inicial(caminho, catalogo=None):
    """The M2.2 initial terrain-cache artifact -> EstadoCache (keys, cursor and payloads, hash-verified)."""
    from ciclo_cache_terreno import blocos_banco_cache
    d = json.loads(Path(caminho).read_text())
    chaves = _ler_comprimido(d['keys_zlib_base64'], d['keys_sha256'])
    base = bytearray(blocos_banco_cache(catalogo or Catalogo()))
    import hashlib
    if hashlib.sha256(bytes(base)).hexdigest() != d['base_payloads_sha256']: raise ValueError('Bank payloads differ from the artifact base')
    for i, b64 in d['modified_slots_zlib_base64'].items():
        import base64, zlib
        base[int(i)*1056:(int(i)+1)*1056] = zlib.decompress(base64.b64decode(b64))
    if hashlib.sha256(bytes(base)).hexdigest() != d['full_payloads_sha256']: raise ValueError('Cache payloads hash mismatch')
    return EstadoCache(chaves, bytes(base), d['cursor'])


def regioes_necessarias(memoria, hud=False):
    """(start, end_exclusive, name) regions a MemoriaDeclarada must declare to render from its current pointers.

    1.7 adds the facade/placement gray table and the saved-background buffer when restoration is pending.
    hud=True adds the minimap, player table, disabled-icon grayscale table and tooltip shadow table.
    """
    regioes = [(DGROUP, DGROUP_FIM, 'dgroup')]
    for nome, slot, tamanho in BLOCOS:
        base = memoria.u32(slot)
        regioes.append((base, base+tamanho, nome))
    base = memoria.u32(0x4e24c4)
    if base: regioes.append((base, base+256, 'gray_effect'))
    if memoria.u8(0x49a041):
        base = memoria.u32(0x49a03c)
        regioes.append((base, base+memoria.u16(0x49a04a)*memoria.u16(0x49a04c), 'saved_background'))
    if hud:
        base = memoria.u32(MINIMAPA[0])
        regioes.append((base, base+memoria.u16(MINIMAPA[1])*memoria.u16(MINIMAPA[2]), 'minimapa'))
        base = memoria.u32(JOGADORES)
        regioes.append((base, base+5*PASSO_JOGADOR, 'jogadores'))
        base = memoria.u32(0x4e24bc)
        regioes.append((base, base+256, 'noir_blanc'))
        base = memoria.u32(0x4e24b4)
        if base: regioes.append((base, base+256, 'tooltip_shadow'))
    return regioes


def renderizar_quadro(memoria, *, superficie_anterior, catalogo=None, paleta=None, habitado=None, relogio=None, cache=None, hud=False, texto=None):
    """Compose the frame.  ``superficie_anterior``: 800*600 bytes (the surface the game draws over).

    hud=False (default, contract 1.3 behaviour): the composition ends at the HUD checkpoint 0x417B1C.
    hud=True (1.4+, expanded by 1.5): a complete playfield is followed by AffGame's tail through 0x417D30 (bottom strip and cursor,
    ``hud_quadro``); the pixels are then the whole offscreen surface AffGame leaves for the flip.

    habitado(indice) -> bool is BatimentEstHabiter (economy's result); required as soon as a structure is occupied.
    relogio() -> GetTickCount; defaults to the tick copy at 0x4E17B4 in memory.
    cache: EstadoCache carried from the previous frame (None = the cold cache of the first InitCache: zero keys, cursor 0,
    original bank payloads); the state after this frame is returned in ``QuadroRenderizado.cache``.
    texto(request, indexed_surface) -> bytes (optional, 1.7): AffText glyph provider. request contains text bytes,
    x/y/right/bottom, font and flags. Called after the tooltip background is saved/framed/shaded, before the cursor.
    Without it, a tooltip whose timer has expired stops visibly at 0x459454. The probe's declared text boundary is
    available only as a strict fixture adapter in validar_sondas_graficos_m3, never as a normal rendering default.
    GetBob exports a write-only saved_background_pixels effect (old hex empty); carry these bytes for the following
    frame's PasteBob restoration. memoria is never mutated, including by that copy.
    """
    if len(superficie_anterior) != LARGURA*ALTURA: raise ValueError('The previous surface must be 800 x 600 bytes')
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
    if cache is None:
        ciclo = CicloCacheTerreno.apos_carregar_banco(catalogo)
    else:
        if len(cache.registros) != 1024 or len(cache.blocos_crus) != 256*1056 or not 0 <= cache.proximo < 256:
            raise ValueError('Invalid EstadoCache')
        ciclo = CicloCacheTerreno(cache.blocos_crus, proximo_u16=cache.proximo)
    ciclo.alocar(mem); ciclo.iniciar()
    if cache is not None: ciclo.cache.registros[:] = cache.registros
    parada = None
    try:
        q = compor_quadro(mundo, tela, ciclo_cache=ciclo, catalogo=catalogo, tabela_sombra=sombra, tabela_eclairage=ecl,
            superficie=bytes(superficie_anterior), relogio=relogio or (lambda: memoria.u32(0x4e17b4) or 1500), directdraw=DD(),
            habitado=habitado, relogios_extra=tuple(memoria.u32(a) for a in RELOGIOS),
            selecao_estruturas=struct.unpack('<5H', lido(SELECAO_ESTRUTURAS, 10)), leitura_entrada=LeituraHud(memoria))
        pixels, chamadas, efeitos = q['superficie'], q['chamadas'], q['efeitos']
        if hud and q['desenhado']:
            sobrepostos = {}
            for nome, endereco, largura in GLOBAIS_QUADRO:
                for i, v in enumerate(tela.bruto(nome)): sobrepostos[endereco+i] = v
            try:
                h = compor_hud(LeituraHud(memoria, sobrepostos), pixels, catalogo=catalogo, evento=q['evento'], texto=texto)
            except DependenciaQuadro as e:
                e.chamadas, e.efeitos = list(chamadas)+e.chamadas, list(efeitos)+e.efeitos
                raise
            pixels, chamadas, efeitos = h['superficie'], list(chamadas)+h['chamadas'], list(efeitos)+h['efeitos']
    except DependenciaQuadro as e:
        parada = dict(endereco=f'0x{e.endereco:08x}', detalhe=e.detalhe)
        pixels, chamadas, efeitos = e.superficie, e.chamadas, e.efeitos
    pal = paleta or catalogo.paleta()
    rgba = b''.join(pal[p*3:p*3+3]+b'\xff' for p in pixels)
    novo = EstadoCache(bytes(ciclo.registros), bytes(ciclo.blocos_crus), ciclo.proximo_u16)
    return QuadroRenderizado(VERSAO_RENDER_QUADRO, LARGURA, ALTURA, bytes(pixels), rgba, parada, tuple(map(tuple, chamadas)), tuple(efeitos), novo)
