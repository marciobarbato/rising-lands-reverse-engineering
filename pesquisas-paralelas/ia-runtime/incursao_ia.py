"""MONDE01 monster raid, AI/runtime side (M2.3): AvanceMonstre 0x47b283 with its spawn branch 0x47b349 and
pending-attack branch 0x47b44c, ConstruitGroupeMonstre 0x47a81d, StockeAction 0x47a99a, and the group kernels
iaGroupNew 0x483bd8, iagUnitAddToGroup 0x482939 and iagUnitGetFirstUnitInGroup 0x4837f0.

Translated from the intact code after the native capture ``evidencias/captura-incursao-ia.json``: frame 1 of
MONDE01 (v1) with the counter forced to 9000, the same input as Combat's 1e9f28e. That capture holds the call's
read-before-write footprint, every outside call (arguments, exit registers, net bytes written) and every byte
these routines write themselves. ``testes/test_incursao_ia.py`` replays it.

Other owners' routines are original-name providers, ``provider(sitio=<CALL address>, **arguments)``. A missing
one raises ``DependenciaIA(name, site)``:

| Provider | Owner | Arguments (original registers) | Result used |
|---|---|---|---|
| MissionGetNum | Missions | — | AX |
| Random | Core | — | EAX (EDX is preserved; the callers divide EDX:EAX) |
| PlayerGetType | Economy | jogador (AL) | AL |
| EnginGetCase | Core | unidade (AX) | AX |
| EnginGetType | Core | unidade (AX) | AL |
| GetFreeCell | Core | celula (AX), tipo (DX) | AX |
| CreerEngin | Core | celula (EAX), edx=1, tipo (EBX), jogador (ECX) | AX |
| EnginSetPlayer | Core | unidade (EAX), jogador (EDX) | — |
| PlaceEngin | Core | unidade (EAX) | — |
| GetRandCaseChamps | Core | — | AX |
| GetRandCaseTypeBatPlayer | Core | jogador (EAX), tipo (EDX) | AX |
| Chemin_Accessible | Core | origem (EAX), destino (EDX) | AL |
| ProjectileInit | Combat | tipo (EAX), origem (EDX), alvo (EBX), modo (ECX), pilha (5 words) | — |
| iaProbPost | Core task VM | jogador (EAX), tipo (EDX), ebx, ecx, pilha (4 words) | EAX (DL used) |

Paths that are not translated raise ``DependenciaIA`` at their original address before their first effect:
- the mission-0x17 attack post (0x47b2d3);
- an expired type-0x31 ambush action (0x47b3d1);
- an empty pending group (iaGroupDelete, 0x47b4a3);
- the StockeAction merge into an existing action (0x47aa07).
"""
from reinicio_ia import DependenciaIA

CONTADOR = 0x508f7c
JOGADOR_LOCAL = 0x508041
UNIDADES, PASSO_UNIDADE = 0x4e19a0, 276
# EntrerMonstre: u8 initialized flag, u16 record count, 12-byte records (+0 u16 cell, +2 u16 group mask,
# +4 u16 period, +6 u8 current group bit, +8 u32 stamp)
MONSTROS_INICIADO, MONSTROS_CONTAGEM, MONSTROS_REGISTROS = 0x50a9cc, 0x50a9ce, 0x50a9d0
SO_HUMANOS, PROBA_CAVERNA_JOGADOR, PROBA_CAVERNA_IA, PROBA_EMBOSCADA = 0x50a9bc, 0x50a9c0, 0x50a9c4, 0x50a9c8
# Group actions: u32 count, 16-byte entries (+0 u32 units, +4 u32 group, +8 u32 task/timer, +0xc u16 cell,
# +0xe u16 action)
ACOES, ACOES_ENTRADAS, ACOES_MAXIMO = 0x50ae80, 0x50ae84, 50
COMPOSICAO_GRUPOS = 0x50af84     # u8 [group * 26 + unit type]: units of that type in the monster group
PENDENTES = 0x50b134             # u8 count; the u32 group list starts at 0x50b138
MONSTROS_VIVOS = 0x50b178        # u32
CURSOR_EMBOSCADA = 0x5223d4      # u32
# IA groups: 100 records of 32 bytes; free-search cursor; list heads per (player, group type)
GRUPOS, GRUPOS_FIM, CURSOR_GRUPOS, CABECAS_GRUPOS = 0x51a9e0, 0xc80, 0x51b660, 0x51b664
TABELA_TIPO_GRUPO = 0x498ec4     # u8 at [type * 4]
GRUPO_ATUAL, UNIDADE_ATUAL = 0x51b844, 0x51b848   # iagUnitGetFirstUnitInGroup's iterator
ESPERA_EMBOSCADA = 0x1c2


