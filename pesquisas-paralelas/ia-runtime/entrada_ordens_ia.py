"""M3.1 input path over live original memory: InputGame -> SetPlayerOrdre -> ProcessInputGame and their leaves.

Translated from the intact bytes after the original-only capture ``evidencias/captura-entrada-ordens-ia.json``
(commit before this module; ``capturar_entrada_ordens_ia.py``) and following the executed blocks recorded
there and in the Mac mini probes P1/P2/P3:

- ``Entrada.input_game``: InputGame 0x429278 (AL = player). Translated: the key block (arrows, space; every
  answer through ``tecla``), the WndProc-flag/zone selection with MouseZone 0x479cac, the right-button
  deselection 0x4295a1, the playfield (zone 0) cell mapping 0x429800..0x42984a and its margins, the
  undiscovered-cell rule 0x4298d9 (troops selected, help page 0: tag 5), the cell information block 0x4299ad
  (sack, field, mine, trap, structure and unit under the cursor), help page 3 (construction placement through
  BatimentPosable, tag 4), page 1 (tag 5), the general page: drag start 0x42a6fd, own-unit hover, attack hover
  of an enemy unit (tag 14), the terrain presses (field: tag 7 or 0x12; mine: tag 6 or 0x12; move: tag 5) and
  the drag box 0x42b854 (selection, tag 1; structure selection, tag 2); the edge zones 1..8 (ScrollTerrain
  0x472068); the minimap zone 10 (MiniMapSetLock/MiniMapSetPos, recentring through MiniMapGetCenterSelect
  with nothing selected, tag 5 through MiniMapGetCase with troops); the HUD zone 11 (IconeGetZone 0x45da4e,
  the order Bag of a single selected unit, BagGetCode, codes 2, 3 and 7: help page 0xb/3/0xa and the CAVE
  mode byte 0x496207 after TestRessource); the dummy zones 0x1c..0x1f (tag 0x26); and the help-text tail.
- ``Entrada.set_player_ordre``: SetPlayerOrdre 0x45ecd4 (AL player, DX tag, BX, CX, two pushed words; RET 8).
- ``Entrada.process_input_game``: ProcessInputGame 0x45edc0, all 40 jump-table targets 0x45ed20, each handing
  its packet words to the owning front's setter with the original registers, then the slot cleanup 0x45f2de.
- Leaves: MouseEstDeplacer 0x4291bc, KeyPressed 0x42c339, KeyUnPressed 0x42c361, KeyTestRelease 0x42c396,
  IconeGetZone, BagGetCode 0x4472d3, BagGetType 0x4472de, EnginGetBagOrdre 0x4474f3, GrabAllInput 0x474fe6,
  InitInputPlayer 0x45f32b, MiniMapGetCase 0x46a224, MiniMapGetCenterSelect 0x46a273, MiniMapSetLock 0x46a1d7,
  the mouse messages 0x200..0x205 of WndProc 0x4181a1, and CalculIconeAction 0x45e944 with IconeFillContenu
  0x45dbd0 for a single selected unit (codes 0..3 of its Bag).

Every branch outside that domain raises ``DependenciaIA(description, original address)`` before its first
effect, after the stores the original made before it. ``m`` serves ``u8/u16/u32(address[, value])`` at
original addresses. Callees owned by other fronts are named providers (``Provedores``; never defaulted):
each receives the original entry registers EAX..EBP (and ESP and pushed words where the owner's API takes
them) and returns the registers the original leaves; only the registers InputGame/ProcessInputGame read
afterwards are consumed. Registers: every routine returns the general registers it leaves (callee-saved ones
restored) except InputGame, whose EAX (the rain routine's or a flag byte) CalculGame discards; InputGame
returns ``None``.
"""
from reinicio_ia import DependenciaIA

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PACOTES = 0x4e2458               # u32 pointer per player to its 10-byte input packet
TABELA_COMANDOS = 0x45ed20
LIMPAR = 0x45f2de
SELECOES = 0x508728
SEL_ESTRUTURA = 0x495be0
POOL = 0x4e19a0
PASSO = 276
CURSOR_X, CURSOR_Y, ZONA = 0x5099a8, 0x5099aa, 0x5099ac
AE, AF, B0, B1, B2 = 0x5099ae, 0x5099af, 0x5099b0, 0x5099b1, 0x5099b2
PAGINA, MODO_ACAO, MODO_SORT, MODO_9 = 0x4e05ae, 0x496207, 0x496208, 0x496209
ARRASTO = 0x4e19b0
UNIDADE_SOB, ESTRUTURA_SOB = 0x496ac2, 0x496ac4
CURSOR_ID, CURSOR_ANIM = 0x49a010, 0x49a014
VISTA = 0x508720                 # u16 x, y, width, height
LARGURA_MAPA, ALTURA_MAPA = 0x497168, 0x49716a
ICONES = 0x4e2410                # 10 slots of (u16 id, u16 active, u16 extra)


def _parar(descricao, endereco):
    raise DependenciaIA(descricao, endereco)


def _s16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


def _idiv(a, b):
    """x86 IDIV: quotient truncated toward zero, remainder with the dividend's sign."""
    a, b = _s32(a), _s32(b)
    q = abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1)
    return q, a - q * b


def _div32(v):
    """``cdq``-free ``sar 0x1f / shl 5 / sbb / sar 5``: signed division by 32 truncated toward zero."""
    return _idiv(v, 32)[0]


def _baixo(v, b):
    return (v & 0xffffff00) | (b & 0xff)


class Provedores:
    """Named providers of other fronts' routines (``f(**args) -> value`` as documented per name).

    ``registros`` names take ``regs`` (EAX..EBP, ESP and, for TestRessource, ``pilha``) and return the exit
    registers; ``consultas`` names take keyword arguments and return the value consumed. A missing name
    raises ``DependenciaIA`` at the original call site, after the stores made before it."""

    def __init__(self, funcoes):
        self.funcoes = dict(funcoes)

    def __call__(self, nome, sitio, **argumentos):
        f = self.funcoes.get(nome)
        if f is None:
            raise DependenciaIA(nome, sitio)
        return f(**argumentos)


