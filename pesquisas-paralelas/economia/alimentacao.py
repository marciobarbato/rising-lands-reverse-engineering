"""Hunger state over live original memory: unit state 19 (a starving unit walks to food and eats), M3 S1.

Translated from the intact bytes after the native capture
``evidencias/alimentacao/captura-alimentacao-exibicao.json.xz`` was committed. Routines:
- the state-19 body of EnginNextEtape, entry ``0x4554db`` (jump table ``0x4543c8`` entry 19), exit ``0x454ccd``
  (the common ``add esp, 0x64; jmp 0x44f29d``); 868 bytes over ``0x454c93..0x4567c9`` (``estado_fome``);
- TerrainRetireMatiere 0x476662 (one unit taken from the sack on a cell).

S1 runs this path: the Mac mini's S1 development run enters the state-19 body's TerrainRetireMatiere (return
0x4555ee) and EnginRestaureEtat first at frame 8057, after EnginSetFatigue at 7958.

Calling convention. ``EstadoFome`` (the body, recorded as ``EnginNextEtape:19``) takes the registers at its entry
EAX..EBP plus ESP: ESI = the unit record, DI = the unit; EBX, ECX and EBP are carried until a path overwrites them.
It returns EAX..EBP and ESP at the exit 0x454ccd (ESP unchanged). EnginNextEtape's own locals ``[esp + 0x24..0x48]``
written by the abort branches are not modeled (those branches are outside the translated domain). ``memoria``:
``u8/u16/u32(addr, value=None)`` (``memoria_quadro_core.MemoriaQuadro``).

Named dependencies (never defaulted), through ``externo(nome, chamada, registradores) -> registradores`` with the
whole register file EAX..EBP, the callee's entry ESP and ``_pilha`` (the pushed words); ``ARGUMENTOS`` names the
argument bits each callee reads (a provider may add ``_incertos``):
- Core: BatimentAdjacent, DeplaceEngin, BatimentGetType, BatimentGetPlayer, BatimentEnDestruction,
  TerrainGetSacType, TerrainEstDecouvert, EnginGetVolume;
- Economy: TestRessource (``ordens_economia``), BatimentEnleveMatiere 0x4235bd, EnginRestaureEtat 0x45315f
  (the saved-state restore; not translated yet);
- terrain search: ChercheVegetLibre 0x477b74;
- Audio: PlaySnd_PostSound (frame boundary; one pushed word, popped by the callee).

Outside the translated domain (``ForaDoDominioFome``, raised before any store of the branch): the validity checks of
saved states +0xa0 = 1, 0xb, 0xd, 0xf, 0x12, 0x15, 0x17, 0x18; the abort of saved state 5 when its depot structure
(mode 2) is destroyed or no longer the unit's owner's (0x455107); the aborts of saved state 0x14 (unloading) when its
unload structure +0xc0 (0x454ddd) or its mode-2 depot (0x454ef8) is destroyed or lost. Saved states 5 and 0x14 whose
structures stand go on to the meal.
"""
M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
JOGADOR_LOCAL = 0x508041
GRADE_OBJETOS, GRADE_TRABALHO = 0x507d74, 0x507dac
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
ROTINAS = {'EstadoFome': 0x4554db, 'TerrainRetireMatiere': 0x476662}
NOME_GRAVADO = {'EnginNextEtape:19': 'EstadoFome'}
INTERNAS = ()
ARGUMENTOS = {
    'BatimentAdjacent': {'EAX': 0xffff, 'EDX': 0xffff}, 'DeplaceEngin': {'EAX': 0xffff},
    'BatimentGetType': {'EAX': 0xffff}, 'BatimentGetPlayer': {'EAX': 0xffff},
    'BatimentEnDestruction': {'EAX': 0xffff}, 'TerrainGetSacType': {'EAX': 0xffff},
    'TerrainEstDecouvert': {'EAX': 0xffff, 'EDX': 0xff}, 'EnginGetVolume': {'EAX': 0xffff},
    'TestRessource': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xffff}, 'BatimentEnleveMatiere': {'EAX': 0xff,
    'EDX': 0xffff, 'EBX': 0xff}, 'EnginRestaureEtat': {'EAX': 0xffff},
    'ChercheVegetLibre': {'EAX': 0xffff, 'EDX': 0xff, 'EBX': 0xff, 'ECX': 0xff},
    'PlaySnd_PostSound': {'EAX': M32, 'EDX': M32, 'EBX': M32, 'ECX': M32},
}
PILHA_EXTERNA = {'TestRessource': 1, 'ChercheVegetLibre': 1, 'PlaySnd_PostSound': 1}
# Saved states +0xa0 with their own validity check before the meal (jump targets of 0x4554db..0x455553).
VERIFICACOES = {1: 0x455393, 5: 0x4550ce, 0xb: 0x454c93, 0xd: 0x4553b4, 0xf: 0x454cd5, 0x12: 0x454fad,
                0x14: 0x454db5, 0x15: 0x454c93, 0x17: 0x4551f6, 0x18: 0x455393}