def s32(v):
    v &= 0xffffffff
    return v - (1 << 32) if v & 0x80000000 else v


def _chamar(p, rotina, sitio, **argumentos):
    provedor = p.get(rotina)
    if provedor is None:
        raise DependenciaIA(rotina, sitio)
    return provedor(sitio=sitio, **argumentos)


# ------------------------------------------------------------------ group kernels
def novo_grupo(m, jogador, tipo):
    """iaGroupNew 0x483bd8 (EAX player, EDX group type) -> group index, or 0xffffffff."""
    cursor = m.u32(CURSOR_GRUPOS)
    indice, deslocamento = cursor, (cursor << 5) & 0xffffffff
    achado = None
    while s32(deslocamento) < GRUPOS_FIM:
        if m.u8(GRUPOS + deslocamento + 0x18) == 0:
            achado = indice
            break
        deslocamento += 0x20
        indice += 1
    if achado is None:
        return 0xffffffff
    g = GRUPOS + deslocamento
    m.u32(g, 0xffffffff)
    m.u32(g + 4, 0xffffffff)
    m.u16(g + 0x12, 0)
    m.u16(g + 0x14, 0x7fff)
    m.u32(g + 8, 0xffffffff)
    m.u32(g + 0xc, 0xffffffff)
    m.u16(g + 0x10, 0xffff)
    m.u8(g + 0x18, 1)
    m.u8(g + 0x19, tipo)
    m.u8(g + 0x1a, 0xff)
    m.u16(g + 0x16, 0xffff)
    m.u32(g + 0x1c, 0)
    m.u8(g + 0x1b, m.u8(TABELA_TIPO_GRUPO + 4 * tipo))
    c = m.u32(CURSOR_GRUPOS)
    m.u32(CURSOR_GRUPOS, c + 1 if s32(c) < 0x63 else 0)
    cabeca = CABECAS_GRUPOS + 0x60 * jogador + 4 * tipo
    anterior = m.u32(cabeca)
    m.u32(cabeca, achado)
    m.u32(GRUPOS + (achado << 5), anterior)
    return achado


def adicionar_ao_grupo(m, grupo, unidade):
    """iagUnitAddToGroup 0x482939 (EAX group, EDX unit) -> EAX."""
    unidade &= 0xffff
    registro = (m.u32(UNIDADES) + unidade * PASSO_UNIDADE) & 0xffffffff
    g = (GRUPOS + (grupo << 5)) & 0xffffffff
    if g == 0:
        return 0x1a1a0010
    m.u16(registro + 0x108, m.u16(g + 0x10))
    m.u32(registro + 0x10c, grupo)
    m.u16(g + 0x10, unidade)
    m.u16(g + 0x12, m.u16(g + 0x12) + 1)
    return 0


def primeira_unidade(m, grupo):
    """iagUnitGetFirstUnitInGroup 0x4837f0 (EAX group) -> AX unit or 0xffff; sets the group iterator."""
    g = (GRUPOS + (grupo << 5)) & 0xffffffff
    m.u32(GRUPO_ATUAL, g)
    if g == 0:
        return 0xffff
    m.u16(UNIDADE_ATUAL, m.u16(g + 0x10))
    return m.u16(UNIDADE_ATUAL)


