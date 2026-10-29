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


# ------------------------------------------------------------------ load-tail clipping and mouse zones
RECORTE = (0x49a020, 0x49a022, 0x49a01c, 0x49a01e)   # SetClipping store order: AX, BX, DX, CX
ZONAS_MOUSE, ZONA_MAXIMA, ZONA_TESTE = 0x5099b4, 0x50a9b8, 0x50a9b4
TELA_LARGURA, TELA_ALTURA = 0x49a018, 0x49a01a        # u16 screen size used by InitGameZone mode 1
VISTA_LARGURA, VISTA_ALTURA = 0x508724, 0x508726      # u16 viewport size in cells
DESLOCAMENTO_PAINEL = 0x508f90                        # s8, sign-extended to 16 bits
JOGADOR_LOCAL = 0x508041
TIPO_CONTATO = 0x4e2e7c                               # u8 per contact id
MINIMAPA_VISIVEL = 0x497285


def definir_recorte(memoria, eax, edx, ebx, ecx):
    """SetClipping 0x40f519: u16 stores [0x49a020]=AX, [0x49a022]=BX, [0x49a01c]=DX, [0x49a01e]=CX."""
    for endereco, valor in zip(RECORTE, (eax, ebx, edx, ecx)):
        memoria.u16(endereco, valor)
    return {}


def definir_zona_mouse(memoria, eax, edx, ebx, ecx, y1):
    """MouseSetZone 0x479c50 (RET 4; ``y1`` is the pushed word): zone AX gets four zero-extended
    u16 dwords (DX, BX, CX, y1) at 0x5099b4+16*AX; u16 0x50a9b8 = AX when AX is larger."""
    indice = eax & 0xffff
    base = ZONAS_MOUSE + indice * 16
    for o, valor in enumerate((edx, ebx, ecx, y1)):
        memoria.u32(base + 4 * o, valor & 0xffff)
    if indice > memoria.u16(ZONA_MAXIMA):
        memoria.u16(ZONA_MAXIMA, indice)
    return dict(EAX=indice << 4, EDX=y1 & 0xffff)


def testar_zona_mouse(memoria, eax, edx):
    """MouseTestZone 0x479c9e: u16 [0x50a9b4]=AX, [0x50a9b6]=DX."""
    memoria.u16(ZONA_TESTE, eax)
    memoria.u16(ZONA_TESTE + 2, edx)
    return {}


def _par_u16(memoria, eax, edx, origem):
    """MiniMapGetPos/MiniMapGetTaille/MarcheGetPos/MarcheGetTaille: u16 [EAX], [EDX] from two globals."""
    primeiro, segundo = memoria.u16(origem[0]), memoria.u16(origem[1])
    memoria.u16(eax, primeiro)
    memoria.u16(edx, segundo)
    return dict(EAX=(eax & 0xffff0000) | segundo)


def posicao_minimapa(memoria, eax, edx):
    """MiniMapGetPos 0x46a1f8: [EAX] = u16 0x507d68, [EDX] = u16 0x507d6a."""
    return _par_u16(memoria, eax, edx, (0x507d68, 0x507d6a))


def tamanho_minimapa(memoria, eax, edx):
    """MiniMapGetTaille 0x46a20e: [EAX] = u16 0x496fe0, [EDX] = u16 0x496fe2."""
    return _par_u16(memoria, eax, edx, (0x496fe0, 0x496fe2))


def posicao_mercado(memoria, eax, edx):
    """MarcheGetPos 0x4620dc: [EAX] = u16 0x4e2906, [EDX] = u16 0x496f80."""
    return _par_u16(memoria, eax, edx, (0x4e2906, 0x496f80))


def tamanho_mercado(memoria, eax, edx):
    """MarcheGetTaille 0x4620f2: [EAX] = u16 0x496f7c, [EDX] = u16 0x496f7e."""
    return _par_u16(memoria, eax, edx, (0x496f7c, 0x496f7e))


def procurar_contato(memoria, eax):
    """ChercheContacteur 0x465818: AL = owner byte when 0x4e2928[owner] == 1, else 0x496f8c[owner]."""
    jogador = eax & 0xff
    if memoria.u8(0x4e2928 + jogador) == 1:
        return dict(EAX=jogador)
    return dict(EAX=memoria.u8(0x496f8c + jogador))


def caixa_mensagem_existe(memoria, eax):
    """MessageBoxExiste 0x469c33: AX = u16 0x507d56, then AL = (AX != u16 0x507d54)."""
    atual = memoria.u16(0x507d56)
    return dict(EAX=(eax & 0xffff0000) | (atual & 0xff00) | (atual != memoria.u16(0x507d54)))


def contatado_para_alianca(memoria, eax, edx):
    """PlayerEstContacterPourAlliance 0x46da1e: AL = u32 [0x5080b0 + 16*AL + 4*DL] != 0."""
    return dict(EAX=int(memoria.u32(0x5080b0 + 16 * (eax & 0xff) + 4 * (edx & 0xff)) != 0))


ZONAS_MENU = ((0x192, 0x1e6, 0x1e0, 0x223), (0x1fa, 0x1d9, 0x243, 0x22b), (0x26c, 0x1d7, 0x2b3, 0x234),
              (0x2d7, 0x1d4, 0x308, 0x221))           # zones 1..4 of modes 4 and 2 (x0, y0, x1, y1)