class DependenciaFome(NotImplementedError):
    """A callee owned elsewhere was reached without its provider."""
    def __init__(self, rotina, chamada, motivo='provider required'):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: {motivo}')


class ForaDoDominioFome(NotImplementedError):
    """A branch outside the translated domain; nothing was written by it."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made by this branch')


def _sx8(b):
    return b - 0x100 if b & 0x80 else b


class Alimentacao:
    def __init__(self, memoria, *, externo=None, proprias=None):
        self.m = memoria
        self.externo = externo
        self.proprias = set(ROTINAS) if proprias is None else set(proprias)
        self.incertos = {}
        self._esp = 0

    def _ext(self, nome, chamada, r, pilha=()):
        """Call ``nome`` at ``chamada`` with the whole register file ``r`` (EAX..EBP) and the callee's entry ESP (the
        body's ESP minus the pushed words and the return address); returns EAX..EBP as the callee leaves them
        (registers a provider does not return keep the caller's values). ``ARGUMENTOS`` names the argument bits each
        callee reads (what the validators compare); every register is passed."""
        esp = (self._esp - 4 * len(pilha) - 4) & M32
        if nome in self.proprias and nome in ROTINAS:
            entrada = {k: r[k] & M32 for k in REG7}
            entrada['ESP'] = esp
            saida = getattr(self, '_' + nome)(entrada)
            return {k: saida[k] & M32 for k in REG7}
        if self.externo is None:
            raise DependenciaFome(nome, chamada)
        entrada = {k: r[k] & M32 for k in REG7}
        entrada['ESP'] = esp
        if pilha:
            entrada['_pilha'] = list(pilha)
        saida = self.externo(nome, chamada, entrada)
        for k, v in (saida.get('_incertos') or {}).items():
            self.incertos[k] = self.incertos.get(k, 0) | v
        return {k: saida[k] & M32 for k in REG7 if k in saida}

    def _chamar(self, r, nome, chamada, pilha=(), **regs):
        """``_ext`` over the register file ``r`` (dict EAX..EBP): the call's argument registers are set in ``r``
        first, the whole file is passed, then every register the callee returns replaces ``r``'s."""
        r.update({k: v & M32 for k, v in regs.items()})
        saida = self._ext(nome, chamada, r, pilha)
        for k in REG7:
            if k in saida:
                r[k] = saida[k]
        return r

    def _reg(self, u):
        return (self.m.u32(PONTEIRO_UNIDADES) + PASSO * (u & 0xffff)) & M32

    # ------------------------------------------------------------ TerrainRetireMatiere
    def _TerrainRetireMatiere(self, regs):
        """TerrainRetireMatiere 0x476662: AX cell. q = byte [[0x507dac] + cell]; when q != 0 it is decremented and
        DL = byte [[0x507d74] + cell] - 0x42 (the sack type), else DL = 0. Then when the byte is 0 the object byte
        becomes 0. EAX = AX with AL = DL; every other register is restored."""
        m = self.m
        c = regs['EAX'] & 0xffff
        q = (m.u32(GRADE_TRABALHO) + c) & M32
        dl = 0
        if m.u8(q):
            m.u8(q, m.u8(q) - 1)
            dl = (m.u8((m.u32(GRADE_OBJETOS) + c) & M32) - 0x42) & 0xff
        if not m.u8((m.u32(GRADE_TRABALHO) + c) & M32):
            m.u8((m.u32(GRADE_OBJETOS) + c) & M32, 0)
        saida = {k: regs[k] & M32 for k in REG7}
        saida['EAX'] = (c & 0xff00) | dl
        saida['ESP'] = (regs.get('ESP', 0) + 4) & M32
        return saida

    # ------------------------------------------------------------ the state-19 body
    def estado_fome(self, regs):
        """The state-19 body for DI = unit, ESI = its record (see ``_EstadoFome``)."""
        return self._EstadoFome(dict(regs))

    def _EstadoFome(self, regs):
        """EnginNextEtape state 19, 0x4554db -> 0x454ccd. ``a0`` = the saved state u16 +0xa0 (set by
        EnginSetFatigue). Saved states with a validity check (``VERIFICACOES``) run it first: state 5 (work) keeps
        eating unless its depot (mode +0x82 = 2, structure +0x80) is destroyed or another owner's. Then the meal
        0x455554: the food structure ``c2`` = u16 +0xc2 (0xffff: a sack at the destination +0x7e).
        - Not there yet (c2 = 0xffff and cell +8 != +0x7e; or c2 set and not BatimentAdjacent(c2, cell)), or
          byte +0x86 or +0x87 nonzero: DeplaceEngin(unit).
        - On a food sack (c2 = 0xffff, TerrainGetSacType(+0x7e) = 1): TerrainRetireMatiere(+0x7e), provisions +4 :=
          +0x76 and +0x74 := 0, the eating sound, EnginRestaureEtat(unit).
        - At an own cave (BatimentGetType(c2) = 3, BatimentGetPlayer(c2) = owner) with TestRessource(1 food):
          BatimentEnleveMatiere(food, 1, owner), the same refill and sound, EnginRestaureEtat(unit).
        - Otherwise ChercheVegetLibre(+0x7c, +0xbb, 0x43, push unit): a sack found -> state 19 again towards it
          (+0x7e, path search released when it is the unit's, +0x88 := 0) and the sound; none -> the hungry voice
          for the local player's unit while +0x74 = 1, then EnginRestaureEtat(unit).
        The sound: owner's cell discovered by the local player (TerrainEstDecouvert) -> EnginGetVolume(unit),
        +0xf9 := 0 and, when the handle +0x104 is -1, PlaySnd_PostSound(0x50, type << 16 [| 0xc00 for the hungry
        voice], rec + 0x104, 0, push volume)."""
        m = self.m
        self.incertos = {}
        r = {k: regs[k] & M32 for k in REG7}
        esp = regs.get('ESP', 0) & M32
        self._esp = esp
        esi = r['ESI']
        di = r['EDI'] & 0xffff
        a0 = m.u16(esi + 0xa0)
        r['EDX'] = (r['EDX'] & 0xffff0000) | a0
        r['EAX'] = r['EDX']
        if a0 in VERIFICACOES:
            if a0 == 5:
                self._verificar_trabalho(r, esi)
            elif a0 == 0x14:
                self._verificar_descarga(r, esi)
            else:
                raise ForaDoDominioFome('EstadoFome', VERIFICACOES[a0], f'saved state {a0:#x} validity check')
        self._refeicao(r, esi, di)
        saida = dict(r, ESP=esp)
        if self.incertos:
            saida['_incertos'] = dict(self.incertos)
        return saida

    def _verificar_trabalho(self, r, esi):
        """Saved state 5, 0x4550ce: depot mode +0x82 = 2 and its structure +0x80 destroyed or not the owner's -> the
        abort 0x455107 (outside the domain); otherwise on to the meal."""
        m = self.m
        r['EAX'] = m.u8(esi + 0x82)
        if r['EAX'] != 2:
            return
        self._chamar(r, 'BatimentEnDestruction', 0x4550e8, EAX=m.u16(esi + 0x80))
        if not r['EAX'] & 0xff:
            self._chamar(r, 'BatimentGetPlayer', 0x4550fa, EAX=m.u16(esi + 0x80))
            if r['EAX'] & 0xff == m.u8(esi):
                return
        raise ForaDoDominioFome('EstadoFome', 0x455107, 'saved state 5: its depot structure is destroyed or lost')

    def _verificar_descarga(self, r, esi):
        """Saved state 0x14 (unloading), 0x454db5: the unload structure +0xc0 destroyed or not the owner's -> the
        abort 0x454ddd (outside the domain); else, with depot mode +0x82 = 2, its structure +0x80 must also stand and
        be the owner's (else the abort 0x454ef8, outside the domain); then on to the meal."""
        m = self.m
        self._chamar(r, 'BatimentEnDestruction', 0x454dbe, EAX=m.u16(esi + 0xc0))
        if not r['EAX'] & 0xff:
            self._chamar(r, 'BatimentGetPlayer', 0x454dd0, EAX=m.u16(esi + 0xc0))
            if r['EAX'] & 0xff == m.u8(esi):
                r['EAX'] = m.u8(esi + 0x82)
                if r['EAX'] != 2:
                    return
                self._chamar(r, 'BatimentEnDestruction', 0x454ed9, EAX=m.u16(esi + 0x80))
                if not r['EAX'] & 0xff:
                    self._chamar(r, 'BatimentGetPlayer', 0x454eeb, EAX=m.u16(esi + 0x80))
                    if r['EAX'] & 0xff == m.u8(esi):
                        return
                raise ForaDoDominioFome('EstadoFome', 0x454ef8, 'saved state 0x14: its depot structure is lost')
        raise ForaDoDominioFome('EstadoFome', 0x454ddd, 'saved state 0x14: its unload structure is destroyed or lost')

    def _refeicao(self, r, esi, di):
        m = self.m
        c2 = m.u16(esi + 0xc2)
        r['EAX'] = c2
        chegou = True
        if c2 == 0xffff:
            r['EAX'] = m.u16(esi + 8)
            chegou = r['EAX'] == m.u16(esi + 0x7e)
        else:
            r['EDX'] = m.u16(esi + 8)
            self._chamar(r, 'BatimentAdjacent', 0x455584, EAX=c2, EDX=r['EDX'])
            chegou = bool(r['EAX'] & 0xff)
        if chegou:
            r['EAX'] = _sx8(m.u8(esi + 0x86)) & M32
            if not r['EAX']:
                r['EAX'] = _sx8(m.u8(esi + 0x87)) & M32
            chegou = not r['EAX']
        if not chegou:
            self._chamar(r, 'DeplaceEngin', 0x4555ac, EAX=di)
            return
        r['EAX'] = c2
        if c2 == 0xffff:
            self._chamar(r, 'TerrainGetSacType', 0x4555ce, EAX=m.u16(esi + 0x7e))
            r['EAX'] &= 0xff
            if r['EAX'] == 1:
                self._chamar(r, 'TerrainRetireMatiere', 0x4555e9, EAX=m.u16(esi + 0x7e), ECX=0)
                self._reabastecer(r, esi, di)
                return self._restaurar(r, di)
        if c2 != 0xffff:
            self._chamar(r, 'BatimentGetType', 0x455688, EAX=c2)
            r['EAX'] &= 0xff
            if r['EAX'] == 3:
                self._chamar(r, 'BatimentGetPlayer', 0x4556a4, EAX=c2)
                if r['EAX'] & 0xff == m.u8(esi):
                    dono = m.u8(esi)
                    self._chamar(r, 'TestRessource', 0x4556c1, pilha=(dono,), EAX=1, EDX=0, EBX=0, ECX=0)
                    if r['EAX'] & 0xff:
                        self._chamar(r, 'BatimentEnleveMatiere', 0x4556d7, EAX=1, EDX=1, EBX=m.u8(esi), ECX=0)
                        self._reabastecer(r, esi, di, cave=True)
                        return self._restaurar(r, di)
        self._procurar(r, esi, di)

    def _reabastecer(self, r, esi, di, cave=False):
        """0x4555ee / 0x4556dc: AX = +0x76, CX = DI, +4 := AX, +0x74 := 0, then the sound over unit ECX
        (+0x104 into EBP for the sack, ESI for the cave)."""
        m = self.m
        r['EAX'] = (r['EAX'] & 0xffff0000) | m.u16(esi + 0x76)
        r['ECX'] = (r['ECX'] & 0xffff0000) | di
        m.u16(esi + 4, r['EAX'] & 0xffff)
        m.u16(esi + 0x74, 0)
        chamadas = (0x455714, 0x455723, 0x455660) if cave else (0x455626, 0x455631, 0x455660)
        self._som(r, chamadas, 'ECX', 'ESI' if cave else 'EBP')

    def _som(self, r, chamadas, origem, destino, voz=0):
        """The sound over unit ``r[origem]``: EBX = its record, EDX = the local player, TerrainEstDecouvert(cell)
        -> EnginGetVolume(unit), ``r[destino]`` = +0x104, +0xf9 := 0 and, when it is -1, PlaySnd_PostSound(0x50,
        type << 16 | voz, rec + 0x104, 0, push volume). True when the sound was posted."""
        m = self.m
        r['EBX'] = (m.u32(PONTEIRO_UNIDADES) + r[origem] * PASSO) & M32
        r['EDX'] = m.u8(JOGADOR_LOCAL)
        r['EAX'] = m.u16(r['EBX'] + 8)
        self._chamar(r, 'TerrainEstDecouvert', chamadas[0], EAX=r['EAX'], EDX=r['EDX'])
        if not r['EAX'] & 0xff:
            return False
        self._chamar(r, 'EnginGetVolume', chamadas[1], EAX=r[origem])
        rec = r['EBX']
        r[destino] = m.u32(rec + 0x104)
        m.u8(rec + 0xf9, 0)
        if r[destino] != M32:
            return False
        volume = r['EAX']
        self._chamar(r, 'PlaySnd_PostSound', chamadas[2], pilha=(volume,), EAX=0x50,
                     EDX=(m.u8(rec + 1) << 16) | voz, EBX=(rec + 0x104) & M32, ECX=0)
        return True

    def _restaurar(self, r, di):
        """0x455665: EnginRestaureEtat(unit), then the exit."""
        self._chamar(r, 'EnginRestaureEtat', 0x45566a, EAX=di)

    def _procurar(self, r, esi, di):
        """0x45573d: ChercheVegetLibre(+0x7c, +0xbb, 0x43, push unit) and its two outcomes."""
        m = self.m
        r.update(ECX=0x43, EBP=di, EBX=0x43, EDX=m.u8(esi + 0xbb), EAX=m.u16(esi + 0x7c))
        self._chamar(r, 'ChercheVegetLibre', 0x455756, pilha=(di,), EAX=r['EAX'], EDX=r['EDX'], EBX=0x43, ECX=0x43)
        achado = r['EAX']
        r['ECX'] = achado & 0xffff
        r['EBX'] = achado
        r['EAX'] = (r['EBP'] * PASSO) & M32
        esi, di = r['ESI'], r['EDI'] & 0xffff
        if r['ECX'] != 0xffff:
            m.u8(esi + 2, 0x13)
            r['EDX'] = m.u32(PONTEIRO_UNIDADES)
            r['EAX'] = (r['EAX'] + r['EDX']) & M32
            m.u16(r['EAX'] + 0x7e, r['EBX'] & 0xffff)
            if di == m.u16(BUSCA_UNIDADE):
                r['ESI'] = 0xffff
                r['EBX'] &= 0xffffff00
                r['EDX'] = 0
                m.u8(BUSCA_OCUPADA, 0)
                m.u8(BUSCA_SUCESSO, 0)
                m.u32(BUSCA_ROTA, 0)
                m.u16(BUSCA_UNIDADE, 0xffff)
            r['ECX'] = di
            m.u8(r['EAX'] + 0x88, 0)
            self._som(r, (0x4557eb, 0x4557fa, 0x45582d), 'ECX', 'ECX')
            return
        r['EDX'] = (r['EDX'] & 0xffffff00) | m.u8(esi)
        if m.u8(esi) == m.u8(JOGADOR_LOCAL):
            r['EDX'] = m.u16(esi + 0x74)
            if r['EDX'] == 1:
                self._som(r, (0x45586a, 0x455879, 0x455660), 'EBP', 'EBP', voz=0xc00)
        self._restaurar(r, di)

    # ------------------------------------------------------------ entry point
    def chamar(self, nome, regs):
        """Run routine ``nome`` (``EstadoFome``, alias ``EnginNextEtape:19``, or ``TerrainRetireMatiere``)."""
        nome = NOME_GRAVADO.get(nome, nome)
        if nome not in ROTINAS:
            raise KeyError(f'{nome} is not a translated hunger routine')
        entrada = {k: regs[k] & M32 for k in REG7}
        entrada['ESP'] = regs.get('ESP', 0) & M32
        return getattr(self, '_' + nome)(entrada)


# Registers each served routine's behaviour depends on: a provider call without one raises ``ArgumentoNaoPassado``.
ARGUMENTOS_EXIGIDOS = {'EstadoFome': ('ESI', 'EDI', 'EDX'), 'TerrainRetireMatiere': ('EAX',)}


def provedor_fome(alimentacao, outros=None):
    """``externo(nome, chamada, registradores)`` serving TerrainRetireMatiere and the state-19 body to another module
    (Core's states 16/17, ai-runtime's dispatcher), in the shape of Core's providers: a register of
    ``ARGUMENTOS_EXIGIDOS`` that is missing raises ``ArgumentoNaoPassado`` before anything runs; any other missing
    register enters as 0 and, when the routine returns it unchanged, comes back in ``_incertos``. Other names go to
    ``outros`` or raise ``DependenciaFome``."""
    def externo(nome, chamada, regs):
        proprio = NOME_GRAVADO.get(nome, nome)
        if proprio not in ROTINAS:
            if outros is None:
                raise DependenciaFome(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        faltando = [k for k in ARGUMENTOS_EXIGIDOS[proprio] if k not in regs]
        if faltando:
            from entrada_estruturas import ArgumentoNaoPassado
            raise ArgumentoNaoPassado(nome, chamada, faltando)
        entrada = {k: regs.get(k, 0) & M32 for k in REG7}
        entrada['ESP'] = regs.get('ESP', 0) & M32
        saida = alimentacao.chamar(nome, entrada)
        resultado = {k: saida[k] & M32 for k in REG7}
        incertos = {k: M32 for k in REG7 if k not in regs and resultado[k] == entrada[k]}
        for k, v in (saida.get('_incertos') or {}).items():
            incertos[k] = incertos.get(k, 0) | v
        if incertos:
            resultado['_incertos'] = incertos
        return resultado
    return externo
