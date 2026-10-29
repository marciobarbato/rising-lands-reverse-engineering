"""Input, icon and menu routines reached by MONDE01 frames 0 and 1 (no human input).

Translated after the original entry/return captures at the exact frame-0/1
inputs (``evidencias/captura-entradas-quadro1-ia-v2.json``, commit ``4e10cdd``),
following exactly the executed basic blocks recorded there:

- ``entrada_jogo``: InputGame 0x429278 with its callees MouseZone 0x479cac,
  ScrollTerrain 0x472068 (direction 0: the cursor-(0, 0) edge scroll of
  0x508720/22) and NextGouttes 0x45ac31;
- ``enviar_entrada``: InputSend 0x45ec9f with ReseauActif 0x42c3b0;
- ``calcular_icone_acao``: CalculIconeAction 0x45e944 with EnginGetNbSelection
  0x4721ce and BatimentGetSelection 0x41a4b6;
- ``iniciar_menu``: MenuInit 0x4682bb on the load-tail path (entry state 0 to
  0x12).

Every conditional branch the captures did not take raises
``DependenciaIA(description, original address)`` before its first effect.
``m`` serves u8/u16/u32 at original addresses (``MemoriaMapaM1`` or a
``MemoriaDeclarada``). ``registro`` records bindings and boundaries in the
capture's fields. ``janelas`` answers the declared Windows calls.
``provedores`` holds other owners' routines (InitGameZone is Core's). Register
values are returned where callers or recorded events consume them.
"""
from memoria_ia_runtime import s32
from reinicio_ia import DependenciaIA

TECLAS = ((0x1b, 0x429300), (0x10, 0x429556), (0x11, 0x4295fc), (0x2e, 0x42967e), (0x12, 0x4296ad),
          (0x20, 0x4296dc), (0x26, 0x4296f1), (0x28, 0x42970b), (0x27, 0x429732), (0x25, 0x42974c),
          (0x0d, 0x429773), (0x58, 0x429781))
CAMINHO_PIE, NOME_PIE = 0x509494, 0x494a4d


def _parar(descricao, endereco):
    raise DependenciaIA(descricao, endereco)


def _sx16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


def _idiv(a, b):
    """x86 signed IDIV: quotient truncates toward zero; remainder has the dividend's sign."""
    q = abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1)
    return q, a - q * b


def zona_mouse(m):
    """MouseZone 0x479cac: first zone [u16 0x50a9b4 .. u16 0x50a9b6] whose rectangle holds the cursor."""
    x, y = m.u16(0x5099a8), m.u16(0x5099aa)
    zona = m.u16(0x50a9b4)
    while zona <= m.u16(0x50a9b6):
        r = 0x5099b4 + 16 * zona
        if s32(m.u32(r)) <= x and s32(m.u32(r + 4)) <= y and x <= s32(m.u32(r + 8)) and y <= s32(m.u32(r + 12)):
            return zona
        zona = (zona + 1) & 0xffff
    return 0                                    # 0x479d06: xor eax, eax


def rolar_terreno(m, ex, ey, zona, passos):
    """ScrollTerrain 0x472068 (EAX=&x, EDX=&y, EBX=zone, ECX=steps): direction = zone - 1."""
    direcao = (zona - 1) & 0xffffffff
    for _ in range(passos & 0xffff):
        if direcao & 0xffff > 7:
            continue
        if direcao != 0:
            _parar(f'ScrollTerrain direction {direcao}', 0x472048 + 4 * direcao)
        if s32(m.u16(ex)) > 0:
            m.u16(ex, m.u16(ex) - 1)
        if s32(m.u16(ey)) > 0:
            m.u16(ey, m.u16(ey) - 1)


