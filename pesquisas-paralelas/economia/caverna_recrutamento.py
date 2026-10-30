"""Cave structure body, structure habitation and sanctuary recruitment over live original memory (M3, S1).

Translated from the intact bytes after the native capture
``evidencias/caverna-recrutamento/captura-caverna-recrutamento-exibicao.json.xz`` was committed. Routines:
- the type-3 (CAVE) body of BatimentNextEtape, ``0x426aff..0x426c10`` (``corpo_caverna``), and BatimentNextEtape
  0x4268d4 itself restricted to type-3 structures (prelude, body and the shared tail ``0x41db1d``);
- BatimentHabitable 0x41cc70 and BatimentSetTechnologie 0x41c76c (structure types 2 and 3; the types with no
  branch), InitBatimentPlayer 0x41be88 and InitBatimentNeutre 0x41c017 (every type but the balloon 0x12, and
  the library 6 once its count reaches 0);
- InitRecruteTroupe 0x4283e2 (tag 17), CalculTroupe 0x4259e6 for structure types 1 and 2 (the sanctuary), and
  SortieTroupe 0x420e4c, including the abandonment of the structure its last colonist leaves;
- their economy leaves: EnginGetTimeRecrute 0x4410b7, EnginGetRessource 0x4410d2, TypeEnginEstRealisable
  0x44228e, BatimentGetColons 0x41a4c4, BatimentGetCapacite 0x41f3ed; TestRessource, EnleveMatiere,
  GetRessourceStock and BagInit run through ``ordens_economia`` (one implementation).

Calling convention. Each routine takes its entry registers EAX..EBP (plus ESP, the return slot) and returns
EAX..EBP as the original leaves them, callee-saved registers included, and the ESP after its RET; flags are not
modeled. Values the original keeps in its own stack frame are computed, not written: the native stack is not
part of the compared state. ``memoria``: ``u8/u16/u32(addr, value=None)`` (``memoria_quadro_core.MemoriaQuadro``).

Named dependencies (never defaulted). A callee owned elsewhere goes through ``externo(nome, chamada,
registradores) -> registradores``: ``chamada`` is the original call address; ``registradores`` holds the argument
registers the callee reads, at the widths of ``ARGUMENTOS``; the provider returns EAX..EBP as the callee leaves
them, after its stores, optionally with ``_incertos`` ({register: mask} of bits it does not reconstruct), which
this module carries to its own exit registers when they flow there. Without a provider the path raises
``DependenciaCavernaRecrutamento`` at that call, after the stores the original made before it. A routine of this
module listed in ``proprias`` runs here instead (default: all of them).
- Core: BagContient, BagContientTroupe, BagRetire, BagPrend, EnginGetBag, BatimentGetCase, BatimentGetType,
  DecouvreTerrain, IllumineTerrain, EteintTerrain, BatimentModifyMap, CalculPosition, RechercheDecalageSortie,
  EnginSetType, EnginAddVie, EnginResetFatigue, EnginSetExperimente, SetSortEngin, SetDeplaceEngin, EnginAsk;
- Economy, other slices: BatimentAjouteMatiere (``ciclo_trabalho``), TerrainDeposeMatiere 0x41bb8a;
- ai-runtime: iagUnitSendMessage, iagVilleSendMessage.

Branches outside the translated domain raise ``ForaDoDominioCaverna`` at their original address before any store
of that branch (see each routine).
"""
import struct

from ordens_economia import OrdensEconomia

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
ESTRUTURAS, PASSO = 0x49a0c8, 276
TOTAL_ESTRUTURAS = 1000
INDICADOR = 0x4dfb2c                 # per player (stride 6): u16 cave count, u16 per-cave word, u8 level
BIBLIOTECAS = 0x4dfb48               # u8 per player: library count
PENDENCIAS = 0x4dd6e8                # per player 22 x 104-byte Bags (stride 0x8f0), Bag of structure type t at +104 t
REALIZAVEIS = 0x4e1934               # u8 per player (stride 26) and unit type
TIPOS_UNIDADE = 0x4965ae             # 50-byte unit-type records: u16 time +0, food +2, parts +4, stone +6
TIPOS_ESTRUTURA = 0x495d8c           # 52-byte structure-type records: u8 capacity +0x12
AJUSTE_HOSPITAL = 0x495be8
SELECOES_ESTRUTURA = 0x495be0        # u16 per player: the selected structure
ANIMACAO = 0x508f80
JOGADOR_LOCAL = 0x508041
DEPOSITANTE = 0x4dfab8
COEFICIENTE, COEFICIENTE_14 = 0x49443a, 0x494432   # doubles read by CalculTroupe
RAIOS = {0: 20, 1: 8, 2: 10, 3: 8, 4: 5, 5: 8, 6: 8, 7: 8, 8: 8, 10: 7, 11: 7, 13: 8, 14: 8, 15: 8, 16: 8, 17: 4,
         18: 8, 19: 4, 20: 8, 21: 4}       # BatimentHabitable's table 0x41cc18 (types 9 and 12 never reach it)
