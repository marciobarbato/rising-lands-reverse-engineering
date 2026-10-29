"""The unit and structure dispatcher loops, IATestUtilite and its unit-message test.

Reconstructed from the intact bytes for the branches the MONDE01 M1 post-load
state reaches (captures ``evidencias/captura-quadro-m2-pos-carga.json``):

- ``calcular_proxima_etapa_unidades``: CalculEnginNextEtape 0x456db5;
- ``calcular_proxima_etapa_estruturas``: CalculBatimentNextEtape 0x4281c7;
- ``testar_utilidade``: IATestUtilite 0x47fbfd;
- ``testar_mensagem_unidade``: iagMessTestSendMessageEngin 0x483ed7.

They run over an explicit ``MemoriaDeclarada``. Per-unit and per-structure
bodies (EnginNextEtape, BatimentNextEtape) and every other callee come from
original-name providers, which receive ``sitio`` and the original register
widths. A missing provider raises ``DependenciaIA`` at its call site, and every
earlier store is retained. iagMessTestSendMessageEngin's group-descriptor path
(an AI-owned unit with a group, 0x483f5d onward) is not reconstructed yet; it
raises ``DependenciaIA`` at 0x483f5d.
"""
from reinicio_ia import DependenciaIA

PONTEIRO_UNIDADES, UNIDADES, PASSO = 0x4e19a0, 800, 276
ESTRUTURAS, QUANTIDADE_ESTRUTURAS = 0x49a0c8, 1000
REGIOES_DESPACHO = (
    (0x495c02, 0x495c04, 'structure period'),
    (0x49a0c8, 0x49a0c8 + QUANTIDADE_ESTRUTURAS * PASSO, 'structure pool'),
    (0x4dfaa8, 0x4dfab8, 'structure counters per owner'),
    (0x4dfb50, 0x4dfb51, 'structure loop flag'),
    (0x4dfb9b, 0x4dfb9c, 'structure period flag'),
    (0x4e1928, 0x4e1932, 'unit counters per owner and owner 4'),
    (0x4e19a0, 0x4e19a4, 'unit pool pointer'),
    (0x4e1a38, 0x4e1a3c, 'unit counters other/local'),
    (0x4e1a3c, 0x4e1a3c + 4 * 0x34, 'unit counters per owner and type'),
    (0x508041, 0x508042, 'local player'),
    (0x508f7c, 0x508f80, 'frame counter'),
)


def _chamar(provedores, rotina, sitio, **argumentos):
    provedor = provedores.get(rotina)
    if provedor is None:
        raise DependenciaIA(rotina, sitio)
    return provedor(sitio=sitio, **argumentos)


def testar_mensagem_unidade(memoria, provedores, unidade):
    """iagMessTestSendMessageEngin 0x483ed7 (eax = u16 unit)."""
    m = memoria
    registro = (m.u32(PONTEIRO_UNIDADES) + (unidade & 0xffff) * PASSO) & 0xffffffff
    if m.u8(registro + 2) == m.u8(registro + 0x10a) and m.u8(registro + 0x89) == m.u8(registro + 0x10b):
        return
    m.u8(registro + 0x10a, m.u8(registro + 2))
    m.u8(registro + 0x10b, m.u8(registro + 0x89))
    dono = m.u8(registro)
    if dono >= 4:
        return
    if _chamar(provedores, 'PlayerGetType', 0x483f3b, jogador=dono) & 0xff != 2:
        return
    if m.u32(registro + 0x10c) == 0xffffffff:
        return
    raise DependenciaIA('iagMessTestSendMessageEngin group-descriptor path', 0x483f5d)


def testar_utilidade(memoria, provedores, tipo, indice):
    """IATestUtilite 0x47fbfd: only eax = 1 tests the unit; iabTestEngin 0x4897a4 is a ret."""
    if tipo & 0xff == 1:
        testar_mensagem_unidade(memoria, provedores, indice & 0xffff)


