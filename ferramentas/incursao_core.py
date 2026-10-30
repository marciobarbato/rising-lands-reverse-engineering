"""Core routines of the first monster raid (M2.3) over a flat memory.

AvanceMonstre 0x47b283 (AI/runtime) spawns MONDE01's first monster group at
cycle counter 9000 through ConstruitGroupeMonstre and posts its first order
(Combat HANDOFF, M2.3). The Core routines that frame reaches are translated
here from the intact bytes. They were validated against the forced
original-first capture ``evidencias/fundacoes-quadro/captura-incursao-core-*.json``:
- GetFreeCell;
- CreerEngin, with EnginSetType (Combat's committed ``definir_tipo`` over the live
  record), EnginTypeGetCapacite and EnginEnArret;
- EnginSetPlayer;
- PlaceEngin for the monster/neutral owners, with SetEnginCollision and SetMiniMap mode 4;
- EnginGetCase, PlayerGetColor;
- GetRandCaseChamps, GetRandCaseTypeBatPlayer with GetNumIndiceTypeBatiment and
  GetCaseIndiceBatiment;
- Chemin_Accessible;
- the task list: iaProbPost, iaProbNew, listNewElem, listLinkElemToTail.

``memoria`` is the flat interface of ``chamadas_quadro_core`` (``u8/u16/u32(addr,
value=None)`` and ``ler``). Results are the exact output registers. A branch
outside the validated domain raises ``DependenciaRamoCore`` at its original
address, after the effects the original made before it.
"""
import struct

from chamadas_quadro_core import (DependenciaRamoCore, M32, PASSO, PONTEIRO_UNIDADES, aleatorio_mundo_memoria,
                                  definir_colisao_unidade, terreno_esta_iluminado)

LARGURA_MAPA, ALTURA_MAPA = 0x497168, 0x49716a        # u16 map size in cells
GRADE_ATRIBUTOS = 0x507da8                            # pointer: u8 attribute (collision) grid
GRADE_OBJETOS = 0x507d74                              # pointer: u8 object-type grid
GRADE_REGIOES = 0x4e0f38                              # pointer: u16 region grid
CLASSE_TAMANHO = 0x4962c8                             # u8 footprint class per unit type
ESTRUTURAS = 0x49a0c8                                 # 1,000 structure records of 276 bytes
COR_JOGADOR = 0x4e24dc                                # u8 colour per player
JOGADOR_LOCAL = 0x508041
MINIMAPA, MINIMAPA_UNIDADES = 0x507d5c, 0x507d60      # pointers: minimap bytes, unit layer
MINIMAPA_LARGURA, MINIMAPA_ALTURA = 0x496fe0, 0x496fe2
TIPOS_UNIDADES = 0x4965ae                             # 26 unit-type records of 50 bytes
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
POOL_TAREFAS, LISTA_LIVRE, CONTEXTOS_TAREFAS, TAREFAS_ATIVAS = 0x512320, 0x5148a0, 0x5148b0, 0x514904
ENTRADAS_PROGRAMA = 0x51a720                          # u16 rule-program entry per task type


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


def _unidade(m, indice):
    return (m.u32(PONTEIRO_UNIDADES) + (indice & 0xffff) * PASSO) & M32


# ------------------------------------------------------------------ small queries
def caso_unidade(m, eax):
    """EnginGetCase 0x44113e: AX = unit +0x7c over the pool pointer's high word; EDX kept."""
    ponteiro = m.u32(PONTEIRO_UNIDADES)
    return dict(EAX=(ponteiro & 0xffff0000) | m.u16((ponteiro + (eax & 0xffff) * PASSO + 0x7c) & M32))


def cor_jogador(m, eax):
    """PlayerGetColor 0x46003b: AL = colour[player], 0x1e for owner 200; EAX = AL."""
    jogador = eax & 0xff
    return dict(EAX=0x1e if jogador == 200 else m.u8(COR_JOGADOR + jogador))


def capacidade_tipo_engin(eax):
    """EnginTypeGetCapacite 0x4475ac (table 0x447544): crew capacity by type AL; EDX kept."""
    tipo = eax & 0xff
    return dict(EAX={5: 1, 6: 1, 7: 1, 11: 1, 14: 1, 16: 1, 12: 2, 13: 5, 15: 3, 17: 6}.get(tipo, 0))


