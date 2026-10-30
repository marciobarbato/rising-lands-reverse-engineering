"""EnginNextEtape state 11 (the builder) and CalculConstruireBatiment's construction-progress branch.

Translated after the native capture ``evidencias/captura-construcao-teclas-ia.json`` (``51a7f46``) from the intact
bytes (state 11 ``0x4564ef``; CalculConstruireBatiment ``0x44b1c1..0x44b342`` and ``0x44b34a..0x44b575``; the
leaves below). Every routine takes the entry registers EAX..EBP and returns the exit registers as the original
leaves them; a register whose value comes from a callee that is not reconstructed here is ``None`` (never
guessed).

- **State 11** ``0x4564ef`` (EnginNextEtape's switch target for state 11, ESI = the record, DI = the unit): when
  +0x89 is set and BatimentEnDestruction(+0xc0) holds, SetDeplaceEngin(unit, +0x7e); otherwise
  CalculConstruireBatiment(unit). Both end at the epilogue ``0x454ccd``. ``proxima_etapa_entrada`` runs the
  pinned ``proxima_etapa_quadro.proxima_etapa_unidade`` (prelude and switch) and dispatches here when its switch
  stops at this state's target before any store of the state body; state 13 (``0x4558e4``, Core's physical entry)
  is dispatched to the provider ``EnginNextEtape:state13`` when one is bound, else stays the named stop.
- **CalculConstruireBatiment** ``0x44ab60`` is Economy's ``ordens_economia.OrdensEconomia`` (walk, creation,
  abandonment) with Core's committed callees (``selecao_ordens`` through ``provedor_core``; ``construcao_core``
  through ``provedor_construcao``: DeplaceEngin, BatimentConstructible, PlaceBatiment, BatimentCollision,
  ResetCheminTerrainModify). Its out-of-domain stop at ``0x44b1c1`` (``+0x89 = 1``, no store made) continues in
  ``progresso``:
  * facing +0x90 != +0x91: RotateEngin (Core), exit;
  * AnimConstruireBatiment; BatimentConstruit(+0xc0) with BatimentGetDegatEffectif = 0 -> the completion block
    ``0x44b34a``;
  * otherwise the countdown +0x8b (decremented when nonzero); at 0 with animation frame +0xa4 = 2: CalculDirCase
    (+8, +0x91), Random, ProjectileInit(0xf or 0x10 by the seed's bit 0, the neighbour cell twice, mode 0, five
    zero words) (Combat), then BatimentRepare when damaged else BatimentConstruction, +0x8b = 0x14, and for the
    local player's builder on a discovered cell the work sound (+0xf9 = 0; a free handle +0x104 posts 0x50 with
    code 0x25);
  * completion: a wall order (+0xbe = 9) with queued cells +0xd8 moves to the next cell (state 11 again);
    otherwise the local player's finish sound (code 0x12), +0xbe = 0xff, +0xb2 = 0xffff, a live builder goes to
    state 7, +0x7e = +0x7c, +0x88 = 0, and the path search [0x496304] is released when the builder owns it.
- Leaves: BatimentEnDestruction ``0x41a70b``, BatimentConstruit ``0x41c652``, BatimentGetDegatEffectif
  ``0x41a976``, BatimentRepare ``0x41cec4``, BatimentConstruction ``0x41cf59`` (+0xa += 2; the owner's sound
  0x42/0x25; at the type limit +5 = 5, +0xa = the limit, BatimentHabitable for type 0x11, SetMurAllentour for
  type 9, then BatimentModifyMap(structure, 1) (Core's ``minimapa_estruturas``)), AnimConstruireBatiment
  ``0x447e12`` (types 6, 7 and 14 while +0x89 = 1).

Named dependencies (``DependenciaIA`` at the original call, after the stores made before it): BatimentHabitable
(Economy), SetMurAllentour, Core's construction routines while ``construcao_core`` is not importable, and every
out-of-domain branch of Economy's CalculConstruireBatiment (state 15, wall/gate orders 9/12).
"""
from reinicio_ia import DependenciaIA

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
POOL, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
TIPOS_ESTRUTURA = 0x495d8c                 # stride 52; u16 +4 = construction limit
LOCAL = 0x508041
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
ESTADO_11, ESTADO_13, SAIDA = 0x4564ef, 0x4558e4, 0x454ccd
ESTADO_5 = 0x456600                     # EnginNextEtape's switch target for state 5 (work)
PROGRESSO = 0x44b1c1


