"""Structure vision, group selection, minimap view and exit-position routines over live original memory (M3.1 round 2).

Translated from the intact bytes (``evidencias/visao-grupos/*.asm``) after the native capture
``evidencias/visao-grupos/captura-visao-grupos-exibicao.json.xz`` was committed. Routines:
- CalculBatimentNextEtape's per-player vision of a structure: BatimentIllumine 0x419233 (AX structure, DL player,
  BL nonzero = light, zero = put out) over its footprint rectangle, BatimentDecouvre 0x419d54 (AX structure,
  DL player) over the footprint grown by one cell on every side, and the per-cell routines they call,
  IllumineCase 0x476968, EteintCase 0x476adc and DecouvreCase 0x47670a (AX cell, DL player);
- SauveSelectionGroupe 0x4726f7 (AL player, DL group), RestaureSelectionGroupe 0x472769 (AL player, DL group),
  EnginGetCentreGroupe 0x442139 (AL player, EDX/EBX addresses of the u16 x/y results, CL group);
- MiniMapRecentre 0x46a01b and MiniMapSetPos 0x46a19e (AX x, DX y);
- CalculPosition 0x420698 (AX structure) with every register, and RechercheDecalageSortie 0x41d1d0 (AX structure).

Every routine takes EAX..EBP at its entry and returns EAX..EBP as the original leaves them, callee-saved registers
included; arithmetic flags are not modeled. ``memoria``: ``u8/u16/u32(addr, value=None)`` plus ``vista(addr, n)``
(``memoria_quadro_core.MemoriaQuadro``). The grids are reached through their live pointers (discovery
[0x507d78 + 4p], light borders [0x507d88 + 4p], light counts [0x507d98 + 4p]), so a cell outside the 256x256 grid
of a footprint touching row 255 writes where the original writes. SetMiniMap (modes 1/2/3, reached only when a cell
changes) is M2.3's ``visao_movimento.minimapa`` over flat-memory views of what it reads (no world is built); those
modes change nothing unless the player is the local one.

Reused single implementations: ``selecao_ordens`` (RetireSelectionEngin, EnginAsk with its volume and sound,
DeSelectionGroupe, BatimentDeselectionner), ``incursao_core.terreno_em_colisao`` (TerrainEnCollision).

Uncertain register bits: RechercheDecalageSortie's EAX bits 16..31 when a free neighbour is found (the upper word
of a 16-bit local the original never initializes, stack residue). Every other bit is exact.

Named dependency (never defaulted): Audio's PlaySnd_PostSound/PlaySnd_StopSound through ``som`` (RestaureSelection-
Groupe's voice, as in ``selecao_ordens``). Outside the translated domain (``ForaDoDominioVisao`` before any store):
players other than 0..3 in the per-cell routines (their grid pointers alias other grids; 0xc8's are beyond the
table), BatimentDecouvre excepted for player 0xc8 (an early return); RechercheDecalageSortie for structure types 9,
12, 17 and above 0x15 (uninitialized locals).
"""
from chamadas_quadro_core import DependenciaRamoCore  # noqa: F401  (re-exported for callers)

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
TIPOS_ESTRUTURA = 0x495d8c              # stride 52: u16 width, u16 height
DESCOBERTA, BORDAS, CONTAGENS = 0x507d78, 0x507d88, 0x507d98
MAPA_L, MAPA_A = 0x497168, 0x49716a
VISTA_X, VISTA_Y, VISTA_L, VISTA_A = 0x508720, 0x508722, 0x508724, 0x508726
MINI_X, MINI_Y, TRAVA_X, TRAVA_Y = 0x507d68, 0x507d6a, 0x507d6c, 0x507d6e
MINI_L, MINI_A = 0x496fe0, 0x496fe2
MARGEM = 0x508f90                       # signed byte (the top byte of the dword at 0x508f8d)
SELECOES = 0x508728                     # u16 count + u16 units, stride 0x200 per player
JOGADOR_LOCAL = 0x508041
ROTINAS = {
    'BatimentIllumine': 0x419233, 'BatimentDecouvre': 0x419d54, 'IllumineCase': 0x476968, 'EteintCase': 0x476adc,
    'DecouvreCase': 0x47670a, 'SauveSelectionGroupe': 0x4726f7, 'RestaureSelectionGroupe': 0x472769,
    'EnginGetCentreGroupe': 0x442139, 'MiniMapRecentre': 0x46a01b, 'MiniMapSetPos': 0x46a19e,
    'CalculPosition': 0x420698, 'RechercheDecalageSortie': 0x41d1d0,
}
# CalculPosition 0x420698: the geometry switch 0x420640 by structure type -> (width subtraction, height subtraction,
# source of the origin word's upper 16 bits), and the correction switches -> (correction, addback). The origin word
# is loaded into a 16-bit register whose upper half is: 0 ('0'), the caller's ESI/EDI ('ESI'/'EDI'), or the upper
# half of height-4 / width-1 ('h-4'/'w-1').
GEOMETRIA = {0x420885: (3, 2, 'ESI'), 0x42072e: (1, 1, 'EDI'), 0x4207a2: (4, 2, '0'), 0x420981: (4, 2, '0'),
             0x420819: (1, 0, '0'), 0x420afd: (4, 1, '0'), 0x420a79: (6, 4, 'h-4'), 0x420902: (6, 4, '0'),
             0x4209fe: (4, 1, '0'), 0x420b65: (1, 1, 'w-1')}
