"""The hunger state's exits and the tag-19 unload order over live original memory, M3 S1.

Translated from the intact bytes after the native captures ``evidencias/restauracao/captura-restauracao-*.json.xz``
were committed. Routines:
- EnginRestaureEtat 0x45315f (1,947 bytes, exit through 0x45305a -> 0x44f29d -> 0x440d58): a fed unit goes back to
  the state it was in when hunger struck (saved state u16 +0xa0, written by EnginSetFatigue). Its only caller is the
  state-19 body (0x45566a); S1 enters it with saved state 5 (work) at frame 8057;
- BatimentEnleveMatiere 0x4235bd: a debit through EnleveMatiere, then the player's stock level byte (eating at a
  cave costs one food through it, 0x4556d7);
- SetDechargeCaveEnginSelect 0x473194 (ProcessInputGame tag 19, 0x45f085) and SetDechargeCaveEngin 0x444dee: every
  live unit of the player's selection is sent to unload at a structure (state 0x14); the first asks mode 0xf when the
  player is local;
- BatimentTailleGet 0x41a996 (structure type -> width/height words written to two addresses), inline in
  EnginRestaureEtat.
EnleveMatiere and GetRessourceStock are ``ordens_economia``'s translations run in-process; GetRessourceStock's four
outputs into BatimentEnleveMatiere's frame land in a local overlay (the native stack is never written).

Calling convention. Every routine takes EAX..EBP plus ESP (the address of its return slot) and returns EAX..EBP and
the ESP after its RET, exactly as the original leaves them (callee-saved registers restored; the registers it
clobbers carry the values it leaves). ``memoria``: ``u8/u16/u32(addr, value=None)``.

Named dependencies (never defaulted). Each callee owned by another front goes through
``externo(nome, chamada, registradores) -> registradores`` with the whole register file EAX..EBP and ESP at the
callee's entry (every register passed: Core's providers raise ``ArgumentoNaoPassado`` for a missing argument). The
provider returns EAX..EBP as the callee leaves them (a register it does not return keeps the caller's value), after
its stores, optionally with ``_incertos``:
- Core: ResetOrdre 0x44357c, BatimentGetCase 0x41aee2, SetDeplaceEngin 0x4457d3, SetEnginRentreBatiment 0x445b10,
  SetEnginConstruitBatiment 0x4454ce, BatimentGetDecalageConstruction 0x41aea4, EnginEstVivant 0x443dad,
  EnginAsk 0x440d5e;
- Combat: SetAttaqueEngin 0x445a36.

Supported domain: every branch of the four routines. BatimentEnleveMatiere raises ZeroDivisionError at 0x423635 when
the player's per-cave word is 0 while it has a cave (the original faults there), after the debit.
"""
from ordens_economia import OrdensEconomia

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
JOGADOR_LOCAL = 0x508041
SELECOES = 0x508728                  # per player (stride 0x200): u16 count, u16 units from +2
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
INDICADOR = 0x4dfb2c                 # per player (stride 6): u16 cave count, u16 per-cave word, u8 level
TIPOS_ESTRUTURA = 0x495d8c           # stride 52: u16 width, u16 height
ROTINAS = {'EnginRestaureEtat': 0x45315f, 'BatimentEnleveMatiere': 0x4235bd,
           'SetDechargeCaveEnginSelect': 0x473194, 'SetDechargeCaveEngin': 0x444dee}
INTERNAS = ('BatimentTailleGet', 'EnleveMatiere', 'GetRessourceStock')
EXTERNAS = {'ResetOrdre': 'core', 'BatimentGetCase': 'core', 'SetDeplaceEngin': 'core',
            'SetEnginRentreBatiment': 'core', 'SetEnginConstruitBatiment': 'core',
            'BatimentGetDecalageConstruction': 'core', 'EnginEstVivant': 'core', 'EnginAsk': 'core',
            'SetAttaqueEngin': 'combat'}
