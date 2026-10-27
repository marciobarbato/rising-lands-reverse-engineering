"""Geometria inicial dos 22 tipos: tabelas e consultas Batiment* do EXE.

Dimensões de 0x495d8c/+2 com passo 52; máscaras referidas por 0x41ab5c.
Não interpreta os nomes nem os efeitos de construção/economia dos tipos.
"""
import struct

TAMANHOS_E_MASCARAS = (
    (3, 4, '110110000000'),
    (5, 6, '011101111111110000000000000000'),
    (6, 5, '011110111111111111000001000000'),
    (5, 5, '1110011100000000000000000'),
    (3, 4, '011111000000'),
    (6, 6, '111110111110111110000000000000000000'),
    (6, 5, '000100011110011111001100000000'),
    (4, 6, '111111111110000000000000'),
    (6, 6, '011110011110111111000000000000000000'),
    (1, 1, '1'),
    (2, 3, '111100'),
    (2, 3, '111100'),
    (1, 1, '1'),
    (4, 5, '11111111000000000000'),
    (4, 6, '011101110110000000000000'),
    (4, 5, '01110111011100100000'),
    (4, 5, '00001111111100000000'),
    (2, 2, '0100'),
    (4, 5, '11111111111100000000'),
    (3, 4, '111111000000'),
    (4, 5, '01110111011100100000'),
    (3, 4, '111111000000'),
)


def tamanho_estrutura(tipo):
    if not 0 <= tipo < 22:
        raise ValueError('Tipo de estrutura fora de 0..21')
    return TAMANHOS_E_MASCARAS[tipo][:2]


def colisao_estrutura(tipo, subcelula):
    """BatimentCollision, 0x41ab5c; domínio da máscara declarada pelo tipo."""
    if not 0 <= tipo < 22:
        return False
    mascara = TAMANHOS_E_MASCARAS[tipo][2]
    if not 0 <= subcelula < len(mascara):
        raise ValueError('Subcélula fora da máscara da estrutura')
    return mascara[subcelula] == '1'


def _dados(mundo, indice):
    if not 0 <= indice < 1000:
        raise ValueError('Índice de estrutura fora de 0..999')
    p = indice * 276
    origem = struct.unpack_from('<H', mundo.estruturas, p + 2)[0]
    tipo = mundo.estruturas[p + 8]
    return origem, tipo, tamanho_estrutura(tipo)


def celulas_estrutura(mundo, indice):
    """GetBatimentCaseList, 0x41a9c3: retângulo de baixo para cima, u16."""
    origem, _, (largura, altura) = _dados(mundo, indice)
    return tuple((origem + y * 256 + x) & 65535
                 for y in range(altura - 1, -1, -1) for x in range(largura))


def estrutura_ocupa_celula(mundo, indice, celula):
    """BatimentOccupeCase, 0x41aff8: só as posições com máscara não zero.

    A soma da posição é de 32 bits, ao contrário da lista serializada u16.
    """
    origem, tipo, (largura, altura) = _dados(mundo, indice)
    celula &= 65535
    for y in range(altura):
        for x in range(largura):
            if origem + y * 256 + x == celula and colisao_estrutura(tipo, y * largura + x):
                return True
    return False
