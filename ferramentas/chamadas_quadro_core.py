"""Core callees reached by the MONDE01 frame-0/frame-1 composition (M2.1).

Translations of intact routines over a flat 32-bit address space: ``memoria``
is any object with ``u8/u16/u32(endereco, valor=None)`` over the live original
buffers (``memoria_quadro_core.MemoriaQuadro`` or ai-runtime's
``MemoriaDeclarada``). Addresses, pointer arithmetic, widths and table indexing
are the original ones, so the original aliasing is reproduced (for example a
discovery query for owner 4 reads the pointer that follows the four discovery
grid pointers). Every function returns a dict with the general registers the
routine leaves different from its inputs (EAX whenever it changes, clobbered
EDX/EBX included); unlisted registers are preserved by the original. Arithmetic flags on
return are not reproduced: every captured caller overwrites them before reading
(``caller_flag_use`` in ``evidencias/fundacoes-quadro/chamadas-quadro1/manifesto.json``).

Branches that the frame-0/frame-1 trace does not reach and that this module
does not translate raise ``DependenciaRamoCore`` at their original address
before any store. Validation: docs/core/FRAME_FOUNDATIONS.md (frame-1 section).
"""
from candidatos_rota import aleatorio_caminhos

PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
DIMENSOES_ESTRUTURA = 0x495d8c          # u16 width, +2 u16 height; stride 52 per type
GRADES_DESCOBERTA, GRADES_LUZ = 0x507d78, 0x507d88   # u32 grid pointer per owner byte
GRADE_ATRIBUTOS, GRADE_REGIOES = 0x507da8, 0x4e0f38
CLASSE_OCUPACAO = 0x4962c8               # u8 per unit type
LIMITE_FADIGA = 0x4965dc                 # u16 per unit type, stride 50
SEMENTE_MUNDO, CONTADOR_QUADRO_JOGO = 0x497164, 0x496d40
# BatimentCollision 0x41ab5c: mask table per structure type 0..0x15, from its
# jump table 0x41ab04 (type 20 shares type 15's table).
MASCARAS_ESTRUTURA = (0x495c04, 0x495c10, 0x495c30, 0x495c50, 0x495cec, 0x495c80, 0x495d6c, 0x495d30,
                      0x495cf8, 0x495d8a, 0x495d64, 0x495d5c, 0x495d8b, 0x495c6c, 0x495ca4, 0x495d1c,
                      0x495cd4, 0x495ce8, 0x495d48, 0x495cbc, 0x495d1c, 0x495cc8)
# SetEnginCollision 0x442cb4 jump table 0x442c4c: unit type -> footprint path.
UMA_CELULA, QUATRO_CELULAS, QUATRO_CELULAS_SEM_REGIAO, UMA_CELULA_SEM_REGIAO = 'single', 'quad', 'quad_mask2', 'single_mask2'
CAMINHO_COLISAO = tuple(QUATRO_CELULAS if t in (3, 11, 12, 13, 14, 15, 25) else
                        QUATRO_CELULAS_SEM_REGIAO if t == 16 else
                        UMA_CELULA_SEM_REGIAO if t == 17 else UMA_CELULA for t in range(26))
M32 = 0xffffffff


