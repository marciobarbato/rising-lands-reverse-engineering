"""S1's work-cycle searches and path-search blocking tests over live original memory, every register.

Translated from the intact bytes (original SHA-256 6c556520...43fb) after the original-only S1 capture
``evidencias/lacunas-s1/`` (``validar_lacunas_s1.py --capturar``). S1 first reaches them at frames 2352-3116
(Economy's ``CalculWorkEngin``) and 2604-2709 (Core's ``CheminCalcul``/``Chemin_Verouille``):

- ChercheVeget 0x47790d..0x477b74: square-ring search around cell AX for an object byte in [BL, CL] (no passage
  test). The cell itself, then rings k = 1..DX; on ring k, for i = -k..k: (row y+i, column x-k), (y+i, x+k) and,
  for -k < i < k, (y-k, x+i), (y+k, x+i). EAX = the entry EAX on the cell itself, else entry EAX +/- the offset
  (all 32 bits: ``(i<<8) + EAX - k`` ...), or 0xffff. EBX = the object-grid address of the hit (or DX's low word),
  ECX = the entry ECX with CH = the last object byte read, EDX = x, k or k<<8 as the exit leaves it.
- ChercheGc 0x4781cc: ChercheVeget(AX, DX, 0x1e, 0x35) (it jumps into ChercheDrapeau's call 0x477ea5); EBX and
  ECX preserved; the upper halves of EAX/EDX cleared before the call.
- ChercheGcLibre 0x477ead..0x4781cc: the same ring order with k < DX (strict), object bytes 0x1e..0x35 and
  EnginPeutPasser(BX = unit, cell, BL = 1) at every candidate (``fadiga_vegetacao``'s inline 0x442668 for unit
  types 0..2/4..10). ECX/ESI/EDI/EBP preserved. EAX on the first two ring checks is a dword local whose upper word
  is stack residue (exact when ESP is given and readable).
- TypeEnginPeutEcraser 0x442409: AL = 1 for unit types 0x0c and 0x0f, else 0 (upper EAX kept).
- IsDirectlyBlocking 0x42eba4 / IsIndirectlyBlocking 0x42ece0: may the searching unit [0x496304] pass the
  occupant EAX given the desired direction EDX? ``caminhos.classificar_passagem``'s rule (alliance at
  [0x5080a8], occupant moving +0x7e != +8 except types 0/1/0x14/0x15 in state 1 with +0x8a = 1 and 6/7 in state 15
  with +0x89 = 1, aligned within one octant of +0x90, crushing exception TypeEnginPeutEcraser x 0x4423d5,
  [0x4e1771] for a stopped ally). AL = 0/1/2 (Indirectly: 0/1), AH = the moving flag, upper EAX 0; EDX as the last
  load leaves it; EBX/ECX/ESI/EDI preserved.

``chamar(nome, regs, pilha=())`` takes EAX..EBP (and optionally ESP, the entry ESP) and returns EAX..EBP and ESP.
Outside the translated domain (``ForaDoDominioBuscas``, raised before any effect; these routines store nothing):
radius words 0x7fff and above; EnginPeutPasser for unit types 3, 11..25; unit indexes above 799 in the blocking
tests. The two crushing tables are complete over all 256 type bytes.
"""
from fadiga_vegetacao import FadigaVegetacao, _Quadro, _b, _h, _s32

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
GRADE_OBJETOS = 0x507d74
LARGURA, ALTURA = 0x497168, 0x49716a
BUSCA_UNIDADE = 0x496304
ALIANCAS = 0x5080a8
PARADOS_PASSAM = 0x4e1771
ROTINAS = {'ChercheVeget': 0x47790d, 'ChercheGc': 0x4781cc, 'ChercheGcLibre': 0x477ead,
           'TypeEnginPeutEcraser': 0x442409, 'IsDirectlyBlocking': 0x42eba4, 'IsIndirectlyBlocking': 0x42ece0}