def _zonas_menu(memoria, eax, ebx, ecx):
    """InitGameZone modes 2, 3, 4 (jump table 0x471820 -> 0x4719be / 0x47194f / 0x47184d)."""
    m = memoria
    zona = lambda i, x0, y0, x1, y1: definir_zona_mouse(m, i, x0 & 0xffff, y0 & 0xffff, x1 & 0xffff, y1 & 0xffff)
    modo = eax & 0xffff
    if modo == 3:                                          # one zone per menu item, 0x19 apart from y 0x11e
        n = itens_menu(m, eax)['EAX'] & 0xffff
        if n > 0xff:
            raise DependenciaRamoCore('InitGameZone', 0x4719ba, f'mode 3 with {n} menu items (byte index never reaches it)')
        y = 0x11e
        for i in range(n):
            zona(i + 1, 0, y, m.u16(TELA_LARGURA), y + 0x14)
            ebx, ecx = (y & 0xff) | ((i + 1) & 0xff) << 8, m.u16(TELA_LARGURA)
            y += 0x19
        testar_zona_mouse(m, 1, n)
        return dict(EAX=1, EDX=n, EBX=ebx & M32, ECX=ecx & M32)
    for i, (x0, y0, x1, y1) in enumerate(ZONAS_MENU[:3], 1):
        zona(i, x0, y0, x1, y1)
    if modo == 4:
        zona(4, *ZONAS_MENU[3])
        zona(5, 0x121, 0x15b, 0x14f, 0x178)
        zona(6, 0x10e, 0xdf, 0x121, 0xf5)
        zona(7, 0x12b, 0xdf, 0x141, 0xf5)
    else:                                                  # mode 2: zone 4 only from mission 7 on
        if numero_missao(m, 0)['EAX'] & 0xffff >= 7:
            zona(4, *ZONAS_MENU[3])
        else:
            zona(4, 0, 0, 0, 1)
        zona(5, 0x122, 0x200, 0x14e, 0x21c)
        zona(6, 0x10e, 0xa2, 0x121, 0xb6)
        zona(7, 0x12b, 0xa2, 0x141, 0xb6)
    zona(8, 0x42, 0x2d, 0x7e, 0x57)
    testar_zona_mouse(m, 1, 8)
    return dict(EAX=1, EDX=8, EBX=0x2d, ECX=0x7e)


def iniciar_zonas_jogo(memoria, eax, edx, ebx=None, ecx=None):
    """InitGameZone 0x471830, mode AX=1 (jump table 0x471820 -> 0x471aa4): the game mouse zones.

    Zones 1..9 come from the screen size u16 0x49a018/0x49a01a; zone 0xa is the
    minimap rectangle when u8 0x497285 is set; zone 0x1a depends on the local
    player's contact type (0x4e2e7c[ChercheContacteur], asked up to three times:
    1 or 2 -> panel corner, 3 -> market rectangle); zone 0x1b on MessageBoxExiste;
    zones 0x1c..0x1f on PlayerEstContacterPourAlliance(local, p); zone 0xb on the
    screen and viewport sizes; then MouseTestZone(1, 0x1f). The panel corner uses
    the s8 0x508f90 only when the screen width is not 640. Every coordinate is
    16-bit. Registers out: EAX=1, EDX=0x1f, EBX=(H<<5)&0xffff, ECX=screen width;
    ESI/EDI preserved. Modes 2/3/4 are the menu layouts (``_zonas_menu``); any other
    mode (AX-1 > 3 unsigned) stores nothing and returns EAX-1.
    """
    modo = (eax - 1) & 0xffff
    if modo > 3:                                           # 'dec eax; cmp ax, 3; ja': nothing stored
        return dict(EAX=(eax - 1) & M32)
    if modo != 0:
        if modo == 2 and None in (ebx, ecx) and memoria.u16(0x4e2f40) == 0:
            raise ValueError('InitGameZone mode 3 with no menu item returns the caller EBX/ECX: pass them')
        return _zonas_menu(memoria, modo + 1, ebx, ecx)
    m, u16 = memoria, lambda v: v & 0xffff
    zona = lambda i, x0, y0, x1, y1: definir_zona_mouse(m, i, u16(x0), u16(y0), u16(x1), u16(y1))
    largura, altura_tela = m.u16(TELA_LARGURA), m.u16(TELA_ALTURA)
    zona(1, 0, 0, 1, 1)
    zona(2, 2, 0, largura - 3, 1)
    zona(3, largura - 2, 0, largura - 1, 1)
    zona(4, largura - 2, 2, largura - 1, altura_tela - 3)
    zona(5, largura - 2, altura_tela - 2, largura - 1, altura_tela - 1)
    zona(6, 2, altura_tela - 2, largura - 3, altura_tela - 1)
    zona(7, 0, altura_tela - 2, 1, altura_tela - 1)
    zona(8, 0, 2, 2, altura_tela - 3)
    zona(9, 0, 0, 0, 0)

    def retangulo(i, posicao, tamanho):
        # MiniMapGet*/MarcheGet* fill u16 stack locals of this routine; only their values matter.
        px, py, tx, ty = (m.u16(a) for a in posicao + tamanho)
        zona(i, px, py, px + tx, py + ty)

    if m.u8(MINIMAPA_VISIVEL):
        retangulo(0xa, (0x507d68, 0x507d6a), (0x496fe0, 0x496fe2))
    else:
        zona(0xa, 0, 0, 1, 1)
    altura = m.u16(VISTA_ALTURA)
    def painel():                     # movsx ax, byte [0x508f90]; shl 5 (read only on the branches using it)
        b = m.u8(DESLOCAMENTO_PAINEL)
        return (b | (0xff00 if b & 0x80 else 0)) << 5
    local = m.u8(JOGADOR_LOCAL)
    tipo = lambda: m.u8(TIPO_CONTATO + procurar_contato(m, local)['EAX'])
    if tipo() == 1 or tipo() == 2:
        if largura == 0x280:
            zona(0x1a, 0x2d, (altura - 1) << 5, 0x4c, (altura << 5) - 1)
        else:
            d = painel()
            zona(0x1a, d + 0x2d, ((altura - 1) << 5) - d, d + 0x4c, (altura << 5) - 1 - d)
    elif tipo() == 3:
        retangulo(0x1a, (0x4e2906, 0x496f80), (0x496f7c, 0x496f7e))
    else:
        zona(0x1a, 0, 0, 1, 1)
    if caixa_mensagem_existe(m, 0)['EAX'] & 0xff:
        d = painel()
        zona(0x1b, d, ((altura - 1) << 5) - d, d + 0x2d, (altura << 5) - d)
    else:
        zona(0x1b, 0, 0, 1, 1)
    for p in range(4):
        if p != local and contatado_para_alianca(m, local, p)['EAX']:
            d = painel()
            base = ((m.u16(VISTA_LARGURA) - 1) << 5) - 0x50 + 20 * p - d
            zona(0x1c + p, base, ((altura - 1) << 5) - d, base + 0x13, (altura << 5) - 1 - d)
        else:
            zona(0x1c + p, 0, 0, 1, 1)
    zona(0xb, 0, altura << 5, largura, altura_tela)
    testar_zona_mouse(m, 1, 0x1f)
    return dict(EAX=1, EDX=0x1f, EBX=u16(altura << 5), ECX=largura)


