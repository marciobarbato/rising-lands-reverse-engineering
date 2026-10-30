"""EnginNextEtape 0x45442c (prelude and state switch) and BatimentNextEtape 0x4268d4 (type switch).

Translated after the original entry/return captures of all 32 EnginNextEtape
calls at the exact MONDE01 frame-0/1 inputs (``evidencias/captura-entradas-
quadro1-ia-v2.json``). The executed basic blocks recorded there are followed
exactly. Every conditional branch they did not take raises
``DependenciaIA(description, original address)`` before its first effect. The
leaves and branch bodies are other owners' committed routines, called through
original-name providers (``provider(sitio=..., **arguments)``):
- Economy: BonusGetValEngin, the state-7 body, the type-2 structure branch.
- Core: GetBit, CalculFatigue, SetEnginCollision.
- Combat: EnginTrouveCible.

State 2 (moving) follows ``evidencias/captura-proxima-etapa-incursao-ia.json`` (the raid unit at counters
9000..9011, forced input) and ``captura-proxima-etapa-chegada-ia.json`` (counters 10523..10531, around its
arrival). Short of its target it calls DeplaceEngin (Core); at the target, EnginEnArret (Core) and state 7. The 32-frame target scan
(0x4546aa..0x4547e0) is translated from the static disassembly: the type
classifier, the owner-200 skip, the states 1/19 skip, the +0xda gate for entry types 14 and 16, and the
hit handling (iagUnitSendMessage 0x49 for player type 2, SetAttaqueEngin(1) for state 7). The capture
took only its no-scan path; frame 17 of the display reference is the first scan (Core's survey).
"""
from reinicio_ia import DependenciaIA

PONTEIRO_UNIDADES, PASSO = 0x4e19a0, 276
TABELA_FADIGA = 0x454344          # 26 targets: 0x454851 = fatigue branch taken
TABELA_ESTADOS = 0x4543c8         # 25 targets
TABELA_TIPOS_ESTRUTURA = 0x426880  # 21 targets
FADIGA, SAIDA = 0x454851, 0x454ccd
# 0x4546d5..0x454711: unit types whose 32-frame step scans for a target (AL = 1).
TIPOS_VARREDURA = frozenset({0, 1, 2, 3, 8, 0xb, 0xc, 0xf, 0x10, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19})
ESTADO_PARADO, RAMO_PRODUCAO = 0x456966, 0x426918
ESTADO_MOVENDO = 0x4563da          # state 2 (moving), the raid unit from counter 9000
ESTADO_ATAQUE = 0x456886           # states 1/24; Combat's published void body


def _parar(descricao, endereco):
    raise DependenciaIA(descricao, endereco)


def _chamar(provedores, rotina, sitio, **argumentos):
    provedor = provedores.get(rotina)
    if provedor is None:
        raise DependenciaIA(rotina, sitio)
    return provedor(sitio=sitio, **argumentos)


