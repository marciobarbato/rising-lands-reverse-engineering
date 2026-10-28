"""Inicialização local de unidade, reconstruída do EXE original.

EnginSetTypeCaract (0x457350) e EnginSetType (0x457b87). Não cria unidades
no mundo, não ocupa terreno e não consulta a economia. Modificadores e a
capacidade de tripulação são entradas explícitas, resolvidas pelo chamador.
As funções alteram o bytearray recebido, preservando campos não escritos no x86.
"""
from dataclasses import dataclass

from animacao_disparo import BuscaAtaque, guardar


@dataclass(frozen=True)
class CaracteristicasTipo:
    """Palavras já carregadas: +2a visão, +2c alcance², +30 recarga.

    Base original 0x4965ae, passo 50. Os inicializadores de tipo leem o byte
    baixo; a pós-carga de missão repõe a palavra inteira de recarga. Não
    repetir a leitura do INI nem quadrar novamente o alcance.
    """
    visao: int
    alcance_quadrado: int
    recarga: int


# Colunas: +93, +98, +a7, +a8, +a5, +a6, +db, +9d, +ac, +ad, +99.
# Transcrição dos 26 ramos de 0x457350; None significa PRESERVAR o byte.
_COLUNAS = (0x93, 0x98, 0xa7, 0xa8, 0xa5, 0xa6, 0xdb, 0x9d, 0xac, 0xad, 0x99)
_RAMOS = (
    (1, 2, 2, 2, 8, 10, 8, 255, 3, 3, 0),  # 0
    (1, 2, 2, 4, 8, 4, 8, 255, 3, 3, 0),
    (1, 3, 2, 3, 8, 10, 10, 255, 3, 3, 0),
    (1, 4, 2, 4, 8, 8, 8, 255, 3, 3, 0),
    (1, 1, 3, 2, 8, 10, 10, 255, 3, 3, 0),
    (1, 2, 2, 4, 8, 8, 8, 255, 3, 3, 0),
    (1, 3, 2, 4, 8, 8, 8, 255, 3, 3, 0),
    (1, 2, 2, 4, 8, 8, 8, 255, 3, 3, 0),
    (1, 2, 2, 2, 10, 10, 8, 255, 3, 3, 0),
    (1, 2, 2, 4, 8, 8, 8, 255, 3, 3, 0),
    (1, 3, 2, 4, 8, 8, 8, 255, 3, 3, 0),
    (1, 8, 1, 1, 3, 3, None, 100, 2, 10, 3),
    (2, 3, 2, 4, 3, 8, None, 100, 15, 20, 2),
    (3, 3, 3, 0, 3, 8, None, 100, 6, 10, 3),
    (4, 3, 3, 4, 3, 2, None, 100, 0, 3, 2),
    (3, 4, 2, 2, 3, 1, None, 100, 0, 3, 2),
    (2, 8, 2, 2, 8, 8, None, 48, 10, 8, 0),
    (2, 1, 4, 4, 3, 4, None, 100, 6, 10, 0),
    (1, 2, 1, 2, 10, 4, 8, 255, 3, 3, 0),
    (1, 2, 1, 2, 15, 15, 15, 255, 3, 3, 0),
    (1, 4, 2, 2, 8, 8, 8, 255, 3, 3, 0),
    (1, 8, 2, 2, 8, 8, 8, 255, 3, 3, 0),
    (1, 4, 2, 2, 8, 8, 8, 255, 3, 3, 0),
    (1, 2, 2, 2, 8, 8, 8, 255, 3, 3, 0),
    (3, 1, 3, 3, 8, 8, 8, 255, 3, 3, 0),
    (1, 4, 2, 4, 8, 8, 8, 255, 3, 3, 0),  # 25
)
PROJETIL_POR_TIPO = {1: 25, 2: 1, 3: 26, 8: 9, 11: 27, 12: 22,
                    15: 1, 18: 17, 21: 24, 22: 23, 23: 23, 25: 26}
QUADRO_POR_TIPO = {0: 6, 1: 1, 2: 7, 3: 4, 4: 5, 8: 6, 11: 1,
                  12: 0, 15: 0, 18: 2, 21: 6, 22: 6, 23: 5, 25: 1}


def caracterizar_tipo(u, recarga, modificador12):
    """0x457350, AX=índice: traduz todas as escritas do registro.

    modificador12 é um callable (dono, tipo) -> valor. Só é consultado para
    tipo 4; donos 4/200 retornam zero antes da consulta em Modificateur.
    +8a/+8b são sempre preservados. Tipo >25 executa apenas o prólogo comum.
    """
    tipo = u[1]
    u[0xbc], u[0xdb], u[0xda], u[0xf9] = 255, 8, 1, 0
    guardar(u, 0x102, recarga & 255)
    if tipo > 25:
        return
    for offset, valor in zip(_COLUNAS, _RAMOS[tipo]):
        if valor is not None:
            u[offset] = valor
    if tipo in PROJETIL_POR_TIPO:
        u[0x78], u[0x79] = 1, PROJETIL_POR_TIPO[tipo]
    elif tipo in (19, 20, 24):
        u[0x78] = 0
    if tipo in QUADRO_POR_TIPO and tipo != 4:
        u[0x7a] = QUADRO_POR_TIPO[tipo]
    if tipo == 4:
        mod = 0 if u[0] in (4, 200) else modificador12(u[0], tipo)
        # 0x457845 queries first; frame/amount are not written on failure.
        u[0x7a] = QUADRO_POR_TIPO[4]
        u[0xda] = (mod + 10) & 255
    elif tipo == 6:
        u[0xbb] = 5
    elif tipo in (16, 17):
        u[0xab] = 50
        if tipo == 17:
            u[0x94], u[0x95], u[0x96], u[0xa4] = 0, 1, 0, 0


