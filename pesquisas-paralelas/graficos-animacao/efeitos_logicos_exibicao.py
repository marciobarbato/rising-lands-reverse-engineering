"""Logic-state effects of the original display path (DDInit, RestoreAll 0x474b08, AffGame 0x417698).

Original-first.  ``evidencias/efeitos-logicos-exibicao.json`` records every value-changing write made inside the
dynamic extent of RestoreAll and AffGame in Missions' ``exibicao`` scenario (load tail, between frames) and every
read of those bytes by code outside the extents.  Result: **no byte that logic code reads is written by either
routine in the captured domain**.  The providers therefore return an empty write list, but only inside the domain
the capture proves; every other state raises a named stop instead of assuming the same.  No pixel, surface, bank
or stack byte is produced (display output).

The providers take ``memoria`` with ``u8/u16/u32(address)`` reads (``MemoriaDeclarada`` fits) and never write.
"""
from dataclasses import dataclass
import json
from pathlib import Path

ROTINAS = {'RestoreAll': 0x474b08, 'AffGame': 0x417698, 'DDInit': 0x43f50b}
ESTRUTURAS, ESTRUTURA_PASSO, ESTRUTURA_ESTADO = 0x49a0c8, 276, 5
# captured pool: 999 free records + the Santuario (type 2); its mode was run natively at 0..7 on five origins
ESTADOS_ESTRUTURA_PROVADOS = frozenset(range(8))
TIPO_ESTRUTURA_PROVADO = 2
# view origins run natively for both routines (isolated captures, 64x64 map): the captured (4, 6) plus a sampled grid
ORIGENS_PROVADAS = frozenset({
    (0, 0), (0, 1), (0, 2), (0, 6), (0, 7), (0, 12), (0, 14), (0, 18), (0, 21), (0, 24),
    (0, 28), (0, 30), (0, 35), (0, 36), (0, 42), (0, 47), (4, 6), (4, 30),
    (1, 3), (2, 4), (3, 5), (4, 44), (6, 0), (6, 7), (6, 14), (6, 21), (6, 28), (6, 35), (6, 42),
    (8, 0), (8, 6), (8, 12), (8, 18), (8, 24), (8, 30), (8, 36), (8, 42),
    (8, 47), (12, 0), (12, 7), (12, 14), (12, 21), (12, 28), (12, 35), (12, 40),
    (12, 42), (16, 0), (16, 6), (16, 12), (16, 18), (16, 24), (16, 30), (16, 36),
    (16, 42), (16, 47), (18, 0), (18, 7), (18, 14), (18, 21), (18, 28), (18, 35),
    (18, 42), (24, 0), (24, 6), (24, 7), (24, 12), (24, 14), (24, 18), (24, 21),
    (24, 24), (24, 28), (24, 30), (24, 35), (24, 36), (24, 42), (24, 47), (30, 0),
    (30, 7), (30, 14), (30, 21), (30, 28), (30, 35), (30, 42), (32, 0), (32, 6),
    (32, 12), (32, 18), (32, 24), (32, 30), (32, 36), (32, 42), (32, 47), (36, 0),
    (36, 7), (36, 14), (36, 21), (36, 28), (36, 35), (36, 42), (39, 0), (39, 6),
    (39, 12), (39, 18), (39, 24), (39, 30), (39, 36), (39, 42), (39, 47),
})
ORIGENS_RESTOREALL_PROVADAS = ORIGENS_PROVADAS
# Exact native probe states; these additions prove AffGame only, not RestoreAll.
ORIGENS_PROVADAS |= frozenset(tuple(v) for v in json.loads(
    Path(__file__).with_name('camadas_colheita_m3.json').read_text())['AffGame_origins'])