def _baixo(v, b):
    return None if v is None else (v & 0xffffff00) | (b & 0xff)


def _idiv(a, b):
    a = a - (1 << 32) if a & 0x80000000 else a
    b = b - (1 << 32) if b & 0x80000000 else b
    if b == 0:
        raise ZeroDivisionError('idiv by zero: the original faults')
    q = abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1)
    return q & M32, (a - q * b) & M32


class ConstrucaoEntrada:
    """The routines over one live memory ``m``.

    ``externo(nome, sitio, regs) -> regs`` runs another front's routine ``nome`` called at ``sitio`` with the entry
    registers ``regs`` and returns its exit registers (``None`` for a value it does not reconstruct); it raises
    ``DependenciaIA`` for a routine it does not provide. ``economia`` runs Economy's CalculConstruireBatiment
    (``regs -> regs``, raising its own out-of-domain exception at 0x44b1c1, see ``calcul_construire_batiment``)."""

    def __init__(self, m, externo, economia=None):
        self.m, self.externo, self.economia = m, externo, economia

    def _rec(self, u):
        return (self.m.u32(POOL) + (u & 0xffff) * PASSO) & M32

    @staticmethod
    def _est(s):
        return ESTRUTURAS + (s & 0xffff) * PASSO

    def _x(self, nome, sitio, r, **mudancas):
        entrada = dict(r, **mudancas)
        saida = self.externo(nome, sitio, dict(entrada))
        return dict(entrada, **saida)

    # ------------------------------------------------------------ structure leaves
    def batiment_en_destruction(self, regs):
        """BatimentEnDestruction 0x41a70b (AX structure): EAX = (+5 == 3); EDX preserved."""
        return dict(regs, EAX=int(self.m.u8(self._est(regs['EAX']) + 5) == 3))

    def batiment_construit(self, regs):
        """BatimentConstruit 0x41c652 (AX): AL = (+0xa == the type's limit); EAX upper = 13 * type."""
        s = self._est(regs['EAX'])
        tipo = self.m.u8(s + 8)
        igual = self.m.u16(s + 0xa) == self.m.u16(TIPOS_ESTRUTURA + 4 + 52 * tipo)
        return dict(regs, EAX=((13 * tipo) & 0xffffff00) | int(igual))

    def batiment_get_degat_effectif(self, regs):
        """BatimentGetDegatEffectif 0x41a976 (AX): AX = +6, EAX upper = the record address's."""
        s = self._est(regs['EAX'])
        return dict(regs, EAX=(s & 0xffff0000) | self.m.u16(s + 6))

    def _som_estrutura(self, r, s, sitio_volume, sitio_som):
        """BatimentGetVolume, then a free handle +0x100 posts sound 0x42 (code 0x25) for the type."""
        v = self._x('BatimentGetVolume', sitio_volume, r, EAX=r['EBX'] & 0xffff)['EAX']
        r = dict(r, EAX=v)
        if self.m.u32(s + 0x100) != M32:
            return r
        return self._x('PlaySnd_PostSound', sitio_som, r, EAX=0x42,
                       EDX=(self.m.u8(s + 8) << 16) | 0x2500, EBX=s + 0x100, ECX=0, pilha=[v])

    def batiment_repare(self, regs):
        """BatimentRepare 0x41cec4 (AX): +6 -= 2 (floor 0); the local owner's sound."""
        s = self._est(regs['EAX'])
        d = self.m.u16(s + 6)
        self.m.u16(s + 6, d - 2 if d >= 2 else 0)
        idx = regs['EAX'] & 0xffff
        r = dict(regs, EBX=idx, EDX=s, EAX=((idx * PASSO) & 0xffffff00) | self.m.u8(s + 4))
        if self.m.u8(s + 4) == self.m.u8(LOCAL):
            r = self._som_estrutura(r, s, 0x41cf25, 0x41cf50)
        return dict(regs, EAX=r['EAX'])

    def batiment_construction(self, regs):
        """BatimentConstruction 0x41cf59 (AX): progress +0xa += 2; at the type limit the structure is built."""
        m = self.m
        s = self._est(regs['EAX'])
        idx = regs['EAX'] & 0xffff
        m.u16(s + 0xa, m.u16(s + 0xa) + 2)
        r = dict(regs, EDI=regs['EAX'], EBX=idx, ESI=s)
        if m.u8(s + 4) == m.u8(LOCAL):
            r = self._som_estrutura(r, s, 0x41cf93, 0x41cfbc)
        tipo = m.u8(s + 8)
        limite = m.u16(TIPOS_ESTRUTURA + 4 + 52 * tipo)
        eax = 52 * tipo
        if m.u16(s + 0xa) >= limite:
            m.u8(s + 5, 5)
            m.u16(s + 0xa, limite)
            if tipo == 0x11:
                self._x('BatimentHabitable', 0x41d000, r, EAX=idx)
            elif tipo == 9:
                self._x('SetMurAllentour', 0x41d012, r, EAX=m.u16(s + 2))
            eax = self._x('BatimentModifyMap', 0x41d021, r, EAX=idx, EDX=1)['EAX']
        return dict(regs, EAX=eax)

    def anim_construire_batiment(self, regs):
        """AnimConstruireBatiment 0x447e12 (AX unit): while +0x89 = 1, types 7, 6 and 14 advance +0xa9 by 1; at its
        period (+0xa7, +0xa7 and +0xa8) +0xa9 = 0 and +0xa4 = (+0xa4 + 1) mod the frame count (+0xa5, 4, +0xa6)."""
        m = self.m
        rec = self._rec(regs['EAX'])
        tipo = m.u8(rec + 1)
        eax = regs['EAX']
        if tipo not in (6, 7, 0xe) or m.u8(rec + 0x89) != 1:
            return dict(regs, EAX=eax)
        periodo, quadros = {7: (0xa7, m.u8(rec + 0xa5)), 6: (0xa7, 4), 0xe: (0xa8, m.u8(rec + 0xa6))}[tipo]
        a9 = (m.u8(rec + 0xa9) + 1) & 0xff
        m.u8(rec + 0xa9, a9)
        if tipo != 7:                               # 0x447eb0/0x447ee7: the period byte goes through AH
            eax = (eax & 0xffff00ff) | (m.u8(rec + periodo) << 8 if tipo == 6 else a9 << 8)
        if a9 != m.u8(rec + periodo):
            return dict(regs, EAX=eax)
        q, resto = _idiv(m.u8(rec + 0xa4) + 1, quadros)
        m.u8(rec + 0xa9, 0)
        m.u8(rec + 0xa4, resto)
        return dict(regs, EAX=q)

    # ------------------------------------------------------------ CalculConstruireBatiment
    def calcul_construire_batiment(self, regs):
        """CalculConstruireBatiment 0x44ab60 (AX unit): Economy's routine, continued here at its 0x44b1c1 stop."""
        if self.economia is None:
            raise DependenciaIA('CalculConstruireBatiment (Economy ordens_economia)', 0x44ab60)
        try:
            return self.economia(regs)
        except NotImplementedError as erro:
            if getattr(erro, 'endereco', None) == PROGRESSO and getattr(erro, 'rotina', None) == \
                    'CalculConstruireBatiment':
                return self.progresso(regs)
            raise DependenciaIA(f'CalculConstruireBatiment (Economy): {erro}',
                                getattr(erro, 'endereco', None) or getattr(erro, 'chamada', None) or 0x44ab60) \
                from erro

    def progresso(self, regs):
        """0x44b1c1..0x44b342: the construction-progress tick of builder AX (+0x89 = 1)."""
        m = self.m
        u = regs['EAX'] & 0xffff
        rec = self._rec(u)
        r = dict(regs, EDI=regs['EAX'], EDX=u, EBX=u * PASSO, ESI=rec)
        sair = lambda eax: dict(regs, EAX=eax)                       # noqa: E731
        if m.u8(rec + 0x90) != m.u8(rec + 0x91):
            return sair(self._x('RotateEngin', 0x44b1d1, r, EAX=u)['EAX'])
        self.anim_construire_batiment(dict(r, EAX=u))
        s = m.u16(rec + 0xc0)
        if self.batiment_construit(dict(r, EAX=s))['EAX'] & 0xff:
            if not self.batiment_get_degat_effectif(dict(r, EAX=s))['EAX'] & 0xffff:
                return sair(self._conclusao(regs, u, rec))
        if m.u8(rec + 0x8b):
            m.u8(rec + 0x8b, m.u8(rec + 0x8b) - 1)
        if m.u8(rec + 0x8b):
            return sair(m.u8(rec + 0x8b))
        if m.u8(rec + 0xa4) != 2:
            return sair(m.u8(rec + 0xa4))
        vizinha = self._x('CalculDirCase', 0x44b24e, r, EAX=m.u16(rec + 8), EDX=m.u8(rec + 0x91))['EAX']
        semente = self._x('Random', 0x44b25a, r, EAX=0x17, EDX=vizinha)['EAX']
        n = vizinha & 0xffff
        self._x('ProjectileInit', 0x44b28d, r, EAX=0x10 if semente & 1 else 0xf, EDX=n, EBX=n, ECX=0,
                pilha=[0] * 5)
        s = m.u16(rec + 0xc0)
        if self.batiment_get_degat_effectif(dict(r, EAX=s))['EAX'] & 0xffff:
            eax = self.batiment_repare(dict(r, EAX=s))['EAX']
        else:
            eax = self.batiment_construction(dict(r, EAX=s))['EAX']
        m.u8(rec + 0x8b, 0x14)
        eax = _baixo(eax, m.u8(rec))
        if m.u8(rec) != m.u8(LOCAL):
            return sair(eax)
        return sair(self._som_construtor(r, u, rec, 0x44b300, 0x44b30b, 0x44b33d, 0x25))

    def _som_construtor(self, r, u, rec, sitio_terreno, sitio_volume, sitio_som, codigo):
        """TerrainEstDecouvert(+8, local); EnginGetVolume; +0xf9 = 0; a free handle +0x104 posts sound 0x50."""
        m = self.m
        t = self._x('TerrainEstDecouvert', sitio_terreno, r, EAX=m.u16(rec + 8), EDX=m.u8(LOCAL))
        if not t['EAX'] & 0xff:
            return t['EAX']
        v = self._x('EnginGetVolume', sitio_volume, r, EAX=u)['EAX']
        m.u8(rec + 0xf9, 0)
        if m.u32(rec + 0x104) != M32:
            return v
        return self._x('PlaySnd_PostSound', sitio_som, r, EAX=0x50, EDX=(m.u8(rec + 1) << 16) | (codigo << 8),
                       EBX=rec + 0x104, ECX=0, pilha=[v])['EAX']

    def _liberar_busca(self):
        self.m.u8(BUSCA_OCUPADA, 0)
        self.m.u32(BUSCA_ROTA, 0)
        self.m.u8(BUSCA_SUCESSO, 0)
        self.m.u16(BUSCA_UNIDADE, 0xffff)

    def _conclusao(self, regs, u, rec):
        """0x44b34a: the structure is built and undamaged. Returns the exit EAX."""
        m = self.m
        di = regs['EAX'] & 0xffff
        n = m.u16(rec + 0xd8)
        if m.u8(rec + 0xbe) == 9 and n:
            proxima = m.u16(rec + 0xc4)
            m.u16(rec + 0x7e, proxima)
            if di == m.u16(BUSCA_UNIDADE):
                self._liberar_busca()
            m.u8(rec + 0x88, 0)
            m.u8(rec + 0x89, 0)
            m.u16(rec + 0xc0, 0xffff)
            m.u8(rec + 2, 0xb)
            m.u16(rec + 0xb2, proxima)
            eax = rec
            for i in range(1, n):
                m.u16(rec + 0xc2 + 2 * i, m.u16(rec + 0xc4 + 2 * i))
                eax = i
            m.u16(rec + 0xd8, n - 1)
            return eax
        if m.u8(LOCAL) == m.u8(rec):
            self._som_construtor(dict(regs, EBX=rec, ECX=u), u, rec, 0x44b446, 0x44b451, 0x44b483, 0x12)
        m.u8(rec + 0xbe, 0xff)
        m.u16(rec + 0xb2, 0xffff)
        if m.u8(rec + 2) not in (0, 4):
            m.u8(rec + 2, 7)
            if di == m.u16(BUSCA_UNIDADE):
                self._liberar_busca()
        m.u16(rec + 0x7e, m.u16(rec + 0x7c))
        if di == m.u16(BUSCA_UNIDADE):
            self._liberar_busca()
        m.u8(rec + 0x88, 0)
        return rec

    # ------------------------------------------------------------ EnginNextEtape state 11
    def estado_11(self, u):
        """0x4564ef (DI unit, ESI its record): the destroyed-structure retreat or one CalculConstruireBatiment tick;
        then the epilogue 0x454ccd."""
        m = self.m
        rec = self._rec(u)
        r = dict.fromkeys(REG7, 0)
        r.update(EDI=u, ESI=rec)
        if m.u8(rec + 0x89) and self.batiment_en_destruction(dict(r, EAX=m.u16(rec + 0xc0)))['EAX'] & 0xff:
            self._x('SetDeplaceEngin', 0x454cc8, r, EAX=u, EDX=m.u16(rec + 0x7e))
            return SAIDA
        self.calcul_construire_batiment(dict(r, EAX=u))
        return SAIDA