ROTINAS = {
    'BatimentNextEtape': 0x4268d4, 'BatimentHabitable': 0x41cc70, 'BatimentSetTechnologie': 0x41c76c,
    'InitBatimentPlayer': 0x41be88, 'InitBatimentNeutre': 0x41c017, 'InitRecruteTroupe': 0x4283e2,
    'CalculTroupe': 0x4259e6, 'SortieTroupe': 0x420e4c, 'EnginGetTimeRecrute': 0x4410b7,
    'EnginGetRessource': 0x4410d2, 'TypeEnginEstRealisable': 0x44228e, 'BatimentGetColons': 0x41a4c4,
    'BatimentGetCapacite': 0x41f3ed,
}
# Callees computed inline through ``ordens_economia`` or as x87 arithmetic (no call into another front).
INTERNAS = ('TestRessource', 'EnleveMatiere', 'GetRessourceStock', 'BagInit', '__CHP')
ARGUMENTOS = {
    'BagContient': {'EAX': M32, 'EDX': 0xff, 'EBX': 0xffff}, 'BagContientTroupe': {'EAX': M32},
    'BagRetire': {'EAX': M32, 'EDX': 0xff, 'EBX': 0xffff}, 'BagPrend': {'EAX': M32, 'EDX': 0xff, 'EBX': 0xffff},
    'EnginGetBag': {'EAX': 0xffff}, 'BatimentGetType': {'EAX': 0xffff},
    # BatimentHabitable reuses EDX/EBX after BatimentGetCase (EDX + 3 is DecouvreTerrain's radius): passed whole
    # so a provider returns them as the callee leaves them.
    'BatimentGetCase': {'EAX': 0xffff, 'EDX': M32, 'EBX': M32},
    'DecouvreTerrain': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff},
    'IllumineTerrain': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff},
    'CalculPosition': {'EAX': 0xffff, 'EBX': 0xff}, 'RechercheDecalageSortie': {'EAX': 0xffff},
    'EnginSetType': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff, 'ECX': 0xff},
    'EnginAddVie': {'EAX': 0xffff, 'EDX': 0xffff},
    'EnginResetFatigue': {'EAX': 0xffff}, 'EnginSetExperimente': {'EAX': 0xffff, 'EDX': 0xffff},
    'SetSortEngin': {'EAX': 0xffff, 'EDX': 0xffff}, 'SetDeplaceEngin': {'EAX': 0xffff, 'EDX': 0xffff},
    'EnginAsk': {'EAX': 0xffff, 'EDX': 0xff, 'EBX': 0xff},
    'BatimentAjouteMatiere': {'EAX': 0xff, 'EDX': 0xffff, 'EBX': 0xff, 'ECX': 0xffff},
    'TerrainDeposeMatiere': {'EAX': 0xff, 'EDX': 0xffff, 'EBX': 0xffff, 'ECX': 0xff},
    'iagUnitSendMessage': {'EAX': 0xffff, 'EDX': 0xff, 'EBX': M32},
    'iagVilleSendMessage': {'EAX': 0xffff, 'EDX': 0xff, 'EBX': M32},
    'SortilegeResetRealisable': {'EAX': 0xff}, 'SortilegeSetTechnologie': {'EAX': 0xff},
    'BatimentAdjacent': {'EAX': 0xffff, 'EDX': 0xffff},
    'EteintTerrain': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff}, 'BatimentModifyMap': {'EAX': 0xffff, 'EDX': 0xff},
}
PILHA_EXTERNA = {'TerrainDeposeMatiere': 1}     # one pushed word (0), popped by the callee


class DependenciaCavernaRecrutamento(NotImplementedError):
    """A callee owned elsewhere was reached without its provider."""
    def __init__(self, rotina, chamada, motivo='provider required'):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: {motivo}')