# ------------------------------------------------------------------ per-frame terrain/vegetation animation
GRADE_TILES, GRADE_OBJETOS, GRADE_ANIMACAO = 0x507d70, 0x507d74, 0x507dac   # u16 / u8 / u8 grid pointers
TABELA_PERMUTACAO, CURSOR_PERMUTACAO = 0x4e1c18, 0x4e1d18
CONTADOR_CICLO = 0x508f7c                    # ProgIteration cycle counter (low byte tested)
OBTER_DADOS_THREAD, DADOS_THREAD = 0x4990cc, 0x522244


def aleatorio_crt_memoria(memoria):
    """CRT rand 0x48c51d (LongRand 0x45841b jumps to it) over memory; EAX out, EDX preserved.

    The seed is the u32 at [0x522244]+0xc, reached through the thread-data getter
    [0x4990cc], which must be the single-thread 0x48e7c7; a zero pointer returns 0
    without a store. seed' = seed*0x41c64e6d + 0x3039; EAX = (seed' >> 16) & 0x7fff
    (the arithmetic of fundacoes_quadro.aleatorio_crt).
    """
    if memoria.u32(OBTER_DADOS_THREAD) != 0x48e7c7:
        raise DependenciaRamoCore('rand', 0x48c513, 'thread-data getter [0x4990cc] is not 0x48e7c7')
    ponteiro = (memoria.u32(DADOS_THREAD) + 0xc) & M32
    if ponteiro == 0:
        return dict(EAX=0)
    semente = (memoria.u32(ponteiro) * 0x41c64e6d + 0x3039) & M32
    memoria.u32(ponteiro, semente)
    return dict(EAX=semente >> 16 & 0x7fff)


