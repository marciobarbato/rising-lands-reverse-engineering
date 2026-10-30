"""Transport (unit state 18) and cave-unload (unit state 20) bodies over live original memory, M3.

Translated from the intact bytes after the native capture ``evidencias/transporte/captura-transporte.json.xz`` was
committed. Routines:
- CalculTransporteEngin 0x44f2d4 (EnginNextEtape 0x455e28, state 18; a press on a sack, ProcessInputGame tag 8):
  units of types 0xb..0x11 with a depot mode other than 1 (vehicles) run its own five phases; every other unit, and
  vehicles with depot mode 1, run EnginCalculTransporte;
- EnginCalculTransporte 0x44ea78 (four phases: walk to the sack, pick it up, walk to the depot, unload);
- CalculDechargeCaveEngin 0x44e35c (EnginNextEtape 0x455d1c, state 20; tag 19): goods are taken OUT of the cave
  (the player totals) one at a time and carried to the depot (a structure, or sacks on a cell).

Calling convention. Each routine takes EAX..EBP plus ESP (the address of its return slot) and returns EAX..EBP and
the ESP after its RET as the original leaves them: every register but EAX is restored (exit 0x44f29d -> 0x440d58).
``memoria``: ``u8/u16/u32(addr, value=None)`` (``memoria_quadro_core.MemoriaQuadro``).

Dependencies. Every callee receives the whole register file EAX..EBP, its entry ESP and ``_pilha`` (the pushed
words); ``ARGUMENTOS`` names the argument bits each one reads (what the validators compare). Economy's own callees run
in-process unless left out of ``proprias``: TerrainRetireMatiere (``alimentacao``), TestRessource
(``ordens_economia``), BatimentEnleveMatiere (``restauracao``), BatimentAjouteMatiere (``ciclo_trabalho``, whose own
TerrainDeposeSac goes to ``externo`` with the argument registers it passes). The others go through
``externo(nome, chamada, registradores) -> registradores`` (never defaulted; ``DependenciaTransporte`` without it):
- Core: DeplaceEngin, SetDeplaceEngin, TerrainGetSacType, BatimentGetCase, BatimentEnDestruction, BatimentAdjacent,
  BatimentLocke, BatimentDelocke, GetCaseCentrale, RotateEngin, BatimentPorte, TuyauEstSortie, BagContient, BagRetire,
  EnginRetireType, DeselectionEngin, Distance2d, TerrainAccepteSac, SacCherchePlaceLibre, Random;
- terrain search: ChercheVegetLibre 0x477b74 (Core's ``fadiga_vegetacao.provedor_fadiga``).

Supported domain: every branch of the three routines.
"""
M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
ROTINAS = {'CalculTransporteEngin': 0x44f2d4, 'EnginCalculTransporte': 0x44ea78, 'CalculDechargeCaveEngin': 0x44e35c}
# Economy routines run in-process by default (their translations live in other Economy modules).
PROPRIAS_ECONOMIA = ('TerrainRetireMatiere', 'TestRessource', 'BatimentEnleveMatiere', 'BatimentAjouteMatiere')
# Names whose subtrees the in-process routines compute (validation: not foreign calls).
INTERNAS = ('EnleveMatiere', 'GetRessourceStock', 'AjouteMatiere')
_16, _8 = 0xffff, 0xff
ARGUMENTOS = {
    'DeplaceEngin': {'EAX': _16}, 'SetDeplaceEngin': {'EAX': _16, 'EDX': _16}, 'TerrainGetSacType': {'EAX': _16},
    'ChercheVegetLibre': {'EAX': _16, 'EDX': _8, 'EBX': _8, 'ECX': _8}, 'TerrainRetireMatiere': {'EAX': _16},
    'Random': {'EAX': M32}, 'BatimentLocke': {'EAX': _16}, 'BatimentDelocke': {'EAX': _16},
    'GetCaseCentrale': {'EAX': _16}, 'RotateEngin': {'EAX': _16}, 'BatimentPorte': {'EAX': _16, 'EDX': _8},
    'TuyauEstSortie': {'EAX': _16}, 'BagContient': {'EAX': M32, 'EDX': _8, 'EBX': _16},
    'BagRetire': {'EAX': M32, 'EDX': _8, 'EBX': _16},
    'BatimentAjouteMatiere': {'EAX': _8, 'EDX': _16, 'EBX': _8, 'ECX': _16},
    'EnginRetireType': {'EAX': _16, 'EDX': _8, 'EBX': _16}, 'BatimentGetCase': {'EAX': _16},
    'BatimentEnDestruction': {'EAX': _16}, 'BatimentAdjacent': {'EAX': _16, 'EDX': _16},
    'Distance2d': {'EAX': M32, 'EDX': M32, 'EBX': M32, 'ECX': M32}, 'TerrainAccepteSac': {'EAX': _16, 'EDX': _8},
    'SacCherchePlaceLibre': {'EAX': _16, 'EDX': _8, 'EBX': _16}, 'DeselectionEngin': {'EAX': _16},
    'TestRessource': {'EAX': _16, 'EDX': _16, 'EBX': _16}, 'BatimentEnleveMatiere': {'EAX': _8, 'EDX': _16, 'EBX': _8},
    'EnginCalculTransporte': {'EAX': _16}, 'TerrainDeposeSac': {'EAX': _16, 'EDX': _8, 'EBX': _16},
}
PILHA_EXTERNA = {'ChercheVegetLibre': 1, 'TestRessource': 1}
# Registers each served routine's behaviour depends on: a provider call without one raises ``ArgumentoNaoPassado``.
ARGUMENTOS_EXIGIDOS = {'CalculTransporteEngin': ('EAX',), 'EnginCalculTransporte': ('EAX',),
                       'CalculDechargeCaveEngin': ('EAX',)}


class DependenciaTransporte(NotImplementedError):
    """A callee owned elsewhere was reached without its provider."""
    def __init__(self, rotina, chamada, motivo='provider required'):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: {motivo}')


def _w(v, w):
    return (v & 0xffff0000) | (w & 0xffff)


