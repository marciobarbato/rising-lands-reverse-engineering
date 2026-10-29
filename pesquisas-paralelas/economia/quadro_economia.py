"""Economy routines the CalculGame frame reaches in MONDE01 (M2), over live memory.

Every entry takes ``memoria``: any object whose ``ler(endereco, tamanho)``
returns the live bytes at that original address and whose
``vista(endereco, tamanho)`` returns a writable view of them (the M1
``MapaMemoriaM1`` has both). Reads use ``ler``, writes use ``vista``.
Nothing is copied or cached between calls, so the
providers bound at those addresses (``Economia.memoria`` 0x4e2ea8,
``CicloMercado`` buffers, the unit pool ``[0x4e19a0]``, the RNG 0x497164)
are read and written by identity.

Scope (see M2_FRAME_INVENTORY.md): the routines and branches the frozen M1
state reaches. Calls the MONDE01 frames do not reach raise
``DependenciaQuadro`` at the original callee or branch address, after the
original's earlier writes, unless an exact callback is supplied. No index
guards are added: the original reads out-of-table bytes (for example
``0x4e2e7c + 0xff``) and so does this module, through ``memoria``.
"""
import struct

LOCAL = 0x508041
CONTADOR = 0x508f7c
ALEATORIO = 0x497164
UNIDADES = 0x4e19a0
RECURSOS = 0x4e2ea8
REDESENHO_RECURSOS = 0x4e05a2
INVENCOES = 0x50871c
PESQUISA = 0x5080f4
CIENTISTAS = 0x508174
TABELA_PESQUISA = 0x50817c
CONSTANTE_PESQUISA = 0x494cbb
MISSAO = 0x496fe4
ALIANCAS = 0x5080b0
ATAQUES = 0x508044
CONTATO = 0x4e2928
PARCEIRO = 0x496f8c
ESTADO_MERCADO = 0x4e2e7c


class DependenciaQuadro(NotImplementedError):
    """An original call the MONDE01 frames do not reach; earlier writes stay."""
    def __init__(self, rotina, endereco, chamada, argumentos):
        self.rotina, self.endereco, self.chamada, self.argumentos = rotina, endereco, chamada, argumentos
        super().__init__(f'{rotina} needs 0x{endereco:08x} ({chamada}) with {argumentos}')


def _u8(m, a):
    return m.ler(a, 1)[0]


def _w8(m, a, v):
    m.vista(a, 1)[0] = v & 0xff


def _u16(m, a):
    return struct.unpack('<H', m.ler(a, 2))[0]


def _w16(m, a, v):
    m.vista(a, 2)[:] = struct.pack('<H', v & 0xffff)


def _u32(m, a):
    return struct.unpack('<I', m.ler(a, 4))[0]


def _w32(m, a, v):
    m.vista(a, 4)[:] = struct.pack('<I', v & 0xffffffff)


def _f64(m, a):
    return struct.unpack('<d', m.ler(a, 8))[0]


def _wf64(m, a, v):
    m.vista(a, 8)[:] = struct.pack('<d', v)


def aleatorio(m):
    """Random 0x4704dc on the live u32 at 0x497164 (Schrage, 32-bit wrap); EAX is ignored."""
    s = _u32(m, ALEATORIO)
    quociente, resto = divmod(s, 0x1f31d)
    novo = ((resto * 0x41a7) - (quociente * 0xb14)) & 0xffffffff
    if novo == 0 or novo & 0x80000000:
        novo = (novo + 0x7fffffff) & 0xffffffff
    _w32(m, ALEATORIO, novo)
    return novo


def int_para_bcd(valor):
    """IntToBCD 0x467cd1: four bytes, units first; the thousands byte may exceed 9."""
    valor &= 0xffff
    digitos, acumulado, divisor = [0] * 4, 0, 1000
    for i in range(4):
        quociente = (valor - (acumulado & 0xffff)) // divisor
        digitos[3 - i] = quociente & 0xff
        acumulado = (acumulado + quociente * divisor) & 0xffffffff
        divisor //= 10
    return digitos


