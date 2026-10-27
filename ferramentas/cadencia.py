"""Contadores e seleção de desenho recuperados; não estabelece FPS fixo."""


def avancar_contadores(ciclo, metade, terco):
    """0x475014..0x475041: três contadores uint32, com overflow preservado."""
    ciclo = (ciclo + 1) & 0xffffffff
    metade = (metade + int(ciclo % 2 == 0)) & 0xffffffff
    terco = (terco + int(ciclo % 3 == 0)) & 0xffffffff
    return ciclo, metade, terco


def deve_desenhar(ciclo, divisor=1, forcar=False):
    """0x417909..0x41792b: divisor afeta desenho, após atualização do mundo."""
    if forcar:
        return True
    divisor &= 255
    if divisor == 0:
        raise ValueError('Divisor zero provocaria divisão por zero no original')
    return (ciclo & 0xffffffff) % divisor == 0


def proximo_aleatorio(estado, limite):
    """Caminho positivo de 0x489728: devolve (novo_estado, valor % limite).

    Estado no domínio 0..0x7fffffff. Não inclui semeadura por timeGetTime nem
    os argumentos não positivos do original. Zero degenera para 0x7fffffff.
    """
    if not 0 <= estado <= 0x7fffffff or not 1 <= limite <= 0x7fffffff:
        raise ValueError('Estado ou limite fora do domínio reconstruído')
    quociente, resto = divmod(estado, 127773)
    novo = resto * 16807 - quociente * 2836
    if novo <= 0:
        novo += 0x7fffffff
    return novo, novo % limite