def unidade_em_arret(m, eax):
    """EnginEnArret 0x448194 (table 0x44812c): store the stop animation +0xa4 by type.

    AL = 1 for types 0..25 (types 11..15 and 17 store nothing), AL = 0 above 25;
    EAX's upper bytes are the record address's. EBX/EDX kept.
    """
    u = _unidade(m, eax)
    tipo = m.u8(u + 1)
    if tipo > 0x19:
        return dict(EAX=u & 0xffffff00)
    animacao = {0: 2, 6: 2, 2: 7, 3: 7, 25: 7, 1: 3, 4: 3, 7: 3, 18: 3, 19: 3, 23: 3, 24: 3, 10: 6, 16: 6,
                5: 5, 9: 5, 8: 0, 21: 0, 22: 0, 20: 1}.get(tipo)
    if animacao is not None:
        m.u8(u + 0xa4, animacao)
    return dict(EAX=(u & 0xffffff00) | 1)


def definir_dono_unidade(m, eax, edx):
    """EnginSetPlayer 0x443108: owner DL into unit +0; group types 11..17 first give it to every
    member whose slot flag +0x4c is 1 (count u16 +0xa, members u16 +0x10)."""
    indice = eax & 0xffff
    dono = edx & 0xff
    u = _unidade(m, indice)
    if not 0 <= m.u8(u + 1) - 0xb <= 6:
        m.u8(u, dono)
        return dict(EAX=(eax & 0xffffff00) | dono, EDX=indice * 69)
    quantidade = m.u16(u + 0xa)
    i = 0
    while (i & 0xffff) < quantidade:
        if m.u8(u + 0xa + (i & 0xffff) + 0x42) == 1:
            membro = m.u16(u + 0xa + 2 * (i & 0xffff) + 6)
            m.u8((m.u32(PONTEIRO_UNIDADES) + membro * PASSO) & M32, dono)
        i += 1
    m.u8(u, dono)
    return dict(EAX=(i & 0xffffff00) | dono, EDX=m.u32(PONTEIRO_UNIDADES))


# ------------------------------------------------------------------ unit creation
class _BuscaPlana:
    """The navigation-search release EnginSetType makes inline (0x457bc2 / 0x457d06)."""
    def __init__(self, m):
        self.m = m

    def liberar(self, indice):
        if self.m.u16(BUSCA_UNIDADE) == indice & 0xffff:
            self.m.u8(BUSCA_OCUPADA, 0)
            self.m.u8(BUSCA_SUCESSO, 0)
            self.m.u32(BUSCA_ROTA, 0)
            self.m.u16(BUSCA_UNIDADE, 0xffff)


def caracterizar_unidade(m, eax, bonus):
    """EnginSetTypeCaract 0x457350 through Combat's committed ``caracterizar_tipo`` over a record copy.

    Recharge byte 0x4965de + 50*type. EBX/ECX/EDX kept. EAX = the type; for type 4 the
    BonusGetValEngin(owner, 4, 12) result with 0xa added to AL; above 25 the pool pointer with AL = type.
    """
    from conversao_unidades import _provedor
    provedor = _provedor()
    u = _unidade(m, eax)
    registro = bytearray(m.ler(u, PASSO))
    tipo = registro[1]
    consultas = []

    def modificador12(dono, t):
        consultas.append(bonus(dono, t, 12))
        return consultas[-1]

    provedor.caracterizar_tipo(registro, m.u8(TIPOS_UNIDADES + 0x30 + 50 * tipo), modificador12)
    for i, v in enumerate(registro):
        m.u8(u + i, v)
    if tipo > 0x19:
        return dict(EAX=(m.u32(PONTEIRO_UNIDADES) & 0xffffff00) | tipo)
    if tipo == 4:
        valor = consultas[0] if consultas else bonus(registro[0], 4, 12)
        return dict(EAX=(valor & 0xffffff00) | ((valor + 0xa) & 0xff))
    return dict(EAX=tipo)