def bcd_para_int(digitos):
    """BCDToInt 0x467d3a: sum of digit·10^k, stored as u16."""
    return sum(d * 10 ** k for k, d in enumerate(digitos)) & 0xffff


def calcular_materia(m):
    """CalculMatiere 0x467718: step the local player's four displayed resource values.

    Each BCD digit of presentation +4 moves one unit toward total +2 every
    two calls, using bit c of +6: upward, a clear bit is set, a set bit
    increments and clears; downward, a clear bit decrements and sets, a set
    bit clears. An equal digit only clears a set bit. Any move or clear
    stores 1 into 0x4e05a2. The result is written back through BCDToInt.
    """
    local = _u8(m, LOCAL)
    for r in range(4):
        registro = RECURSOS + ((local * 4 + r) << 3)
        exibido = int_para_bcd(_u16(m, registro + 4))
        alvo = int_para_bcd(_u16(m, registro + 2))
        bits = registro + 6
        for c in range(4):
            d, t = exibido[c], alvo[c]
            ligado = (_u8(m, bits) >> c) & 1
            if d < t:
                _w8(m, REDESENHO_RECURSOS, 1)
                if ligado:
                    exibido[c] = (d + 1) & 0xff
                    _w8(m, bits, _u8(m, bits) & ~(1 << c))
                else:
                    _w8(m, bits, _u8(m, bits) | (1 << c))
            elif d > t:
                _w8(m, REDESENHO_RECURSOS, 1)
                if ligado:
                    _w8(m, bits, _u8(m, bits) & ~(1 << c))
                else:
                    exibido[c] = (d - 1) & 0xff
                    _w8(m, bits, _u8(m, bits) | (1 << c))
            elif ligado:
                _w8(m, bits, _u8(m, bits) & ~(1 << c))
                _w8(m, REDESENHO_RECURSOS, 1)
        _w16(m, registro + 4, bcd_para_int(exibido))


def calcular_pesquisa(m, invencao=None):
    """RechercheCalcul 0x47125c: accumulate research and detect a reached invention.

    Players 0..3 whose invention count 0x50871c[p] is below 2 look at their
    current item (branch +4, item byte +branch, 12-byte record at 0x50817c).
    An available item (marker +6 != 0xff and minimum mission +5 <= the
    mission number at 0x496fe4) adds 0.0, or 2.0 - 1/scientists (constant
    read from 0x494cbb), to the f64 at +8 and zeroes the scientist word. When
    the u32 cost is not above the accumulator, the count is incremented and
    InventionSetEffet 0x470f98 (AL=player, DL=item, BL=branch, ECX=1) runs;
    then the item advances and the accumulator is zeroed. Without
    ``invencao(jogador, item, ramo)`` that call raises ``DependenciaQuadro``
    after the count increment. An unavailable item at its end marker rotates
    the branch; a mission-gated item whose +4 byte is not 100 is skipped.
    """
    missao = _u8(m, MISSAO)
    for p in range(4):
        if _u8(m, INVENCOES + p) >= 2:
            continue
        base = PESQUISA + 16 * p

        def registro():
            ramo = _u8(m, base + 4)
            return ramo, _u8(m, base + ramo), TABELA_PESQUISA + ramo * 0x168 + _u8(m, base + ramo) * 12

        ramo, item, reg = registro()
        disponivel = _u8(m, reg + 6) != 0xff and _u8(m, reg + 5) <= missao
        if disponivel:
            cientistas = _u16(m, CIENTISTAS + 2 * p)
            incremento = 0.0 if cientistas == 0 else _f64(m, CONSTANTE_PESQUISA) - 1.0 / cientistas
            _wf64(m, base + 8, _f64(m, base + 8) + incremento)
            _w16(m, CIENTISTAS + 2 * p, 0)
            ramo, item, reg = registro()
            if float(_u32(m, reg)) > _f64(m, base + 8):
                continue
            _w8(m, INVENCOES + p, _u8(m, INVENCOES + p) + 1)
            item = _u8(m, base + _u8(m, base + 4))
            if invencao is None:
                raise DependenciaQuadro('RechercheCalcul', 0x470f98, 'InventionSetEffet',
                                        dict(AL=p, DL=item, BL=_u8(m, base + 4), ECX=1))
            invencao(p, item, _u8(m, base + 4))
        elif _u8(m, reg + 6) == 0xff:
            _w8(m, base + 4, (ramo + 1) % 4)
            continue
        elif _u8(m, reg + 4) == 100:
            continue
        ramo = _u8(m, base + 4)
        _w8(m, base + ramo, _u8(m, base + ramo) + 1)
        _w32(m, base + 8, 0)
        _w32(m, base + 12, 0)


