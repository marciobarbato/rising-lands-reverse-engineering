"""Player selection and order-setter routines over live original memory (M3 groundwork).

Translated from the intact bytes (``evidencias/selecao-ordens/*.asm``) after the native
capture ``evidencias/selecao-ordens/captura-selecao-ordens-exibicao.json``. Every routine
takes its argument registers and returns the general registers it leaves (EAX..EBP, the
callee-saved ones included unchanged), so callers that read clobbered registers see the
original values. Arithmetic flags are not modeled.

``memoria`` is the flat interface of ``memoria_quadro_core.MemoriaQuadro`` (``u8/u16/u32``
plus ``vista``): ResetOrdre and SetDeplaceEngin run through Core's navigation world bound
live to it (``mundo_vivo``), as validated in M2.3.

Named dependencies (never defaulted; a path that reaches one without its provider raises
``DependenciaRamoCore`` at the original call, after the stores the original made before it):
- ``som(nome, registradores, pilha) -> EAX``: the sound-library boundary (Audio).
  ``PlaySnd_PostSound 0x48aa79`` receives EAX = request opcode (0x50 unit voice, 0x42
  structure), EDX = sound code, EBX = address of the handle field, ECX = flag and one pushed
  word, the volume (``pilha``). ``PlaySnd_StopSound 0x48aac0`` receives EAX = handle-field
  address, EDX = sound code, EBX, ECX. The returned EAX is what the caller then holds; the
  accepted frame bench declares it unchanged (the library is never initialized).
- ``definir_ataque(unidade, modo, referencia) -> {'EAX': .., 'EDX': ..}``: SetAttaqueEngin
  0x445a36 (Combat). It performs the order stores (including its own ResetOrdre) and returns
  the two registers it leaves; EBX, ECX, ESI, EDI and EBP are preserved by the original.
"""
from chamadas_quadro_core import DependenciaRamoCore, terreno_esta_descoberto
from movimento import distancia_quadratica

M32 = 0xffffffff
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
SELECOES = 0x508728                 # per player: u16 count, u16 units from +2; stride 0x200
ESTRUTURAS = 0x49a0c8
SELECAO_ESTRUTURAS = 0x495be0       # u16 per player
JOGADOR_LOCAL = 0x508041
CONTADOR = 0x508f7c                 # u32 cycle counter
JANELA = 0x508720                   # u16 view x, y, width, height
DIMENSOES_ESTRUTURA = 0x495d8c      # u16 width, +2 height; stride 52 per structure type
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
# Deselection 0x429180 UI stores
MODO_ACAO, INFO_SELECAO, ZONA_INFO, ZONA_INFO_BYTE, REDESENHAR = 0x496207, 0x4e19b0, 0x4e05ae, 0x4e05ab, 0x496d48
# BatimentGetDecalageConstruction 0x41aea4, jump table 0x41ae4c by structure type 0..0x15
DECALAGEM = (0x201, 0x300, 0x101, 0x202, 0x100, 0x202, 0x100, 0x300, 0x202, 0x100, 0, 0, 0x100, 0x200,
             0x300, 0x100, 0x100, 1, 0x201, 0x100, 0x100, 0x100)
QUATRO_CELULAS = frozenset((3, 11, 12, 13, 14, 15, 16, 25))   # EnginInZone jump table 0x44618c
NAO_TROPAS = frozenset((3, 11, 12, 13, 14, 15, 16, 17, 25))   # BagContientTroupe 0x44728f..0x4472c1
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
ROTINAS = {
    'SelectionEngin': 0x4742dc, 'EnginAddSelection': 0x4741cd, 'EnginSelectionnable': 0x474169,
    'SelectionAddEngin': 0x4725ee, 'RetireSelectionEngin': 0x472576, 'DeselectionEngin': 0x472648,
    'DeSelectionGroupe': 0x47268b, 'Deselection': 0x429180, 'EnginInZone': 0x4461f4,
    'BatimentSelection': 0x41b673, 'BatimentDeselectionner': 0x41b663,
    'SetDeplaceEnginSelect': 0x473e6e, 'SetAttaqueEnginSelect': 0x473dbf,
    'SetConstruitBatimentSelect': 0x473a07, 'SetEnginConstruitBatiment': 0x4454ce,
    'SetRecolteEnginSelect': 0x473290, 'SetRecolteEngin': 0x444ebd,
    'SetTransporteEnginSelect': 0x473212, 'SetTransporteEngin': 0x444e7f,
    'SetDeplaceEngin': 0x4457d3, 'ResetOrdre': 0x44357c, 'EnginAsk': 0x440d5e,
}


def _baixo(r, nome, v):
    """Replace the low byte of register ``nome``."""
    r[nome] = (r[nome] & 0xffffff00) | (v & 0xff)


def _idiv256(v):
    """Watcom ``cdq``-style signed idiv by 0x100 of a 32-bit value: (quotient, remainder) as u32."""
    v &= M32
    s = v - (1 << 32) if v & 0x80000000 else v
    q = abs(s) // 256 * (1 if s >= 0 else -1)
    return q & M32, (s - q * 256) & M32


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


