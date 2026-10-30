"""Hunger entry, food search and light removal over live original memory (M3 S1 path), every register.

Translated from the intact bytes after the original-only capture ``evidencias/fadiga-vegetacao/`` (see
``validar_fadiga_vegetacao.py --capturar``). Routines (original SHA-256 6c556520...43fb):
- EnginSetFatigue 0x453b84..0x453d56 (+ shared tails 0x44b334..0x44b34a, 0x44f29d, 0x440d58): a starving unit
  saves its state and target, looks for a food sack (ChercheVegetLibre(cell, 20, 0x43..0x43)) and walks to it in
  state 19; with no sack and food >= 3, the nearest own cave within 40 cells; else the hungry voice;
- ChercheVegetLibre 0x477b74..0x477e91: square-ring search around a cell for an object byte in [BL, CL] the unit
  (pushed word) can enter; EnginPeutPasser 0x442668 is evaluated inline for the unit types that reach its
  0x4426c7 path (0..2, 4..10: every fatigable type but 3 and 25);
- ChercheTypeBatimentProximite 0x4538fa..0x4539f3: the nearest existing structure of type BL and owner CL whose
  centre is within DX cells (squared distance < DX*DX, strict minimum, lowest index on ties);
- EteintTerrain 0x476e82..0x477042 (epilogue 0x476e7b): one light count removed on the disc of radius DX around AX
  for owner BL (``visao_movimento.apagar_area``, the routine RetireEngin's and BatimentRetireColon's translations
  already use), with its exit registers.

Calling convention: ``chamar(nome, regs, pilha=())`` with EAX..EBP (and optionally ESP, the routine's entry ESP:
the address of its return address) returns EAX..EBP and ESP as the routine leaves them. ``pilha``: the pushed words
of ChercheVegetLibre (the unit; RET 4). Registers the original leaves to uninitialized stack words are exact when
``ESP`` is given and readable in ``memoria``; otherwise they are returned as 0 in ``_incertos``:
- ChercheVegetLibre's EAX bits 16..31 when the hit comes from its first two ring checks (locals [esp+0x10],
  [esp+0xc] are 16-bit stores read back as dwords);
- EteintTerrain's EBX bits 16..31 when no row of the disc is inside the map (only a centre outside the map rows).

Dependencies (never defaulted): ``externo(nome, chamada, registradores) -> registradores`` for Economy's
TestRessource 0x4676e5 (registers EAX/EDX/EBX/ECX and ``_pilha`` = [player]; RET 4); ``som(nome, registradores,
pilha) -> EAX`` for Audio's PlaySnd_PostSound 0x48aa79 (the shape of ``selecao_ordens``). Core callees are
existing translations: BatimentGetCase (``chamadas_quadro_core.caso_estrutura``), TerrainEstDecouvert
(``terreno_esta_descoberto``), EnginGetVolume (``selecao_ordens``), the live world's ``apagar_area``.

Outside the translated domain (``ForaDoDominioFadiga``, raised before any store of the branch): a unit index
above 799; EnginPeutPasser for unit types 3, 11..25 (inside ChercheVegetLibre, raised before its first passage
test; nothing is stored by the search); ChercheVegetLibre radius words 0x7fff and above; EteintTerrain owners
other than 0..3 (the light grids are indexed by owner; owner 0xc8 faults in the original) and radii above 0x7ffe.
"""
from entrada_estruturas import ArgumentoNaoPassado

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
ESTRUTURAS, NUM_ESTRUTURAS = 0x49a0c8, 1000
GRADE_OBJETOS, GRADE_ATRIBUTOS = 0x507d74, 0x507da8
LARGURA, ALTURA = 0x497168, 0x49716a
JOGADOR_LOCAL = 0x508041
BUSCA_UNIDADE, BUSCA_OCUPADA, BUSCA_SUCESSO, BUSCA_ROTA = 0x496304, 0x4e0f36, 0x4e0f37, 0x4e0f3c
ROTINAS = {'EnginSetFatigue': 0x453b84, 'ChercheVegetLibre': 0x477b74, 'ChercheTypeBatimentProximite': 0x4538fa,
           'EteintTerrain': 0x476e82}
