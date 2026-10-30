"""S1's first fight (frames 11500-12460): Core's terrain/structure queries, task-list helpers and structure voice.

Translated from the intact bytes (original SHA-256 6c556520...43fb) after the original-only S1 capture
``evidencias/lacunas-s1/captura-c.json.xz`` (``validar_lacunas_s1.py --janela c --capturar``). Every register:

- TerrainEstMontagne 0x47653c: AL = 1 when the tile word [0x507d70][cell] is in [0x1dd, 0x260); EAX = the tile's
  high byte above AL; EDX preserved.
- BatimentGetCaseAdjacent 0x4239a0 (epilogue 0x423997): the first cell of the 3x3 block around DX (rows dy = -1..1,
  then columns dx = -1..1, each on the 256-cell grid) that is a set BatimentCollision cell of structure AX's
  footprint. EAX = (dy<<8) + dx + the entry EDX, where dy and dx are dword locals whose upper words are stack
  residue (exact when ESP is given and readable); 0xffff when none. EDX as the last load leaves it.
- ChercheCaseBatiment 0x41b489 (epilogue 0x41db1e): the first existing structure (0..999) whose footprint
  rectangle holds cell AX (no mask: ``origin + (row<<8) + column == cell`` without wrap); EAX = its index or
  0xffff; every other register preserved.
- GetCaseIndiceBatiment 0x41aab2: ``incursao_core.caso_indice_estrutura`` (already translated; first reached by S1).
- listDeleteElem 0x47d03a: push element EDX on the free list EAX ([+0] head, [+4] count, [+8] size, [+0xc]
  base); EAX = EDX.
- listUnlinkElem 0x47d11a: unlink element EDX from list EAX (walk from the head; the first match is spliced and
  the count decremented); EAX = EDX = the element, or -1 when absent.
- iaProbReturnTo 0x47da54: task EAX (records of 96 bytes at 0x512320): +0x5e = 0, +0x5f = 1, +0x14 = 0,
  +0x54 = EDX; EAX = the record address, EDX = the entry EAX.
- VoixOffAsk 0x41a1ac: structure AX's voice: PlaySnd_StopSound(EAX = record + 0x100, EBX = 0), then
  PlaySnd_PostSound(EAX = 0x41, EBX = record + 0x100, ECX = BL, EDX = (a<<16)|(b<<8), pushed 0x100) with (a, b) by
  DX = 0..6 (table 0x41a190: (0,0) (1,3) (2,0) (1,0) (1,1) (2,1) (2,2)); DX > 6 keeps EBX = 0 and b = DX. EAX =
  the post request's return.

``chamar(nome, regs, pilha=())`` takes EAX..EBP (and optionally ESP) and returns EAX..EBP and ESP.
Dependency (never defaulted): ``som(nome, registradores, pilha) -> EAX`` for Audio's PlaySnd_StopSound 0x48aac0 and
PlaySnd_PostSound 0x48aa79 (the shape of ``selecao_ordens``; ``chamada`` passed when the provider declares it).
Outside the domain (``ForaDoDominioLuta``, before any store): structure indexes above 999.
"""
import inspect

from chamadas_quadro_core import colisao_estrutura
from fadiga_vegetacao import _Quadro
from incursao_core import caso_indice_estrutura

M32 = 0xffffffff
REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
ESTRUTURAS, PASSO_ESTRUTURA = 0x49a0c8, 276
DIMENSOES = 0x495d8c
GRADE_TILES = 0x507d70
TAREFAS, PASSO_TAREFA = 0x512320, 96
VOZ = {0: (0, 0), 1: (1, 3), 2: (2, 0), 3: (1, 0), 4: (1, 1), 5: (2, 1), 6: (2, 2)}
ROTINAS = {'TerrainEstMontagne': 0x47653c, 'BatimentGetCaseAdjacent': 0x4239a0, 'ChercheCaseBatiment': 0x41b489,
           'GetCaseIndiceBatiment': 0x41aab2, 'listDeleteElem': 0x47d03a, 'listUnlinkElem': 0x47d11a,
           'iaProbReturnTo': 0x47da54, 'VoixOffAsk': 0x41a1ac}