def animar_terreno(memoria, eax, edx, edi=None):
    """NextAnimTerrain 0x477700 (AX, DX = viewport origin x, y) over the viewport cells.

    Per cell (tile grid [0x507d70], u16): tiles 0x5d/0x94 draw the permutation byte
    (cursor 0x4e1d18 +1) and become 0x95 when it is 0 mod 0x40; tiles 0x95..0x9c on
    an even cycle counter become t+1, and at 0x9d draw again (0x5d if even, else
    0x94); 0x251/0x252 add 4 when the animation byte [0x507dac] is nonzero;
    0x255/0x256 subtract 4; every other tile calls LongRand, and when it is 0 mod
    0x400 a tile in 0x8b..0x92 or 0x6d whose object byte [0x507d74] is 0 gets object
    0x1b. Registers out: EAX = rows walked, EDX = the routine's last EDX (needs the
    caller's ``edi`` only for a zero-width viewport with rows; None then), others kept.
    """
    m = memoria
    edx = (edx << 8) & M32
    celula = (eax + edx) & 0xffff
    edx = 0
    linha = 0
    while (linha & 0xffff) < m.u16(VISTA_ALTURA):
        coluna = 0
        while True:
            largura = m.u16(VISTA_LARGURA)
            if edi is not None:
                edi = (edi & 0xffff0000) | largura
            if (coluna & 0xffff) >= largura:
                break
            edi = celula * 2
            tiles = m.u32(GRADE_TILES)
            t = m.u16((tiles + edi) & M32)
            if t in (0x5d, 0x94):
                c = m.u8(CURSOR_PERMUTACAO)
                b = m.u8(TABELA_PERMUTACAO + c)
                m.u8(CURSOR_PERMUTACAO, (c + 1) & 0xff)
                edi, edx = 0x40, b % 0x40
                if edx == 0:
                    edx = m.u32(GRADE_TILES)
                    m.u16((edx + celula * 2) & M32, 0x95)
            elif 0x95 <= t <= 0x9c and not m.u8(CONTADOR_CICLO) & 1:
                m.u16((tiles + edi) & M32, t + 1)
                endereco = (m.u32(GRADE_TILES) + edi) & M32
                edx = m.u16(endereco)
                if edx == 0x9d:
                    c = m.u8(CURSOR_PERMUTACAO)
                    b = m.u8(TABELA_PERMUTACAO + c)
                    edi, edx = 2, b % 2
                    m.u8(CURSOR_PERMUTACAO, (c + 1) & 0xff)
                    m.u16(endereco, 0x94 if edx else 0x5d)
            else:
                t = m.u16((m.u32(GRADE_TILES) + celula * 2) & M32)
                if t in (0x251, 0x252):
                    edx = celula
                    if m.u8((m.u32(GRADE_ANIMACAO) + celula) & M32):
                        endereco = (m.u32(GRADE_TILES) + celula * 2) & M32
                        m.u16(endereco, m.u16(endereco) + 4)
                elif t in (0x255, 0x256):
                    edx = celula
                    endereco = (m.u32(GRADE_TILES) + celula * 2) & M32
                    m.u16(endereco, m.u16(endereco) - 4)
                else:
                    edi, edx = 0x400, aleatorio_crt_memoria(m)['EAX'] % 0x400
                    if edx == 0:
                        edx = m.u16((m.u32(GRADE_TILES) + celula * 2) & M32)
                        if not 0x8b <= edx < 0x93:
                            edx = m.u16((m.u32(GRADE_TILES) + celula * 2) & M32)
                        if 0x8b <= edx < 0x93 or edx == 0x6d:
                            edx = (m.u32(GRADE_OBJETOS) + celula) & M32
                            if m.u8(edx) == 0:
                                m.u8(edx, 0x1b)
            celula = (celula + 1) & 0xffff
            coluna += 1
        edx = None if edi is None else (0x100 - edi) & M32
        celula = (celula + 0x100 - largura) & 0xffff
        linha += 1
    return dict(EAX=linha & M32, EDX=edx)


def _vegetacao_celula(m, celula, r):
    """Per-cell body shared by NextAnimVeget 0x47731b.. and NextAnimVegetFullMap 0x47751f..
    (byte-identical apart from the column test). ``r`` holds the register state the
    routine carries (eax, edx, alto = ECX's upper word or None, cx = ECX's low word)."""
    baixa = lambda v, b: None if v is None else (v & 0xffffff00) | b
    r['edx'] = celula
    r['eax'] = (m.u32(GRADE_OBJETOS) + celula) & M32
    o = m.u8(r['eax'])
    r['cx'] = (r['cx'] & 0xff00) | o
    if not o:
        return
    r['eax'] = baixa(r['eax'], o)
    contador = lambda: m.u8(CONTADOR_CICLO)       # read only where the original tests it
    animacao = lambda: m.u32(GRADE_ANIMACAO)
    if 1 <= o <= 0xb:
        if not contador() & 3:
            c = m.u8(CURSOR_PERMUTACAO)
            r['alto'], r['cx'] = 0, c
            r['eax'] = baixa(r['eax'], (c + 1) & 0xff)
            m.u8(CURSOR_PERMUTACAO, (c + 1) & 0xff)
            if not m.u8(TABELA_PERMUTACAO + c) & 3:
                r['edx'] = (celula + animacao()) & M32
                v = (m.u8(r['edx']) + 1) & 3
                m.u8(r['edx'], v)
                r['eax'] = (m.u32(GRADE_ANIMACAO) & 0xffffff00) | v
    elif 0x17 <= o <= 0x1a:
        if not contador() & 1:
            r['edx'] = (celula + animacao()) & M32
            v = (m.u8(r['edx']) + 1) & 0xf
            m.u8(r['edx'], v)
            r['eax'] = (m.u32(GRADE_ANIMACAO) & 0xffffff00) | v
    elif o in (0x1b, 0x37):
        if not contador() & 1:
            m.u8((animacao() + celula) & M32, m.u8((animacao() + celula) & M32) + 1)
        r['eax'], r['edx'] = celula, m.u8((m.u32(GRADE_ANIMACAO) + celula) & M32)
        if r['edx'] == 0x10:
            m.u8((m.u32(GRADE_OBJETOS) + celula) & M32, 0)
            r['edx'] = m.u32(GRADE_ANIMACAO)
            m.u8((r['edx'] + celula) & M32, 0)
    elif 0x38 <= o <= 0x3d:
        if not contador() & 1:
            m.u8((celula + animacao()) & M32, m.u8((celula + animacao()) & M32) + 1)
        r['eax'], r['edx'] = celula, m.u8((m.u32(GRADE_ANIMACAO) + celula) & M32)
        if r['edx'] == 0x40:
            r['edx'] = (m.u32(GRADE_OBJETOS) + celula) & M32
            atual = m.u8(r['edx'])
            r['alto'], r['cx'] = 0, atual
            if atual in (0x3b, 0x38):
                m.u8(r['edx'], 0)
            else:
                m.u8(r['edx'], 0)
                m.u8((m.u32(GRADE_ANIMACAO) + celula) & M32, 0)
                r['edx'] = (m.u32(GRADE_OBJETOS) + celula) & M32
                r['cx'] = m.u8(r['edx'])
                if r['cx'] == 0:
                    r['cx'] = (atual - 1) & 0xff
                    m.u8(r['edx'], r['cx'])
            r['edx'] = m.u32(GRADE_ANIMACAO)
            m.u8((r['edx'] + celula) & M32, 0)
    elif 0x3e <= o <= 0x41:
        m.u8((animacao() + celula) & M32, m.u8((animacao() + celula) & M32) + 1)
        r['eax'] = m.u8((m.u32(GRADE_ANIMACAO) + celula) & M32)
        if r['eax'] == 0x20:
            m.u8((m.u32(GRADE_OBJETOS) + celula) & M32, 0)
            r['eax'] = m.u32(GRADE_ANIMACAO)
            m.u8((r['eax'] + celula) & M32, 0)


