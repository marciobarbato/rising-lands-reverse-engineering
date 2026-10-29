"""iaSolver rules of MONDE01's first raid task at counter 9000 (M2.3), with the war kernels they call.

Translated after the native capture ``evidencias/captura-regras-incursao-9000-ia.json`` (forced counter 9000,
Combat's course input). The capture gives each rule call's argument block, footprint, written bytes and outside
calls, and ``testes/test_regras_incursao_ia.py`` replays it.

iaSolver calls a rule with EAX pointing to an argument block: seven argument words, the player at +0x1c and the
task index at +0x20. Here a rule is ``regra(m, p, argumentos, jogador, indice) -> EAX``, the shape of Core's
``MaquinaTarefas`` ``operacoes`` (``operacoes_regras`` binds the memory and providers). Other owners'
routines are providers, ``provider(sitio=<CALL address>, **arguments)``:

| Provider | Owner | Arguments | Result used |
|---|---|---|---|
| EnginEstVivant | Core | unidade (AX) | AL |
| SetDeplaceEngin | Core | unidade (AX), destino (DX) | — |

War table: per player, 16 battle records of 0x110 bytes at ``0x51bcfc + 0x1144 * player + 0x28``:
- +0 u32 group;
- +4 u32 position (-1 = free);
- +8 u32 waiting task;
- +0xc u16 radius;
- +0xe u16.
"""
from incursao_ia import GRUPOS, PASSO_UNIDADE, UNIDADE_ATUAL, UNIDADES, primeira_unidade
from reinicio_ia import DependenciaIA

TAREFAS, PASSO_TAREFA = 0x512320, 0x60
BATALHAS, PASSO_JOGADOR_BATALHAS, PASSO_BATALHA, BATALHAS_POR_JOGADOR = 0x51bcfc + 0x28, 0x1144, 0x110, 0x10


def s32(v):
    v &= 0xffffffff
    return v - (1 << 32) if v & 0x80000000 else v


def _div(a, b):
    """x86 IDIV quotient (truncated toward zero)."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _mod(a, b):
    return a - _div(a, b) * b


def _chamar(p, rotina, sitio, **argumentos):
    provedor = p.get(rotina)
    if provedor is None:
        raise DependenciaIA(rotina, sitio)
    return provedor(sitio=sitio, **argumentos)


def _grupo(grupo):
    return (GRUPOS + (grupo << 5)) & 0xffffffff


def proxima_unidade(m):
    """iagUnitGetNextUnitInGroup 0x483825: follow +0x108 of the iterator's unit."""
    atual = m.u16(UNIDADE_ATUAL)
    m.u16(UNIDADE_ATUAL, m.u16((m.u32(UNIDADES) + atual * PASSO_UNIDADE + 0x108) & 0xffffffff))
    return m.u16(UNIDADE_ATUAL)


def _batalha(jogador, k):
    return BATALHAS + PASSO_JOGADOR_BATALHAS * jogador + PASSO_BATALHA * k


def procurar_batalha(m, jogador, posicao):
    """iagWarSearchBattleFromPos 0x487594 (EAX player, EDX position) -> battle covering the position, or -1."""
    posicao = s32(posicao)
    x, y = _mod(posicao, 0x100), _div(posicao, 0x100)
    for k in range(BATALHAS_POR_JOGADOR):
        b = _batalha(jogador, k)
        outra = s32(m.u32(b + 4))
        if outra == -1:
            continue
        bx, by, raio = _mod(outra, 0x100), _div(outra, 0x100), m.u16(b + 0xc)
        if x < bx - raio or x > bx + raio or by - raio > y or by + raio < y:
            continue
        return k
    return 0xffffffff


def nova_batalha(m, jogador, posicao, raio, grupo):
    """iagWarNewBattleToPos 0x487643 (EAX player, EDX position, BX radius, ECX group) -> battle index or -1."""
    for k in range(BATALHAS_POR_JOGADOR):
        if m.u32(_batalha(jogador, k) + 4) == posicao & 0xffffffff:
            return k
    for k in range(BATALHAS_POR_JOGADOR):
        b = _batalha(jogador, k)
        if m.u32(b + 4) != 0xffffffff:
            continue
        m.u16(b + 0xe, 0)
        m.u32(b + 4, posicao)
        m.u32(b, grupo)
        m.u16(b + 0xc, raio)
        if grupo & 0xffffffff != 0xffffffff and _grupo(grupo):
            m.u32(_grupo(grupo) + 0xc, k)
        return k
    return 0xffffffff


def dormir_tarefa(m, tarefa, tempo):
    """iaProbSleep 0x47da39 (EAX task, EDX time)."""
    t = (TAREFAS + PASSO_TAREFA * tarefa) & 0xffffffff
    m.u8(t + 0x5e, 1)
    m.u32(t + 0x14, tempo)


