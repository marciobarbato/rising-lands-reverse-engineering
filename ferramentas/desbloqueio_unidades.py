"""EnginChercheCaseLibre e EnginDebloqueNextCase, sem execução do EXE."""
from movimento import celula_vizinha, direcao_entre_celulas
from passagem_unidades import consultar_passagem, procurar_ocupante


def procurar_celula_livre(mundo, centro, indice):
    """0x44330c: oito posições de uma janela 3×3, em ordem de leitura.

    O canto superior esquerdo é limitado a zero; o índice central (4) é
    sempre omitido. Não aumenta a janela para unidades de quatro células.
    """
    indice = mundo._indice(indice)
    centro &= 65535
    x, y = max(0, (centro & 255) - 1), max(0, (centro >> 8) - 1)
    for j in range(9):
        cx, cy = x + j % 3, y + j // 3
        if j != 4 and cx < mundo.largura and cy < mundo.altura:
            celula = cx + cy * 256
            if consultar_passagem(mundo, indice, celula)[0]:
                return celula
    return 0xffff


def afastar_bloqueadores(mundo, indice):
    """0x449176: tenta d, d−2, d e emite SetDeplaceEngin para o mesmo dono.

    Retorno verdadeiro significa que encontrou um bloqueador elegível, mesmo
    sem célula livre. Os dois globais de consulta conservam o último valor.
    """
    indice = mundo._indice(indice)
    p = indice * 276
    d = direcao_entre_celulas(mundo.palavra(indice, 8), mundo.palavra(indice, 0x7e))
    encontrou = False
    for tentativa in range(3):
        celula = celula_vizinha(mundo.palavra(indice, 8), d, mundo.largura, mundo.altura)
        if celula != 0xffff:
            outro = procurar_ocupante(mundo, celula)
            mundo.ultimo_bloqueador = outro
            if (outro != 0xffff and mundo.unidades[outro * 276] == mundo.unidades[p] and
                    mundo.palavra(outro, 8) == mundo.palavra(outro, 0x7e)):
                livre = procurar_celula_livre(mundo, celula, outro)
                mundo.ultima_celula_livre = livre
                if livre != 0xffff:
                    mundo.definir_movimento(outro, livre)
                encontrou = True
        for _ in range(2):
            d = (16 if d == 1 else (d - 1) & 255) if tentativa == 0 else d % 16 + 1
    mundo.unidades[p + 0x8b], mundo.unidades[p + 0x88] = 0, 1
    return dict(desbloqueou=encontrou)