def definir_tipo_unidade(m, eax, edx, ebx, ecx, bonus):
    """EnginSetType 0x457b87 through Combat's committed ``inicializacao_ataque.definir_tipo``.

    AX unit, DX cell, BL direction, CL type. The record is edited as a copy of its 276 bytes and
    written back whole (the original writes only what the provider writes; the rest is unchanged).
    Exit: EAX = capacity + BonusGetValEngin(owner, type, 1), EBX = 0x1d, ECX = record +0xa, EDX = 0x1e.
    """
    from conversao_unidades import _provedor
    provedor = _provedor()
    indice, tipo = eax & 0xffff, ecx & 0xff
    u = _unidade(m, indice)
    registro = bytearray(m.ler(u, PASSO))
    base = TIPOS_UNIDADES + 50 * tipo
    # The original reads the low bytes of the +2a/+2c/+30 words (0x457d4e, 0x457d5b, EnginSetTypeCaract).
    caracteristicas = provedor.CaracteristicasTipo(m.u8(base + 0x2a), m.u8(base + 0x2c), m.u8(base + 0x30))
    capacidade = {}

    def capacidade_tipo(t):
        capacidade['valor'] = capacidade_tipo_engin(t)['EAX']
        return capacidade['valor']

    def modificador(dono, t, seletor):
        valor = bonus(dono, t, seletor)
        if seletor == 1:
            capacidade['bonus'] = valor
        return valor

    provedor.definir_tipo(registro, indice, edx & 0xffff, ebx & 0xff, tipo, caracteristicas, capacidade_tipo,
                          modificador, _BuscaPlana(m))
    for i, v in enumerate(registro):
        m.u8(u + i, v)
    if 'bonus' not in capacidade:
        # Owners 4 and 200: the provider skips the query; the original calls BonusGetValEngin, whose
        # neutral-owner bypass returns 0 (Economy's provider gives the same).
        capacidade['bonus'] = bonus(registro[0], tipo, 1)
    soma = (capacidade['valor'] + capacidade['bonus']) & M32
    # The closing 30-slot clear loop leaves EBX = its last index 0x1d and EDX = 0x1e.
    return dict(EAX=soma, EBX=0x1d, ECX=(u + 0xa) & M32, EDX=0x1e)


def criar_unidade(m, eax, edx, ebx, ecx, bonus):
    """CreerEngin 0x457e6c: AX cell, DL direction, BL type, CL owner -> EAX = new unit or 0xffff.

    First unit 0..799 with state +2 == 0; group types 11..17 other than 16/17 belong to owner 200.
    Calls EnginSetType, initialises the creation fields, EnginEnArret, then BonusGetValEngin(owner,
    type 4, 12) + 10 into +0xda for type 4; types 14/16 clear +0xda.
    """
    tipo, dono = ebx & 0xff, ecx & 0xff
    ponteiro = m.u32(PONTEIRO_UNIDADES)
    indice = 0
    while indice < 800 and m.u8((ponteiro + indice * PASSO + 2) & M32):
        indice += 1
    if indice == 800:
        return dict(EAX=0xffff, EBX=800, EDX=800)
    u = (ponteiro + indice * PASSO) & M32
    m.u8(u, 0xc8 if 0 <= tipo - 0xb <= 6 and tipo not in (0x10, 0x11) else dono)
    saida = definir_tipo_unidade(m, indice, eax & 0xffff, edx & 0xff, tipo, bonus)
    for off, n, v in ((0xdc, 1, 0), (2, 1, 7), (0x9a, 2, 0x64), (0x72, 1, 0), (0x74, 2, 0), (0xc0, 2, 0xffff),
                      (0xbe, 1, 0xff), (0xbc, 1, 0xff), (0xbd, 1, 0), (0xaf, 1, 0), (0x104, 4, M32), (0x10c, 4, M32),
                      (0xf5, 1, 0), (0xf6, 1, 0), (0xf7, 1, 0), (0xf8, 1, 0), (0x110, 4, 0)):
        (m.u8, m.u16, None, m.u32)[n - 1](u + off, v)
    m.u8(u + 0x94, 1)
    m.u16(u + 4, m.u16(u + 0x76))
    i = 0
    while i < m.u16(u + 0xc):
        m.u8(u + 0x4c + i, 0)
        m.u16(u + 0x10 + 2 * i, 0)
        i += 1
    unidade_em_arret(m, indice)
    tipo_final = m.u8(u + 1)
    if tipo_final == 4:
        m.u8(u + 0xda, (bonus(m.u8(u), 4, 0xc) + 0xa) & 0xff)
    if tipo_final in (0x10, 0xe):
        m.u8(u + 0xda, 0)
        return dict(EAX=indice, EBX=indice, ECX=saida['ECX'], EDX=ponteiro)
    return dict(EAX=indice, EBX=indice, ECX=saida['ECX'], EDX=indice * 69)