PILHA = {'ChercheVegetLibre': 1}
# Registers each routine's behaviour depends on: a provider call without one raises ``ArgumentoNaoPassado``.
ARGUMENTOS_EXIGIDOS = {
    'EnginSetFatigue': ('EAX',),
    'ChercheVegetLibre': ('EAX', 'EDX', 'EBX', 'ECX'),
    'ChercheTypeBatimentProximite': ('EAX', 'EDX', 'EBX', 'ECX'),
    'EteintTerrain': ('EAX', 'EDX', 'EBX'),
}
TIPOS_PASSAGEM = frozenset((0, 1, 2, 4, 5, 6, 7, 8, 9, 10))     # EnginPeutPasser's 0x4426c7 path


class DependenciaFadiga(NotImplementedError):
    """A callee owned elsewhere was reached without its provider."""
    def __init__(self, rotina, chamada, motivo='provider required'):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: {motivo}')


class ForaDoDominioFadiga(NotImplementedError):
    """A branch outside the translated domain; nothing was written by it."""
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made by this branch')


def _s16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


def _s32(v):
    v &= M32
    return v - (1 << 32) if v & 0x80000000 else v


def _b(v, b):
    return (v & 0xffffff00) | (b & 0xff)


def _h(v, b):
    return (v & 0xffff00ff) | ((b & 0xff) << 8)


def _w(v, w):
    return (v & 0xffff0000) | (w & 0xffff)


class _Quadro:
    """A routine's stack frame: bytes at offsets from its final ESP; ``residuo(o)`` reads a never-written word from
    memory (exact) or reports it unknown."""

    def __init__(self, memoria, base, tamanho):
        self.m, self.base = memoria, base
        self.b = bytearray(tamanho)
        self.escrito = bytearray(tamanho)

    def w8(self, o, v):
        self.b[o] = v & 0xff
        self.escrito[o] = 1

    def w16(self, o, v):
        self.w8(o, v)
        self.w8(o + 1, v >> 8)

    def w32(self, o, v):
        self.w16(o, v)
        self.w16(o + 2, v >> 16)

    def r8(self, o):
        if not self.escrito[o]:
            raise AssertionError(f'frame byte +0x{o:x} read before written')
        return self.b[o]

    def r16(self, o):
        return self.r8(o) | (self.r8(o + 1) << 8)

    def r32(self, o):
        return self.r16(o) | (self.r16(o + 2) << 16)

    def r32_residuo(self, o):
        """(value, uncertain mask) of a dword whose upper word may never have been written."""
        baixo = self.r16(o)
        if self.escrito[o + 2] and self.escrito[o + 3]:
            return baixo | (self.r16(o + 2) << 16), 0
        valor = self.palavra_memoria(o + 2)
        if valor is None:
            return baixo, 0xffff0000
        return baixo | (valor << 16), 0

    def palavra_memoria(self, o):
        if self.base is None:
            return None
        try:
            return self.m.u16((self.base + o) & M32)
        except LookupError:
            return None