ORIGENS_ANTERIORES = {'AffGame': ORIGENS_PROVADAS, 'RestoreAll': ORIGENS_RESTOREALL_PROVADAS}
# Finite, original-only 3840-call matrix, committed and audited before this extension.
GRADE_VISTAS = json.loads(Path(__file__).with_name('origens_efeitos_monde01.json').read_text())
ORIGENS_PROVADAS |= frozenset(map(tuple, GRADE_VISTAS['origins_by_routine']['AffGame']))
ORIGENS_RESTOREALL_PROVADAS |= frozenset(map(tuple, GRADE_VISTAS['origins_by_routine']['RestoreAll']))
VIEWPORT, TELA = (25, 17), (800, 600)               # DDInit hi-res values (0x508724/26, 0x49a018/1a)
CURSOR_RNG_SITIOS = (0x407dd3, 0x411147, 0x412392, 0x415b77, 0x415c19, 0x43f191)   # display-side 0x4e1d18 writers


class DependenciaExibicao(Exception):
    """A display-path branch whose logic-state effect the capture did not prove."""
    def __init__(self, rotina, sitio, motivo):
        super().__init__(f'{rotina} @0x{sitio:x}: {motivo}')
        self.rotina, self.sitio, self.motivo = rotina, sitio, motivo


@dataclass(frozen=True)
class EfeitosExibicao:
    rotina: str
    escritas: tuple = ()          # (address, width, value): logic-state stores; empty for the proved domain
    verificacoes: tuple = ()      # (name, observed) guard values read, in order
    liberacoes: tuple = ()        # allocator frees in call order (DeleteBank)
    eax: object = None            # EAX observed at the original return; None when it is a leftover register


def _guardas_estruturas(memoria, rotina, lidas, habitado=None):
    estados = {memoria.u8(ESTRUTURAS + i*ESTRUTURA_PASSO + ESTRUTURA_ESTADO) for i in range(1000)}
    lidas.append(('structure states', tuple(sorted(estados))))
    ocupadas = [i for i in range(1000) if memoria.u8(ESTRUTURAS + i*ESTRUTURA_PASSO + ESTRUTURA_ESTADO)]
    simples = estados <= ESTADOS_ESTRUTURA_PROVADOS and len(ocupadas) <= 1 and all(
        memoria.u8(ESTRUTURAS + i*ESTRUTURA_PASSO + 8) == TIPO_ESTRUTURA_PROVADO for i in ocupadas)
    par_cave = False
    if rotina in ('AffGame','RestoreAll') and ocupadas == [0, 1]:
        r0, r1 = ESTRUTURAS, ESTRUTURAS+ESTRUTURA_PASSO
        modo = memoria.u8(r1+5);dono = memoria.u8(r1+4);vida = memoria.u16(r1+0xa);dano = memoria.u16(r1+6)
        par_cave = (memoria.u8(0x508041) == 0 and memoria.u8(r0+8) == 2 and memoria.u8(r0+5) in (4,5) and memoria.u8(r0+4) == 0
            and memoria.u16(r0+6) == 0 and memoria.u16(r0+0xa) == 600
            and memoria.u8(r1+8) == 3 and (dano == 0 or rotina=='AffGame' and dano<=100 and _raide_s1_provado(memoria,rotina,memoria.u8(MONSTROS)))
            and ((modo == 2 and dono == 0xc8 and vida <= 100) or (modo == 5 and dono in (0,0xc8) and vida == 100)))
        if par_cave:lidas.append(('native sanctuary/CAVE pair', (memoria.u8(r0+5),modo,dono,vida,dano)))
    if not simples and not par_cave:
        raise DependenciaExibicao(rotina, CURSOR_RNG_SITIOS[0], f'structure states {sorted(estados)}, occupied '
                                  f'records {ocupadas}: outside the single sanctuary or native sanctuary/CAVE pair domain')
    for i in ocupadas:
        # AffBatiments 0x408627: mode 3 without habitation advances 0x4e1d18 (0x408679); the captured Santuario is inhabited
        if memoria.u8(ESTRUTURAS + i*ESTRUTURA_PASSO + ESTRUTURA_ESTADO) == 3 and not (callable(habitado) and habitado(i)):
            raise DependenciaExibicao(rotina, 0x40863e, f'structure {i} in mode 3 needs BatimentEstHabiter true '
                                      '(uninhabited advances the RNG cursor; not captured)')