ARGUMENTOS_EXIGIDOS = {
    'ChercheVeget': ('EAX', 'EDX', 'EBX', 'ECX'),
    'ChercheGc': ('EAX', 'EDX'),
    'ChercheGcLibre': ('EAX', 'EDX', 'EBX'),
    'TypeEnginPeutEcraser': ('EAX',),
    'IsDirectlyBlocking': ('EAX', 'EDX'),
    'IsIndirectlyBlocking': ('EAX', 'EDX'),
}


class ForaDoDominioBuscas(NotImplementedError):
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); these routines store nothing')


def _peut_ecraser(tipo):
    """TypeEnginPeutEcraser 0x442409."""
    return int(tipo & 0xff in (0x0c, 0x0f))


def _ecrasable(tipo):
    """0x4423d5 (the occupant side of the crushing exception): 1 for 0..2, 4..10, 0x12, 0x13, 0x16, >= 0x1a."""
    t = tipo & 0xff
    if t < 0x10:
        return 0 if t >= 0x0c or t in (3, 0xb) else 1
    if t in (0x10, 0x11, 0x14, 0x15, 0x17, 0x18, 0x19):
        return 0
    return 1


class BuscasBloqueios:
    def __init__(self, memoria):
        self.m = memoria
        self._fadiga = FadigaVegetacao(memoria)

    def chamar(self, nome, regs, pilha=()):
        if nome not in ROTINAS:
            raise KeyError(f'{nome} is not a translated S1 search/blocking routine')
        if pilha:
            raise ValueError(f'{nome} takes no pushed words')
        r = {k: regs[k] & M32 for k in REG7}
        esp = regs.get('ESP')
        saida = getattr(self, '_' + nome)(r, None if esp is None else esp & M32)
        if esp is not None:
            saida['ESP'] = (esp + 4) & M32
        if not saida.get('_incertos'):
            saida.pop('_incertos', None)
        return saida

    # ------------------------------------------------------------ ChercheVeget / ChercheGc
    def _ChercheVeget(self, r, esp):
        m = self.m
        a, d, c = r['EAX'], r['EDX'], r['ECX']
        lo, hi = r['EBX'] & 0xff, c & 0xff
        if d & 0xffff >= 0x7fff:
            raise ForaDoDominioBuscas('ChercheVeget', 0x477962, f'radius word {d & 0xffff:#x}')
        objetos = m.u32(GRADE_OBJETOS)
        largura, altura = m.u16(LARGURA), m.u16(ALTURA)
        celula = a & 0xffff
        x, y = celula % 256, celula // 256
        ecx = c

        def sair(eax, ebx, edx):
            return dict(EAX=eax & M32, EBX=ebx & M32, ECX=ecx & M32, EDX=edx & M32, ESI=r['ESI'], EDI=r['EDI'],
                        EBP=r['EBP'])

        def objeto(desl):
            nonlocal ecx
            v = m.u8((objetos + desl) & M32)
            ecx = _h(ecx, v)
            return lo <= v <= hi

        if lo <= m.u8((objetos + celula) & M32) <= hi:
            return sair(a, objetos + celula, x)
        k = 1
        while True:                                            # 0x477962
            if k > d & 0xffff:
                return sair(0xffff, d & 0xffff, k)
            i = -k
            while i <= k:                                      # 0x47797b (16-bit signed compares; |i|, k < 0x7fff)
                if x - k >= 0 and 0 <= y + i < altura and objeto((i << 8) + celula - k):
                    return sair((i << 8) + a - k, objetos + (i << 8) + celula - k, k)
                if largura > x + k and 0 <= y + i < altura and objeto((i << 8) + celula + k):
                    return sair((i << 8) + a + k, objetos + (i << 8) + celula + k, k)
                if i != -k and i != k:
                    if y - k >= 0 and 0 <= x + i < largura and objeto(celula - (k << 8) + i):
                        return sair(i + a - (k << 8), objetos + celula - (k << 8) + i, k << 8)
                    if altura > y + k and 0 <= x + i < largura and objeto(celula + (k << 8) + i):
                        return sair(i + a + (k << 8), objetos + celula + (k << 8) + i, k << 8)
                i += 1
            k += 1

    def _ChercheGc(self, r, esp):
        e = dict(r, EAX=r['EAX'] & 0xffff, EDX=r['EDX'] & 0xffff, EBX=0x1e, ECX=0x35)
        s = self._ChercheVeget(e, None if esp is None else (esp - 8) & M32)
        s.update(EBX=r['EBX'], ECX=r['ECX'])
        return s

    # ------------------------------------------------------------ ChercheGcLibre
    def _ChercheGcLibre(self, r, esp):
        m = self.m
        a, d, b = r['EAX'], r['EDX'], r['EBX']
        if d & 0xffff >= 0x7fff:
            raise ForaDoDominioBuscas('ChercheGcLibre', 0x477f27, f'radius word {d & 0xffff:#x}')
        q = _Quadro(m, None if esp is None else (esp - 0x44) & M32, 0x44)
        incertos = {}
        objetos = m.u32(GRADE_OBJETOS)
        largura, altura = m.u16(LARGURA), m.u16(ALTURA)
        unidade = b & 0xffff
        celula = a & 0xffff
        x, y = celula % 256, celula // 256
        lo, hi = 0x1e, 0x35

        def sair(eax, ebx, edx, incerto=0):
            if incerto:
                incertos['EAX'] = incerto
            return dict(EAX=eax & M32, EBX=ebx & M32, ECX=r['ECX'], EDX=edx & M32, ESI=r['ESI'], EDI=r['EDI'],
                        EBP=r['EBP'], _incertos=incertos)

        def passar(alvo):
            ok, ebx_, _, edx_, _ = self._fadiga._peut_passer(unidade, alvo & 0xffff, 0, 0x477f0d)
            return ok, ebx_, edx_

        ebx = 0x100
        if lo <= m.u8((objetos + celula) & M32) <= hi:
            ok, ebx, edx = passar(celula)
            if ok:
                return sair(celula, ebx, edx)
        k = 1
        while True:                                            # 0x477f27
            if k >= d & 0xffff:
                return sair(0xffff, ebx, k)
            q.w16(0x18, ((-k) << 8) - k + a)
            q.w16(0x1c, ((-k) << 8) + k + a)
            i = -k
            while i <= k:                                      # 0x477f88
                # check 1: (y + i, x - k)
                if x - k >= 0:
                    ebx = y + i
                    if 0 <= ebx < altura:
                        ebx = _h(celula, lo)
                        if lo <= m.u8((objetos + (i << 8) + celula - k) & M32) <= hi:
                            ok, ebx, edx = passar(q.r16(0x18))
                            if ok:
                                v, inc = q.r32_residuo(0x18)
                                return sair(v, ebx, edx, inc)
                # check 2: (y + i, x + k)
                ebx = k
                if x + k < largura and 0 <= y + i < altura:
                    if lo <= m.u8((objetos + (i << 8) + celula + k) & M32) <= hi:
                        ok, ebx, edx = passar(q.r16(0x1c))
                        if ok:
                            v, inc = q.r32_residuo(0x1c)
                            return sair(v, ebx, edx, inc)
                # corners belong to checks 1/2
                ebx = -k
                if i != -k and i != k:
                    # check 3: (y - k, x + i)
                    ebx = y - k
                    if ebx >= 0:
                        ebx = x + i
                        if 0 <= ebx < largura:
                            ebx = k << 8
                            if lo <= m.u8((objetos + celula - (k << 8) + i) & M32) <= hi:
                                alvo = a - (k << 8) + i
                                ok, ebx, edx = passar(alvo)
                                if ok:
                                    return sair(alvo, ebx, edx)
                    # check 4: (y + k, x + i)
                    ebx = y + k
                    if ebx < altura:
                        ebx = x + i
                        if 0 <= ebx < largura:
                            ebx = _h(celula, lo)
                            if lo <= m.u8((objetos + celula + (k << 8) + i) & M32) <= hi:
                                alvo = a + (k << 8) + i
                                ok, ebx, edx = passar(alvo)
                                if ok:
                                    return sair(alvo, ebx, edx)
                # 0x477f73: the high bytes of the two word locals advance by one row
                q.w8(0x19, q.r8(0x19) + 1)
                q.w8(0x1d, q.r8(0x1d) + 1)
                i += 1
            k += 1

    # ------------------------------------------------------------ blocking tests
    def _TypeEnginPeutEcraser(self, r, esp):
        return dict(r, EAX=_b(r['EAX'], _peut_ecraser(r['EAX'])))

    def _bloqueio(self, r, nome, positivo):
        m = self.m
        base = m.u32(PONTEIRO_UNIDADES)
        busca = m.u16(BUSCA_UNIDADE)
        if busca > 799 or r['EAX'] > 799:
            raise ForaDoDominioBuscas(nome, ROTINAS[nome], f'unit index {max(busca, r["EAX"])}')
        ecx = (base + PASSO * busca) & M32
        ebx = (base + PASSO * r['EAX']) & M32
        dif = _s32((m.u8(ebx + 0x90) - r['EDX']) & M32)
        dif = int(dif / 2)                                     # sar after subtracting the sign: toward zero
        if dif < -4:
            dif += 8
        if dif > 4:
            dif -= 8
        alinhado = -2 < dif < 2
        # PlayerEstAllie 0x46d838 (AL searcher owner, DL occupant owner)
        dono, outro = m.u8(ecx), m.u8(ebx)
        if dono == outro:
            amigo = 1
        elif dono > 4 or outro > 4:
            amigo = 0
        else:
            mascara = _s32(m.u32((m.u32(ALIANCAS) + 4 * (dono * 5) + 3) & M32)) >> 24
            bit = (1 << outro) & 0xff
            amigo = int(bool(mascara & (bit - 256 if bit & 0x80 else bit)))
        tipo_busca, tipo = m.u8(ecx + 1), m.u8(ebx + 1)
        excecao = _peut_ecraser(tipo_busca) and _ecrasable(tipo)
        edx = m.u16(ebx + 8)
        movendo = int(m.u16(ebx + 0x7e) != edx)
        if tipo in (0, 1, 0x14, 0x15):
            edx = m.u8(ebx + 2)
            if edx == 1:
                edx = m.u8(ebx + 0x8a)
                if edx == 1:
                    movendo = 0
        elif tipo in (6, 7):
            edx = m.u8(ebx + 2)
            if edx == 0xf:
                edx = m.u8(ebx + 0x89)
                if edx == 1:
                    movendo = 0
        if amigo:
            al = positivo if (alinhado if movendo else m.u8(PARADOS_PASSAM)) else 0
        elif excecao:
            al = 1
        else:
            al = positivo if movendo and alinhado else 0
        return dict(r, EAX=(movendo << 8) | al, EDX=edx & M32)

    def _IsDirectlyBlocking(self, r, esp):
        return self._bloqueio(r, 'IsDirectlyBlocking', 2)

    def _IsIndirectlyBlocking(self, r, esp):
        return self._bloqueio(r, 'IsIndirectlyBlocking', 1)