def definir_tipo(u, indice, celula, direcao, tipo, caracteristicas,
                 capacidade_tipo, modificador, busca):
    """0x457b87: AX=índice, DX=célula, BL=direção, CL=tipo.

    capacidade_tipo(tipo) resolve EnginTypeGetCapacite; modificador(dono,
    tipo, id) resolve IDs 1 e 12. Mantêm-se externos à economia. `busca` é
    um BuscaAtaque local, não o objeto de navegação do chat principal.
    Esta rotina zera +8b, mas NÃO zera +8a, +79 ou +7a antecipadamente.
    """
    indice, tipo, direcao = indice & 65535, tipo & 255, direcao & 255
    for off in (8, 0x7c, 0x7e):
        guardar(u, off, celula)
    # No x86, a liberação usa XOR BH,BH; BL (direção) permanece intacto.
    busca.liberar(indice)
    for off in (0x88, 0xab, 0x97, 0x95, 0x96, 0x92, 0x86, 0x87,
                0xb6, 0xaa, 0xa4, 0xa9, 0x9e, 0x8e, 0x8b, 0xbc, 0xbd):
        u[off] = 0
    guardar(u, 0xb2, 65535)
    guardar(u, 0xb8, 65535)
    guardar(u, 0x8c, 0)
    u[0x9c], u[0x90], u[0x91], u[0x94], u[1] = 99, direcao, direcao, direcao, tipo
    if u[2] not in (0, 4):
        u[2] = 7
        busca.liberar(indice)
    guardar(u, 4, 4)
    guardar(u, 0x74, 0)
    guardar(u, 0x76, 4)
    guardar(u, 0xc2, 0)
    u[6], u[0x78] = 4, 0
    u[0xbb] = caracteristicas.visao & 255
    u[0xb0] = caracteristicas.alcance_quadrado & 255
    caracterizar_tipo(u, caracteristicas.recarga,
                      lambda dono, t: modificador(dono, t, 12))
    capacidade = capacidade_tipo(tipo)
    capacidade += 0 if u[0] in (4, 200) else modificador(u[0], tipo, 1)
    # Limpa a estrutura de carga local +0a..+71 (sem alterar saldo de jogador).
    for off in (0xa, 0xc, 0xe, 0x70):
        guardar(u, off, 0)
    for i in range(30):
        guardar(u, 0x10 + i * 2, 0)
        u[0x4c + i] = 0
    guardar(u, 0xc, capacidade)


def preparar_apos_carga_missao(u, caracteristicas, modificador12):
    """0x46ad8b..0x46b019: pós-leitura de UMA unidade no LoadEngin ETA.

    Não inclui o laço/I/O nem a escrita +bd=0 no slot ordinal em 0x46ad83.
    ExisteEngin aceita qualquer estado diferente de zero, inclusive 4.
    O carregador chama caracterizar_tipo e depois sobrescreve alguns valores.
    """
    if not u[2]:
        return
    caracterizar_tipo(u, caracteristicas.recarga, modificador12)
    guardar(u, 0x9a, 100)
    u[0xbb] = caracteristicas.visao & 255
    u[0xb0] = caracteristicas.alcance_quadrado & 255
    u[0xbc] = 255
    for off in (0xf5, 0xf6, 0xf7, 0xf8, 0xdc):
        u[off] = 0
    u[0x104:0x108] = u[0x10c:0x110] = b'\xff' * 4
    u[0x110:0x114] = bytes(4)
    if u[2] == 14:
        u[0x72] = 0
    guardar(u, 0x102, caracteristicas.recarga)  # agora palavra inteira
    if u[1] == 4:
        u[0xda] = 10  # sobrescreve o resultado que incluía modificador12
    elif u[1] in (14, 16):
        u[0xda] = 0
    if u[1] == 16:
        u[0] = 0
    elif 20 <= u[1] <= 24:
        u[0] = 4


def preparar_apos_carga_game(u):
    """0x46b08f..0x46b0e3: limpeza local após leitura de um save.

    Não chama EnginSetTypeCaract. Conserva os quatro campos investigados,
    incluindo fases 2/3 quando já estão presentes no registro serializado.
    """
    u[0xbd] = 0
    u[0x110:0x114] = bytes(4)
    u[0x104:0x108] = b'\xff' * 4


def pedido_leitura_registro(indice, tamanho=276):
    """Pedido de leitura: 0x479d47..60 usa 276; 0x46b06f..8a usa o cabeçalho.

    Retorna (offset relativo à tabela, tamanho), sem I/O nem validação extra
    de índice. Os originais aceitam u16 e não filtram +79/+7a/+8a/+8b ao ler.
    A bancada valida o pedido; não substitui nem emula FileRead/Windows.
    """
    return (indice & 65535) * 276, tamanho & 65535