def proximas_gotas(m):
    """NextGouttes 0x45ac31: rain mode u8 0x496d2c = 1 with negative wind (s16 0x496d2e)."""
    vento = _sx16(m.u16(0x496d2e))
    if vento >= 0:
        _parar('NextGouttes non-negative wind', 0x45ac56)
    forca = (-(m.u8(0x496d2e))) & 0xff
    modo = m.u8(0x496d2c)
    if modo == 2:
        _parar('NextGouttes mode 2', 0x45ac6b)
    if modo != 1:
        return
    for i in range(0x78):
        r = 0x4e1da0 + 6 * i
        _, y = _idiv(_sx16(m.u16(r + 2)) + 0x14, 0x1be)
        m.u16(r + 2, y)
        if vento > 0:
            _parar('NextGouttes positive wind', 0x45ad5e)
        if vento < 0:
            passo, _ = _idiv(0x14, 5 - forca)
            _, x = _idiv(_sx16(m.u16(r)) - passo + 0x1fe, 0x1fe)
            m.u16(r, x)
        _, quadro = _idiv(m.u8(r + 4) + 1, 4)
        m.u8(r + 4, quadro)


def entrada_jogo(m, jogador, registro, janelas, provedores=None):
    """InputGame 0x429278 (AL = player), no-human-input path; zone 0 (cursor over the map) hovers."""
    m.u16(0x49a010, 0x1dd8)
    m.u16(0x4e0612, 0)
    m.u16(0x4e0614, 0)
    m.u32(0x49a014, 0)
    m.u16(0x4e0616, 0)
    m.u8(0x508f8f, 0)
    m.u8(0x4e17ac, 0)
    m.u16(0x4e0618, 0)
    for a in (0x496d4a, 0x496ac2, 0x496ac4):
        m.u16(a, 0xffff)
    teclas = iter(TECLAS)

    def tecla(nao_pressionada):
        vk, retorno = next(teclas)
        resposta = janelas.tecla(vk) & 0xffffffff
        registro.vinculo('USER32.GetAsyncKeyState', (vk,), retorno, resposta)
        if not nao_pressionada(resposta):
            _parar(f'InputGame key 0x{vk:x} pressed', retorno + 5)

    sinal = lambda r: not (r & 0x8000)          # cwde; test eax, eax; jge  # noqa: E731
    tecla(sinal)
    for a, alvo in ((0x5099ae, 0x42934d), (0x5099ae, 0x42935e), (0x4e05a8, 0x42937b), (0x5099b1, 0x4293a1)):
        if m.u8(a):
            _parar(f'InputGame byte 0x{a:x} set', alvo)
    m.u8(0x4e19b0, 0)
    m.u16(0x5099ac, zona_mouse(m))
    if m.u8(0x49a05a):
        _parar('InputGame byte 0x49a05a set', 0x4293dc)
    tecla(sinal)
    if m.u16(0x4e05ae) == 0xc:
        _parar('InputGame help page 0xc', 0x429573)
    for alvo in (0x429585, 0x4295aa):
        if m.u8(0x5099b1):
            _parar('InputGame byte 0x5099b1 set', alvo)
    tecla(sinal)
    if m.u16(0x4e05ae) in (8, 9):
        _parar('InputGame help page 8/9', 0x42966c)
    tecla(sinal)
    if m.u16(0x4e05ae) == 7:
        _parar('InputGame help page 7', 0x42969b)
    tecla(sinal)
    if m.u16(0x4e05ae) == 2:
        _parar('InputGame help page 2', 0x4296ca)
    for _ in range(5):                          # 0x20, 0x26, 0x28, 0x27, 0x25
        tecla(sinal)
    tecla(lambda r: r & 0xffff == 0)            # 0x0d: test ax, ax; jne
    tecla(lambda r: r & 0xffff == 0)            # 0x58: test ax, ax; je
    if m.u16(0x4e05ae) == 0xd:
        _parar('InputGame help page 0xd', 0x4297a2)
    zona = m.u16(0x5099ac)
    if zona >= 0xa:
        _parar('InputGame zone >= 10', 0x4297cd)
    if zona == 0:
        pairar_mapa(m, jogador & 0xff, provedores or {})
    elif zona > 8:
        _parar('InputGame zone 9', 0x42c29f)
    else:
        if m.u8(0x5099ae):
            _parar('InputGame scroll with button', 0x42ba8c)
        m.u32(0x49a014, 0)
        m.u16(0x49a010, zona + 0x1dd7)
        rolar_terreno(m, 0x508720, 0x508722, zona, 1)
    if m.u32(0x4e060c) != 0:
        _parar('InputGame help-info change', 0x42c2bd)
    ajuda = m.u16(0x4e0610)
    if ajuda < m.u16(0x49620a):
        m.u16(0x4e0610, ajuda + 1)
    m.u32(0x4e060c, 0)
    m.u16(0x49620c, 0xffff)
    if m.u8(0x496d2c):
        proximas_gotas(m)