def proxima_etapa_entrada(m, p, unidade, tabelas, construcao, etapa=None):
    """EnginNextEtape 0x45442c: the pinned prelude and switch (``proxima_etapa_quadro``), with state 11 run by
    ``construcao`` (a ``ConstrucaoEntrada``) and state 13 by the provider ``EnginNextEtape:state13`` when bound.
    The pinned switch stops at a state's target before the first store of its body (``_trocar_estado``), so the
    dispatch continues exactly there. ``etapa()`` (default: the pinned routine over ``m``/``p``) lets a composition
    keep its own wrapper of the pinned routine (e.g. its crossing check)."""
    from proxima_etapa_quadro import proxima_etapa_unidade
    try:
        return etapa() if etapa is not None else proxima_etapa_unidade(m, p, unidade, tabelas)
    except DependenciaIA as erro:
        if erro.rotina == 'EnginNextEtape state 11' and erro.sitio == ESTADO_11 == tabelas['estados'][11]:
            return construcao.estado_11(unidade & 0xffff)
        if erro.rotina == 'EnginNextEtape state 13' and erro.sitio == ESTADO_13 == tabelas['estados'][13] \
                and 'EnginNextEtape:state13' in p:
            p['EnginNextEtape:state13'](sitio=ESTADO_13, unidade=unidade & 0xffff)
            return SAIDA
        if erro.rotina == 'EnginNextEtape state 5' and erro.sitio == ESTADO_5 == tabelas['estados'][5] \
                and 'EnginNextEtape:state5' in p:
            p['EnginNextEtape:state5'](sitio=ESTADO_5, unidade=unidade & 0xffff)
            return SAIDA
        raise