def proxima_etapa_unidade(m, provedores, unidade, tabelas):
    """EnginNextEtape 0x45442c (EAX = u16 unit). ``tabelas`` holds the image jump tables."""
    unidade &= 0xffff
    registro = lambda: (m.u32(PONTEIRO_UNIDADES) + unidade * PASSO) & 0xffffffff  # noqa: E731
    r = registro()
    if m.u8(r + 2):
        dono, tipo = m.u8(r), m.u8(r + 1)
        if m.u32(r + 0x104) != 0xffffffff:
            _parar('EnginNextEtape sound handle', 0x454479)
        m.u8(r + 0xf9, 0)
    else:
        dono = tipo = None
    estado = m.u8(registro() + 2)
    if estado in (0, 4):
        return _trocar_estado(m, provedores, unidade, r, tabelas)
    if m.u8(r + 1) == 0x10:
        _parar('EnginNextEtape type-16 animation', 0x4544d7)
    rr = registro()
    tipo_atual = m.u8(rr + 1)
    limite = m.u16(0x4965de + 50 * tipo_atual)
    bonus = _chamar(provedores, 'BonusGetValEngin', 0x45456e, jogador=m.u8(rr), tipo=tipo_atual, seletor=3,
                    ecx=rr) & 0xffff
    from combate import avancar_recarga
    atual = m.u16(rr + 0x102)
    seguinte = avancar_recarga(atual, limite, bonus)
    if seguinte != atual:
        m.u16(rr + 0x102, seguinte)
    if tipo >= 0x10:
        _parar('EnginNextEtape type >= 0x10 gate', 0x45459a)
    if 0 <= (tipo - 0xb) & 0xff <= 5:
        _parar('EnginNextEtape types 11..16', 0x4545b9)
    if tipo == 0x10:
        _parar('EnginNextEtape type 16', 0x4545fe)
    if m.u8(r + 2) != 0xe and (m.u32(0x508f7c) + unidade) & 0x1f == 0:
        # 0x4546aa: owner 200 skips the scan; 0x4546d5..0x454711 classify the current type.
        if dono != 0xc8 and m.u8(registro() + 1) in TIPOS_VARREDURA:
            tipo_jogador = _chamar(provedores, 'PlayerGetType', 0x454721, jogador=dono) & 0xff
            if m.u8(r + 2) not in (1, 0x13):
                # 0x454746..0x454792: entry types 14 and 16 scan only when +0xda is set.
                if tipo not in (0xe, 0x10) or m.u8(registro() + 0xda):
                    alvo = _chamar(provedores, 'EnginTrouveCible', 0x45479d, unidade=unidade) & 0xffff
                    if alvo != 0xffff:
                        if tipo_jogador == 2:
                            _chamar(provedores, 'iagUnitSendMessage', 0x4547bf, unidade=unidade, mensagem=0x49,
                                    alvo=alvo)
                        elif m.u8(r + 2) == 7:
                            _chamar(provedores, 'SetAttaqueEngin', 0x4547db, unidade=unidade, edx=1)
    if _chamar(provedores, 'GetBit', 0x454808, valor=m.u8(registro() + 0xdc), bit=2) & 0xff:
        _parar('EnginNextEtape spell timer', 0x454811)
    tipo_r = m.u8(r + 1)
    if tipo_r > 0x19:
        _parar('EnginNextEtape type > 25 fatigue gate', 0x454869)
    alvo_fadiga = tabelas['fadiga'][tipo_r]
    if alvo_fadiga != FADIGA:
        _parar(f'EnginNextEtape fatigue table type {tipo_r}', alvo_fadiga)
    if not _chamar(provedores, 'GetBit', 0x45489d, valor=m.u8(registro() + 0xdc), bit=2) & 0xff:
        _chamar(provedores, 'CalculFatigue', 0x4548ac, unidade=unidade)
        if m.u8(registro() + 2) in (0, 4):
            return SAIDA
        if m.u16(r + 4) != 4:
            # 0x4548e3 (captura-proxima-etapa-fadiga-ia.json, counters 10879..10882): a unit in a state other than
            # 0/4 with +0x72 set and no provisions left (+4 == 0) and both +0x86/+0x87 clear is told it starves:
            # AI type 2 -> iagUnitSendMessage(0x4b), else EnginSetFatigue. Then the normal path at 0x454994.
            rr = registro()
            if m.u8(rr + 2) not in (0, 4) and m.u8(rr + 0x72) and m.u16(rr + 4) == 0 \
                    and not m.u8(r + 0x86) and not m.u8(r + 0x87):
                if _chamar(provedores, 'PlayerGetType', 0x45496e, jogador=m.u8(rr)) & 0xff == 2:
                    _chamar(provedores, 'iagUnitSendMessage', 0x454986, unidade=unidade, mensagem=0x4b, alvo=0)
                else:
                    _chamar(provedores, 'EnginSetFatigue', 0x45498f, unidade=unidade)
    if m.u8(registro() + 1) == 0x11:
        _parar('EnginNextEtape type 17', 0x4549c2)
    rr = registro()
    if m.u8(rr + 0x72) and m.u8(r + 2) != 4:
        _chamar(provedores, 'SetEnginCollision', 0x454b6d, unidade=unidade, caso=m.u16(r + 8))
    rr = registro()
    if _chamar(provedores, 'GetBit', 0x454b9c, valor=m.u8(rr + 0xdc), bit=1) & 0xff:
        _parar('EnginNextEtape bit 1', 0x454ba5)
    if _chamar(provedores, 'GetBit', 0x454c05, valor=m.u8(m.u32(PONTEIRO_UNIDADES) + unidade * PASSO + 0xdc),
               bit=3) & 0xff:
        _parar('EnginNextEtape bit 3', 0x454c0e)
    if m.u8(registro() + 1) >= 0xc:
        _parar('EnginNextEtape type >= 12 tail', 0x454c70)
    return _trocar_estado(m, provedores, unidade, r, tabelas)