# ------------------------------------------------------------------ placement
def definir_minimapa(m, eax, edx, ebx):
    """SetMiniMap 0x46a388: AL owner, DL mode, BX cell; the minimap rectangle of the cell.

    Only mode 4 (the unit layer, PlaceEngin) is translated: each pixel gets the owner colour in
    the unit layer [0x507d60] and, when the unit cell is lit for the local player, in the minimap
    [0x507d5c]. Other modes raise at their handler. EAX = rows, EBX = the pixel cursor, EDX as left.
    """
    dono, modo, celula = eax & 0xff, edx & 0xff, ebx & 0xffff
    x, y = celula % 256, celula >> 8
    mm_w, mm_h, w, h = m.u16(MINIMAPA_LARGURA), m.u16(MINIMAPA_ALTURA), m.u16(LARGURA_MAPA), m.u16(ALTURA_MAPA)
    if not w or not h:
        raise DependenciaRamoCore('SetMiniMap', 0x46a3dc, 'zero map size divides by zero')
    px, py = x * mm_w // w, y * mm_h // h
    sx, sy = mm_w // w, mm_h // h
    sx, sy = sx if sx & 0xffff else 1, sy if sy & 0xffff else 1
    cursor = ((py & 0xffff0000) | ((py * mm_h) & 0xffff)) + px
    edx_saida = sx
    if modo - 1 & 0xff <= 6 and modo != 4:
        raise DependenciaRamoCore('SetMiniMap', (0x46a49f, 0x46a4d9, 0x46a528, None, 0x46a5a6, 0x46a647,
                                                 0x46a69d)[modo - 1 & 0xff], f'mode {modo}')
    linha = 0
    while (linha & 0xffff) < (sy & 0xffff):
        coluna = 0
        while (coluna & 0xffff) < (sx & 0xffff):
            if modo == 4:
                pixel = cursor & 0xffff
                cor = cor_jogador(m, dono)['EAX']
                m.u8((m.u32(MINIMAPA_UNIDADES) + pixel) & M32, cor)
                local = m.u8(JOGADOR_LOCAL)
                luz = terreno_esta_iluminado(m, celula, local)
                edx_saida = luz['EDX']
                if luz['EAX'] & 0xff:
                    cor = cor_jogador(m, dono)['EAX']
                    edx_saida = (edx_saida & 0xffffff00) | cor
                    m.u8((m.u32(MINIMAPA) + pixel) & M32, cor)
            coluna += 1
            cursor = (cursor + 1) & M32
        linha += 1
        cursor = (cursor + 0x80 - sx) & M32
    return dict(EAX=linha & M32, EBX=cursor, EDX=edx_saida & M32)


def colocar_unidade(m, eax):
    """PlaceEngin 0x456fa6 for owners 4 and 200: SetEnginCollision(unit, +8), +0x72 = 1, then
    SetMiniMap(owner, 4, +8). Other owners discover and light terrain first (DecouvreTerrain
    0x476851 / IllumineTerrain 0x476cb3), outside this flat translation: they raise at 0x457019
    after the collision and +0x72 stores, as the world provider ``colocacao_missao`` does."""
    indice = eax & 0xffff
    u = _unidade(m, indice)
    definir_colisao_unidade(m, indice, m.u16(u + 8))
    m.u8(u + 0x72, 1)
    u = _unidade(m, indice)
    dono = m.u8(u)
    if dono not in (4, 200):
        raise DependenciaRamoCore('PlaceEngin', 0x457019, f'terrain discovery/illumination for owner {dono}')
    return dict(EAX=definir_minimapa(m, dono, 4, m.u16(u + 8))['EAX'])


def terreno_em_colisao(m, eax, edx):
    """TerrainEnCollision 0x4761d4: EAX = attribute[AX] & DL != 0; EDX kept."""
    return dict(EAX=int(bool(m.u8((m.u32(GRADE_ATRIBUTOS) + (eax & 0xffff)) & M32) & (edx & 0xff))))


def terreno_esta_gc(m, eax):
    """TerrainEstGc 0x4762b9: EAX = 1 when the object byte [[0x507d74] + AX] is in 0x1d..0x34, else 0 (the byte is
    zero-extended into EAX before AL is set, so the upper bits are 0); EDX kept (pushed); nothing else touched."""
    objeto = m.u8((m.u32(GRADE_OBJETOS) + (eax & 0xffff)) & M32)
    return dict(EAX=int(0x1d <= objeto < 0x35))


def remover_colisao(m, eax, edx):
    """ResetCollision 0x47623e: attribute[AX] &= ~DL; EAX = AX, DL = ~DL."""
    endereco = (m.u32(GRADE_ATRIBUTOS) + (eax & 0xffff)) & M32
    m.u8(endereco, m.u8(endereco) & ~edx & 0xff)
    return dict(EAX=eax & 0xffff, EDX=(edx & 0xffffff00) | (~edx & 0xff))