def animar_vegetacao(memoria, eax, edx, ecx=None):
    """NextAnimVeget 0x4772ec (AX, DX = viewport origin) over the viewport cells.

    Per cell with a nonzero object byte o ([0x507d74]) and animation byte a
    ([0x507dac]): trees 1..0xb on a cycle counter divisible by 4 draw the
    permutation byte (cursor +1) and when it is 0 mod 4 set a = (a+1)&3; 0x17..0x1a
    on even counters set a = (a+1)&0xf; 0x1b and 0x37 (a+1 on even counters) are
    removed (o = a = 0) at a == 0x10; 0x38..0x3d (a+1 on even counters) at a == 0x40
    are removed when o is 0x38/0x3b and otherwise become o-1 with a = 0; 0x3e..0x41
    (a+1 every frame) are removed at a == 0x20. Registers out: EAX/EDX as the routine
    leaves them (EAX needs the caller's ``ecx`` upper word only when no clearing
    branch ran in the last row; None then); ECX/EBX/ESI/EDI/EBP kept.
    """
    m = memoria
    edx = (edx << 8) & M32
    celula = (eax + edx) & 0xffff
    r = dict(eax=eax & M32, edx=edx, alto=None if ecx is None else ecx & 0xffff0000, cx=0)
    linha = 0
    while (linha & 0xffff) < m.u16(VISTA_ALTURA):
        coluna = 0
        while True:
            largura = m.u16(VISTA_LARGURA)
            r['cx'] = largura
            if (coluna & 0xffff) >= largura:
                break
            _vegetacao_celula(m, celula, r)
            celula = (celula + 1) & 0xffff
            coluna += 1
        r['eax'] = None if r['alto'] is None else (0x100 - (r['alto'] | largura)) & M32
        celula = (celula + 0x100 - largura) & 0xffff
        linha += 1
    return dict(EAX=r['eax'], EDX=r['edx'])


def animar_vegetacao_mapa(memoria):
    """NextAnimVegetFullMap 0x4774fa: the NextAnimVeget cell body over all 65,536 cells,
    rows 0..255 x columns 0..255 from cell 0 (network games call it at 0x42d44f instead
    of NextAnimVeget; single player never does). EAX = 0x100; every other register kept.
    """
    r = dict(eax=0, edx=0, alto=0, cx=0)
    for celula in range(65536):
        _vegetacao_celula(memoria, celula, r)
    return dict(EAX=0x100)


# ------------------------------------------------------------------ Core queries the display path calls
def _registro_unidade(memoria, eax):
    return (memoria.u32(PONTEIRO_UNIDADES) + (eax & 0xffff) * PASSO) & M32


def terreno_esta_descoberto(memoria, eax, edx):
    """TerrainEstDecouvert 0x4766f0: AL = (discovery[DL][AX] & 0x1f) == 0; EDX = grid pointer."""
    ponteiro = memoria.u32(GRADES_DESCOBERTA + 4 * (edx & 0xff))
    return dict(EAX=(eax & 0xff00) | (not memoria.u8((ponteiro + (eax & 0xffff)) & M32) & 0x1f), EDX=ponteiro)


def terreno_esta_iluminado(memoria, eax, edx):
    """TerrainEstIllumine 0x476951: the same 0x1f test on the light grid [0x507d88 + 4*DL]."""
    ponteiro = memoria.u32(GRADES_LUZ + 4 * (edx & 0xff))
    return dict(EAX=(eax & 0xff00) | (not memoria.u8((ponteiro + (eax & 0xffff)) & M32) & 0x1f), EDX=ponteiro)


