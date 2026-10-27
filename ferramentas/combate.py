"""Aritmética parcial de 0x4502f0. Sem alvos, projéteis ou efeitos de morte.

Os parâmetros de modificadores são valores já resolvidos pelo chamador. Esta
implementação não supõe que BLINDAGE do INI seja subtraído diretamente da matriz.
"""


def inteiro_com_sinal8(valor):
    valor &= 255
    return valor - 256 if valor >= 128 else valor


def dano_bruto_unidade(matriz, bonus_f7=0, modificador5=0, bonus_proximidade=0):
    """Modo 1 em 0x4503b8..0x45043f, condicionando o bônus à consulta externa.

    bonus_proximidade deve ser zero quando 0x4500e4 retorna falso. Seu nome
    não afirma que a consulta filtre capitães; essa condição merece investigação.
    """
    return (matriz + bonus_f7 + modificador5 + bonus_proximidade) & 255


def reduzir_dano(dano_bruto, reducao_f6=0, modificador6=0):
    """0x45059c..0x4505d8: byte negativo vira 1; zero permanece zero."""
    resultado = (dano_bruto - reducao_f6 - modificador6) & 255
    return 1 if inteiro_com_sinal8(resultado) < 0 else resultado


def aplicar_dano_parcial(vida, dano_reduzido, protecao_bit3=False):
    """0x450644..0x4506a1, sem executar o ramo de morte.

    A proteção subtrai um DEPOIS do limite anterior, também em 8 bits. Dano
    zero protegido vira -1: a subtração aumenta a vida em um, sem clamp aqui.
    Retorna a vida aritmética e se o código entra no ramo que trata a morte.
    """
    dano = inteiro_com_sinal8(dano_reduzido - int(bool(protecao_bit3)))
    vida &= 65535
    entra_no_ramo_morte = vida <= dano
    return dict(vida=0 if entra_no_ramo_morte else (vida - dano) & 65535,
                dano_com_sinal=dano, entra_no_ramo_morte=entra_no_ramo_morte)