def provedor_buscas(buscas, outros=None):
    """``externo(nome, chamada, registradores) -> registradores`` serving the six routines (``buscas``: a
    ``BuscasBloqueios`` over the caller's memory), in the shape of ``fadiga_vegetacao.provedor_fadiga``: the
    argument registers of ``ARGUMENTOS_EXIGIDOS`` are required (``ArgumentoNaoPassado``), ``ESP`` optional; other
    names go to ``outros``."""
    from entrada_estruturas import ArgumentoNaoPassado
    from fadiga_vegetacao import DependenciaFadiga

    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise DependenciaFadiga(nome, chamada, 'no provider for this routine')
            return outros(nome, chamada, regs)
        faltando = [k for k in ARGUMENTOS_EXIGIDOS[nome] if k not in regs]
        if faltando:
            raise ArgumentoNaoPassado(nome, chamada, faltando)
        entrada = {k: regs.get(k, 0) & M32 for k in REG7}
        if 'ESP' in regs:
            entrada['ESP'] = regs['ESP']
        saida = buscas.chamar(nome, entrada)
        incertos = dict(saida.get('_incertos') or {})
        for k in REG7:
            if k not in regs and saida[k] == entrada[k]:
                incertos[k] = M32
        saida = {k: saida[k] for k in REG7}
        if incertos:
            saida['_incertos'] = incertos
        return saida
    return externo
