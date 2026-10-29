"""Economy order setters and construction gates over live original memory (M3 groundwork).

Translated from the intact bytes (``evidencias/ordens-economia/*.asm``) after the native capture
``evidencias/ordens-economia/captura-ordens-economia-exibicao.json`` was committed. Routines:
EnginTravailSelectionne, SetMineEnginSelect/SetMineEngin, SetDepotEnginSelect/SetDepotEngin,
SetRamasseEnginSelect/SetRamasseEngin, TestRessource, GetRessourceStock, EnleveMatiere,
CreerBatiment (with BagReset/BagInit) and one CalculConstruireBatiment tick of a builder that
walks to and starts a structure.

Every routine takes its entry registers EAX..EBP plus ESP (the address of its return slot) and
returns EAX..EBP and the ESP after its RET, exactly as the original leaves them (callee-saved
registers included). Arithmetic flags are not modeled. ``memoria`` is the flat interface of
``memoria_quadro_core.MemoriaQuadro`` (``u8/u16/u32``); the native stack is never written:
GetRessourceStock's outputs into CreerBatiment's frame are consumed as values.

Named dependencies (never defaulted). Every callee owned by another front goes through
``externo(nome, chamada, registradores) -> registradores``: ``chamada`` is the original call
address, ``registradores`` holds EAX..EBP and ESP at the callee entry and the provider returns
EAX..EBP as the callee leaves them, after making its stores. Without a provider the path raises
``DependenciaOrdemEconomia`` at that call, after the stores the original made before it:
- Core: EnginEstVivant 0x443dad, ResetOrdre 0x44357c, EnginAsk 0x440d5e (which hands
  PlaySnd_PostSound to Audio), BatimentGetDecalageConstruction 0x41aea4, DeplaceEngin 0x44930c,
  PlaceBatiment 0x41c4ac; ``provedor_core`` wires the first four to Core's committed
  ``selecao_ordens.SelecaoOrdens``;
- structure placement and gates: BatimentConstructible 0x41fb12, BatimentCollision 0x41ab5c,
  ResetCheminTerrainModify 0x41b78f.

Branches outside the translated domain raise ``ForaDoDominioOrdem`` at their original address
before any store: in CalculConstruireBatiment, gate/wall orders (+0xbe 9 or 12), the state-15
approach and the construction progress (+0x89 = 1); a CreerBatiment stock indicator with a zero
second divisor raises ZeroDivisionError at 0x41ffd0/0x42004e after the debit, as the original
faults there.
"""
M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
SELECOES = 0x508728                  # per player (stride 0x200): u16 count, u16 units from +2
JOGADOR_LOCAL = 0x508041
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
RECURSOS = 0x4e2ea8                  # player * 32 + resource * 8: u16 RMI +0, u16 total +2
INDICADOR = 0x4dfb2c                 # per player (stride 6): u16 divisor, u16 divisor, u8 level
ESTRUTURAS, MAX_ESTRUTURAS = 0x49a0c8, 1000
TIPOS_ESTRUTURA = 0x495d8c           # stride 52: u16 w, u16 h, +0xc food, +0xe stone, +0x10 parts, u8 +0x12 Bag capacity
ROTINAS = {
    'EnginTravailSelectionne': 0x47248f, 'SetMineEnginSelect': 0x473324, 'SetMineEngin': 0x444f48,
    'SetDepotEnginSelect': 0x47312c, 'SetDepotEngin': 0x444dad, 'SetRamasseEnginSelect': 0x473d2c,
    'SetRamasseEngin': 0x445947, 'TestRessource': 0x4676e5, 'GetRessourceStock': 0x46769d,
    'EnleveMatiere': 0x46792c, 'CreerBatiment': 0x41fea2, 'BagReset': 0x44710b, 'BagInit': 0x447148,
    'CalculConstruireBatiment': 0x44ab60,
}
PILHA_PALAVRAS = {'TestRessource': 1, 'GetRessourceStock': 1}       # RET 4: the player word


class DependenciaOrdemEconomia(NotImplementedError):
    """A callee owned by another front was reached without its provider."""
    def __init__(self, rotina, chamada, motivo='provider required'):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: {motivo}')