# Registers each routine's behaviour depends on: a provider call without one raises ``ArgumentoNaoPassado``.
ARGUMENTOS_EXIGIDOS = {'EnginRestaureEtat': ('EAX',), 'BatimentEnleveMatiere': ('EAX', 'EDX', 'EBX'),
                       'SetDechargeCaveEnginSelect': ('EAX', 'EDX'), 'SetDechargeCaveEngin': ('EAX', 'EDX')}


class DependenciaRestauracao(NotImplementedError):
    """A callee owned elsewhere was reached without its provider."""
    def __init__(self, rotina, chamada, motivo='provider required'):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: {motivo}')


def _w(v, w):
    return (v & 0xffff0000) | (w & 0xffff)


def _sar(v, n):
    v &= M32
    return ((v - (1 << 32) if v & 0x80000000 else v) >> n) & M32


class _Sobreposicao:
    """``memoria`` with a few addresses (a native frame's locals) kept in a local dict."""
    def __init__(self, m, enderecos):
        self.m = m
        self.locais = {a & M32: 0 for a in enderecos}

    def u8(self, a, v=None):
        a &= M32
        if a in self.locais:
            if v is None:
                return self.locais[a]
            self.locais[a] = v & 0xff
            return None
        return self.m.u8(a) if v is None else self.m.u8(a, v)

    def u16(self, a, v=None):
        if v is None:
            return self.u8(a) | self.u8(a + 1) << 8
        self.u8(a, v)
        self.u8(a + 1, v >> 8)

    def u32(self, a, v=None):
        if v is None:
            return self.u16(a) | self.u16(a + 2) << 16
        self.u16(a, v)
        self.u16(a + 2, v >> 16)