def unidade_existe(memoria, eax):
    """ExisteEngin 0x441fff: AL = unit +2 != 0 (EAX = 0/1); EDX kept."""
    return dict(EAX=int(memoria.u8(_registro_unidade(memoria, eax) + 2) != 0))


def tipo_da_unidade(memoria, eax):
    """EnginGetType 0x442025: AL = unit +1 over the unit-pool pointer in EAX; EDX kept."""
    ponteiro = memoria.u32(PONTEIRO_UNIDADES)
    return dict(EAX=(ponteiro & 0xffffff00) | memoria.u8((ponteiro + (eax & 0xffff) * PASSO + 1) & M32))


def dono_da_unidade(memoria, eax):
    """EnginGetPlayer 0x442045: AL = unit +0 over the unit-pool pointer in EAX; EDX kept."""
    ponteiro = memoria.u32(PONTEIRO_UNIDADES)
    return dict(EAX=(ponteiro & 0xffffff00) | memoria.u8((ponteiro + (eax & 0xffff) * PASSO) & M32))


def _bit_unidade(memoria, eax, bit):
    return dict(EAX=memoria.u8(_registro_unidade(memoria, eax) + 0xdc) >> bit & 1)


def unidade_terror(memoria, eax):
    """EnginEstTerreur 0x45002e: GetBit(unit +0xdc, 1); EDX kept."""
    return _bit_unidade(memoria, eax, 1)


def unidade_espelho(memoria, eax):
    """EnginEstMiroir 0x44fffe: GetBit(unit +0xdc, 2); EDX kept."""
    return _bit_unidade(memoria, eax, 2)


def unidade_armadura(memoria, eax):
    """EnginEstArmure 0x450054: GetBit(unit +0xdc, 3); EDX kept."""
    return _bit_unidade(memoria, eax, 3)


def tipo_cansa(eax):
    """TypeEnginSeFatigue 0x442c34 (AL = unit type; table 0x442bcc): types 0..10 and 25 give
    AL 1, 11..24 give 0 (EAX = AL); types above 0x19 return AL 0 with EAX's upper bytes kept."""
    tipo = eax & 0xff
    if tipo > 0x19:
        return dict(EAX=eax & 0xffffff00)
    return dict(EAX=int(tipo <= 10 or tipo == 25))


def numero_missao(memoria, eax):
    """MissionGetNum 0x46c11a (Missions' getter, used by InitGameZone mode 2): AX = u8 0x496fe4."""
    return dict(EAX=(eax & 0xffff0000) | memoria.u8(0x496fe4))


def itens_menu(memoria, eax):
    """MenuGetNbItem 0x46936d (UI getter, used by InitGameZone mode 3): AX = u16 0x4e2f40."""
    return dict(EAX=(eax & 0xffff0000) | memoria.u16(0x4e2f40))


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
    'SetClipping': (0x40f519, lambda m, r, s, b: definir_recorte(m, r['EAX'], r['EDX'], r['EBX'], r['ECX'])),
    'InitGameZone': (0x471830, lambda m, r, s, b: iniciar_zonas_jogo(m, r['EAX'], r['EDX'], r['EBX'], r['ECX'])),
    'MouseSetZone': (0x479c50, lambda m, r, s, b: definir_zona_mouse(m, r['EAX'], r['EDX'], r['EBX'], r['ECX'], s)),
    'MouseTestZone': (0x479c9e, lambda m, r, s, b: testar_zona_mouse(m, r['EAX'], r['EDX'])),
    'MiniMapGetPos': (0x46a1f8, lambda m, r, s, b: posicao_minimapa(m, r['EAX'], r['EDX'])),
    'MiniMapGetTaille': (0x46a20e, lambda m, r, s, b: tamanho_minimapa(m, r['EAX'], r['EDX'])),
    'MarcheGetPos': (0x4620dc, lambda m, r, s, b: posicao_mercado(m, r['EAX'], r['EDX'])),
    'MarcheGetTaille': (0x4620f2, lambda m, r, s, b: tamanho_mercado(m, r['EAX'], r['EDX'])),
    'ChercheContacteur': (0x465818, lambda m, r, s, b: procurar_contato(m, r['EAX'])),
    'MessageBoxExiste': (0x469c33, lambda m, r, s, b: caixa_mensagem_existe(m, r['EAX'])),
    'PlayerEstContacterPourAlliance': (0x46da1e, lambda m, r, s, b: contatado_para_alianca(m, r['EAX'], r['EDX'])),
    'NextAnimTerrain': (0x477700, lambda m, r, s, b: animar_terreno(m, r['EAX'], r['EDX'], r['EDI'])),
    'NextAnimVeget': (0x4772ec, lambda m, r, s, b: animar_vegetacao(m, r['EAX'], r['EDX'], r['ECX'])),
    'LongRand': (0x45841b, lambda m, r, s, b: aleatorio_crt_memoria(m)),
    'rand': (0x48c51d, lambda m, r, s, b: aleatorio_crt_memoria(m)),
    'NextAnimVegetFullMap': (0x4774fa, lambda m, r, s, b: animar_vegetacao_mapa(m)),
    'TerrainEstDecouvert': (0x4766f0, lambda m, r, s, b: terreno_esta_descoberto(m, r['EAX'], r['EDX'])),
    'TerrainEstIllumine': (0x476951, lambda m, r, s, b: terreno_esta_iluminado(m, r['EAX'], r['EDX'])),
    'ExisteEngin': (0x441fff, lambda m, r, s, b: unidade_existe(m, r['EAX'])),
    'EnginGetType': (0x442025, lambda m, r, s, b: tipo_da_unidade(m, r['EAX'])),
    'EnginGetPlayer': (0x442045, lambda m, r, s, b: dono_da_unidade(m, r['EAX'])),
    'EnginEstTerreur': (0x45002e, lambda m, r, s, b: unidade_terror(m, r['EAX'])),
    'EnginEstMiroir': (0x44fffe, lambda m, r, s, b: unidade_espelho(m, r['EAX'])),
    'EnginEstArmure': (0x450054, lambda m, r, s, b: unidade_armadura(m, r['EAX'])),
    'TypeEnginSeFatigue': (0x442c34, lambda m, r, s, b: tipo_cansa(r['EAX'])),
    'MissionGetNum': (0x46c11a, lambda m, r, s, b: numero_missao(m, r['EAX'])),
    'MenuGetNbItem': (0x46936d, lambda m, r, s, b: itens_menu(m, r['EAX'])),
}
# Routines with a pushed argument (stack word 1 = u32 [ESP+4] at entry); the callee pops it.
ARGUMENTO_PILHA = ('Chemin_ModifieZone', 'MouseSetZone')