def tropas_selecionadas(m, jogador):
    """DesTroupesSelectionnes 0x47253d: AL = u16 0x508728[player << 9] != 0."""
    return int(m.u16(0x508728 + ((jogador & 0xff) << 9)) != 0)


def selecao_estrutura(m, jogador):
    """BatimentGetSelection 0x41a4b6: AX = u16 0x495be0[player]."""
    return m.u16(0x495be0 + 2 * (jogador & 0xff))


def _objeto(m, celula):
    return m.u8(m.u32(0x507d74) + (celula & 0xffff))


def terreno_sac(m, celula):
    """TerrainEstSac 0x4766b1: objects below 0x42 return 0 (the bag range is unreached)."""
    if _objeto(m, celula) >= 0x42:
        _parar('TerrainEstSac object >= 0x42', 0x4766c9)
    return 0


def terreno_gc(m, celula):
    """TerrainEstGc 0x4762b9: objects below 0x1d return 0."""
    if _objeto(m, celula) >= 0x1d:
        _parar('TerrainEstGc object >= 0x1d', 0x4762d1)
    return 0


def terreno_mina(m, celula):
    """TerrainEstMine 0x476263: tiles outside 0x251..0x252 and 0x255..0x256 return 0."""
    tile = m.u16(m.u32(0x507d70) + 2 * (celula & 0xffff))
    if 0x251 <= tile <= 0x252 or 0x255 <= tile <= 0x256:
        _parar('TerrainEstMine mine tile', 0x4762af)
    return 0


def terreno_armadilha(m, celula, jogador):
    """TerrainEstPiege 0x4762de: object 0x46 (trap) is unreached; otherwise 0."""
    if _objeto(m, celula) == 0x46:
        _parar('TerrainEstPiege trap object', 0x4762fa)
    return 0


def procurar_unidade(m, celula, provedores):
    """ChercheIndiceEngin 0x446693 (AX cell, EDX 0): first live unit with +0x72 occupying the cell.

    EnginOccupeCase 0x44246e is Combat's ``alvos_alcance.ocupa_celula`` (BL = 1 + (+0xab != 0)).
    """
    for i in range(800):
        r = m.u32(0x4e19a0) + 276 * i
        if m.u8(r + 2) in (0, 4) or not m.u8(r + 0x72):
            continue
        filtro = 1 + (m.u8(r + 0xab) != 0)
        if _chamar(provedores, 'EnginOccupeCase', 0x446713, unidade=i, celula=celula & 0xffff, filtro=filtro) & 0xff:
            _parar('ChercheIndiceEngin unit found', 0x44671c)
    return 0xffff


def pairar_mapa(m, jogador, provedores):
    """InputGame 0x429800..0x42b854: cursor-over-map hover (no click, nothing selected)."""
    y, x = m.u16(0x5099aa), m.u16(0x5099a8)
    celula = (((y >> 5) + m.u16(0x508722)) << 8) + (x >> 5) + m.u16(0x508720)
    margem = m.s8(0x508f90) * 32
    if x >= m.u16(0x508724) * 32 - margem or y >= m.u16(0x508726) * 32 - margem or x < margem or y < margem:
        return
    c = celula & 0xffff
    if not _chamar(provedores, 'CaseEstDecouverte', 0x4298d9, caso=c, jogador=m.u8(0x508041)) & 0xff:
        _parar('InputGame hover on an undiscovered cell', 0x4298e2)
    terreno_sac(m, c)
    terreno_gc(m, c)
    terreno_mina(m, c)
    terreno_armadilha(m, c, jogador)
    if _chamar(provedores, 'CaseEstIlluminee', 0x429a6e, caso=c, jogador=jogador) & 0xff:
        if m.u8(m.u32(0x4e0f38) + 2 * c + 1) & 0x80:
            _parar('InputGame hover over a structure cell', 0x429a8c)
        m.u16(0x496ac4, 0xffff)
        unidade = procurar_unidade(m, c, provedores)
        m.u16(0x496ac2, unidade)
        if unidade != 0xffff:
            _parar('InputGame hover over a unit', 0x429af9)
    pagina = m.u16(0x4e05ae)
    if pagina in (9, 0xc, 0xb, 3, 0xd, 5, 0xa, 1, 2, 7):
        _parar(f'InputGame hover with help page {pagina}', 0x429b8c)
    if not tropas_selecionadas(m, jogador):
        if selecao_estrutura(m, jogador) == 0xffff and not m.u8(0x4e19b0) and m.u8(0x5099ae):
            _parar('InputGame hover with a held button', 0x42a6fd)
    if m.u8(0x4e19b0):
        _parar('InputGame hover with byte 0x4e19b0 set', 0x42b85d)
    if tropas_selecionadas(m, jogador):
        _parar('InputGame hover with selected troops', 0x42a762)
    if m.u16(0x496ac2) != 0xffff:
        _parar('InputGame hover unit info', 0x42a793)
    if m.u16(0x496ac4) != 0xffff:
        _parar('InputGame hover structure info', 0x42ac1b)
    if tropas_selecionadas(m, jogador):
        _parar('InputGame hover with selected troops', 0x42b31f)