def memset_crt(m, eax, edx, ebx):
    """CRT memset 0x48c3b0 (Watcom: EAX dest, DL byte, EBX count) through __STOSB 0x48d890.

    Reads the first destination byte (CMP at 0x48d894) when the count is not 0. EAX/EBX/ECX
    kept; EDX = DL repeated in all four bytes.
    """
    valor, n = edx & 0xff, ebx & M32
    if n:
        m.u8(eax)
    for i in range(n):
        m.u8((eax + i) & M32, valor)
    return dict(EDX=valor * 0x01010101)


# ------------------------------------------------------------------ free cell
def celula_livre(m, eax, edx, esp):
    r = _celula_livre(m, eax, edx, esp)
    return r if esp is not None else dict(EAX=r['EAX'] & 0xffff)


def _celula_livre(m, eax, edx, esp):
    """GetFreeCell 0x479f20: AX centre cell, DX unit type -> EAX = first free cell of rings 1..29.

    Each ring k tests the row y-k (x-k..x+k), the row y+k, then the columns x-k and x+k, in
    the original's arithmetic. The cell values are 32-bit sums whose 16-bit locals' upper words are
    never written: they hold stack residue read at their original slots (ESP - 0x32, -0x1a,
    -0x3a, -0x2e). The column sides test an x-based counter against the map height and their
    first cell lags the row by one, as in the original. Type class (0x4962c8) 0 or above 3 takes
    the first candidate; 1 tests the attribute mask; 2..3 test a 2x2 footprint up-left.
    EAX = 0xffff when the centre is off the map or no ring has a free cell; other registers kept.

    With ``esp=None`` (no native stack) the residue is not read and only AX is returned: AX, the
    cells tested and the search order do not depend on the residue (the callers read AX).
    """
    a = eax & M32
    x, y = a & 0xff, (a & 0xffff) >> 8
    w = m.u16(LARGURA_MAPA)
    if w <= x:
        return dict(EAX=0xffff)
    h = m.u16(ALTURA_MAPA)
    if h <= y:
        return dict(EAX=0xffff)
    tipo = edx & 0xffff
    mascara = 2 if tipo in (0x10, 0x11) else 1
    classe = m.u8(CLASSE_TAMANHO + tipo)
    residuo = (lambda d: 0) if esp is None else (lambda d: m.u16((esp - d) & M32))

    def livre(c):
        if classe < 1 or classe > 3:
            return True
        atributos = m.u32(GRADE_ATRIBUTOS)
        teste = lambda cc: m.u8((atributos + (cc & 0xffff)) & M32) & mascara
        if classe == 1:
            return not teste(c)
        if not c & 0xff or not (c & 0xffff) >> 8:
            return False
        return not (teste(c) or teste(c - 1) or teste(c - 0x101) or teste(c - 0x100))

    for k in range(1, 30):
        canto = (a - k - ((residuo(0x32) << 16) | (k << 8 & 0xffff))) & M32
        if not y - k < 0:
            c = canto
            for coluna in range(x - k, x + k + 1):
                if 0 <= coluna <= w and livre(c):
                    return dict(EAX=c)
                c = (c + 1) & M32
        if h > y + k:
            c = (canto + ((residuo(0x1a) << 16) | (k << 9 & 0xffff))) & M32
            for coluna in range(x - k, x + k + 1):
                if 0 <= coluna <= w and livre(c):
                    return dict(EAX=c)
                c = (c + 1) & M32
        if not x - k < 0:
            palavra = canto & 0xffff
            for i in range(2 * k - 1):
                if not (y + 1 - k + i < 0 or x + 1 - k + i >= h):
                    c = (residuo(0x3a) << 16) | palavra
                    if livre(c):
                        return dict(EAX=c)
                palavra = (palavra & 0xff) | (((palavra >> 8) + 1) & 0xff) << 8
        if w > x + k:
            palavra = (canto + 2 * k) & 0xffff
            for i in range(2 * k - 1):
                if not (y + 1 - k + i < 0 or x + 1 - k + i >= h):
                    c = (residuo(0x2e) << 16) | palavra
                    if livre(c):
                        return dict(EAX=c)
                palavra = (palavra & 0xff) | (((palavra >> 8) + 1) & 0xff) << 8
    return dict(EAX=0xffff)