def calcular_proxima_etapa_unidades(memoria, provedores):
    """CalculEnginNextEtape 0x456db5."""
    m = memoria
    m.u16(0x4e1a38, 0)
    m.u16(0x4e1a3a, 0)
    for dono in range(4):
        for tipo in range(26):
            m.u16(0x4e1a3c + dono * 0x34 + tipo * 2, 0)
        m.u16(0x4e1928 + dono * 2, 0)
    m.u16(0x4e1930, 0)
    for indice in range(UNIDADES):
        registro = (m.u32(PONTEIRO_UNIDADES) + indice * PASSO) & 0xffffffff
        estado = m.u8(registro + 2)
        if not estado:
            continue
        if estado != 4:
            dono, tipo = m.u8(registro), m.u8(registro + 1)
            if dono not in (200, 4):
                endereco = 0x4e1a3c + dono * 0x34 + tipo * 2
                m.u16(endereco, m.u16(endereco) + 1)
            testar_utilidade(m, provedores, 1, indice)
            if tipo != 17:
                contador = 0x4e1a3a if dono == m.u8(0x508041) else 0x4e1a38
                m.u16(contador, m.u16(contador) + 1)
            if dono != 200 and tipo != 5:
                m.u16(0x4e1928 + dono * 2, m.u16(0x4e1928 + dono * 2) + 1)
        _chamar(provedores, 'EnginNextEtape', 0x456ead, unidade=indice)


def calcular_proxima_etapa_estruturas(memoria, provedores):
    """CalculBatimentNextEtape 0x4281c7."""
    m = memoria
    _chamar(provedores, 'ResetTableauHangar', 0x4281d0)
    periodo = m.u16(0x495c02)
    if periodo == 0:
        raise ZeroDivisionError('div by u16 0x495c02 = 0 at 0x4281e5 faults in the original')
    if m.u32(0x508f7c) % periodo == 0:
        m.u8(0x4dfb9b, 0)
    for dono in range(4):
        m.u32(0x4dfaa8 + 4 * dono, 0)
    for indice in range(QUANTIDADE_ESTRUTURAS):
        registro = ESTRUTURAS + indice * PASSO
        if not m.u8(registro + 5):
            continue
        dono, tipo = m.u8(registro + 4), m.u8(registro + 8)
        if dono < 4 and tipo not in (9, 12, 17):
            m.u32(0x4dfaa8 + 4 * dono, m.u32(0x4dfaa8 + 4 * dono) + 1)
        if m.u8(registro + 5) == 3:
            _chamar(provedores, 'DemonteBatiment', 0x4282bb, estrutura=indice)
            continue
        testar_utilidade(m, provedores, 3, indice)
        _chamar(provedores, 'BatimentNextEtape', 0x4282da, estrutura=indice)
        caso = _chamar(provedores, 'BatimentGetCase', 0x4282e1, estrutura=indice) & 0xffffffff
        for jogador in range(4):
            if m.u8(registro + 4) == jogador:
                continue
            if _chamar(provedores, 'CaseEstDecouverte', 0x42832b, caso=caso & 0xffff, jogador=jogador) & 0xff:
                continue
            if not _chamar(provedores, 'BatimentEstDecouvert', 0x428338, estrutura=indice, jogador=jogador) & 0xff:
                continue
            _chamar(provedores, 'BatimentDecouvre', 0x428345, estrutura=indice, jogador=jogador)
        for jogador in range(4):
            if m.u8(registro + 4) == jogador:
                continue
            bandeira = registro + 0x110 + jogador
            if _chamar(provedores, 'BatimentContourEstIllumine', 0x4283ac, estrutura=indice,
                       jogador=jogador) & 0xff:
                if not m.u8(bandeira):
                    _chamar(provedores, 'BatimentIllumine', 0x4283c7, estrutura=indice, jogador=jogador, ebx=1)
                    m.u8(bandeira, 1)
            elif m.u8(bandeira):
                _chamar(provedores, 'BatimentIllumine', 0x428363, estrutura=indice, jogador=jogador, ebx=0)
                m.u8(bandeira, 0)
    m.u8(0x4dfb50, 0)