def contar_aliancas(m, zona=None, simpatia=None):
    """PlayerInitAllianceCompteur 0x46da3b: count down the 16 alliance counters.

    A nonzero u32 at 0x5080b0+16p+4q is decremented. When the local player's
    counter reaches 0, InitGameZone 0x471830 (EAX=1, EDX=EBX=ECX=0) then
    MAJSympathie 0x475118 (EAX=q, EDX=p, EBX=9) run. Without ``zona`` the
    first raises ``DependenciaQuadro`` after the decrement; ``simpatia``
    defaults to ``atualizar_simpatia``.
    """
    for p in range(4):
        for q in range(4):
            a = ALIANCAS + 16 * p + 4 * q
            v = _u32(m, a)
            if v == 0:
                continue
            _w32(m, a, v - 1)
            if v != 1 or p != _u8(m, LOCAL):
                continue
            if zona is None:
                raise DependenciaQuadro('PlayerInitAllianceCompteur', 0x471830, 'InitGameZone',
                                        dict(EAX=1, EDX=0, EBX=0, ECX=0))
            zona()
            (simpatia or (lambda x, y, e: atualizar_simpatia(m, x, y, e)))(q, p, 9)


def calcular_simpatia_ataques(m, simpatia=None):
    """PlayerAttaqueCalculSympa 0x46d629: every 2000 frames, reward unattacked pairs.

    When u32 0x508f7c % 2000 = 0, for p, q in 0..3: a zero attack flag
    0x508044+20p+4q with p != q calls MAJSympathie 0x475118 (EAX=p, EDX=q,
    EBX=0x13); then the flag is zeroed. ``simpatia`` defaults to
    ``atualizar_simpatia``; an error leaves that pair's flag unstored.
    """
    simpatia = simpatia or (lambda x, y, e: atualizar_simpatia(m, x, y, e))
    if _u32(m, CONTADOR) % 2000:
        return
    for p in range(4):
        for q in range(4):
            a = ATAQUES + 20 * p + 4 * q
            if _u32(m, a) == 0 and p != q:
                simpatia(p, q, 0x13)
            _w32(m, a, 0)


_ESCALARES_CAMPOS = ((CONTADOR, 'I', None, 'tempo'), (0x4973ea, 'H', None, 'periodo'),
                     (0x509952, 'B', None, 'atualizar'), (0x4973e8, 'H', None, 'linha'),
                     (ALEATORIO, 'I', 'terreno', 'semente'))


def _campos(m, recursos, metodo):
    alvos = [(a, f, recursos if dono is None else getattr(recursos, dono), nome)
             for a, f, dono, nome in _ESCALARES_CAMPOS]
    for a, f, objeto, nome in alvos:
        setattr(objeto, nome, struct.unpack('<' + f, m.ler(a, struct.calcsize(f)))[0])
    try:
        metodo()
    finally:
        for a, f, objeto, nome in alvos:
            m.vista(a, struct.calcsize(f))[:] = struct.pack('<' + f, getattr(objeto, nome))


def agendar_campos(m, recursos):
    """SetUpdateChamp 0x475328 through the validated ``extracao.RecursosTerreno``.

    The counter, period, flag, row and RNG are pulled from their original
    addresses before the call and pushed back after it (also on error). The
    caller binds the provider's grids by identity; none is copied here.
    """
    _campos(m, recursos, recursos.agendar_campos)