class Entrada:
    """The input-path routines over one live memory ``m`` with providers ``p`` (``Provedores``)."""

    def __init__(self, m, p):
        self.m, self.p = m, p

    # ------------------------------------------------------------ unit/structure records and small queries
    def _rec(self, u):
        return (self.m.u32(POOL) + (u & 0xffff) * PASSO) & M32

    def _tipo(self, u):                                  # EnginGetType 0x442025
        return self.m.u8(self._rec(u) + 1)

    def _dono(self, u):                                  # EnginGetPlayer 0x442045
        return self.m.u8(self._rec(u))

    def _vivo(self, u):                                  # EnginEstVivant 0x443dad
        return self.m.u8(self._rec(u) + 2) not in (0, 4)

    def _miroir(self, u):                                # EnginEstMiroir 0x44fffe (GetBit 2 of +0xdc)
        return (self.m.u8(self._rec(u) + 0xdc) >> 2) & 1

    def _est_selectionne(self, jogador, u):              # EnginEstSelectionne 0x472174
        r = self._rec(u)
        return self.m.u8(r + 0xbd) != 0 and self.m.u8(r) == jogador & 0xff

    def _tipo_estrutura(self, s):                        # BatimentGetType 0x41a4f4
        return self.m.u8(0x49a0c8 + (s & 0xffff) * PASSO + 8)

    def _dono_estrutura(self, s):                        # BatimentGetPlayer 0x41a08c
        return self.m.u8(0x49a0c8 + (s & 0xffff) * PASSO + 4)

    def _sel_estrutura(self, jogador):                   # BatimentGetSelection 0x41a4b6
        return self.m.u16(SEL_ESTRUTURA + 2 * (jogador & 0xff))

    def _nb(self, jogador):                              # EnginGetNbSelection 0x4721ce
        return self.m.u16(SELECOES + ((jogador & 0xff) << 9))

    def _tropas(self, jogador):                          # DesTroupesSelectionnes 0x47253d
        return self._nb(jogador) != 0

    def _primeira(self, jogador):                        # EnginGetSelection 0x4721a8
        base = SELECOES + ((jogador & 0xff) << 9)
        return self.m.u16(base + 2) if self.m.u16(base) else 0xffff

    def _selecao(self, jogador):
        base = SELECOES + ((jogador & 0xff) << 9)
        return [self.m.u16(base + 2 + 2 * i) for i in range(self.m.u16(base))]

    def _tipo_selecionado(self, jogador, tipo):         # EnginTypeSelectionne 0x47242e
        achou = 0
        for u in self._selecao(jogador):
            if not self._vivo(u):
                continue
            if self._tipo(u) != tipo & 0xff:
                return 0
            achou = 1
        return achou

    def _objeto(self, celula):
        return self.m.u8(self.m.u32(0x507d74) + (celula & 0xffff))

    def _mosaico(self, celula):
        return self.m.u16(self.m.u32(0x507d70) + 2 * (celula & 0xffff))

    def _descoberta(self, celula, jogador):             # CaseEstDecouverte 0x4766d6
        return not self.m.u8(self.m.u32(0x507d78 + 4 * (jogador & 0xff)) + (celula & 0xffff)) & 0x10

    def _iluminada(self, celula, jogador):              # CaseEstIlluminee 0x47693a
        return not self.m.u8(self.m.u32(0x507d88 + 4 * (jogador & 0xff)) + (celula & 0xffff)) & 0x10

    def _sac(self, celula):                              # TerrainEstSac 0x4766b1
        return 0x42 <= self._objeto(celula) <= 0x44

    def _tipo_sac(self, celula):                         # TerrainGetSacType 0x476038 (0xff: none)
        o = self._objeto(celula)
        return o - 0x42 if 0x42 <= o <= 0x44 else 0xff

    def _gc(self, celula):                               # TerrainEstGc 0x4762b9
        return 0x1d <= self._objeto(celula) < 0x35

    def _mina(self, celula):                             # TerrainEstMine 0x476263
        t = self._mosaico(celula)
        return 0x251 <= t <= 0x252 or 0x255 <= t <= 0x256

    def _armadilha(self, celula, jogador):              # TerrainEstPiege 0x4762de
        if self._objeto(celula) != 0x46:
            return False
        return self.m.u8(self.m.u32(0x507dac) + (celula & 0xffff)) == jogador & 0xff

    def _colisao(self, celula, mascara):                 # TerrainEnCollision 0x4761d4
        return (self.m.u8(self.m.u32(0x507da8) + (celula & 0xffff)) & mascara & 0xff) != 0

    def _obstaculo(self, celula):                        # TerrainEstObstacleNaturel 0x4752b8
        t = self._mosaico(celula)
        if t < 0x2be and self.m.u8(self.m.u32(0x507db0) + t):
            return True
        return 1 <= self._objeto(celula) <= 0xb

    def _selecao_terrestre(self, jogador):              # TypeEnginSelectEstTerrestre 0x47295e
        for u in self._selecao(jogador):
            if self._vivo(u) and 0x10 <= self._tipo(u) <= 0x11:   # TypeEnginEstTerrestre 0x4422fc
                return False
        return True

    def _texto(self, n):                                 # TextGetMessage 0x478a3b
        """u32 [[0x5099a4] + 4n]. In the MONDE01 display bench the text table pointer is 0 (no text file is
        loaded), so the original would read unmapped low memory: a named gap, never a guessed 0."""
        tabela = self.m.u32(0x5099a4)
        if tabela == 0:
            _parar('TextGetMessage with the text table pointer 0x5099a4 = 0 (texts not loaded)', 0x478a47)
        return self.m.u32(tabela + 4 * (n & 0xffff))

    @staticmethod
    def _nome_unidade(tipo):                             # EnginGetTypeName 0x441775
        return 0x4965ae + 50 * (tipo & 0xff) + 0xc

    @staticmethod
    def _nome_estrutura(tipo):                           # BatimentGetTypeName 0x418af7
        return 0x495d8c + 52 * (tipo & 0xff) + 0x13

    def _custo_estrutura(self, tipo):                    # BatimentGetRessource 0x41aace: food, stone, parts
        b = 0x495d98 + 52 * (tipo & 0xff)
        return self.m.u16(b), self.m.u16(b + 2), self.m.u16(b + 4)

    def _pode_atacar(self, jogador, modo, alvo):         # EnginSelectPeutAttaquer 0x472355
        if modo == 1:
            if self._tipo(alvo) == 0x11:
                return 0
        elif modo == 5:
            return 1
        for u in self._selecao(jogador):
            if not self._vivo(u):
                continue
            if not self._armee(self._tipo(u)):
                return 0
            _parar('EnginSelectPeutAttaquer with an army type selected (TypeEnginPeutAttaquer)', 0x4723e2)
        return 1

    @staticmethod
    def _armee(t):                                       # TypeEnginEstArmee 0x44230c
        return t <= 3 or t == 8 or 0xb <= t <= 0xc or t == 0xf or 0x10 <= t <= 0x11 or 0x14 <= t <= 0x19

    def _pode_entrar(self, jogador, modo, alvo):         # EnginSelectPeutEntrer 0x472b6c
        for u in self._selecao(jogador):
            if self._vivo(u) and self._miroir(u):
                return 0
        if modo == 1:
            t = self._tipo(alvo)
            if t == 0x10 or not 0xb <= t <= 0x11:         # TypeEnginEstEngin 0x442434: types 11..17
                return 0
            _parar('EnginSelectPeutEntrer over a vehicle', 0x472fbc)
        if modo == 3:
            _parar('EnginSelectPeutEntrer over a structure', 0x472bca)
        return 0

    def _chercher_unite(self, celula):                   # ChercheIndiceEngin 0x446693 (EDX = 0)
        achada = 0xffff
        for i in range(800):
            r = self._rec(i)
            if self.m.u8(r + 2) in (0, 4) or not self.m.u8(r + 0x72):
                continue
            filtro = 1 + (self.m.u8(r + 0xab) != 0)
            if not self.p('EnginOccupeCase', 0x446713, unidade=i, celula=celula & 0xffff, filtro=filtro) & 0xff:
                continue
            if self.m.u8(r + 1) == 0x10 and self.m.u8(r + 0xab) != 0x32:
                continue
            achada = i                                  # the last occupant with +0xab = 0, unless one with
            if self.m.u8(r + 0xab):                     # +0xab != 0 returns at once
                return i
        return achada

    # ------------------------------------------------------------ keys, mouse, Windows messages
    def _tecla(self, vk, sitio):
        """GetAsyncKeyState(vk) through the declared answers; returns the signed 16-bit result (cwde)."""
        return _s16(self.p('GetAsyncKeyState', sitio, vk=vk, local=sitio))

    def key_pressed(self, regs):
        """KeyPressed 0x42c339 (AL vkey): AL = 1 and byte 0x4e0630[vk] = 1 when held."""
        vk = regs['EAX'] & 0xff
        r = self._tecla(vk, 0x42c348)
        eax = r & M32
        if r < 0:
            self.m.u8(0x4e0630 + vk, 1)
            return dict(regs, EAX=(eax & 0xffff0000) | 0x0101)
        return dict(regs, EAX=eax & 0xffffff00)

    def key_unpressed(self, regs):
        """KeyUnPressed 0x42c361 (AL vkey): AL = 1 (and the latch cleared) when latched and now released."""
        vk = regs['EAX'] & 0xff
        if self.m.u8(0x4e0630 + vk) != 1:
            return dict(regs, EAX=0)
        r = self._tecla(vk, 0x42c37d)
        eax = r & M32
        if r < 0:
            return dict(regs, EAX=eax & 0xffffff00)
        self.m.u8(0x4e0630 + vk, 0)
        return dict(regs, EAX=(eax & 0xffff0000) | 1)

    def key_test_release(self, regs):
        """KeyTestRelease 0x42c396 (AL vkey): polls until released; EAX = the last answer (cwde)."""
        vk = regs['EAX'] & 0xff
        while True:
            r = self._tecla(vk, 0x42c3a7)
            if r >= 0:
                return dict(regs, EAX=r & M32)

    def mouse_est_deplacer(self, regs):
        """MouseEstDeplacer 0x4291bc: AL = 1 when the cursor is more than 10 px from u16 0x49a042 (x) or
        0x49a044 (y), else 0. EAX = (the smaller word of the deciding pair & 0xff00) | AL."""
        m = self.m
        for anterior, atual in ((0x49a042, CURSOR_X), (0x49a044, CURSOR_Y)):
            menor, maior = sorted((m.u16(anterior), m.u16(atual)))
            if maior - menor > 10:
                return dict(regs, EAX=(menor & 0xff00) | 1)
        return dict(regs, EAX=menor & 0xff00)

    def mouse_zone_regs(self, regs):
        """MouseZone as a leaf: EAX = (entry EDX & 0xffff0000) | zone (its loop counter), or 0."""
        z = self.mouse_zone()
        return dict(regs, EAX=((regs['EDX'] & 0xffff0000) | z) if z else 0)

    def mouse_zone(self, regs=None):
        """MouseZone 0x479cac: AX = first zone in [u16 0x50a9b4, u16 0x50a9b6] whose rectangle holds the cursor."""
        m = self.m
        x, y = m.u16(CURSOR_X), m.u16(CURSOR_Y)
        zona = m.u16(0x50a9b4)
        while zona <= m.u16(0x50a9b6):
            r = 0x5099b4 + 16 * zona
            if _s32(m.u32(r)) <= x and _s32(m.u32(r + 4)) <= y and x <= _s32(m.u32(r + 8)) and y <= _s32(m.u32(r + 12)):
                return zona
            zona = (zona + 1) & 0xffff
        return 0

    def grab_all_input(self, regs):
        """GrabAllInput 0x474fe6: GetCursorPos -> u16 0x5099a8/aa; EAX = the y dword."""
        x, y = self.p('GetCursorPos', 0x474fee)
        self.m.u16(CURSOR_X, x)
        self.m.u16(CURSOR_Y, y)
        return dict(regs, EAX=y & M32)

    def init_input_player(self, regs):
        """InitInputPlayer 0x45f32b: five 16-byte packets through MemAlloc; u32 0x4e2458+4p = pointer and
        u32 0x4e246c+4p = 0x10 for p = 0..4. EAX = the last pointer."""
        eax = regs['EAX']
        for k in range(5):
            self.m.u32(0x4e246c + 4 * k, 0x10)
            eax = self.mem_alloc(0x10)
            self.m.u32(PACOTES + 4 * k, eax)
        return dict(regs, EAX=eax)

    def mem_alloc(self, tamanho):
        """MemAlloc 0x467ea6 (EAX size): u32 0x4e2f3c += size; GlobalAlloc(0, size) and GlobalLock(handle)
        are the declared Windows bindings (provider ``GlobalAlloc``: flags, size -> pointer, the lock
        included). EAX = the locked pointer."""
        self.m.u32(0x4e2f3c, self.m.u32(0x4e2f3c) + tamanho)
        return self.p('GlobalAlloc', 0x467ec0, flags=0, tamanho=tamanho) & M32

    def wnd_proc(self, regs, pilha):
        """WndProc 0x4181a1, mouse messages 0x200..0x205 (hwnd, msg, wParam, lParam pushed; RET 0x10): the
        cursor words, the left/right flags and the double click (0x5099b0 in the playfield, else 0x5099ae).
        EAX = 0; ECX = lParam; EDX = wParam (0x203: the cursor y word)."""
        _, msg, wparam, lparam = (v & M32 for v in pilha)
        m = self.m
        if msg == 0x200:
            m.u16(CURSOR_X, lparam)
            m.u16(CURSOR_Y, lparam >> 16)
        elif msg == 0x201:
            m.u8(AE, 1)
        elif msg == 0x202:
            m.u8(AF, 1)
        elif msg == 0x203:
            wparam = m.u16(CURSOR_Y)                    # EDX = the cursor y read by the playfield test
            if wparam < m.u16(VISTA + 6) * 32:
                m.u8(B0, 1)
            else:
                m.u8(AE, 1)
        elif msg == 0x204:
            m.u8(B1, 1)
        elif msg == 0x205:
            m.u8(B2, 1)
        else:
            _parar(f'WndProc message 0x{msg:x}', 0x4181b5)
        return dict(regs, EAX=0, EBX=regs['EBX'], ECX=lparam, EDX=wparam)

    # ------------------------------------------------------------ minimap
    def mini_map_get_case(self, regs):
        """MiniMapGetCase 0x46a224 (AX x, DX y in minimap pixels): EAX = (y*H/mh) << 8 + x*W/mw."""
        m = self.m
        q1, _ = _idiv((regs['EAX'] & 0xffff) * m.u16(LARGURA_MAPA), m.u16(0x496fe0))
        q2, _ = _idiv((regs['EDX'] & 0xffff) * m.u16(ALTURA_MAPA), m.u16(0x496fe2))
        return dict(regs, EAX=((q2 << 8) + q1) & M32, EDX=_idiv((regs['EDX'] & 0xffff) * m.u16(ALTURA_MAPA),
                                                                 m.u16(0x496fe2))[1] & M32)

    def mini_map_get_center_select(self, regs):
        """MiniMapGetCenterSelect 0x46a273 (AX, DX minimap point; EBX/ECX addresses of the view words)."""
        m = self.m
        mw, mh = m.u16(0x496fe0), m.u16(0x496fe2)
        w, h = m.u16(LARGURA_MAPA), m.u16(ALTURA_MAPA)
        vw, vh = m.u16(VISTA + 4), m.u16(VISTA + 6)
        t = _idiv(vw * mw, w)[0]
        bx = _idiv(((regs['EAX'] & 0xffff) - _idiv(t, 2)[0]) * w, mw)[0]
        t = _idiv(vh * mh, h)[0]
        dy = _idiv(((regs['EDX'] & 0xffff) - _idiv(t, 2)[0]) * h, mh)[0]
        if _s16(bx) < 0:
            bx = 0
        if _s16(dy) < 0:
            dy = 0
        if _s16(bx) + vw > w:
            bx = w - vw
        eax = (vh + _s16(dy)) & M32
        if eax > h:
            dy, eax = h - vh, vh
        m.u16(regs['EBX'], bx)
        m.u16(regs['ECX'], dy)
        return dict(regs, EAX=eax, EBX=bx & M32, EDX=dy & M32)

    # ------------------------------------------------------------ action icons and Bags
    @staticmethod
    def icone_get_zone(m, x, y):
        """IconeGetZone 0x45da4e (AX x, DX y): icon 0..3 at x in [31+60i, 89+60i], scroll icons 8 (x 8..30)
        and 9 (x 272..294), y in [b, b+50] (b+52 for 8/9) with b = 420 at width 640 else 548; else 0xffff."""
        b = 0x1a4 if m.u16(0x49a018) == 0x280 else 0x224
        x &= 0xffff
        y &= 0xffff
        for i in range(4):
            a = 0x1f + 0x3c * i
            if x >= a and a + 0x3a >= x and y >= b and b + 0x32 >= y:
                return i
        if 8 <= x <= 0x1e and y >= b and y <= b + 0x34:
            return 8
        if 0x110 <= x <= 0x126 and y >= b and y <= b + 0x34:
            return 9
        return 0xffff

    def icone_get_zone_regs(self, regs):
        """IconeGetZone as a leaf: EAX = the zone; EDX = its icon-loop counter (the icon, else 4)."""
        z = self.icone_get_zone(self.m, regs['EAX'], regs['EDX'])
        return dict(regs, EAX=z, EDX=z if z < 4 else 4)

    def bag_regs(self, nome, regs):
        """BagGetCode/BagGetType/EnginGetBagOrdre as leaves (EDX &= 0xffff for the two Bag reads)."""
        if nome == 'EnginGetBagOrdre':
            return dict(regs, EAX=self.bag_ordre(regs['EAX']))
        i = regs['EDX'] & 0xffff
        if nome == 'BagGetCode':
            return dict(regs, EAX=_baixo(regs['EAX'], self._bag_code(regs['EAX'], i)), EDX=i)
        return dict(regs, EAX=(regs['EAX'] & 0xffff0000) | self._bag_type(regs['EAX'], i), EDX=i)

    def bag_ordre(self, u):
        """EnginGetBagOrdre 0x4474f3: [u32 [0x4e19b8] + 4*owner] + 104*type of the unit's record."""
        r = self._rec(u)
        return (self.m.u32(self.m.u32(0x4e19b8) + 4 * self.m.u8(r)) + 104 * self.m.u8(r + 1)) & M32

    def _bag_code(self, bag, i):                         # BagGetCode 0x4472d3
        return self.m.u8(bag + 0x42 + (i & 0xffff))

    def _bag_type(self, bag, i):                         # BagGetType 0x4472de
        return self.m.u16(bag + 6 + 2 * (i & 0xffff))

    def _icone(self, slot, ident, ativo, extra):
        """One IconeFillContenu/CalculIconeAction slot store; byte 0x4e05a2 = 1 when the triple changes."""
        a = ICONES + 6 * slot
        if (self.m.u16(a), self.m.u16(a + 2), self.m.u16(a + 4)) != (ident & 0xffff, ativo & 0xffff, extra & 0xffff):
            self.m.u8(0x4e05a2, 1)
        self.m.u16(a, ident)
        self.m.u16(a + 2, ativo)
        self.m.u16(a + 4, extra)

    def icone_fill_contenu(self, bag, modo, unidade):
        """IconeFillContenu 0x45dbd0 (EAX Bag, DL mode 1 = a unit's order Bag, BX unit): scroll icons 8/9 and
        slots 0..3 from the Bag's scroll position. Codes 0 (empty), 1/5 (skipped), 2 (0x29f0+type) and 3
        (structure 0x29b9+type, active when TestRessource accepts its food and stone; parts are not passed)."""
        m = self.m
        rolagem, total, capacidade = m.u16(bag + 4), m.u16(bag), m.u16(bag + 2)
        self._icone(8, 0x29b1 if rolagem == 0 else 0x29cf, 1, 0)
        self._icone(9, 0x29b1 if rolagem + 4 >= total else 0x29cf, 1, 0)
        slot, k = 0, rolagem
        while (k & 0xffff) < capacidade:
            tipo = m.u8(bag + 2 * (k & 0xffff) + 6)
            codigo = m.u8(bag + 0x42 + (k & 0xffff))
            if codigo == 0:
                self._icone(slot, 0x29b1, 1, 0)
            elif codigo == 2:
                self._icone(slot, (m.u16(bag + 2 * (k & 0xffff) + 6) + 0x29f0), 1, 0)
            elif codigo == 3:
                if modo == 3:
                    _parar('IconeFillContenu structure Bag of a selected structure', 0x45dec6)
                comida, pedra, _ = self._custo_estrutura(tipo)
                jogador = m.u8(0x508041)
                ok = self.p('TestRessource', 0x45df93, regs=dict(EAX=comida, EDX=pedra, EBX=0, ECX=0),
                            pilha=[jogador])['EAX'] & 0xff
                self._icone(slot, 0x29b9 + tipo, 1 if ok else 0, 0)
            elif codigo in (4, 6, 7):
                _parar(f'IconeFillContenu Bag code {codigo}', {4: 0x45e40c, 6: 0x45e430, 7: 0x45e696}[codigo])
            slot += 1                                   # 0x45ddf7: codes 1, 5 and > 7 use a slot unwritten
            if slot == 4:
                return
            k += 1
        for s in range(slot, 4):
            self._icone(s, 0x29b1, 1, 0)

    def calcul_icone_action(self, regs):
        """CalculIconeAction 0x45e944 (exit registers restored except EAX)."""
        m = self.m
        local = m.u8(0x508041)
        if self._nb(local) == 1:
            m.u8(0x496d48, 0)
            u = self._primeira(local)
            self.icone_fill_contenu(self.bag_ordre(u), 1, u)
            return dict(regs, EAX=None)             # IconeFillContenu's leftover EAX; CalculGame discards it
        if self._sel_estrutura(local) != 0xffff:
            _parar('CalculIconeAction structure selected', 0x45e9bf)
        for i in range(10):
            self._icone(i, 0x29b1, 1, 0)
        m.u8(0x496d48, 0xff)
        return dict(regs, EAX=10)

    # ------------------------------------------------------------ packet producer and dispatcher
    def set_player_ordre(self, regs, pilha):
        """SetPlayerOrdre 0x45ecd4 (AL player, DX tag, BX, CX, pushed words 6 and 8; RET 8)."""
        j = regs['EAX'] & 0xff
        p = self.m.u32(PACOTES + 4 * j)
        self.m.u16(p, regs['EDX'])
        self.m.u16(p + 2, regs['EBX'])
        self.m.u16(p + 4, regs['ECX'])
        self.m.u16(p + 6, pilha[0])
        self.m.u16(p + 8, pilha[1])
        return dict(regs, EAX=self.m.u32(PACOTES + 4 * j), EBX=pilha[0] & M32, EDX=pilha[1] & M32)

    def _ordre(self, jogador, etiqueta, bx, cx, w6=0, w8=0, sitio=0):
        self.set_player_ordre(dict(EAX=jogador, EDX=etiqueta, EBX=bx, ECX=cx), [w6, w8])
        if self.ordens is not None:
            self.ordens.append(dict(site=hex(sitio), player=jogador & 0xff, tag=etiqueta, word2=bx & 0xffff,
                                    word4=cx & 0xffff, word6=w6, word8=w8))

    ordens = None

    def process_input_game(self, regs):
        """ProcessInputGame 0x45edc0 (AL player): dispatches the packet's tag through table 0x45ed20 to the
        owning front's routine, then clears the five packet words. Exit: EBX/ECX/EDX/ESI restored; EAX = the
        packet pointer."""
        m, p = self.m, self.p
        j = regs['EAX'] & 0xff
        pac = m.u32(PACOTES + 4 * j)
        etiqueta = m.u16(pac)
        w = lambda o: m.u16(pac + o)                           # noqa: E731
        b = lambda o: m.u8(pac + o)                            # noqa: E731
        base = dict(regs, ESI=j, EBX=j << 2, EDX=etiqueta)     # registers at the jump (EAX = packet)

        def chamar(nome, sitio, **r):
            return p(nome, sitio, regs=dict(base, **r))

        alvo = LIMPAR if etiqueta > 0x27 else self.comandos[etiqueta]
        if etiqueta in (1, 2, 3):
            chamar('DeSelectionGroupe', {1: 0x45ee4b, 2: 0x45eeb4, 3: 0x45ee32}[etiqueta], EAX=j)
            chamar('BatimentDeselectionner', {1: 0x45ee55, 2: 0x45eebe, 3: 0x45ee3c}[etiqueta], EAX=j)
            if etiqueta == 1:
                chamar('SelectionEngin', 0x45ee83, EAX=j, EDX=w(2), EBX=w(4))
            elif etiqueta == 2:
                chamar('BatimentSelection', 0x45eed8, EAX=w(2))
        elif etiqueta == 4:
            chamar('SetConstruitBatimentSelect', 0x45ef9b, EAX=j, EDX=b(2), EBX=w(4))
        elif etiqueta == 5:
            chamar('SetDeplaceEnginSelect', 0x45efd8, EAX=j, EDX=w(2))
        elif etiqueta in (6, 7, 8, 19):
            nome, sitio = {6: ('SetMineEnginSelect', 0x45eff9), 7: ('SetRecolteEnginSelect', 0x45f058),
                           8: ('SetTransporteEnginSelect', 0x45f076),
                           19: ('SetDechargeCaveEnginSelect', 0x45f085)}[etiqueta]
            chamar(nome, sitio, EAX=j, EDX=w(2), **({'EBX': j << 2} if etiqueta == 19 else {}))
            chamar('SetDepotEnginSelect', 0x45f037, EAX=j, EDX=b(4), EBX=w(6), ECX=b(8))
        elif etiqueta == 14:
            if self._sel_estrutura(j) == 0xffff:
                chamar('SetAttaqueEnginSelect', 0x45f105, EAX=j, EDX=b(2), EBX=w(4))
            else:
                chamar('BatimentInitAttaqueSelect', 0x45f13f, EAX=j, EDX=b(2), EBX=w(4))
        elif etiqueta == 17:
            chamar('InitRecruteTroupe', 0x45f1a9, EAX=b(2), EDX=j)
        elif etiqueta == 18:
            chamar('SetRamasseEnginSelect', 0x45f217, EAX=j, EDX=w(2))
        elif etiqueta == 36:
            chamar('BatimentDeselectionner', 0x45ee8f, EAX=j)
            chamar('EnginAddSelection', 0x45eea5, EAX=w(2), EDX=j)
        elif alvo != LIMPAR:
            _parar(f'ProcessInputGame tag 0x{etiqueta:x}', alvo)
        for o in (0, 2, 4, 6, 8):
            m.u16(m.u32(PACOTES + 4 * j) + o, 0)
        return dict(regs, EAX=m.u32(PACOTES + 4 * j))

    comandos = None

    # ------------------------------------------------------------ InputGame
    def _rolar(self, zona, passos):
        """ScrollTerrain 0x472068 on the view (EAX = &x, EDX = &y, EBX = zone, ECX = steps)."""
        m = self.m
        direcao = (zona - 1) & 0xffff
        w, h = m.u16(LARGURA_MAPA), m.u16(ALTURA_MAPA)

        def x_menos():
            if m.u16(VISTA):
                m.u16(VISTA, m.u16(VISTA) - 1)

        def y_menos():
            if m.u16(VISTA + 2):
                m.u16(VISTA + 2, m.u16(VISTA + 2) - 1)

        def x_mais():
            if m.u16(VISTA + 4) + m.u16(VISTA) < w:
                m.u16(VISTA, m.u16(VISTA) + 1)

        def y_mais():
            if m.u16(VISTA + 6) + m.u16(VISTA + 2) < h:
                m.u16(VISTA + 2, m.u16(VISTA + 2) + 1)
        acoes = ((x_menos, y_menos), (y_menos,), (x_mais, y_menos), (x_mais,), (x_mais, y_mais), (y_mais,),
                 (x_menos, y_mais), (x_menos,))
        for _ in range(passos & 0xffff):
            if direcao > 7:
                continue
            for f in acoes[direcao]:
                f()

    def _core(self, nome, sitio, **regs):
        return self.p(nome, sitio, regs=dict(dict.fromkeys(REG7, 0), **regs))

    def input_game(self, jogador):
        """InputGame 0x429278 (AL = player). See the module docstring for the translated domain."""
        m = self.m
        p = jogador & 0xff
        self.local = dict(info=0, info2=0xffff, flag=1)
        m.u16(CURSOR_ID, 0x1dd8)
        m.u16(0x4e0612, 0)
        m.u16(0x4e0614, 0)
        m.u32(CURSOR_ANIM, 0)
        m.u16(0x4e0616, 0)
        m.u8(0x508f8f, 0)
        m.u8(0x4e17ac, 0)
        m.u16(0x4e0618, 0)
        for a in (0x496d4a, UNIDADE_SOB, ESTRUTURA_SOB):
            m.u16(a, 0xffff)
        if self._tecla(0x1b, 0x429300) < 0:
            _parar('InputGame Escape held', 0x429305)
        if m.u8(AE):
            m.u16(CURSOR_ID, m.u16(CURSOR_ID) + 8)
        if m.u8(AE) and m.u8(ARRASTO):
            m.u16(ZONA, 0)
        elif m.u8(0x4e05a8):
            if m.u8(B1):
                m.u16(ZONA, 0xa)
            else:
                m.u8(0x4e05a8, 0)
        elif m.u8(B1) and (m.u8(0x4e05a9) or m.u8(0x4e05aa)):
            m.u16(ZONA, 0x1a)
        else:
            m.u8(ARRASTO, 0)
            m.u16(ZONA, self.mouse_zone())
        if m.u8(0x49a05a):
            _parar('InputGame group-number key path', 0x4293e0)
        if self._tecla(0x10, 0x429556) < 0:
            m.u16(PAGINA, 0xc)
        elif m.u16(PAGINA) == 0xc:
            m.u16(PAGINA, 0)
        if m.u8(B1) and m.u16(0x4e062c):
            m.u16(0x4e062c, 0)
            m.u16(PAGINA, 0)
        if m.u8(B1) and m.u16(ZONA) != 0xb:
            self._core('DeSelectionGroupe', 0x4295c0, EAX=p, EDX=p)
            self._core('BatimentDeselectionner', 0x4295c9, EAX=p, EDX=p)
            m.u16(PAGINA, 0)
            m.u8(0x4e05ab, 0)
            m.u8(MODO_ACAO, 0xff)
            m.u8(ARRASTO, 0)
            m.u8(0x496d48, 1)
        if self._tecla(0x11, 0x4295fc) < 0:
            _parar('InputGame Ctrl held (deposit mode 8/9)', 0x429601)
        elif m.u16(PAGINA) in (8, 9):
            m.u16(PAGINA, 0)
        if self._tecla(0x2e, 0x42967e) < 0:
            m.u16(PAGINA, 7)
        elif m.u16(PAGINA) == 7:
            m.u16(PAGINA, 0)
        if self._tecla(0x12, 0x4296ad) < 0:
            m.u16(PAGINA, 2)
        elif m.u16(PAGINA) == 2:
            m.u16(PAGINA, 0)
        if self._tecla(0x20, 0x4296dc) < 0:
            m.u8(0x508f8f, 1)
        if self._tecla(0x26, 0x4296f1) < 0:
            self._rolar(2, 1)
        elif self._tecla(0x28, 0x42970b) < 0:
            self._rolar(6, 1)
        if self._tecla(0x27, 0x429732) < 0:
            self._rolar(4, 1)
        elif self._tecla(0x25, 0x42974c) < 0:
            self._rolar(8, 1)
        if self._tecla(0x0d, 0x429773) & 0xffff or self._tecla(0x58, 0x429781) & 0xffff:
            _parar('InputGame GoLastAttaque key', 0x429786)
        if m.u16(PAGINA) == 0xd:
            _parar('InputGame help page 0xd (VoixOffAsk)', 0x4297a6)
        zona = m.u16(ZONA)
        if zona == 0:
            self._mapa(p)
            self._caixa(p)
        elif zona <= 8:
            self._borda(zona)
        elif zona == 0xa:
            self._minimapa(p)
        elif zona == 0xb:
            self._painel(p)
        elif zona == 0x1a:
            _parar('InputGame market zone 0x1a', 0x42bbff)
        elif zona == 0x1b:
            if m.u8(AE) and m.u8(AF):
                _parar('InputGame message-box zone (MessageBoxRun)', 0x42bc98)
        elif 0x1c <= zona <= 0x1f:
            if m.u8(AE) and m.u8(AF):
                self._ordre(p, 0x26, p, zona - 0x1c, sitio=0x42bbd6)
        self._fim()

    def _fim(self):
        """0x42c2ae: help-text timer, info pointer/word, then the rain routine."""
        m, loc = self.m, self.local
        if m.u32(0x4e060c) != loc['info'] & M32:
            m.u16(0x4e0610, 1 if loc['flag'] else m.u16(0x49620a))
        elif m.u16(0x4e0610) < m.u16(0x49620a):
            m.u16(0x4e0610, m.u16(0x4e0610) + 1)
        m.u32(0x4e060c, loc['info'])
        m.u16(0x49620c, loc['info2'])
        if m.u8(0x496d2c):
            self.p('NextGouttes', 0x42c30d)

    def _borda(self, zona):
        m = self.m
        m.u16(CURSOR_ID, zona + 0x1dd7 + (8 if m.u8(AE) else 0))
        m.u32(CURSOR_ANIM, 0)
        self._rolar(zona, 2 if m.u8(AE) else 1)

    def _contador(self, mod=None, mascara=None, endereco=0x508f80):
        v = self.m.u32(endereco)
        return v & mascara if mascara is not None else v % mod

    def _minimapa(self, p):
        m = self.m
        if self._tropas(p):
            m.u16(CURSOR_ID, 0x1df5)
            m.u32(CURSOR_ANIM, self._contador(mascara=7))
        if m.u8(B1):
            m.u16(CURSOR_ID, 0x1e0b)
            if not m.u8(0x4e05a8):
                m.u8(0x4e05a8, 1)
                x, y = m.u16(CURSOR_X), m.u16(CURSOR_Y)       # MiniMapSetLock 0x46a1d7
                m.u16(0x507d6c, m.u16(0x507d68) - x)
                m.u16(0x507d6e, m.u16(0x507d6a) - y)
            else:
                self.p('MiniMapSetPos', 0x42bb5d, x=_s16(m.u16(CURSOR_X)), y=_s16(m.u16(CURSOR_Y)))
                self.p('InitGameZone', 0x42bb66, eax=1, edx=0)
        else:
            m.u8(0x4e05a8, 0)
        if not m.u8(AE):
            return
        dx = (m.u16(CURSOR_X) - m.u16(0x507d68)) & 0xffff
        dy = (m.u16(CURSOR_Y) - m.u16(0x507d6a)) & 0xffff
        if self._tropas(p):
            celula = self.mini_map_get_case(dict(EAX=dx, EDX=dy))['EAX'] & 0xffff
            self._ordre(p, 5, celula, 0, sitio=0x42bbd6)
        else:
            self.mini_map_get_center_select(dict(EAX=dx, EDX=dy, EBX=VISTA, ECX=VISTA + 2))

    def _painel(self, p):
        m, loc = self.m, self.local
        si = self.icone_get_zone(m, m.u16(CURSOR_X), m.u16(CURSOR_Y))
        if self._sel_estrutura(p) != 0xffff:
            _parar('InputGame HUD with a structure selected (BatimentGetBagOrdre)', 0x42bd0d)
        if self._nb(p) != 1:
            return
        bag = self.bag_ordre(self._primeira(p))
        ae, af = m.u8(AE), m.u8(AF)
        if si in (8, 9):
            m.u8(0x4e05a2, 1)
            if ae and af:
                _parar('InputGame icon scroll (IconeScroll)', 0x42bd7e)
        elif si < 4:
            indice = m.u16(bag + 4) + si
            codigo = self._bag_code(bag, indice)
            tipo = self._bag_type(bag, indice)
            if codigo == 2:
                loc['info'] = self._texto((tipo & 0xff) + 0x28)
                loc['info2'], loc['flag'] = 0xffff, 0
                for a in (0x4e0614, 0x4e0616, 0x4e0612, 0x4e0618):
                    m.u16(a, 0)
                if ae and af:
                    m.u8(MODO_9, tipo)
                    m.u16(PAGINA, 0xb)
            elif codigo == 3:
                t = tipo & 0xff
                loc['info2'] = 0xffff
                loc['info'] = self._nome_estrutura(t)
                comida, pedra, pecas = self._custo_estrutura(t)
                m.u16(0x4e0612, comida)
                m.u16(0x4e0614, pedra)
                m.u16(0x4e0616, pecas)
                loc['flag'] = 0
                m.u16(0x4e0618, 0)
                if ae and af:
                    ok = self.p('TestRessource', 0x42c1a9, regs=dict(EAX=comida, EDX=pedra, EBX=0, ECX=0),
                                pilha=[p])['EAX'] & 0xff
                    if ok:
                        if t == 0x14:
                            self._ordre(p, 0xf, 0, 0, sitio=0x42bf88)
                        else:
                            m.u16(PAGINA, 3)
                            m.u8(MODO_ACAO, t)
            elif codigo == 7:
                loc['info'] = self._texto(0x61)
                loc['info2'], loc['flag'] = 0xffff, 0
                if ae and af:
                    m.u8(MODO_ACAO, tipo)
                    m.u16(PAGINA, 0xa)
            elif codigo in (4, 6):
                _parar(f'InputGame icon Bag code {codigo}', {4: 0x42be78, 6: 0x42c063}[codigo])
        if si != 0xff and m.u8(AE):
            m.u16(0x496d4a, si)
            m.u8(0x4e05a2, 1)

    def _arrasto(self, x, y, celula):
        m = self.m
        m.u16(0x49a024, x)
        m.u16(0x49a026, y)
        m.u16(0x4e19b2, celula)
        m.u16(0x49a028, x + 1)
        m.u16(0x4e19b4, celula)
        m.u8(ARRASTO, 1)
        m.u16(0x49a02a, y + 1)

    def _mapa(self, p):
        """Zone 0 (cursor over the playfield) up to 0x42b854."""
        m, loc = self.m, self.local
        x, y = m.u16(CURSOR_X), m.u16(CURSOR_Y)
        si = (((_div32(y) + m.u16(VISTA + 2)) << 8) + _div32(x) + m.u16(VISTA)) & 0xffff
        margem = (m.u8(0x508f90) - (0x100 if m.u8(0x508f90) & 0x80 else 0)) * 32
        if x >= m.u16(VISTA + 4) * 32 - margem or y >= m.u16(VISTA + 6) * 32 - margem or x < margem or y < margem:
            return
        pagina = m.u16(PAGINA)
        if (not self._descoberta(si, m.u8(0x508041)) and pagina != 5 and m.u8(MODO_SORT) and pagina != 0xd):
            if not self._tropas(p):
                return
            if pagina == 0:
                m.u16(CURSOR_ID, 0x1df5)
                m.u32(CURSOR_ANIM, self._contador(mascara=7))
                if m.u8(AE) and m.u8(AF):
                    self._ordre(p, 5, si, 0, sitio=0x42aecf)
            else:
                m.u16(CURSOR_ID, 0x1e0e)
                m.u32(CURSOR_ANIM, 0)
            return
        if self._sac(si):
            loc['info'] = self._texto(((self._tipo_sac(si) & 0xff) + 0x28) & 0xffff)
            loc['info2'] = self.p('SacGetCapacite', 0x4299da, celula=si)
        elif self._gc(si):
            loc['info'] = self._texto(0x2c)
        elif self._mina(si):
            loc['info'] = self._texto(0x5b)
            loc['info2'] = self.p('MineGetCapacite', 0x429a22,
                                  indice=self.p('MineGetIndice', 0x429a18, celula=si) & 0xffff)
            loc['flag'] = 0
        elif self._armadilha(si, p):
            loc['info'] = self._texto(0x33)
            loc['info2'], loc['flag'] = 0xffff, 0
        tipo_sob = 5
        if self._iluminada(si, p):
            w = m.u16(m.u32(0x4e0f38) + 2 * si)
            s = (w & 0x7fe0) >> 5 if w & 0x8000 else 0xffff
            m.u16(ESTRUTURA_SOB, s)
            if s != 0xffff:
                tipo_sob = 3
                loc['info'] = self._nome_estrutura(self._tipo_estrutura(s))
                loc['info2'] = 0xffff
            u = self._chercher_unite(si)
            m.u16(UNIDADE_SOB, u)
            if u != 0xffff:
                tipo_sob = 1
                loc['info'] = self._nome_unidade(self._tipo(u))
                loc['info2'] = 0xffff
                if self._est_selectionne(m.u8(0x508041), u) and m.u8(B0):
                    self.p('PlaySnd_StopSound', 0x429b6a,
                           regs=dict(EAX=self._rec(u) + 0x104, EDX=2, EBX=u * PASSO, ECX=u))
                    self._core('EnginAsk', 0x429b79, EAX=u, EDX=2, EBX=0, ECX=u)
        self.tipo_sob = tipo_sob
        if pagina == 9:
            _parar('InputGame help page 9 (deposit target)', 0x429b90)
        if pagina in (0xc, 0xb, 0xd, 5, 0xa, 2, 7):
            _parar(f'InputGame help page 0x{pagina:x}', {0xc: 0x429daa, 0xb: 0x429e31, 0xd: 0x42a080,
                                                          5: 0x42a110, 0xa: 0x42a373, 2: 0x42a4a2,
                                                          7: 0x42a600}[pagina])
        if pagina == 3:
            return self._pagina_construcao(p, si)
        if pagina == 1:
            m.u16(CURSOR_ID, 0x1df5)
            m.u32(CURSOR_ANIM, self._contador(mascara=7))
            if m.u8(AE) and m.u8(AF):
                self._ordre(p, 5, si, 0, sitio=0x42a488)
                m.u16(PAGINA, 0)
            return
        self._pagina_geral(p, si, x, y)

    def _pagina_construcao(self, p, si):
        m = self.m
        s = self._primeira(p)
        m.u16(0x4e0628, s)
        if s == 0xffff or self._tipo(s) != 7:
            m.u8(ARRASTO, 0)
            m.u16(PAGINA, 0)
            m.u8(0x496d48, 1)
            m.u8(MODO_ACAO, 0xff)
            return
        if m.u8(MODO_ACAO) == 9:
            _parar('InputGame wall placement (EnginSelectMurComplet)', 0x429fb6)
        sel = self._primeira(p)
        ok = self.p('BatimentPosable', 0x42a002,
                    regs=dict(EAX=m.u8(MODO_ACAO), EDX=si, EBX=sel, ECX=si, ESI=si, EDI=p, EBP=0))['EAX'] & 0xff
        if not ok or not (m.u8(AE) and m.u8(AF)):
            return
        self._ordre(p, 4, m.u8(MODO_ACAO), si, sitio=0x42a03c)
        if m.u8(MODO_ACAO) == 9:
            return
        m.u8(ARRASTO, 0)
        m.u16(PAGINA, 0)
        m.u8(0x496d48, 1)
        m.u8(MODO_ACAO, 0xff)

    def _pagina_geral(self, p, si, x, y):
        """0x42a6c6: drag start, unit/structure/terrain under the cursor with page 0 or 8."""
        m = self.m
        if (not self._tropas(p) and self._sel_estrutura(p) == 0xffff and not m.u8(ARRASTO) and m.u8(AE)):
            self._arrasto(x, y, si)
            return
        if m.u8(ARRASTO):
            return
        if self._tropas(p) and self._tecla(0x45, 0x42a76b) < 0:
            self._ordre(p, 0x25, 0, 0, sitio=0x42a77f)
        u = m.u16(UNIDADE_SOB)
        if u != 0xffff:
            return self._sobre_unidade(p, u, x, y, si)
        if m.u16(ESTRUTURA_SOB) != 0xffff:
            return self._sobre_estrutura(p, m.u16(ESTRUTURA_SOB), x, y, si)
        self._terreno(p, si)

    def _sobre_estrutura(self, p, s, x, y, si):
        """0x42ac1f with no troops selected: the selected structure's double click (tag 0x21), else an own
        structure's cursor and drag start (0x42b1ab)."""
        m = self.m
        if self._tropas(p):
            _parar('InputGame structure under the cursor with troops selected', 0x42ac32)
        if self._sel_estrutura(p) == s and m.u8(B0):
            self._ordre(p, 0x21, s, 0, sitio=0x42aecf)
            return
        if self._sel_estrutura(p) != 0xffff:
            _parar('InputGame structure under the cursor with a structure selected (BatimentPeutAttaquer)', 0x42b289)
        if self._dono_estrutura(s) != p:
            return
        m.u16(CURSOR_ID, 0x1df0)
        m.u32(CURSOR_ANIM, self._contador(5))
        if m.u8(AE):
            self._arrasto(x, y, si)

    def _sobre_unidade(self, p, u, x, y, si):
        m = self.m
        if m.u16(PAGINA) == 8:
            return
        if self._dono(u) == p:
            m.u16(CURSOR_ID, 0x1df0)
            m.u32(CURSOR_ANIM, self._contador(5))
        if self._tropas(p) and self._pode_atacar(p, 1, u) and self._dono(u) != p and self._dono(u) != 0xc8:
            m.u16(CURSOR_ID, 0x1dfd)
            m.u32(CURSOR_ANIM, self._contador(6))
            if m.u8(AE) and m.u8(AF):
                self._ordre(p, 0xe, 1, u, sitio=0x42aecf)
            return
        if self._tropas(p) and self._pode_entrar(p, 1, u) and not self._miroir(u):
            _parar('InputGame enter-vehicle hover', 0x42a8ce)
        if self._sel_estrutura(p) != 0xffff:
            _parar('InputGame unit hover with a structure selected (BatimentPeutAttaquer)', 0x42a9d3)
        if m.u8(B0) and self._primeira(p) == u and not self._miroir(u):
            t = self._tipo(u)                           # 0x42aa87: tag 9 (cx, word 6) by the unit's type
            if t == 0xd:
                _parar('InputGame double click on a type-13 unit (BagContient)', 0x42ab1f)
            alvo = {7: (2, 2), 5: (2, 1), 6: (2, 0)}.get(t)
            if alvo is None and 0xb <= t <= 0x11:       # TypeEnginEstEngin 0x442434
                alvo = (1, 0)
            if alvo is not None:
                self._ordre(p, 9, u, alvo[0], alvo[1], 0, sitio=0x42ab7d)
        if self._dono(u) != p:
            return
        m.u16(CURSOR_ID, 0x1df0)
        m.u32(CURSOR_ANIM, self._contador(5))
        if m.u8(AE):
            self._arrasto(x, y, si)

    def _terreno(self, p, si):
        """0x42b311: no unit or structure under the cursor."""
        m = self.m
        if not self._tropas(p):
            return
        if self._gc(si) or self._tipo_sac(si) == 1:
            if self._travail(p, 1):
                if m.u16(PAGINA) == 8:
                    _parar('InputGame deposit page 8 over a field', 0x42b393)
                m.u16(CURSOR_ID, 0x1e10)
                m.u32(CURSOR_ANIM, self._contador(6))
                if m.u8(AE) and m.u8(AF):
                    self._ordre(p, 7 if self._gc(si) else 0x12, si, 0, sitio=0x42b486 if self._gc(si) else 0x42af96)
                    m.u16(0x496204, si)
                    m.u16(0x4e05ac, 0x1e03)
                return
        if self._mina(si) or self._tipo_sac(si) == 2:
            if self._travail(p, 2):
                if m.u16(PAGINA) == 8:
                    _parar('InputGame deposit page 8 over a mine', 0x42b525)
                m.u16(CURSOR_ID, 0x1e10)
                m.u32(CURSOR_ANIM, self._contador(6))
                if m.u8(AE) and m.u8(AF):
                    if self._sac(si):
                        self._ordre(p, 0x12, si, 0, sitio=0x42b61c)
                    else:
                        self._ordre(m.u8(0x508041), 6, si, 0, sitio=0x42ad8e)
                    m.u16(0x496204, si)
                    m.u16(0x4e05ac, 0x1e03)
                return
        if self._tipo_sac(si) == 0 and self._travail(p, 0):
            _parar('InputGame parts sack press', 0x42b699)
        if m.u16(PAGINA) == 8:
            m.u16(CURSOR_ID, 0x1e0e)
            m.u32(CURSOR_ANIM, 0)
            return
        ruim = (self._iluminada(si, p) and self._colisao(si, 1) and self._selecao_terrestre(p)) or (
            not self._iluminada(si, p) and self._obstaculo(si) and self._selecao_terrestre(p))
        if ruim:
            m.u16(CURSOR_ID, 0x1e0e)
            m.u32(CURSOR_ANIM, 0)
            return
        m.u32(CURSOR_ANIM, self._contador(mascara=7))
        m.u16(CURSOR_ID, 0x1df5)
        if m.u8(AE) and m.u8(AF):
            self._ordre(p, 5, si, 0, sitio=0x42b82a)
            m.u16(0x496204, si)
            m.u16(0x4e05ac, 0x1e03)

    def _travail(self, p, tipo):
        return self.p('EnginTravailSelectionne', 0x42b375,
                      regs=dict(EAX=p, EDX=tipo, EBX=0, ECX=0, ESI=0, EDI=p, EBP=0))['EAX'] & 0xff

    def _caixa(self, p):
        """0x42b854: the drag box while the left button is down; its release selects (tag 1/2)."""
        m = self.m
        if not (m.u8(ARRASTO) and m.u8(AE)):
            return
        x, y = m.u16(CURSOR_X), m.u16(CURSOR_Y)
        w32, h32 = m.u16(VISTA + 4) << 5, m.u16(VISTA + 6) << 5
        m.u16(0x49a028, x if x < w32 else w32 - 1)
        m.u16(0x49a02a, y if y < h32 else h32 - 1)
        linha = _div32(_s16(m.u16(0x49a02a))) + m.u16(VISTA + 2)
        m.u16(0x4e19b4, ((linha << 8) + _div32(_s16(m.u16(0x49a028))) + m.u16(VISTA)) & 0xffff)
        if m.u8(AF):
            self._core('DeSelectionGroupe', 0x42b935, EAX=p)
            self._core('SelectionEngin', 0x42b94a, EAX=p, EDX=m.u16(0x4e19b2), EBX=m.u16(0x4e19b4))
            if not self._tropas(p):
                m.u8(0x4e17b8, 3)                                  # SetDebug 0x43f92a
                m.u16(0x4963c0, m.u16(ESTRUTURA_SOB))
                s = m.u16(ESTRUTURA_SOB)
                if s != 0xffff and self._dono_estrutura(s) == p:
                    self._ordre(p, 2, s, 0, sitio=0x42b9aa)
                    self._core('BatimentSelection', 0x42b9b9, EAX=s)
                    m.u16(0x4e244c, 0)
                    m.u16(0x4e244e, 0)
                    if self._tipo_estrutura(s) == 0x10:
                        m.u8(0x496fd8, 1)
                        self.p('InitGameZone', 0x42b9f5, eax=1, edx=0)
            else:
                self._core('BatimentDeselectionner', 0x42ba03, EAX=p, EDX=1)
                self._ordre(p, 1, m.u16(0x4e19b2), m.u16(0x4e19b4), sitio=0x42ba20)
                m.u8(0x4e17b8, 1)                                  # SetDebug 0x43f92a
                m.u16(0x4963c0, m.u16(UNIDADE_SOB))
                m.u16(0x4e2454, 0)
            m.u8(ARRASTO, 0)
        m.u16(CURSOR_ID, 0x1e0c)
        m.u32(CURSOR_ANIM, 0)
        m.u16(CURSOR_X, m.u16(CURSOR_X) - 7)
        m.u16(CURSOR_Y, m.u16(CURSOR_Y) - 7)
