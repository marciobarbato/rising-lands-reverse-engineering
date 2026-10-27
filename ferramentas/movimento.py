"""Primitivas recuperadas do movimento; não implementa IA, colisão ou relógio."""

# Direções de deslocamento são ímpares. Orientação visual também usa as pares.
VETORES = {1: (-1, 0), 3: (-1, -1), 5: (0, -1), 7: (1, -1),
           9: (1, 0), 11: (1, 1), 13: (0, 1), 15: (-1, 1)}

# Despacho 0x4572e8, inicializador 0x457350. Tuplas na ordem dos IDs 0..25:
# incremento 0x98, período de giro 0x93, quadros 0xa5, período de animação 0xa7.
PARAMETROS_TIPOS = (
    (2, 1, 8, 2), (2, 1, 8, 2), (3, 1, 8, 2), (4, 1, 8, 2),
    (1, 1, 8, 3), (2, 1, 8, 2), (3, 1, 8, 2), (2, 1, 8, 2),
    (2, 1, 10, 2), (2, 1, 8, 2), (3, 1, 8, 2), (8, 1, 3, 1),
    (3, 2, 3, 2), (3, 3, 3, 3), (3, 4, 3, 3), (4, 3, 3, 2),
    (8, 2, 8, 2), (1, 2, 3, 4), (2, 1, 10, 1), (2, 1, 15, 1),
    (4, 1, 8, 2), (8, 1, 8, 2), (4, 1, 8, 2), (2, 1, 8, 2),
    (1, 3, 8, 3), (4, 1, 8, 2),
)


def parametros_tipo(tipo):
    if not 0 <= tipo < 26:
        raise ValueError('Tipo fora da tabela original')
    nomes = ('incremento_passo', 'periodo_giro', 'quadros_movimento', 'periodo_animacao')
    return dict(zip(nomes, PARAMETROS_TIPOS[tipo]))


def direcao_entre_celulas(origem, destino):
    """0x477042: só os sinais das diferenças; 0 quando as células coincidem."""
    dx = (destino & 255) - (origem & 255)
    dy = ((destino & 65535) >> 8) - ((origem & 65535) >> 8)
    vetor = ((dx > 0) - (dx < 0), (dy > 0) - (dy < 0))
    return next((direcao for direcao, v in VETORES.items() if v == vetor), 0)


def celula_vizinha(celula, direcao, largura, altura):
    """0x4770ee no domínio de células válidas. 0xffff indica borda bloqueada.

    Direções sem vetor (incluindo pares) devolvem a célula sem alteração.
    Não consulta obstáculos ou ocupação; a rotina original também não o faz.
    """
    x, y = celula & 255, (celula & 65535) >> 8
    if not (1 <= largura <= 256 and 1 <= altura <= 256 and
            0 <= celula <= 65535 and x < largura and y < altura):
        raise ValueError('Célula fora do domínio jogável')
    dx, dy = VETORES.get(direcao & 255, (0, 0))
    x, y = x + dx, y + dy
    return y * 256 + x if 0 <= x < largura and 0 <= y < altura else 65535


def distancia_quadratica(x1, y1, x2, y2):
    """0x479555: argumentos uint16, resultado em EAX com overflow de 32 bits."""
    dx, dy = (x1 & 65535) - (x2 & 65535), (y1 & 65535) - (y2 & 65535)
    return (dx * dx + dy * dy) & 0xffffffff


def atualizar_orientacao(desejada, atual, contador, periodo):
    """Campos 0x90..0x93 em 0x448599; empate de meia volta gira para baixo.

    Devolve (orientação atual, contador). O campo auxiliar 0xda dos tipos 12 e
    15 não está incluído nesta primitiva. Período 0 espera o contador dar a volta.
    """
    if not (1 <= desejada <= 16 and 1 <= atual <= 16):
        raise ValueError('Orientações devem estar entre 1 e 16')
    contador, periodo = contador & 255, periodo & 255
    if desejada == atual:
        return atual, contador
    contador = (contador + 1) & 255
    if contador != periodo:
        return atual, contador
    if (desejada - atual) % 16 < 8:
        atual = atual % 16 + 1
    else:
        atual = 16 if atual == 1 else atual - 1
    return atual, 0


def pode_avancar(desejada, atual):
    """0x4490fd..0x44915d: diferença de até duas posições no círculo de 16."""
    if not (1 <= desejada <= 16 and 1 <= atual <= 16):
        raise ValueError('Orientações devem estar entre 1 e 16')
    return (atual - desejada) % 16 in (0, 1, 2, 14, 15)


def integrar_prefixo_passo(dx, dy, progresso, direcao, incremento, desconto=0):
    """0x448704..0x4488a8, antes dos efeitos de chegada à célula.

    Conserva os bytes de deslocamento e progresso, incluindo overflow. Quando
    chegou=True, o restante da rotina zera deslocamentos/progresso, transfere a
    célula e atualiza ocupação/visão. Esses efeitos não estão implementados aqui.
    """
    passo = (incremento - desconto) & 255
    vx, vy = VETORES.get(direcao & 255, (0, 0))
    dx, dy = (dx + vx * passo) & 255, (dy + vy * passo) & 255
    progresso = (progresso + passo) & 255
    return dict(deslocamento_x_u8=dx, deslocamento_y_u8=dy,
                progresso=progresso, chegou=progresso > 31)