def _guardas(memoria, rotina, habitado=None):
    lidas = []
    def ler(nome, valor):
        lidas.append((nome, valor))
        return valor
    ler('[0x4dfb44]', memoria.u8(0x4dfb44))      # shake counter: modelled by _voltas below
    viewport = (ler('[0x508724]', memoria.u16(0x508724)), ler('[0x508726]', memoria.u16(0x508726)))
    if viewport != VIEWPORT:
        raise DependenciaExibicao(rotina, 0x4178f7, f'viewport {viewport} is not the captured {VIEWPORT}')
    origem = (ler('[0x508720]', memoria.u16(0x508720)), ler('[0x508722]', memoria.u16(0x508722)))
    origens = ORIGENS_RESTOREALL_PROVADAS if rotina == 'RestoreAll' else ORIGENS_PROVADAS
    if origem not in origens:
        raise DependenciaExibicao(rotina, CURSOR_RNG_SITIOS[3], f'view origin {origem}: vegetation/terrain handlers '
                                  '(0x411147, 0x412392, 0x415b77/0x415c19) only proved native on the sampled origins')
    if origem not in ORIGENS_ANTERIORES[rotina]:
        mapa = (ler('[0x497168]', memoria.u16(0x497168)), ler('[0x49716a]', memoria.u16(0x49716a)))
        camera = ler('[0x508041]', memoria.u8(0x508041))
        modo = ler('[0x4e2f78]', memoria.u8(0x4e2f78))
        if mapa != tuple(GRADE_VISTAS['map']) or camera != GRADE_VISTAS['camera'] or modo != GRADE_VISTAS['mode']:
            raise DependenciaExibicao(rotina, CURSOR_RNG_SITIOS[3],
                f'finite native view matrix requires map64x64, camera0 and mode0x12; got {mapa}, {camera}, {modo:#x}')
    _guardas_estruturas(memoria, rotina, lidas, habitado)
    monstros = memoria.u8(MONSTROS)
    # Historical no-wave providers need only DGROUP and projectile memory.
    # Request the new full-unit-pool contract only for an extended raid domain.
    raide_s1=monstros>1 and _raide_s1_provado(memoria,rotina,monstros)
    if monstros > 1 and not raide_s1:
        raise DependenciaExibicao(rotina, 0x41591f, f'monster count {monstros}: only 0 and 1 (raid unit 16, '
                                  'on screen or not) captured; a second monster is not proved')
    pool = memoria.u32(POOL_PROJETEIS)
    ativos = [i for i in range(100) if memoria.u8(pool + 56*i + 2)]
    if not raide_s1 and (len(ativos)>1 or any(
            memoria.u8(pool+56*i) in range(9,14) or i>0 and memoria.u8(pool+56*i) in (14,15,16)
            for i in ativos)):
        raide_s1=_raide_s1_provado(memoria,rotina,monstros)
    def projetil_provado(i):
        r = pool + 56*i
        if memoria.u8(r) in TIPOS_PROJETIL_PROVADOS:return True
        if rotina=='AffGame' and i<=6 and raide_s1 and memoria.u8(r+2)==1:
            kind,phase=memoria.u8(r),memoria.u8(r+0x18)
            if kind in range(9,14) and phase==0:return True
            if kind in (14,15,16) and phase<(32 if kind==14 else 16):return True
        # Native P3 frames245..260 / 309..324: types15/16, all16 phases, active state1, slot0; no logic writer.
        return (rotina == 'AffGame' and i == 0 and memoria.u8(r) in (14,15,16) and memoria.u8(r+2) == 1
                and memoria.u8(r+0x18) < (32 if memoria.u8(r)==14 else 16))
    multiple_s1=len(ativos)<=7 and raide_s1
    if (len(ativos) > 1 and not multiple_s1) or any(not projetil_provado(i) for i in ativos):
        raise DependenciaExibicao(rotina, 0x46ff70, f'projectile slots {ativos}: captured only one raid effect '
                                  f'projectile of type {sorted(TIPOS_PROJETIL_PROVADOS)} or the native AffGame type15/16 cycles')
    if rotina=='AffGame' and memoria.u16(0x507d54)!=memoria.u16(0x507d56):
        index=memoria.u16(0x507d54)
        if index>=256:raise DependenciaExibicao(rotina,0x469c5f,'Alert queue index outside the captured ring')
        if memoria.u16(0x4e7754+518*index+0x104)!=399:
            from alertas_s1_graficos import planejar_zonas,DependenciaZonasAlerta
            try:zones=planejar_zonas(memoria,memoria.u8(0x508041))
            except DependenciaZonasAlerta as error:raise DependenciaExibicao(rotina,error.address,error.reason) from error
    return tuple(lidas)