def _provedores_incursao(memoria, bonus):
    import incursao_core as ic
    m = memoria

    def bonus_exigido(jogador, tipo, seletor):
        if bonus is None:
            raise DependenciaRamoCore('BonusGetValEngin', 0x428cc0, 'Economy bonus provider required')
        return bonus(jogador, tipo, seletor)

    return {
        'GetFreeCell': lambda sitio, celula, tipo: ic.celula_livre(m, celula, tipo, None)['EAX'],
        'CreerEngin': lambda sitio, celula, edx, tipo, jogador: ic.criar_unidade(m, celula, edx, tipo, jogador,
                                                                                bonus_exigido)['EAX'],
        'EnginSetType': lambda sitio, unidade, caso, direcao, tipo: ic.definir_tipo_unidade(
            m, unidade, caso, direcao, tipo, bonus_exigido)['EAX'],
        'EnginSetTypeCaract': lambda sitio, unidade: ic.caracterizar_unidade(m, unidade, bonus_exigido)['EAX'],
        'EnginTypeGetCapacite': lambda sitio, tipo: ic.capacidade_tipo_engin(tipo)['EAX'],
        'EnginEnArret': lambda sitio, unidade: ic.unidade_em_arret(m, unidade)['EAX'],
        'EnginSetPlayer': lambda sitio, unidade, jogador: ic.definir_dono_unidade(m, unidade, jogador)['EAX'],
        'PlaceEngin': lambda sitio, unidade: ic.colocar_unidade(m, unidade)['EAX'],
        'SetMiniMap': lambda sitio, jogador, modo, caso: ic.definir_minimapa(m, jogador, modo, caso)['EAX'],
        'PlayerGetColor': lambda sitio, jogador: ic.cor_jogador(m, jogador)['EAX'],
        'EnginGetCase': lambda sitio, unidade: ic.caso_unidade(m, unidade)['EAX'],
        'GetRandCaseChamps': lambda sitio: ic.caso_campo_aleatoria(m)['EAX'],
        'GetRandCaseTypeBatPlayer': lambda sitio, jogador, tipo: ic.caso_estrutura_tipo_jogador(m, jogador,
                                                                                                tipo)['EAX'],
        'Chemin_Accessible': lambda sitio, origem, destino: ic.acessivel(m, origem, destino)['EAX'],
        'TerrainEnCollision': lambda sitio, caso, mascara: ic.terreno_em_colisao(m, caso, mascara)['EAX'],
        'ResetCollision': lambda sitio, caso, mascara: ic.remover_colisao(m, caso, mascara)['EAX'],
        'iaProbPost': lambda sitio, jogador, tipo, ebx, ecx, pilha: ic.postar_tarefa(m, jogador, tipo, ebx, ecx,
                                                                                      pilha)['EAX'],
        'iaProbNew': lambda sitio, tipo: ic.tarefa_nova(m, tipo)['EAX'],
        'listNewElem': lambda sitio, lista: ic.lista_novo_elemento(m, lista)['EAX'],
        'listLinkElemToTail': lambda sitio, lista, elemento: ic.lista_ligar_ao_fim(m, lista, elemento)['EAX'],
        **_provedores_movimento(memoria),
    }