class DependenciaRamoCore(NotImplementedError):
    """A branch outside the frame-0/frame-1 domain; nothing was written."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made')


def _sx16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


def _metade(v):
    """Watcom signed /2: (v - (v >> 31)) >> 1 (sar) on a 32-bit value."""
    v &= M32
    s = v - (1 << 32) if v & 0x80000000 else v
    return (s - (-1 if s < 0 else 0)) >> 1 & M32


# ------------------------------------------------------------------ pure bit helpers
def obter_bit(eax, edx):
    """GetBit 0x467d97: EAX = ((u8 AL) sar (DL & 31)) & 1. ECX/EDX preserved."""
    return dict(EAX=(eax & 0xff) >> (edx & 0x1f) & 1)


def definir_bit(memoria, eax, edx, ebx):
    """SetBit 0x467d71: BL=0 clears, BL=1 sets bit DL of byte [EAX]; BL>1 returns.

    The 8-bit ``shl dl, cl`` uses CL = DL & 31, so a bit index >= 8 yields mask 0.
    Clearing leaves BL = new byte and DL = ~mask; setting leaves DL = mask.
    """
    bl, deslocamento = ebx & 0xff, edx & 0x1f
    mascara = (1 << deslocamento) & 0xff
    if bl == 0:
        novo = memoria.u8(eax) & (~mascara & 0xff)
        memoria.u8(eax, novo)
        return dict(EAX=eax & M32, EBX=(ebx & 0xffffff00) | novo, EDX=(edx & 0xffffff00) | (~mascara & 0xff))
    if bl == 1:
        memoria.u8(eax, memoria.u8(eax) | mascara)
        return dict(EAX=eax & M32, EDX=(edx & 0xffffff00) | mascara)
    return dict(EAX=eax & M32)


# ------------------------------------------------------------------ cell visibility queries
def _consulta_grade(memoria, tabela, eax, edx):
    ponteiro = memoria.u32(tabela + 4 * (edx & 0xff))
    oculto = not memoria.u8((ponteiro + (eax & 0xffff)) & M32) & 0x10
    return dict(EAX=(eax & 0xff00) | oculto, EDX=ponteiro)


def caso_esta_descoberta(memoria, eax, edx):
    """CaseEstDecouverte 0x4766d6: AL = (discovery[DL][AX] & 0x10) == 0; EDX = grid pointer."""
    return _consulta_grade(memoria, GRADES_DESCOBERTA, eax, edx)


def caso_esta_iluminada(memoria, eax, edx):
    """CaseEstIlluminee 0x47693a: same test on the light grid [0x507d88 + 4*DL] (tail 0x4766e8)."""
    return _consulta_grade(memoria, GRADES_LUZ, eax, edx)


# ------------------------------------------------------------------ structure geometry queries
def colisao_estrutura(memoria, eax, edx):
    """BatimentCollision 0x41ab5c: AL = type mask byte at index DX; types > 0x15 give AL 0.

    Valid types leave EDX = type and EAX = (DX & 0xff00) | mask byte; above 0x15
    EAX = EDX & ~0xff and EDX is unchanged. EBX preserved.
    """
    tipo = eax & 0xff
    if tipo > 0x15:
        return dict(EAX=edx & 0xffffff00)
    return dict(EAX=(edx & 0xff00) | memoria.u8(MASCARAS_ESTRUTURA[tipo] + (edx & 0xffff)), EDX=tipo)


def _estrutura(memoria, eax):
    indice = eax & 0xffff
    base = (ESTRUTURAS + indice * PASSO) & M32
    tipo = memoria.u8(base + 8)
    largura = memoria.u16(DIMENSOES_ESTRUTURA + 52 * tipo)
    altura = memoria.u16(DIMENSOES_ESTRUTURA + 2 + 52 * tipo)
    return indice, base, tipo, largura, altura


def caso_estrutura(memoria, eax):
    """BatimentGetCase 0x41aee2: centre cell of the masked footprint; only EAX changes.

    The origin dword keeps the high word of index*276 (the original loads the
    u16 origin into AX over that product), and the halving is Watcom's signed /2.
    """
    indice, base, tipo, largura, altura = _estrutura(memoria, eax)
    origem = (indice * PASSO & 0xffff0000) | memoria.u16(base + 2)
    min_x, min_y, max_y, max_x = 0xffff, 0xffff, 0, 0
    for y in range(altura):
        for x in range(largura):
            if colisao_estrutura(memoria, tipo, (largura * y + x) & 0xffff)['EAX'] & 0xff:
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_y, max_x = max(max_y, y), max(max_x, x)
    meio_y = _metade((max_y & 0xffff) - (min_y & 0xffff))
    meio_x = _metade((max_x & 0xffff) - (min_x & 0xffff))
    return dict(EAX=(((meio_y + min_y) << 8) + origem + min_x + meio_x) & M32)


def estrutura_esta_descoberta(memoria, eax, edx):
    """BatimentEstDecouvert 0x419c4f: AL = 1 at the first in-map footprint-rectangle cell
    (no mask) for which CaseEstDecouverte(cell, DL) is 1, scanning rows then columns;
    else 0 (shared tail 0x419c3f/0x419c4b). AL and DL both carry the result.
    """
    _, base, _, largura, altura = _estrutura(memoria, eax)
    origem = memoria.u16(base + 2)
    x0, y0 = origem % 256, origem // 256
    for linha in range(altura):
        if not 0 <= y0 + linha < 256:
            continue
        for coluna in range(largura):
            if 0 <= x0 + coluna < 256:
                r = caso_esta_descoberta(memoria, (origem + coluna + ((linha & 0xff) << 8)) & 0xffff, edx)
                if r['EAX'] & 0xff:
                    return dict(EAX=(r['EAX'] & 0xffffff00) | 1, EDX=(r['EDX'] & 0xffffff00) | 1)
    return dict(EAX=altura & 0xff00, EDX=altura & 0xff00)


def contorno_estrutura_iluminado(memoria, eax, edx):
    """BatimentContourEstIllumine 0x4199f9: AL = 1 at the first in-map cell of the ring
    around the footprint rectangle (dy in -1..H, dx in -1..W, border only) for which
    CaseEstIlluminee(cell, DL) is 1, rows then columns; else 0.
    """
    _, base, _, largura, altura = _estrutura(memoria, eax)
    largura1, altura1 = (largura + 1) & 0xffff, (altura + 1) & 0xffff
    origem = memoria.u16(base + 2)
    x0, y0 = origem % 256, origem // 256
    dy = -1
    while dy < altura1:
        if 0 <= y0 + dy < 256:
            for dx in range(-1, largura1):
                if not 0 <= x0 + dx < 256:
                    continue
                if dx == -1 or dx == largura1 - 1 or dy == -1 or dy == altura1 - 1:
                    r = caso_esta_iluminada(memoria, (origem + dx + ((dy & 0xff) << 8)) & 0xffff, edx)
                    if r['EAX'] & 0xff:
                        return dict(EAX=(r['EAX'] & 0xffffff00) | 1, EDX=r['EDX'])
        dy = _sx16(dy + 1)
    return dict(EAX=dy & 0xffffff00, EDX=altura1)


# ------------------------------------------------------------------ unit collision
def definir_colisao(memoria, eax, edx):
    """SetCollision 0x47622e: attribute[AX] |= DL; EAX = attribute grid pointer."""
    ponteiro = memoria.u32(GRADE_ATRIBUTOS)
    endereco = (ponteiro + (eax & 0xffff)) & M32
    memoria.u8(endereco, memoria.u8(endereco) | (edx & 0xff))
    return dict(EAX=ponteiro)


def modificar_zona_caminho(memoria, eax, edx, ebx, ecx, sub):
    """Chemin_ModifieZone 0x43e138, mode BL=2 (unit tag insert); ``sub`` is the pushed byte.

    Tag = (EDX<<3)+sub with BH += 0x40 (8-bit) and BL |= 4 unless the unit type's
    occupation class 0x4962c8 is 1. If region[AX] < 0x4000 the old word goes to
    [ECX], the tag to region[AX] and AL = 1; otherwise AL = 0. EBX = tag and
    EDX = 2*cell on both exits; ESI/EDI/ECX preserved; RET 4.
    """
    modo = ebx & 0xff
    if modo != 2:
        alvo = {0: 0x43e153, 1: 0x43e1b4, 3: 0x43e256}.get(modo, 0x43e29c)
        raise DependenciaRamoCore('Chemin_ModifieZone', alvo, f'mode {modo} not translated')
    unidade = edx & M32
    marca = ((unidade << 3) + (sub & 0xff)) & M32
    marca = (marca & 0xffff00ff) | ((((marca >> 8) & 0xff) + 0x40) & 0xff) << 8
    tipo = memoria.u8((memoria.u32(PONTEIRO_UNIDADES) + (unidade & 0xffff) * PASSO + 1) & M32)
    if memoria.u8(CLASSE_OCUPACAO + tipo) != 1:
        marca |= 4
    deslocamento = (eax & 0xffff) * 2
    regioes = memoria.u32(GRADE_REGIOES)
    endereco = (regioes + deslocamento) & M32
    antigo = memoria.u16(endereco)
    if antigo >= 0x4000:
        return dict(EAX=endereco & 0xffffff00, EBX=marca, EDX=deslocamento)
    memoria.u16(ecx, antigo)
    memoria.u16((memoria.u32(GRADE_REGIOES) + deslocamento) & M32, marca)
    return dict(EAX=(memoria.u32(GRADE_REGIOES) & 0xffffff00) | 1, EBX=marca, EDX=deslocamento)


def definir_colisao_unidade(memoria, eax, edx):
    """SetEnginCollision 0x442cb4: occupy the unit footprint at cell EDX for unit AX.

    Paths by unit type (jump table 0x442c4c): single cell (mask 1 + region tag
    sub 0, slot +0xfa); quad (cells c, c-1, c-0x101, c-0x100, each mask 1 then
    region tag sub 0..3, slots +0xfa..+0x100); type 16 quad mask 2 only; type 17
    single mask 2 only; type > 0x19 returns. EBX/ECX/ESI/EDI/EBP preserved.
    """
    indice = eax & 0xffff
    registro = (memoria.u32(PONTEIRO_UNIDADES) + indice * PASSO) & M32
    tipo = memoria.u8(registro + 1)
    if tipo > 0x19:
        return dict(EAX=(indice * PASSO & 0xffffff00) | tipo)
    caminho = CAMINHO_COLISAO[tipo]
    celulas = [edx & 0xffff]
    if caminho in (QUATRO_CELULAS, QUATRO_CELULAS_SEM_REGIAO):
        celulas += [(edx - d) & 0xffff for d in (1, 0x101, 0x100)]
    if caminho in (UMA_CELULA_SEM_REGIAO, QUATRO_CELULAS_SEM_REGIAO):
        for c in celulas:
            r = definir_colisao(memoria, c, 2)
        return dict(EAX=r['EAX'], EDX=2)
    for sub, c in enumerate(celulas):
        definir_colisao(memoria, c, 1)
        r = modificar_zona_caminho(memoria, c, indice, 2, registro + 0xfa + 2 * sub, sub)
    return dict(EAX=r['EAX'], EDX=r['EDX'])


# ------------------------------------------------------------------ fatigue
def calcular_fadiga(memoria, eax, bonus):
    """CalculFatigue 0x452cc8 for unit AX; ``bonus(jogador, tipo, seletor)`` is
    economy's BonusGetValEngin 0x428cc0 (called with AL=owner, BL=type, DL=0).

    Translated: +0x72 == 0 returns; types 11..17 return AL 1; otherwise the
    threshold u16 [0x4965dc+50*type] + u8 +0xf8 + bonus is compared with the
    incremented u16 counter +0x74, which is stored while it stays below. When
    the counter reaches the threshold (provisions/bag/death/sound, 0x452d61)
    DependenciaRamoCore is raised before the counter store. Only EAX changes.
    """
    indice = eax & 0xffff
    registro = (memoria.u32(PONTEIRO_UNIDADES) + indice * PASSO) & M32
    produto = indice * PASSO & 0xffffff00
    if memoria.u8(registro + 0x72) == 0:
        return dict(EAX=produto)
    tipo = memoria.u8(registro + 1)
    if (tipo - 0xb) & 0xff <= 6:
        return dict(EAX=1)
    if bonus is None:
        raise DependenciaRamoCore('CalculFatigue', 0x452d48, 'BonusGetValEngin provider (economy) not supplied')
    valor = bonus(memoria.u8(registro), tipo, 0) & M32
    limite = (memoria.u16(LIMITE_FADIGA + 50 * tipo) + memoria.u8(registro + 0xf8) + valor) & 0xffff
    contador = (memoria.u16(registro + 0x74) + 1) & 0xffff
    if limite <= contador:
        raise DependenciaRamoCore('CalculFatigue', 0x452d61, 'fatigue threshold reached: branch not translated')
    memoria.u16(registro + 0x74, contador)
    return dict(EAX=valor)


# ------------------------------------------------------------------ frame counter and world RNG
def avancar_quadro_jogo_memoria(memoria):
    """GameNextFrame 0x45d015 over memory: INC u32 0x496d40; no register output."""
    memoria.u32(CONTADOR_QUADRO_JOGO, memoria.u32(CONTADOR_QUADRO_JOGO) + 1)
    return {}


def aleatorio_mundo_memoria(memoria):
    """Random 0x4704dc over memory: advance u32 0x497164, EAX = new seed."""
    novo = aleatorio_caminhos(memoria.u32(SEMENTE_MUNDO))
    memoria.u32(SEMENTE_MUNDO, novo)
    return dict(EAX=novo)


# Original name -> (entry, translation(memoria, registers in, stack word 1, bonus) -> registers out)
ROTINAS = {
    'GameNextFrame': (0x45d015, lambda m, r, s, b: avancar_quadro_jogo_memoria(m)),
    'Random': (0x4704dc, lambda m, r, s, b: aleatorio_mundo_memoria(m)),
    'GetBit': (0x467d97, lambda m, r, s, b: obter_bit(r['EAX'], r['EDX'])),
    'SetBit': (0x467d71, lambda m, r, s, b: definir_bit(m, r['EAX'], r['EDX'], r['EBX'])),
    'CaseEstDecouverte': (0x4766d6, lambda m, r, s, b: caso_esta_descoberta(m, r['EAX'], r['EDX'])),
    'CaseEstIlluminee': (0x47693a, lambda m, r, s, b: caso_esta_iluminada(m, r['EAX'], r['EDX'])),
    'BatimentCollision': (0x41ab5c, lambda m, r, s, b: colisao_estrutura(m, r['EAX'], r['EDX'])),
    'BatimentGetCase': (0x41aee2, lambda m, r, s, b: caso_estrutura(m, r['EAX'])),
    'BatimentEstDecouvert': (0x419c4f, lambda m, r, s, b: estrutura_esta_descoberta(m, r['EAX'], r['EDX'])),
    'BatimentContourEstIllumine': (0x4199f9, lambda m, r, s, b: contorno_estrutura_iluminado(m, r['EAX'], r['EDX'])),
    'SetCollision': (0x47622e, lambda m, r, s, b: definir_colisao(m, r['EAX'], r['EDX'])),
    'Chemin_ModifieZone': (0x43e138, lambda m, r, s, b: modificar_zona_caminho(m, r['EAX'], r['EDX'], r['EBX'],
                                                                                r['ECX'], s)),
    'SetEnginCollision': (0x442cb4, lambda m, r, s, b: definir_colisao_unidade(m, r['EAX'], r['EDX'])),
    'CalculFatigue': (0x452cc8, lambda m, r, s, b: calcular_fadiga(m, r['EAX'], b)),
}


def provedores_core(memoria, bonus=None):
    """ai-runtime provider adapters ``provider(sitio=..., **arguments) -> EAX``.

    Keyword names follow ``laco_despachantes``: caso, jogador, estrutura, unidade.
    """
    def quadro_jogo(sitio):
        avancar_quadro_jogo_memoria(memoria)   # void: EAX unchanged, nothing to return

    return {
        'GameNextFrame': quadro_jogo,
        'Random': lambda sitio: aleatorio_mundo_memoria(memoria)['EAX'],
        'GetBit': lambda sitio, valor, bit: obter_bit(valor, bit)['EAX'],
        'SetBit': lambda sitio, endereco, bit, modo: definir_bit(memoria, endereco, bit, modo)['EAX'],
        'CaseEstDecouverte': lambda sitio, caso, jogador: caso_esta_descoberta(memoria, caso, jogador)['EAX'],
        'CaseEstIlluminee': lambda sitio, caso, jogador: caso_esta_iluminada(memoria, caso, jogador)['EAX'],
        'BatimentGetCase': lambda sitio, estrutura: caso_estrutura(memoria, estrutura)['EAX'],
        'BatimentEstDecouvert': lambda sitio, estrutura, jogador: estrutura_esta_descoberta(memoria, estrutura,
                                                                                            jogador)['EAX'],
        'BatimentContourEstIllumine': lambda sitio, estrutura, jogador: contorno_estrutura_iluminado(
            memoria, estrutura, jogador)['EAX'],
        'SetEnginCollision': lambda sitio, unidade, caso: definir_colisao_unidade(memoria, unidade, caso)['EAX'],
        'CalculFatigue': lambda sitio, unidade: calcular_fadiga(memoria, unidade, bonus)['EAX'],
    }