# ------------------------------------------------------------------ monster group and action table
def construir_grupo_monstros(m, p, celula, grupo):
    """ConstruitGroupeMonstre 0x47a81d (AX entry cell, DL monster group)."""
    celula &= 0xffff
    grupo &= 0xff
    if grupo == 0xff or s32(m.u32(MONSTROS_VIVOS)) >= 0x32 or m.u8(PENDENTES) >= 0x10:
        return
    g = novo_grupo(m, 4, 0x10)
    if g == 0xffffffff:
        return
    for tipo in range(0x1a):
        quantidade = m.u8(COMPOSICAO_GRUPOS + grupo * 0x1a + tipo)
        for _ in range(quantidade):
            livre = _chamar(p, 'GetFreeCell', 0x47a8ec, celula=celula, tipo=tipo) & 0xffff
            if livre == 0xffff:
                continue
            unidade = _chamar(p, 'CreerEngin', 0x47a90f, celula=livre, edx=1, tipo=tipo, jogador=4) & 0xffff
            if unidade == 0xffff:
                continue
            m.u32(MONSTROS_VIVOS, m.u32(MONSTROS_VIVOS) + 1)
            _chamar(p, 'EnginSetPlayer', 0x47a938, unidade=unidade, jogador=4)
            _chamar(p, 'PlaceEngin', 0x47a93f, unidade=unidade)
            registro = (m.u32(UNIDADES) + unidade * PASSO_UNIDADE) & 0xffffffff
            efeito = 0x20 if not _chamar(p, 'Random', 0x47a954) & 1 else 0x1f
            caso = m.u16(registro + 8)
            _chamar(p, 'ProjectileInit', 0x47a8c7, tipo=efeito, origem=caso, alvo=caso, modo=0, pilha=(0,) * 5)
            adicionar_ao_grupo(m, g, unidade)
    n = m.u8(PENDENTES)
    m.u32(PENDENTES + 4 + 4 * n, g)
    m.u8(PENDENTES, n + 1)


def guardar_acao(m, p, acao, grupo, celula, origem):
    """StockeAction 0x47a99a (EAX action, EDX group, EBX cell, ECX origin cell) -> AL."""
    g = (GRUPOS + (grupo << 5)) & 0xffffffff
    if g == 0:
        return 0
    for k in range(max(0, s32(m.u32(ACOES)))):
        e = ACOES_ENTRADAS + 16 * k
        if m.u16(e + 0xc) == celula & 0xffff and m.u16(e + 0xe) == acao:
            raise DependenciaIA('StockeAction merge into an existing group action', 0x47aa07)
    n = m.u32(ACOES)
    if s32(n) >= ACOES_MAXIMO:
        return 0
    e = ACOES_ENTRADAS + 16 * n
    if acao == 0x31:
        m.u32(e, m.u16(g + 0x12))
        m.u32(e + 4, grupo)
        m.u32(e + 8, ESPERA_EMBOSCADA)
        m.u16(e + 0xc, celula)
        m.u32(ACOES, n + 1)
        m.u16(e + 0xe, acao)
        return 1
    tarefa = _chamar(p, 'iaProbPost', 0x47ab43, jogador=4, tipo=acao, ebx=grupo, ecx=celula & 0xffff,
                     pilha=(origem & 0xffff, 0, 0, 0))
    # 0x47ab4c compares the zero-extended DL with -1, which never matches.
    e = ACOES_ENTRADAS + 16 * m.u32(ACOES)
    m.u32(e, m.u16(g + 0x12))
    m.u32(e + 4, grupo)
    m.u32(e + 8, tarefa & 0xff)
    m.u16(e + 0xc, celula)
    m.u32(ACOES, m.u32(ACOES) + 1)
    m.u16(e + 0xe, acao)
    return 1