def _provedores_movimento(memoria):
    """Movement and orders over Core's navigation world bound live to ``memoria`` (``mundo_vivo``), built on
    first use. They return the part the native differential validates (AL/AX/EAX as noted in RAID_CORE.md);
    routines whose callers use no result return None."""
    from movimento import celula_vizinha, direcao_entre_celulas, distancia_quadratica
    from passagem_unidades import consultar_passagem, ocupa_celula, procurar_ocupante
    estado = {}

    def w():
        if 'mundo' not in estado:
            from mundo_vivo import mundo_vivo
            from solucionador_vivo import SolucionadorCaminhosVivo
            estado['mundo'] = mundo_vivo(memoria, SolucionadorCaminhosVivo(memoria))
        return estado['mundo']

    def nada(f):
        def provedor(sitio, **argumentos):     # EAX not modeled (path-dependent); callers do not use it
            f(**argumentos)
        return provedor

    def registro(unidade, _):
        return (memoria.u32(PONTEIRO_UNIDADES) + (unidade & 0xffff) * PASSO) & M32

    return {
        # Both end every path with EAX = the unit record address (store base of their last writes).
        'SetDeplaceEngin': lambda sitio, unidade, destino: registro(
            unidade, w().definir_movimento(unidade & 0xffff, destino)),
        'ResetOrdre': lambda sitio, unidade: registro(unidade, w().redefinir_ordem(unidade & 0xffff)),
        'DeplaceEngin': nada(lambda unidade: w().deslocar(unidade & 0xffff)),
        'CalculNextCase': nada(lambda unidade: w().calcular_proxima_celula(unidade & 0xffff)),
        'AvanceEngin': nada(lambda unidade: w().avancar_passo(unidade & 0xffff)),
        'RotateEngin': nada(lambda unidade: w().girar(unidade & 0xffff)),
        'EnginNextCase': nada(lambda unidade: w().escolher_direto(unidade & 0xffff)),
        'EnginNextCaseChemin': nada(lambda unidade: w().escolher_da_rota(unidade & 0xffff)),
        'ResetEnginCollision': nada(lambda unidade, caso: w().ocupar(unidade & 0xffff, caso & 0xffff, False)),
        'EnginEstVivant': lambda sitio, unidade: int(w().viva(unidade & 0xffff)),
        'EnginOccupeCase': lambda sitio, unidade, caso, mascara: int(ocupa_celula(w(), unidade & 0xffff,
                                                                                 caso & 0xffff, mascara & 0xff)),
        'EnginPeutPasser': lambda sitio, unidade, caso, mascara: int(consultar_passagem(
            w(), unidade & 0xffff, caso & 0xffff, mascara & 0xff)[0]),
        'ChercheIndiceEngin': lambda sitio, caso: procurar_ocupante(w(), caso & 0xffff),
        'CalculDirection': lambda sitio, origem, destino: direcao_entre_celulas(origem & 0xffff, destino & 0xffff),
        'CalculDirCase': lambda sitio, caso, direcao: celula_vizinha(caso & 0xffff, direcao & 0xff, w().largura,
                                                                      w().altura),
        'Distance2d': lambda sitio, x1, y1, x2, y2: distancia_quadratica(x1, y1, x2, y2),
    }


def provedores_core(memoria, bonus=None):
    """ai-runtime provider adapters ``provider(sitio=..., **arguments) -> EAX``.

    Keyword names follow ``laco_despachantes``: caso, jogador, estrutura, unidade.
    """
    def quadro_jogo(sitio):
        avancar_quadro_jogo_memoria(memoria)   # void: EAX unchanged, nothing to return

    def vazio(funcao):
        def provedor(sitio, **argumentos):     # void routine: nothing to return
            funcao(**argumentos)
        return provedor

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
        'SetClipping': vazio(lambda eax, edx, ebx, ecx: definir_recorte(memoria, eax, edx, ebx, ecx)),
        'InitGameZone': vazio(lambda eax, edx: iniciar_zonas_jogo(memoria, eax, edx)),
        'NextAnimTerrain': vazio(lambda x, y: animar_terreno(memoria, x, y)),
        'NextAnimVeget': vazio(lambda x, y: animar_vegetacao(memoria, x, y)),
        'NextAnimVegetFullMap': vazio(lambda: animar_vegetacao_mapa(memoria)),
        'TerrainEstDecouvert': lambda sitio, caso, jogador: terreno_esta_descoberto(memoria, caso, jogador)['EAX'],
        'TerrainEstIllumine': lambda sitio, caso, jogador: terreno_esta_iluminado(memoria, caso, jogador)['EAX'],
        'ExisteEngin': lambda sitio, unidade: unidade_existe(memoria, unidade)['EAX'],
        'EnginGetType': lambda sitio, unidade: tipo_da_unidade(memoria, unidade)['EAX'],
        'EnginGetPlayer': lambda sitio, unidade: dono_da_unidade(memoria, unidade)['EAX'],
        'EnginEstTerreur': lambda sitio, unidade: unidade_terror(memoria, unidade)['EAX'],
        'EnginEstMiroir': lambda sitio, unidade: unidade_espelho(memoria, unidade)['EAX'],
        'EnginEstArmure': lambda sitio, unidade: unidade_armadura(memoria, unidade)['EAX'],
        'TypeEnginSeFatigue': lambda sitio, tipo: tipo_cansa(tipo)['EAX'],
        # M2.3 raid spawn and first order (incursao_core; keyword names follow ai-runtime's incursao_ia).
        **_provedores_incursao(memoria, bonus),
    }