def atualizar_campos(m, recursos):
    """UpdateChamp 0x478806 through ``extracao.RecursosTerreno``, same scalar binding.

    ``recursos.terreno.tipos``/``quantidades`` must be the live grids at
    [0x507d74]/[0x507dac], ``atributos`` [0x507da8], ``mosaicos`` the u16
    grid at [0x507d70] as bytes, and ``minas`` 0x509954.
    """
    _campos(m, recursos, recursos.atualizar_campos)


def _indice_mercado(m, jogador):
    jogador &= 0xff
    return jogador if _u8(m, CONTATO + jogador) == 1 else _u8(m, PARCEIRO + jogador)


IA_INATIVO = 0x51a990
TABELA_HANGAR = 0x4e296c


EVENTOS_SIMPATIA = 0x497288   # 16-byte records: s32 delta, mode byte +4, u32 counter +8, u32 limit +0xc


def _s32(v):
    v &= 0xffffffff
    return v - (1 << 32) if v & 0x80000000 else v


def _ajustar_simpatia(m, i, j, delta):
    """PlayerGetSympathie 0x46dc6c / PlayerSetSympathie 0x46dc90 on s16 [0x5080a8]+20i+0xc+2j, clamped to ±50."""
    endereco = (_u32(m, JOGADORES) + 20 * (i & 0xff) + 0xc + 2 * (j & 0xff)) & 0xffffffff
    atual = _u16(m, endereco)
    soma = _s32(delta + (atual - 0x10000 if atual & 0x8000 else atual))
    _w16(m, endereco, max(-50, min(50, soma)) & 0xffff)


def atualizar_simpatia(m, a, b, evento):
    """MAJSympathie 0x475118 (EAX=a, EDX=b, EBX=event).

    It returns at once when a = b, a >= 4, b >= 4 (unsigned u32), or when
    the AI context byte 0x51a990+16a, then 0x51a990+16b, is nonzero. MONDE01
    frame 0 returns here for all twelve calls (AI players 1-3 are flagged).
    Otherwise the event record at 0x497288 + 16·event (u32 wrap) counts:
    counter +8 is incremented and, while below the limit +0xc (unsigned),
    nothing else happens. At the limit the counter is zeroed and the s32
    delta +0 is added to sympathy, clamped to ±50: for every ordered pair
    i != j of players 0..3 when the mode byte +4 is 1, else for (a, b) only.
    """
    a &= 0xffffffff
    b &= 0xffffffff
    if a == b or a >= 4 or b >= 4:
        return
    if _u8(m, IA_INATIVO + 16 * a) or _u8(m, IA_INATIVO + 16 * b):
        return
    registro = (EVENTOS_SIMPATIA + (evento << 4)) & 0xffffffff
    contador = (_u32(m, registro + 8) + 1) & 0xffffffff
    _w32(m, registro + 8, contador)
    if contador < _u32(m, registro + 0xc):
        return
    modo = _u8(m, registro + 4)
    _w32(m, registro + 8, 0)
    pares = [(i, j) for i in range(4) for j in range(4) if i != j] if modo == 1 else [(a, b)]
    for i, j in pares:
        _ajustar_simpatia(m, i, j, _u32(m, registro))


METEO, METEO_ROLAGEM = 0x496d2c, 0x496d2e


def calcular_meteo(m):
    """GetMeteo 0x4290cf: weather byte 0x496d2c and the s16 drift at 0x496d2e.

    At counter % 900 = 0 the byte becomes (byte + 1) % 3, then it is always
    stored 0. At counter % 100 = 0, Random 0x4704dc % 5 < 3 increments the
    drift word, else decrements it; -5 then becomes -4 and 5 becomes 4.
    """
    contador = _u32(m, CONTADOR)
    if contador % 900 == 0:
        _w8(m, METEO, (_u8(m, METEO) + 1) % 3)
    _w8(m, METEO, 0)
    if contador % 100:
        return
    deriva = (_u16(m, METEO_ROLAGEM) + (1 if aleatorio(m) % 5 < 3 else -1)) & 0xffff
    _w16(m, METEO_ROLAGEM, deriva)
    if deriva == 0xfffb:
        _w16(m, METEO_ROLAGEM, 0xfffc)
    if _u16(m, METEO_ROLAGEM) == 5:
        _w16(m, METEO_ROLAGEM, 4)