def estado_trabalho(m, chamar, unidade):
    """EnginNextEtape's state-5 body 0x456600..0x456736 (ESI = the record, DI = the unit), from the intact bytes:

    - u8 +0x82 == 2 (the unit's work target is a structure, +0x80): BatimentEnDestruction(AX = +0x80) at
      0x45661a; when it returns 0, BatimentGetPlayer(AX = +0x80) at 0x45662c compared with the unit's owner
      byte +0. A destroyed or foreign structure takes the release branch 0x456639 (SetEnginCollision, discovery,
      0x4550a2), outside this translation: ``DependenciaIA`` at 0x456639 before any store.
    - otherwise (or an intact own structure): CalculWorkEngin(AX = unit, zero-extended) at 0x456731, then the
      exit 0x454ccd.

    ``chamar(nome, chamada, **regs) -> regs`` runs the owners' routines (Core's BatimentEnDestruction and
    BatimentGetPlayer, Economy's CalculWorkEngin); registers not given enter as 0 (none of them reads another)."""
    from entrada_ordens_ia import M32, PASSO, POOL
    unidade &= 0xffff
    rec = (m.u32(POOL) + unidade * PASSO) & M32
    if m.u8(rec + 0x82) == 2:
        s = m.u16(rec + 0x80)
        if chamar('BatimentEnDestruction', 0x45661a, EAX=s)['EAX'] & 0xff or \
                chamar('BatimentGetPlayer', 0x45662c, EAX=s)['EAX'] & 0xff != m.u8(rec):
            raise DependenciaIA('EnginNextEtape state 5: work structure destroyed or foreign (0x456639)', 0x456639)
    chamar('CalculWorkEngin', 0x456731, EAX=unidade)
    return SAIDA


