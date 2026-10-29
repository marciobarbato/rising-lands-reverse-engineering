"""Missions frame callees: EvenementEnCours 0x4581b6 and TestFinDeMission 0x458606.

Translated after the original-only isolated captures
(evidencias/captura-isolada-missoes-quadro1.json) of both routines at the
exact MONDE01 frame-0 and frame-1 entry states.  Every input is an explicit
live view at its original address; every other routine is a provider the
caller supplies.  A provider that a reached branch needs and the caller did
not supply raises ``DependenciaFimMissao`` at the original CALL, after the
effects that precede it, exactly like a stopped native run.

Register facts the translation relies on, all from the intact bytes: the
structure getters 0x41a735/0x41a08c/0x41a4f4, BatimentGetCase 0x41aee2 and
CaseGetZoneInfluence 0x47bf66 preserve ECX/EDX; RechercheGetNbInvention
0x470554 does not touch EDX; PlayerEstAllie 0x46d838 clobbers DL, which the
caller never reads afterwards.  Importing this module executes nothing.
"""
from dataclasses import dataclass
from typing import Callable, Optional

CONDICOES = 0x4e1d20          # 10 records x 10 bytes: type u8, pad u8, four u16 parameters
ESTADO = 0x4e1d84             # +0 latch, +1 counted owners, +2..+3 untouched, +4..+13 per-record marks
CONTAGEM_INICIAL = 0x4e1a3a   # u16 tested after the condition loop
EXERCITOS = 0x4e1928          # four u16 (type-5 condition)
EXERCITOS_IA = 0x4dfaa8       # four u32 (type-5 condition)
EVENEMENT = 0x4e1b0e          # EvenementEnCours AL source


class DependenciaFimMissao(NotImplementedError):
    """A routine the caller did not supply, raised at the original CALL."""
    def __init__(self, rotina, chamada, motivo=''):
        self.rotina, self.chamada = rotina, chamada
        super().__init__(f'{rotina} required at TestFinDeMission CALL 0x{chamada:x}' + (f': {motivo}' if motivo else ''))


def _vista(memoria, tamanho, nome, escrita=False):
    try:
        v = memoryview(memoria)
    except TypeError as erro:
        raise ValueError(f'{nome} requires an explicit byte buffer') from erro
    if v.ndim != 1 or not v.c_contiguous or v.itemsize != 1 or len(v) != tamanho:
        raise ValueError(f'{nome} requires exactly {tamanho} contiguous bytes')
    if escrita and v.readonly:
        raise ValueError(f'{nome} must be writable')
    return v.cast('B')


def evento_em_curso(evenement_u8):
    """EvenementEnCours 0x4581b6: AL = byte 0x4e1b0e; no store, upper EAX bits not modeled."""
    return _vista(evenement_u8, 1, 'EvenementEnCours')[0]


@dataclass
class ConsultasFimMissao:
    """Providers called by TestFinDeMission, each with its original entry and register contract."""
    existe: Callable[[int], int]                      # BatimentExiste 0x41a735 (AX index) -> AL
    dono: Callable[[int], int]                        # BatimentGetPlayer 0x41a08c (AX index) -> AL
    tipo: Callable[[int], int]                        # BatimentGetType 0x41a4f4 (AX index) -> AL
    recursos: Callable[[int, int, int, int], bool]    # TestRessource 0x4676e5 (player, food AX, stone DX, parts BX)
    numero_missao: Callable[[], int]                  # MissionGetNum 0x46c11a -> AX
    celula: Optional[Callable[[int], int]] = None     # BatimentGetCase 0x41aee2 (AX index) -> AX cell
    zona: Optional[Callable[[int], int]] = None       # CaseGetZoneInfluence 0x47bf66 (AX cell, BX 0) -> AX zone
    invencoes: Optional[Callable[[int], int]] = None  # RechercheGetNbInvention 0x470554 (AL player) -> AL
    aliado: Optional[Callable[[int, int], int]] = None  # PlayerEstAllie 0x46d838 (AL player, DL other) -> AL
    canto_zona: Optional[Callable[[int], int]] = None   # GetTopLeftCaseZoneInfluence 0x47c114 (AX zone, DX 0) -> AX
    iluminada: Optional[Callable[[int, int], int]] = None  # CaseEstIlluminee 0x47693a (AX cell, DL player) -> AL

    def chamar(self, campo, chamada, *args):
        f = getattr(self, campo)
        if f is None:
            nomes = dict(celula='BatimentGetCase 0x41aee2', zona='CaseGetZoneInfluence 0x47bf66',
                         invencoes='RechercheGetNbInvention 0x470554', aliado='PlayerEstAllie 0x46d838',
                         canto_zona='GetTopLeftCaseZoneInfluence 0x47c114', iluminada='CaseEstIlluminee 0x47693a')
            raise DependenciaFimMissao(nomes[campo], chamada)
        return f(*args)