def resetar_tabela_hangar(m):
    """ResetTableauHangar 0x461e33: the 4 x 10 u16 table at 0x4e296c (player stride 20) = 0xffff."""
    for jogador in range(4):
        for i in range(10):
            _w16(m, TABELA_HANGAR + 20 * jogador + 2 * i, 0xffff)


def numero_invencoes(m, jogador):
    """RechercheGetNbInvention 0x470554: AL = byte 0x50871c[AL & 0xff] (no range check)."""
    return _u8(m, INVENCOES + (jogador & 0xff))


JOGADORES = 0x5080a8   # DWORD pointer to the 20-byte player records
RECURSOS = 0x4e2ea8    # resource table: 4 players x 4 records x 8 bytes, +2 total
ESTRUTURAS = 0x49a0c8  # structure pool, 276 bytes per structure


def tipo_jogador(m, jogador):
    """PlayerGetType 0x46d817: AL = record byte +1 of player AL & 0xff, or 2 when that is >= 4.

    Live form of ``Mercado.tipo_jogador``; the record base is read from 0x5080a8 on every call.
    """
    j = jogador & 0xff
    return _u8(m, _u32(m, JOGADORES) + 20 * j + 1) if j < 4 else 2


def aliado(m, jogador, outro):
    """PlayerEstAllie 0x46d838: AL = 1 when AL == DL, else 0 when either is > 4, else the alliance bit.

    The bit is ``1 << DL`` tested against the sign-extended byte +6 of AL's record,
    read as the dword at +3 (``sar 24``). Indices 4 are not rejected (the original
    reads a fifth record). Live form of ``Mercado.aliado``, without its 0..3 protection.
    """
    j, k = jogador & 0xff, outro & 0xff
    if j == k:
        return 1
    if j > 4 or k > 4:
        return 0
    registro = _u32(m, _u32(m, JOGADORES) + 20 * j + 3)
    return int(bool((registro >> 24) & (1 << k)))


def recursos_suficientes(m, jogador, comida, pedra, pecas):
    """TestRessource 0x4676e5: AX food, DX stone, BX parts, player byte as the RET-4 stack argument.

    AL = 1 when each u16 cost is <= the player's total (+2 of records 1, 2, 0, compared
    in that order with unsigned jumps), else 0. No player range check. Live form of
    ``Economia.suficiente``.
    """
    base = RECURSOS + 32 * (jogador & 0xff)
    for custo, registro in ((comida, 1), (pedra, 2), (pecas, 0)):
        if custo & 0xffff > _u16(m, base + 8 * registro + 2):
            return 0
    return 1


def tipo_estrutura_viva(m, estrutura):
    """BatimentGetType 0x41a4f4: AL = byte +8 of structure AX (u16, no range check)."""
    return _u8(m, ESTRUTURAS + 276 * (estrutura & 0xffff) + 8)


def escrever_bcd(m, destino, valor):
    """IntToBCD 0x467cd1: EDX value (u16), EAX destination; byte destino+3-i = digit i (thousands first).

    The four stores happen in that order through ``vista``; see ``int_para_bcd``.
    """
    digitos = int_para_bcd(valor)
    for i in range(4):
        _w8(m, (destino + 3 - i) & 0xffffffff, digitos[3 - i])


def ler_bcd(m, destino, origem):
    """BCDToInt 0x467d3a: EAX destination word, EDX four digit bytes (units first).

    Stores 0, then adds digit k * 10**k to the word four times, rereading it each
    time, so an overlapping destination behaves as in the original.
    """
    _w16(m, destino, 0)
    for k in range(4):
        d = _u8(m, (origem + k) & 0xffffffff)
        _w16(m, destino, (_u16(m, destino) + d * 10 ** k) & 0xffff)