class SelecaoOrdens:
    """The routines over one live memory; providers are explicit (see the module docstring)."""

    def __init__(self, memoria, *, som=None, definir_ataque=None):
        self.m = memoria
        self.som, self.definir_ataque = som, definir_ataque
        self._mundo = None

    # ------------------------------------------------------------ memory helpers
    def _pool(self):
        return self.m.u32(PONTEIRO_UNIDADES)

    def _rec(self, u):
        return (self._pool() + (u & 0xffff) * PASSO) & M32

    def _mundo_vivo(self):
        if self._mundo is None:
            from mundo_vivo import mundo_vivo
            self._mundo = mundo_vivo(self.m)        # no path search is reached by these setters
        return self._mundo

    def _fronteira(self, nome, endereco, r, pilha=()):
        if self.som is None:
            raise DependenciaRamoCore(nome, endereco, 'Audio sound-library provider required')
        r['EAX'] = self.som(nome, {k: r[k] for k in ('EAX', 'EDX', 'EBX', 'ECX')}, list(pilha)) & M32

    # ------------------------------------------------------------ small callees (exact registers)
    def _vivo(self, r):
        """EnginEstVivant 0x443dad: EAX = 0/1 (state not 0/4); EDX kept."""
        r['EAX'] = int(self.m.u8(self._rec(r['EAX']) + 2) not in (0, 4))

    def _byte_unidade(self, r, campo):
        """EnginGetPlayer/EnginGetType/EnginVisible/EnginGetEtat: AL = unit byte over the pool pointer."""
        p = self._pool()
        r['EAX'] = (p & 0xffffff00) | self.m.u8((p + (r['EAX'] & 0xffff) * PASSO + campo) & M32)

    def _dono(self, r):
        self._byte_unidade(r, 0)

    def _tipo(self, r):
        self._byte_unidade(r, 1)

    def _visivel(self, r):
        self._byte_unidade(r, 0x72)

    def _etat(self, r):
        self._byte_unidade(r, 2)

    @staticmethod
    def _faixa(r, base, limite):
        """TypeEnginEstEnLoop (0xb, 5) / TypeEnginEstVehicule (0xb, 4): AL - base <= limite gives EAX 1."""
        t = (r['EAX'] - base) & 0xff
        r['EAX'] = 1 if t <= limite else r['EAX'] & 0xffffff00

    @staticmethod
    def _aereo(r):
        """TypeEnginEstAerien 0x4422cf: AL 0x10/0x11 -> AL 1 (EAX upper bytes kept)."""
        _baixo(r, 'EAX', int(0x10 <= r['EAX'] & 0xff <= 0x11))

    def _volume_unidade(self, u):
        """EnginGetVolume 0x440c5d: EAX = volume; every other register preserved."""
        celula = self.m.u16(self._rec(u) + 8)
        x, y = celula % 256, celula // 256
        cx = (self.m.u16(JANELA + 4) >> 1) + self.m.u16(JANELA)
        cy = (self.m.u16(JANELA + 6) >> 1) + self.m.u16(JANELA + 2)
        d = _s32(distancia_quadratica(cx, cy, x, y))
        v = 0x100 if d <= 0x91 else 0xb4 if d <= 0x12c else 0x64 if d < 0x258 else 0
        rec = self._rec(u)
        if not (self.m.u8(rec + 0xbd) != 0 and self.m.u8(rec) == self.m.u8(JOGADOR_LOCAL)):
            v >>= 1
        return v

    def _volume_estrutura(self, s):
        """BatimentGetVolume 0x41a0ab: EAX = volume from the structure cell; no selection halving."""
        celula = self.m.u16(ESTRUTURAS + (s & 0xffff) * PASSO + 2)
        x, y = celula % 256, celula // 256
        cx = (self.m.u16(JANELA + 4) >> 1) + self.m.u16(JANELA)
        cy = (self.m.u16(JANELA + 6) >> 1) + self.m.u16(JANELA + 2)
        d = _s32(distancia_quadratica(cx, cy, x, y))
        return 0x100 if d <= 0x91 else 0xb4 if d <= 0x12c else 0x64 if d < 0x258 else 0

    # ------------------------------------------------------------ voice
    def engin_ask(self, regs):
        """EnginAsk 0x440d5e: AX unit, DX mode, BL flag. Discovered cell -> volume; +0xf9 = flag; a free handle
        (+0x104 = -1) posts the voice request to the sound library."""
        r = dict(regs)
        u, modo, flag = r['EAX'] & 0xffff, r['EDX'] & 0xffff, r['EBX'] & 0xff
        rec = self._rec(u)
        r['EBX'] = rec
        celula = self.m.u16(rec + 8)
        d = terreno_esta_descoberto(self.m, celula, self.m.u8(JOGADOR_LOCAL))
        r['EAX'], r['EDX'] = d['EAX'], d['EDX']
        if not r['EAX'] & 0xff:
            return r
        volume = self._volume_unidade(u)
        r['EDX'] = modo
        if modo == 0x10:
            volume = 0x100
        r['EAX'] = volume
        handle = self.m.u32(rec + 0x104)
        r['EDX'] = handle
        self.m.u8(rec + 0xf9, flag)
        if handle != M32:
            return r
        r.update(EAX=0x50, EDX=(self.m.u8(rec + 1) << 16) | (modo << 8), EBX=(rec + 0x104) & M32, ECX=flag)
        self._fronteira('PlaySnd_PostSound', 0x440de7, r, [volume])
        r['ECX'] = regs['ECX']
        return r

    # ------------------------------------------------------------ unit selection
    def engin_selectionnable(self, regs):
        """EnginSelectionnable 0x474169: AL = alive-for-selection (state != 14, the type-16 state-13 rule,
        visible +0x72); only EAX changes."""
        u = regs['EAX'] & 0xffff
        rec = self._rec(u)
        r = dict(regs, EAX=rec)
        self._selecionavel_registro(r, u, rec, self.m.u8(rec + 2))
        return dict(regs, EAX=r['EAX'])

    def engin_add_selection(self, regs):
        """EnginAddSelection 0x4741cd: AX unit, DL player. Appends a live selectable unoccupied unit of
        that owner (count < 0xff) and sets +0xbd. EAX and EDX change."""
        r = dict(regs)
        u, jogador = regs['EAX'] & 0xffff, regs['EDX'] & 0xff
        r['EDX'] = u
        r['EAX'] = u
        self._vivo(r)
        if not r['EAX'] & 0xff:
            return r
        rec = self._rec(u)
        estado = self.m.u8(rec + 2)
        r['EAX'], r['EDX'] = rec, estado
        if not self._selecionavel_registro(r, u, rec, estado):
            return r
        r['EDX'] = u
        r['EAX'] = u
        self._dono(r)
        if r['EAX'] & 0xff != jogador:
            return r
        r['EAX'], r['EDX'] = u * PASSO, rec
        if self.m.u8(rec + 0xbd):
            return r
        base = jogador << 9
        n = self.m.u16(SELECOES + base)
        if n >= 0xff:
            r['EAX'] = base
            return r
        self.m.u16(SELECOES + base, n + 1)
        self.m.u16(SELECOES + base + (n + 1) * 2, u)
        self.m.u8(rec + 0xbd, 1)
        self.m.u8(rec + 0xbd, 1)
        r['EAX'], r['EDX'] = u * 69, self._pool()
        return r

    def _selecionavel_registro(self, r, u, rec, estado):
        """The selectability test of EnginAddSelection/SelectionEngin with EAX = record on entry."""
        if estado == 0xe:
            r['EAX'] &= 0xffffff00
            return False
        if self.m.u8(rec + 1) == 0x10 and estado == 0xd and self.m.u8(rec + 0xab) != 0x32:
            r['EAX'] = 0
            return False
        r['EAX'] = u
        self._visivel(r)
        ok = bool(r['EAX'] & 0xff)
        _baixo(r, 'EAX', int(ok))
        return ok

    def selection_add_engin(self, regs):
        """SelectionAddEngin 0x4725ee: AX unit, DL player; unconditional append (count < 0xff), +0xbd = 1."""
        r = dict(regs)
        u, base = regs['EAX'] & 0xffff, (regs['EDX'] & 0xff) << 9
        n = self.m.u16(SELECOES + base)
        if n >= 0xff:
            r['EAX'], r['EDX'] = base, n
            return r
        self.m.u16(SELECOES + base, n + 1)
        self.m.u16(SELECOES + base + (n + 1) * 2, u)
        self.m.u8(self._rec(u) + 0xbd, 1)
        r['EAX'], r['EDX'] = (self._pool() & 0xffffff00) | 1, u * PASSO
        return r

    def retire_selection_engin(self, regs):
        """RetireSelectionEngin 0x472576: AX unit, DL player. Clears the unit's +0xbd at each slot before the
        match, removes the first match by shifting the tail and decrements the count. EAX and EDX change."""
        r = dict(regs)
        u = regs['EAX'] & 0xffff
        base = (regs['EDX'] & 0xff) << 9
        lista = SELECOES + base
        n = self.m.u16(lista)
        r['EDX'] = base
        achou = False
        i = 1
        while i <= n:
            if not achou:
                if self.m.u16(lista + 2 * i) == u:
                    achou = True
                self.m.u8(self._rec(u) + 0xbd, 0)
                r['EDX'] = self._pool()
            else:
                self.m.u16(lista + 2 * i - 2, self.m.u16(lista + 2 * i))
                r['EDX'] = i
            i += 1
        if achou:
            self.m.u16(lista, self.m.u16(lista) - 1)
        r['EAX'] = i
        return r

    def deselection_engin(self, regs):
        """DeselectionEngin 0x472648: AX unit. A unit with +0xbd set is cleared and removed from its
        owner's list. Only EAX changes."""
        u = regs['EAX'] & 0xffff
        rec = self._rec(u)
        if not self.m.u8(rec + 0xbd):
            return dict(regs, EAX=rec)
        self.m.u8(rec + 0xbd, 0)
        dono = self.m.u8(rec)
        r = self.retire_selection_engin(dict(regs, EAX=u, EDX=dono))
        return dict(regs, EAX=r['EAX'])

    def deselection_groupe(self, regs):
        """DeSelectionGroupe 0x47268b: AL player. Every live unit of that owner with +0xbd set is cleared and
        removed. Only EAX changes."""
        jogador = regs['EAX'] & 0xff
        eax = regs['EAX']
        for u in range(800):
            r = dict(EAX=u)
            self._vivo(r)
            eax = r['EAX']
            if not eax & 0xff:
                continue
            rec = self._rec(u)
            eax = rec
            if not self.m.u8(rec + 0xbd) or self.m.u8(rec) != jogador:
                continue
            self.m.u8(rec + 0xbd, 0)
            eax = self.retire_selection_engin(dict(regs, EAX=u, EDX=self.m.u8(rec)))['EAX']
        return dict(regs, EAX=eax)

    def batiment_deselectionner(self, regs):
        """BatimentDeselectionner 0x41b663: AL player; structure selection word = 0xffff; EAX = AL."""
        jogador = regs['EAX'] & 0xff
        self.m.u16(SELECAO_ESTRUTURAS + 2 * jogador, 0xffff)
        return dict(regs, EAX=jogador)

    def deselection(self, regs):
        """Deselection 0x429180: AL player. DeSelectionGroupe, BatimentDeselectionner, then the action-mode
        byte 0x496207 = 0xff, 0x4e19b0 = 0, u16 0x4e05ae = 0, 0x4e05ab = 0, redraw flag 0x496d48 = 1."""
        jogador = regs['EAX'] & 0xff
        self.deselection_groupe(dict(regs, EAX=jogador))
        r = self.batiment_deselectionner(dict(regs, EAX=jogador))
        self.m.u8(MODO_ACAO, 0xff)
        self.m.u8(INFO_SELECAO, 0)
        self.m.u16(ZONA_INFO, 0)
        self.m.u8(ZONA_INFO_BYTE, 0)
        self.m.u8(REDESENHAR, 1)
        return dict(regs, EAX=r['EAX'] & 0xffff00ff)

    def engin_in_zone(self, regs, y2):
        """EnginInZone 0x4461f4: AX unit, DX x1, BX y1, CX x2, pushed y2 (RET 4). AL = the unit cell (or, for the
        four-cell types, any of cell, cell-1, cell-0x101, cell-0x100) inside [x1..x2] x [y1..y2], unsigned 16-bit
        compares on the signed-idiv coordinates. EAX, EBX, ECX and EDX change."""
        r = dict(regs)
        u = regs['EAX'] & 0xffff
        x1, y1, x2, y2 = regs['EDX'] & 0xffff, regs['EBX'] & 0xffff, regs['ECX'] & 0xffff, y2 & 0xffff
        p = self._pool()
        tipo = self.m.u8((p + u * PASSO + 1) & M32)
        cl = 0
        r['EBX'], r['EDX'] = u, p
        if tipo > 0x19:
            r['EAX'] = (u * 69) & 0xffffff00
            r['ECX'] = regs['ECX'] & 0xffffff00
            return r
        celula = self.m.u16((p + u * PASSO + 8) & M32)

        def dentro(valor):
            q, resto = _idiv256(valor)
            x, y = resto & 0xffff, q & 0xffff
            return x1 <= x <= x2 and y1 <= y <= y2
        if tipo in QUATRO_CELULAS:
            for d in (0, 1, 0x101):
                if dentro(celula - d):
                    cl = 1
            ultimo = (celula - 0x100) & M32
        else:
            ultimo = celula
        if dentro(ultimo):
            cl = 1
        negativo = bool(ultimo & 0x80000000)
        y = ((_s32(ultimo) + (255 if negativo else 0)) >> 8) & M32
        r['EAX'] = (y & 0xffffff00) | cl
        r['EBX'] = ultimo
        r['EDX'] = 0xffffff00 if negativo else 0
        r['ECX'] = (regs['ECX'] & 0xffffff00) | cl
        return r

    def selection_engin(self, regs):
        """SelectionEngin 0x4742dc: AL player, DX corner A, BX corner B (cells). For every live selectable unit
        of the player: clear its selection, then select it again if it lies in the rectangle (corners
        ordered with SwapWORD). The first selected local-player unit whose type is not 10 nor 11..16 speaks:
        a type-7 builder in state 11/15 stops its sound (code 0x16) and asks mode 0x16, every other unit asks
        mode 8. ECX, ESI, EDI, EBP are preserved."""
        r = dict(regs)
        jogador = regs['EAX'] & 0xff
        a, b = regs['EDX'] & 0xffff, regs['EBX'] & 0xffff
        xa, ya, xb, yb = a % 256, a // 256, b % 256, b // 256
        if xb < xa:
            xa, xb = xb, xa
        if ya > yb:
            ya, yb = yb, ya
        falou = 0
        r['EBX'] = b
        for u in range(800):
            r['EDX'] = u
            r['EAX'] = u
            self._vivo(r)
            if not r['EAX'] & 0xff:
                continue
            rec = self._rec(u)
            r['EDX'] = rec
            estado = self.m.u8(rec + 2)
            r['EAX'] = estado
            if estado == 0xe:
                r['EAX'] = 0
                continue
            r['EBX'] = self.m.u8(rec + 1)
            if r['EBX'] == 0x10 and estado == 0xd:
                ab = self.m.u8(rec + 0xab)
                if ab != 0x32:
                    r['EAX'] = 0
                    continue
            r['EAX'] = u
            self._visivel(r)
            if not r['EAX'] & 0xff:
                continue
            _baixo(r, 'EAX', 1)
            r['EBX'] = u
            r['EAX'] = u
            self._dono(r)
            if r['EAX'] & 0xff != jogador:
                continue
            r['EDX'] = rec
            if self.m.u8(rec + 0xbd):
                self.m.u8(rec + 0xbd, 0)
                saida = self.retire_selection_engin(dict(r, EAX=u, EDX=self.m.u8(rec)))
                r['EAX'], r['EDX'] = saida['EAX'], saida['EDX']
            zona = self.engin_in_zone(dict(r, EAX=u, EDX=xa, EBX=ya, ECX=xb), yb)
            r.update(EAX=zona['EAX'], EBX=zona['EBX'], ECX=zona['ECX'], EDX=zona['EDX'])
            if not r['EAX'] & 0xff:
                continue
            _baixo(r, 'EAX', jogador)
            self._adicionar_na_selecao(r, u, jogador)
            # 0x4744d5: the voice of the first eligible unit
            r['EAX'] = falou & 0xffff
            if falou >= 1:
                continue
            r['EDX'] = u
            r['EAX'] = u
            self._tipo(r)
            r['EAX'] &= 0xff
            if r['EAX'] == 0xa:
                continue
            _baixo(r, 'EAX', jogador)
            if jogador != self.m.u8(JOGADOR_LOCAL):
                continue
            r['EAX'] = u
            self._tipo(r)
            r['EAX'] &= 0xff
            self._faixa(r, 0xb, 5)
            if r['EAX'] & 0xff:
                continue
            falou += 1
            r['EAX'] = u
            self._tipo(r)
            r['EAX'] &= 0xff
            if r['EAX'] == 7:
                r['EAX'] = u
                self._etat(r)
                r['EAX'] &= 0xff
                if r['EAX'] != 0xb:
                    r['EAX'] = u
                    self._etat(r)
                    r['EAX'] &= 0xff
                if r['EAX'] in (0xb, 0xf):
                    r.update(EAX=(rec + 0x104) & M32, EBX=0, EDX=0x16)
                    self._fronteira('PlaySnd_StopSound', 0x474582, r)
                    saida = self.engin_ask(dict(r, EAX=u))
                    r.update(EAX=saida['EAX'], EBX=saida['EBX'], EDX=saida['EDX'])
                    continue
            r.update(EDX=8, EAX=u, EBX=0)
            saida = self.engin_ask(r)
            r.update(EAX=saida['EAX'], EBX=saida['EBX'], EDX=saida['EDX'])
        r['EDX'] = 0x320
        return dict(regs, EAX=r['EAX'], EBX=r['EBX'], EDX=r['EDX'])

    def _adicionar_na_selecao(self, r, u, jogador):
        """SelectionEngin 0x4743e3..0x4744d5: the inlined EnginAddSelection on unit ``u``."""
        r['ECX'] = u
        r['EAX'] = u
        self._vivo(r)
        if not r['EAX'] & 0xff:
            return
        rec = self._rec(u)
        r['EDX'] = rec
        estado = self.m.u8(rec + 2)
        r['EAX'] = estado
        r['EBX'] = u
        if estado == 0xe:
            r['EAX'] = 0
            return
        if self.m.u8(rec + 1) == 0x10 and estado == 0xd and self.m.u8(rec + 0xab) != 0x32:
            r['EAX'] = 0
            return
        r['EAX'] = u
        self._visivel(r)
        if not r['EAX'] & 0xff:
            _baixo(r, 'EAX', 0)
            return
        _baixo(r, 'EAX', 1)
        r['EDX'] = u
        r['EAX'] = u
        self._dono(r)
        r['EAX'] = (r['EAX'] & 0xffff00ff) | (jogador << 8)
        if r['EAX'] & 0xff != jogador:
            return
        r['EDX'] = u * PASSO
        r['EBX'] = rec
        if self.m.u8(rec + 0xbd):
            return
        base = jogador << 9
        r['EDX'] = base
        n = self.m.u16(SELECOES + base)
        r['EAX'] = n
        if n >= 0xff:
            r['EAX'] = n & 0xffffff00
            return
        self.m.u16(SELECOES + base, n + 1)
        self.m.u16(SELECOES + base + (n + 1) * 2, u)
        self.m.u8(rec + 0xbd, 1)
        self.m.u8(rec + 0xbd, 1)
        r['EAX'], r['EDX'] = u * PASSO, self._pool()

    # ------------------------------------------------------------ structure selection
    def _bag_contient_troupe(self, bag, eax):
        """BagContientTroupe 0x44724a: EAX = Bag at ``bag``; AL = a tag-1 slot holds a troop type. Exact EAX."""
        n = self.m.u16(bag + 2)
        for i in range(n):
            eax = self.m.u8(bag + 0x42 + i)
            if eax != 1:
                continue
            unidade = self.m.u16(bag + 6 + 2 * i)
            tipo = self.m.u8(self._rec(unidade) + 1)
            eax = ((unidade * PASSO) & 0xffff0000) | tipo
            if tipo not in NAO_TROPAS:
                return ((unidade * PASSO) & 0xffff0000) | 0x101
        return eax & 0xffffff00

    def _bag_contient(self, bag, modo, alvo):
        """BagContient 0x4471b8 for mode 1 only: EAX = count of tag-1 slots whose unit type is ``alvo``."""
        if modo != 1:
            raise DependenciaRamoCore('BagContient', 0x447238, f'mode {modo} is outside the captured domain')
        conta = 0
        for i in range(self.m.u16(bag + 2)):
            if self.m.u8(bag + 0x42 + i) == 1 and self.m.u8(self._rec(self.m.u16(bag + 6 + 2 * i)) + 1) == alvo & 0xffff:
                conta += 1
        return conta

    def batiment_selection(self, regs):
        """BatimentSelection 0x41b673: AX structure. Type 12 selects directly; otherwise an active (+5) structure
        is selected when its Bag holds a troop (types 2/21) or, types other than 21, a type-9 unit. A local
        player's selection with a free sound handle (+0x100 = -1) posts sound 0x42. Only EAX changes."""
        s = regs['EAX'] & 0xffff
        e = (ESTRUTURAS + s * PASSO) & M32
        tipo = self.m.u8(e + 8)
        if tipo == 0xc:
            dono = self.m.u8(e + 4)
            self.m.u16(SELECAO_ESTRUTURAS + 2 * dono, s)
            return dict(regs, EAX=dono)
        if not self.m.u8(e + 5):
            return dict(regs, EAX=0)
        bag = e + 0xc
        if tipo in (0x15, 2):
            eax = self._bag_contient_troupe(bag, bag)
            ok = bool(eax & 0xff)
            if not ok and tipo == 0x15:
                return dict(regs, EAX=eax & 0xffffff00)
        else:
            ok = False
        if not ok and tipo != 0x15:
            eax = self._bag_contient(bag, 1, 9)
            ok = bool(eax & 0xffff)
            if not ok:
                return dict(regs, EAX=eax & 0xffffff00)
        dono = self.m.u8(e + 4)
        self.m.u16(SELECAO_ESTRUTURAS + 2 * dono, s)
        eax = ((s * PASSO) & 0xffffff00) | dono
        if dono != self.m.u8(JOGADOR_LOCAL):
            return dict(regs, EAX=eax)
        volume = self._volume_estrutura(s)
        if self.m.u32(e + 0x100) != M32:
            return dict(regs, EAX=volume)
        r = dict(regs, EAX=0x42, EDX=(tipo << 16) | 0x800, EBX=(e + 0x100) & M32, ECX=0)
        self._fronteira('PlaySnd_PostSound', 0x41b785, r, [volume])
        return dict(regs, EAX=r['EAX'])

    # ------------------------------------------------------------ single-unit order setters
    def reset_ordre(self, regs):
        """ResetOrdre 0x44357c (Core, M2.3): only EAX changes, to the unit record address."""
        u = regs['EAX'] & 0xffff
        self._mundo_vivo().redefinir_ordem(u)
        return dict(regs, EAX=self._rec(u))

    def set_deplace_engin(self, regs):
        """SetDeplaceEngin 0x4457d3 (Core, M2.3): AX unit, DX cell; EAX = EDX = the unit record address."""
        u = regs['EAX'] & 0xffff
        self._mundo_vivo().definir_movimento(u, regs['EDX'] & 0xffff)
        rec = self._rec(u)
        return dict(regs, EAX=rec, EDX=rec)

    def _liberar_busca(self, u, r):
        """The inlined search-context release when unit ``u`` owns it (0x496304)."""
        if u == self.m.u16(BUSCA_UNIDADE):
            self.m.u8(BUSCA_OCUPADA, 0)
            self.m.u8(BUSCA_SUCESSO, 0)
            self.m.u16(BUSCA_UNIDADE, 0xffff)
            self.m.u32(BUSCA_ROTA, 0)
            return True
        return False

    def set_engin_construit_batiment(self, regs):
        """SetEnginConstruitBatiment 0x4454ce: AX unit, DL structure type, BX cell. A unit already building
        (state 11) a gate (+0xbe = 9) queues the cell (+0xc4, count +0xd8 < 10). Otherwise ResetOrdre, the cell
        is moved to the footprint origin (types other than 9/12: + ((h - h/2) << 8) - 0x100 + (w - w/2) - 1 -
        BatimentGetDecalageConstruction), +0x7e = cell, search released, +0x88 = +0x89 = 0, +0xc0 = 0xffff,
        +0xbe = type, state 11, +0xb2 = cell, and a gate clears +0xd8. EAX, EBX, EDX change."""
        r = dict(regs)
        u, tipo = regs['EAX'] & 0xffff, regs['EDX'] & 0xff
        celula = regs['EBX']
        rec = self._rec(u)
        largura = self.m.u16(DIMENSOES_ESTRUTURA + 52 * tipo)
        altura = self.m.u16(DIMENSOES_ESTRUTURA + 52 * tipo + 2)
        if self.m.u8(rec + 2) == 0xb and self.m.u8(rec + 0xbe) == 9:
            n = self.m.u16(rec + 0xd8)
            r['EAX'], r['EDX'], r['EBX'] = rec, n, largura
            if n >= 0xa:
                return r
            self.m.u16(rec + 0xd8, n + 1)
            self.m.u16(rec + 0xc4 + 2 * n, celula)
            r['EBX'] = n + 1
            return r
        self.reset_ordre(dict(EAX=u))
        if tipo not in (9, 0xc):
            celula = (celula + ((altura - (altura >> 1)) << 8) - 0x100 + (largura - (largura >> 1)) - 1) & M32
            celula = (celula - (DECALAGEM[tipo] if tipo <= 0x15 else 0)) & M32
        self.m.u16(rec + 0x7e, celula)
        r['EBX'], r['EDX'] = u, u * PASSO
        if self._liberar_busca(u, r):
            r['EBX'], r['EDX'] = 0xffff, 0
        self.m.u8(rec + 0x88, 0)
        self.m.u8(rec + 0x88, 0)
        self.m.u8(rec + 0x89, 0)
        self.m.u16(rec + 0xc0, 0xffff)
        self.m.u8(rec + 0xbe, tipo)
        self.m.u8(rec + 2, 0xb)
        self.m.u16(rec + 0xb2, celula)
        if tipo == 9:
            self.m.u16(rec + 0xd8, 0)
        r['EAX'] = tipo
        return r

    def set_recolte_engin(self, regs):
        """SetRecolteEngin 0x444ebd: AX unit, DX cell. ResetOrdre, +0x7e = cell, search released, +0x88 = 0,
        +0x89 = 0, state 5, +0x82 = 0, +0xb2 = cell. EAX = EDX = the record address."""
        u, celula = regs['EAX'] & 0xffff, regs['EDX']
        rec = self._rec(u)
        self.reset_ordre(dict(EAX=u))
        self.m.u16(rec + 0x7e, celula)
        self._liberar_busca(u, None)
        self.m.u8(rec + 0x88, 0)
        self.m.u8(rec + 0x89, 0)
        self.m.u8(rec + 2, 5)
        self.m.u8(rec + 0x82, 0)
        self.m.u16(rec + 0xb2, celula)
        return dict(regs, EAX=rec, EDX=rec)

    def set_transporte_engin(self, regs):
        """SetTransporteEngin 0x444e7f: AX unit, DX value. State 0x12, +0x89 = 0, +0xb2 = value, +0x7e = value,
        search released, +0x88 = 0 (no ResetOrdre). EAX = the record; EDX = unit*276, or 0 after a release."""
        u, valor = regs['EAX'] & 0xffff, regs['EDX']
        rec = self._rec(u)
        self.m.u8(rec + 2, 0x12)
        self.m.u8(rec + 0x89, 0)
        self.m.u16(rec + 0xb2, valor)
        self.m.u16(rec + 0x7e, valor)
        edx = u * PASSO
        if self._liberar_busca(u, None):
            edx = 0
        self.m.u8(rec + 0x88, 0)
        return dict(regs, EAX=rec, EDX=edx)

    # ------------------------------------------------------------ selection-wide order setters
    def _unidades_selecionadas(self, jogador):
        """(slot, unit) pairs read live as the loop advances (the count is re-read every iteration)."""
        base = SELECOES + (jogador << 9)
        i = 0
        while i < self.m.u16(base):
            yield i, self.m.u16(base + 2 + 2 * i)
            i += 1

    def _falar(self, r, u, modo):
        saida = self.engin_ask(dict(r, EAX=u, EDX=modo, EBX=0))
        r.update(EAX=saida['EAX'], EBX=saida['EBX'], EDX=saida['EDX'])

    def set_deplace_engin_select(self, regs):
        """SetDeplaceEnginSelect 0x473e6e: AL player, DX cell. Each live selected unit of that owner gets
        SetDeplaceEngin and +0x110 = the cycle counter; the first that is neither a vehicle (11..15) nor
        aerial (16/17) asks mode 0xb when the player is local. EAX and EDX change."""
        r = dict(regs)
        jogador, destino = regs['EAX'] & 0xff, regs['EDX'] & 0xffff
        falou = 0
        for _, u in self._unidades_selecionadas(jogador):
            r['EAX'] = u
            self._vivo(r)
            if not r['EAX'] & 0xff:
                continue
            r['EAX'] = (self._pool() & 0xffffff00) | self.m.u8(self._rec(u))
            if r['EAX'] & 0xff != jogador:
                continue
            self.set_deplace_engin(dict(EAX=u, EDX=destino))
            r['EDX'] = self.m.u32(CONTADOR)
            self.m.u32(self._rec(u) + 0x110, r['EDX'])
            r['EAX'] = u
            self._tipo(r)
            r['EAX'] &= 0xff
            self._faixa(r, 0xb, 4)
            if r['EAX'] & 0xff:
                continue
            r['EAX'] = u
            self._tipo(r)
            r['EAX'] &= 0xff
            self._aereo(r)
            if r['EAX'] & 0xff:
                continue
            r['EAX'] = falou & 0xffff
            if falou >= 1:
                continue
            _baixo(r, 'EAX', jogador)
            _baixo(r, 'EDX', self.m.u8(JOGADOR_LOCAL))
            falou += 1
            if jogador != self.m.u8(JOGADOR_LOCAL):
                continue
            self._falar(r, u, 0xb)
        return dict(regs, EAX=r['EAX'], EDX=r['EDX'])

    def set_attaque_engin_select(self, regs):
        """SetAttaqueEnginSelect 0x473dbf: AL player, DL mode, BX reference. Each live selected unit of that
        owner gets +0x110 = the cycle counter and then SetAttaqueEngin (Combat's ``definir_ataque``); the first
        asks mode 0x17 when the player is local. EAX, EBX and EDX change."""
        r = dict(regs)
        jogador, modo, ref = regs['EAX'] & 0xff, regs['EDX'] & 0xff, regs['EBX'] & 0xffff
        falou = 0
        for i, u in self._unidades_selecionadas(jogador):
            r['EDX'] = i
            r['ECX'] = u
            r['EAX'] = u
            self._vivo(r)
            if not r['EAX'] & 0xff:
                continue
            rec = self._rec(u)
            r['EAX'] = rec
            r['EDX'] = ((u * PASSO) & 0xffffff00) | self.m.u8(rec)
            if self.m.u8(rec) != jogador:
                continue
            r['EBX'] = ref
            self.m.u32(rec + 0x110, self.m.u32(CONTADOR))
            if self.definir_ataque is None:
                raise DependenciaRamoCore('SetAttaqueEngin', 0x473e39, 'Combat attack-order provider required')
            saida = self.definir_ataque(u, modo, ref)
            r['EAX'], r['EDX'] = saida['EAX'] & M32, saida['EDX'] & M32
            r['EAX'] = falou & 0xffff
            if falou >= 1:
                continue
            _baixo(r, 'EAX', jogador)
            _baixo(r, 'EBX', self.m.u8(JOGADOR_LOCAL))
            falou += 1
            if jogador != self.m.u8(JOGADOR_LOCAL):
                continue
            self._falar(r, u, 0x17)
        return dict(regs, EAX=jogador << 9, EBX=r['EBX'], EDX=r['EDX'])

    def set_construit_batiment_select(self, regs):
        """SetConstruitBatimentSelect 0x473a07: AL player, DL structure type, BX cell. Each live selected type-7
        unit of that owner gets SetEnginConstruitBatiment; the first asks mode 0x11 when the player is local.
        EAX, EBX and EDX change."""
        r = dict(regs)
        jogador, tipo, celula = regs['EAX'] & 0xff, regs['EDX'] & 0xff, regs['EBX'] & 0xffff
        falou = 0
        for _, u in self._unidades_selecionadas(jogador):
            r['EDX'] = u
            r['ECX'] = u
            r['EAX'] = u
            r['EBX'] = self._pool()
            self._vivo(r)
            rec = self._rec(u)
            r['EDX'] = rec
            if not r['EAX'] & 0xff:
                continue
            _baixo(r, 'EAX', self.m.u8(rec))
            if r['EAX'] & 0xff != jogador:
                continue
            r['EDX'] = self.m.u8(rec + 1)
            if r['EDX'] != 7:
                continue
            saida = self.set_engin_construit_batiment(dict(r, EAX=u, EDX=tipo, EBX=celula))
            r.update(EAX=saida['EAX'], EBX=saida['EBX'], EDX=saida['EDX'])
            r['EDX'] = falou & 0xffff
            if falou >= 1:
                continue
            _baixo(r, 'EAX', jogador)
            _baixo(r, 'EDX', self.m.u8(JOGADOR_LOCAL))
            falou += 1
            if jogador != self.m.u8(JOGADOR_LOCAL):
                continue
            self._falar(r, u, 0x11)
        return dict(regs, EAX=r['EAX'], EBX=r['EBX'], EDX=jogador << 9)

    def set_recolte_engin_select(self, regs):
        """SetRecolteEnginSelect 0x473290: AL player, DX cell. Each live selected unit of that owner gets
        SetRecolteEngin; the first asks mode 0xf when the player is local. EAX and EDX change."""
        r = dict(regs)
        jogador, celula = regs['EAX'] & 0xff, regs['EDX'] & 0xffff
        falou = 0
        for _, u in self._unidades_selecionadas(jogador):
            rec = self._rec(u)
            r['EDX'] = rec
            r['EAX'] = u
            self._vivo(r)
            if not r['EAX'] & 0xff:
                continue
            _baixo(r, 'EAX', self.m.u8(rec))
            if r['EAX'] & 0xff != jogador:
                continue
            saida = self.set_recolte_engin(dict(r, EAX=u, EDX=celula))
            r['EAX'] = saida['EAX']
            r['EDX'] = falou & 0xffff
            if falou >= 1:
                continue
            _baixo(r, 'EAX', jogador)
            _baixo(r, 'EDX', self.m.u8(JOGADOR_LOCAL))
            falou += 1
            if jogador != self.m.u8(JOGADOR_LOCAL):
                continue
            self._falar(r, u, 0xf)
        return dict(regs, EAX=r['EAX'], EDX=r['EDX'])

    def set_transporte_engin_select(self, regs):
        """SetTransporteEnginSelect 0x473212: AL player, DX value. Each live selected unit, of any owner (no owner
        test), gets SetTransporteEngin; the first asks mode 0xf when the player is local. EAX and EDX change."""
        r = dict(regs)
        jogador, valor = regs['EAX'] & 0xff, regs['EDX'] & 0xffff
        falou = 0
        local = None
        for _, u in self._unidades_selecionadas(jogador):
            r['EDX'] = u
            r['EAX'] = u
            self._vivo(r)
            if not r['EAX'] & 0xff:
                continue
            saida = self.set_transporte_engin(dict(r, EAX=u, EDX=valor))
            r.update(EAX=saida['EAX'], EDX=saida['EDX'])
            r['EDX'] = falou & 0xffff
            if falou >= 1:
                continue
            local = self.m.u8(JOGADOR_LOCAL)
            r['EAX'] = (r['EAX'] & 0xffff0000) | (local << 8) | jogador
            falou += 1
            if jogador != local:
                continue
            self._falar(r, u, 0xf)
        return dict(regs, EAX=r['EAX'], EDX=r['EDX'])

    # ------------------------------------------------------------ dispatch by original name
    def chamar(self, nome, regs, pilha=()):
        """Run routine ``nome`` with the entry registers ``regs`` (and its pushed words); returns EAX..EBP."""
        regs = {k: regs[k] & M32 for k in REGISTROS}
        f = {
            'SelectionEngin': self.selection_engin, 'EnginAddSelection': self.engin_add_selection,
            'EnginSelectionnable': self.engin_selectionnable, 'SelectionAddEngin': self.selection_add_engin,
            'RetireSelectionEngin': self.retire_selection_engin, 'DeselectionEngin': self.deselection_engin,
            'DeSelectionGroupe': self.deselection_groupe, 'Deselection': self.deselection,
            'BatimentSelection': self.batiment_selection, 'BatimentDeselectionner': self.batiment_deselectionner,
            'SetDeplaceEnginSelect': self.set_deplace_engin_select,
            'SetAttaqueEnginSelect': self.set_attaque_engin_select,
            'SetConstruitBatimentSelect': self.set_construit_batiment_select,
            'SetEnginConstruitBatiment': self.set_engin_construit_batiment,
            'SetRecolteEnginSelect': self.set_recolte_engin_select, 'SetRecolteEngin': self.set_recolte_engin,
            'SetTransporteEnginSelect': self.set_transporte_engin_select,
            'SetTransporteEngin': self.set_transporte_engin, 'SetDeplaceEngin': self.set_deplace_engin,
            'ResetOrdre': self.reset_ordre, 'EnginAsk': self.engin_ask,
        }.get(nome)
        if nome == 'EnginInZone':
            if len(pilha) != 1:
                raise ValueError('EnginInZone takes exactly one pushed word (y2)')
            return self.engin_in_zone(regs, pilha[0])
        if f is None:
            raise KeyError(f'{nome} is not a translated selection/order routine')
        return f(regs)