# ------------------------------------------------------------------ order targets
def caso_campo_aleatoria(m):
    """GetRandCaseChamps 0x489147: Random % n over the cells whose object type is 0x1c (column-major
    scan, at most 201 kept); 0xffff when none. The 201st entry lands on the scan's own column bound
    and is returned + 1, as the original's 200-entry stack buffer does. Other registers kept."""
    tipos = m.u32(GRADE_OBJETOS)
    celulas = []
    for x in range(256):
        if len(celulas) > 200:
            break
        for c in range(x, 0x10000 + x, 0x100):
            if len(celulas) > 200:
                break
            if m.u8((tipos + c) & M32) == 0x1c:
                celulas.append(c)
    if not celulas:
        return dict(EAX=0xffff)
    if len(celulas) == 201:
        celulas[200] += 1
    return dict(EAX=celulas[aleatorio_mundo_memoria(m)['EAX'] % len(celulas)])


def indice_tipo_estrutura(m, eax, edx, ebx):
    """GetNumIndiceTypeBatiment 0x41db24: first structure i >= AX (u16 < 1000) with +4 == BL and
    +8 == DL -> EAX = EDX = i; 0xffff (EDX = the end index) when none. BH = BL, BL = last +4 read."""
    edx_i, alvo4, alvo8 = eax & M32, ebx & 0xff, edx & 0xff
    ebx_saida = (ebx & 0xffff0000) | alvo4 << 8 | alvo4
    while (edx_i & 0xffff) < 1000:
        e = ESTRUTURAS + (edx_i & 0xffff) * PASSO
        lido = m.u8(e + 4)
        ebx_saida = (ebx_saida & 0xffffff00) | lido
        if lido == alvo4 and m.u8(e + 8) == alvo8:
            return dict(EAX=edx_i, EDX=edx_i, EBX=ebx_saida)
        edx_i = (edx_i + 1) & M32
    return dict(EAX=0xffff, EDX=edx_i, EBX=ebx_saida)


def caso_indice_estrutura(m, eax):
    """GetCaseIndiceBatiment 0x41aab2: AX = structure +2 over (index*69)'s high word; EDX kept."""
    i = eax & 0xffff
    return dict(EAX=((i * 69) & 0xffff0000) | m.u16(ESTRUTURAS + 2 + i * PASSO))


def caso_estrutura_tipo_jogador(m, eax, edx):
    """GetRandCaseTypeBatPlayer 0x489300: cell of a random structure with +4 == AL and +8 == DL.

    Collects the matches of GetNumIndiceTypeBatiment from 0 into a 200-entry stack buffer; more than
    200 would overwrite the saved registers and raise at 0x48933f. EAX = 0xffff when none; else
    Random % n picks one and EAX = GetCaseIndiceBatiment & 0xffff, EDX = the remainder.
    """
    achados, inicio = [], 0
    while True:
        r = indice_tipo_estrutura(m, inicio, edx & 0xff, eax & 0xff)
        if r['EAX'] & 0xffff == 0xffff:
            break
        if len(achados) == 200:
            raise DependenciaRamoCore('GetRandCaseTypeBatPlayer', 0x48933f, 'more than 200 structures')
        achados.append(r['EAX'] & 0xffff)
        inicio = (r['EAX'] & 0xffff) + 1
    if not achados:
        return dict(EAX=0xffff, EDX=r['EDX'])
    resto = aleatorio_mundo_memoria(m)['EAX'] % len(achados)
    return dict(EAX=caso_indice_estrutura(m, achados[resto])['EAX'] & 0xffff, EDX=resto)


def _regiao_efetiva(m, r):
    """The region word Chemin_Accessible compares: structure (bit 15) and unit (bit 14) cells take
    the region of their footprint slot; returns (word, EAX left by the computation or None)."""
    if r & 0x8000:
        i = (r & 0x7fe0) >> 5
        return m.u16(0x49a194 + i * PASSO + 2 * (r & 0x1f)), 69 * i
    if r & 0x4000:
        i = (r & 0x3ff8) >> 3
        unidades = m.u32(PONTEIRO_UNIDADES)
        return m.u16((unidades + i * PASSO + 0xfa + 2 * (r & 3)) & M32), (unidades + i * PASSO) & M32
    return r, None