def enviar_entrada(m, jogador):
    """InputSend 0x45ec9f: only when ReseauActif (byte 0x4e0730) is set."""
    if m.u8(0x4e0730):
        _parar('InputSend network path', 0x45ecac)


def calcular_icone_acao(m):
    """CalculIconeAction 0x45e944; returns EAX (the final table index)."""
    local = m.u8(0x508041)
    if m.u16(0x508728 + (local << 9)) == 1:
        _parar('CalculIconeAction one unit selected', 0x45e962)
    if m.u16(0x495be0 + 2 * local) != 0xffff:
        _parar('CalculIconeAction structure selected', 0x45e9bf)
    for i in range(10):
        r = 0x4e2410 + 6 * i
        if m.u16(r) != 0x29b1 or m.u16(r + 2) != 1 or m.u16(r + 4) != 0:
            _parar('CalculIconeAction icon slot differs', 0x45ea64)
        m.u16(r, 0x29b1)
        m.u16(r + 2, 1)
        m.u16(r + 4, 0)
    m.u8(0x496d48, 0xff)
    return 10


def _cadeia(m, endereco):
    saida = bytearray()
    while True:
        b = m.u8(endereco + len(saida))
        if b == 0:
            return bytes(saida)
        saida.append(b)


def _exibir(provedores, rotina, sitio, registros, palavras=(None, None, None, None), limpeza=0):
    """Call a display routine or boundary: ``provider(sitio, registros, palavras, limpeza) -> EAX``.

    The v1 composition records a declared boundary; the display composition crosses the
    executed display routine. ``registros`` are EAX/EDX/EBX/ECX at the CALL; ``palavras``
    the four stack words after the return slot (None where they are uninitialized locals).
    """
    return _chamar(provedores, rotina, sitio, registros=registros, palavras=palavras, limpeza=limpeza)


