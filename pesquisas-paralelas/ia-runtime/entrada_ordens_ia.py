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
GRUPO, ESTADO_JOGO = 0x49a05a, 0x4e2f78   # WndProc's digit key; CalculGame's state (0x12 = playing)
ICONES = 0x4e2410                # 10 slots of (u16 id, u16 active, u16 extra)


def _parar(descricao, endereco):
    raise DependenciaIA(descricao, endereco)


def _s16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


def _s8(v):
    v &= 0xff
    return v - 0x100 if v & 0x80 else v


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


def batiment_peut_attaquer_prefixo(m, regs):
    """BatimentPeutAttaquer 0x42436c, its type prefix only (0x42436c..0x4243b9, from the intact bytes): AX the
    attacking structure; byte +8 of its record not 0xa or 0xb (not a turret) -> AL = 0 at 0x4243b0 with
    EAX = 0, EBX = the record address, EDX = the u16 index, ECX/ESI/EDI/EBP restored. A turret (types 0xa/0xb)
    continues into the target checks 0x42443f, which are Combat's (``DependenciaIA`` there, nothing stored)."""
    s = regs['EAX'] & 0xffff
    rec = (0x49a0c8 + 276 * s) & M32
    if m.u8(rec + 8) in (0xa, 0xb):
        _parar("BatimentPeutAttaquer turret target checks (Combat)", 0x42443f)
    return dict(regs, EAX=0, EBX=rec, EDX=s)


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

    def _texto(self, n, sitio):                          # TextGetMessage 0x478a3b, called at ``sitio``
        """u32 [[0x5099a4] + 4n]. In the MONDE01 display scenario InitTextLangue never runs (TEXTES.TXT needs CRT
        fgets/ftell, not inventoried I/O boundaries), so the table pointer is 0 and the body would read unmapped
        low memory. The frame chain declares TextGetMessage as the same boundary as Missions' display scenario
        (``oraculo_exibicao_missao.FRONTEIRAS_EXIBICAO``: EAX 0, no cleanup, the body never executed): a bound
        provider ``TextGetMessage(n, local) -> EAX`` (``local``: the call site) answers it. Without one (the leaf bench) the pointer-0 read
        is a named gap, never a guessed 0."""
        tabela = self.m.u32(0x5099a4)
        if tabela == 0:
            if self.p is not None and 'TextGetMessage' in getattr(self.p, 'funcoes', {}):
                return self.p('TextGetMessage', sitio, n=n & 0xffff, local=sitio) & M32
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
        return self.engin_select_peut_attaquer(dict(EAX=jogador & 0xff, EDX=modo & 0xff, EBX=alvo & 0xffff,
                                                    ECX=0, ESI=0, EDI=0, EBP=0))['EAX'] & 0xff

    @staticmethod
    def _armee(t):                                       # TypeEnginEstArmee 0x44230c
        t &= 0xff
        return t <= 3 or t == 8 or 0xb <= t <= 0xc or 0xf <= t <= 0x10 or 0x12 <= t <= 0x19

    @staticmethod
    def _peut_attaquer_type(atacante, alvo):             # TypeEnginPeutAttaquer 0x453d7d (AL, DL)
        if alvo in (0x11, 0xa):
            return 0
        if alvo == 0x10 and atacante not in (2, 8):
            return 0
        return 1

    @staticmethod
    def _largue_bombe(t):                                # TypeEnginLargueBombe 0x4422eb
        return t in (0xe, 0x10)

    @staticmethod
    def _est_troupe(t):                                  # TypeEnginEstTroupe 0x442347
        return t not in (3, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x19)

    # ------------------------------------------------------------ selection and structure leaves (round 3)
    # Each takes the entry registers EAX..EBP and returns them as the original leaves them.
    def engin_select_peut_attaquer(self, r):
        """EnginSelectPeutAttaquer 0x472355 (AL player, DL mode, BX target; ECX/ESI saved, EBX/EDX not):
        mode 5: 1; mode 1: 0 for a type-0x11 target; then every live selected unit must be an army type
        (TypeEnginEstArmee), for mode 1 able to attack the target's type (TypeEnginPeutAttaquer), and a bomber
        type (TypeEnginLargueBombe) must hold a bomb (+0xda)."""
        m, j, modo = self.m, r['EAX'] & 0xff, r['EDX'] & 0xff
        eax, ebx, edx = r['EAX'], r['EBX'], r['EDX']
        alvo_tipo = None
        if modo == 1:
            alvo_tipo = self._tipo(r['EBX'] & 0xffff)
            if alvo_tipo == 0x11:
                return dict(r, EAX=0)
            eax = alvo_tipo
        elif modo == 5:
            return dict(r, EAX=(eax & 0xffffff00) | 1)
        for u in self._selecao(j):
            eax = int(self._vivo(u))
            if not eax:
                continue
            t = self._tipo(u)
            ebx = t
            if not self._armee(t):
                return dict(r, EAX=0, EBX=ebx, EDX=edx)
            if modo == 1:
                edx = alvo_tipo
                if not self._peut_attaquer_type(t, alvo_tipo):
                    return dict(r, EAX=0, EBX=ebx, EDX=edx)
            if not self._largue_bombe(t):
                eax = 0
                continue
            eax = m.u8(self._rec(u) + 0xda)
            if not eax:
                return dict(r, EAX=0, EBX=ebx, EDX=edx)
        return dict(r, EAX=(eax & 0xffffff00) | 1, EBX=j << 9, EDX=edx)

    def _laco_selecao(self, r, teste):
        """The shared loop of EnginSelectEstTroupe/EstEngin 0x4729b4/0x472a0c (AL player): a live unit whose
        type fails ``teste`` returns 0 at once; AL = 1 when a live unit passed (EAX upper bits: the last call's)."""
        eax, achou = r['EAX'], 0
        for u in self._selecao(r['EAX']):
            eax = int(self._vivo(u))
            if not eax:
                continue
            eax = teste(self._tipo(u))
            if not eax:
                return dict(r, EAX=0)
            achou = 1
        return dict(r, EAX=(eax & 0xffffff00) | achou)

    def engin_select_est_troupe(self, r):
        """EnginSelectEstTroupe 0x4729b4: TypeEnginEstTroupe returns 0x101 (true) or 0."""
        return self._laco_selecao(r, lambda t: 0x101 if self._est_troupe(t) else 0)

    def engin_select_est_engin(self, r):
        """EnginSelectEstEngin 0x472a0c: TypeEnginEstEngin 0x442434 (types 0xb..0x11) returns 1 or 0."""
        return self._laco_selecao(r, lambda t: int(0xb <= t <= 0x11))

    def engin_select_contient_miroir(self, r):
        """EnginSelectContientMiroir 0x472a64: AL = 1 at the first live mirror unit (EnginEstMiroir), else 0."""
        eax = r['EAX']
        for u in self._selecao(r['EAX']):
            eax = int(self._vivo(u))
            if eax:
                eax = self._miroir(u)
                if eax:
                    return dict(r, EAX=1)
        return dict(r, EAX=eax & 0xffffff00)

    def engin_select_peuvent_transporter(self, r):
        """EnginSelectPeuventTransporter 0x472ab2: 0 when a live selected unit's type is not 5, 6, 7 or 0xd."""
        eax = r['EAX']
        for u in self._selecao(r['EAX']):
            eax = int(self._vivo(u))
            if eax and self._tipo(u) not in (5, 7, 6, 0xd):
                return dict(r, EAX=0)
        return dict(r, EAX=(eax & 0xffffff00) | 1)

    def engin_select_est_blesse(self, r):
        """EnginSelectEstBlesse 0x4721f9: AL = (live selected units with hit points +0x9a != the type's
        maximum (u16 0x4965b6 + 50 * type) >= 1); EAX bits 8..15 = the count's."""
        n = 0
        for u in self._selecao(r['EAX']):
            if self._vivo(u) and self.m.u16(self._rec(u) + 0x9a) != self.m.u16(0x4965b6 + 50 * self._tipo(u)):
                n += 1
        n &= 0xffff
        return dict(r, EAX=(n & 0xff00) | int(n >= 1))

    def engin_select_peut_deposer(self, r):
        """EnginSelectPeutDeposer 0x4722a5 (AL player, DX structure; EBX/ECX saved, EDX is the loop index): a
        live selected unit makes it 0 unless the structure type is 3 (unit types 5, 6, 7, 0xd) or 4 (type 5);
        AL = 1 when one live unit qualified."""
        j, tipo = r['EAX'] & 0xff, self._tipo_estrutura(r['EDX'])
        lista = self._selecao(j)
        achou = 0
        for i, u in enumerate(lista):
            if not self._vivo(u):
                continue
            t = self._tipo(u)
            if tipo < 3 or tipo > 4 or (tipo == 3 and t not in (7, 5, 0xd, 6)) or (tipo == 4 and t != 5):
                return dict(r, EAX=0, EDX=i)
            achou = 1
        return dict(r, EAX=((j << 9) & 0xffffff00) | achou, EDX=len(lista))

    def batiment_est_depot(self, r):
        """BatimentEstDepot 0x4191c9 (AX): EAX = 1 for structure types 3 and 4, else 0."""
        return dict(r, EAX=int(self._tipo_estrutura(r['EAX']) in (3, 4)))

    def batiment_est_neutre(self, r):
        """BatimentEstNeutre 0x41d02b (AX): EAX = (owner == 0xc8)."""
        return dict(r, EAX=int(self._dono_estrutura(r['EAX']) == 0xc8))

    def player_est_allie(self, r):
        """PlayerEstAllie 0x46d838 (AL, DL): 1 for the same player; 0 when either is above 4; else bit DL of the
        byte [0x5080a8] + 20 * AL + 6 (DL becomes 1 << DL)."""
        a, b = r['EAX'] & 0xff, r['EDX'] & 0xff
        if a == b:
            return dict(r, EAX=(r['EAX'] & 0xffffff00) | 1)
        if a > 4 or b > 4:
            return dict(r, EAX=0)
        bit = 1 << b
        edx = (r['EDX'] & 0xffffff00) | bit
        aliados = self.m.u8(self.m.u32(0x5080a8) + 20 * a + 6)
        return dict(r, EAX=int(bool(aliados & bit)), EDX=edx)

    def batiment_est_ennemi(self, r):
        """BatimentEstEnnemi 0x41a61c (AX structure, DL player; EBX saved, EDX not): 0 for a 0xc8 owner (EDX =
        the structure), else not PlayerEstAllie(owner, player)."""
        s, j = r['EAX'] & 0xffff, r['EDX'] & 0xff
        dono = self._dono_estrutura(s)
        if dono == 0xc8:
            return dict(r, EAX=0, EDX=s)
        a = self.player_est_allie(dict(r, EAX=dono, EDX=j))
        return dict(r, EAX=0 if a['EAX'] & 0xff else 1, EDX=a['EDX'])

    def batiment_peut_se_vendre(self, r):
        """BatimentPeutSeVendre 0x4233d8 (AX): 0 for type 0x11 (EAX upper bits = 276 * structure) or a nonzero
        byte +0x74, else 1."""
        s = r['EAX'] & 0xffff
        if self._tipo_estrutura(s) == 0x11:
            return dict(r, EAX=(s * PASSO) & 0xffffff00)
        return dict(r, EAX=0 if self.m.u8(0x49a0c8 + s * PASSO + 0x74) else 1)

    def cherche_indice_batiment(self, r):
        """ChercheIndiceBatiment 0x41b54a (AX cell): the structure index of the cell's grid word [0x4e0f38]
        (bit 15 set, bits 5..14), else 0xffff."""
        return dict(r, EAX=self._estrutura_na_celula(r['EAX']))

    def _estrutura_na_celula(self, celula):
        w = self.m.u16(self.m.u32(0x4e0f38) + 2 * (celula & 0xffff))
        return (w & 0x7fe0) >> 5 if w & 0x8000 else 0xffff

    def _construida(self, s):                            # BatimentConstruit 0x41c652
        b = 0x49a0c8 + (s & 0xffff) * PASSO
        return self.m.u16(b + 0xa) == self.m.u16(0x495d90 + 52 * self.m.u8(b + 8))

    def _dano(self, s):                                  # BatimentGetDegatEffectif 0x41a976
        return self.m.u16(0x49a0c8 + (s & 0xffff) * PASSO + 6)

    FOLHAS = {'EnginSelectPeutAttaquer': 'engin_select_peut_attaquer', 'EnginSelectEstTroupe': 'engin_select_est_troupe',
              'EnginSelectEstEngin': 'engin_select_est_engin',
              'EnginSelectContientMiroir': 'engin_select_contient_miroir',
              'EnginSelectPeuventTransporter': 'engin_select_peuvent_transporter',
              'EnginSelectEstBlesse': 'engin_select_est_blesse', 'EnginSelectPeutDeposer': 'engin_select_peut_deposer',
              'BatimentEstDepot': 'batiment_est_depot', 'BatimentEstNeutre': 'batiment_est_neutre',
              'BatimentEstEnnemi': 'batiment_est_ennemi', 'PlayerEstAllie': 'player_est_allie',
              'BatimentPeutSeVendre': 'batiment_peut_se_vendre', 'ChercheIndiceBatiment': 'cherche_indice_batiment'}

    def chamar_folha(self, nome, regs):
        """Run the round-3 leaf ``nome`` with entry registers ``regs`` (EAX..EBP)."""
        return getattr(self, self.FOLHAS[nome])({k: regs[k] & M32 for k in REG7})

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
        elif msg == 0x100:
            wparam = self._tecla_baixo(wparam)
        elif msg == 0x101:
            r = self._tecla_cima(regs, wparam, lparam)
            if r is not None:
                return r
        else:
            _parar(f'WndProc message 0x{msg:x}', 0x4181b5)
        return dict(regs, EAX=0, EBX=regs['EBX'], ECX=lparam, EDX=wparam)

    def _tecla_baixo(self, wparam):
        """WM_KEYDOWN 0x418301 (in game state 0x12 only): digits 1..9 store [0x49a05a] = digit (DL -= 0x30, EDX
        keeps the result), F1..F4 [0x497284] = 1..4. VK_ADD/VK_SUBTRACT (zoom) and F11 are named stops past their
        gates. Returns EDX."""
        m = self.m
        if m.u8(ESTADO_JOGO) != 0x12:
            return wparam
        if 0x31 <= wparam <= 0x39:
            m.u8(GRUPO, wparam - 0x30)
            return (wparam & 0xffffff00) | ((wparam - 0x30) & 0xff)
        if 0x70 <= wparam <= 0x73:
            m.u8(0x497284, wparam - 0x6f)
        elif wparam == 0x6b:
            if _s8(m.u8(0x508f90)) > 0 and m.u16(0x49a018) == 0x320:
                _parar('WndProc VK_ADD zoom (InitGameZone/SetClipping)', 0x418374)
        elif wparam == 0x6d:
            if _s8(m.u8(0x508f90)) < 3 and m.u16(0x49a018) == 0x320:
                _parar('WndProc VK_SUBTRACT zoom (MiniMapRecentre)', 0x41843e)
        elif wparam == 0x7a:
            _parar('WndProc F11 (ResetMode, MiniMapRecentre)', 0x418488)
        return wparam

    def _tecla_cima(self, regs, wparam, lparam):
        """WM_KEYUP 0x4182eb: F5 (0x74) without a network ([0x4e0730] = 0, ReseauActif) steps [0x49a05b] mod 4
        (EDX = the remainder); Tab (9) toggles [0x497285] and calls InitGameZone(1, 0) (Core). Returns the exit
        registers when they differ from the plain exit, else None."""
        m = self.m
        if wparam == 0x74:
            if self.reseau_actif(dict(regs, EAX=0x101, EDX=wparam, ECX=lparam))['EAX'] & 0xff:
                return None
            _, resto = _idiv(m.u8(0x49a05b) + 1, 4)
            m.u8(0x49a05b, resto)
            return dict(regs, EAX=0, ECX=lparam, EDX=resto)
        if wparam == 9:
            m.u8(0x497285, int(m.u8(0x497285) == 0))
            saida = self.p('InitGameZone', 0x4182bb, eax=1, edx=0)
            return dict(regs, EAX=0, ECX=None, EDX=None) if saida is None else dict(
                regs, EAX=0, ECX=saida.get('ECX'), EDX=saida.get('EDX'))
        return None

    def reseau_actif(self, regs):
        """ReseauActif 0x42c3b0: AL = [0x4e0730]."""
        return dict(regs, EAX=_baixo(regs['EAX'], self.m.u8(0x4e0730)))

    def go_last_attaque(self, regs):
        """GoLastAttaque 0x440b63 (EAX, EDX: the view word addresses): within 1,000 cycles (unsigned) of the last
        attack [0x4e19c0] at a cell [0x496acc] != 0xffff, centres the view there, clamped to the map. EBX, ECX,
        ESI, EDI preserved; EDX = the cycle difference, or EAX = EDX = map height - view height when it moves."""
        m = self.m
        dif = (m.u32(0x508f7c) - m.u32(0x4e19c0)) & M32
        celula = m.u16(0x496acc)
        if dif > 1000 or celula == 0xffff:
            return dict(regs, EDX=dif)
        x = celula % 256 - _idiv(m.u16(VISTA + 4), 2)[0]
        y = celula // 256 - _idiv(m.u16(VISTA + 6), 2)[0]
        x = max(x, 0)
        limite = m.u16(LARGURA_MAPA) - m.u16(VISTA + 4)
        if x > _s32(limite):
            x = limite
        y = max(y, 0)
        limite = m.u16(ALTURA_MAPA) - m.u16(VISTA + 6)
        if y > _s32(limite):
            y = limite
        m.u16(regs['EAX'], x & 0xffff)
        m.u16(regs['EDX'], y & 0xffff)
        return dict(regs, EAX=limite & M32, EDX=limite & M32)

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

    @staticmethod
    def bag_ordre_estrutura(tipo, jogador):
        """BatimentGetBagOrdre 0x41c734 (AL structure type, DL player): the player's order Bag of that type."""
        return (0x4dd6e8 + 0x8f0 * (jogador & 0xff) + 104 * (tipo & 0xff)) & M32

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
            elif codigo == 6:
                self._icone_recrutamento(slot, tipo)
            elif codigo in (4, 7):
                _parar(f'IconeFillContenu Bag code {codigo}', {4: 0x45e40c, 7: 0x45e696}[codigo])
            slot += 1                                   # 0x45ddf7: codes 1, 5 and > 7 use a slot unwritten
            if slot == 4:
                return
            k += 1
        for s in range(slot, 4):
            self._icone(s, 0x29b1, 1, 0)

    def _icone_recrutamento(self, slot, tipo):
        """IconeFillContenu's code 6 (a recruitable unit type; 0x45e430..0x45e691), local player j, icon
        0x29cf + type (type 0x19 shows 0x12):
        - EnginEnRecrutement(AL type, DL j) (Economy) nonzero: (icon, 0, GetStatusRecrute(AL type, DL j) & 0xffff);
        - else BatimentEstOccupe(DL j) (0x422fa5: the selected structure's u32 +0x8c nonzero) : (icon, 0, 0);
        - else EnginGetRessource(AL type) (food +2, stone +6, parts +4 of the 50-byte record 0x4965ae + 50 type,
          into the caller's frame) and TestRessource(AX food, DX stone, BX parts, CX 0, pushed j) (Economy):
          (icon, 1, 0) when accepted, else (icon, 0, 0).
        Each store sets byte 0x4e05a2 when the triple changes (``_icone``)."""
        m = self.m
        j = m.u8(0x508041)
        icone = 0x29cf + (0x12 if tipo == 0x19 else tipo)
        if self.p('EnginEnRecrutement', 0x45e447, tipo=tipo, jogador=j) & 0xff:
            self._icone(slot, icone, 0, self.p('GetStatusRecrute', 0x45e480, tipo=tipo, jogador=j) & 0xffff)
            return
        selecionada = m.u16(SEL_ESTRUTURA + 2 * j)                       # BatimentEstOccupe 0x422fa5
        if selecionada != 0xffff and m.u32(0x49a0c8 + 276 * selecionada + 0x8c):
            self._icone(slot, icone, 0, 0)
            return
        r = 0x4965ae + 50 * tipo                                         # EnginGetRessource 0x4410d2
        comida, pecas, pedra = m.u16(r + 2), m.u16(r + 4), m.u16(r + 6)
        ok = self.p('TestRessource', 0x45e5c1, regs=dict(EAX=comida, EDX=pedra, EBX=pecas, ECX=0),
                    pilha=[j])['EAX'] & 0xff
        self._icone(slot, icone, 1 if ok else 0, 0)

    def calcul_icone_action(self, regs):
        """CalculIconeAction 0x45e944 (exit registers restored except EAX)."""
        m = self.m
        local = m.u8(0x508041)
        if self._nb(local) == 1:
            m.u8(0x496d48, 0)
            u = self._primeira(local)
            self.icone_fill_contenu(self.bag_ordre(u), 1, u)
            return dict(regs, EAX=None)             # IconeFillContenu's leftover EAX; CalculGame discards it
        estrutura = self._sel_estrutura(local)
        if estrutura != 0xffff:
            # 0x45e9bf: BatimentGetType(AX = the selected structure) reads byte +8 unfiltered; BatimentGetBagOrdre
            # 0x41c734 (AL type, DL player) = 0x4dd6e8 + 0x8f0 * player + 104 * type, EBX = 0xffff kept;
            # IconeFillContenu(EAX Bag, DL 3, BX 0xffff); byte 0x496d48 = 1.
            tipo = m.u8(0x49a0c8 + 276 * estrutura + 8)
            self.icone_fill_contenu(self.bag_ordre_estrutura(tipo, local), 3, 0xffff)
            m.u8(0x496d48, 1)
            return dict(regs, EAX=None)             # IconeFillContenu's leftover EAX; CalculGame discards it
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
        elif etiqueta == 0xb:
            chamar('SauveSelectionGroupe', 0x45eef8, EAX=j, EDX=b(2))
        elif etiqueta == 0xc:
            chamar('BatimentDeselectionner', 0x45ef07, EAX=j)
            chamar('DeSelectionGroupe', 0x45ef11, EAX=j)
            chamar('RestaureSelectionGroupe', 0x45ef2c, EAX=j, EDX=b(2))
        elif etiqueta == 0x10:
            if w(2) == 1:
                chamar('SetEnginSelectRentreEngin', 0x45f17a, EAX=j, EDX=w(4))
            elif w(2) == 3:
                chamar('SetEnginSelectRentreBatiment', 0x45f195, EAX=j, EDX=w(4))
        elif etiqueta == 0x21:
            chamar('BatimentRetireColon', 0x45f22a, EAX=w(2))
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

    def _grupo(self, p):
        """0x4293e0: the digit WndProc stored. Ctrl held: tag 0xb (store group); else tag 0xc (restore), and with
        Shift held the view is centred on the group (EnginGetCentreGroupe, then clamped to the map). Then
        [0x49a05a] = 0."""
        m = self.m
        g = m.u8(GRUPO)
        if self._tecla(0x11, 0x4293e9) < 0:
            self._ordre(p, 0xb, g, 0, sitio=0x429540)
        elif self._tecla(0x10, 0x429403) >= 0:
            self._ordre(p, 0xc, g, 0, sitio=0x429540)
        else:
            self._ordre(p, 0xc, g, 0, sitio=0x429425)
            self.p('EnginGetCentreGroupe', 0x42943e, regs=dict(EAX=p, EDX=VISTA, EBX=VISTA + 2, ECX=g))
            for o, t, mapa in ((0, 4, LARGURA_MAPA), (2, 6, ALTURA_MAPA)):
                meio = _idiv(m.u16(VISTA + t), 2)[0]
                m.u16(VISTA + o, m.u16(VISTA + o) - meio if m.u16(VISTA + o) >= meio else 0)
                if m.u16(VISTA + o) + m.u16(VISTA + t) >= m.u16(mapa):
                    m.u16(VISTA + o, m.u16(VISTA + o) - (m.u16(VISTA + o) + m.u16(VISTA + t) - m.u16(mapa)))
        m.u8(GRUPO, 0)

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
        if m.u8(GRUPO):
            self._grupo(p)
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
        if self._tecla(0x11, 0x4295fc) < 0:                # 0x429601: the deposit mode
            transporte = self._tropas(p) and self.engin_select_peuvent_transporter(dict(EAX=p))['EAX'] & 0xff
            if m.u16(PAGINA) != 9:
                if transporte:
                    m.u16(PAGINA, 8)
            elif not transporte:
                m.u16(PAGINA, 0)
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
            self.go_last_attaque(dict(dict.fromkeys(REG7, 0), EAX=VISTA, EDX=VISTA + 2))
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
                loc['info'] = self._texto((tipo & 0xff) + 0x28, 0x42be16)
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
                loc['info'] = self._texto(0x61, 0x42c218)
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
            loc['info'] = self._texto(((self._tipo_sac(si) & 0xff) + 0x28) & 0xffff, 0x4299d0)
            loc['info2'] = self.p('SacGetCapacite', 0x4299da, celula=si)
        elif self._gc(si):
            loc['info'] = self._texto(0x2c, 0x4299f4)
        elif self._mina(si):
            loc['info'] = self._texto(0x5b, 0x429a0e)
            loc['info2'] = self.p('MineGetCapacite', 0x429a22,
                                  indice=self.p('MineGetIndice', 0x429a18, celula=si) & 0xffff)
            loc['flag'] = 0
        elif self._armadilha(si, p):
            loc['info'] = self._texto(0x33, 0x429a46)
            loc['info2'], loc['flag'] = 0xffff, 0
        tipo_sob, objeto = 5, si                     # [ebp-0xc] and ECX's low word from 0x429a6c on
        if self._iluminada(si, p):
            s = self._estrutura_na_celula(si)
            m.u16(ESTRUTURA_SOB, s)
            if s != 0xffff:
                tipo_sob, objeto = 3, s
                loc['info'] = self._nome_estrutura(self._tipo_estrutura(s))
                loc['info2'] = 0xffff
            u = self._chercher_unite(si)
            m.u16(UNIDADE_SOB, u)
            if u != 0xffff:
                tipo_sob, objeto = 1, u
                loc['info'] = self._nome_unidade(self._tipo(u))
                loc['info2'] = 0xffff
                if self._est_selectionne(m.u8(0x508041), u) and m.u8(B0):
                    self.p('PlaySnd_StopSound', 0x429b6a,
                           regs=dict(EAX=self._rec(u) + 0x104, EDX=2, EBX=u * PASSO, ECX=u))
                    self._core('EnginAsk', 0x429b79, EAX=u, EDX=2, EBX=0, ECX=u)
        self.tipo_sob, self.objeto_sob = tipo_sob, objeto
        if pagina == 9:
            return self._pagina_deposito(p, si)
        if pagina == 0xc:
            return self._pagina_grupo(p)
        if pagina == 0xb:
            return self._pagina_engenheiro(p)
        if pagina == 2:
            return self._pagina_ataque(p, tipo_sob, objeto)
        if pagina == 7:
            return self._pagina_venda(p, si)
        if pagina in (0xd, 5, 0xa):
            _parar(f'InputGame help page 0x{pagina:x}', {0xd: 0x42a080, 5: 0x42a110, 0xa: 0x42a373}[pagina])
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

    def _cursor(self, ident, anim):
        self.m.u16(CURSOR_ID, ident)
        self.m.u32(CURSOR_ANIM, anim)

    def _clique(self):
        return self.m.u8(AE) and self.m.u8(AF)

    def _apontar(self, si):
        """0x42af9b: the pointer target word 0x496204 and the cursor-after-order word 0x4e05ac."""
        self.m.u16(0x496204, si)
        self.m.u16(0x4e05ac, 0x1e03)

    def _pagina_deposito(self, p, si):
        """Help page 9 0x429b90 (deposit target): a depot structure (types 3/4) the selection may use and the player
        owns, or no structure; the click sends tag 6/7/8/0x13 by table 0x42923c[u16 0x4e05b0] (BX = u16 0x4e05b2,
        CX = 2 with the structure as word 6, else 1 with the cell; word 8 = byte 0x4e05b4)."""
        m = self.m
        s = m.u16(ESTRUTURA_SOB)
        if s != 0xffff and not (self.batiment_est_depot(dict(EAX=s))['EAX'] and
                                self.engin_select_peut_deposer(dict(EAX=p, EDX=s))['EAX'] & 0xff and
                                self._dono_estrutura(s) == p):
            return self._cursor(0x1e0e, 0)
        self._cursor(0x1e40, self._contador(3, endereco=0x508f84))
        if not self._clique():
            return
        modo = m.u16(0x4e05b0)
        if modo <= 3:
            etiqueta = (6, 7, 8, 0x13)[modo]
            if s != 0xffff:
                self._ordre(p, etiqueta, m.u16(0x4e05b2), 2, s, m.u8(0x4e05b4), sitio=0x429c88)
            else:
                self._ordre(p, etiqueta, m.u16(0x4e05b2), 1, si, m.u8(0x4e05b4), sitio=0x429c88)
        m.u16(PAGINA, 0)
        self._apontar(si)

    def _pagina_grupo(self, p):
        """Help page 0xc 0x429daa (Shift): a selectable unit under the cursor; the button release (AF alone)
        sends tag 0x24 (add it to the group)."""
        u = self.m.u16(UNIDADE_SOB)
        if u == 0xffff or not self._core('EnginSelectionnable', 0x429dc5, EAX=u)['EAX'] & 0xff:
            return
        self._cursor(0x1df0, self._contador(5))
        if self.m.u8(AF):
            self._ordre(p, 0x24, u, 0, sitio=0x42aecf)

    def _pagina_engenheiro(self, p):
        """Help page 0xb 0x429e31 (the engineer's structure target, mode byte 0x496209): with a type-8 selection,
        a type-3 structure for a mode other than 3 or a type-7 structure for mode 3; the click sends tag 0x22."""
        m = self.m
        m.u16(0x4e0628, self._primeira(p))
        if m.u16(0x4e0628) == 0xffff or not self._tipo_selecionado(p, 8):
            m.u8(ARRASTO, 0)
            m.u8(MODO_ACAO, 0xff)
            m.u16(PAGINA, 0)
            m.u8(0x496d48, 1)
            return
        self._cursor(0x1e0e, 0)
        s = m.u16(ESTRUTURA_SOB)
        if s == 0xffff:
            _parar('InputGame page 0xb with no structure under the cursor (BatimentGetType(0xffff) reads '
                   '0x15d9fbc, outside the structure pool)', 0x429ea2)
        t, modo = self._tipo_estrutura(s), m.u8(MODO_9)
        if not ((t == 3 and modo != 3) or (t == 7 and modo == 3)):
            return
        self._cursor(0x1ea9, self._contador(3))
        if self._clique():
            self._ordre(p, 0x22, 3, s, modo, 0, sitio=0x42aecf)

    def _pagina_ataque(self, p, tipo_sob, objeto):
        """Help page 2 0x42a4a2 (Alt: forced attack on the object under the cursor, mode [ebp-0xc] = 1 unit,
        3 structure, 5 cell; ECX = the object). A selected structure asks Combat's BatimentPeutAttaquer; troops
        ask EnginSelectPeutAttaquer, or target a type-10 unit regardless. The click sends tag 0xe."""
        m = self.m
        sel = self._sel_estrutura(p)
        m.u16(0x4e0628, self._primeira(p))
        if sel != 0xffff:
            ok = self.p('BatimentPeutAttaquer', 0x42a4dc,
                        regs=dict(EAX=sel, EDX=tipo_sob, EBX=objeto, ECX=objeto, ESI=tipo_sob, EDI=p, EBP=0))
            if not ok['EAX'] & 0xff:
                return self._cursor(0x1e0e, 0)
            self._cursor(0x1dfd, self._contador(6))
            if self._clique():
                self._ordre(p, 0xe, tipo_sob, objeto, sitio=0x42a52c)
                m.u16(PAGINA, 0)
            return
        if m.u16(0x4e0628) == 0xffff:
            return
        if not self._pode_atacar(p, tipo_sob, objeto) and self._tipo(objeto) != 0xa:
            return self._cursor(0x1e0e, 0)
        self._cursor(0x1dfd, self._contador(6))
        if self._clique():
            self._ordre(p, 0xe, tipo_sob, objeto, sitio=0x42a5e6)
            m.u16(PAGINA, 0)

    def _pagina_venda(self, p, si):
        """Help page 7 0x42a600 (Delete: sell): ChercheIndiceBatiment replaces the structure under the cursor; an
        own structure that BatimentPeutSeVendre allows takes the click: tag 0xa, then BatimentDeselectionner."""
        m = self.m
        s = self._estrutura_na_celula(si)
        m.u16(ESTRUTURA_SOB, s)
        self._cursor(0x1e0e, 0)
        if s == 0xffff:
            return
        if self._dono_estrutura(s) != p or not self.batiment_peut_se_vendre(dict(EAX=s))['EAX'] & 0xff:
            return self._cursor(0x1e0e, 0)
        self._cursor(0x1e1c, self._contador(6))
        if self._clique():
            self._ordre(p, 0xa, s, 0, sitio=0x42a6a3)
            self._core('BatimentDeselectionner', 0x42a6aa, EAX=p)

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
        """0x42ac1f: troops selected -> ``_estrutura_tropas`` (0x42ac32); otherwise the selected structure's double
        click (tag 0x21), a selected structure's attack on a foreign structure (Combat's BatimentPeutAttaquer,
        tag 0xe), else an own structure's cursor and drag start (0x42b1ab)."""
        m = self.m
        if self._tropas(p):
            return self._estrutura_tropas(p, s, x, y, si)
        if self._sel_estrutura(p) == s and m.u8(B0):
            self._ordre(p, 0x21, s, 0, sitio=0x42aecf)
            return
        sel = self._sel_estrutura(p)
        if sel != 0xffff:
            ok = self.p('BatimentPeutAttaquer', 0x42b2a3, regs=dict(EAX=sel, EDX=3, EBX=s, ECX=s, ESI=si, EDI=p,
                                                                     EBP=0))['EAX'] & 0xff
            dono = self._dono_estrutura(s)
            if ok and dono != p and dono != 0xc8:
                self._cursor(0x1dfd, self._contador(6))
                if self._clique():
                    self._ordre(p, 0xe, 3, s, sitio=0x42aecf)
                return
        self._estrutura_propria(p, s, x, y, si)

    def _estrutura_propria(self, p, s, x, y, si):
        """0x42b1ab: an own structure's cursor and, with the left button down, the drag start."""
        if self._dono_estrutura(s) != p:
            return
        self._cursor(0x1df0, self._contador(5))
        if self.m.u8(AE):
            self._arrasto(x, y, si)

    def _estrutura_tropas(self, p, s, x, y, si):
        """0x42ac32: troops selected, structure ``s`` under the cursor.
        - Page 8 (Ctrl deposit mode): an own cave with carriers (types 5/7/6) selected arms page 9 (0x4e05b0 = 3,
          0x4e05b2 = the structure, 0x4e05b4 = 2 for builders, 1 for colonists, else 0); otherwise a move (tag 5).
        - A foreign, not neutral structure: type 0x10 or 2 with type-10 units selected, tag 0x10 (BX 3); else
          tag 0xe (BX 3) when EnginSelectPeutAttaquer(mode 3) allows it.
        - Otherwise: the builder first selected on an unbuilt or damaged structure, tag 0x14 (BX 3); wounded
          troops at an own built type-0x13 (troops) or type-0xe (engins) structure without mirrors, tag 0x15;
          EnginSelectPeutEntrer(mode 3) without mirrors: a built structure, tag 0x10 (BX 3), an unbuilt one,
          tag 5; else the own-structure drag start."""
        m = self.m
        if m.u16(PAGINA) == 8:
            if self._dono_estrutura(s) == p and self._tipo_estrutura(s) == 3 and (
                    self._tipo_selecionado(p, 5) or self._tipo_selecionado(p, 7) or self._tipo_selecionado(p, 6)):
                self._cursor(0x1e3d, self._contador(3, endereco=0x508f84))
                if self._clique():
                    m.u16(0x4e05b0, 3)
                    m.u16(0x4e05b2, s)
                    m.u16(PAGINA, 9)
                    m.u8(0x4e05b4, 2 if self._tipo_selecionado(p, 7) else 1 if self._tipo_selecionado(p, 5) else 0)
                return
            self._cursor(0x1e0e, 0)
            if self._clique():
                self._ordre(p, 5, si, 0, sitio=0x42ad8e)
                self._apontar(si)
            return
        if self.batiment_est_ennemi(dict(EAX=s, EDX=p))['EAX'] & 0xff and \
                not self.batiment_est_neutre(dict(EAX=s))['EAX'] & 0xff:
            t = self._tipo_estrutura(s)
            if t in (0x10, 2) and self._tipo_selecionado(p, 0xa):
                self._cursor(0x1e6f, self._contador(mascara=1))
                if self._clique():
                    self._ordre(p, 0x10, 3, s, sitio=0x42aecf)
                return
            if not self._pode_atacar(p, 3, s):
                return
            self._cursor(0x1dfd, self._contador(6))
            if self._clique():
                self._ordre(p, 0xe, 3, s, sitio=0x42aecf)
            return
        self._cursor(0x1df0, self._contador(5))
        if self._tipo(self._primeira(p)) == 7 and (not self._construida(s) or self._dano(s)):
            self._cursor(0x1e10, self._contador(6))
            if self._clique():
                self._ordre(p, 0x14, 3, s, sitio=0x42af96)
                self._apontar(si)
            return
        if self.engin_select_est_blesse(dict(EAX=p))['EAX'] & 0xff and self._dono_estrutura(s) == p:
            t = self._tipo_estrutura(s)
            alvo = (self.engin_select_est_troupe(dict(EAX=p))['EAX'] & 0xff and t == 0x13) or (
                self.engin_select_est_engin(dict(EAX=p))['EAX'] & 0xff and t == 0xe)
            if alvo and not self.engin_select_contient_miroir(dict(EAX=p))['EAX'] & 0xff:
                if not self._construida(s):
                    return
                self._cursor(0x1e3b, self._contador(mascara=1))
                if self._clique():
                    self._ordre(p, 0x15, s, 0, sitio=0x42aecf)
                return
        if self._pode_entrar_estrutura(p, s) and not self.engin_select_contient_miroir(dict(EAX=p))['EAX'] & 0xff:
            if self._construida(s):
                self._cursor(0x1e16, self._contador(6))
                if self._tipo_estrutura(s) == 0x15:
                    self._cursor(0x1eac, self._contador(9))
                if self._clique():
                    self._ordre(p, 0x10, 3, s, sitio=0x42aecf)
                return
            self._cursor(0x1e0e, 0)
            if self._clique():
                self._ordre(p, 5, si, 0, sitio=0x42af96)
                self._apontar(si)
            return
        self._estrutura_propria(p, s, x, y, si)

    def _pode_entrar_estrutura(self, p, s):
        """EnginSelectPeutEntrer 0x472b6c mode 3 (AL player, DL 3, BX structure): Core's ``entrada_estruturas``
        through the provider of the same name (a named dependency without it)."""
        return self.p('EnginSelectPeutEntrer', 0x42b0ae, regs=dict(EAX=p, EDX=3, EBX=s, ECX=0, ESI=0, EDI=p,
                                                                     EBP=0))['EAX'] & 0xff

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
        sel = self._sel_estrutura(p)
        if sel != 0xffff:
            # 0x42a9d3: BatimentPeutAttaquer(AX the selected structure, DL 1, BX the unit under the cursor, EDI the
            # player; ECX/ESI/EBP are not determined here and enter as 0) (Combat). AL = 0 continues at 0x42aa4d.
            ok = self.p('BatimentPeutAttaquer', 0x42a9ed, regs=dict(EAX=sel, EDX=1, EBX=m.u16(UNIDADE_SOB), ECX=0,
                                                                   ESI=0, EDI=p, EBP=0))
            if ok['EAX'] & 0xff:
                _parar('InputGame unit hover: the selected structure can attack the unit', 0x42a9f6)
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
        caverna = m.u16(ESTRUTURA_SOB) != 0xffff and self._tipo_estrutura(m.u16(ESTRUTURA_SOB)) == 3
        if self._gc(si) or self._tipo_sac(si) == 1 or caverna:
            if self._travail(p, 1):
                if m.u16(PAGINA) == 8:                          # 0x42b393: arm the deposit target page
                    return self._armar_deposito(si, 1 if self._gc(si) else 3 if caverna else 2, 1)
                m.u16(CURSOR_ID, 0x1e10)
                m.u32(CURSOR_ANIM, self._contador(6))
                if m.u8(AE) and m.u8(AF):
                    self._ordre(p, 7 if self._gc(si) else 0x12, si, 0, sitio=0x42b486 if self._gc(si) else 0x42af96)
                    m.u16(0x496204, si)
                    m.u16(0x4e05ac, 0x1e03)
                return
        if self._mina(si) or self._tipo_sac(si) == 2 or caverna:
            if self._travail(p, 2):
                if m.u16(PAGINA) == 8:                          # 0x42b525
                    return self._armar_deposito(si, 0 if self._mina(si) else 3 if caverna else 2, 2)
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

    def _armar_deposito(self, si, modo, carga):
        """Page 8 over a field (0x42b393) or a mine (0x42b525): the click sets page 9 with the deposit table index
        0x4e05b0, the first target cell 0x4e05b2 and the cargo byte 0x4e05b4."""
        m = self.m
        self._cursor(0x1e3d, self._contador(3, endereco=0x508f84))
        if not self._clique():
            return
        m.u16(PAGINA, 9)
        m.u16(0x4e05b0, modo)
        m.u16(0x4e05b2, si)
        m.u8(0x4e05b4, carga)

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