def esperar_batalha(m, jogador, tarefa, grupo, tempo):
    """iagWarSetWait 0x488d21 (EAX player, EDX task, EBX group, ECX time)."""
    g = _grupo(grupo)
    if g == 0:
        return
    batalha = m.u32(g + 0xc)
    m.u32((0x51bd2c + PASSO_BATALHA * batalha + PASSO_JOGADOR_BATALHAS * jogador) & 0xffffffff, tarefa)
    m.u32(g + 8, tarefa)
    if tarefa & 0xffffffff != 0xffffffff:
        dormir_tarefa(m, tarefa, tempo)


# ------------------------------------------------------------------ rules (argumentos, jogador, indice) -> EAX
def b_testa_grupo_vazio(m, p, a, jogador, indice):
    """B_TestGroupeVide 0x48232f: 1 when the group record is absent or has no unit, else -1."""
    g = _grupo(a[0])
    if g and s32(m.u16(g + 0x12)) > 0:
        return 0xffffffff
    return 1


def b_novo_conflito(m, p, a, jogador, indice):
    """B_NewConflit 0x47fee0: -1 when a battle already covers the position; else a new battle, 1 or -1."""
    if procurar_batalha(m, jogador, a[0]) != 0xffffffff:
        return 0xffffffff
    return 1 if nova_batalha(m, jogador, a[0], a[1], a[2]) != 0xffffffff else 0xffffffff


def b_espera_conflito(m, p, a, jogador, indice):
    """B_AttenteConflit 0x47ff4d: iagWarSetWait(player, task, group, time); always 1."""
    esperar_batalha(m, jogador, indice, a[0], a[1])
    return 1


def i_tempo_trajeto(m, p, a, jogador, indice):
    """I_DetermineTempsTrajet 0x482354: 40 * Chebyshev distance / the group's slowest unit (+0x98)."""
    g = _grupo(a[0])
    if not g or not m.u16(g + 0x12):
        return 0xffffffff
    lento = 0x100
    unidade = primeira_unidade(m, a[0])
    while unidade != 0xffff:
        lento = min(lento, m.u8((m.u32(UNIDADES) + unidade * PASSO_UNIDADE + 0x98) & 0xffffffff))
        unidade = proxima_unidade(m)
    de, para = s32(a[1]), s32(a[2])
    dx = abs(_mod(de, 0x100) - _mod(para, 0x100))
    dy = abs(_div(de, 0x100) - _div(para, 0x100))
    if lento == 0:
        raise DependenciaIA('I_DetermineTempsTrajet: a unit of speed 0 (#DE at idiv)', 0x482427)
    return _div(40 * max(dx, dy), lento) & 0xffffffff


def v_desloca_grupo(m, p, a, jogador, indice):
    """V_DeplaceGroupe 0x481f4c: SetDeplaceEngin(unit, destination) for every live unit not already walking."""
    unidade = primeira_unidade(m, a[0])
    while unidade != 0xffff:
        if _chamar(p, 'EnginEstVivant', 0x481f6d, unidade=unidade) & 0xff:
            r = (m.u32(UNIDADES) + unidade * PASSO_UNIDADE) & 0xffffffff
            if not (m.u8(r + 2) == 1 and m.u16(r + 0xb8) != 0xffff):
                _chamar(p, 'SetDeplaceEngin', 0x481fa8, unidade=unidade, destino=a[1] & 0xffff)
        unidade = proxima_unidade(m)
    return 1


REGRAS = {'B_TestGroupeVide': b_testa_grupo_vazio, 'B_NewConflit': b_novo_conflito,
          'B_AttenteConflit': b_espera_conflito, 'I_DetermineTempsTrajet': i_tempo_trajeto,
          'V_DeplaceGroupe': v_desloca_grupo}


def operacoes_regras(m, p):
    """Core ``MaquinaTarefas`` ``operacoes``: name -> f(vm, argumentos, jogador, indice)."""
    return {nome: (lambda vm, argumentos, jogador, indice, f=f: f(m, p, list(argumentos) + [0] * 7, jogador,
                                                                   indice))
            for nome, f in REGRAS.items()}


class MundoRegras:
    """``MaquinaTarefas``' unit-operation hook over the live memory.

    Core's VM sends V_DeplacerUnite, V_DeplaceGroupe, I_DonneTypeUnite, B_TestUniteFaitRien and
    I_AttenteMessageGroupe to ``mundo``. Core's ``ordens_unidades.MundoUnidades`` implements them over its
    own copied buffers. Here V_DeplaceGroupe runs this front's live-memory rule, and the others are named stops
    until they are reached and captured.
    """
    def __init__(self, m, p):
        self.m, self.p = m, p

    def executar_operacao(self, nome, argumentos):
        if nome == 'V_DeplaceGroupe':
            return v_desloca_grupo(self.m, self.p, list(argumentos) + [0] * 7, None, None)
        raise DependenciaIA(f'{nome} (iaSolver unit operation over the live memory)', 0x47d4ea)

    def aguardar_mensagem_grupo(self, maquina, tarefa, grupo, mascara):
        raise DependenciaIA('I_AttenteMessageGroupe (iaSolver unit operation over the live memory)', 0x47d4ea)