class ForaDoDominioCaverna(NotImplementedError):
    """A branch outside the translated domain; nothing was written by it."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made by this branch')


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


def _idiv(a, b, rotina, endereco):
    """x86 IDIV of 32-bit signed values: (quotient, remainder), truncation toward zero."""
    a, b = _s32(a), _s32(b)
    if b == 0:
        raise ZeroDivisionError(f'{rotina}: idiv by zero at 0x{endereco:x} (the original faults)')
    q = abs(a) // abs(b)
    q = q if (a < 0) == (b < 0) else -q
    return q & M32, (a - q * b) & M32


def _baixo(v, b):
    return (v & 0xffffff00) | (b & 0xff)


class CavernaRecrutamento:
    def __init__(self, memoria, *, externo=None, proprias=None):
        self.m = memoria
        self.externo = externo
        self.proprias = set(ROTINAS) if proprias is None else set(proprias)
        self.ordens = OrdensEconomia(memoria)
        self.incertos = {}
        self._ultimos_incertos = {}

    # ------------------------------------------------------------ helpers
    def _ext(self, nome, chamada, pilha=(), **regs):
        """Call ``nome`` at ``chamada`` with argument registers ``regs``; returns EAX..EBP after it (bits the
        provider marks uncertain are recorded in ``self.incertos`` for the registers they reach)."""
        if nome in self.proprias and nome in ROTINAS:
            entrada = {k: regs.get(k, 0) & M32 for k in REG7}
            entrada['ESP'] = 0
            saida = getattr(self, '_' + nome)(entrada)
            self._ultimos_incertos = dict(saida.get('_incertos') or {})
            return {k: saida[k] & M32 for k in REG7}
        if self.externo is None:
            raise DependenciaCavernaRecrutamento(nome, chamada)
        larguras = ARGUMENTOS[nome]
        entrada = {k: regs[k] & larguras[k] for k in larguras}
        if pilha:
            entrada['_pilha'] = list(pilha)
        saida = self.externo(nome, chamada, entrada)
        self._ultimos_incertos = dict(saida.get('_incertos') or {})
        return {k: saida[k] & M32 for k in REG7 if k in saida}

    @staticmethod
    def _est(s):
        s &= 0xffff
        if s >= TOTAL_ESTRUTURAS:
            raise ValueError(f'Structure index {s} outside 0..999')
        return ESTRUTURAS + PASSO * s

    @staticmethod
    def _sair(regs, r, salvos, pop=0, incertos=None):
        saida = {k: (regs[k] if k in salvos else r[k]) & M32 for k in REG7}
        saida['ESP'] = (regs.get('ESP', 0) + 4 + pop) & M32
        if incertos:
            saida['_incertos'] = {k: v for k, v in incertos.items() if v and k not in salvos}
        return saida

    def _nivel(self, p, rotina, endereco_div):
        """The stock-level recalculation inlined after a cave-count or debit change (player ``p`` < 4 with a
        nonzero count): GetRessourceStock into the frame, AX = (food + stone stock) low word // count,
        level byte = AX * 7 // the per-cave word. Returns (EAX, EDX, EBX) after it."""
        m = self.m
        base = 0x4e2ea8 + 32 * p
        comida = (m.u16(base + 0xa) - m.u16(base + 8)) & 0xffff
        pedra = (m.u16(base + 0x12) - m.u16(base + 0x10)) & 0xffff
        q = ((comida + pedra) & 0xffff) // m.u16(INDICADOR + 6 * p)
        w2 = m.u16(INDICADOR + 6 * p + 2)
        eax, edx = _idiv(q * 7, w2, rotina, endereco_div)
        m.u8(INDICADOR + 6 * p + 4, eax)
        return eax, edx, w2

    # ------------------------------------------------------------ economy leaves
    def _EnginGetTimeRecrute(self, regs):
        """EnginGetTimeRecrute 0x4410b7: AL unit type -> AX = u16 time of its record (EAX upper 0)."""
        t = regs['EAX'] & 0xff
        return self._sair(regs, dict(regs, EAX=self.m.u16(TIPOS_UNIDADE + 50 * t)), REG7[1:])

    def _EnginGetRessource(self, regs):
        """EnginGetRessource 0x4410d2: AL type; writes u16 food (+2) at [EDX], stone (+6) at [EBX], parts (+4)
        at [ECX]. EAX = parts, EBX = type, EDX = (EDX & 0xffff0000) | stone."""
        t = regs['EAX'] & 0xff
        r = TIPOS_UNIDADE + 50 * t
        comida, pecas, pedra = self.m.u16(r + 2), self.m.u16(r + 4), self.m.u16(r + 6)
        self.m.u16(regs['EDX'], comida)
        self.m.u16(regs['EBX'], pedra)
        self.m.u16(regs['ECX'], pecas)
        return self._sair(regs, dict(regs, EAX=pecas, EBX=t, EDX=(regs['EDX'] & 0xffff0000) | pedra),
                          ('ECX', 'ESI', 'EDI', 'EBP'))

    def _TypeEnginEstRealisable(self, regs):
        """TypeEnginEstRealisable 0x44228e: AL player, DL unit type -> EAX = byte [0x4e1934 + 26 p + t];
        EDX = 26 p."""
        p, t = regs['EAX'] & 0xff, regs['EDX'] & 0xff
        return self._sair(regs, dict(regs, EAX=self.m.u8(REALIZAVEIS + 26 * p + t), EDX=26 * p),
                          ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    def _BatimentGetColons(self, regs):
        """BatimentGetColons 0x41a4c4: AX structure -> BagContient(Bag +0xc, DL 1, BX 9) (Core); its EAX."""
        e = self._est(regs['EAX'])
        r = self._ext('BagContient', 0x41a4ec, EAX=e + 0xc, EDX=1, EBX=9)
        return self._sair(regs, dict(regs, EAX=r['EAX'], ECX=r['ECX'], ESI=r['ESI'], EDI=r['EDI'], EBP=r['EBP']),
                          ('EBX', 'EDX'))

    def _BatimentGetCapacite(self, regs):
        """BatimentGetCapacite 0x41f3ed: AX structure -> AL = capacity byte +0x12 of its type record (type 14:
        minus 1; type 0x13: minus byte 0x495be8); EAX upper = (13 type) upper."""
        e = self._est(regs['EAX'])
        t = self.m.u8(e + 8)
        cap = self.m.u8(TIPOS_ESTRUTURA + 52 * t + 0x12)
        if t == 0xe:
            cap = cap - 1
        elif t == 0x13:
            cap = cap - self.m.u8(AJUSTE_HOSPITAL)
        return self._sair(regs, dict(regs, EAX=_baixo(13 * t, cap)), REG7[1:])

    # ------------------------------------------------------------ cave body
    def corpo_caverna(self, estrutura):
        """BatimentNextEtape's type-3 body 0x426aff..0x426c10 for structure ``estrutura`` (DI). Returns EAX at
        the exit 0x4281c0 (the caller ignores it; every other register is restored by the tail 0x41db1d).

        BagContient(Bag +0xc, DL 1, BX 9) (Core): no colonist -> exit with BagContient's EAX, AL 0. Otherwise,
        unless bit 0 of u32 0x508f80 is set: +0x75 nonzero raises the counter +0x76 by one up to 15; +0x75 zero
        lowers it by one down to 0."""
        m = self.m
        e = self._est(estrutura)
        tipo = m.u8(e + 8)
        if tipo != 3:
            raise ForaDoDominioCaverna('BatimentNextEtape', 0x426aff, f'structure type {tipo} at the type-3 body')
        r = self._ext('BagContient', 0x426b8d, EAX=e + 0xc, EDX=1, EBX=9)
        self.incertos = {'EAX': self._ultimos_incertos.get('EAX', 0) & ~0xff} if self.externo else {}
        if not r['EAX'] & 0xffff:
            return r['EAX'] & 0xffffff00
        self.incertos = {}
        if m.u8(ANIMACAO) & 1:
            return 3
        contador = m.u8(e + 0x76)
        if m.u8(e + 0x75):
            if contador >= 15:
                return contador
            m.u8(e + 0x76, contador + 1)
            return contador
        if not contador:
            return 0
        m.u8(e + 0x76, contador - 1)
        return (((contador - 1) & 0xff) << 8) | contador

    def _BatimentNextEtape(self, regs):
        """BatimentNextEtape 0x4268d4 for a type-3 structure (AX): the type switch 0x426880, the body, the tail.
        Other types are ai-runtime's dispatch and the other bodies (``ForaDoDominioCaverna`` at 0x426910)."""
        e = self._est(regs['EAX'])
        if self.m.u8(e + 8) != 3:
            raise ForaDoDominioCaverna('BatimentNextEtape', 0x426910, f'structure type {self.m.u8(e + 8)}')
        self.incertos = {}
        eax = self.corpo_caverna(regs['EAX'])
        return self._sair(regs, dict(regs, EAX=eax), REG7[1:], incertos=self.incertos)

    # ------------------------------------------------------------ habitation and ownership
    def _BatimentSetTechnologie(self, regs):
        """BatimentSetTechnologie 0x41c76c: AL player, DL structure type. Player >= 4: nothing. Bag
        B = 0x4dd6e8 + 0x8f0 p + 104 t. Type 3: BagInit(B, 3). Type 2: BagInit(B, 4), then for unit types 5, 6,
        7 TypeEnginEstRealisable(p, u) -> BagPrend(B, 6, u) (Core). Types 0, 4, 7..0xc, 0xe, 0x11, 0x13 and
        above 0x14: nothing. Types 1, 5, 6, 0xd, 0xf, 0x10, 0x12, 0x14 are outside this translation."""
        p, t = regs['EAX'] & 0xff, regs['EDX'] & 0xff
        if p >= 4:
            return self._sair(regs, regs, REG7)
        sem_ramo = {0, 4, 7, 8, 9, 0xa, 0xb, 0xc, 0xe, 0x11, 0x13} | set(range(0x15, 0x100))
        if t in sem_ramo:
            return self._sair(regs, regs, REG7)
        if t not in (2, 3):
            raise ForaDoDominioCaverna('BatimentSetTechnologie', 0x41c7af, f'structure type {t:#x}')
        bag = (PENDENCIAS + 0x8f0 * p + 104 * t) & M32
        r = self.ordens.bag_init(dict(regs, EAX=bag, EDX=3 if t == 3 else 4, ESP=0))
        eax, edx = r['EAX'], r['EDX']
        if t == 2:
            ebx = p
            for u in (5, 6, 7):
                q = self._ext('TypeEnginEstRealisable', 0x41c89a, EAX=p, EDX=u)
                eax, edx = q['EAX'], q['EDX']
                if eax & 0xff:
                    q = self._ext('BagPrend', 0x41c8af, EAX=bag, EDX=6, EBX=u)
                    eax, edx, ebx = q['EAX'], q['EDX'], q['EBX']
        return self._sair(regs, dict(regs, EAX=eax, EDX=edx), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    def _BatimentHabitable(self, regs):
        """BatimentHabitable 0x41cc70: AX structure (the hand-over of a 0xc8 structure to its new owner).
        BatimentSetTechnologie(owner, type); types 0x11/9/0xc skip to the end; type 4: +0x78 = 0; type 3 with
        owner < 4 and a nonzero cave count: the stock level is recalculated. Then cell = BatimentGetCase(AX, EDX =
        R), DecouvreTerrain(cell, R + 3, owner), IllumineTerrain(cell, R, owner) with R from table 0x41cc18;
        finally u16 +0x84 = 0xc8. EAX = the last callee's; every other register restored."""
        m = self.m
        s = regs['EAX'] & 0xffff
        e = self._est(s)
        tipo, dono = m.u8(e + 8), m.u8(e + 4)
        r = self._ext('BatimentSetTechnologie', 0x41cca4, EAX=dono, EDX=tipo)
        eax = tipo
        incertos = {}
        if tipo not in (0x11, 9, 0xc):
            if tipo == 4:
                m.u16(e + 0x78, 0)
            elif tipo == 3 and dono < 4 and m.u16(INDICADOR + 6 * dono):
                self._nivel(dono, 'BatimentHabitable', 0x41cd55)
            if tipo > 0x15:
                raise ForaDoDominioCaverna('BatimentHabitable', 0x41cd62, f'structure type {tipo} (no radius)')
            raio = RAIOS[tipo]
            c = self._ext('BatimentGetCase', 0x41cda3, EAX=s, EDX=raio, EBX=0)
            celula = c['EAX'] & 0xffff
            self._ext('DecouvreTerrain', 0x41cdb9, EAX=celula, EDX=(c['EDX'] + 3) & 0xffff,
                      EBX=_baixo(c['EBX'], dono))
            r = self._ext('IllumineTerrain', 0x41cdca, EAX=celula, EDX=raio, EBX=dono)
            eax = r['EAX']
            incertos = {'EAX': self._ultimos_incertos.get('EAX', 0)}
        m.u16(e + 0x84, 0xc8)
        return self._sair(regs, dict(regs, EAX=eax), REG7[1:], incertos=incertos)

    def _InitBatimentPlayer(self, regs):
        """InitBatimentPlayer 0x41be88: AX structure, DL player (the owner is not written). Type 3: the cave count
        u16 0x4dfb2c + 6 p += 1; for p < 4 and a nonzero count the stock level is recalculated (EAX/EDX = its
        IDIV quotient/remainder). Type 6: library count byte += 1. Other types: nothing (EAX = entry with AH = DL,
        AL = type; EDX = the record address). Type 0x12 (balloon arrival) is outside this translation."""
        m = self.m
        e = self._est(regs['EAX'])
        p = regs['EDX'] & 0xff
        tipo = m.u8(e + 8)
        eax = (regs['EAX'] & 0xffff0000) | (p << 8) | tipo
        if tipo == 0x12:
            raise ForaDoDominioCaverna('InitBatimentPlayer', 0x41bec6, 'type-0x12 balloon arrival')
        if tipo == 6:
            m.u8(BIBLIOTECAS + p, m.u8(BIBLIOTECAS + p) + 1)
            return self._sair(regs, dict(regs, EAX=p, EDX=e), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))
        if tipo != 3:
            return self._sair(regs, dict(regs, EAX=eax, EDX=e), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))
        n = (m.u16(INDICADOR + 6 * p) + 1) & 0xffff
        m.u16(INDICADOR + 6 * p, n)
        if p >= 4:
            return self._sair(regs, dict(regs, EAX=p, EDX=e), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))
        if not n:
            return self._sair(regs, dict(regs, EAX=p, EDX=0), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))
        eax, edx, _ = self._nivel(p, 'InitBatimentPlayer', 0x41bfbe)
        return self._sair(regs, dict(regs, EAX=eax, EDX=edx), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    def _InitBatimentNeutre(self, regs):
        """InitBatimentNeutre 0x41c017: AX structure, DL player (owner/state unchanged). Type 3: the cave count
        -= 1; unless state +5 is 3, TerrainDeposeMatiere(depositor byte 0x4dfab8, structure, origin + 0x202,
        CL 0 food then CL 1 stone, pushed 0) (Economy, named). Type 6: library count -= 1 (at 0
        SortilegeResetRealisable/SortilegeSetTechnologie, named). Type 0x14: +0x7a = 0, +0x104 = 0, u32 +0x108 =
        1. Other types: nothing (EAX = entry with AL = type). Type 0x12 is outside this translation."""
        m = self.m
        s = regs['EAX'] & 0xffff
        e = self._est(s)
        tipo = m.u8(e + 8)
        p = regs['EDX'] & 0xff
        salvos = ('EBX', 'ECX', 'ESI', 'EDI', 'EBP')
        eax = _baixo(regs['EAX'], tipo)
        if tipo == 0x12:
            raise ForaDoDominioCaverna('InitBatimentNeutre', 0x41c05d, 'type-0x12 balloon departure')
        if tipo == 0x14:
            m.u8(e + 0x7a, 0)
            m.u8(e + 0x104, 0)
            m.u32(e + 0x108, 1)
            return self._sair(regs, dict(regs, EAX=eax), salvos + ('EDX',))
        if tipo == 6:
            n = (m.u8(BIBLIOTECAS + p) - 1) & 0xff
            m.u8(BIBLIOTECAS + p, n)
            if n:
                return self._sair(regs, dict(regs, EAX=n, EDX=_baixo(regs['EDX'], n)), salvos)
            self._ext('SortilegeResetRealisable', 0x41c152, EAX=p)
            r = self._ext('SortilegeSetTechnologie', 0x41c159, EAX=p)
            return self._sair(regs, dict(regs, EAX=r['EAX'], EDX=r['EDX']), salvos)
        if tipo != 3:
            return self._sair(regs, dict(regs, EAX=eax), salvos + ('EDX',))
        m.u16(INDICADOR + 6 * p, m.u16(INDICADOR + 6 * p) - 1)
        if m.u8(e + 5) == 3:
            return self._sair(regs, dict(regs, EAX=3), salvos + ('EDX',))
        r = None
        for modo in (0, 1):
            celula = (m.u16(e + 2) + 0x202) & 0xffff
            r = self._ext('TerrainDeposeMatiere', 0x41c10a if modo == 0 else 0x41c12d, pilha=(0,),
                          EAX=m.u8(DEPOSITANTE), EDX=s, EBX=celula, ECX=modo)
        return self._sair(regs, dict(regs, EAX=r['EAX'], EDX=r['EDX']), salvos)

    # ------------------------------------------------------------ recruitment
    def _InitRecruteTroupe(self, regs):
        """InitRecruteTroupe 0x4283e2 (tag 17): AL unit type, DL player; the structure is the player's selected one
        (u16 0x495be0 + 2 p). Costs (EnginGetRessource): food +2, stone +6, parts +4 of the unit-type record.
        TestRessource fails, or the structure type is not 1/2/5/13/15/16/18/20, or a request is pending (+0x74):
        AL = 0, nothing written. Otherwise EnleveMatiere food, stone, parts (each followed by the stock-level
        recalculation when the cave count is nonzero), +0x74 = 1, +0x7a = 0, +5 = 4, u32 +0x8c = 1, +0x7b = type,
        u16 +0x7e = 0, u16 +0x80 = +0x82 = 0 (not for type 0x14), u16 +0x7c = RechercheDecalageSortie(structure)
        (Core), AL = 1. EDX: the stone cost on refusal, RechercheDecalageSortie's on success."""
        m = self.m
        t, p = regs['EAX'] & 0xff, regs['EDX'] & 0xff
        s = m.u16(SELECOES_ESTRUTURA + 2 * p)
        e = self._est(s)
        r = TIPOS_UNIDADE + 50 * t
        comida, pecas, pedra = m.u16(r + 2), m.u16(r + 4), m.u16(r + 6)
        tr = self.ordens.test_ressource(dict(regs, EAX=comida, EDX=pedra, EBX=pecas, ECX=0, ESP=0), [p])
        recusa = self._sair(regs, dict(regs, EAX=tr['EAX'] & 0xffffff00, EDX=pedra), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))
        if not tr['EAX'] & 0xff:
            return recusa
        tipo = m.u8(e + 8)
        if tipo not in (1, 2, 5, 13, 15, 16, 18, 20) or m.u8(e + 0x74):
            return recusa
        estado = dict(regs, ECX=p, ESI=e, EDI=4 * p)
        for recurso, quantidade in ((1, comida), (2, pedra), (0, pecas)):
            q = self.ordens.enleve_matiere(dict(estado, EAX=recurso, EBX=p, EDX=quantidade, ESP=0))
            estado.update(EAX=q['EAX'], EBX=q['EBX'], EDX=q['EDX'])
            if m.u16(INDICADOR + 6 * p):
                eax, edx, ebx = self._nivel(p, 'InitRecruteTroupe', {1: 0x4284e6, 2: 0x428565, 0: 0x4285e1}[recurso])
                estado.update(EAX=eax, EDX=edx, EBX=ebx)
        m.u8(e + 0x74, 1)
        m.u8(e + 0x7a, 0)
        m.u8(e + 5, 4)
        m.u32(e + 0x8c, 1)
        m.u8(e + 0x7b, t)
        m.u16(e + 0x7e, 0)
        if tipo != 0x14:
            m.u16(e + 0x80, 0)
            m.u16(e + 0x82, 0)
        q = self._ext('RechercheDecalageSortie', 0x42863b, EAX=m.u16(SELECOES_ESTRUTURA + 2 * p))
        incertos = {k: v for k, v in self._ultimos_incertos.items() if k in ('EAX', 'EDX')} if self.externo else {}
        if 'EAX' in incertos:
            incertos['EAX'] &= ~0xff
        m.u16(e + 0x7c, q['EAX'])
        return self._sair(regs, dict(regs, EAX=_baixo(q['EAX'], 1), EDX=q['EDX']), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'),
                          incertos=incertos)

    def _CalculTroupe(self, regs):
        """CalculTroupe 0x4259e6 for structure types 1 and 2 (AX). No request (u32 +0x8c = 0 or +0x74 = 0): EAX =
        (276 s) with AL 0. Otherwise, while +0x8c < time * 100 (EnginGetTimeRecrute(+0x7b)), +0x8c += 100 + the
        low word of trunc(colonists / capacity * double [0x49443a]) (x87, precision 53, chop; a zero capacity
        gives 0x80000000); then SortieTroupe(AX = s, DL = 4) in every case; EAX = SortieTroupe's. Every other
        register is restored. Types 0, 3, 4: nothing. Other types are outside this translation."""
        m = self.m
        s = regs['EAX'] & 0xffff
        e = self._est(s)
        tipo = m.u8(e + 8)
        if tipo in (0, 3, 4):
            return self._sair(regs, dict(regs, EAX=_baixo(276 * s, tipo)), REG7[1:])
        if tipo not in (1, 2):
            raise ForaDoDominioCaverna('CalculTroupe', 0x425a0f, f'structure type {tipo}')
        if not m.u32(e + 0x8c) or not m.u8(e + 0x74):
            return self._sair(regs, dict(regs, EAX=(276 * s) & 0xffffff00), REG7[1:])
        tempo = self._ext('EnginGetTimeRecrute', 0x425a84, EAX=m.u8(e + 0x7b))['EAX'] & 0xffff
        if tempo * 100 > m.u32(e + 0x8c):
            colonos = self._ext('BatimentGetColons', 0x425aaf, EAX=s)['EAX'] & 0xffff
            capacidade = self._ext('BatimentGetCapacite', 0x425acd, EAX=s)['EAX'] & 0xff
            t = self._ext('BatimentGetType', 0x425ae8, EAX=s)['EAX'] & 0xff
            a = COEFICIENTE_14 if t == 0xe else COEFICIENTE
            coef = struct.unpack('<d', struct.pack('<II', m.u32(a), m.u32(a + 4)))[0]
            convertido = 0x80000000 if capacidade == 0 else int((colonos / capacidade) * coef) & M32
            m.u32(e + 0x8c, m.u32(e + 0x8c) + (convertido & 0xffff) + 100)
        r = self._ext('SortieTroupe', 0x425b50, EAX=s, EDX=4)
        return self._sair(regs, dict(regs, EAX=r['EAX']), REG7[1:], incertos=dict(self.incertos))

    def _SortieTroupe(self, regs):
        """SortieTroupe 0x420e4c: AX structure, DL direction. Below the threshold (time * 100 > u32 +0x8c): EAX =
        time, EDX = time * 100. Otherwise: the first colonist leaves the Bag (BagRetire(B, 1, 9)), its carried
        stone (tag 2 value 2) then food (tag 2 value 1) are credited (BagRetire + BatimentAjouteMatiere(resource,
        value, owner, structure)); CalculPosition(structure, direction); EnginSetType(unit, cell,
        BL preserved by CalculPosition, CL = +0x7b);
        EnginAddVie(unit, 1000); EnginResetFatigue; EnginSetExperimente(unit, cell); SetSortEngin;
        SetDeplaceEngin(unit, +0x7c); EnginAsk(unit, 6, 0) for the local player's structure. A structure that
        still holds a colonist (type 2: or a troop) then clears its request (+0x78 = 0xffff, +0x7b = 0xff, +0x7c =
        +0x7e = 0, +0x86 = 0xffff, +0x80 = +0x82 = 0 unless type 0x14, +0x74 = 0, +0x8c = 0, +5 = 5 unless 3) and
        sends iagUnitSendMessage(unit, 0x46), iagVilleSendMessage(structure, 3); an emptied structure is first
        abandoned (``_abandonar``, 0x42101d..0x42114e: owner 0xc8). EDX is not restored by the epilogue."""
        m = self.m
        s = regs['EAX'] & 0xffff
        direcao = regs['EDX'] & 0xff
        e = self._est(s)
        tempo = self._ext('EnginGetTimeRecrute', 0x420e7a, EAX=m.u8(e + 0x7b))['EAX'] & 0xffff
        progresso = m.u32(e + 0x8c)
        if tempo * 100 > progresso:
            return self._sair(regs, dict(regs, EAX=tempo, EDX=tempo * 100), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))
        bag = e + 0xc
        u = self._ext('BagRetire', 0x420eae, EAX=bag, EDX=1, EBX=9)['EAX']
        bolsa = self._ext('EnginGetBag', 0x420ebc, EAX=u & 0xffff)['EAX']
        dono = m.u8(e + 4)
        for valor, recurso, chamadas in ((2, 2, (0x420ecc, 0x420ee9, 0x420efa)), (1, 1, (0x420f0d, 0x420f29, 0x420f3e))):
            while self._ext('BagContient', chamadas[0], EAX=bolsa, EDX=2, EBX=valor)['EAX'] & 0xffff:
                q = self._ext('BagRetire', chamadas[1], EAX=bolsa, EDX=2, EBX=valor)['EAX'] & 0xffff
                self._ext('BatimentAjouteMatiere', chamadas[2], EAX=recurso, EDX=q, EBX=dono, ECX=s)
        unidade = u & 0xffff
        c = self._ext('CalculPosition', 0x420f5a, EAX=s, EBX=direcao, ECX=0, ESI=unidade, EDI=e)
        celula = c['EAX'] & 0xffff
        self._ext('EnginSetType', 0x420f69, EAX=unidade, EDX=celula, EBX=c['EBX'],
                  ECX=_baixo(c['ECX'], m.u8(e + 0x7b)))
        self._ext('EnginAddVie', 0x420f75, EAX=unidade, EDX=1000)
        self._ext('EnginResetFatigue', 0x420f7c, EAX=unidade)
        self._ext('EnginSetExperimente', 0x420f85, EAX=unidade, EDX=celula)
        # EBP saves CalculPosition's cell; EnginSetExperimente preserves its DX at this call.
        self._ext('SetSortEngin', 0x420f8c, EAX=unidade, EDX=celula)
        self._ext('SetDeplaceEngin', 0x420f99, EAX=unidade, EDX=m.u16(e + 0x7c))
        if m.u8(e + 4) == m.u8(JOGADOR_LOCAL):
            self._ext('EnginAsk', 0x420fb2, EAX=unidade, EDX=6, EBX=0)
        tipo = m.u8(e + 8)
        habitada = False
        if tipo in (0x15, 2):
            habitada = bool(self._ext('BagContientTroupe', 0x420fe1 if tipo == 0x15 else 0x420ff3, EAX=bag)['EAX'] & 0xff)
        if not habitada:
            habitada = bool(self._ext('BagContient', 0x421009, EAX=bag, EDX=1, EBX=9)['EAX'] & 0xffff)
        if not habitada:
            self._abandonar(s, e)
        self._limpar_pedido(e)
        self._ext('iagUnitSendMessage', 0x4211d3, EAX=unidade, EDX=0x46, EBX=0)
        r = self._ext('iagVilleSendMessage', 0x4211e5, EAX=s, EDX=3, EBX=0)
        incertos = {k: v for k, v in self._ultimos_incertos.items() if k in ('EAX', 'EDX')} if self.externo else {}
        return self._sair(regs, dict(regs, EAX=r['EAX'], EDX=r['EDX']), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'),
                          incertos=incertos)

    def _limpar_pedido(self, e):
        """The request reset 0x42107d / 0x421153: +0x78 = 0xffff, +0x7b = 0xff, +0x7c = +0x7e = 0, +0x86 = 0xffff,
        +0x80 = +0x82 = 0 unless type 0x14, +0x74 = 0, +0x8c = 0, +5 = 5 unless 3."""
        m = self.m
        m.u16(e + 0x78, 0xffff)
        m.u8(e + 0x7b, 0xff)
        m.u16(e + 0x7c, 0)
        m.u16(e + 0x7e, 0)
        m.u16(e + 0x86, 0xffff)
        if m.u8(e + 8) != 0x14:
            m.u16(e + 0x80, 0)
            m.u16(e + 0x82, 0)
        m.u8(e + 0x74, 0)
        m.u32(e + 0x8c, 0)
        if m.u8(e + 5) != 3:
            m.u8(e + 5, 5)

    def _abandonar(self, s, e):
        """SortieTroupe 0x42101d..0x42114e, the structure left with no colonist (nor, types 2/0x15, troop): types
        1/2/5 reset the request first; unless type 9/0xc, BatimentGetCase(structure, DX = the type's radius
        [table 0x420df4, BatimentHabitable's], BL = owner) and EteintTerrain(its cell, its EDX, its EBX) (Core);
        the owner's structure selection u16 0x495be0 + 2 owner := 0xffff when it is this structure; owner +4 :=
        0xc8; BatimentModifyMap(structure, DL 1) (Core). The caller then runs the common reset and messages."""
        m = self.m
        if m.u8(e + 8) in (1, 2, 5):
            self._limpar_pedido(e)
        tipo = m.u8(e + 8)
        if tipo not in (9, 0xc):
            if tipo > 0x15:
                raise ForaDoDominioCaverna('SortieTroupe', 0x42123d, f'structure type {tipo} (uninitialized radius)')
            g = self._ext('BatimentGetCase', 0x42110c, EAX=s, EDX=RAIOS[tipo], EBX=m.u8(e + 4))
            self._ext('EteintTerrain', 0x421116, EAX=g['EAX'] & 0xffff, EDX=g['EDX'], EBX=g['EBX'])
        dono = m.u8(e + 4)
        if m.u16(SELECOES_ESTRUTURA + 2 * dono) == s & 0xffff:
            m.u16(SELECOES_ESTRUTURA + 2 * dono, 0xffff)
        m.u8(e + 4, 0xc8)
        self._ext('BatimentModifyMap', 0x42114e, EAX=s, EDX=1)

    # ------------------------------------------------------------ entry point
    def chamar(self, nome, regs):
        """Run routine ``nome`` with entry registers ``regs`` (EAX..EBP, optional ESP)."""
        if nome not in ROTINAS:
            raise KeyError(f'{nome} is not a translated cave/recruitment routine')
        entrada = {k: regs[k] & M32 for k in REG7}
        entrada['ESP'] = regs.get('ESP', 0) & M32
        return getattr(self, '_' + nome)(entrada)


def provedor_caverna(caverna, outros=None):
    """``externo(nome, chamada, registradores)`` serving this module's routines (BatimentHabitable,
    InitBatimentPlayer, InitBatimentNeutre, ...) to another module (``ciclo_trabalho``, Core's
    ``entrada_estruturas``); other names go to ``outros`` or raise ``DependenciaCavernaRecrutamento``."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise DependenciaCavernaRecrutamento(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        saida = caverna.chamar(nome, {k: regs.get(k, 0) for k in REG7})
        return {k: v for k, v in saida.items() if k != 'ESP'}
    return externo
