"""Work cycle and lodging credit over live original memory (M3/M4 economy row).

Translated from the intact bytes after the native capture
``evidencias/ciclo-trabalho/captura-ciclo-trabalho-exibicao.json.xz`` was committed. Routines:
- CalculWorkEngin 0x44bc74 (unit state 5) for unit types 5 (food) and 7 (stone), every phase +0x89;
- the mine and field leaves it calls: MineGetIndice 0x47544c, MineEstSurTerrain 0x475402,
  MineSetWork 0x4754a7, MineEndWork 0x4754de, MineRecolte 0x4755a7, TerrainRecolte 0x4781e8;
- AjouteMatiere 0x4678f2 (the only writer of a player total that is not a debit);
- BatimentLogeEngin 0x41f76e for every unit type but 10 (the colonist/troop lodging, its cargo credit and
  the 0xc8 -> player hand-over of a structure).

Calling convention. Each routine takes its entry registers EAX..EBP plus ESP (the return slot) and returns
EAX..EBP and ESP after its RET as the original leaves them; arithmetic flags are not modeled. ``memoria``
is the flat interface of ``memoria_quadro_core.MemoriaQuadro``.

Named dependencies (never defaulted). A callee owned elsewhere goes through ``externo(nome, chamada,
registradores) -> registradores``: ``chamada`` is the original call address; ``registradores`` holds the
argument registers the callee reads, at the widths of ``ARGUMENTOS`` (other bits are not modeled); the
provider returns EAX..EBP as the callee leaves them, after making its stores. Without a provider the path
raises ``DependenciaCicloTrabalho`` at that call, after the stores the original made before it. A routine
of this module listed in ``proprias`` runs here instead (default: all of them).

Branches outside the translated domain raise ``ForaDoDominioTrabalho`` at their original address before
any store of that branch: depot mode 1 (sacks dropped on a cell: Ctrl + a ground press), other unit types in
CalculWorkEngin, a depleted mine, the builder idling off its mine, and type-10 units in BatimentLogeEngin.
"""
M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
ESTRUTURAS = 0x49a0c8
JOGADOR_LOCAL, CONTADOR = 0x508041, 0x508f7c
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
TIPOS_UNIDADE = 0x4965c0             # 50-byte records; the work timer word is +0x1e (0x4965de + 50 * type)
TOTAIS = 0x4e2eaa                    # player * 32 + resource * 8: u16 total (+2 of the record)
MINAS = 0x509954                     # 20 x (u16 origin, u16 reserve)
GRADE_OBJETOS, GRADE_MOSAICOS, GRADE_TRABALHO = 0x507d74, 0x507d70, 0x507dac
ROTINAS = {
    'CalculWorkEngin': 0x44bc74, 'MineGetIndice': 0x47544c, 'MineEstSurTerrain': 0x475402,
    'MineSetWork': 0x4754a7, 'MineEndWork': 0x4754de, 'MineRecolte': 0x4755a7, 'TerrainRecolte': 0x4781e8,
    'AjouteMatiere': 0x4678f2, 'BatimentLogeEngin': 0x41f76e, 'BatimentAjouteMatiere': 0x42340f,
}
INTERNAS = ('GetRessourceStock',)    # callees whose effect is computed inline (outputs to the caller's frame)
CAVES = 0x4dfb2c                     # per player (stride 6): u16 cave count, u16 per-cave capacity, u8 level
RECURSOS = 0x4e2ea8                  # per player (stride 32): 4 records of u16 RMI, u16 total, u16, u16
# Argument registers each external callee reads, with the bits it reads.
ARGUMENTOS = {
    'DeplaceEngin': {'EAX': 0xffff}, 'SetDeplaceEngin': {'EAX': 0xffff, 'EDX': 0xffff},
    'BatimentGetCase': {'EAX': 0xffff}, 'GetCaseCentrale': {'EAX': 0xffff},
    'BatimentAdjacent': {'EAX': 0xffff, 'EDX': 0xffff}, 'TerrainEstGc': {'EAX': 0xffff},
    'ChercheGcLibre': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xffff}, 'ChercheGc': {'EAX': 0xffff, 'EDX': 0xffff},
    'Random': {'EAX': M32}, 'AnimWorkEngin': {'EAX': 0xffff}, 'RetireEngin': {'EAX': 0xffff, 'EBX': 0xff},
    'BonusGetValEngin': {'EAX': 0xff, 'EBX': 0xff, 'EDX': 0xff}, 'TerrainEstDecouvert': {'EAX': 0xffff, 'EDX': 0xff},
    'EnginGetVolume': {'EAX': 0xffff}, 'PlaySnd_PostSound': {'EAX': M32, 'EDX': M32, 'EBX': M32, 'ECX': M32},
    'EnginPeutPasser': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff, 'ECX': 0xff},
    'SetEnginCollision': {'EAX': 0xffff, 'EDX': 0xffff}, 'DecouvreTerrain': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff},
    'IllumineTerrain': {'EAX': 0xffff, 'EDX': 0xffff, 'EBX': 0xff}, 'SetMiniMap': {'EAX': 0xff, 'EBX': 0xffff, 'EDX': 0xff},
    'BagContient': {'EAX': M32, 'EDX': 0xff, 'EBX': 0xffff}, 'BagRetire': {'EAX': M32, 'EDX': 0xff, 'EBX': 0xffff},
    'BatimentAjouteMatiere': {'EAX': 0xff, 'EDX': 0xffff, 'EBX': 0xff, 'ECX': 0xffff},
    'MineGetCapacite': {'EAX': 0xffff},
    'EnginGetType': {'EAX': 0xffff}, 'EnginGetPlayer': {'EAX': 0xffff}, 'BagContientTroupe': {'EAX': M32},
    'PlaceLibre': {'EAX': 0xffff, 'EDX': 0xffff}, 'EnginGetBag': {'EAX': 0xffff},
    'BatimentHabitable': {'EAX': 0xffff, 'EDX': 0xff}, 'BatimentModifyMap': {'EAX': 0xffff},
    'InitBatimentPlayer': {'EAX': 0xffff, 'EDX': 0xff}, 'BatimentGetVolume': {'EAX': 0xffff},
    'BagPrend': {'EAX': M32, 'EDX': 0xff, 'EBX': 0xffff},
    'TerrainDeposeSac': {'EAX': 0xffff, 'EDX': 0xff, 'EBX': 0xffff},
}
PILHA_EXTERNA = {'PlaySnd_PostSound': 1}   # one pushed word, popped by the callee