def bolsa_vazia(m, bolsa):
    """BagVide 0x4470b9: reads the Bag count word at EAX; EAX = (count & 0xff00) | (count == 0).

    ``mov ax,[eax]; and eax,0xffff; sete al``: AH keeps the count's high byte.
    Any address is accepted, as in the original.
    """
    contagem = _u16(m, bolsa & 0xffffffff)
    return (contagem & 0xff00) | int(contagem == 0)


CORES_JOGADORES = 0x4e24dc


def cor_jogador(m, jogador):
    """PlayerGetColor 0x46003b: EAX = 0x1e when AL = 0xc8, else the byte at 0x4e24dc + AL (upper bits cleared)."""
    jogador &= 0xff
    return 0x1e if jogador == 0xc8 else _u8(m, CORES_JOGADORES + jogador)


def calcular_contador_mercado(m, jogador):
    """CalculCompteurMarche 0x466dd1 (AL=player): read-only unless market state is 3.

    The index is the player when 0x4e2928[player] = 1, otherwise the partner
    byte 0x496f8c[player] (0xff in MONDE01, so 0x4e2e7c+0xff is read). State 3
    enters the counter branch at 0x466e01, which raises ``DependenciaQuadro``.
    """
    x = _indice_mercado(m, jogador)
    if _u8(m, ESTADO_MERCADO + x) == 3:
        raise DependenciaQuadro('CalculCompteurMarche', 0x466e01, 'state-3 counter branch',
                                dict(indice=x))


def calcular_contador_proposicao(m, jogador, edx=0):
    """CalculCompteurProposition 0x466e9b (AL=player, EDX unused): read-only unless state 4/5.

    Same index as ``calcular_contador_mercado``. State 4 (branch 0x466ed1) and
    state 5 (branch 0x466fe1) raise ``DependenciaQuadro``.
    """
    x = _indice_mercado(m, jogador)
    estado = _u8(m, ESTADO_MERCADO + x)
    if estado == 4:
        raise DependenciaQuadro('CalculCompteurProposition', 0x466ed1, 'state-4 branch',
                                dict(indice=x))
    if estado == 5:
        raise DependenciaQuadro('CalculCompteurProposition', 0x466fe1, 'state-5 branch',
                                dict(indice=x))


def ramo_producao_estrutura(producao, indice, calcular_tropa):
    """BatimentNextEtape branch 0x426918..0x42698d for structure types 1/2/13/16 (AX index).

    The branch inlines BatimentEstHabiter (the existing ``estrutura_habitada``):
    type 2 tries BagContientTroupe first and skips BagContient when it is
    nonzero. An inhabited structure then calls CalculTroupe 0x4259e6 once
    through ``calcular_tropa(indice)``, the caller's world-joined producer
    (``producao_limpa.calcular_tropa_com_limpeza_no_mundo``); its result is
    returned. An uninhabited one returns None. The exit is 0x4281c0.
    """
    from construcoes_habitaveis import estrutura_habitada
    indice &= 0xffff
    if not estrutura_habitada(producao, indice):
        return None
    return calcular_tropa(indice)


def estado_parado_unidade(m, unidade):
    """Unit state-7 body 0x456966..0x4569f0 of EnginNextEtape (DI = unit).

    Types 0–10 and 18–25 draw Random once; on a draw % 200 = 0, facing bytes
    +0x90 and +0x91 become (+0x91 % 16) + 1. Types 11–16 and 26–255 exit
    without a draw. Type 17 calls AnimBallonStatic 0x447b2f (EAX = unit),
    which raises ``DependenciaQuadro``. Exit is 0x454ccd in every case.
    """
    unidade &= 0xffff
    registro = _u32(m, UNIDADES) + unidade * 276
    tipo = _u8(m, registro + 1)
    if tipo == 17:
        raise DependenciaQuadro('EnginNextEtape state 7', 0x447b2f, 'AnimBallonStatic', dict(EAX=unidade))
    if 11 <= tipo <= 16 or tipo >= 26:
        return
    if aleatorio(m) % 200:
        return
    direcao = _u8(m, registro + 0x91) % 16 + 1
    _w8(m, registro + 0x90, direcao)
    _w8(m, registro + 0x91, direcao)