class ForaDoDominioLuta(NotImplementedError):
    def __init__(self, rotina, endereco, motivo):
        self.rotina, self.endereco = rotina, endereco
        super().__init__(f'{rotina}: {motivo} (0x{endereco:x}); no store was made by this branch')


class DependenciaLuta(NotImplementedError):
    def __init__(self, rotina, chamada):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} called at 0x{chamada:x}: provider required')


def _s16(v):
    v &= 0xffff
    return v - 0x10000 if v & 0x8000 else v


class ConsultasLuta:
    def __init__(self, memoria, *, som=None):
        self.m, self.som = memoria, som

    def chamar(self, nome, regs, pilha=()):
        if nome not in ROTINAS:
            raise KeyError(f'{nome} is not a translated S1 fight routine')
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

    def _som(self, nome, chamada, regs, pilha):
        if self.som is None:
            raise DependenciaLuta(nome, chamada)
        if 'chamada' in inspect.signature(self.som).parameters:
            return self.som(nome, regs, pilha, chamada=chamada) & M32
        return self.som(nome, regs, pilha) & M32

    # ------------------------------------------------------------ terrain / structures
    def _TerrainEstMontagne(self, r, esp):
        t = self.m.u16((self.m.u32(GRADE_TILES) + 2 * (r['EAX'] & 0xffff)) & M32)
        return dict(r, EAX=(t & 0xff00) | int(0x1dd <= t < 0x260))

    def _GetCaseIndiceBatiment(self, r, esp):
        return dict(r, **caso_indice_estrutura(self.m, r['EAX']))

    def _estrutura(self, nome, endereco, i):
        if i > 999:
            raise ForaDoDominioLuta(nome, endereco, f'structure index {i}')
        base = ESTRUTURAS + PASSO_ESTRUTURA * i
        tipo = self.m.u8(base + 8)
        return base, tipo, self.m.u16(DIMENSOES + 52 * tipo), self.m.u16(DIMENSOES + 2 + 52 * tipo)

    def _ChercheCaseBatiment(self, r, esp):
        m = self.m
        alvo = r['EAX'] & 0xffff
        for i in range(1000):
            base = ESTRUTURAS + PASSO_ESTRUTURA * i
            if not m.u8(base + 5):
                continue
            origem = m.u16(base + 2)
            tipo = m.u8(base + 8)
            larg, alt = m.u16(DIMENSOES + 52 * tipo), m.u16(DIMENSOES + 2 + 52 * tipo)
            if any(origem + (y << 8) + x == alvo for y in range(alt) for x in range(larg)):
                return dict(r, EAX=i)
        return dict(r, EAX=0xffff)

    def _BatimentGetCaseAdjacent(self, r, esp):
        m = self.m
        q = _Quadro(m, None if esp is None else (esp - 0x40) & M32, 0x40)
        incertos = {}
        indice = r['EAX'] & 0xffff
        celula = r['EDX'] & 0xffff
        x, y = celula % 256, celula // 256
        edx = M32
        q.w16(0x24, 0xffff)
        q.w16(0x14, 0xff00)
        while True:                                            # 0x4239ef
            dy = _s16(q.r16(0x24))
            if dy > 1:
                return dict(r, EAX=0xffff, EDX=edx & M32)
            edx = y
            if 0 <= y + dy < 0x100:
                q.w16(0x1c, 0xffff)
                cand = (r['EDX'] + 0xffff + q.r16(0x14)) & 0xffff   # [0x18]'s low word (the high word is unused)
                while True:                                    # 0x423a44
                    dx = _s16(q.r16(0x1c))
                    if dx > 1:
                        break
                    edx = x
                    if 0 <= x + dx < 0x100:
                        base, tipo, larg, alt = self._estrutura('BatimentGetCaseAdjacent', 0x423a6b, indice)
                        origem = m.u16(base + 2)
                        edx = tipo * 0x34
                        achou = False
                        for cy in range(alt):
                            for cx in range(larg):
                                edx = (cy << 8) + origem + cx
                                if edx == cand:
                                    s = colisao_estrutura(m, tipo, (larg * cy + cx) & 0xffff)
                                    edx = s.get('EDX', (larg * cy + cx) & 0xffff)
                                    if s['EAX'] & 0xff:
                                        achou = True
                                        break
                            if achou:
                                break
                        if achou:
                            v24, i24 = q.r32_residuo(0x24)
                            v1c, i1c = q.r32_residuo(0x1c)
                            if i24 or i1c:
                                incertos['EAX'] = 0xffff0000
                            return dict(r, EAX=((v24 << 8) + v1c + r['EDX']) & M32, EDX=edx & M32,
                                        _incertos=incertos)
                    cand = (cand + 1) & 0xffff                 # 0x423a31
                    q.w16(0x1c, q.r16(0x1c) + 1)
            q.w8(0x15, q.r8(0x15) + 1)                         # 0x4239e6
            q.w16(0x24, q.r16(0x24) + 1)

    # ------------------------------------------------------------ task lists
    def _listDeleteElem(self, r, esp):
        m, lista, e = self.m, r['EAX'], r['EDX']
        ptr = (m.u32(lista + 8) * e + m.u32(lista + 0xc)) & M32
        m.u32(ptr, m.u32(lista))
        m.u32(lista, e)
        m.u32(lista + 4, (m.u32(lista + 4) + 1) & M32)
        return dict(r, EAX=e)

    def _listUnlinkElem(self, r, esp):
        m, lista, alvo = self.m, r['EAX'], r['EDX']
        tam, base = m.u32(lista + 8), m.u32(lista + 0xc)
        ptr_alvo = (base + tam * alvo) & M32
        anterior, atual = M32, m.u32(lista)
        while atual != M32:
            if atual == alvo:
                if anterior == M32:
                    m.u32(lista, m.u32(ptr_alvo))
                else:
                    m.u32((base + tam * anterior) & M32, m.u32(ptr_alvo))
                m.u32(lista + 4, (m.u32(lista + 4) - 1) & M32)
                break
            anterior, atual = atual, m.u32((base + tam * atual) & M32)
        return dict(r, EAX=atual, EDX=atual)

    def _iaProbReturnTo(self, r, esp):
        m = self.m
        rec = (TAREFAS + PASSO_TAREFA * r['EAX']) & M32
        m.u8(rec + 0x5e, 0)
        m.u8(rec + 0x5f, 1)
        m.u32(rec + 0x14, 0)
        m.u32(rec + 0x54, r['EDX'])
        return dict(r, EAX=rec, EDX=r['EAX'])

    # ------------------------------------------------------------ structure voice
    def _VoixOffAsk(self, r, esp):
        i = r['EAX'] & 0xffff
        if i > 999:
            raise ForaDoDominioLuta('VoixOffAsk', 0x41a1b5, f'structure index {i}')
        canal = (ESTRUTURAS + PASSO_ESTRUTURA * i + 0x100) & M32
        cl = r['EBX'] & 0xff
        ecx = (r['ECX'] & 0xffffff00) | cl
        eax = self._som('PlaySnd_StopSound', 0x41a1d3, dict(r, EAX=canal, EBX=0, ECX=ecx), [])
        dx = r['EDX'] & 0xffff
        a, b = VOZ[dx] if dx <= 6 else (0, r['EDX'])
        edx = ((a & 0xffff) << 16) | ((b & 0xffff) << 8)
        regs = dict(r, EAX=0x41, EBX=canal, ECX=cl, EDX=edx & M32)
        eax = self._som('PlaySnd_PostSound', 0x41a221, regs, [0x100])
        return dict(r, EAX=eax, EBX=canal, EDX=edx & M32)