def _u16(v, o):
    return v[o] | v[o+1] << 8


def _zona_coincide(cond, base, zona):
    """Three zone words at +4/+6/+8: 0x00ff is a wildcard, otherwise the low-16 zone must match."""
    for o in (4, 6, 8):
        z = _u16(cond, base+o)
        if z == 0xff or zona & 0xffff == z:
            return True
    return False


def testar_fim_missao(jogador, condicoes, estado, contagem_inicial, exercitos, exercitos_ia, consultas):
    """TestFinDeMission 0x458606: AL result; updates the latch, owner count and per-record marks.

    ``condicoes`` 100 bytes at 0x4e1d20 (read), ``estado`` 14 bytes at
    0x4e1d84 (written), ``contagem_inicial`` 2 bytes at 0x4e1a3a, ``exercitos``
    8 bytes at 0x4e1928 and ``exercitos_ia`` 16 bytes at 0x4dfaa8 (read only
    by type-5 records).  ``jogador`` is AL; only its low byte is used.
    """
    cond = _vista(condicoes, 100, 'TestFinDeMission conditions 0x4e1d20')
    est = _vista(estado, 14, 'TestFinDeMission state 0x4e1d84', escrita=True)
    inicial = _vista(contagem_inicial, 2, 'TestFinDeMission word 0x4e1a3a')
    ex = _vista(exercitos, 8, 'TestFinDeMission 0x4e1928')
    ex_ia = _vista(exercitos_ia, 16, 'TestFinDeMission 0x4dfaa8')
    q = consultas
    jogador &= 0xff
    resultado = 1                 # [esp+0x10]
    ultimo_tipo4 = None           # [esp+8]: set only by a type-4 match (0x4587db)
    marca = lambda i: est[4+i]

    def definir(i, valor):
        est[4+i] = valor

    for i in range(10):
        o = 10*i
        t = cond[o]
        if t in (0, 1, 2):
            # 0x458644 / 0x4586a7 / 0x45898a: one resource argument, the others 0.
            p = _u16(cond, o+2)
            comida, pedra, pecas = (p, 0, 0) if t == 0 else (0, p, 0) if t == 1 else (0, 0, p)
            if q.recursos(jogador, comida, pedra, pecas):
                if marca(i) == 0:
                    definir(i, 1)
            else:
                resultado = 0
                if marca(i):
                    definir(i, 0)
        elif t == 3:
            # 0x45878d: AL = inventions of the player, compared with DX = parameter (EDX kept by the callee).
            p = _u16(cond, o+2)
            if q.chamar('invencoes', 0x45879c, jogador) & 0xff >= p:
                if marca(i) == 0:
                    definir(i, 1)
            else:
                resultado = 0
                if marca(i):
                    definir(i, 0)
        elif t == 4:
            # 0x4587cc: scan every structure of the player with type == parameter.
            for j in range(1000):
                if not q.existe(j):
                    continue
                if q.dono(j) & 0xff != jogador:
                    continue
                if q.tipo(j) & 0xff != _u16(cond, o+2):
                    continue
                celula = q.chamar('celula', 0x45883f, j) & 0xffff
                zona = q.chamar('zona', 0x45884b, celula)
                if _zona_coincide(cond, o, zona):
                    ultimo_tipo4 = i
                    if marca(i) == 0:
                        definir(i, 1)
                elif marca(i):
                    definir(i, 0)
            if marca(i) == 0:
                resultado = 0
        elif t == 5:
            # 0x4588de: no non-allied opponent may keep units (0x4e1928) or AI armies (0x4dfaa8).
            definir(i, 1)
            for c in range(4):
                if c == jogador:
                    continue
                if q.chamar('aliado', 0x458903, jogador, c) & 0xff:
                    continue
                if _u16(ex, 2*c) or int.from_bytes(ex_ia[4*c:4*c+4], 'little'):
                    definir(i, 0)
            resultado &= marca(i)
        elif t == 0xff:
            # 0x458620: only a first record of 0xff (no conditions) blocks victory.
            if i == 0:
                if marca(0):
                    definir(0, 0)
                resultado = 0
    numero = q.numero_missao() & 0xffff
    if numero == 6:
        canto = q.chamar('canto_zona', 0x45870e, 0) & 0xffff
        resultado = q.chamar('iluminada', 0x45871c, canto, jogador) & 0xff
    if resultado:
        est[0] = 1
    if _u16(inicial, 0) == 0:
        resultado = 1
        est[0] = 0
    if resultado == 0 or est[0] == 0:
        return resultado
    if q.numero_missao() & 0xffff != 8 and q.numero_missao() & 0xffff != 13:
        return resultado
    # 0x458786: count the opponents owning a structure of the last matched
    # type-4 record's type inside its zones.
    if ultimo_tipo4 is None:
        raise DependenciaFimMissao('uninitialized local [esp+8]', 0x4589dc,
                                   'no type-4 match stored the record index this call')
    donos = [0, 0, 0, 0]
    o = 10*ultimo_tipo4
    for j in range(1000):
        if not q.existe(j):
            continue
        dono = q.dono(j) & 0xff
        if dono == jogador or dono == 0xc8:
            continue
        if q.tipo(j) & 0xff != _u16(cond, o+2):
            continue
        celula = q.chamar('celula', 0x458a44, j) & 0xffff
        zona = q.chamar('zona', 0x458a50, celula)
        if not _zona_coincide(cond, o, zona):
            continue
        if dono >= 4:
            raise DependenciaFimMissao('owner outside the four-byte local array', 0x458aa8,
                                       f'owner {dono} would write the caller stack')
        donos[dono] = 1
    est[1] = sum(1 for d in donos if d)
    return resultado


def consultas_publicadas(estruturas, recursos, missao_u8, **opcionais):
    """Bind the committed providers over live views; optional ones stay None unless supplied.

    ``estruturas`` is the live 276,000-byte pool at 0x49a0c8, ``recursos`` an
    Economy ``Economia`` whose ``memoria`` is the live 128-byte table at
    0x4e2ea8, ``missao_u8`` the live byte at 0x496fe4.
    """
    from consultas_missao import existe_estrutura, numero_missao
    from ataque_vivo import batiment_get_player
    from consultas_reinicio_economia import tipo_estrutura
    return ConsultasFimMissao(
        existe=lambda j: existe_estrutura(estruturas, j),
        dono=lambda j: batiment_get_player(estruturas, j),
        tipo=lambda j: tipo_estrutura(estruturas, j),
        recursos=lambda jogador, comida, pedra, pecas: recursos.suficiente(jogador, comida, pedra, pecas),
        numero_missao=lambda: numero_missao(missao_u8), **opcionais)