def _b(v, b):
    return (v & 0xffffff00) | (b & 0xff)


def _sx8(b):
    return (b - 0x100 if b & 0x80 else b) & M32


class Transporte:
    def __init__(self, memoria, *, externo=None, proprias=None):
        self.m = memoria
        self.externo = externo
        self.proprias = set(ROTINAS) | set(PROPRIAS_ECONOMIA) if proprias is None else set(proprias)
        self.incertos = {}
        self._esp = 0

    # ------------------------------------------------------------ helpers
    def _pool(self):
        return self.m.u32(PONTEIRO_UNIDADES)

    def _ext(self, nome, chamada, r, pilha=()):
        esp = (self._esp - 4 * len(pilha) - 4) & M32
        entrada = {k: r[k] & M32 for k in REG7}
        entrada['ESP'] = esp
        if nome in self.proprias and nome in PROPRIAS_ECONOMIA:
            saida = self._propria(nome, entrada, pilha)
        else:
            if self.externo is None:
                raise DependenciaTransporte(nome, chamada)
            if pilha:
                entrada['_pilha'] = list(pilha)
            saida = self.externo(nome, chamada, entrada)
        for k, v in (saida.get('_incertos') or {}).items():
            self.incertos[k] = self.incertos.get(k, 0) | v
        return {k: saida[k] & M32 for k in REG7 if k in saida}

    def _chamar(self, r, nome, chamada, pilha=(), **regs):
        """Set the argument registers in ``r``, pass the whole file, take every register the callee returns."""
        r.update({k: v & M32 for k, v in regs.items()})
        saida = self._ext(nome, chamada, r, pilha)
        r.update(saida)
        return r

    def _propria(self, nome, entrada, pilha):
        m = self.m
        if nome == 'TerrainRetireMatiere':
            from alimentacao import Alimentacao
            return Alimentacao(m).chamar('TerrainRetireMatiere', entrada)
        if nome == 'TestRessource':
            from ordens_economia import OrdensEconomia
            return OrdensEconomia(m).chamar('TestRessource', entrada, pilha)
        if nome == 'BatimentEnleveMatiere':
            from restauracao import Restauracao
            return Restauracao(m).chamar('BatimentEnleveMatiere', entrada)
        from ciclo_trabalho import CicloTrabalho
        externo = self.externo

        def repassar(n, chamada, regs):
            if externo is None:
                raise DependenciaTransporte(n, chamada)
            return externo(n, chamada, regs)
        return CicloTrabalho(m, externo=repassar).batiment_ajoute_matiere(entrada)

    def _liberar_busca(self, ocupada=0, sucesso=0, rota=0):
        self.m.u8(BUSCA_OCUPADA, ocupada)
        self.m.u8(BUSCA_SUCESSO, sucesso)
        self.m.u32(BUSCA_ROTA, rota)
        self.m.u16(BUSCA_UNIDADE, 0xffff)

    def _dono(self, di):
        return di & 0xffff == self.m.u16(BUSCA_UNIDADE)

    def _rec(self, u):
        return (self._pool() + (u & M32) * PASSO) & M32

    @staticmethod
    def _sair(regs, eax, pop=0):
        saida = {k: regs[k] & M32 for k in REG7}
        saida['EAX'] = eax & M32
        saida['ESP'] = (regs['ESP'] + 4 + pop) & M32
        return saida

    def _cheia(self, rec, extra=1):
        """``(u16 bag +0x66) + extra <= u16 capacity +2`` (setle over 32-bit values)."""
        return (self.m.u16(rec + 0xa + 0x66) + extra) <= self.m.u16(rec + 0xa + 2)

    def _distancia(self, r, alvo, cel, locais=None):
        """The inline cell split of 0x44ef0d / 0x44e7a0: (EAX, EDX, EBX, ECX) for Distance2d(cell x, cell y, target
        x, target y)."""
        tx, ty = alvo & 0xff, alvo >> 8
        cx, cy = cel & 0xff, cel >> 8
        r.update(EAX=cx, EDX=cy, EBX=tx, ECX=ty)

    # ------------------------------------------------------------ CalculDechargeCaveEngin
    def calcul_decharge_cave_engin(self, regs):
        """CalculDechargeCaveEngin 0x44e35c: AX unit, state 20 (tag 19: unload the cave into a depot). By phase +0x89:
        - 0: bag full -> phase 1 (timer 10); else walk (DeplaceEngin) until at +0x7e or BatimentAdjacent(+0xc0);
          adjacent -> phase 1; at +0x7e but not adjacent -> +0x7e := BatimentGetCase(+0xc0) (search released);
        - 1: with room, the timer +0x8b counts down; at 0, TestRessource(kind 1, kind 2, kind 0, push owner) and
          BatimentEnleveMatiere(kind, 1, owner): one good taken out of the totals into the bag (tag 2), timer 10;
          when full: depot mode 2 -> +0x7e := BatimentGetCase(+0x80), phase 2 (no structure: state 7 unless 0/4);
          mode 1 -> +0x7e := +0x80, phase 2;
        - 2: mode 2: byte +0x86/+0x87 set or not adjacent to +0x80 -> DeplaceEngin; adjacent -> DeselectionEngin,
          phase 3; mode 1: walk to +0x7e; there, Distance2d to +0x80 > 16 -> +0x7e := +0x80; else TerrainAccepteSac
          -> phase 3, or +0x7e := SacCherchePlaceLibre(+0x80) when found;
        - 3: the timer counts down; at 0 (timer 10): a carried good -> mode 2 BatimentAjouteMatiere(kind, 1, owner,
          +0x80) + BagRetire, mode 1 EnginRetireType(unit, 2, kind); none left -> back to the cave (phase 0, +0x7e :=
          +0xb2) or, without +0xb2, state 7 unless 0/4.
        Phase > 3: nothing. The path search is released wherever +0x7e is set and the search is the unit's."""
        m = self.m
        self.incertos = {}
        e = {k: regs[k] & M32 for k in REG7}
        self._esp = (regs['ESP'] - 0x40) & M32
        quadro = (regs['ESP'] - 0x1c) & M32           # EBP after the six pushes
        u = e['EAX'] & 0xffff
        desloc = u * PASSO
        rec = (self._pool() + desloc) & M32
        r = dict(e, EBX=u, ESI=rec, EDI=e['EAX'], EBP=quadro)
        fase = m.u8(rec + 0x89)
        if fase > 3:
            return self._fim(regs, (desloc & 0xffff0000) | fase)
        r['EAX'] = fase
        di = u
        if fase == 0:
            return self._fim(regs, self._dc0(r, rec, di))
        if fase == 1:
            return self._fim(regs, self._dc1(r, rec, di, desloc))
        if fase == 2:
            return self._fim(regs, self._dc2(r, rec, di, desloc))
        return self._fim(regs, self._dc3(r, rec, di, desloc))

    def _fim(self, regs, eax):
        saida = self._sair(regs, eax)
        if self.incertos:
            saida['_incertos'] = {k: v for k, v in self.incertos.items() if k == 'EAX'}
            if not saida['_incertos']:
                del saida['_incertos']
        return saida

    def _dc0(self, r, rec, di):
        m = self.m
        r['EDX'] = _b(r['EDX'], 2)
        r['ECX'] = 1
        cnt = m.u16(rec + 0x70)
        r['EBX'] = 1
        r['EDX'] = cnt + 1
        cabe = r['EDX'] <= m.u16(rec + 0xc)
        if not cabe:
            m.u8(rec + 0x8b, 0xa)
            m.u8(rec + 0x89, 1)
            return 0
        cel = m.u16(rec + 8)
        r['EAX'] = cel
        if cel != m.u16(rec + 0x7e):
            self._chamar(r, 'BatimentAdjacent', 0x44e3f7, EDX=cel, EAX=m.u16(rec + 0xc0))
            if not r['EAX'] & 0xff:
                self._chamar(r, 'DeplaceEngin', 0x44e405, EAX=di)
                return r['EAX']
        self._chamar(r, 'BatimentAdjacent', 0x44e41e, EDX=m.u16(rec + 8), EAX=m.u16(rec + 0xc0))
        if r['EAX'] & 0xff:
            m.u8(rec + 0x8b, 0xa)
            m.u8(rec + 0x89, 1)
            return r['EAX']
        r['EBX'] = di
        self._chamar(r, 'BatimentGetCase', 0x44e44f, EDX=di * 17, EAX=m.u16(rec + 0xc0))
        celula = r['EAX']
        edx = (((r['EDX'] << 2) + r['EBX']) << 2) & M32
        alvo = (self._pool() + edx) & M32
        m.u16(alvo + 0x7e, celula)
        if self._dono(di):
            self._liberar_busca()
        m.u8(alvo + 0x88, 0)
        return alvo

    def _dc1(self, r, rec, di, desloc):
        m = self.m
        r['EDX'] = _b(r['EDX'], 2)
        cnt = m.u16(rec + 0x70)
        r['EBX'] = 1
        r['EDX'] = cnt + 1
        pronto = False
        eax = 0
        if r['EDX'] > m.u16(rec + 0xc):
            pronto = True
        else:
            t = (m.u8(rec + 0x8b) - 1) & 0xff
            r['ECX'] = _b(r['ECX'], t)
            m.u8(rec + 0x8b, t)
            if t:
                return t
            dono = m.u8(rec)
            tipo = m.u16(rec + 0x84)
            self._chamar(r, 'TestRessource', 0x44e54b, pilha=(dono,), ECX=0, EBX=int(tipo == 0), EDX=int(tipo == 2),
                         EAX=int(tipo == 1))
            if not r['EAX'] & 0xff:
                return r['EAX']
            self._chamar(r, 'BatimentEnleveMatiere', 0x44e565, EDX=1, EBX=m.u8(rec), EAX=m.u8(rec + 0x84))
            bolsa = (rec + 0xa) & M32
            r['EBX'] = (_w(r['EBX'], m.u16(bolsa + 0x66)) + 1) & M32
            n = m.u16(bolsa)
            m.u16(bolsa + 0x66, r['EBX'])
            m.u8(bolsa + 0x42 + n, 2)
            m.u16(bolsa + 6 + 2 * n, m.u16(rec + 0x84))
            m.u16(bolsa, n + 1)
            m.u8(rec + 0x8b, 0xa)
            return bolsa
        del eax
        modo = m.u8(rec + 0x82)
        if modo == 2:
            alvo = m.u16(rec + 0x80)
            if alvo != 0xffff:
                self._chamar(r, 'BatimentGetCase', 0x44e5d2, EAX=alvo, EBX=0)
                ebx = _w(r['EBX'], di)
                celula = r['EAX']
                m.u8(rec + 0x89, 2)
                novo = (self._pool() + ebx * PASSO) & M32
                m.u16(novo + 0x7e, celula)
                if self._dono(di):
                    self._liberar_busca()
                m.u8(novo + 0x88, 0)
                return novo
            return self._ocioso(rec, di, r['EDI'])
        if modo == 1:
            novo = self._rec(di)
            m.u8(rec + 0x89, 2)
            m.u16(novo + 0x7e, m.u16(rec + 0x80))
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return novo
        return modo

    def _ocioso(self, rec, di, edi):
        """0x44e62f / 0x44e9f5: state 7 unless the unit is in state 0 or 4 (EAX 0 then); EAX = unit * 69."""
        m = self.m
        alvo = self._rec(di)
        estado = m.u8(alvo + 2)
        if estado in (0, 4):
            return 0
        u = edi & 0xffff
        m.u8((self._pool() + u * PASSO + 2) & M32, 7)
        if self._dono(u):
            self._liberar_busca()
        return u * 69

    def _dc2(self, r, rec, di, desloc):
        m = self.m
        modo = m.u8(rec + 0x82)
        if modo == 2:
            if _sx8(m.u8(rec + 0x86)) or _sx8(m.u8(rec + 0x87)):
                self._chamar(r, 'DeplaceEngin', 0x44e405, EAX=di)
                return r['EAX']
            self._chamar(r, 'BatimentAdjacent', 0x44e75f, EDX=m.u16(rec + 8), EAX=m.u16(rec + 0x80))
            if not r['EAX'] & 0xff:
                self._chamar(r, 'DeplaceEngin', 0x44e405, EAX=di)
                return r['EAX']
            self._chamar(r, 'DeselectionEngin', 0x44e76e, EAX=r['EBX'])
            m.u8(rec + 0x89, 3)
            m.u8(rec + 0x8b, 0xa)
            return r['EAX']
        if modo != 1:
            return modo
        cel = m.u16(rec + 8)
        if cel != m.u16(rec + 0x7e):
            self._chamar(r, 'DeplaceEngin', 0x44e405, EAX=r['EBX'])
            return r['EAX']
        alvo = m.u16(rec + 0x80)
        self._distancia(r, alvo, cel)
        self._chamar(r, 'Distance2d', 0x44e811)
        if r['EAX'] > 0x10:
            novo = (self._pool() + desloc) & M32
            m.u16(novo + 0x7e, alvo)
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return novo
        k42 = (m.u8(rec + 0x84) + 0x42) & 0xff
        self._chamar(r, 'TerrainAccepteSac', 0x44e831, EDX=k42, EAX=cel)
        if r['EAX'] & 0xff:
            m.u8(rec + 0x89, 3)
            m.u8(rec + 0x8b, 0xa)
            return r['EAX']
        self._chamar(r, 'SacCherchePlaceLibre', 0x44e856, EDX=k42, EBX=di, EAX=alvo)
        lugar = r['EAX'] & 0xffff
        if lugar == 0xffff:
            return 0xffff
        novo = (self._pool() + desloc) & M32
        m.u16(novo + 0x7e, lugar)
        if self._dono(di):
            self._liberar_busca()
        m.u8(novo + 0x88, 0)
        return novo

    def _dc3(self, r, rec, di, desloc):
        m = self.m
        t = (m.u8(rec + 0x8b) - 1) & 0xff
        r['EDX'] = _b(r['EDX'], t)
        m.u8(rec + 0x8b, t)
        if t:
            return t
        m.u8(rec + 0x8b, 0xa)
        bolsa = (rec + 0xa) & M32
        tipo = m.u16(rec + 0x84)
        self._chamar(r, 'BagContient', 0x44e920, EDX=2, EBX=tipo, EAX=bolsa)
        if r['EAX'] & 0xffff:
            modo = m.u8(rec + 0x82)
            if modo == 2:
                self._chamar(r, 'BatimentAjouteMatiere', 0x44e953, EDX=1, ECX=m.u16(rec + 0x80), EBX=m.u8(rec),
                             EAX=m.u8(rec + 0x84))
                self._chamar(r, 'BagRetire', 0x44e969, EDX=2, EBX=m.u16(rec + 0x84), EAX=bolsa)
                return r['EAX']
            if modo == 1:
                self._chamar(r, 'EnginRetireType', 0x44e98d, EDX=2, EBX=m.u16(rec + 0x84), EAX=di)
                return r['EAX']
            return modo
        b2 = m.u16(rec + 0xb2)
        if b2 != 0xffff:
            m.u8(rec + 0x89, 0)
            novo = (self._pool() + desloc) & M32
            m.u16(novo + 0x7e, b2)
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return novo
        return self._ocioso(rec, di, r['EDI'])

    # ------------------------------------------------------------ CalculTransporteEngin
    def calcul_transporte_engin(self, regs):
        """CalculTransporteEngin 0x44f2d4: AX unit, state 18 (tag 8: carry sacks to the depot +0x80/+0x82/+0x84).
        Not a vehicle (type outside 0xb..0x11), or depot mode 1: EnginCalculTransporte(unit). A vehicle by phase:
        - 0: walk to +0x7e; there, a sack of kind +0x84 -> phase 1 (timer 10, +0xa4 := 0); else
          ChercheVegetLibre(+0xb2, 10, kind + 0x42) -> +0x7e (none: nothing);
        - 1: with room, the timer counts down; at 0, TerrainRetireMatiere(cell) into the bag (tag 2), then
          ChercheVegetLibre around the cell offset by two Random(5) draws -> phase 0 towards it; full or none:
          mode 2 -> +0xc0 := +0x80, BatimentLocke, +0x7e := GetCaseCentrale - 0xfe, phase 2 (no structure: +0x7e :=
          +0x7c); mode 1 -> +0x7e := +0x80, phase 2;
        - 2: walk to +0x7e; there phase 3 (mode 2: facing +0x90 := 9), timer 10;
        - 3: RotateEngin until +0x90 = +0x91; then mode 2: BatimentPorte(+0xc0, 1) and, when TuyauEstSortie, phase 4
          with timer 50; other modes: phase 4, timer 10;
        - 4: empty bag -> (mode 2: BatimentPorte(+0xc0, 0), BatimentDelocke) +0xc0 := 0xffff, phase 0 towards +0xb2;
          else the timer counts down and at 0 BagRetire, then mode 2 BatimentAjouteMatiere (timer 50) or
          EnginRetireType (timer 10)."""
        m = self.m
        self.incertos = {}
        e = {k: regs[k] & M32 for k in REG7}
        self._esp = (regs['ESP'] - 0x20) & M32
        u = e['EAX'] & 0xffff
        desloc = u * PASSO
        rec = (self._pool() + desloc) & M32
        tipo = m.u8(rec + 1)
        r = dict(e, EBX=u, ESI=rec, EDI=e['EAX'])
        veiculo = ((tipo - 0xb) & 0xff) <= 6
        if veiculo:
            r['EBX'] = m.u8(rec + 0x82)
        if not veiculo or r['EBX'] == 1:
            esp = self._esp
            r['EAX'] = u
            saida = self.engin_calcul_transporte(dict(r, ESP=(esp - 4) & M32))
            self._esp = esp
            return self._fim(regs, saida['EAX'])
        fase = m.u8(rec + 0x89)
        if fase > 4:
            return self._fim(regs, fase)
        r['EAX'] = fase
        f = (self._v0, self._v1, self._v2, self._v3, self._v4)[fase]
        return self._fim(regs, f(r, rec, u, desloc))

    def _v0(self, r, rec, di, desloc):
        m = self.m
        d7e, cel = m.u16(rec + 0x7e), m.u16(rec + 8)
        r['ECX'] = _w(r['ECX'], cel)
        if d7e != cel:
            self._chamar(r, 'DeplaceEngin', 0x44f356, EAX=di)
            return r['EAX']
        tipo = m.u16(rec + 0x84)
        self._chamar(r, 'TerrainGetSacType', 0x44f36b, EAX=cel, EDX=tipo)
        saco = r['EAX'] & 0xff
        if saco == r['EDX']:
            m.u8(rec + 0x89, 1)
            m.u8(rec + 0x8b, 0xa)
            m.u8(rec + 0xa4, 0)
            return saco
        k42 = (m.u8(rec + 0x84) + 0x42) & 0xff
        self._chamar(r, 'ChercheVegetLibre', 0x44f3b0, pilha=(di,), EDX=0xa, EBP=di, EBX=k42, ECX=k42,
                     EAX=m.u16(rec + 0xb2))
        achado = r['EAX'] & 0xffff
        if achado == 0xffff:
            return 0xffff
        novo = (self._pool() + r['EBP'] * PASSO) & M32
        m.u16(novo + 0x7e, achado)
        if self._dono(di):
            self._liberar_busca()
        m.u8(novo + 0x88, 0)
        return novo

    def _v1(self, r, rec, di, desloc):
        m = self.m
        pronto = False
        cnt = m.u16(rec + 0x70)
        r['EDX'] = cnt + 1
        if r['EDX'] > m.u16(rec + 0xc):
            pronto = True
        else:
            t = (m.u8(rec + 0x8b) - 1) & 0xff
            m.u8(rec + 0x8b, t)
            if t:
                return t
            cel = m.u16(rec + 8)
            r['ECX'] &= 0xffff00ff
            self._chamar(r, 'TerrainRetireMatiere', 0x44f455, EAX=cel)
            r['ECX'] = _b(r['ECX'], r['EAX'])
            bolsa = (rec + 0xa) & M32
            m.u16(bolsa + 0x66, m.u16(bolsa + 0x66) + 1)
            n = m.u16(bolsa)
            m.u8(bolsa + 0x42 + n, 2)
            m.u16(bolsa + 6 + 2 * n, r['ECX'])
            m.u16(bolsa, n + 1)
            k42 = (m.u8(rec + 0x84) + 0x42) & 0xff
            r.update(EBX=k42, EBP=di, EDX=n)
            local = cel
            r['ECX'] = 5
            for argumento, chamada in ((0x1f, 0x44f4a0), (0x20, 0x44f4b8)):
                self._chamar(r, 'Random', chamada, EDX=0, EAX=argumento)
                dividendo = (r['EDX'] << 32) | r['EAX']
                q, resto = divmod(dividendo, r['ECX'])
                if q > M32:
                    raise ZeroDivisionError(f'CalculTransporteEngin {chamada:#x}: div overflow')
                r.update(EAX=q, EDX=resto)
                if argumento == 0x1f:
                    local = (local + resto) & M32
            pos = (local - 2 + ((r['EDX'] << 8) - 0x200)) & 0xffff
            self._chamar(r, 'ChercheVegetLibre', 0x44f4dd, pilha=(di,), EDX=0xa, ECX=r['EBX'], EAX=pos)
            achado = r['EAX'] & 0xffff
            r['ECX'] = r['EAX']
            if achado == 0xffff:
                pronto = True
            else:
                novo = (self._pool() + r['EBP'] * PASSO) & M32
                m.u8(rec + 0xa4, 0)
                m.u16(novo + 0x7e, achado)
                if self._dono(di):
                    self._liberar_busca()
                m.u8(novo + 0x88, 0)
                m.u8(rec + 0x89, 0)
                return novo
        modo = m.u8(rec + 0x82)
        if modo == 2:
            alvo = m.u16(rec + 0x80)
            m.u16(rec + 0xc0, alvo)
            if alvo != 0xffff:
                self._chamar(r, 'BatimentLocke', 0x44f58c, EAX=alvo)
                self._chamar(r, 'GetCaseCentrale', 0x44f59c, EBX=0, EAX=m.u16(rec + 0xc0))
                ebx = _w(r['EBX'], di)
                celula = (r['EAX'] - 0xfe) & M32
                m.u8(rec + 0x89, 2)
                novo = (self._pool() + ebx * PASSO) & M32
                m.u16(novo + 0x7e, celula)
                if self._dono(di):
                    self._liberar_busca()
                m.u8(novo + 0x88, 0)
                return novo
            novo = self._rec(di)
            m.u16(novo + 0x7e, m.u16(rec + 0x7c))
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return novo
        if modo == 1:
            novo = self._rec(di)
            m.u8(rec + 0x89, 2)
            m.u16(novo + 0x7e, m.u16(rec + 0x80))
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return novo
        return modo

    def _v2(self, r, rec, di, desloc):
        m = self.m
        if m.u16(rec + 0x7e) != m.u16(rec + 8):
            self._chamar(r, 'DeplaceEngin', 0x44f356, EAX=di)
            return r['EAX']
        modo = m.u8(rec + 0x82)
        m.u8(rec + 0x89, 3)
        if modo == 2:
            m.u8(rec + 0x90, 9)
        m.u8(rec + 0x8b, 0xa)
        return modo

    def _v3(self, r, rec, di, desloc):
        m = self.m
        b90 = m.u8(rec + 0x90)
        if b90 != m.u8(rec + 0x91):
            self._chamar(r, 'RotateEngin', 0x44f705, EAX=di)
            return r['EAX']
        if r['EBX'] == 2:
            self._chamar(r, 'BatimentPorte', 0x44f722, EDX=1, EAX=m.u16(rec + 0xc0))
            self._chamar(r, 'TuyauEstSortie', 0x44f730, EAX=m.u16(rec + 0xc0))
            if r['EAX'] & 0xff:
                m.u8(rec + 0x89, 4)
                m.u8(rec + 0x8b, 0x32)
            return r['EAX']
        m.u8(rec + 0x89, 4)
        m.u8(rec + 0x8b, 0xa)
        return b90

    def _v4(self, r, rec, di, desloc):
        m = self.m
        bolsa = (rec + 0xa) & M32
        self._chamar(r, 'BagContient', 0x44f76c, EDX=2, ECX=bolsa, EBX=m.u16(rec + 0x84), EAX=bolsa)
        if not r['EAX'] & 0xffff:
            if m.u8(rec + 0x82) == 2:
                self._chamar(r, 'BatimentPorte', 0x44f792, EDX=0, EAX=m.u16(rec + 0xc0))
                self._chamar(r, 'BatimentDelocke', 0x44f7a0, EAX=m.u16(rec + 0xc0))
            m.u16(rec + 0xc0, 0xffff)
            m.u8(rec + 0x89, 0)
            novo = self._rec(di)
            m.u16(novo + 0x7e, m.u16(rec + 0xb2))
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return novo
        t = (m.u8(rec + 0x8b) - 1) & 0xff
        m.u8(rec + 0x8b, t)
        if t:
            return t
        self._chamar(r, 'BagRetire', 0x44f839, EDX=2, EBX=m.u16(rec + 0x84), EAX=r['ECX'])
        if m.u8(rec + 0x82) == 2:
            self._chamar(r, 'BatimentAjouteMatiere', 0x44f865, EDX=1, ECX=m.u16(rec + 0x80), EBX=m.u8(rec),
                         EAX=m.u8(rec + 0x84))
            m.u8(rec + 0x8b, 0x32)
            return r['EAX']
        self._chamar(r, 'EnginRetireType', 0x44f882, EDX=2, EAX=di, EBX=m.u16(rec + 0x84))
        m.u8(rec + 0x8b, 0xa)
        return r['EAX']

    # ------------------------------------------------------------ EnginCalculTransporte
    def engin_calcul_transporte(self, regs):
        """EnginCalculTransporte 0x44ea78: AX unit. By phase +0x89:
        - 0: bag full -> phase 1 (timer 10, +0xa4 := 0); else walk to +0x7e; there, a sack of kind +0x84 -> phase 1;
          else ChercheVegetLibre(+0xb2, 5, kind + 0x42) -> +0x7e, none -> SetDeplaceEngin(unit, +0x7c);
        - 1: with room, the timer counts down; at 0, TerrainRetireMatiere(cell) into the bag (tag 2) and
          ChercheVegetLibre around the cell offset by two Random(5) draws: found with room left -> phase 0 towards
          it (+0xa4 := 0); full or none: mode 2 -> +0xc0 := +0x80, +0x7e := BatimentGetCase(+0x80), phase 2 (no
          structure: SetDeplaceEngin(unit, +0x7c)); mode 1 -> +0x7e := +0x80, phase 2;
        - 2: mode 2: BatimentEnDestruction(+0xc0) -> SetDeplaceEngin(unit, +0x7e); byte +0x86/+0x87 set or not
          BatimentAdjacent(+0xc0) -> DeplaceEngin; adjacent -> phase 3 (timer 10); mode 1: walk to +0x7e; there,
          Distance2d to +0x80 > 16 -> +0x7e := +0x80, else TerrainAccepteSac -> phase 3 or +0x7e :=
          SacCherchePlaceLibre(+0x80);
        - 3: BatimentEnDestruction(+0xc0) -> SetDeplaceEngin(unit, +0x7e), then the timer counts down; at 0 (timer
          10): a carried good -> mode 2 BatimentAjouteMatiere(kind, 1, owner, +0x80) + BagRetire, mode 1
          EnginRetireType; none: ChercheVegetLibre(+0xb2, 5, kind + 0x42) -> phase 0 towards a sack other than the
          depot cell, none (or no +0xb2) -> state 7 unless 0/4."""
        m = self.m
        e = {k: regs[k] & M32 for k in REG7}
        self._esp = (regs['ESP'] - 0x2c) & M32
        u = e['EAX'] & 0xffff
        desloc = u * PASSO
        rec = (self._pool() + desloc) & M32
        r = dict(e, EDX=desloc, ESI=rec, EDI=e['EAX'], EBP=u)
        fase = m.u8(rec + 0x89)
        if fase > 3:
            return self._sair(regs, (e['EAX'] & 0xffff0000) | fase)
        r['EAX'] = fase
        f = (self._t0, self._t1, self._t2, self._t3)[fase]
        return self._sair(regs, f(r, rec, u, desloc))

    def _t0(self, r, rec, di, desloc):
        m = self.m
        cnt = m.u16(rec + 0x70)
        r['EDX'] = cnt + 1
        if r['EDX'] > m.u16(rec + 0xc):
            m.u8(rec + 0x89, 1)
            m.u8(rec + 0x8b, 0xa)
            m.u8(rec + 0xa4, 0)
            return 0
        cel = m.u16(rec + 8)
        r['EBX'] = _w(rec + 0xa, cel)
        if m.u16(rec + 0x7e) != cel:
            self._chamar(r, 'DeplaceEngin', 0x44eaf3, EAX=di)
            return r['EAX']
        self._chamar(r, 'TerrainGetSacType', 0x44eb0b, EAX=cel, EDX=m.u16(rec + 0x84))
        saco = r['EAX'] & 0xff
        if saco == r['EDX']:
            m.u8(rec + 0x89, 1)
            m.u8(rec + 0x8b, 0xa)
            m.u8(rec + 0xa4, 0)
            return saco
        k42 = (m.u8(rec + 0x84) + 0x42) & 0xff
        self._chamar(r, 'ChercheVegetLibre', 0x44eb53, pilha=(di,), EDX=5, EBP=di, EBX=k42, ECX=k42,
                     EAX=m.u16(rec + 0xb2))
        if r['EAX'] & 0xffff == 0xffff:
            self._chamar(r, 'SetDeplaceEngin', 0x44ebbf, EDX=m.u16(rec + 0x7c), EAX=r['EBP'])
            return r['EAX']
        novo = (self._pool() + r['EBP'] * PASSO) & M32
        m.u16(novo + 0x7e, r['EAX'])
        if self._dono(di):
            self._liberar_busca()
        m.u8(novo + 0x88, 0)
        return r['EAX']

    def _t1(self, r, rec, di, desloc):
        m = self.m
        bolsa = (rec + 0xa) & M32
        r['EBX'] = bolsa
        r['EDX'] = m.u16(bolsa + 0x66) + 1
        pronto = r['EDX'] > m.u16(bolsa + 2)
        eax = 0
        if not pronto:
            t = (m.u8(rec + 0x8b) - 1) & 0xff
            m.u8(rec + 0x8b, t)
            if t:
                return t
            cel = m.u16(rec + 8)
            self._chamar(r, 'TerrainRetireMatiere', 0x44ec1b, EAX=cel)
            r['EBP'] = bolsa
            r['EBX'] = (bolsa & 0xffff0000) | (r['EAX'] & 0xff)
            r['ECX'] = (_w(r['ECX'], m.u16(bolsa + 0x66)) + 1) & M32
            n = m.u16(bolsa)
            m.u16(bolsa + 0x66, r['ECX'])
            m.u8(bolsa + 0x42 + n, 2)
            m.u16(bolsa + 6 + 2 * n, r['EBX'])
            m.u16(bolsa, n + 1)
            k42 = (m.u8(rec + 0x84) + 0x42) & 0xff
            r.update(EBX=k42, EDX=0)
            r['ECX'] = cel
            self._chamar(r, 'Random', 0x44ec76, EAX=0x1d)
            q, resto = divmod((r['EDX'] << 32) | r['EAX'], 5)
            if q > M32:
                raise ZeroDivisionError('EnginCalculTransporte 0x44ec7b: div overflow')
            local = (r['ECX'] + resto) & M32
            r.update(EAX=q, EDX=resto)
            r['ECX'] = 5
            self._chamar(r, 'Random', 0x44ec91, EDX=0, EAX=0x1e)
            q, resto = divmod((r['EDX'] << 32) | r['EAX'], r['ECX'])
            if q > M32:
                raise ZeroDivisionError('EnginCalculTransporte 0x44ec96: div overflow')
            pos = (local - 2 + ((resto << 8) - 0x200)) & 0xffff
            self._chamar(r, 'ChercheVegetLibre', 0x44ecb6, pilha=(di,), EDX=5, ECX=r['EBX'], EAX=pos)
            r['ECX'] = r['EAX']
            achado = r['EAX'] & 0xffff
            if achado == 0xffff:
                eax = 0xffff
            elif not self._cheia(rec):
                eax = 0
            else:
                novo = self._rec(di)
                m.u8(rec + 0xa4, 0)
                m.u16(novo + 0x7e, achado)
                if self._dono(di):
                    self._liberar_busca()
                m.u8(novo + 0x88, 0)
                m.u8(rec + 0x89, 0)
                return di
        modo = m.u8(rec + 0x82)
        if modo == 2:
            alvo = m.u16(rec + 0x80)
            m.u16(rec + 0xc0, alvo)
            if alvo == 0xffff:
                self._chamar(r, 'SetDeplaceEngin', 0x44ebbf, EDX=m.u16(rec + 0x7c), EAX=di)
                return r['EAX']
            self._chamar(r, 'BatimentGetCase', 0x44ed84, EAX=alvo)
            celula = r['EAX']
            m.u8(rec + 0x89, 2)
            novo = self._rec(di)
            m.u16(novo + 0x7e, celula)
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return di
        if modo == 1:
            alvo = m.u16(rec + 0x80)
            m.u8(rec + 0x89, 2)
            novo = self._rec(di)
            m.u16(novo + 0x7e, alvo)
            if self._dono(di):
                alvo &= 0xff00
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return alvo
        del eax
        return modo

    def _t2(self, r, rec, di, desloc):
        m = self.m
        modo = m.u8(rec + 0x82)
        if modo == 2:
            self._chamar(r, 'BatimentEnDestruction', 0x44ee71, EAX=m.u16(rec + 0xc0))
            if r['EAX'] & 0xff:
                self._chamar(r, 'SetDeplaceEngin', 0x44ebbf, EDX=m.u16(rec + 0x7e), EAX=r['EBP'])
                return r['EAX']
            if _sx8(m.u8(rec + 0x86)) or _sx8(m.u8(rec + 0x87)):
                self._chamar(r, 'DeplaceEngin', 0x44eaf3, EAX=di)
                return r['EAX']
            self._chamar(r, 'BatimentAdjacent', 0x44eeb6, EDX=m.u16(rec + 8), EAX=m.u16(rec + 0xc0))
            if not r['EAX'] & 0xff:
                self._chamar(r, 'DeplaceEngin', 0x44eaf3, EAX=di)
                return r['EAX']
            m.u8(rec + 0x89, 3)
            m.u8(rec + 0x8b, 0xa)
            return r['EAX']
        if modo != 1:
            return modo
        cel = m.u16(rec + 8)
        if cel != m.u16(rec + 0x7e):
            self._chamar(r, 'DeplaceEngin', 0x44eaf3, EAX=r['EBP'])
            return r['EAX']
        alvo = m.u16(rec + 0x80)
        self._distancia(r, alvo, cel)
        self._chamar(r, 'Distance2d', 0x44ef69)
        if r['EAX'] > 0x10:
            eax = _w(r['EAX'], alvo)
            novo = (self._pool() + desloc) & M32
            m.u16(novo + 0x7e, alvo)
            if self._dono(di):
                self._liberar_busca()
            m.u8(novo + 0x88, 0)
            return eax
        k42 = (m.u8(rec + 0x84) + 0x42) & 0xff
        self._chamar(r, 'TerrainAccepteSac', 0x44ef89, EDX=k42, EAX=cel)
        if r['EAX'] & 0xff:
            m.u8(rec + 0x89, 3)
            m.u8(rec + 0x8b, 0xa)
            return r['EAX']
        self._chamar(r, 'SacCherchePlaceLibre', 0x44efad, EDX=k42, EBX=r['EBP'], EAX=alvo)
        lugar = r['EAX'] & 0xffff
        if lugar == 0xffff:
            return r['EAX']
        novo = (self._pool() + desloc) & M32
        m.u16(novo + 0x7e, lugar)
        eax = r['EAX']
        if self._dono(di):
            eax = 0
            self._liberar_busca()
        m.u8(novo + 0x88, 0)
        return eax

    def _t3(self, r, rec, di, desloc):
        m = self.m
        self._chamar(r, 'BatimentEnDestruction', 0x44f04a, EAX=m.u16(rec + 0xc0))
        if r['EAX'] & 0xff:
            self._chamar(r, 'SetDeplaceEngin', 0x44f05b, EDX=m.u16(rec + 0x7e), EAX=r['EBP'])
        t = (m.u8(rec + 0x8b) - 1) & 0xff
        r['EDX'] = _b(r['EDX'], t)
        m.u8(rec + 0x8b, t)
        if t:
            return t
        bolsa = (rec + 0xa) & M32
        r['EBP'] = bolsa
        m.u8(rec + 0x8b, 0xa)
        self._chamar(r, 'BagContient', 0x44f094, EDX=2, EBX=m.u16(rec + 0x84), EAX=bolsa)
        if r['EAX'] & 0xffff:
            modo = m.u8(rec + 0x82)
            if modo == 2:
                self._chamar(r, 'BatimentAjouteMatiere', 0x44f0c7, EDX=1, ECX=m.u16(rec + 0x80), EBX=m.u8(rec),
                             EAX=m.u8(rec + 0x84))
                self._chamar(r, 'BagRetire', 0x44f0dc, EDX=2, EBX=m.u16(rec + 0x84), EAX=r['EBP'])
                m.u8(rec + 0x8b, 0xa)
                return r['EAX']
            if modo == 1:
                self._chamar(r, 'EnginRetireType', 0x44f102, EDX=2, EAX=di, EBX=m.u16(rec + 0x84))
                m.u8(rec + 0x8b, 0xa)
                return r['EAX']
            return modo
        b2 = m.u16(rec + 0xb2)
        if b2 == 0xffff:
            alvo = self._rec(di)
            if m.u8(alvo + 2) in (0, 4):
                return 0
            u = r['EDI'] & 0xffff
            pool = self._pool()
            m.u8((pool + u * PASSO + 2) & M32, 7)
            if self._dono(u):
                self._liberar_busca()
            return pool
        k42 = (m.u8(rec + 0x84) + 0x42) & 0xff
        self._chamar(r, 'ChercheVegetLibre', 0x44f136, pilha=(di,), EBP=di, EBX=k42, EDX=5, ECX=k42, EAX=b2)
        achado = r['EAX'] & 0xffff
        ebp = (r['EBP'] * PASSO) & M32
        if achado == 0xffff:
            pool = self._pool()
            if m.u8((pool + ebp + 2) & M32) in (0, 4):
                return 0
            m.u8((pool + di * PASSO + 2) & M32, 7)
            if self._dono(di):
                self._liberar_busca()
                return pool & 0xffffff00
            return pool
        if achado == m.u16(rec + 0x80):
            return r['EAX']
        m.u8(rec + 0x89, 0)
        novo = (self._pool() + ebp) & M32
        m.u16(novo + 0x7e, achado)
        if self._dono(di):
            self._liberar_busca()
        m.u8(novo + 0x88, 0)
        return r['EAX']

    # ------------------------------------------------------------ dispatch by original name
    def chamar(self, nome, regs):
        """Run routine ``nome`` with entry registers ``regs`` (EAX..EBP and ESP)."""
        f = {'CalculTransporteEngin': self.calcul_transporte_engin,
             'EnginCalculTransporte': self.engin_calcul_transporte,
             'CalculDechargeCaveEngin': self.calcul_decharge_cave_engin}.get(nome)
        if f is None:
            raise KeyError(f'{nome} is not a translated transport routine')
        self.incertos = {}
        entrada = {k: regs[k] & M32 for k in REG7}
        entrada['ESP'] = regs.get('ESP', 0) & M32
        saida = f(entrada)
        if nome == 'EnginCalculTransporte' and self.incertos.get('EAX'):
            saida['_incertos'] = {'EAX': self.incertos['EAX']}
        return saida