class ForaDoDominioOrdem(NotImplementedError):
    """A branch outside the translated and captured domain; nothing was written by it."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made')


def _baixo(v, b):
    return (v & 0xffffff00) | (b & 0xff)


def provedor_core(core, outros=None):
    """``externo`` that runs Core's translations (``selecao_ordens.SelecaoOrdens`` bound to the same
    memory) for EnginEstVivant, ResetOrdre, EnginAsk and BatimentGetDecalageConstruction and hands
    every other callee to ``outros`` (same signature), or raises."""
    from selecao_ordens import DECALAGEM

    def externo(nome, chamada, regs):
        r = {k: regs[k] & M32 for k in REG7}
        if nome == 'EnginEstVivant':
            core._vivo(r)
            return r
        if nome == 'ResetOrdre':
            return {k: v for k, v in core.reset_ordre(r).items() if k in REG7}
        if nome == 'EnginAsk':
            return {k: v for k, v in core.engin_ask(r).items() if k in REG7}
        if nome == 'BatimentGetDecalageConstruction':
            al = r['EAX'] & 0xff
            return dict(r, EAX=DECALAGEM[al] if al <= 0x15 else 0)
        if outros is None:
            raise DependenciaOrdemEconomia(nome, chamada, 'no provider for this front')
        return outros(nome, chamada, regs)
    return externo


class OrdensEconomia:
    """The routines over one live memory; ``externo`` is the only route to other fronts."""

    def __init__(self, memoria, *, externo=None):
        self.m = memoria
        self.externo = externo

    # ------------------------------------------------------------ helpers
    def _pool(self):
        return self.m.u32(PONTEIRO_UNIDADES)

    def _ext(self, nome, chamada, r, esp):
        """Call another front's routine; ``r['_incertos']`` ({register: mask}) marks bits the original
        leaves as uninitialized frame bytes there (passed on as ``_incertos``, never guessed)."""
        if self.externo is None:
            raise DependenciaOrdemEconomia(nome, chamada)
        entrada = dict({k: r[k] & M32 for k in REG7}, ESP=esp & M32)
        if r.get('_incertos'):
            entrada['_incertos'] = dict(r['_incertos'])
        saida = self.externo(nome, chamada, entrada)
        return {k: saida[k] & M32 for k in REG7}

    def _liberar_busca(self):
        self.m.u8(BUSCA_OCUPADA, 0)
        self.m.u8(BUSCA_SUCESSO, 0)
        self.m.u16(BUSCA_UNIDADE, 0xffff)
        self.m.u32(BUSCA_ROTA, 0)

    @staticmethod
    def _sair(regs, r, salvos, pop=0):
        """Exit registers: ``salvos`` restored from the entry, the rest from ``r``; ESP after RET ``pop``."""
        saida = {k: (regs[k] if k in salvos else r[k]) & M32 for k in REG7}
        saida['ESP'] = (regs['ESP'] + 4 + pop) & M32
        return saida

    # ------------------------------------------------------------ selection-wide queries and setters
    def engin_travail_selectionne(self, regs):
        """EnginTravailSelectionne 0x47248f: AL player, DL kind (0 parts: type 6; 1 food: type 5/13;
        2 stone: type 7). AL = 1 when every live unit of the player's selection list has the type and at
        least one does, 0 when one does not (it returns at once) or none counts; kinds above 2 never set
        it. EAX and DH change (DH = AL)."""
        r = dict(regs)
        jogador, esp = regs['EAX'] & 0xff, regs['ESP'] - 12
        r['EDX'] &= 0xffff00ff
        i = 0
        while (i & 0xffff) < self.m.u16(SELECOES + (jogador << 9)):
            u = self.m.u16(SELECOES + (jogador << 9) + 2 + 2 * (i & 0xffff))
            r.update(EAX=u, ECX=u, EBX=i)
            r = self._ext('EnginEstVivant', 0x4724f9, r, esp - 4)
            if r['EAX'] & 0xff:
                kind = r['EDX'] & 0xff
                if kind <= 2:
                    pool = self._pool()
                    tipo = self.m.u8((pool + u * PASSO + 1) & M32)
                    r.update(EAX=pool, ECX=tipo)
                    if tipo not in ((6,), (13, 5), (7,))[kind]:
                        r['EAX'] = pool & 0xffffff00
                        return self._sair(regs, r, ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))
                    r['EDX'] = (r['EDX'] & 0xffff00ff) | 0x100
                else:
                    r['ECX'] = u * PASSO & M32
            i += 1
        r['EAX'] = _baixo(r['EAX'], r['EDX'] >> 8)
        return self._sair(regs, r, ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    def _setter_com_voz(self, regs, chamada_vivo, chamada_voz, setter, dono_via_registro):
        """Shared loop of SetMineEnginSelect / SetRamasseEnginSelect: AL player, DX cell."""
        r = dict(regs)
        jogador, celula, esp = regs['EAX'] & 0xff, regs['EDX'] & 0xffff, regs['ESP'] - 24
        falou, slot = 0, 0
        while True:
            base = SELECOES + (jogador << 9)
            r['ECX'] = jogador << 9
            if (slot & 0xffff) >= self.m.u16(base):
                break
            u = self.m.u16(base + 2 + 2 * (slot & 0xffff))
            r.update(ECX=u, ESI=slot, EDI=falou)
            if dono_via_registro:            # SetMineEnginSelect: EDX = record before the liveness call
                r.update(EAX=u, EDX=(self._pool() + u * PASSO) & M32)
            else:
                r['EAX'] = u
            r = self._ext('EnginEstVivant', chamada_vivo, r, esp - 4)
            if not r['EAX'] & 0xff:
                slot += 1
                continue
            if dono_via_registro:
                dono = self.m.u8(r['EDX'])
                r['EAX'] = _baixo(r['EAX'], dono)
            else:
                pool = self._pool()
                dono = self.m.u8((pool + u * PASSO) & M32)
                r.update(EAX=_baixo(u * PASSO, dono), EDX=pool)
            if dono != jogador:
                slot += 1
                continue
            s = setter(dict(r, EAX=u, EDX=celula, ESP=esp - 4))
            r.update(EAX=s['EAX'], EDX=s['EDX'])
            if dono_via_registro:
                r['EDX'] = falou & 0xffff
            else:
                r['EAX'] = falou & 0xffff
            if (falou & 0xffff) >= 1:
                slot += 1
                continue
            local = self.m.u8(JOGADOR_LOCAL)
            r.update(EAX=_baixo(r['EAX'], jogador), EDX=_baixo(r['EDX'], local))
            falou += 1
            if jogador != local:
                slot += 1
                continue
            r.update(EDX=0xf, EAX=u, EBX=0, EDI=falou)
            r = self._ext('EnginAsk', chamada_voz, r, esp - 4)
            slot += 1
        return self._sair(regs, r, ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    def set_mine_engin_select(self, regs):
        """SetMineEnginSelect 0x473324: AL player, DX cell. Each live selected unit of that owner (any type)
        gets SetMineEngin; the first asks mode 0xf when the player is local. EAX and EDX change."""
        return self._setter_com_voz(regs, 0x473371, 0x4733b1, self.set_mine_engin, True)

    def set_ramasse_engin_select(self, regs):
        """SetRamasseEnginSelect 0x473d2c: AL player, DX cell. Each live selected unit of that owner (any type)
        gets SetRamasseEngin; the first asks mode 0xf when the player is local. EAX and EDX change."""
        return self._setter_com_voz(regs, 0x473d6b, 0x473db8, self.set_ramasse_engin,
                                    False)

    def set_depot_engin_select(self, regs):
        """SetDepotEnginSelect 0x47312c: AL player, DL byte, BX word, CL byte. Each live unit of the player's
        selection list, with no owner test and no voice, gets SetDepotEngin. EAX, EBX, ECX, EDX change."""
        r = dict(regs)
        jogador, esp = regs['EAX'] & 0xff, regs['ESP'] - 24
        dl, bx, cl = regs['EDX'] & 0xff, regs['EBX'] & 0xffff, regs['ECX'] & 0xff
        slot = 0
        while (slot & 0xffff) < self.m.u16(SELECOES + (jogador << 9)):
            u = self.m.u16(SELECOES + (jogador << 9) + 2 + 2 * (slot & 0xffff))
            r.update(EDX=u, ESI=u, EAX=u, EDI=slot)
            r = self._ext('EnginEstVivant', 0x47316a, r, esp - 4)
            if r['EAX'] & 0xff:
                r.update(EAX=u, ECX=cl, EBX=bx, EDX=dl)
                s = self.set_depot_engin(dict(r, ESP=esp - 4))
                r.update(EAX=s['EAX'], EDX=s['EDX'])
            slot += 1
        return self._sair(regs, r, ('ESI', 'EDI', 'EBP'))

    # ------------------------------------------------------------ single-unit setters
    def set_mine_engin(self, regs):
        """SetMineEngin 0x444f48: AX unit, DX mine cell. ResetOrdre; +0x7e = cell + 0x100; search released if
        owned; +0x88 = +0x89 = 0; state 5; +0x82 = 0; +0xb2 = cell with its row byte + 1. EAX = EDX = record."""
        u, cx = regs['EAX'] & 0xffff, regs['EDX']
        pool = self._pool()
        r = dict(regs, EBX=regs['EAX'], ECX=cx, ESI=u, EDI=u * 68, EDX=pool, EAX=u)
        r = self._ext('ResetOrdre', 0x444f67, r, regs['ESP'] - 20)
        desloc = u * PASSO
        rec_eax = (self._pool() + desloc) & M32
        self.m.u16(rec_eax + 0x7e, (cx + 0x100) & 0xffff)
        if regs['EAX'] & 0xffff == self.m.u16(BUSCA_UNIDADE):
            self._liberar_busca()
        rec_edx = (r['EDX'] + desloc) & M32
        self.m.u8(rec_eax + 0x88, 0)
        self.m.u8(rec_edx + 0x89, 0)
        self.m.u8(rec_edx + 2, 5)
        self.m.u8(rec_edx + 0x82, 0)
        self.m.u16(rec_edx + 0xb2, (cx & 0xff) | ((((cx >> 8) + 1) & 0xff) << 8))
        return self._sair(regs, dict(r, EAX=rec_eax, EDX=rec_edx), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    def set_ramasse_engin(self, regs):
        """SetRamasseEngin 0x445947: AX unit, DX cell. ResetOrdre; +0x7e = cell; search released if owned;
        +0x88 = 0; state 0x10; +0x89 = 0; +0xb2 = cell. EAX = EDX = record."""
        u, celula = regs['EAX'] & 0xffff, regs['EDX'] & 0xffff
        pool = self._pool()
        r = dict(regs, EBX=regs['EAX'], ESI=regs['EDX'], ECX=u, EDI=u * 68, EDX=pool, EAX=u)
        r = self._ext('ResetOrdre', 0x445966, r, regs['ESP'] - 20)
        desloc = u * PASSO
        rec_eax = (self._pool() + desloc) & M32
        self.m.u16(rec_eax + 0x7e, celula)
        if regs['EAX'] & 0xffff == self.m.u16(BUSCA_UNIDADE):
            self._liberar_busca()
        rec_edx = (r['EDX'] + desloc) & M32
        self.m.u8(rec_eax + 0x88, 0)
        self.m.u8(rec_edx + 2, 0x10)
        self.m.u8(rec_edx + 0x89, 0)
        self.m.u16(rec_edx + 0xb2, celula)
        return self._sair(regs, dict(r, EAX=rec_eax, EDX=rec_edx), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    def set_depot_engin(self, regs):
        """SetDepotEngin 0x444dad: AX unit, DL byte -> +0x82, BX word -> +0x80, CL -> u16 +0x84. EAX =
        (unit*276 & 0xffff0000) | CL; EDX = record."""
        u = regs['EAX'] & 0xffff
        desloc = u * PASSO
        rec = (self._pool() + desloc) & M32
        self.m.u8(rec + 0x82, regs['EDX'])
        self.m.u16(rec + 0x80, regs['EBX'])
        self.m.u16(rec + 0x84, regs['ECX'] & 0xff)
        return self._sair(regs, dict(regs, EAX=(desloc & 0xffff0000) | (regs['ECX'] & 0xff), EDX=rec),
                          ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    # ------------------------------------------------------------ resources
    def test_ressource(self, regs, pilha):
        """TestRessource 0x4676e5: AX food, DX stone, BX parts, player = low byte of the pushed word (RET 4).
        AL = 1 when each u16 cost is <= that total (food, stone, parts order; the same rule as
        ``quadro_economia.recursos_suficientes``); EAX upper bytes = (player << 5) upper bytes."""
        jogador = pilha[0] & 0xff
        base = RECURSOS + 32 * jogador
        ok = int(all(regs[r] & 0xffff <= self.m.u16(base + 8 * rid + 2)
                     for r, rid in (('EAX', 1), ('EDX', 2), ('EBX', 0))))
        return self._sair(regs, dict(regs, EAX=_baixo(jogador << 5, ok)), REG7[1:], pop=4)

    def get_ressource_stock(self, regs, pilha):
        """GetRessourceStock 0x46769d: EAX/EDX/EBX/ECX = addresses of four u16 outputs, player = pushed word
        (RET 4). Writes food, stone and parts stock (total - RMI, u16 wrap) and 0, in that order. EAX =
        player << 5; EDX = the last 32-bit subtraction (upper halves of the EDX/EAX/EDX pointers)."""
        p = (pilha[0] & 0xff) << 5
        pa, pb, pc, pd = regs['EAX'], regs['EDX'], regs['EBX'], regs['ECX']
        u = lambda o: self.m.u16(RECURSOS + p + o)
        self.m.u16(pa, u(0xa) - u(8))
        edx = (pb & 0xffff0000) | u(0x12)
        edx = (edx - ((pa & 0xffff0000) | u(0x10))) & M32
        self.m.u16(pb, edx)
        edx = (edx & 0xffff0000) | u(2)
        edx = (edx - ((pb & 0xffff0000) | u(0))) & M32
        self.m.u16(pc, edx)
        self.m.u16(pd, 0)
        return self._sair(regs, dict(regs, EAX=p, EDX=edx), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'), pop=4)

    def enleve_matiere(self, regs):
        """EnleveMatiere 0x46792c: AL resource, BX player, DX quantity. Total (+2) and then RMI (+0) of
        record (BX*4 + AL)*8 each lose DX, flooring at 0 (u16 compares). EAX = that offset; EBX = AL when
        the RMI floors, else the 32-bit RMI - EDX (EDI's upper half kept when the total floored)."""
        cl, bx, dx = regs['EAX'] & 0xff, regs['EBX'] & 0xffff, regs['EDX']
        o = ((bx * 4 + cl) * 8) & M32
        total = self.m.u16(RECURSOS + 2 + o)
        if dx & 0xffff > total:
            self.m.u16(RECURSOS + 2 + o, 0)
            edi = regs['EDI']
        else:
            edi = (total - dx) & M32
            self.m.u16(RECURSOS + 2 + o, edi)
        rmi = self.m.u16(RECURSOS + o)
        edi = (edi & 0xffff0000) | rmi
        if dx & 0xffff > rmi:
            self.m.u16(RECURSOS + o, 0)
            ebx = cl
        else:
            ebx = (edi - dx) & M32
            self.m.u16(RECURSOS + o, ebx)
        return self._sair(regs, dict(regs, EAX=o, EBX=ebx), ('ECX', 'EDX', 'ESI', 'EDI', 'EBP'))

    # ------------------------------------------------------------ Bags
    def _bag_limpar(self, bag):
        self.m.u16(bag, 0)
        self.m.u16(bag + 0x66, 0)
        self.m.u16(bag + 4, 0)
        self.m.u16(bag + 2, 0)
        for i in range(30):
            self.m.u16(bag + 6 + 2 * i, 0)
            self.m.u8(bag + 0x42 + i, 0)

    def bag_reset(self, regs):
        """BagReset 0x44710b: EAX = Bag. Clears count/+0x66/+4/capacity, 30 values and 30 tags. EAX = 30."""
        self._bag_limpar(regs['EAX'])
        return self._sair(regs, dict(regs, EAX=30), REG7[1:])

    def bag_init(self, regs):
        """BagInit 0x447148: EAX = Bag, EDX = capacity. As BagReset, then capacity (+2) = DX. EAX = entry EDX;
        EDX = 30."""
        self._bag_limpar(regs['EAX'])
        self.m.u16(regs['EAX'] + 2, regs['EDX'])
        return self._sair(regs, dict(regs, EAX=regs['EDX'], EDX=30), ('EBX', 'ECX', 'ESI', 'EDI', 'EBP'))

    # ------------------------------------------------------------ construction
    def _nivel(self, jogador6, jogador, chamada_div):
        """CreerBatiment's stock indicator recalculation: GetRessourceStock into the frame, level =
        ((food + stone stock) u16 // first word) * 7 // second word, low byte. Returns the stone stock."""
        p = jogador << 5
        u = lambda o: self.m.u16(RECURSOS + p + o)
        comida, pedra = (u(0xa) - u(8)) & 0xffff, (u(0x12) - u(0x10)) & 0xffff
        w1 = self.m.u16(INDICADOR + jogador6)
        q = ((comida + pedra) & 0xffff) // w1
        w2 = self.m.u16(INDICADOR + jogador6 + 2)
        if not w2:
            raise ZeroDivisionError(f'CreerBatiment: idiv by the zero indicator word 0x{INDICADOR + jogador6 + 2:x} '
                                    f'(0x{chamada_div:x}) after the debit')
        self.m.u8(INDICADOR + jogador6 + 4, (q * 7 // w2) & 0xff)
        return pedra

    def creer_batiment(self, regs):
        """CreerBatiment 0x41fea2: AX cell (32-bit EAX used), DL type, BL player. First free record of the
        1,000-record pool (+5 = 0); TestRessource(type food, type stone, parts 0); EnleveMatiere food then
        stone, each followed by the indicator recalculation when the player's first indicator word is
        nonzero; record +5 = 2, owner +4 = 0xc8 (type 17: the player), +2 = cell - ((h-1) << 8) - (w-1);
        type 12 resets a live type-9 record that BatimentCollision reports at that cell; +8 = type,
        +0xa = 1, +6 = 0; PlaceBatiment; BagReset(+0xc); types 9/12 owner = player; BagInit(+0xc, capacity).
        EAX = record index, or 0xffff when the pool is full or the stock is short (nothing written)."""
        esp_b = (regs['ESP'] - 0x68) & M32             # frame base after the prologue and push eax
        celula, tipo, jogador = regs['EAX'], regs['EDX'] & 0xff, regs['EBX'] & 0xff
        salvos = ('ECX', 'ESI', 'EDI', 'EBP')
        i = 0
        while (i & 0xffff) < MAX_ESTRUTURAS and self.m.u8(ESTRUTURAS + PASSO * (i & 0xffff) + 5):
            i += 1
        if (i & 0xffff) == MAX_ESTRUTURAS:
            return self._sair(regs, dict(regs, EAX=0xffff, EDX=0), salvos)
        t = TIPOS_ESTRUTURA + 52 * tipo
        comida, pedra = self.m.u16(t + 0xc), self.m.u16(t + 0xe)
        r = dict(regs, EAX=comida, EDX=pedra, EBX=0, ECX=0, EDI=jogador)
        teste = self.test_ressource(dict(r, ESP=esp_b - 8), [jogador])
        if not teste['EAX'] & 0xff:
            return self._sair(regs, dict(regs, EAX=0xffff, EBX=0, EDX=pedra), salvos)
        r = dict(teste)
        for rid, custo, chamada, divisao in ((1, comida, 0x41ff72, 0x41ffd0), (2, pedra, 0x41fff0, 0x42004e)):
            r.update(EAX=rid, EBX=jogador, EDX=custo, ESI=jogador * 4, EDI=jogador)
            r = self.enleve_matiere(dict(r, ESP=esp_b - 4))
            r['ESI'] = jogador * 6
            if self.m.u16(INDICADOR + jogador * 6):
                pedra_estoque = self._nivel(jogador * 6, jogador, divisao)
                if rid == 1:
                    r['ECX'] = (esp_b + 0x20) & M32
                else:
                    # 0x420022 reloads ECX as the dword at frame +0x30: its low half is the stone stock just
                    # written there, its upper half uninitialized frame bytes (no store reaches them).
                    r.update(ECX=pedra_estoque, EDI=self.m.u16(INDICADOR + jogador * 6),
                             _incertos={'ECX': 0xffff0000})
        w, h = self.m.u16(t), self.m.u16(t + 2)
        rec = ESTRUTURAS + PASSO * (i & 0xffff)
        self.m.u8(rec + 5, 2)
        self.m.u8(rec + 4, 0xc8)
        edx = (celula - ((((h - 1) & M32) << 8) + w - 1)) & M32
        self.m.u16(rec + 2, edx)
        if tipo == 0x11:
            self.m.u8(rec + 4, jogador)
        r.update(EBX=tipo, EDX=edx)
        if tipo == 12:
            r = self._varrer_portoes(r, rec, esp_b)
        self.m.u8(rec + 8, tipo)
        self.m.u16(rec + 0xa, 1)
        self.m.u16(rec + 6, 0)
        r.update(EAX=i & 0xffff, EBP=rec)
        r = self._ext('PlaceBatiment', 0x420274, r, esp_b - 4)
        self.bag_reset(dict(r, EAX=rec + 0xc, ESP=esp_b - 4))
        if tipo in (9, 12):
            self.m.u8(rec + 4, jogador)
        capacidade = self.m.u8(t + 0x12)
        self.bag_init(dict(r, EAX=rec + 0xc, EDX=capacidade, ESP=esp_b - 4))
        return self._sair(regs, dict(r, EAX=i, EDX=30), salvos)

    def _varrer_portoes(self, r, rec, esp_b):
        """CreerBatiment type 12 (0x4200da..0x420253): the first live type-9 record whose footprint holds the
        new origin and that BatimentCollision confirms is reset and handed to ResetCheminTerrainModify."""
        alvo = self.m.u16(rec + 2)
        encontrado = None
        j = 0
        while (j & 0xffff) < MAX_ESTRUTURAS:
            s = ESTRUTURAS + PASSO * (j & 0xffff)
            r['EDI'] = s
            if not self.m.u8(s + 5):
                r['EAX'] = 0
                j += 1
                continue
            t2 = self.m.u8(s + 8)
            r.update(EAX=t2, EDX=t2)
            if t2 != 9:
                j += 1
                continue
            r['EDX'] = t2 * 52
            w2, h2 = self.m.u16(TIPOS_ESTRUTURA + t2 * 52), self.m.u16(TIPOS_ESTRUTURA + t2 * 52 + 2)
            origem = self.m.u16(s + 2)
            r.update(ESI=s, EDI=(s & 0xffff0000) | origem, EAX=h2, ECX=0, _incertos=None)
            achou = False
            while (r['ECX'] & 0xffff) < h2 and not achou:
                r['EBX'] = 0
                while (r['EBX'] & 0xffff) < w2:
                    cx, bx = r['ECX'] & 0xffff, r['EBX'] & 0xffff
                    r.update(EAX=(cx << 8) + (r['EDI'] & 0xffff) + bx, EDX=alvo)
                    if r['EAX'] == alvo:
                        r.update(EDX=(w2 * r['ECX'] + r['EBX']) & 0xffff, EAX=self.m.u8(r['ESI'] + 8))
                        r = self._ext('BatimentCollision', 0x42019a, r, esp_b - 4)
                        if r['EAX'] & 0xff:
                            achou = True
                            break
                    r['EBX'] = (r['EBX'] + 1) & M32
                if not achou:
                    r['ECX'] = (r['ECX'] + 1) & M32
            if achou:
                encontrado = j
                break
            r['EAX'] &= 0xffffff00
            j += 1
        if encontrado is None:
            r.update(EAX=0xffff, EDX=0xffff)
            return r
        g = ESTRUTURAS + PASSO * (encontrado & 0xffff)
        self.m.u8(g + 5, 0)
        self.m.u16(g + 0x78, 0xffff)
        self.m.u16(g + 0x7c, 0)
        self.m.u16(g + 0x7e, 0)
        self.m.u16(g + 0xa, 0)
        self.m.u16(g + 0x82, 0)
        self.m.u8(g, 0xff)
        for o in (0x74, 0x75, 0x76):
            self.m.u8(g + o, 0)
        self.m.u8(g + 0x7b, 0xff)
        self.m.u16(g + 0x80, 0)
        self.m.u32(g + 0x8c, 0)
        idx = encontrado & 0xffff
        r.update(EAX=idx, EBX=0, ECX=0, EDX=idx, ESI=0, EDI=0)
        return self._ext('ResetCheminTerrainModify', 0x420253, r, esp_b - 4)

    def calcul_construire_batiment(self, regs):
        """CalculConstruireBatiment 0x44ab60, one tick of unit AX. Only type 7 (the builder) acts, with
        +0x89 = 0 and state 11 (an order from SetEnginConstruitBatiment) for structure types other than
        9/12. Not at the target (+8 != +0x7e) or pushed (+0x86/+0x87 nonzero): DeplaceEngin. At it with
        +0xb2 moved: the order is abandoned (+0xbe = 0xff, +0xb2 = +0xc0 = 0xffff, +0x89 = 0, state 7,
        search released if owned, +0x88 = 0). At it: cell + BatimentGetDecalageConstruction(type) goes to
        BatimentConstructible; when it holds, CreerBatiment(cell, type, owner) -> +0xc0; success sets
        +0x89 = 1, +0x8b = 0x14, +0xa9 = +0xa4 = 0, +0x90 = 7 (type 17) or 3; failure sets state 7 and
        releases the search if owned. Only EAX changes."""
        u = regs['EAX'] & 0xffff
        esp_b = (regs['ESP'] - 28) & M32
        rec = (self._pool() + u * PASSO) & M32
        r = dict(regs, EDI=regs['EAX'], EDX=u, EBX=u * PASSO, ESI=rec)
        sair = lambda eax: self._sair(regs, dict(r, EAX=eax), REG7[1:])
        tipo_u = self.m.u8(rec + 1)
        if tipo_u != 7:
            return sair(tipo_u)
        progresso = self.m.u8(rec + 0x89)
        if progresso == 1:
            raise ForaDoDominioOrdem('CalculConstruireBatiment', 0x44b1c1, 'construction progress (+0x89 = 1)')
        if progresso:
            return sair(progresso)
        estado = self.m.u8(rec + 2)
        if estado != 0xb:
            if estado == 0xf:
                raise ForaDoDominioOrdem('CalculConstruireBatiment', 0x44b15d, 'state-15 approach')
            return sair(estado)
        tipo = self.m.u8(rec + 0xbe)
        if tipo in (9, 12):
            raise ForaDoDominioOrdem('CalculConstruireBatiment', 0x44abbf, f'gate/wall order (type {tipo})')
        posicao = self.m.u16(rec + 8)

        def deplace():
            s = self._ext('DeplaceEngin', 0x44accb, dict(r, EAX=u), esp_b - 4)
            return sair(s['EAX'])
        if self.m.u16(rec + 0x7e) != posicao:
            return deplace()
        if self.m.u8(rec + 0x86) or self.m.u8(rec + 0x87):
            return deplace()
        if posicao != self.m.u16(rec + 0xb2):
            return self._abandonar(regs, r, u, rec)
        if tipo == 0xff:
            return sair(0xff)
        d = self._ext('BatimentGetDecalageConstruction', 0x44ad30, dict(r, EAX=tipo), esp_b - 4)
        r.update(d)
        celula = (posicao + r['EAX']) & 0xffff
        r.update(EBP=u, ECX=celula, EAX=tipo, EBX=u, EDX=celula)
        c = self._ext('BatimentConstructible', 0x44ad5f, r, esp_b - 4)
        r.update(c, EDX=u, EBP=u * PASSO)
        if not r['EAX'] & 0xff:
            return sair(tipo)
        criado = self.creer_batiment(dict(r, EAX=r['ECX'], EBX=self.m.u8(rec), EDX=tipo, ESP=esp_b - 4))
        r.update({k: criado[k] for k in REG7})
        indice = r['EAX'] & 0xffff
        self.m.u16(rec + 0xc0, indice)
        if indice == 0xffff:
            # 0x44ae0c: inlined EnginEstVivant on the builder, then state 7 and the search release.
            estado = self.m.u8((self._pool() + u * PASSO + 2) & M32)
            if estado in (0, 4):
                return sair(0)
            self.m.u8((self._pool() + u * PASSO + 2) & M32, 7)
            if regs['EAX'] & 0xffff != self.m.u16(BUSCA_UNIDADE):
                return sair(u * 69)
            self._liberar_busca()
            return sair(0)
        self.m.u8(rec + 0x89, 1)
        self.m.u8(rec + 0x8b, 0x14)
        self.m.u8(rec + 0xa9, 0)
        self.m.u8(rec + 0xa4, 0)
        self.m.u8(rec + 0x90, 7 if tipo == 0x11 else 3)
        return sair(tipo)

    def _abandonar(self, regs, r, u, rec):
        """0x44b0ac: the order target moved; abandon and fall back to state 7 (inlined EnginEstVivant)."""
        self.m.u8(rec + 0xbe, 0xff)
        self.m.u16(rec + 0xb2, 0xffff)
        self.m.u16(rec + 0xc0, 0xffff)
        self.m.u8(rec + 0x89, 0)
        estado_end = (self._pool() + u * PASSO + 2) & M32
        eax = 0
        if self.m.u8(estado_end) not in (0, 4):
            self.m.u8(estado_end, 7)
            eax = u * 69
            if regs['EAX'] & 0xffff == self.m.u16(BUSCA_UNIDADE):
                self._liberar_busca()
                eax = 0xffff
        self.m.u8(rec + 0x88, 0)
        return self._sair(regs, dict(r, EAX=eax), REG7[1:])

    # ------------------------------------------------------------ dispatch by original name
    def chamar(self, nome, regs, pilha=()):
        """Run routine ``nome`` with entry registers ``regs`` (EAX..EBP and ESP) and its pushed words."""
        regs = {k: regs[k] & M32 for k in REG7 + ('ESP',)}
        if nome in PILHA_PALAVRAS:
            if len(pilha) != PILHA_PALAVRAS[nome]:
                raise ValueError(f'{nome} takes exactly {PILHA_PALAVRAS[nome]} pushed word')
            return {'TestRessource': self.test_ressource,
                    'GetRessourceStock': self.get_ressource_stock}[nome](regs, list(pilha))
        f = {
            'EnginTravailSelectionne': self.engin_travail_selectionne,
            'SetMineEnginSelect': self.set_mine_engin_select, 'SetMineEngin': self.set_mine_engin,
            'SetDepotEnginSelect': self.set_depot_engin_select, 'SetDepotEngin': self.set_depot_engin,
            'SetRamasseEnginSelect': self.set_ramasse_engin_select, 'SetRamasseEngin': self.set_ramasse_engin,
            'EnleveMatiere': self.enleve_matiere, 'CreerBatiment': self.creer_batiment,
            'BagReset': self.bag_reset, 'BagInit': self.bag_init,
            'CalculConstruireBatiment': self.calcul_construire_batiment,
        }.get(nome)
        if f is None:
            raise KeyError(f'{nome} is not a translated economy order routine')
        if pilha:
            raise ValueError(f'{nome} takes no pushed word')
        return f(regs)