def acessivel(m, eax, edx):
    """Chemin_Accessible 0x42d4f8: AL = both cells on the map and in the same region; EBX/ECX kept."""
    a, b = eax & 0xffff, edx & 0xffff
    w, h = m.u16(LARGURA_MAPA), m.u16(ALTURA_MAPA)
    if (a & 0xff) >= w or (b & 0xff) >= w:
        return dict(EAX=eax & 0xffffff00)
    if (a >> 8) >= h:
        return dict(EAX=0)
    if (b >> 8) >= h:
        return dict(EAX=b & 0xff00, EDX=b >> 8)
    regioes = m.u32(GRADE_REGIOES)
    ra, rb = m.u16((regioes + 2 * a) & M32), m.u16((regioes + 2 * b) & M32)
    eax_saida = b
    va, eax_a = _regiao_efetiva(m, ra)
    if eax_a is not None:
        eax_saida = eax_a
    vb, eax_b = _regiao_efetiva(m, rb)
    if eax_b is not None:
        eax_saida = eax_b
        edx_saida = vb
    else:
        edx_saida = (regioes & 0xffff0000) | rb
    return dict(EAX=(eax_saida & 0xffffff00) | int(va == vb), EDX=edx_saida)


# ------------------------------------------------------------------ task list
def lista_novo_elemento(m, eax):
    """listNewElem 0x47d012: pop the head of the free list at EAX (head, count, size, base)."""
    cabeca = eax & M32
    indice = m.u32(cabeca)
    if indice != M32:
        elemento = (m.u32(cabeca + 8) * indice + m.u32(cabeca + 0xc)) & M32
        m.u32(cabeca, m.u32(elemento))
        m.u32(elemento, M32)
        m.u32(cabeca + 4, (m.u32(cabeca + 4) - 1) & M32)
    return dict(EAX=indice)


def lista_ligar_ao_fim(m, eax, edx):
    """listLinkElemToTail 0x47d07a: append element EDX to the list at EAX -> EAX = EDX = element
    (-1 links nothing); EDX = size * element after a link."""
    cabeca, elemento = eax & M32, edx & M32
    if elemento == M32:
        return dict(EAX=M32)
    tamanho, base = m.u32(cabeca + 8), m.u32(cabeca + 0xc)
    anterior = m.u32(cabeca)
    if anterior == M32:
        m.u32(cabeca, elemento)
    else:
        while (seguinte := m.u32((tamanho * anterior + base) & M32)) != M32:
            anterior = seguinte
        m.u32((tamanho * anterior + base) & M32, elemento)
    m.u32((tamanho * elemento + base) & M32, M32)
    m.u32(cabeca + 4, (m.u32(cabeca + 4) + 1) & M32)
    return dict(EAX=elemento, EDX=(tamanho * elemento) & M32)


def tarefa_nova(m, eax):
    """iaProbNew 0x47d7ec: a task of type EAX (1..63 with a program entry) from the free list."""
    tipo = eax & M32
    if tipo == 0 or _s32(tipo) >= 0x40:
        return dict(EAX=M32)
    entrada = m.u16((ENTRADAS_PROGRAMA + 2 * tipo) & M32)
    if not entrada:
        return dict(EAX=M32)
    indice = lista_novo_elemento(m, LISTA_LIVRE)['EAX']
    if indice == M32:
        return dict(EAX=M32)
    t = (POOL_TAREFAS + indice * 96) & M32
    m.u32(TAREFAS_ATIVAS, (m.u32(TAREFAS_ATIVAS) + 1) & M32)
    m.u32(t + 4, M32)
    m.u32(t + 8, M32)
    m.u16(t + 0x5a, tipo)
    m.u16(t + 0x58, 0)
    m.u8(t + 0x5e, 0)
    m.u8(t + 0x5f, 0)
    m.u32(t + 0x10, 0)
    m.u8(t + 0x5d, 0xff)
    m.u32(t + 0x14, 0)
    m.u32(t + 0xc, entrada)
    return dict(EAX=indice)


def postar_tarefa(m, eax, edx, ebx, ecx, pilha):
    """iaProbPost 0x47d920: new task EDX for player AL, arguments EBX, ECX and the four stack words,
    linked to the tail of the player's list (0x5148b0 + 16*EAX). EAX = EBX = task or -1."""
    indice = tarefa_nova(m, edx)['EAX']
    if indice == M32:
        return dict(EAX=M32, EBX=M32)
    t = (POOL_TAREFAS + indice * 96) & M32
    for off, v in zip(range(0x18, 0x30, 4), (ebx, ecx, *pilha[:4])):
        m.u32(t + off, v & M32)
    m.u8(t + 0x5c, eax & 0xff)
    ligado = lista_ligar_ao_fim(m, (CONTEXTOS_TAREFAS + (eax << 4)) & M32, indice)
    return dict(EAX=indice, EBX=indice, EDX=ligado['EDX'])