class FadigaVegetacao:
    def __init__(self, memoria, *, externo=None, som=None):
        self.m = memoria
        self.externo, self.som = externo, som
        self._selecao = self._mundo = None

    # ------------------------------------------------------------ helpers
    def _rec(self, u):
        return (self.m.u32(PONTEIRO_UNIDADES) + PASSO * (u & 0xffff)) & M32

    def mundo(self):
        if self._mundo is None:
            from construcao_core import ConstrucaoCore
            self._mundo = ConstrucaoCore(self.m).mundo()
        return self._mundo

    def selecao(self):
        if self._selecao is None:
            from selecao_ordens import SelecaoOrdens
            self._selecao = SelecaoOrdens(self.m, som=self.som)
        return self._selecao

    def chamar(self, nome, regs, pilha=()):
        if nome not in ROTINAS:
            raise KeyError(f'{nome} is not a translated hunger/search/light routine')
        if len(pilha) != PILHA.get(nome, 0):
            raise ValueError(f'{nome} takes {PILHA.get(nome, 0)} pushed word(s)')
        r = {k: regs[k] & M32 for k in REG7}
        esp = regs.get('ESP')
        saida = getattr(self, '_' + nome)(r, None if esp is None else esp & M32, list(pilha))
        if esp is not None:
            saida['ESP'] = (esp + 4 + 4 * PILHA.get(nome, 0)) & M32
        if not saida.get('_incertos'):
            saida.pop('_incertos', None)
        return saida

    # ------------------------------------------------------------ EnginPeutPasser (inline, types 0..2 / 4..10)
    def _peut_passer(self, u, celula, ecx, chamada):
        """EnginPeutPasser 0x442668 with BL = 1 as ChercheVegetLibre calls it; returns (AL, EBX, ECX, EDX).
        Types 0..2/4..10 take 0x4426c7: EnginOccupeCase (the unit's own cell +8 or +0x7c, unless +0xab/mask/state
        14 exclude it) passes with EBX = 0x101, EDX = the cell; else TerrainEnCollision (attribute & mask) clear
        passes and set fails (ChercheIndiceEngin only reads), both with EDX = 1 and EBX = 0x100, or 0x101 when an
        early exclusion left EnginOccupeCase's BL = 1.
        ECX = the entry ECX upper half | AL. EAX on failure is not modeled: every caller overwrites it."""
        m = self.m
        rec = self._rec(u)
        tipo = m.u8(rec + 1)
        if tipo not in TIPOS_PASSAGEM:
            raise ForaDoDominioFadiga('ChercheVegetLibre', chamada, f'EnginPeutPasser for unit type {tipo}')
        mascara = 1
        ab = m.u8(rec + 0xab)
        # EnginOccupeCase 0x44246e: BH := BL (mask), BL := 1 first; the early exclusions (+0xab with mask 1, no
        # +0xab with mask 2, state 14) return AL = 0 with BL still 1; otherwise BL = AL = the cell test.
        if (ab and mascara == 1) or (not ab and mascara == 2) or m.u8(rec + 2) == 0xe:
            ocupa, bl = 0, 1
        else:
            ocupa = bl = int(celula in (m.u16(rec + 8), m.u16(rec + 0x7c)))
        ebx = (mascara << 8) | bl
        ecx_alto = ecx & 0xffff0000
        if ocupa:
            return 1, ebx, ecx_alto | 1, celula & 0xffff, (rec & 0xffffff00) | 1
        colisao = m.u8((m.u32(GRADE_ATRIBUTOS) + (celula & 0xffff)) & M32) & mascara
        if not colisao:
            return 1, ebx, ecx_alto | 1, mascara, 1
        return 0, ebx, ecx_alto, mascara, None

    # ------------------------------------------------------------ ChercheVegetLibre
    def _ChercheVegetLibre(self, r, esp, pilha):
        """ChercheVegetLibre 0x477b74: AX cell, DX radius word, BL/CL object byte bounds, pushed unit. The cell
        itself, then rings 1..DX; on ring k, for i = -k..k: (row y+i, column x-k) [cell - k*256 - k + i*256],
        (y+i, x+k), and for -k < i < k also (y-k, x+i) and (y+k, x+i); each in the map, its object byte in
        [BL, CL], and EnginPeutPasser(unit, cell, 1). EAX = the cell found (see the module docstring for its
        upper half) or 0xffff; ESI/EDI/EBP preserved."""
        m = self.m
        q = _Quadro(m, None if esp is None else (esp - 0x3c) & M32, 0x44)
        incertos = {}
        q.w32(0x40, pilha[0])
        eax, ebx, ecx, edx = r['EAX'], r['EBX'], r['ECX'], r['EDX']
        esi0, edi0, ebp0 = r['ESI'], r['EDI'], r['EBP']
        q.w32(4, eax)
        q.w32(0, edx)
        q.w8(0x2c, ebx)
        q.w8(0x28, ecx)
        if q.r16(0) >= 0x7fff:
            raise ForaDoDominioFadiga('ChercheVegetLibre', 0x477bf0, f'radius word {q.r16(0):#x}')
        objetos = m.u32(GRADE_OBJETOS)
        largura, altura = m.u16(LARGURA), m.u16(ALTURA)
        unidade = q.r16(0x40)
        esi = eax & 0xffff
        ebx = 0x100
        q.w16(0x1c, esi % 256)
        q.w16(0x18, esi // 256)
        edx = esi % 256
        eax = (objetos + esi) & M32
        dl = m.u8(eax)
        edx = _b(edx, dl)

        def sair(eax_saida, ebx, ecx, edx, incerto=0):
            saida = dict(EAX=eax_saida & M32, EBX=ebx & M32, ECX=ecx & M32, EDX=edx & M32, ESI=esi0, EDI=edi0,
                         EBP=ebp0)
            if incerto:
                incertos['EAX'] = incerto
            saida['_incertos'] = incertos
            return saida

        def passar(celula, ecx_antes):
            ok, b_, c_, d_, a_ = self._peut_passer(unidade, celula, ecx_antes, 0x477bcd)
            return ok, b_, c_, d_

        if q.r8(0x2c) <= dl <= (ecx & 0xff):
            ok, ebx, ecx, edx = passar(esi, 0)
            if ok:
                return sair(esi, ebx, ecx, edx)
        edi = 1
        while True:                                            # 0x477be7
            eax = q.r16(0)
            edx = _s16(edi) & M32
            if _s32(edx) > eax:
                return sair(0xffff, ebx, ecx, edx)
            esi = (-edi) & M32
            ebx = (esi << 8) & M32
            ecx = q.r32(4)
            q.w16(0x10, ebx + esi + ecx)
            edx = (ebx + edi + ecx) & M32
            q.w16(0xc, edx)
            eax = (edi << 8) & M32
            q.w32(0x24, ecx + eax)
            edx = (ecx - eax) & M32
            q.w32(0x20, edx)
            while _s16(esi) <= _s16(edi):                       # 0x477c47
                # check 1: (y + i, x - k)
                eax = _s16(q.r16(0x1c))
                ebx = _s16(edi) & M32
                eax = (eax - _s32(ebx)) & M32
                if _s32(eax) >= 0:
                    eax = _s16(q.r16(0x18))
                    edx = _s16(esi) & M32
                    eax = (eax + _s32(edx)) & M32
                    if _s32(eax) >= 0:
                        ecx = altura
                        if _s32(eax) < ecx:
                            edx = ((edx << 8) + q.r16(4) - ebx) & M32
                            eax = (objetos + edx) & M32
                            ebx = _h(ebx, q.r8(0x2c))
                            dl = m.u8(eax)
                            edx = _b(edx, dl)
                            if (ebx >> 8) & 0xff <= dl <= q.r8(0x28):
                                ok, ebx, ecx, edx = passar(q.r16(0x10), 0)
                                if ok:
                                    v, inc = q.r32_residuo(0x10)
                                    return sair(v, ebx, ecx, edx, inc)
                # check 2: (y + i, x + k)
                edx = _s16(q.r16(0x1c))
                eax = _s16(edi) & M32
                ebx = largura
                edx = (edx + _s32(eax)) & M32
                if _s32(edx) < ebx:
                    ebx = _s16(q.r16(0x18))
                    edx = _s16(esi) & M32
                    ebx = (ebx + _s32(edx)) & M32
                    if _s32(ebx) >= 0:
                        ecx = altura
                        if _s32(ebx) < ecx:
                            ebx = q.r16(4)
                            edx = ((edx << 8) + ebx) & M32
                            eax = (eax + edx + objetos) & M32
                            ecx = _h(ecx, q.r8(0x2c))
                            dl = m.u8(eax)
                            edx = _b(objetos, dl)
                            if (ecx >> 8) & 0xff <= dl <= q.r8(0x28):
                                ok, ebx, ecx, edx = passar(q.r16(0xc), 0)
                                if ok:
                                    v, inc = q.r32_residuo(0xc)
                                    return sair(v, ebx, ecx, edx, inc)
                # 0x477d4c: the corners are covered by checks 1/2
                edx = _s16(edi) & M32
                ebx = (-edx) & M32
                eax = _s16(esi) & M32
                if eax != ebx and (esi & 0xffff) != (edi & 0xffff):
                    # check 3: (y - k, x + i)
                    ebx = ((_s16(q.r16(0x18))) - _s32(edx)) & M32
                    if _s32(ebx) >= 0:
                        ebx = ((_s16(q.r16(0x1c))) + _s32(eax)) & M32
                        if _s32(ebx) >= 0:
                            ecx = largura
                            if _s32(ebx) < ecx:
                                edx = (edx << 8) & M32
                                ebx = (q.r16(4) - edx) & M32
                                edx = (ebx + eax) & M32
                                eax = (objetos + edx) & M32
                                dl = m.u8(eax)
                                edx = _b(edx, dl)
                                if q.r8(0x2c) <= dl <= q.r8(0x28):
                                    eax = (q.r32(0x20) + esi) & M32
                                    q.w32(8, eax)
                                    ok, ebx, ecx, edx = passar(eax & 0xffff, 0)
                                    if ok:
                                        return sair(q.r32(8), ebx, ecx, edx)
                    # check 4: (y + k, x + i)
                    edx = _s16(q.r16(0x18))
                    ebx = _s16(edi) & M32
                    eax = altura
                    edx = (edx + _s32(ebx)) & M32
                    if _s32(edx) < eax:
                        edx = _s16(q.r16(0x1c))
                        eax = _s16(esi) & M32
                        edx = (edx + _s32(eax)) & M32
                        if _s32(edx) >= 0:
                            ecx = largura
                            if _s32(edx) < ecx:
                                ebx = (ebx << 8) & M32
                                edx = (q.r16(4) + ebx + eax) & M32
                                eax = (objetos + edx) & M32
                                ebx = _h(ebx, q.r8(0x2c))
                                dl = m.u8(eax)
                                edx = _b(edx, dl)
                                if (ebx >> 8) & 0xff <= dl <= q.r8(0x28):
                                    eax = (q.r32(0x24) + esi) & M32
                                    q.w32(0x14, eax)
                                    ok, ebx, ecx, edx = passar(eax & 0xffff, 0)
                                    if ok:
                                        return sair(q.r32(0x14), ebx, ecx, edx)
                # 0x477c32
                ch = (q.r8(0x11) + 1) & 0xff
                al = (q.r8(0xd) + 1) & 0xff
                esi = (esi + 1) & M32
                ecx = _h(ecx, ch)
                eax = _b(eax, al)
                q.w8(0x11, ch)
                q.w8(0xd, al)
            edi = (edi + 1) & M32                             # 0x477be6

    # ------------------------------------------------------------ ChercheTypeBatimentProximite
    def _ChercheTypeBatimentProximite(self, r, esp, pilha):
        """ChercheTypeBatimentProximite 0x4538fa: AX cell, DX radius word, BL type, CL owner. Structures 0..999
        that exist (+5), have owner +4 = CL and type +8 = BL; squared distance (Distance2d) from BatimentGetCase's
        centre < DX*DX and < the best so far. EAX = the index or 0xffff; EDX = 1000; EBX/ECX = the last values the
        scan left (ECX = the last match's centre row; EBX from the last owner match); ESI/EDI/EBP preserved."""
        from chamadas_quadro_core import caso_estrutura
        m = self.m
        celula = r['EAX'] & 0xffff
        raio2 = ((r['EDX'] & 0xffff) ** 2) & M32
        tipo, dono = r['EBX'] & 0xff, r['ECX'] & 0xff
        ebx, ecx = r['EBX'], r['ECX']
        melhor, indice = M32, 0xffff
        yp, xp = celula >> 8, celula & 0xff
        for s in range(NUM_ESTRUTURAS):
            e = ESTRUTURAS + PASSO * s
            if not m.u8(e + 5) or m.u8(e + 4) != dono:
                continue
            ebx = _b(ebx, tipo)
            if m.u8(e + 8) != tipo:
                continue
            c = caso_estrutura(m, s)['EAX'] & 0xffff
            ys, xs = c >> 8, c & 0xff
            ecx = ys
            # Distance2d 0x479555: EAX = x_p, EBX = x_s, EDX = y_p, ECX = y_s
            dx2 = ((xp - xs) ** 2) & M32
            if yp > ys:
                ebx, dy2 = ys, ((yp - ys) ** 2) & M32
            else:
                ebx = (ys - yp) & M32
                dy2 = (ebx * ebx) & M32
            d = (dx2 + dy2) & M32
            if d < raio2 and d < melhor:
                melhor, indice = d, s
        return dict(EAX=indice, EBX=ebx, ECX=ecx, EDX=NUM_ESTRUTURAS, ESI=r['ESI'], EDI=r['EDI'], EBP=r['EBP'])

    # ------------------------------------------------------------ EteintTerrain
    def _EteintTerrain(self, r, esp, pilha):
        """EteintTerrain 0x476e82: AX cell, DX radius, BL owner. EteintCase on every map cell (y+i, x+j), i and j
        in -DX..DX, with (i*i + j*j) mod 65536 <= (DX*DX + (DX >= 2)) mod 65536, rows then columns; a second
        identical row/column pass only reads. EAX = DX + 1 (word, sign-extended), EDX = DX, EBX = -EDX + 2*DX + 1
        (the column counter of the last row inside the map); ECX/ESI/EDI/EBP preserved."""
        celula, edx_in, dono = r['EAX'] & 0xffff, r['EDX'], r['EBX'] & 0xff
        raio = edx_in & 0xffff
        if dono > 3:
            raise ForaDoDominioFadiga('EteintTerrain', 0x476f85, f'owner {dono} (light grids are per player 0..3)')
        if raio > 0x7ffe:
            raise ForaDoDominioFadiga('EteintTerrain', 0x476f08, f'radius {raio:#x}')
        altura = self.m.u16(ALTURA)
        y = celula // 256
        self.mundo().apagar_area(celula, raio, dono)
        saida = dict(r, EAX=_s16(raio + 1) & M32, EDX=raio)
        if any(0 <= y + i < altura for i in range(-raio, raio + 1)):
            saida['EBX'] = (-edx_in + 2 * raio + 1) & M32
            return saida
        # No row inside the map: the first pass's skip path left [esp+8] (row word | never-written word) + 1.
        base = None if esp is None else (esp - 0x28) & M32
        q = _Quadro(self.m, base, 0x20)
        alto = q.palavra_memoria(0xa)
        baixo = (raio + 1) & 0xffff
        if alto is None:
            saida['EBX'] = baixo
            saida['_incertos'] = {'EBX': 0xffff0000}
        else:
            saida['EBX'] = ((alto << 16) + raio + 1) & M32
        return saida

    # ------------------------------------------------------------ EnginSetFatigue
    def _EnginSetFatigue(self, r, esp, pilha):
        """EnginSetFatigue 0x453b84: AX unit. Word +4 = 4 or state 19: nothing (EAX = that value). Otherwise +0xa0 :=
        state byte, +0xa2 := +0x7e, then ChercheVegetLibre(+8, 20, 0x43, 0x43, push unit):
        - a sack: +0xc2 := 0xffff, state 19, +0x7e := the cell, the unit's path search released, +0x88 := 0;
        - none: TestRessource(food 3, 0, 0, push owner); false: done. True: ChercheTypeBatimentProximite(+8, 40,
          type 3, owner): a cave: state 19, +0xc2 := it, +0x7e := BatimentGetCase(it), search released, +0x88 := 0;
          none: for the local player's unit with +0x74 = 1 whose cell the local player discovered: EnginGetVolume,
          +0xf9 := 0 and, when +0x104 = -1, PlaySnd_PostSound(0x50, type << 16 | 0xc00, rec + 0x104, 0, push volume).
        EBX..EBP preserved; EAX: the entry EAX on the two state-19 paths, else the last value (see the code)."""
        m = self.m
        eax_in = r['EAX']
        u = eax_in & 0xffff
        if u >= 800:
            raise ForaDoDominioFadiga('EnginSetFatigue', 0x453b8b, f'unit {u}')
        rec = self._rec(u)
        saida = dict(r)
        if m.u16(rec + 4) == 4:
            return dict(saida, EAX=4)
        estado = m.u8(rec + 2)
        if estado == 0x13:
            return dict(saida, EAX=0x13)
        m.u16(rec + 0xa0, estado)
        m.u16(rec + 0xa2, m.u16(rec + 0x7e))
        esp_cvl = None if esp is None else (esp - 0x24) & M32
        cvl = self._ChercheVegetLibre(dict(r, EAX=m.u16(rec + 8), EDX=0x14, EBX=0x43, ECX=0x43, EDI=0, ESI=rec,
                                           EBP=u), esp_cvl, [u])
        achado = cvl['EAX'] & 0xffff
        if achado != 0xffff:
            m.u16(rec + 0xc2, 0xffff)
            m.u8(rec + 2, 0x13)
            m.u16(rec + 0x7e, achado)
            self._liberar_busca(u)
            m.u8(rec + 0x88, 0)
            return dict(saida, EAX=eax_in)
        dono = m.u8(rec)
        t = self._externo('TestRessource', 0x453c5f, dict(EAX=3, EDX=0, EBX=0, ECX=0, _pilha=[dono]))
        if not t['EAX'] & 0xff:
            return dict(saida, EAX=t['EAX'])
        ctbp = self._ChercheTypeBatimentProximite(dict(r, EAX=m.u16(rec + 8), EDX=0x28, EBX=3, ECX=dono), None, [])
        s = ctbp['EAX'] & 0xffff
        if s != 0xffff:
            from chamadas_quadro_core import caso_estrutura
            c = caso_estrutura(m, s)['EAX']
            m.u8(rec + 2, 0x13)
            m.u16(rec + 0xc2, ctbp['EAX'])
            m.u16(rec + 0x7e, c)
            self._liberar_busca(u)
            m.u8(rec + 0x88, 0)
            return dict(saida, EAX=eax_in)
        eax = _b(0xffff, dono)
        if dono != m.u8(JOGADOR_LOCAL):
            return dict(saida, EAX=eax)
        eax = m.u16(rec + 0x74)
        if eax != 1:
            return dict(saida, EAX=eax)
        from chamadas_quadro_core import terreno_esta_descoberto
        eax = terreno_esta_descoberto(m, m.u16(rec + 8), m.u8(JOGADOR_LOCAL))['EAX']
        if not eax & 0xff:
            return dict(saida, EAX=eax)
        volume = self.selecao()._volume_unidade(u)
        alca = m.u32(rec + 0x104)
        m.u8(rec + 0xf9, 0)
        if alca != M32:
            return dict(saida, EAX=volume)
        if self.som is None:
            raise DependenciaFadiga('PlaySnd_PostSound', 0x44b33d, 'Audio sound-library provider required')
        eax = self.som('PlaySnd_PostSound', dict(EAX=0x50, EDX=(m.u8(rec + 1) << 16) | 0xc00,
                                                 EBX=(rec + 0x104) & M32, ECX=0), [volume]) & M32
        return dict(saida, EAX=eax)

    def _liberar_busca(self, u):
        m = self.m
        if (u & 0xffff) == m.u16(BUSCA_UNIDADE):
            m.u8(BUSCA_OCUPADA, 0)
            m.u8(BUSCA_SUCESSO, 0)
            m.u32(BUSCA_ROTA, 0)
            m.u16(BUSCA_UNIDADE, 0xffff)

    def _externo(self, nome, chamada, regs):
        if self.externo is None:
            raise DependenciaFadiga(nome, chamada)
        saida = self.externo(nome, chamada, regs)
        return {k: saida[k] & M32 for k in REG7 if k in saida}


def provedor_fadiga(fadiga, outros=None):
    """``externo(nome, chamada, registradores) -> registradores`` serving EnginSetFatigue, ChercheVegetLibre,
    ChercheTypeBatimentProximite and EteintTerrain (``fadiga``: a ``FadigaVegetacao`` over the caller's memory), in
    the shape of ``entrada_estruturas.provedor_entrada``.

    Input: the argument registers, optionally the other registers, ``ESP`` (the routine's entry ESP, for the
    stack-residue bits) and ``_pilha`` (ChercheVegetLibre: [unit], required) and ``_incertos``. A register in
    ``ARGUMENTOS_EXIGIDOS`` that is missing raises ``ArgumentoNaoPassado`` before anything runs; any other missing
    register enters as 0 and, when the routine leaves it unchanged, comes back in ``_incertos``. Output: EAX..EBP
    after the routine's stores, plus ``_incertos`` for bits not reconstructed. Other names go to ``outros`` or raise
    ``DependenciaFadiga``."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise DependenciaFadiga(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        faltando = [k for k in ARGUMENTOS_EXIGIDOS[nome] if k not in regs]
        if PILHA.get(nome) and len(regs.get('_pilha') or ()) != PILHA[nome]:
            faltando.append('_pilha')
        if faltando:
            raise ArgumentoNaoPassado(nome, chamada, faltando)
        entrada = {k: regs.get(k, 0) & M32 for k in REG7}
        if 'ESP' in regs:
            entrada['ESP'] = regs['ESP']
        incertos_in = dict(regs.get('_incertos') or {})
        for k in REG7:
            if k not in regs:
                incertos_in[k] = M32
        saida = fadiga.chamar(nome, entrada, list(regs.get('_pilha') or ()))
        resultado = {k: saida[k] & M32 for k in REG7}
        incertos = {k: v for k, v in incertos_in.items() if v and resultado.get(k) == entrada.get(k)}
        for k, v in (saida.get('_incertos') or {}).items():
            incertos[k] = incertos.get(k, 0) | v
        if incertos:
            resultado['_incertos'] = incertos
        return resultado
    return externo