# ------------------------------------------------------------------ AvanceMonstre
def avancar_monstros(m, p):
    """AvanceMonstre 0x47b283 (player 4, every frame)."""
    if m.u8(MONSTROS_INICIADO) == 0:
        m.u8(MONSTROS_INICIADO, 1)
        for i in range(m.u16(MONSTROS_CONTAGEM)):
            m.u32(MONSTROS_REGISTROS + 12 * i + 8, m.u32(CONTADOR))
    if _chamar(p, 'MissionGetNum', 0x47b2c4) & 0xffff == 0x17:
        if m.u8(PENDENTES):
            raise DependenciaIA('AvanceMonstre mission-0x17 pending group post', 0x47b2d3)
        return
    agora = m.u32(CONTADOR)
    for k in range(m.u16(MONSTROS_CONTAGEM)):
        r = MONSTROS_REGISTROS + 12 * k
        periodo = m.u16(r + 4)
        if not periodo or s32(agora - m.u32(r + 8)) < periodo:
            continue
        mascara, bit = m.u16(r + 2), m.u8(r + 6)
        for _ in range(0x10):                       # 0x47b352: next set bit of the group mask, cyclically
            bit = (bit + 1) & 0xf
            if (1 << bit) & 0xffff & mascara:
                break
        else:
            bit = 0xff
        m.u8(r + 6, bit)
        m.u32(r + 8, agora)
        construir_grupo_monstros(m, p, m.u16(r), m.u8(r + 6))
    i = 0
    while s32(i) < s32(m.u32(ACOES)):               # 0x47b3a1: ambush actions count down
        e = ACOES_ENTRADAS + 16 * i
        if m.u16(e + 0xe) == 0x31:
            m.u32(e + 8, m.u32(e + 8) - 1)
            if s32(m.u32(e + 8)) <= 0:
                raise DependenciaIA('AvanceMonstre expired ambush action (SetDeplaceEngin/iaGroupDelete)',
                                    0x47b3d1)
        i += 1
    if not m.u8(PENDENTES):
        return
    _ataque_pendente(m, p)


def _ataque_pendente(m, p):
    """0x47b44c: order the most recent pending monster group to a cave, an ambush cell or a field."""
    while True:
        jogador = (_chamar(p, 'Random', 0x47b44e) & 3) + 1
        if jogador >= 4:
            jogador = 0
        if not m.u8(SO_HUMANOS) or _chamar(p, 'PlayerGetType', 0x47b472, jogador=jogador) & 0xff != 2:
            break
    grupo = m.u32(PENDENTES + 4 * m.u8(PENDENTES))
    unidade = primeira_unidade(m, grupo)
    if unidade == 0xffff:
        raise DependenciaIA('AvanceMonstre empty pending group (iaGroupDelete)', 0x47b4a3)
    origem = _chamar(p, 'EnginGetCase', 0x47b4c1, unidade=unidade) & 0xffff
    sorte = (_chamar(p, 'Random', 0x47b4cc) & 0xffffffff) % 100
    tipo = _chamar(p, 'EnginGetType', 0x47b4d8, unidade=unidade) & 0xff

    def tentar(acao, destino):
        if not _chamar(p, 'Chemin_Accessible', SITIOS_CAMINHO[acao], origem=origem, destino=destino) & 0xff:
            return False
        return bool(guardar_acao(m, p, acao, grupo, destino, origem) & 0xff)

    if tipo == 0x18:
        for _ in range(0x14):
            c = _chamar(p, 'GetRandCaseChamps', 0x47b4f9) & 0xffff
            if c == 0xffff:
                break
            if tentar(0x31, c):
                return _concluir(m)
    p0 = s32(m.u32(PROBA_CAVERNA_JOGADOR))
    if sorte < p0:
        jogador, modo = m.u8(JOGADOR_LOCAL), 0
    elif s32(p0 + m.u32(PROBA_CAVERNA_IA)) > sorte:
        modo = 1
    elif s32(p0 + m.u32(PROBA_CAVERNA_IA) + m.u32(PROBA_EMBOSCADA)) > sorte:
        modo = 2
    else:
        modo = 3
    if modo == 2:
        for _ in range(0x14):
            c = _celula_emboscada(m)
            if c == 0xffff:
                break
            if tentar(0x2e, c):
                return _concluir(m)
        modo = 1
    if modo <= 1:
        for _ in range(0x14):
            c = _chamar(p, 'GetRandCaseTypeBatPlayer', 0x47b654, jogador=jogador, tipo=3) & 0xffff
            if c == 0xffff:
                break
            if tentar(0x30, c):
                return _concluir(m)
    for _ in range(0x14):
        c = _chamar(p, 'GetRandCaseChamps', 0x47b69d) & 0xffff
        if c == 0xffff:
            return None
        if tentar(0x2f, c):
            return _concluir(m)
    return None