CORPO_CAVERNA = 0x426aff               # BatimentNextEtape's type-3 switch target (Economy's corpo_caverna)


def instalar_donos(m, p, donos, tabelas):
    """Install in the keyword provider dict ``p`` the providers past frame 220 from ``donos``
    (``provedores_entrada_ia.DonosM3``):
    - ``BatimentNextEtape`` wraps ``p``'s pinned one: its type-3 target 0x426aff (the pinned switch stops there
      before any store) runs ``BatimentNextEtape:cave`` = Economy's ``corpo_caverna(structure)``;
    - ``BatimentIllumine(sitio, estrutura, jogador, ebx)`` and ``BatimentDecouvre(sitio, estrutura, jogador)``:
      Core's ``visao_grupos`` (EAX structure, EDX player, EBX light flag; other registers 0, which they do not read);
    - ``EnginNextEtape:state13``: Core's ``estado_entrada`` with ESI = the unit record, EDI = the unit;
    - ``EnginNextEtape:state5``: ``estado_trabalho`` with Core's BatimentEnDestruction/BatimentGetPlayer and
      Economy's CalculWorkEngin.
    ``proxima_etapa_entrada`` dispatches states 5/13 to the last two."""
    from reinicio_ia import DependenciaIA
    estrutura_pinada = p['BatimentNextEtape']

    def batiment_next_etape(sitio, estrutura):
        try:
            return estrutura_pinada(sitio=sitio, estrutura=estrutura)
        except DependenciaIA as erro:
            if erro.rotina == 'BatimentNextEtape type 3' and erro.sitio == CORPO_CAVERNA == \
                    tabelas['tipos_estrutura'][2]:
                p['BatimentNextEtape:cave'](sitio=CORPO_CAVERNA, estrutura=estrutura & 0xffff)
                return None
            raise
    zero = dict.fromkeys(('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'), 0)
    for nome in ('BatimentIllumine', 'BatimentDecouvre'):
        if nome in p:
            raise RuntimeError(f'{nome} already has a provider')
    p['BatimentNextEtape'] = batiment_next_etape
    p['BatimentNextEtape:cave'] = lambda sitio, estrutura: donos.caverna.corpo_caverna(estrutura)
    p['BatimentIllumine'] = lambda sitio, estrutura, jogador, ebx: donos.visao.chamar(
        'BatimentIllumine', dict(zero, EAX=estrutura, EDX=jogador, EBX=ebx))
    p['BatimentDecouvre'] = lambda sitio, estrutura, jogador: donos.visao.chamar(
        'BatimentDecouvre', dict(zero, EAX=estrutura, EDX=jogador))
    p['EnginNextEtape:state13'] = lambda sitio, unidade: donos.ee.chamar('EnginNextEtape:state13', dict(
        zero, ESI=(m.u32(0x4e19a0) + unidade * 276) & 0xffffffff, EDI=unidade))

    def chamar(nome, chamada, **r):
        regs = dict(zero, **r)
        if nome == 'CalculWorkEngin':
            return donos.ciclo.calcul_work_engin(dict(regs, ESP=0))
        return donos.ee.chamar(nome, regs)
    p['EnginNextEtape:state5'] = lambda sitio, unidade: estado_trabalho(m, chamar, unidade)