class Restauracao:
    """The routines over one live memory; ``externo`` is the only route to other fronts."""

    def __init__(self, memoria, *, externo=None):
        self.m = memoria
        self.externo = externo
        self.incertos = {}

    # ------------------------------------------------------------ helpers
    def _pool(self):
        return self.m.u32(PONTEIRO_UNIDADES)

    def _ext(self, nome, chamada, r, esp, pilha=()):
        """Call another front's routine with the register file ``r`` (EAX..EBP) and ESP = ``esp``; returns the
        register file after the call (registers the provider does not return keep their values)."""
        if self.externo is None:
            raise DependenciaRestauracao(nome, chamada)
        entrada = dict({k: r[k] & M32 for k in REG7}, ESP=esp & M32)
        if pilha:
            entrada['_pilha'] = list(pilha)
        saida = self.externo(nome, chamada, entrada)
        for k, v in (saida.get('_incertos') or {}).items():
            self.incertos[k] = self.incertos.get(k, 0) | v
        return {k: saida.get(k, r[k]) & M32 for k in REG7}

    @staticmethod
    def _sair(regs, r, salvos, pop=0):
        saida = {k: (regs[k] if k in salvos else r[k]) & M32 for k in REG7}
        saida['ESP'] = (regs['ESP'] + 4 + pop) & M32
        return saida

    def _liberar_busca(self):
        self.m.u8(BUSCA_OCUPADA, 0)
        self.m.u8(BUSCA_SUCESSO, 0)
        self.m.u32(BUSCA_ROTA, 0)
        self.m.u16(BUSCA_UNIDADE, 0xffff)

    def _dono_busca(self, v):
        return v & 0xffff == self.m.u16(BUSCA_UNIDADE)

    # ------------------------------------------------------------ EnginRestaureEtat
    def engin_restaure_etat(self, regs):
        """EnginRestaureEtat 0x45315f: AX unit. By the saved state ``a0`` = u16 +0xa0:
        - 1: SetAttaqueEngin(unit, DL = +0xb7, BX = +0xb8) (Combat);
        - 2, 3, 7: state 2 towards the saved target (+0x7e := +0xa2), the path search released when it is the
          unit's, +0x88 := 0;
        - 5 (work): ResetOrdre, then the work order again: +0x7e := +0xb2, the search released, +0x88 := 0,
          +0x89 := 0, state 5, +0x82 := 0, +0xb2 kept, and the depot tuple +0x80/+0x82/+0x84 saved before
          ResetOrdre put back (+0x85 := 0). A builder (type 7) computes the same cell through +0xb2 - 0x100 with
          its high byte incremented;
        - 0xb, 0xf: type 7 with a structure +0xc0: ResetOrdre, BatimentGetCase(+0xc0) -> +0x7e/+0xb2, state 0xf;
          type 7 without one: BatimentTailleGet/BatimentGetDecalageConstruction of type +0xbe, then
          SetEnginConstruitBatiment(unit, +0xbe, the origin cell); type 6: ResetOrdre, +0x7e/+0xb2 := the cell +0x7c
          of unit +0xc0, state 0xf; other types: nothing;
        - 0xd: a structure +0xc0: SetEnginRentreBatiment(unit, +0xc0); else a unit +0xb8: follow it (+0x7e := its
          cell, +0xc0 := 0xffff, state 0xd); else nothing;
        - 0x10: ResetOrdre, +0x7e := +0xb2, state 0x10;
        - 0x11: +0x82 := 2, +0x80 := +0x84, +0x84 := 0;
        - 0x12: state 0x12 towards +0xb2;
        - 0x14: state 0x14, BatimentGetCase(+0xc0) -> +0xb2/+0x7e, the depot tuple put back;
        - 0x18: ResetOrdre; a type-4 unit gets +0xf4 back and, with target mode +0xb7 = 5, or 1 on another unit,
          state 0x18 with +0x8a := 0 and the saved +0xb7/+0xb8;
        - every other value: SetDeplaceEngin(unit, +0x7c).
        Exit: every register but EAX restored; EAX as the branch leaves it."""
        m = self.m
        e = {k: regs[k] & M32 for k in REG7}
        esp = (regs['ESP'] - 0x40) & M32          # after 6 pushes and sub esp, 0x28
        loc = {}
        esi = e['EAX']
        si = esi & 0xffff
        ebx = si
        desloc = ebx * PASSO
        ebp = self._pool()
        rec = (desloc + ebp) & M32
        a0 = m.u16(rec + 0xa0)
        r = dict(EAX=_w(e['EAX'], a0), EBX=ebx, ECX=rec, EDX=desloc, ESI=esi, EDI=e['EDI'], EBP=ebp)
        self.incertos = {}
        if a0 == 1:
            r.update(EBX=m.u16(rec + 0xb8), EAX=si, EDX=m.u8(rec + 0xb7))
            r.update(self._ext('SetAttaqueEngin', 0x45349a, r, esp - 4))
        elif a0 in (2, 3, 7):
            r['EAX'] = self._estado2(rec, si, r)
        elif a0 == 5:
            self._estado5(rec, si, r, esp, loc)
        elif a0 in (0xb, 0xf):
            self._estado_construcao(rec, si, r, esp, loc)
        elif a0 == 0xd:
            self._estado_seguir(rec, si, r, esp)
        elif a0 == 0x10:
            self._estado10(rec, r, esp)
        elif a0 == 0x11:
            m.u8(rec + 0x82, 2)
            w = m.u16(rec + 0x84)
            r['EAX'] = _w(r['EAX'], w)
            m.u16(rec + 0x84, 0)
            m.u16(rec + 0x80, w)
        elif a0 == 0x12:
            m.u8(rec + 2, 0x12)
            w = m.u16(rec + 0xb2)
            r['EAX'] = _w(r['EAX'], w)
            m.u8(rec + 0x89, 0)
            m.u16(rec + 0xb2, w)
            alvo = (desloc + self._pool()) & M32
            m.u16(alvo + 0x7e, w)
            if self._dono_busca(si):
                r['EAX'] = 0xffff
                self._liberar_busca()
            m.u8(alvo + 0x88, 0)
        elif a0 == 0x14:
            self._estado14(rec, si, r, esp, loc)
        elif a0 == 0x18:
            self._estado18(rec, r, esp)
        else:
            r.update(EAX=si, EDX=m.u16(rec + 0x7c))
            r.update(self._ext('SetDeplaceEngin', 0x4538f0, r, esp - 4))
        saida = self._sair(regs, r, REG7[1:])
        if self.incertos:
            saida['_incertos'] = dict(self.incertos)
        return saida

    def _estado2(self, rec, si, r):
        """0x453232: state 2 towards the saved target +0xa2. Returns EAX (the record)."""
        m = self.m
        m.u8(rec + 2, 2)
        alvo = (self._pool() + si * PASSO) & M32
        m.u16(alvo + 0x7e, m.u16(rec + 0xa2))
        if self._dono_busca(si):
            self._liberar_busca()
        m.u8(alvo + 0x88, 0)
        return alvo

    def _estado5(self, rec, si, r, esp, loc):
        """0x4535ea: saved state 5 (work)."""
        m = self.m
        b82 = m.u8(rec + 0x82)
        loc[0] = _w(_w(r['EAX'], (r['EAX'] & 0xff00) | b82), m.u16(rec + 0x80))
        b84 = m.u8(rec + 0x84)
        construtor = m.u8(rec + 1) == 7
        edi = _w(r['EDI'], m.u16(rec + 0xb2))
        if construtor:
            edi = (edi - 0x100) & M32
        r.update(EAX=si, ECX=si * 69, EDI=edi)
        r.update(self._ext('ResetOrdre', 0x453639 if construtor else 0x4536d4, r, esp - 4))
        if construtor:
            ah = ((r['EDI'] >> 8) + 1) & 0xff
            celula = (r['EDI'] & 0xffff00ff) | (ah << 8)
        else:
            celula = r['EDI']
        edx = ((r['ECX'] << 2) + r['EBP']) & M32
        sir = r['ESI'] & 0xffff
        alvo = (self._pool() + sir * PASSO) & M32
        m.u16(alvo + 0x7e, celula)
        if self._dono_busca(r['ESI']):
            self._liberar_busca()
        m.u8(alvo + 0x88, 0)
        m.u8(edx + 0x89, 0)
        m.u8(edx + 2, 5)
        di = ((r['EDI'] + 0x100) if construtor else r['EDI']) & 0xffff
        m.u8(edx + 0x82, 0)
        m.u16(edx + 0xb2, di)
        rr = (self._pool() + sir * PASSO) & M32
        m.u16(rr + 0x80, loc[0])
        m.u8(rr + 0x82, b82)
        m.u16(rr + 0x84, b84)
        r['EAX'] = (loc[0] & 0xffff0000) | b84

    def _estado_construcao(self, rec, si, r, esp, loc):
        """0x453293: saved states 0xb and 0xf."""
        m = self.m
        tipo = m.u8(rec + 1)
        r['EAX'] = tipo
        if tipo == 7:
            c0 = m.u16(rec + 0xc0)
            r['EAX'] = c0
            if c0 != 0xffff:
                ecx = self._pool()
                r.update(EDX=si, ECX=ecx, EBX=c0, EAX=si, EDI=si)
                r.update(self._ext('ResetOrdre', 0x4532c6, r, esp - 4))
                edi = ((((r['EDI'] << 4) + r['EDX']) & M32) << 2) & M32
                r.update(EAX=r['EBX'] & 0xffff, EDI=edi)
                r.update(self._ext('BatimentGetCase', 0x4532d8, r, esp - 4))
                edi = ((r['EDI'] + r['EDX']) << 2) & M32
                loc[0xc] = r['EAX']
                alvo = (self._pool() + edi) & M32
                m.u16(alvo + 0x7e, r['EAX'])
                ecx = (r['ECX'] + edi) & M32
                if self._dono_busca(r['ESI']):
                    self._liberar_busca()
                m.u8(alvo + 0x88, 0)
                m.u8(ecx + 0x88, 0)
                m.u8(ecx + 0x89, 0)
                m.u8(ecx + 2, 0xf)
                m.u16(ecx + 0xc0, r['EBX'])
                m.u16(ecx + 0xb2, loc[0xc])
                r['EAX'] = loc[0xc]
                return
            # 0x453350: a new structure of type +0xbe at the saved cell
            be = m.u8(rec + 0xbe)
            larg, alt = self._batiment_taille_get(be)
            loc[4], loc[8] = larg, alt
            edi = _w(r['EDI'], m.u16(rec + 0xb2))
            r.update(EAX=be, EBX=0, EDX=(esp + 8) & M32, EDI=edi)
            r.update(self._ext('BatimentGetDecalageConstruction', 0x453376, r, esp - 4))
            ebx = _w(r['EBX'], loc[8])
            edi = (r['EDI'] + r['EAX']) & M32
            eax = _sar((ebx - _sar(ebx, 31)) & M32, 1)
            ebp = (ebx - eax) & M32
            ebx = loc[4]
            eax = _sar((ebx - _sar(ebx, 31)) & M32, 1)
            ebp = ((ebp << 8) - 0x100) & M32
            ebx = (ebx - eax - 1 + ebp) & M32
            edi = (edi - ebx) & M32
            r.update(EAX=r['ESI'] & 0xffff, EBX=edi & 0xffff, EDX=be, EDI=edi, EBP=ebp)
            r.update(self._ext('SetEnginConstruitBatiment', 0x4533c5, r, esp - 4))
            return
        if tipo != 6:
            return
        # 0x4533d8: type 6 follows unit +0xc0
        c0 = m.u16(rec + 0xc0)
        loc[0x10] = c0
        edi = si * 69
        r.update(EAX=si, EDI=edi, EDX=self._pool())
        r.update(self._ext('ResetOrdre', 0x4533fa, r, esp - 4))
        pool = self._pool()
        edi = (r['EDI'] << 2) & M32
        ebx = _w(r['EBX'], m.u16((pool + c0 * 69 * 4 + 0x7c) & M32))
        alvo = (pool + edi) & M32
        m.u16(alvo + 0x7e, ebx)
        edx = (r['EDX'] + edi) & M32
        if self._dono_busca(r['ESI']):
            self._liberar_busca()
        m.u8(alvo + 0x88, 0)
        m.u8(edx + 0x88, 0)
        m.u8(edx + 0x89, 0)
        m.u8(edx + 2, 0xf)
        m.u16(edx + 0xb2, ebx)
        m.u16(edx + 0xc0, c0)
        r['EAX'] = c0

    def _batiment_taille_get(self, tipo):
        """BatimentTailleGet 0x41a996 (inline): BL type -> the words +0 and +2 of its 52-byte record."""
        base = TIPOS_ESTRUTURA + (tipo & 0xff) * 52
        return self.m.u16(base), self.m.u16(base + 2)

    def _estado_seguir(self, rec, si, r, esp):
        """0x45378c: saved state 0xd."""
        m = self.m
        c0 = m.u16(rec + 0xc0)
        r['EAX'] = c0
        if c0 != 0xffff:
            r.update(EDX=c0, EAX=r['EBX'])
            r.update(self._ext('SetEnginRentreBatiment', 0x4537a0, r, esp - 4))
            return
        b8 = m.u16(rec + 0xb8)
        r['EAX'] = b8
        if b8 == 0xffff:
            return
        m.u16(rec + 0x7e, m.u16((r['EBP'] + b8 * PASSO + 8) & M32))
        if self._dono_busca(si):
            self._liberar_busca()
        m.u8(rec + 0x88, 0)
        m.u16(rec + 0xc0, 0xffff)
        m.u8(rec + 2, 0xd)
        m.u16(rec + 0xb8, b8)
        r['EAX'] = rec

    def _estado10(self, rec, r, esp):
        """0x45384b: saved state 0x10."""
        m = self.m
        di = m.u16(rec + 0xb2)
        r.update(EAX=r['EBX'], EDI=_w(r['EDI'], di))
        r.update(self._ext('ResetOrdre', 0x453854, r, esp - 4))
        pool = self._pool()
        edx = (r['EDX'] + pool) & M32
        m.u16(edx + 0x7e, r['EDI'])
        eax = pool
        if self._dono_busca(r['ESI']):
            eax &= 0xffffff00
            self._liberar_busca()
        m.u8(edx + 0x88, 0)
        m.u8(r['ECX'] + 2, 0x10)
        m.u8(r['ECX'] + 0x89, 0)
        m.u16(r['ECX'] + 0xb2, r['EDI'])
        r['EAX'] = eax

    def _estado14(self, rec, si, r, esp, loc):
        """0x453522: saved state 0x14 (unloading at a structure)."""
        m = self.m
        loc[0x1c] = m.u8(rec + 0x82)
        edi = _w(r['EDI'], m.u16(rec + 0x80))
        loc[0x24] = m.u8(rec + 0x84)
        c0 = m.u16(rec + 0xc0)
        m.u8(rec + 2, 0x14)
        m.u8(rec + 0x89, 0)
        r.update(EBX=_w(r['EBX'], c0), EAX=c0, EDI=edi)
        r.update(self._ext('BatimentGetCase', 0x453554, r, esp - 4))
        ecx = r['ECX']
        m.u16(ecx + 0xb2, r['EAX'])
        m.u16(ecx + 0xc0, r['EBX'])
        edx = (r['EDX'] + self._pool()) & M32
        m.u16(edx + 0x7e, m.u16(ecx + 0xb2))
        if self._dono_busca(r['ESI']):
            self._liberar_busca()
        m.u8(edx + 0x88, 0)
        sir = r['ESI'] & 0xffff
        rr = (self._pool() + sir * PASSO) & M32
        m.u8(rr + 0x82, loc[0x1c])
        m.u16(rr + 0x80, r['EDI'])
        m.u16(rr + 0x84, loc[0x24])
        r['EAX'] = ((sir * PASSO) & 0xffff0000) | loc[0x24]

    def _estado18(self, rec, r, esp):
        """0x4531c8: saved state 0x18."""
        m = self.m
        dh, di, dl = m.u8(rec + 0xf4), m.u16(rec + 0xb8), m.u8(rec + 0xb7)
        r.update(EAX=r['EBX'], EDX=(r['EDX'] & 0xffff0000) | dh << 8 | dl, EDI=_w(r['EDI'], di))
        r.update(self._ext('ResetOrdre', 0x4531dd, r, esp - 4))
        ecx = r['ECX']
        tipo = m.u8(ecx + 1)
        r['EAX'] = tipo
        if tipo != 4:
            return
        m.u8(ecx + 0xf4, r['EDX'] >> 8)
        dl = r['EDX'] & 0xff
        if dl == 1 and (r['ESI'] & 0xffff) == (r['EDI'] & 0xffff):
            return
        if dl in (1, 5):
            m.u8(ecx + 2, 0x18)
            m.u8(ecx + 0x8a, 0)
            m.u8(ecx + 0xb7, dl)
            m.u16(ecx + 0xb8, r['EDI'])

    # ------------------------------------------------------------ BatimentEnleveMatiere
    def batiment_enleve_matiere(self, regs):
        """BatimentEnleveMatiere 0x4235bd: AL resource, DX quantity, BL player. EnleveMatiere(AL, DX, BL), then, when
        the player's cave count u16 0x4dfb2c + 6p is nonzero, its level byte +4 := ((food + stone stock) low word //
        count) * 7 // the per-cave word +2 (GetRessourceStock into the frame). Exit: ECX, ESI, EDI, EBP restored;
        EAX/EBX/EDX as left: with no cave EAX = 0 and EnleveMatiere's EBX/EDX, else EAX = the level, EBX = the
        per-cave word and EDX = the remainder."""
        m = self.m
        esp = (regs['ESP'] - 0x18) & M32
        cl = regs['EBX'] & 0xff
        r = {k: regs[k] & M32 for k in REG7}
        r.update(ECX=cl, EDX=regs['EDX'] & 0xffff, EAX=regs['EAX'] & 0xff, ESI=cl << 2, EBX=cl)
        ordens = OrdensEconomia(m)
        s = ordens.chamar('EnleveMatiere', dict(r, ESP=esp - 4))
        r = {k: s[k] for k in REG7}
        esi = ((r['ESI'] - r['ECX']) * 2) & M32
        contagem = m.u16((esi + INDICADOR) & M32)
        r.update(EAX=contagem, ESI=esi)
        if contagem:
            ordens_locais = OrdensEconomia(_Sobreposicao(m, [esp + i for i in range(16)]))
            entrada = dict(r, EAX=esp, EDX=(esp + 4) & M32, EBX=(esp + 0xc) & M32, ECX=(esp + 8) & M32,
                           ESP=(esp - 8) & M32)
            s = ordens_locais.chamar('GetRessourceStock', entrada, pilha=(r['ECX'],))
            locais = ordens_locais.m
            soma = (locais.u16(esp) + locais.u16(esp + 4)) & 0xffff
            q = soma // m.u16((esi + INDICADOR) & M32)
            eax = q * 7
            por_cave = m.u16((esi + INDICADOR + 2) & M32)
            if not por_cave:
                raise ZeroDivisionError('BatimentEnleveMatiere 0x423635: idiv by the per-cave word 0')
            r.update(EAX=eax // por_cave, EDX=eax % por_cave, EBX=por_cave)
            m.u8((esi + INDICADOR + 4) & M32, r['EAX'])
        return self._sair(regs, r, ('ECX', 'ESI', 'EDI', 'EBP'))

    # ------------------------------------------------------------ SetDechargeCaveEngin(Select)
    def set_decharge_cave_engin(self, regs):
        """SetDechargeCaveEngin 0x444dee: AX unit, DX structure. State 0x14, +0x89 := 0, +0xb2 :=
        BatimentGetCase(structure), +0xc0 := structure, +0x7e := +0xb2, the path search released when it is the
        unit's, +0x88 := 0. Exit: EBX/ECX/ESI restored; EAX = the record; EDX = 0 after the release, else
        +0xb2 in its low word."""
        m = self.m
        esp = (regs['ESP'] - 12) & M32
        r = {k: regs[k] & M32 for k in REG7}
        u = regs['EAX'] & 0xffff
        esi = u * PASSO
        pool = self._pool()
        r.update(ECX=regs['EAX'], EBX=regs['EDX'], ESI=esi, EDX=pool)
        m.u8(pool + esi + 2, 0x14)
        m.u8(pool + esi + 0x89, 0)
        r['EAX'] = regs['EDX'] & 0xffff
        r.update(self._ext('BatimentGetCase', 0x444e21, r, esp - 4))
        base = (r['EDX'] + r['ESI']) & M32
        m.u16(base + 0xb2, r['EAX'])
        m.u16(base + 0xc0, r['EBX'])
        rec = (self._pool() + r['ESI']) & M32
        edx = _w(r['EDX'], m.u16(base + 0xb2))
        m.u16(rec + 0x7e, edx)
        if self._dono_busca(r['ECX']):
            edx = 0
            self._liberar_busca()
        m.u8(rec + 0x88, 0)
        return self._sair(regs, dict(r, EAX=rec, EDX=edx), ('EBX', 'ECX', 'ESI'))

    def set_decharge_cave_engin_select(self, regs):
        """SetDechargeCaveEnginSelect 0x473194: AL player, DX structure. Each live unit of the player's selection
        list (no owner or type test) gets SetDechargeCaveEngin(unit, DX); the first one asks EnginAsk(unit, 0xf, 0)
        when the player is the local one. Exit: EBX/ECX/ESI/EDI restored; EAX/EDX as left."""
        m = self.m
        esp = (regs['ESP'] - 0x18) & M32
        r = {k: regs[k] & M32 for k in REG7}
        jogador, estrutura = regs['EAX'] & 0xff, regs['EDX'] & 0xffff
        r.update(EDI=0, ESI=0)
        while True:
            r['ECX'] = jogador << 9
            if (r['ESI'] & 0xffff) >= m.u16(SELECOES + r['ECX']):
                break
            u = m.u16(SELECOES + r['ECX'] + 2 + 2 * (r['ESI'] & 0xffff))
            r.update(EDX=u, ECX=u, EAX=u)
            r.update(self._ext('EnginEstVivant', 0x4731d3, r, esp - 4))
            if r['EAX'] & 0xff:
                r.update(EDX=estrutura, EAX=r['ECX'])
                s = self.set_decharge_cave_engin(dict(r, ESP=esp - 4))
                r = {k: s[k] for k in REG7}
                r['EDX'] = r['EDI'] & 0xffff
                if r['EDX'] < 1:
                    local = m.u8(JOGADOR_LOCAL)
                    r['EAX'] = (r['EAX'] & 0xffff0000) | local << 8 | jogador
                    r['EDI'] = (r['EDI'] + 1) & M32
                    if jogador == local:
                        r.update(EDX=0xf, EAX=r['ECX'], EBX=0)
                        r.update(self._ext('EnginAsk', 0x47320b, r, esp - 4))
            r['ESI'] = (r['ESI'] + 1) & M32
        return self._sair(regs, r, ('EBX', 'ECX', 'ESI', 'EDI'))

    # ------------------------------------------------------------ dispatch by original name
    def chamar(self, nome, regs):
        """Run routine ``nome`` with entry registers ``regs`` (EAX..EBP and ESP)."""
        f = {'EnginRestaureEtat': self.engin_restaure_etat, 'BatimentEnleveMatiere': self.batiment_enleve_matiere,
             'SetDechargeCaveEnginSelect': self.set_decharge_cave_engin_select,
             'SetDechargeCaveEngin': self.set_decharge_cave_engin}.get(nome)
        if f is None:
            raise KeyError(f'{nome} is not a translated restore/unload routine')
        self.incertos = {}
        saida = f({k: regs[k] & M32 for k in REG7 + ('ESP',)})
        if self.incertos and '_incertos' not in saida:
            saida['_incertos'] = dict(self.incertos)
        return saida


def provedor_restauracao(restauracao, outros=None):
    """``externo(nome, chamada, registradores) -> registradores`` serving EnginRestaureEtat (the state-19 body,
    0x45566a), BatimentEnleveMatiere (0x4556d7 and the other callers), SetDechargeCaveEnginSelect (ProcessInputGame
    tag 19, 0x45f085) and SetDechargeCaveEngin (V_SetNavetteCaveToCulture, 0x482120), in the shape of Core's
    providers. Input: the registers EAX..EBP (a register of ``ARGUMENTOS_EXIGIDOS`` that is missing raises
    ``ArgumentoNaoPassado`` before anything runs; any other missing register enters as 0 and, when the routine
    returns it unchanged, comes back in ``_incertos``) and optionally ``ESP``. Output: EAX..EBP after the stores,
    plus ``_incertos``. Other names go to ``outros`` or raise ``DependenciaRestauracao``."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise DependenciaRestauracao(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        faltando = [k for k in ARGUMENTOS_EXIGIDOS[nome] if k not in regs]
        if faltando:
            from entrada_estruturas import ArgumentoNaoPassado
            raise ArgumentoNaoPassado(nome, chamada, faltando)
        entrada = {k: regs.get(k, 0) & M32 for k in REG7}
        entrada['ESP'] = regs.get('ESP', 0) & M32
        saida = restauracao.chamar(nome, entrada)
        resultado = {k: saida[k] & M32 for k in REG7}
        incertos = {k: M32 for k in REG7 if k not in regs and resultado[k] == entrada[k]}
        for k, v in (saida.get('_incertos') or {}).items():
            incertos[k] = incertos.get(k, 0) | v
        if incertos:
            resultado['_incertos'] = incertos
        return resultado
    return externo