SITIOS_CAMINHO = {0x31: 0x47b512, 0x2e: 0x47b614, 0x30: 0x47b66d, 0x2f: 0x47b6b6}


def _concluir(m):
    m.u8(PENDENTES, m.u8(PENDENTES) - 1)


def _celula_emboscada(m):
    """0x47b5a8: the next EntrerMonstre record with period 0 and a cell, from the cyclic cursor."""
    b = 0
    while b < m.u16(MONSTROS_CONTAGEM):
        n = m.u16(MONSTROS_CONTAGEM)
        c = m.u32(CURSOR_EMBOSCADA) + 1
        m.u32(CURSOR_EMBOSCADA, c)
        if not s32(n) > s32(c):
            m.u32(CURSOR_EMBOSCADA, 0)
        r = MONSTROS_REGISTROS + 12 * m.u32(CURSOR_EMBOSCADA)
        if m.u16(r + 4) == 0 and m.u16(r) != 0xffff:
            return m.u16(r)
        b += 1
    return 0xffff


# ------------------------------------------------------------------ unit messages
MENSAGEM_PRIMEIRA = 0x41     # jump table 0x482998: 12 handlers for messages 0x41..0x4c
COMPORTAMENTOS = 0x498e94                                 # u32 [behaviour] -> handler table (+4, +8, +0x10 used)


def enviar_mensagem_unidade(m, p, unidade, mensagem, alvo):
    """iagUnitSendMessage 0x4829c8 (AX unit, DL message, EBX argument): message 0x49 (target found) only.

    Translated from the code; no native capture reaches it yet (the first monster scan is at counter 9008 at
    the earliest). For an AI-type-2 owner, it calls the +8 handler of the unit group's behaviour
    ``[0x498e94 + 4 * group+0x1b]`` with AX = unit and EDX = argument & 0xffff. For a monster group (type 0x10,
    behaviour 9) that handler is iabDetection_AjouteEnnemiOuAlerteConflit 0x489b5a, a provider of this front
    that is not translated yet. Other messages stop at their handler address.
    """
    unidade &= 0xffff
    registro = (m.u32(UNIDADES) + unidade * PASSO_UNIDADE) & 0xffffffff
    if _chamar(p, 'PlayerGetType', 0x482a01, jogador=m.u8(registro)) & 0xff != 2:
        return
    grupo = m.u32(registro + 0x10c)
    g = 0 if grupo == 0xffffffff else (GRUPOS + (grupo << 5)) & 0xffffffff
    indice = (mensagem - MENSAGEM_PRIMEIRA) & 0xff
    if indice > 0xb:
        return
    if mensagem & 0xff != 0x49:
        raise DependenciaIA(f'iagUnitSendMessage message 0x{mensagem & 0xff:x}', 0x482a49)
    if g == 0:
        return
    comportamento = m.u8(g + 0x1b)
    if comportamento == 0xff:
        return
    manipulador = m.u32(m.u32(COMPORTAMENTOS + 4 * comportamento) + 8)
    if manipulador == 0:
        return
    nome = MANIPULADORES.get(manipulador)
    if nome is None:
        raise DependenciaIA(f'iagUnitSendMessage 0x49 handler 0x{manipulador:x}', 0x482e2e)
    _chamar(p, nome, 0x482e2e, unidade=unidade, alvo=alvo & 0xffff)


MANIPULADORES = {0x489b5a: 'iabDetection_AjouteEnnemiOuAlerteConflit',
                 0x489ace: 'iabDetection_AjouteEnnemiSaufCivilOuAlerteConflit',
                 0x489a0f: 'iabAlerteConflitVilleOuUnite', 0x48986f: 'iabAlerteConflitMinageOuVille',
                 0x489957: 'iabAlerteConflitChampOuVille'}