# Original name -> (entry, translation(memoria, registers in, stack words after the return, bonus)
# -> changed registers). ``bonus(owner, type, selector)`` is Economy's BonusGetValEngin provider.
ROTINAS = {
    'EnginGetCase': (0x44113e, lambda m, r, p, b: caso_unidade(m, r['EAX'])),
    'PlayerGetColor': (0x46003b, lambda m, r, p, b: cor_jogador(m, r['EAX'])),
    'EnginTypeGetCapacite': (0x4475ac, lambda m, r, p, b: capacidade_tipo_engin(r['EAX'])),
    'EnginEnArret': (0x448194, lambda m, r, p, b: unidade_em_arret(m, r['EAX'])),
    'EnginSetPlayer': (0x443108, lambda m, r, p, b: definir_dono_unidade(m, r['EAX'], r['EDX'])),
    'EnginSetTypeCaract': (0x457350, lambda m, r, p, b: caracterizar_unidade(m, r['EAX'], b)),
    'EnginSetType': (0x457b87, lambda m, r, p, b: definir_tipo_unidade(m, r['EAX'], r['EDX'], r['EBX'], r['ECX'], b)),
    'CreerEngin': (0x457e6c, lambda m, r, p, b: criar_unidade(m, r['EAX'], r['EDX'], r['EBX'], r['ECX'], b)),
    'SetMiniMap': (0x46a388, lambda m, r, p, b: definir_minimapa(m, r['EAX'], r['EDX'], r['EBX'])),
    'PlaceEngin': (0x456fa6, lambda m, r, p, b: colocar_unidade(m, r['EAX'])),
    'GetFreeCell': (0x479f20, lambda m, r, p, b: celula_livre(m, r['EAX'], r['EDX'], r['ESP'])),
    'GetRandCaseChamps': (0x489147, lambda m, r, p, b: caso_campo_aleatoria(m)),
    'GetNumIndiceTypeBatiment': (0x41db24, lambda m, r, p, b: indice_tipo_estrutura(m, r['EAX'], r['EDX'], r['EBX'])),
    'GetCaseIndiceBatiment': (0x41aab2, lambda m, r, p, b: caso_indice_estrutura(m, r['EAX'])),
    'GetRandCaseTypeBatPlayer': (0x489300, lambda m, r, p, b: caso_estrutura_tipo_jogador(m, r['EAX'], r['EDX'])),
    'Chemin_Accessible': (0x42d4f8, lambda m, r, p, b: acessivel(m, r['EAX'], r['EDX'])),
    'TerrainEnCollision': (0x4761d4, lambda m, r, p, b: terreno_em_colisao(m, r['EAX'], r['EDX'])),
    'TerrainEstGc': (0x4762b9, lambda m, r, p, b: terreno_esta_gc(m, r['EAX'])),
    'ResetCollision': (0x47623e, lambda m, r, p, b: remover_colisao(m, r['EAX'], r['EDX'])),
    'memset': (0x48c3b0, lambda m, r, p, b: memset_crt(m, r['EAX'], r['EDX'], r['EBX'])),
    'listNewElem': (0x47d012, lambda m, r, p, b: lista_novo_elemento(m, r['EAX'])),
    'listLinkElemToTail': (0x47d07a, lambda m, r, p, b: lista_ligar_ao_fim(m, r['EAX'], r['EDX'])),
    'iaProbNew': (0x47d7ec, lambda m, r, p, b: tarefa_nova(m, r['EAX'])),
    'iaProbPost': (0x47d920, lambda m, r, p, b: postar_tarefa(m, r['EAX'], r['EDX'], r['EBX'], r['ECX'], p)),
}


def traducao_core(nome):
    """translation(memoria, registers, stack words, bonus) for a raid routine or a frame-1 Core routine
    (``chamadas_quadro_core.ROTINAS``; its pushed-argument routines take the first stack word); None
    when Core has no translation."""
    import chamadas_quadro_core as cq
    if nome in ROTINAS:
        return ROTINAS[nome][1]
    if nome in cq.ROTINAS:
        f = cq.ROTINAS[nome][1]
        return lambda m, r, p, b: f(m, r, p[0] if nome in cq.ARGUMENTO_PILHA else None, b)
    return None