GEOMETRIA_POR_TIPO = (0x420885, 0x42072e, 0x4207a2, 0x4207a2, 0x420981, 0x420819, 0x4207a2, 0x420afd, 0x420a79,
                      None, 0x420885, 0x420885, None, 0x420afd, 0x420902, 0x4209fe, 0x4207a2, None, 0x420b65,
                      0x420981, 0x4209fe, 0x420981)
CORRECAO_POR_TIPO = (0x201, 0x300, 0x101, 0x202, 0x100, 0x202, 0x100, 0x300, 0x202, None, 0, 0, None, 0x200, 0x300,
                     0x100, 0x100, None, 0x201, 0x100, 0x100, 0x100)
REPOSICAO = {0x42072e: 0xff, 0x420b65: 1}       # other geometry branches add back 0x102
TIPOS_LOOP = range(0xb, 0x11)                   # TypeEnginEstEnLoop 0x440c44 (table 0x440c2c: all six -> 1)


class ForaDoDominioVisao(NotImplementedError):
    """A branch outside the translated domain; nothing was written by it."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made by this branch')


def _b(v, b):
    return (v & 0xffffff00) | (b & 0xff)


def _w(v, w):
    return (v & 0xffff0000) | (w & 0xffff)


def _s8(v):
    v &= 0xff
    return v - 0x100 if v & 0x80 else v


def _s16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


def _idiv2(v):
    """``mov eax, edx; sar edx, 31; sub eax, edx; sar eax, 1`` on a 32-bit value: (EAX, EDX)."""
    s = _s32(v)
    sinal = M32 if s < 0 else 0
    return ((s - (-1 if s < 0 else 0)) >> 1) & M32, sinal


class _VistaPlana:
    """Items of ``largura`` bytes at ``base`` + ``largura`` * index over flat memory, unbounded like the original's
    u16-indexed accesses (a minimap index past the 128x128 buffer reaches the memory after it)."""

    def __init__(self, m, base, largura=1):
        self._m, self._base, self._largura = m, base, largura
        self._f = m.u8 if largura == 1 else m.u16

    def __getitem__(self, i):
        return self._f((self._base + self._largura * i) & M32)

    def __setitem__(self, i, valor):
        self._f((self._base + self._largura * i) & M32, valor)


def _minimapa_plano():
    from visao_movimento import VisaoMovimento

    class MinimapaPlano(VisaoMovimento):
        """What M2.3's ``VisaoMovimento.minimapa`` (SetMiniMap 0x46a388) reads and writes, as flat-memory
        properties read at each use: no world is built, so only the bytes the routine touches are read."""

        def __init__(self, m):
            self._m = m

        def _p(self, endereco, largura=1):
            return _VistaPlana(self._m, self._m.u32(endereco), largura)

        tamanho_minimapa = property(lambda s: (s._m.u16(MINI_L), s._m.u16(MINI_A)))
        largura = property(lambda s: s._m.u16(MAPA_L))
        altura = property(lambda s: s._m.u16(MAPA_A))
        jogador_local = property(lambda s: s._m.u8(JOGADOR_LOCAL))
        objetos = property(lambda s: s._p(0x507d74))
        tiles = property(lambda s: s._p(0x507d70, 2))
        cores_tiles = property(lambda s: _VistaPlana(s._m, 0x509694))
        cores_jogadores = property(lambda s: _VistaPlana(s._m, 0x4e24dc))
        sombra = property(lambda s: s._p(0x4e24b4))
        mini_final = property(lambda s: s._p(0x507d5c))
        mini_unidades = property(lambda s: s._p(0x507d60))
        mini_estruturas = property(lambda s: s._p(0x507d64))
        descoberto = property(lambda s: [s._p(DESCOBERTA + 4 * j) for j in range(4)])
        luz_bordas = property(lambda s: [s._p(BORDAS + 4 * j) for j in range(4)])
    return MinimapaPlano


def _MinimapaPlano(m):
    return _minimapa_plano()(m)


class VisaoGrupos:
    """The routines over one live memory. ``som``: Audio's sound-library boundary, as in ``selecao_ordens``."""

    def __init__(self, memoria, *, som=None):
        self.m = memoria
        self.som = som
        self._selecao = self._mundo = None

    # ------------------------------------------------------------ composition
    def selecao(self):
        if self._selecao is None:
            from selecao_ordens import SelecaoOrdens
            self._selecao = SelecaoOrdens(self.m, som=self.som)
        return self._selecao

    def mundo(self):
        """The minimap side of M2.3's world over this memory (``_MinimapaPlano``)."""
        if self._mundo is None:
            self._mundo = _MinimapaPlano(self.m)
        return self._mundo

    def _pool(self):
        return self.m.u32(PONTEIRO_UNIDADES)

    def _rec(self, u):
        return (self._pool() + (u & 0xffff) * PASSO) & M32

    @staticmethod
    def _est(s):
        return (ESTRUTURAS + (s & 0xffff) * PASSO) & M32

    def _tamanho(self, tipo):
        return self.m.u16(TIPOS_ESTRUTURA + 52 * tipo), self.m.u16(TIPOS_ESTRUTURA + 52 * tipo + 2)

    # ------------------------------------------------------------ entry point
    def chamar(self, nome, regs, pilha=()):
        """Run routine ``nome`` with entry registers ``regs`` (EAX..EBP; missing keys are an error)."""
        r = {k: regs[k] & M32 for k in REG7}
        metodo = {
            'BatimentIllumine': self.batiment_illumine, 'BatimentDecouvre': self.batiment_decouvre,
            'IllumineCase': self.illumine_case, 'EteintCase': self.eteint_case, 'DecouvreCase': self.decouvre_case,
            'SauveSelectionGroupe': self.sauve_selection_groupe,
            'RestaureSelectionGroupe': self.restaure_selection_groupe,
            'EnginGetCentreGroupe': self.engin_get_centre_groupe, 'MiniMapRecentre': self.minimap_recentre,
            'MiniMapSetPos': self.minimap_set_pos, 'CalculPosition': self.calcul_position,
            'RechercheDecalageSortie': self.recherche_decalage_sortie,
        }.get(nome)
        if metodo is not None:
            return metodo(r)
        if nome in ('BatimentDeselectionner', 'DeSelectionGroupe'):
            return self.selecao().chamar(nome, r, pilha)
        raise KeyError(f'{nome} is not a translated vision/group/minimap routine')

    # ------------------------------------------------------------ per-cell vision
    def _jogador(self, rotina, endereco, p):
        if p > 3:
            raise ForaDoDominioVisao(rotina, endereco, f'player {p:#x} (grid pointers outside players 0..3)')

    def _bordas(self, base, celula, apagar):
        """The four neighbour border bits of DecouvreCase/IllumineCase (clear) and EteintCase (set), in order."""
        m = self.m
        x, y = celula % 256, celula >> 8
        lados = ((celula - 1, 2) if x else (celula, 8),
                 (celula - 0x100, 1) if y else (celula, 4),
                 (celula + 1, 8) if x != m.u16(MAPA_L) - 1 else (celula, 2),
                 (celula + 0x100, 4) if y != m.u16(MAPA_A) - 1 else (celula, 1))
        for alvo, bit in lados:
            a = (base + alvo) & M32
            m.u8(a, (m.u8(a) | bit) if apagar else (m.u8(a) & ~bit & 0xff))

    def _minimapa(self, p, celula, modo):
        """SetMiniMap 0x46a388 modes 1/2/3 (M2.3's ``minimapa``): only the local player's minimap changes."""
        if p == self.m.u8(JOGADOR_LOCAL):
            self.mundo().minimapa(p, celula, modo)

    def _decouvre_case(self, celula, p):
        """DecouvreCase 0x47670a body; returns (EAX, EDX) = (player, cell)."""
        m = self.m
        base = m.u32(DESCOBERTA + 4 * p)
        self._bordas(base, celula, False)
        if m.u8((base + celula) & M32):
            self._minimapa(p, celula, 1)
        a = (base + celula) & M32
        m.u8(a, m.u8(a) & 0xef)
        return p, celula

    def _illumine_case(self, celula, p):
        """IllumineCase 0x476968 body; returns (EAX, EDX) = (player, count | (count + 1) << 8 unless 0xff)."""
        m = self.m
        contagem = (m.u32(CONTAGENS + 4 * p) + celula) & M32
        if m.u8(contagem) == 0:
            base = m.u32(BORDAS + 4 * p)
            self._bordas(base, celula, False)
            a = (base + celula) & M32
            m.u8(a, m.u8(a) & 0xef)
            self._minimapa(p, celula, 2)
        n = m.u8(contagem)
        if n == 0xff:
            return p, n
        m.u8(contagem, n + 1)
        return p, n | (((n + 1) & 0xff) << 8)

    def _eteint_case(self, celula, p):
        """EteintCase 0x476adc body; returns (EAX, EDX) = (count byte address, (cell & 0xff) | count << 8)."""
        m = self.m
        contagem = (m.u32(CONTAGENS + 4 * p) + celula) & M32
        if m.u8(contagem) == 1:
            base = m.u32(BORDAS + 4 * p)
            self._bordas(base, celula, True)
            a = (base + celula) & M32
            m.u8(a, m.u8(a) | 0x10)
            self._minimapa(p, celula, 3)
        n = m.u8(contagem)
        if n:
            m.u8(contagem, n - 1)
        return contagem, (celula & 0xff) | (n << 8)

    def _por_celula(self, nome, endereco, r, funcao):
        p, celula = r['EDX'] & 0xff, r['EAX'] & 0xffff
        self._jogador(nome, endereco, p)
        eax, edx = funcao(celula, p)
        return dict(r, EAX=eax & M32, EDX=edx & M32)

    def illumine_case(self, r):
        """IllumineCase 0x476968: AX cell, DL player 0..3. A count of 0: the borders and the cell's own bit 4
        cleared, SetMiniMap mode 2; then the count grows unless 0xff. EAX = player, EDX = old count | new << 8
        (0xff alone when saturated); others preserved."""
        return self._por_celula('IllumineCase', 0x476968, r, self._illumine_case)

    def eteint_case(self, r):
        """EteintCase 0x476adc: AX cell, DL player 0..3. A count of 1: the borders and bit 4 set, SetMiniMap mode 3;
        then a nonzero count drops. EAX = the count byte's address, EDX = (cell & 0xff) | old count << 8."""
        return self._por_celula('EteintCase', 0x476adc, r, self._eteint_case)

    def decouvre_case(self, r):
        """DecouvreCase 0x47670a: AX cell, DL player 0..3. The borders cleared; a nonzero discovery byte gives
        SetMiniMap mode 1; then bit 4 cleared. EAX = player, EDX = cell; others preserved."""
        return self._por_celula('DecouvreCase', 0x47670a, r, self._decouvre_case)

    # ------------------------------------------------------------ structure vision
    def batiment_illumine(self, r):
        """BatimentIllumine 0x419233: AX structure, DL player 0..3, BL nonzero: IllumineCase, zero: EteintCase over
        the footprint (type width x height from the origin +2), rows then columns, cells whose column and row are
        0..255. EAX = height; EBX = width once a row is in range (else the origin word); EDX = the last cell
        routine's EDX, or the last row/column index tested; ECX/ESI/EDI/EBP preserved."""
        m = self.m
        s, p, acender = r['EAX'] & 0xffff, r['EDX'] & 0xff, r['EBX'] & 0xff
        self._jogador('BatimentIllumine', 0x419233, p)
        e = self._est(s)
        largura, altura = self._tamanho(m.u8(e + 8))
        origem = m.u16(e + 2)
        x, y = origem % 256, origem // 256
        ebx, edx = origem, 0
        celula_f = self._illumine_case if acender else self._eteint_case
        linha = 0
        while linha < altura:
            edx = linha
            if 0 <= y + linha < 0x100:
                ebx = 0
                while ebx < largura:
                    edx = x
                    if 0 <= ebx + x < 0x100:
                        celula = (m.u16(e + 2) + ebx + ((linha & 0xff) << 8)) & 0xffff
                        _, edx = celula_f(celula, p)
                    ebx += 1
            linha += 1
        return dict(r, EAX=altura, EBX=ebx & M32, EDX=edx & M32)

    def batiment_decouvre(self, r):
        """BatimentDecouvre 0x419d54: AX structure, DL player. Player 0xc8 returns at once (EAX = 0xc8, EDX = the
        structure word). Otherwise DecouvreCase over rows -1..height and columns -1..width around the origin (a
        dimension of 0x100 or more is not grown), cells whose column and row are 0..255. EAX = EDX = the grown
        height; EBX/ECX/ESI/EDI/EBP preserved."""
        m = self.m
        s, p = r['EAX'] & 0xffff, r['EDX'] & 0xff
        if p == 0xc8:
            return dict(r, EAX=0xc8, EDX=s)
        self._jogador('BatimentDecouvre', 0x419d54, p)
        e = self._est(s)
        largura, altura = self._tamanho(m.u8(e + 8))
        largura += largura < 0x100
        altura += altura < 0x100
        origem = m.u16(e + 2)
        x, y = origem % 256, origem // 256
        for linha in range(-1, altura):
            if not 0 <= linha + y < 0x100:
                continue
            for coluna in range(-1, largura):
                if 0 <= coluna + x < 0x100:
                    self._decouvre_case((m.u16(e + 2) + coluna + ((linha << 8) & 0xffff)) & 0xffff, p)
        return dict(r, EAX=altura, EDX=altura)

    # ------------------------------------------------------------ group selection
    def sauve_selection_groupe(self, r):
        """SauveSelectionGroupe 0x4726f7: AL player, DL group. For every live unit (state not 0/4) of that owner:
        a member of the group leaves it (+0xbc = 0), then a selected one (+0xbd) joins it. EAX = unit 799's last
        query (0 dead; the pool pointer with AL = owner for another owner; the pool pointer for the player);
        EDX = 0x320; others preserved."""
        m = self.m
        jogador, grupo = r['EAX'] & 0xff, r['EDX'] & 0xff
        eax = r['EAX']
        for u in range(0x320):
            rec = self._rec(u)
            if m.u8(rec + 2) in (0, 4):
                eax = 0
                continue
            eax = _b(self._pool(), m.u8(rec))
            if eax & 0xff != jogador:
                continue
            if m.u8(rec + 0xbc) == grupo:
                m.u8(rec + 0xbc, 0)
            eax = self._pool()
            if m.u8(rec + 0xbd):
                m.u8(rec + 0xbc, grupo)
        return dict(r, EAX=eax, EDX=0x320)

    def restaure_selection_groupe(self, r):
        """RestaureSelectionGroupe 0x472769: AL player, DL group. For every live unit of that owner: a selected one
        is unselected (+0xbd = 0, RetireSelectionEngin); a group member not in state 14 is appended to the
        player's list (count < 0xff) with +0xbd = 1; the first member that is not type 10, belongs to the local
        player and is not of types 0xb..0x10 speaks: a type-7 unit in state 0xb/0xf stops its sound
        (PlaySnd_StopSound(+0x104, 0x16, 0)) and EnginAsk(unit, 0x16), any other EnginAsk(unit, 8, 0).
        Only EAX and EDX change."""
        m, sel = self.m, self.selecao()
        jogador, grupo = r['EAX'] & 0xff, r['EDX'] & 0xff
        eax, edx = r['EAX'], r['EDX']
        falou = False
        for u in range(0x320):
            rec = self._rec(u)
            if m.u8(rec + 2) in (0, 4):
                eax = 0
                continue
            eax = _b(self._pool(), m.u8(rec))
            if eax & 0xff != jogador:
                continue
            eax, edx = rec, self._pool()
            if m.u8(rec + 0xbd):
                m.u8(rec + 0xbd, 0)
                s = sel.retire_selection_engin(dict(r, EAX=u, EDX=m.u8(rec)))
                eax, edx = s['EAX'], s['EDX']
            eax, edx = u, (u * PASSO) & M32
            if m.u8(rec + 0xbc) != grupo:
                continue
            eax = m.u8(rec + 2)
            if eax == 0xe:
                continue
            base = jogador << 9
            eax = m.u16(SELECOES + base)
            if eax < 0xff:
                m.u16(SELECOES + base, eax + 1)
                m.u16(SELECOES + base + 2 * (eax + 1), u)
                eax = self._pool()
                m.u8(rec + 0xbd, 1)
            if falou:
                continue
            tipo = m.u8(rec + 1)
            eax = tipo
            if tipo == 0xa:
                continue
            eax = jogador
            if jogador != m.u8(JOGADOR_LOCAL):
                continue
            if tipo in TIPOS_LOOP:
                eax = 1
                continue
            falou = True
            regs = dict(r, EAX=u, EDX=8, EBX=0, ECX=u, ESI=r['ESI'])
            if tipo == 7 and m.u8(rec + 2) in (0xb, 0xf):
                parada = dict(regs, EAX=(rec + 0x104) & M32, EDX=0x16, EBX=0, ECX=u)
                if self.som is None:
                    raise DependenciaRamoCore('PlaySnd_StopSound', 0x4728e4, 'Audio sound-library provider required')
                parada['EAX'] = self.som('PlaySnd_StopSound', {k: parada[k] for k in ('EAX', 'EDX', 'EBX', 'ECX')},
                                         []) & M32
                regs = dict(parada, EAX=u)
            s = sel.engin_ask(regs)
            eax, edx = s['EAX'], s['EDX']
        return dict(r, EAX=eax & M32, EDX=edx & M32)

    def engin_get_centre_groupe(self, r):
        """EnginGetCentreGroupe 0x442139: AL player, CL group, EDX/EBX addresses of the u16 x/y results. Only the
        first live unit of that owner in the group counts (the original leaves the loop after it): its cell.
        Without one, the view rectangle's centre from the current words at EDX/EBX and the view size. EAX = the y
        result before truncation, EDX = its halving's sign, ECX = the low y bound, EBX = that unit (else the view
        height word); ESI/EDI/EBP preserved."""
        m = self.m
        jogador, grupo = r['EAX'] & 0xff, r['ECX'] & 0xff
        px, py = r['EDX'], r['EBX']
        minx, miny, maxx, maxy = 0xffff, 0xffff, 0, 0
        achado = None
        for u in range(0x320):
            rec = self._rec(u)
            if m.u8(rec + 2) in (0, 4) or m.u8(rec + 0xbc) != grupo or m.u8(rec) != jogador:
                continue
            achado = u
            celula = m.u16(rec + 8)
            minx = maxx = celula % 256
            miny = maxy = celula // 256
            break
        if achado is None:
            miny = m.u16(py)
            minx = _w(px, m.u16(px))
            maxx = (m.u16(VISTA_L) + minx - 1) & M32
            ebx = m.u16(VISTA_A)
            maxy = (miny + ebx - 1) & M32
        else:
            ebx = achado
        cx = minx & 0xffff
        eax, edx = _idiv2(((maxx & 0xffff) - cx) & M32)
        m.u16(px, (eax + cx) & 0xffff)
        ecx = miny & 0xffff
        eax, edx = _idiv2(((maxy & 0xffff) - ecx) & M32)
        eax = (eax + ecx) & M32
        m.u16(py, eax & 0xffff)
        return dict(r, EAX=eax, EBX=ebx, ECX=ecx, EDX=edx)

    # ------------------------------------------------------------ minimap view
    def _recentre(self, r):
        """MiniMapRecentre 0x46a01b body over the registers ``r`` (its EAX..EDI at entry); returns EAX."""
        m = self.m
        ebx, ecx, esi, edi = r['EBX'], r['ECX'], r['ESI'], r['EDI']
        margem = _s8(m.u8(MARGEM))
        for pos, vista, display in ((MINI_X, VISTA_L, MINI_L), (MINI_Y, VISTA_A, MINI_A)):
            edx = (margem << 5) & M32
            eax = m.u16(pos)
            if eax < _s32(edx):
                m.u16(pos, ((margem & 0xffff) << 5) & 0xffff)
                continue
            ebx = ((m.u16(vista) << 5) - _s32(edx)) & M32
            eax = (eax + m.u16(display) + 2) & M32
            if _s32(eax) > _s32(ebx):
                d = m.u16(display)
                if pos == MINI_X:
                    ebx = _w(ebx, d)
                    sub = ebx
                else:
                    ecx = _w(ecx, d)
                    sub = ecx
                v = ((m.u16(vista) << 5) - (((margem & 0xffff) << 5) & M32) - sub - 2) & M32
                m.u16(pos, v & 0xffff)
        eax = m.u16(MAPA_L)
        if m.u16(VISTA_X) + m.u16(VISTA_L) >= eax:
            esi = _w(esi, m.u16(VISTA_L))
            edi = _w(edi, m.u16(MAPA_L))
            eax = (m.u16(VISTA_X) + esi - edi) & M32
            m.u16(VISTA_X, (m.u16(VISTA_X) - eax) & 0xffff)
        eax = m.u16(MAPA_A)
        if m.u16(VISTA_Y) + m.u16(VISTA_A) >= eax:
            ebx = _w(ebx, m.u16(VISTA_A))
            ecx = _w(ecx, m.u16(MAPA_A))
            eax = (m.u16(VISTA_Y) + ebx - ecx) & M32
            esi = _w(esi, m.u16(VISTA_Y))
            m.u16(VISTA_Y, (esi - eax) & 0xffff)
        return eax

    def minimap_recentre(self, r):
        """MiniMapRecentre 0x46a01b: the minimap scroll words 0x507d68/6a kept within [margin * 32, view * 32 -
        margin * 32 - display - 2] (margin: the signed byte 0x508f90), then the view origin 0x508720/22 pulled
        back inside the map. Only EAX changes (its last computation, which reads the upper halves of the
        registers the routine loads words into)."""
        return dict(r, EAX=self._recentre(r))

    def minimap_set_pos(self, r):
        """MiniMapSetPos 0x46a19e: AX x, DX y. 0x507d68 = AX + 0x507d6c and 0x507d6a = DX + 0x507d6e, each 0 when
        negative as a signed word, then MiniMapRecentre. EAX = MiniMapRecentre's, EDX = DX + the lock word (32-bit;
        0 when the word is negative); others preserved."""
        m = self.m
        eax = _w(r['EAX'], r['EAX'] + m.u16(TRAVA_X))
        ecx = _w(r['ECX'], m.u16(TRAVA_Y))
        ebx = _s16(eax) & M32
        edx = (r['EDX'] + ecx) & M32
        if _s32(ebx) < 0:
            eax = 0
        m.u16(MINI_X, eax & 0xffff)
        if _s16(edx) < 0:
            edx = 0
        m.u16(MINI_Y, edx & 0xffff)
        return dict(r, EAX=self._recentre(dict(r, EAX=eax, EBX=ebx, ECX=ecx, EDX=edx)), EDX=edx)

    # ------------------------------------------------------------ recruitment exit position
    def _calcul_position(self, r):
        """CalculPosition 0x420698 body: the full EAX (``posicao_saida`` gives its AX)."""
        m = self.m
        e = self._est(r['EAX'])
        tipo = m.u8(e + 8)
        if tipo > 0x15 or GEOMETRIA_POR_TIPO[tipo] is None:
            return 0
        ramo = GEOMETRIA_POR_TIPO[tipo]
        dx, dy, alto = GEOMETRIA[ramo]
        largura, altura = self._tamanho(tipo)
        superior = {'0': 0, 'ESI': r['ESI'], 'EDI': r['EDI'], 'h-4': altura - 4, 'w-1': largura - 1}[alto]
        base = _w(superior & M32, m.u16(e + 2))
        ajuste = CORRECAO_POR_TIPO[tipo] - REPOSICAO.get(ramo, 0x102)
        return (base + ((altura - dy) << 8) + largura - dx - ajuste) & M32

    def calcul_position(self, r):
        """CalculPosition 0x420698: AX structure (BL unused). EAX = the exit cell (AX as ``posicao_saida``; bits
        16+ from the 32-bit arithmetic over the origin word loaded into a register that keeps its upper half);
        types 9, 12, 17 and above 0x15 give 0. Every other register preserved."""
        return dict(r, EAX=self._calcul_position(r))

    def recherche_decalage_sortie(self, r):
        """RechercheDecalageSortie 0x41d1d0: AX structure. The first cell of the 8 around CalculPosition's AX
        (rows then columns; row and column 0..255) whose attribute bit 0 is clear (TerrainEnCollision mask 1),
        else CalculPosition's EAX. Only EAX changes; with a free neighbour its bits 16+ are uncertain (stack
        residue)."""
        from incursao_core import terreno_em_colisao
        m = self.m
        tipo = m.u8(self._est(r['EAX']) + 8)
        if tipo > 0x15 or tipo in (9, 0xc, 0x11):
            raise ForaDoDominioVisao('RechercheDecalageSortie', 0x41d23d, f'structure type {tipo} (uninitialized '
                                                                         'locals)')
        cp = self._calcul_position(dict(r, EAX=r['EAX'] & 0xffff))
        celula = cp & 0xffff
        x, y = celula % 256, celula // 256
        for dy in (-1, 0, 1):
            if not 0 <= y + dy < 256:
                continue
            for dx in (-1, 0, 1):
                if not 0 <= x + dx < 256 or (dx == 0 and dy == 0):
                    continue
                alvo = (celula + dy * 256 + dx) & 0xffff
                if not terreno_em_colisao(m, alvo, 1)['EAX'] & 0xff:
                    return dict(r, EAX=alvo, _incertos={'EAX': 0xffff0000})
        return dict(r, EAX=cp)