def _trocar_estado(m, provedores, unidade, r, tabelas):
    """State switch 0x456c1c: byte +2 of the record ESI computed at entry."""
    estado = m.u8(r + 2)
    if estado > 0x18:
        return SAIDA
    alvo = tabelas['estados'][estado]
    if alvo == SAIDA:
        return SAIDA
    if alvo == ESTADO_PARADO:
        _chamar(provedores, 'EnginNextEtape:state7', ESTADO_PARADO, unidade=unidade)
        return SAIDA
    if alvo == ESTADO_ATAQUE:
        _chamar(provedores, 'EnginNextEtape:state1', ESTADO_ATAQUE, unidade=unidade)
        return SAIDA
    if alvo == ESTADO_MOVENDO:
        # 0x4563da: still short of the target cell +0x7e -> 0x4555a7 DeplaceEngin(AX = unit), exit.
        if m.u16(r + 0x7e) != m.u16(r + 8):
            _chamar(provedores, 'DeplaceEngin', 0x4555ac, unidade=unidade)
            return SAIDA
        # 0x4563e8: at the target cell. Facing +0x91 == +0x90, EnginEnArret != 0 -> 0x456447: a state other
        # than 0 and 4 becomes 7 (0x4564b7); the path-search unit [0x496304] has a further reset.
        if m.u8(r + 0x91) != m.u8(r + 0x90):
            _parar('EnginNextEtape state 2 facing change at the target cell', 0x455a6f)
        if not _chamar(provedores, 'EnginEnArret', 0x4563ff, unidade=unidade) & 0xff:
            _parar('EnginNextEtape state 2 animation step (EnginEnArret returned 0)', 0x456408)
        if m.u8(r + 2) not in (0, 4):
            m.u8(r + 2, 7)
            if unidade == m.u16(0x496304):
                _parar('EnginNextEtape arrival of the path-search unit [0x496304]', 0x4564c8)
        return SAIDA
    _parar(f'EnginNextEtape state {estado}', alvo)


def proxima_etapa_estrutura(m, provedores, estrutura, tabelas):
    """BatimentNextEtape 0x4268d4 (EAX = u16 structure): type switch through 0x426880."""
    estrutura &= 0xffff
    tipo = m.u8(0x49a0c8 + estrutura * PASSO + 8)
    indice = (tipo - 1) & 0xff
    if indice > 0x14:
        return
    alvo = tabelas['tipos_estrutura'][indice]
    if alvo == RAMO_PRODUCAO:
        _chamar(provedores, 'BatimentNextEtape:production', RAMO_PRODUCAO, estrutura=estrutura)
        return
    _parar(f'BatimentNextEtape type {tipo}', alvo)


def tabelas_imagem(imagem):
    return dict(fadiga=imagem.table(TABELA_FADIGA, 26), estados=imagem.table(TABELA_ESTADOS, 25),
                tipos_estrutura=imagem.table(TABELA_TIPOS_ESTRUTURA, 21))
