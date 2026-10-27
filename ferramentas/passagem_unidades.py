"""EnginOccupeCase e EnginPeutPasser: consultas locais reconstruídas do x86."""
QUADRUPLOS = frozenset((3, 11, 12, 13, 14, 15, 16, 25))
TIPOS_ATROPELAVEIS = frozenset((0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 18, 19, 22))


def ocupa_celula(mundo, indice, celula, mascara):
    p = indice * 276
    u = mundo.unidades
    if (u[p + 0xab] != 0 and mascara == 1) or (u[p + 0xab] == 0 and mascara == 2) or u[p + 2] == 14:
        return False
    bases = (mundo.palavra(indice, 8), mundo.palavra(indice, 0x7c))
    deltas = (0, 1, 257, 256) if u[p + 1] in QUADRUPLOS else (0,)
    # As subtrações deste predicado são de 32 bits, sem wrap u16.
    return celula in (base - d for base in bases for d in deltas)


def procurar_ocupante(mundo, celula):
    """ChercheIndiceEngin: primeiro modo não zero; senão último modo zero."""
    candidato = 0xffff
    u = mundo.unidades
    for i in range(800):
        p = i * 276
        if not mundo.viva(i) or not u[p + 0x72]:
            continue
        if not ocupa_celula(mundo, i, celula, 1 + int(u[p + 0xab] != 0)):
            continue
        if u[p + 1] == 16 and u[p + 0xab] != 50:
            continue
        candidato = i
        if u[p + 0xab]:
            return i
    return candidato


def consultar_passagem(mundo, indice, celula, mascara=None):
    """Retorna (permissão, quatro candidatos), sem aplicar atropelamento."""
    p = indice * 276
    tipo = mundo.unidades[p + 1]
    celula &= 65535
    if not 0 <= tipo < 26:
        raise ValueError('Tipo fora do domínio reconstruído')
    mascara = 1 + int(mundo.unidades[p + 0xab] != 0) if mascara is None else mascara & 255
    candidatos = [0xffff] * 4
    grande = tipo in QUADRUPLOS
    if grande and ((celula & 255) == 0 or (celula >> 8) == 0):
        return False, candidatos
    permitido, n = True, 0
    for d in ((0, 1, 257, 256) if grande else (0,)):
        c = (celula - d) & 65535
        if ocupa_celula(mundo, indice, c, mascara) or not mundo.atributos[c] & mascara:
            continue
        outro = procurar_ocupante(mundo, c)
        candidatos[n] = outro
        n += 1
        pode_atropelar = (tipo in (12, 15) and outro != 0xffff and
                          mundo.unidades[outro * 276] != mundo.unidades[p] and
                          mundo.unidades[outro * 276 + 1] in TIPOS_ATROPELAVEIS)
        if not pode_atropelar:
            permitido = False
    return permitido, candidatos