# ------------------------------------------------------------ adapters for ai-runtime and Economy
def provedores_visao(memoria, som=None):
    """ai-runtime's keyword-shaped original-name providers over one live memory: the structure loop's
    ``BatimentIllumine(sitio, estrutura, jogador, ebx)`` and ``BatimentDecouvre(sitio, estrutura, jogador)``
    (``laco_despachantes``), InputGame's ``MiniMapSetPos(sitio, x, y)`` (EAX/EDX = the signed cursor words, EBX = 0,
    ECX = 1 as at 0x42bb45..0x42bb5b) and WndProc's ``MiniMapRecentre(sitio)``. Each returns the routine's exit
    registers (dict EAX..EBP, plus ``_incertos`` when present). Registers a call site does not determine (ESI/EDI
    here, ECX/ESI/EDI/EBP in the structure loop) enter as 0; they reach only MiniMapRecentre's EAX, which both
    callers discard. The register-shaped routines (SauveSelectionGroupe, RestaureSelectionGroupe,
    EnginGetCentreGroupe, every name above) are ``VisaoGrupos(memoria, som=som).chamar(nome, regs)``, the shape
    of ``SelecaoOrdens.chamar`` that ``provedores_entrada_ia`` already binds."""
    v = VisaoGrupos(memoria, som=som)
    zero = dict.fromkeys(REG7, 0)

    def chamar(nome, **regs):
        return v.chamar(nome, dict(zero, **{k: x & M32 for k, x in regs.items()}))
    return {
        'BatimentIllumine': lambda sitio, estrutura, jogador, ebx: chamar('BatimentIllumine', EAX=estrutura,
                                                                         EDX=jogador, EBX=ebx),
        'BatimentDecouvre': lambda sitio, estrutura, jogador: chamar('BatimentDecouvre', EAX=estrutura, EDX=jogador),
        'MiniMapSetPos': lambda sitio, x, y: chamar('MiniMapSetPos', EAX=x, EDX=y, EBX=0, ECX=1),
        'MiniMapRecentre': lambda sitio: chamar('MiniMapRecentre'),
    }