def provedor_transporte(transporte, outros=None):
    """``externo(nome, chamada, registradores) -> registradores`` serving CalculTransporteEngin (EnginNextEtape
    0x455e28), EnginCalculTransporte and CalculDechargeCaveEngin (0x455d1c) in the shape of Core's providers: a
    register of ``ARGUMENTOS_EXIGIDOS`` that is missing raises ``ArgumentoNaoPassado`` before anything runs; any other
    missing register enters as 0 and, when the routine returns it unchanged, comes back in ``_incertos``. Other names
    go to ``outros`` or raise ``DependenciaTransporte``."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise DependenciaTransporte(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        faltando = [k for k in ARGUMENTOS_EXIGIDOS[nome] if k not in regs]
        if faltando:
            from entrada_estruturas import ArgumentoNaoPassado
            raise ArgumentoNaoPassado(nome, chamada, faltando)
        entrada = {k: regs.get(k, 0) & M32 for k in REG7}
        entrada['ESP'] = regs.get('ESP', 0) & M32
        saida = transporte.chamar(nome, entrada)
        resultado = {k: saida[k] & M32 for k in REG7}
        incertos = {k: M32 for k in REG7 if k not in regs and resultado[k] == entrada[k]}
        for k, v in (saida.get('_incertos') or {}).items():
            incertos[k] = incertos.get(k, 0) | v
        if incertos:
            resultado['_incertos'] = incertos
        return resultado
    return externo