MONSTROS, POOL_PROJETEIS, TIPOS_PROJETIL_PROVADOS = 0x50b178, 0x5080f0, frozenset({31, 32})
CURSOR, TREMOR, CONTADOR_QUADROS, PAGINAS = 0x4e1d18, 0x4dfb44, 0x508f7c, 0x49a05b


def _raide_s1_provado(memoria,rotina,monstros):
    """S1 clean soldier waves: original mixed combat/death and prepared2/3/5 raiders.

    The native observer hashes all world blocks and records every changed DGROUP
    byte. No world input or shared RNG cursor changes in these display calls.
    RestoreAll and other monster configurations retain their existing boundary.
    """
    if rotina!='AffGame' or not 0<=monstros<=5 or memoria.u8(0x508041)!=0:return False
    cave=ESTRUTURAS+ESTRUTURA_PASSO
    if memoria.u8(cave+5)!=5 or memoria.u8(cave+8)!=3 or memoria.u8(cave+4)!=0:return False
    pool=memoria.u32(0x4e19a0)
    foreign=[];alive=0
    def unit_byte(address):
        try:return memoria.u8(address)
        except KeyError as error:
            raise DependenciaExibicao(rotina,0x41591f,'Late-S1 wave/fire proof requires the complete native unit pool') from error
    friendly={0:(1,2,4,7,19),1:(2,7,19),5:(2,4,5,7,19),7:(2,5,7,11,15),8:(1,2,7,19),9:(2,7,13,14)}
    for i in range(800):
        r=pool+276*i;state=unit_byte(r+2)
        if not state:continue
        owner,kind=unit_byte(r),unit_byte(r+1)
        if unit_byte(r+0x99) or unit_byte(r+0xdc):return False
        if owner==4:
            if kind!=0 or state not in (1,2,4,7):return False
            foreign.append(i)
            alive+=state!=4
        elif owner!=0 or state not in friendly.get(kind,()):return False
        if owner==0 and state==5:
            task=unit_byte(r+0x89)
            if kind==7 and task not in range(6) or kind==5 and task not in range(4):return False
    # S1 frame12460 draws the new corpse before the next phase recounts it:
    # the count is still2 for that one frame, then becomes1 at12461.
    return len(foreign)<=6 and alive<=monstros<=len(foreign)


def _voltas(memoria, voltas):
    """DDFlipPage 0x43f14f shake path, ``voltas`` consecutive calls: the logic-state stores.

    While [0x4dfb44] (n) is nonzero a call reads table[cursor], advances the cursor (u8) and, when the low byte of the
    frame counter [0x508f7c] is even, decrements n.  The table value only picks the BltFast offset (display).
    """
    cursor, n, par = memoria.u8(CURSOR), memoria.u8(TREMOR), memoria.u8(CONTADOR_QUADROS) & 1 == 0
    cursor0, n0 = cursor, n
    for _ in range(voltas):
        if n:
            cursor = (cursor+1) & 0xff
            if par:
                n -= 1
    return (((CURSOR, 1, cursor),) if cursor != cursor0 else ()) + (((TREMOR, 1, n),) if n != n0 else ())


def restaurar_tudo(memoria, habitado=None):
    """RestoreAll 0x474b08 in the captured domain: only the shake path of its two DDFlipPage calls writes logic state."""
    guardas = _guardas(memoria, 'RestoreAll', habitado)
    return EfeitosExibicao('RestoreAll', _voltas(memoria, 2), guardas)