def provedor_saida(visao, outros=None):
    """Economy's ``externo(nome, chamada, registradores)`` for CalculPosition and RechercheDecalageSortie (the shape of
    ``entrada_estruturas.provedor_entrada``): a missing register enters as 0 with a full uncertain mask, carried to
    the output when the callee leaves it unchanged. Other names go to ``outros`` or raise ``DependenciaRamoCore``."""
    def externo(nome, chamada, regs):
        if nome not in ('CalculPosition', 'RechercheDecalageSortie'):
            if outros is None:
                raise DependenciaRamoCore(nome, chamada, 'not an exit-position routine and no other provider')
            return outros(nome, chamada, regs)
        incertos_in = dict(regs.get('_incertos') or {})
        entrada = {}
        for k in REG7:
            if k in regs:
                entrada[k] = regs[k] & M32
            else:
                entrada[k] = 0
                incertos_in[k] = M32
        saida = visao.chamar(nome, entrada)
        resultado = {k: saida[k] for k in REG7}
        incertos = {k: v for k, v in incertos_in.items() if saida[k] == entrada[k] and v}
        for k, v in (saida.get('_incertos') or {}).items():
            incertos[k] = incertos.get(k, 0) | v
        if 'ESI' in incertos_in or 'EDI' in incertos_in:      # CalculPosition may take EAX's upper half from them
            incertos['EAX'] = incertos.get('EAX', 0) | 0xffff0000
        if incertos:
            resultado['_incertos'] = incertos
        return resultado
    return externo


def escolher_saida(memoria):
    """Economy's ``Recrutamento.iniciar(escolher_saida=...)`` callback: structure index -> RechercheDecalageSortie's
    u16 cell (the AX the suffix 0x428640 stores in +0x7c)."""
    v = VisaoGrupos(memoria)
    zero = dict.fromkeys(REG7, 0)
    return lambda indice: v.chamar('RechercheDecalageSortie', dict(zero, EAX=indice & 0xffff))['EAX'] & 0xffff