class DependenciaCicloTrabalho(NotImplementedError):
    """A callee owned elsewhere was reached without its provider."""
    def __init__(self, rotina, chamada, motivo='provider required'):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: {motivo}')


class ForaDoDominioTrabalho(NotImplementedError):
    """A branch outside the translated domain; nothing was written by it."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made by this branch')


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


def _idiv(a, b):
    """x86 IDIV quotient (truncation toward zero) of 32-bit signed values."""
    a, b = _s32(a), _s32(b)
    q = abs(a) // abs(b)
    return (q if (a < 0) == (b < 0) else -q) & M32


class CicloTrabalho:
    def __init__(self, memoria, *, externo=None, proprias=None):
        self.m = memoria
        self.externo = externo
        self.proprias = set(ROTINAS) if proprias is None else set(proprias)

    # ------------------------------------------------------------ helpers
    def _ext(self, nome, chamada, pilha=(), **regs):
        """Call ``nome`` at ``chamada``: this module's routine when it is in ``proprias``, else ``externo``.
        Returns the callee's exit registers EAX..EBP."""
        if nome in self.proprias and nome in ROTINAS:
            entrada = {k: regs.get(k, 0) & M32 for k in REG7}
            entrada['ESP'] = 0
            saida = getattr(self, '_' + nome)(entrada)
            return {k: saida[k] & M32 for k in REG7}
        if self.externo is None:
            raise DependenciaCicloTrabalho(nome, chamada)
        larguras = ARGUMENTOS[nome]
        entrada = {k: regs[k] & larguras[k] for k in larguras}
        if pilha:
            entrada['_pilha'] = list(pilha)
        saida = self.externo(nome, chamada, entrada)
        return {k: saida[k] & M32 for k in REG7 if k in saida}

    def _reg(self, u):
        return (self.m.u32(PONTEIRO_UNIDADES) + PASSO * u) & M32

    def _liberar_busca(self):
        self.m.u8(BUSCA_OCUPADA, 0)
        self.m.u8(BUSCA_SUCESSO, 0)
        self.m.u32(BUSCA_ROTA, 0)
        self.m.u16(BUSCA_UNIDADE, 0xffff)

    def _destino(self, u, rec, valor):
        """+0x7e := valor; the path search is released when it belongs to the unit. True when released."""
        self.m.u16(rec + 0x7e, valor)
        if u == self.m.u16(BUSCA_UNIDADE):
            self._liberar_busca()
            return True
        return False

    def _tem_lugar(self, rec):
        """Bag at +0xa has room for one more: u16 +0x66 + 1 <= u16 capacity +2."""
        return self.m.u16(rec + 0xa + 0x66) + 1 <= self.m.u16(rec + 0xa + 2)

    def _palavra_tempo(self, tipo):
        return self.m.u16(TIPOS_UNIDADE + 0x1e + 50 * tipo)

    def _ociosa(self, rec, u):
        """State := 7 unless the state is 0 or 4. (stored, released)."""
        if self.m.u8(rec + 2) in (0, 4):
            return False, False
        self.m.u8(rec + 2, 7)
        if u == self.m.u16(BUSCA_UNIDADE):
            self._liberar_busca()
            return True, True
        return True, False

    def _som_trabalho(self, rec, u, chamadas):
        """The 'cannot work here' voice: owner local and cell discovered -> EnginGetVolume, +0xf9 := 0, and when
        +0x104 = -1 PlaySnd_PostSound(0x50, type << 16 | 0x1000, rec + 0x104, 0, push 0x100)."""
        local = self.m.u8(JOGADOR_LOCAL)
        if self.m.u8(rec) != local:
            return
        r = self._ext('TerrainEstDecouvert', chamadas[0], EAX=self.m.u16(rec + 8), EDX=local)
        if r['EAX'] & 0xff == 0:
            return
        self._ext('EnginGetVolume', chamadas[1], EAX=u)
        self.m.u8(rec + 0xf9, 0)
        if self.m.u32(rec + 0x104) != M32:
            return
        self._ext('PlaySnd_PostSound', chamadas[2], pilha=(0x100,), EAX=0x50,
                  EDX=(self.m.u8(rec + 1) << 16) | 0x1000, EBX=rec + 0x104, ECX=0)

    def _bonus_tempo(self, rec, chamada):
        """BonusGetValEngin(owner, type, 3) and the timer byte: table byte - bonus low byte. Returns EAX."""
        tipo = self.m.u8(rec + 1)
        b = self._ext('BonusGetValEngin', chamada, EAX=self.m.u8(rec), EBX=tipo, EDX=3)['EAX']
        al = (self.m.u8(TIPOS_UNIDADE + 0x1e + 50 * tipo) - b) & 0xff
        return (b & 0xffffff00) | al

    def _adicionar_bolsa(self, bolsa, valor):
        """Inline Bag append of CalculWorkEngin: +0x66 += 1, tag 2 and value at the count, count += 1."""
        n = self.m.u16(bolsa)
        self.m.u16(bolsa + 0x66, self.m.u16(bolsa + 0x66) + 1)
        self.m.u8(bolsa + n + 0x42, 2)
        self.m.u16(bolsa + 6 + 2 * n, valor)
        self.m.u16(bolsa, n + 1)
        return n

    @staticmethod
    def _sair(regs, eax):
        saida = {k: regs[k] & M32 for k in REG7}
        saida['EAX'] = eax & M32
        saida['ESP'] = (regs['ESP'] + 4) & M32
        return saida

    # ------------------------------------------------------------ leaves
    def _MineGetIndice(self, regs):
        """MineGetIndice 0x47544c: AX cell -> EAX = first mine (of 20) with a nonzero origin o and cell in
        {o, o+1, o+0x100, o+0x101} (no 16-bit wrap), else 0xffff."""
        c = regs['EAX'] & 0xffff
        for i in range(20):
            o = self.m.u16(MINAS + 4 * i)
            if o and c in (o, o + 1, o + 0x100, o + 0x101):
                return self._sair(regs, i)
        return self._sair(regs, 0xffff)

    def _MineEstSurTerrain(self, regs):
        """MineEstSurTerrain 0x475402: tile word of the cell is 0x253/0x254 -> AL = 1."""
        t = self.m.u16(self.m.u32(GRADE_MOSAICOS) + 2 * (regs['EAX'] & 0xffff))
        return self._sair(regs, (t & 0xff00) | (1 if t in (0x253, 0x254) else 0))

    def _trabalho(self, regs, delta):
        i = self._MineGetIndice(dict(regs))['EAX'] & 0xffff
        if i == 0xffff:
            return self._sair(regs, 0xffff)
        o = self.m.u16(MINAS + 4 * i)
        base = self.m.u32(GRADE_TRABALHO)
        for d in (0, 1):
            self.m.u8(base + o + d, self.m.u8(base + o + d) + delta)
        return self._sair(regs, base)

    def _MineSetWork(self, regs):
        """MineSetWork 0x4754a7: the work bytes of the mine's two origin cells (grid [0x507dac]) += 1."""
        return self._trabalho(regs, 1)

    def _MineEndWork(self, regs):
        """MineEndWork 0x4754de: the same two bytes -= 1."""
        return self._trabalho(regs, -1)

    def _MineRecolte(self, regs):
        """MineRecolte 0x4755a7: AX cell. Unknown mine -> EAX 0. Reserve > 1: reserve -= 1, EAX 1. Otherwise the
        reserve becomes 0, the origin tiles become 0x1db/0x1dc and EAX = the old reserve over entry EBX's upper half."""
        i = self._MineGetIndice(dict(regs, EAX=regs['EAX'] & 0xffff))['EAX'] & 0xffff
        if i == 0xffff:
            return self._sair(regs, 0)
        reserva = self.m.u16(MINAS + 4 * i + 2)
        if reserva > 1:
            self.m.u16(MINAS + 4 * i + 2, reserva - 1)
            return self._sair(regs, 1)
        self.m.u16(MINAS + 4 * i + 2, 0)
        o = self.m.u16(MINAS + 4 * i)
        grade = self.m.u32(GRADE_MOSAICOS)
        self.m.u16(grade + 2 * o, 0x1db)
        self.m.u16(grade + 2 * o + 2, 0x1dc)
        return self._sair(regs, (regs['EBX'] & 0xffff0000) | reserva)

    def _TerrainRecolte(self, regs):
        """TerrainRecolte 0x4781e8: AX cell, object byte g of grid [0x507d74]. Outside 0x1d..0x34: no change,
        EAX = g. 0x33/0x34: g -= 10, EAX = grid + cell. Otherwise g := 0, EAX = grid."""
        c = regs['EAX'] & 0xffff
        grade = self.m.u32(GRADE_OBJETOS)
        g = self.m.u8(grade + c)
        if not 0x1d <= g < 0x35:
            return self._sair(regs, g)
        if g >= 0x33:
            self.m.u8(grade + c, g - 10)
            return self._sair(regs, grade + c)
        self.m.u8(grade + c, 0)
        return self._sair(regs, grade)

    def _AjouteMatiere(self, regs):
        """AjouteMatiere 0x4678f2: AL resource, BX player, DX quantity. Total (+2 of record (BX*4 + AL)*8) :=
        low 16 bits of total + EDX, then 9999 when that u16 exceeds 9999. EAX = record offset; EBX = the 32-bit
        sum over (BX*4)'s upper half; EDX = the u16 sum (before the clamp)."""
        bx4 = ((regs['EBX'] & 0xffff) << 2) & M32
        o = (((regs['EAX'] & 0xff) + bx4) << 3) & M32
        ebx = (((bx4 & 0xffff0000) | self.m.u16(TOTAIS + o)) + regs['EDX']) & M32
        total = ebx & 0xffff
        self.m.u16(TOTAIS + o, total)
        if total > 9999:
            self.m.u16(TOTAIS + o, 9999)
        saida = self._sair(regs, o)
        saida.update(EBX=ebx, EDX=total)
        return saida

    # ------------------------------------------------------------ CalculWorkEngin
    def calcul_work_engin(self, regs):
        return self._CalculWorkEngin(dict(regs))

    def _CalculWorkEngin(self, regs):
        """CalculWorkEngin 0x44bc74: AX unit. Only EAX changes (epilogue 0x44f29d -> 0x440d58)."""
        u = regs['EAX'] & 0xffff
        rec = self._reg(u)
        tipo = self.m.u8(rec + 1)
        eax0 = regs['EAX'] & 0xffff00ff
        if tipo not in (5, 6, 7, 13):
            return self._sair(regs, eax0)
        if tipo in (6, 13):
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44cde4 if tipo == 6 else 0x44d85b, f'unit type {tipo}')
        fase = self.m.u8(rec + 0x89)
        if tipo == 5:
            if fase > 3:
                return self._sair(regs, (eax0 & 0xffff0000) | fase)
            return self._sair(regs, (self._comida0, self._comida1, self._comida2, self._comida3)[fase](u, rec))
        if fase > 5:
            return self._sair(regs, (eax0 & 0xffff0000) | fase)
        return self._sair(regs, (self._pedra0, self._pedra1, self._pedra2, self._pedra3, self._pedra4,
                                 self._pedra5)[fase](u, rec))

    def _andar(self, u, chamada=0x44bd16):
        return self._ext('DeplaceEngin', chamada, EAX=u)['EAX']

    # ---- type 5 (food)
    def _comida0(self, u, rec):
        """Phase 0 0x44d880: walk to the field; on a TerrainEstGc cell start harvesting (phase 1, timer);
        elsewhere look for a free field around (ChercheGcLibre radius 5) or, if none, call the voice and send the
        unit to its depot. A full Bag goes straight to phase 1."""
        if not self._tem_lugar(rec):
            self.m.u8(rec + 0x89, 1)
            return self._comida_tempo(rec, 0x44d8f7)
        celula = self.m.u16(rec + 8)
        if self.m.u16(rec + 0x7e) != celula:
            return self._andar(u)
        if self._ext('TerrainEstGc', 0x44d8cd, EAX=celula)['EAX'] & 0xff:
            self.m.u8(rec + 0x89, 1)
            return self._comida_tempo(rec, 0x44d8f7)
        r = self._ext('ChercheGcLibre', 0x44d928, EAX=celula, EDX=5, EBX=u)['EAX']
        if r & 0xffff != 0xffff:
            self._destino(u, rec, r)
            self.m.u8(rec + 0x88, 0)
            self.m.u16(rec + 0xb2, r)
            return r
        self._som_trabalho(rec, u, (0x44d9a6, 0x44d9b1, 0x44d9e5))
        modo = self.m.u8(rec + 0x82)
        if modo == 2:
            c = self._ext('GetCaseCentrale', 0x44da02, EAX=self.m.u16(rec + 0x80), EDX=0)['EAX']
            return self._ext('SetDeplaceEngin', 0x44da0f, EAX=u, EDX=c)['EAX']
        if modo == 1:
            return self._ext('SetDeplaceEngin', 0x44da0f, EAX=u, EDX=self.m.u16(rec + 0x80))['EAX']
        return modo

    def _comida_tempo(self, rec, chamada):
        self.m.u8(rec + 0xa4, 0)
        eax = self._bonus_tempo(rec, chamada)
        self.m.u8(rec + 0x8b, eax)
        return eax

    def _comida1(self, u, rec):
        """Phase 1 0x44da5d: harvest. Each frame AnimWorkEngin and timer -= 1; at 0 TerrainRecolte on the cell
        and one food entry (tag 2, value 1) is appended, a second one when room remains and bonus selector 7 is
        nonzero. Then a nearby field is chosen (Random x2, ChercheGc radius 5): with room left the unit goes there
        (phase 0); otherwise (or with no field) the Bag is full and the depot decides."""
        bolsa = rec + 0xa
        cheia = not self._tem_lugar(rec)
        if not cheia:
            self._ext('AnimWorkEngin', 0x44da95, EAX=u)
            t = (self.m.u8(rec + 0x8b) - 1) & 0xff
            self.m.u8(rec + 0x8b, t)
            if t:
                return t
            celula = self.m.u16(rec + 8)
            self._ext('TerrainRecolte', 0x44dabb, EAX=celula, ECX=bolsa)
            self._adicionar_bolsa(bolsa, 1)
            if self.m.u16(bolsa + 0x66) + 1 <= self.m.u16(bolsa + 2):
                b = self._ext('BonusGetValEngin', 0x44db0a, EAX=self.m.u8(rec), EBX=self.m.u8(rec + 1), EDX=7)
                if b['EAX'] & 0xffff:
                    self._adicionar_bolsa(bolsa, 1)
            r1 = self._ext('Random', 0x44db44, EAX=0x1b, EBX=5, ECX=celula, EDX=0)
            ecx = (celula + (((r1['EDX'] << 32) | r1['EAX']) % 5)) & M32
            r2 = self._ext('Random', 0x44db54, EAX=0x1c, EBX=5, ECX=ecx, EDX=0)
            d2 = ((r2['EDX'] << 32) | r2['EAX']) % 5
            alvo = (((d2 << 8) - 0x200) + ecx - 2) & 0xffff
            g = self._ext('ChercheGc', 0x44db70, EAX=alvo, EDX=5)['EAX']
            if g & 0xffff != 0xffff and self.m.u16(bolsa + 0x66) + 1 <= self.m.u16(bolsa + 2):
                self.m.u8(rec + 0xa4, 0)
                liberou = self._destino(u, rec, g)
                self.m.u8(rec + 0x88, 0)
                self.m.u8(rec + 0x89, 0)
                self.m.u16(rec + 0xb2, g)
                return 0xffff if liberou else 1
        return self._comida_deposito(u, rec)

    def _comida_deposito(self, u, rec):
        """0x44dc1c: the Bag is full. Mode 2: +0xc0 := +0x80, go to BatimentGetCase(+0xc0), phase 2 (a 0xffff
        structure makes the unit idle). Mode 1: outside the domain. Other modes: the unit becomes idle (state 7)
        with its cargo."""
        modo = self.m.u8(rec + 0x82)
        if modo == 2:
            alvo = self.m.u16(rec + 0x80)
            self.m.u16(rec + 0xc0, alvo)
            if alvo == 0xffff:
                pool = self.m.u32(PONTEIRO_UNIDADES)
                feito, liberou = self._ociosa(rec, u)
                return 0 if not feito else (pool & 0xffff00ff if liberou else pool)
            c = self._ext('BatimentGetCase', 0x44dc4b, EAX=alvo)['EAX']
            self.m.u8(rec + 0x89, 2)
            self._destino(u, rec, c)
            self.m.u8(rec + 0x88, 0)
            return u
        if modo == 1:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44dd3b, 'depot mode 1 (sacks on a cell)')
        pool = self.m.u32(PONTEIRO_UNIDADES)
        feito, liberou = self._ociosa(rec, u)
        return 0 if not feito or liberou else pool

    def _comida2(self, u, rec):
        """Phase 2 0x44df0c: carry to the depot structure; adjacent (and not pushed) -> phase 3 with timer
        word / 5; otherwise walk, re-aiming at BatimentGetCase(+0x80) on arrival."""
        modo = self.m.u8(rec + 0x82)
        if modo == 2:
            if self._adjacente(rec, 0x44df44):
                self.m.u8(rec + 0x89, 3)
                eax = _idiv(self._palavra_tempo(self.m.u8(rec + 1)), 5)
                self.m.u8(rec + 0x8b, eax)
                return eax
            if self.m.u16(rec + 8) != self.m.u16(rec + 0x7e):
                return self._andar(u)
            c = self._ext('BatimentGetCase', 0x44df64, EAX=self.m.u16(rec + 0x80))['EAX']
            liberou = self._destino(u, rec, c)
            self.m.u8(rec + 0x88, 0)
            return u & 0xff00 if liberou else u
        if modo == 1:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44dfed, 'depot mode 1 (sacks on a cell)')
        return modo

    def _adjacente(self, rec, chamada):
        """Signed bytes +0x86/+0x87 both zero and BatimentAdjacent(+0xc0, cell)."""
        if self.m.u8(rec + 0x86) or self.m.u8(rec + 0x87):
            return False
        return bool(self._ext('BatimentAdjacent', chamada, EAX=self.m.u16(rec + 0xc0), EDX=self.m.u16(rec + 8))['EAX'] & 0xff)

    def _comida3(self, u, rec):
        """Phase 3 0x44e186: unload. Timer -= 1; at 0, while a food entry (tag 2 value 1) remains: mode 2 ->
        BatimentAjouteMatiere(food, 1, owner, +0x80), BagRetire one entry, timer 0x32. With no food left the unit
        returns to +0xb2 (phase 0) or, with no work cell, becomes idle."""
        t = (self.m.u8(rec + 0x8b) - 1) & 0xff
        self.m.u8(rec + 0x8b, t)
        if t:
            return t
        bolsa = rec + 0xa
        if self._ext('BagContient', 0x44e1ad, EAX=bolsa, EDX=2, EBX=1)['EAX'] & 0xffff:
            modo = self.m.u8(rec + 0x82)
            if modo == 2:
                self._ext('BatimentAjouteMatiere', 0x44e1da, EAX=1, EDX=1, EBX=self.m.u8(rec), ECX=self.m.u16(rec + 0x80))
                eax = self._ext('BagRetire', 0x44e1ec, EAX=bolsa, EDX=2, EBX=1)['EAX']
                self.m.u8(rec + 0x8b, 0x32)
                return eax
            if modo == 1:
                raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44e207, 'depot mode 1 (sacks on a cell)')
            return modo
        return self._voltar_trabalho(u, rec, 0x44e22e)

    def _voltar_trabalho(self, u, rec, endereco):
        b2 = self.m.u16(rec + 0xb2)
        if b2 != 0xffff:
            self.m.u8(rec + 0x89, 0)
            liberou = self._destino(u, rec, b2)
            self.m.u8(rec + 0x88, 0)
            return b2 & 0xff00 if liberou else b2
        pool = self.m.u32(PONTEIRO_UNIDADES)
        feito, liberou = self._ociosa(rec, u)
        return 0 if not feito or liberou else pool

    # ---- type 7 (stone)
    def _pedra0(self, u, rec):
        """Phase 0 0x44bcd5: walk below the mine (+0x7e); there, with +0xb2 the current cell and the mine tile
        under it, MineSetWork, RetireEngin (the unit goes in), phase 1 and the timer. A full Bag goes to the
        depot (mode 2: GetCaseCentrale(+0x80), phase 3)."""
        if not self._tem_lugar(rec):
            modo = self.m.u8(rec + 0x82)
            if modo == 0:
                return 0
            if modo != 2:
                raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44bf78 if modo == 1 else 0x44bfef,
                                            f'depot mode {modo} with a full Bag')
            self.m.u16(rec + 0xc0, self.m.u16(rec + 0x80))
            t = self._ext('GetCaseCentrale', 0x44bf6a, EAX=self.m.u16(rec + 0x80))['EAX']
            if t & 0xffff != 0xffff:
                self.m.u8(rec + 0x89, 3)
                liberou = self._destino(u, rec, t)
                self.m.u8(rec + 0x88, 0)
                return t & 0xffff00ff if liberou else t
            pool = self.m.u32(PONTEIRO_UNIDADES)
            feito, _ = self._ociosa(rec, u)
            return pool if feito else 0
        celula = self.m.u16(rec + 8)
        if self.m.u16(rec + 0x7e) != celula:
            return self._andar(u)
        b2 = self.m.u16(rec + 0xb2)
        if celula != b2:
            self._destino(u, rec, b2)
            self.m.u8(rec + 0x88, 0)
            return ((rec + 0xa) & 0xffff0000) | b2
        if not self._ext('MineEstSurTerrain', 0x44bd36, EAX=celula)['EAX'] & 0xff:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44bd8a, 'builder below a cell that is not a mine tile')
        self._ext('MineSetWork', 0x44bd45, EAX=celula)
        self._ext('RetireEngin', 0x44bd51, EAX=u, EBX=0)
        self.m.u8(rec + 0x89, 1)
        eax = self._bonus_tempo(rec, 0x44bd77)
        self.m.u8(rec + 0x8b, eax)
        return eax

    def _pedra1(self, u, rec):
        """Phase 1 0x44c0e3: inside the mine. AnimWorkEngin, timer -= 1; at 0 with room MineRecolte: one stone
        entry (tag 2, value 2), timer 0x32; a full Bag -> phase 2."""
        self._ext('AnimWorkEngin', 0x44c0e8, EAX=u)
        t = (self.m.u8(rec + 0x8b) - 1) & 0xff
        self.m.u8(rec + 0x8b, t)
        if t:
            return t
        bolsa = rec + 0xa
        if not self._tem_lugar(rec):
            self.m.u8(rec + 0x89, 2)
            return self.m.u16(bolsa + 2) & 0xff00
        r = self._ext('MineRecolte', 0x44c14b, EAX=self.m.u16(rec + 8), EBX=self.m.u16(bolsa + 0x66) + 1)
        if not r['EAX'] & 0xffff:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44c181, 'depleted mine')
        n = self._adicionar_bolsa(bolsa, 2)
        self.m.u8(rec + 0x8b, 0x32)
        return n

    def _pedra2(self, u, rec):
        """Phase 2 0x44c33b: leave the mine when the cell is free, then mode 2 -> GetCaseCentrale(+0x80),
        phase 3; mode 0 -> idle with the cargo."""
        celula = self.m.u16(rec + 8)
        r = self._ext('EnginPeutPasser', 0x44c34d, EAX=u, EDX=celula, EBX=1, ECX=0)
        if not r['EAX'] & 0xff:
            return r['EAX']
        self._ext('MineEndWork', 0x44c360, EAX=celula)
        self._ext('SetEnginCollision', 0x44c38b, EAX=u, EDX=celula)
        self.m.u8(rec + 0x72, 1)
        dono = self.m.u8(rec)
        if dono not in (0xc8, 4):
            raio = (self.m.u8(rec + 0xbb) + self.m.u8(rec + 0xf5)) & 0xffff
            self._ext('DecouvreTerrain', 0x44c3f5, EAX=celula, EDX=raio + 2, EBX=dono)
            self._ext('IllumineTerrain', 0x44c422, EAX=celula, EDX=raio, EBX=dono)
        self._ext('SetMiniMap', 0x44c437, EAX=dono, EBX=celula, EDX=4)
        modo = self.m.u8(rec + 0x82)
        if modo == 0:
            pool = self.m.u32(PONTEIRO_UNIDADES)
            feito, liberou = self._ociosa(rec, u)
            return 0 if not feito else (pool & 0xffffff00 if liberou else pool)
        if modo == 1:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44c4ac, 'depot mode 1 (sacks on a cell)')
        if modo != 2:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44c523, f'depot mode {modo}')
        self.m.u16(rec + 0xc0, self.m.u16(rec + 0x80))
        t = self._ext('GetCaseCentrale', 0x44c49e, EAX=self.m.u16(rec + 0x80))['EAX']
        if t & 0xffff != 0xffff:
            self.m.u8(rec + 0x89, 3)
            liberou = self._destino(u, rec, t)
            self.m.u8(rec + 0x88, 0)
            return 0 if liberou else t & 0xffff
        pool = self.m.u32(PONTEIRO_UNIDADES)
        feito, _ = self._ociosa(rec, u)
        return pool if feito else 0

    def _pedra3(self, u, rec):
        """Phase 3 0x44c660: carry the stone; adjacent -> phase 4, timer 0x32; else walk / re-aim."""
        modo = self.m.u8(rec + 0x82)
        if modo == 2:
            if self.m.u8(rec + 0x86) == 0 and self.m.u8(rec + 0x87) == 0:
                r = self._ext('BatimentAdjacent', 0x44c698, EAX=self.m.u16(rec + 0xc0), EDX=self.m.u16(rec + 8))
                if r['EAX'] & 0xff:
                    self.m.u8(rec + 0x89, 4)
                    self.m.u8(rec + 0x8b, 0x32)
                    return r['EAX']
            if self.m.u16(rec + 8) != self.m.u16(rec + 0x7e):
                return self._andar(u)
            c = self._ext('BatimentGetCase', 0x44c6b8, EAX=self.m.u16(rec + 0x80))['EAX']
            liberou = self._destino(u, rec, c)
            self.m.u8(rec + 0x88, 0)
            return u
        if modo == 1:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44c729, 'depot mode 1 (sacks on a cell)')
        return modo

    def _pedra4(self, u, rec):
        """Phase 4 0x44c8c0: unload. Timer -= 1; at 0 with a stone entry: BagRetire it, then
        BatimentAjouteMatiere(stone, 1, owner, +0x80) and timer = word / 2; no stone left -> phase 5."""
        modo = self.m.u8(rec + 0x82)
        if modo == 1:
            raise ForaDoDominioTrabalho('CalculWorkEngin', 0x44c970, 'depot mode 1 (sacks on a cell)')
        if modo != 2:
            return modo
        t = (self.m.u8(rec + 0x8b) - 1) & 0xff
        self.m.u8(rec + 0x8b, t)
        if t:
            return t
        bolsa = rec + 0xa
        r = self._ext('BagContient', 0x44c8f5, EAX=bolsa, EDX=2, EBX=2)
        if not r['EAX'] & 0xffff:
            self.m.u8(rec + 0x89, 5)
            return r['EAX']
        self._ext('BagRetire', 0x44c90b, EAX=bolsa, EDX=2, EBX=2, ECX=0)
        self._ext('BatimentAjouteMatiere', 0x44c925, EAX=2, EDX=1, EBX=self.m.u8(rec), ECX=self.m.u16(rec + 0x80))
        w = self._palavra_tempo(self.m.u8(rec + 1))
        eax = ((w - (w >> 31)) >> 1) & M32
        self.m.u8(rec + 0x8b, eax)
        return eax

    def _pedra5(self, u, rec):
        """Phase 5 0x44c9bb: back to work. Mode 2 waits for EnginPeutPasser, clears +0xc0 and returns to +0xb2
        (phase 0) while its mine has reserve; otherwise (or without a work cell) the unit idles and +0x82 := 0."""
        modo = self.m.u8(rec + 0x82)
        b2 = self.m.u16(rec + 0xb2)
        if modo == 2:
            r = self._ext('EnginPeutPasser', 0x44c9de, EAX=u, EDX=self.m.u16(rec + 8), EBX=1, ECX=0)
            if not r['EAX'] & 0xff:
                return r['EAX']
            self.m.u16(rec + 0xc0, 0xffff)
            if b2 != 0xffff:
                i = self._ext('MineGetIndice', 0x44ca0d, EAX=b2)['EAX'] & 0xffff
                cap = self._ext('MineGetCapacite', 0x44ca17, EAX=i)['EAX'] & 0xffff
                if cap:
                    self.m.u8(rec + 0x89, 0)
                    liberou = self._destino(u, rec, b2)
                    self.m.u8(rec + 0x88, 0)
                    return b2 & 0xff if liberou else b2
            pool = self.m.u32(PONTEIRO_UNIDADES)
            feito, liberou = self._ociosa(rec, u)
            self.m.u8(rec + 0x82, 0)
            return 0 if not feito else (0xffff if liberou else pool)
        if b2 != 0xffff:
            self.m.u8(rec + 0x89, 0)
            self._destino(u, rec, b2)
            self.m.u8(rec + 0x88, 0)
            return self.m.u32(PONTEIRO_UNIDADES) + PASSO * u
        pool = self.m.u32(PONTEIRO_UNIDADES)
        feito, _ = self._ociosa(rec, u)
        self.m.u8(rec + 0x82, 0)
        return pool if feito else 0

    # ------------------------------------------------------------ BatimentAjouteMatiere
    def batiment_ajoute_matiere(self, regs):
        return self._BatimentAjouteMatiere(dict(regs))

    def _BatimentAjouteMatiere(self, regs):
        """BatimentAjouteMatiere 0x42340f: AL resource, DX quantity, BL player, CX structure.

        Structure type 4 is outside this translation (0x423511, the colonist hut). Otherwise, with the player's
        cave count (0x4dfb2c + 6p) zero, everything is excess. With caves: stock = food + stone stock
        (GetRessourceStock: total - RMI, u16), capacity = count * per-cave word (u16); a quantity above
        capacity - stock is cut there and the rest is excess. AjouteMatiere(resource, credit, player) adds to the
        total only, then the level byte = ((stock + credit) u16 // count * 7) // per-cave word. Excess goes to the
        ground as sacks next to a cave (type 3: origin + 0x202 food, + 3 stone) or a sanctuary (type 2: + 0x303)
        through TerrainDeposeSac; at other structures it is lost.

        Exit: ESI, EDI, EBP restored. ECX bits 16..31 are the caller-frame bytes GetRessourceStock leaves
        unwritten (``_incertos``); a zero per-cave word raises ZeroDivisionError after the credit."""
        recurso, qtd, jogador, s = regs['EAX'] & 0xff, regs['EDX'], regs['EBX'] & 0xff, regs['ECX'] & 0xffff
        est = ESTRUTURAS + PASSO * s
        tipo = self.m.u8(est + 8)
        if tipo == 4:
            raise ForaDoDominioTrabalho('BatimentAjouteMatiere', 0x423511, 'structure type 4')
        cave = CAVES + 6 * jogador
        incertos = {}
        if self.m.u16(cave) == 0:
            excesso = qtd
            r = dict(EAX=tipo, ECX=regs['ECX'], EDX=jogador)
        else:
            base = RECURSOS + 32 * jogador
            comida = (self.m.u16(base + 0xa) - self.m.u16(base + 8)) & 0xffff
            pedra = (self.m.u16(base + 0x12) - self.m.u16(base + 0x10)) & 0xffff
            estoque = (comida + pedra) & 0xffff               # ECX's low half; its upper half is frame garbage
            capacidade = (self.m.u16(cave) * self.m.u16(cave + 2)) & 0xffff
            excesso, credito = 0, qtd
            if (qtd & 0xffff) + estoque > capacidade:
                excesso = (qtd + estoque - capacidade) & M32
                credito = (capacidade - estoque) & M32
            self._ext('AjouteMatiere', 0x4234ce, EAX=recurso, EDX=credito & 0xffff, EBX=jogador)
            por = self.m.u16(cave + 2)
            q = ((estoque + credito) & 0xffff) // self.m.u16(cave)
            if por == 0:
                raise ZeroDivisionError('BatimentAjouteMatiere 0x423501: per-cave capacity word is zero')
            self.m.u8(cave + 4, (q * 7) // por)
            r = dict(EAX=(q * 7) // por, ECX=estoque, EDX=(q * 7) % por)
            incertos = {'ECX': 0xffff0000}
        sobra = excesso & 0xffff
        r['EBX'] = sobra
        if sobra and tipo in (2, 3):
            alvo = self.m.u16(est + 2) + (0x303 if tipo == 2 else 0x202 if recurso == 1 else 3)
            r = self._ext('TerrainDeposeSac', 0x4235b1, EAX=alvo & 0xffff, EDX=recurso, EBX=sobra)
            incertos = {}
        saida = {k: regs[k] & M32 for k in REG7}
        saida.update({k: r[k] & M32 for k in ('EAX', 'EBX', 'ECX', 'EDX')})
        saida['ESP'] = (regs['ESP'] + 4) & M32
        if incertos:
            saida['_incertos'] = incertos
        return saida

    # ------------------------------------------------------------ BatimentLogeEngin
    def batiment_loge_engin(self, regs):
        return self._BatimentLogeEngin(dict(regs))

    def _BatimentLogeEngin(self, regs):
        """BatimentLogeEngin 0x41f76e: AX structure, DX unit. AL = 1 when the unit was lodged.

        Type-10 units are outside this translation (0x41f7ab). Otherwise:
        1. Structure type 0x15 or 2 holding a troop (BagContientTroupe), or any other type holding a colonist
           (BagContient tag 1 type 9): the unit's player must own it, else AL = 0.
        2. PlaceLibre(structure, unit) = 0 -> AL = 0 (EAX = PlaceLibre's).
        3. A unit that is not a colonist (type 9) unloads: each stone entry (tag 2 value 2) gives
           BatimentAjouteMatiere(2, 1, player, structure) then BagRetire; then each food entry (tag 2 value 1) the
           same with resource 1. The credit is 1 per entry whatever its value.
        4. A structure owned by 0xc8 becomes the unit's player's: BatimentHabitable(s, 1), BatimentModifyMap(s),
           InitBatimentPlayer(s, player) (for a cave: the player's cave count += 1); when it is the local player's
           and its volume handle +0x100 is -1, PlaySnd_PostSound(0x42, type << 16 | 0x2700, s + 0x100, 0, push).
        5. BagPrend(structure Bag, 1, unit). AL = 1."""
        s, u = regs['EAX'] & 0xffff, regs['EDX'] & 0xffff
        est = ESTRUTURAS + PASSO * s
        tipo_u = self._ext('EnginGetType', 0x41f798, EAX=u)['EAX'] & 0xff
        if tipo_u == 0xa:
            raise ForaDoDominioTrabalho('BatimentLogeEngin', 0x41f7ab, 'type-10 unit')
        tipo_s = self.m.u8(est + 8)
        if tipo_s in (0x15, 2):
            ocupada = self._ext('BagContientTroupe', 0x41f934 if tipo_s == 0x15 else 0x41f946, EAX=est + 0xc)['EAX'] & 0xff
            if not ocupada and tipo_s == 2:
                ocupada = self._ext('BagContient', 0x41f95c, EAX=est + 0xc, EDX=1, EBX=9)['EAX'] & 0xffff
        else:
            ocupada = self._ext('BagContient', 0x41f95c, EAX=est + 0xc, EDX=1, EBX=9)['EAX'] & 0xffff
        if ocupada:
            r = self._ext('EnginGetPlayer', 0x41f972, EAX=u)
            if r['EAX'] & 0xff != self.m.u8(est + 4):
                return self._sair_loge(regs, r, 0)
        r = self._ext('PlaceLibre', 0x41f98f, EAX=s, EDX=u)
        if not r['EAX'] & 0xff:
            return self._sair_loge(regs, r, None)
        if self._ext('EnginGetType', 0x41f99e, EAX=u)['EAX'] & 0xff != 9:
            bolsa = self._ext('EnginGetBag', 0x41f9bb, EAX=u)['EAX']
            for recurso, contem, credito, retira in ((2, 0x41f9cb, 0x41f9f4, 0x41fa02), (1, 0x41fa15, 0x41fa3b, 0x41fa4c)):
                while self._ext('BagContient', contem, EAX=bolsa, EDX=2, EBX=recurso)['EAX'] & 0xffff:
                    j = self._ext('EnginGetPlayer', credito - 0xc, EAX=u)['EAX'] & 0xff
                    self._ext('BatimentAjouteMatiere', credito, EAX=recurso, EDX=1, EBX=j, ECX=s)
                    self._ext('BagRetire', retira, EAX=bolsa, EDX=2, EBX=recurso)
        if self.m.u8(est + 4) == 0xc8:
            j = self._ext('EnginGetPlayer', 0x41fa72, EAX=u)['EAX'] & 0xff
            self.m.u8(est + 4, j)
            self._ext('BatimentHabitable', 0x41fa81, EAX=s, EDX=1)
            self._ext('BatimentModifyMap', 0x41fa88, EAX=s)
            j = self._ext('EnginGetPlayer', 0x41fa91, EAX=u)['EAX'] & 0xff
            self._ext('InitBatimentPlayer', 0x41fa9a, EAX=s, EDX=j)
            if self.m.u8(est + 4) == self.m.u8(JOGADOR_LOCAL):
                v = self._ext('BatimentGetVolume', 0x41fac2, EAX=s)['EAX']
                if self.m.u32(est + 0x100) == M32:
                    self._ext('PlaySnd_PostSound', 0x41faeb, pilha=(v,), EAX=0x42,
                              EDX=(self.m.u8(est + 8) << 16) | 0x2700, EBX=est + 0x100, ECX=0)
        r = self._ext('BagPrend', 0x41fafe, EAX=est + 0xc, EDX=1, EBX=u)
        return self._sair_loge(regs, r, 1)

    @staticmethod
    def _sair_loge(regs, ultimo, al):
        """Exit through 0x41fb0a / 0x42399a: EBX, ECX, ESI, EDI, EBP restored; EAX and EDX are the last callee's
        (``ultimo``), with AL replaced by ``al`` when the original sets it (1 lodged, 0 refused)."""
        saida = {k: regs[k] & M32 for k in REG7}
        saida['EDX'] = ultimo['EDX'] & M32
        saida['EAX'] = ultimo['EAX'] & M32 if al is None else (ultimo['EAX'] & 0xffffff00) | al
        saida['ESP'] = (regs['ESP'] + 4) & M32
        return saida