def desenhar_jogo(memoria, habitado=None):
    """AffGame: alert input-zone stores, then the existing flip-loop shake stores."""
    guardas = _guardas(memoria, 'AffGame', habitado)
    zones=()
    index=memoria.u16(0x507d54)
    if index!=memoria.u16(0x507d56) and memoria.u16(0x4e7754+518*index+0x104)!=399:
        from alertas_s1_graficos import planejar_zonas,escritas_zonas
        zones=escritas_zonas(memoria,planejar_zonas(memoria,memoria.u8(0x508041)))
    return EfeitosExibicao('AffGame', zones+_voltas(memoria, memoria.u8(PAGINAS)+1), guardas)


def inicializar_dimensoes(memoria, alta_resolucao=True):
    """DDInit 0x43f50b stores read by logic: screen 800x600 and the 25x17 viewport (hi-res path only)."""
    if not alta_resolucao:
        raise DependenciaExibicao('DDInit', 0x43f50b, 'low-resolution path not captured')
    escritas = ((0x49a018, 2, TELA[0]), (0x49a01a, 2, TELA[1]), (0x508724, 2, VIEWPORT[0]), (0x508726, 2, VIEWPORT[1]))
    return EfeitosExibicao('DDInit', escritas)


# ---- display calls MenuInit makes in phase (a): LockSurface, DeleteBank, FilledBox, UnlockSurface, FlipPage -----
BLOQUEIO_PONTEIRO, BLOQUEIO_CONTADOR = 0x4e17a4, 0x4e17a8      # nested-lock bookkeeping (net unchanged per phase)


def ddlocksurface(memoria, ponteiro_superficie):
    """DDLockSurface 0x43f3b4, first lock: stores the surface pointer and count 1; returns the pointer in EAX."""
    if memoria.u32(BLOQUEIO_CONTADOR) != 0:
        raise DependenciaExibicao('DDLockSurface', 0x43f3b4, 'nested lock: only count 0 -> 1 was captured')
    return EfeitosExibicao('DDLockSurface', ((BLOQUEIO_PONTEIRO, 4, ponteiro_superficie), (BLOQUEIO_CONTADOR, 4, 1)),
                           eax=ponteiro_superficie)


def ddunlocksurface(memoria):
    """DDUnlockSurface, last unlock (count 1 -> 0): clears pointer and count; EAX = 1."""
    if memoria.u32(BLOQUEIO_CONTADOR) != 1:
        raise DependenciaExibicao('DDUnlockSurface', 0x43f445, 'only the 1 -> 0 unlock was captured')
    return EfeitosExibicao('DDUnlockSurface', ((BLOQUEIO_PONTEIRO, 4, 0), (BLOQUEIO_CONTADOR, 4, 0)), eax=1)


def ddflippage(memoria, copiar=1):
    """DDFlipPage 0x43f14f(1): BltFast pair; DGROUP writes only through the shake path (see _voltas); EAX = 0."""
    return EfeitosExibicao('DDFlipPage', _voltas(memoria, 1), eax=0)


def filledbox(memoria):
    """FilledBox 0x45cacd: writes surface pixels only (display output); no DGROUP or heap store; EAX is a leftover pointer."""
    return EfeitosExibicao('FilledBox', ())


def deletebank(memoria, banco):
    """DeleteBank 0x418a12: the frees in original order and the zeroed count; ``banco`` 0 returns untouched.

    Layout read from the bytes: u16 count at +0, u32 table at +4 (4-byte entries), entry+8 a sub-block.  Per entry
    the sub-block then the entry are freed; then the count is zeroed, the table freed, the bank freed.
    """
    if banco == 0:
        return EfeitosExibicao('DeleteBank')
    n, tabela = memoria.u16(banco), memoria.u32(banco+4)
    ordem = []
    for i in range(n):
        entrada = memoria.u32(tabela+4*i)
        if entrada:
            sub = memoria.u32(entrada+8)
            if sub:
                ordem.append(sub)
            ordem.append(entrada)
    return EfeitosExibicao('DeleteBank', ((banco, 2, 0),), liberacoes=tuple(ordem)+(tabela, banco), eax=0)