def iniciar_menu(m, jogador, estado, ecx, registro, janelas, provedores, ebx, esp):
    """MenuInit 0x4682bb (AL player, DL new state, ECX), load-tail path to state 0x12.

    ``ebx`` and ``esp`` are the caller's EBX and its ESP before the CALL: they shape the
    recorded registers (BH = state, BL = track index) and the stack path buffer
    ``esp - 4 - 0x14 - 0x138`` handed to LoadPie. Display routines and boundaries are
    providers (``_exibir``); InitGameZone is Core's and may return its register dict.
    """
    jogador, estado = jogador & 0xff, estado & 0xff
    if jogador != m.u8(0x508041):
        return
    atual = m.u8(0x4e2f78)
    if atual == estado:
        return
    if atual in (6, 7):
        _parar('MenuInit from state 6/7', 0x4682f5)
    if atual in (0xa, 1, 0x13, 0x18):
        _parar(f'MenuInit from state 0x{atual:x}', 0x468368)
    if atual == 0x12:
        _parar('MenuInit from state 0x12', 0x46835f)
    cursor = janelas.mostrar_cursor(0) & 0xffffffff
    registro.vinculo('USER32.ShowCursor', (0,), 0x46837a, cursor)
    ebx = (ebx & ~0xff00) | (atual << 8)
    superficie = _exibir(provedores, 'DDLockSurface', 0x46837a, dict(EAX=cursor, EDX=estado, EBX=ebx, ECX=ecx))
    m.u32(0x508f70, superficie)
    if estado == m.u8(0x4e2f78):
        _parar('MenuInit same state after lock', 0x468c60)
    if estado != 0x12:
        _parar(f'MenuInit to state 0x{estado:x}', 0x4684c2)
    banco = m.u32(0x508f64)
    if banco:
        _exibir(provedores, 'DeleteBank', 0x4683ae, dict(EAX=banco, EDX=estado, EBX=banco, ECX=0))
        m.u32(0x508f64, 0)
    if m.u32(0x508f68):
        _parar('MenuInit u32 0x508f68 set', 0x4683c3)
    if m.u8(0x49a054):
        _parar('MenuInit byte 0x49a054 set', 0x4683db)
    largura, altura = (m.u16(0x49a018) - 1) & 0xffff, (m.u16(0x49a01a) - 1) & 0xffff
    _exibir(provedores, 'FilledBox', 0x468400,
            dict(EAX=0, EDX=0, EBX=_sx16(largura) & 0xffffffff, ECX=_sx16(altura) & 0xffffffff),
            palavras=(2, 0, None, None), limpeza=8)
    if m.u8(0x4e2f79):
        _parar('MenuInit byte 0x4e2f79 set', 0x46840e)
    caminho = _cadeia(m, CAMINHO_PIE)
    texto = caminho + _cadeia(m, NOME_PIE) + b'\0'
    palavras = tuple(int.from_bytes(texto[4 * k:4 * k + 4].ljust(4, b'\0'), 'little') if 4 * k < len(texto)
                     else None for k in range(4))
    ecx_scan = (-2 - len(caminho)) & 0xffffffff
    _exibir(provedores, 'LoadPie', 0x468476,
            dict(EAX=(esp - 4 - 0x14 - 0x138) & 0xffffffff, EDX=m.u32(0x508f70), EBX=0, ECX=ecx_scan), palavras)
    zona = _chamar(provedores, 'InitGameZone', 0x468484, eax=1, edx=0, ecx=0)
    ebx = zona['EBX'] if isinstance(zona, dict) and 'EBX' in zona else 0
    indice = m.u8(0x4e1d18)
    faixa = 2 + m.u8(0x4e1c18 + indice) % 2
    m.u8(0x4e1d18, indice + 1)
    ebx = (ebx & ~0xff) | ((indice + 1) & 0xff)
    _exibir(provedores, 'MCICD_Play', 0x4684b8, dict(EAX=faixa, EDX=0, EBX=ebx, ECX=2), palavras)
    m.u8(0x4e2f78, estado)
    if m.u8(0x508f90):
        _parar('MenuInit byte 0x508f90 set', 0x468c76)
    _exibir(provedores, 'DDUnlockSurface', 0x468c91, dict(EAX=m.u32(0x508f70), EDX=0, EBX=ebx, ECX=2), palavras)
    ebx = (ebx & ~0xff00) | (estado << 8)
    _exibir(provedores, 'DDFlipPage', 0x468ca2, dict(EAX=1, EDX=0, EBX=ebx, ECX=2), palavras)
    if estado < 5:
        _parar('MenuInit tail state < 5', 0x4692c6)
    if estado == 5:
        _parar('MenuInit tail state 5', 0x468f5f)
    if estado < 0xe:
        _parar('MenuInit tail state < 0xe', 0x469289)
    if estado == 0xe:
        _parar('MenuInit tail state 0xe', 0x4691d7)
    if estado == 0x10:
        _parar('MenuInit tail state 0x10', 0x468ff7)
    m.u32(0x4e2f70, 0)
    m.u16(0x4e2f40, 0)
    if estado == 0x12:
        m.u8(0x508f90, m.u8(0x4e2f7a))


def _chamar(provedores, rotina, sitio, **argumentos):
    provedor = provedores.get(rotina)
    if provedor is None:
        raise DependenciaIA(rotina, sitio)
    return provedor(sitio=sitio, **argumentos)
