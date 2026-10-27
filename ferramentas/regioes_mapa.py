"""Chemin_Remap: componentes naturais, com quatro/oito vizinhos diferentes."""


def obstaculo_natural(tile, objeto, marcadores_tiles):
    return (tile < 702 and marcadores_tiles[tile] != 0) or 1 <= objeto <= 11


def classificar_terreno(atributos, tiles, objetos, marcadores_tiles):
    return bytearray((atributos[i] & 1) if obstaculo_natural(tiles[i], objetos[i], marcadores_tiles) else 0 for i in range(65536))


def preencher_componente(classes, regioes, inicio, rotulo):
    classe = classes[inicio]
    pilha = [inicio]
    while pilha:
        c = pilha.pop()
        if classes[c] != classe or regioes[c] != 0:
            continue
        regioes[c] = rotulo & 65535
        x, y = c & 255, c >> 8
        if x: pilha.append(c - 1)
        if x < 255: pilha.append(c + 1)
        if y < 255: pilha.append(c + 256)
        if y: pilha.append(c - 256)
        if classe == 0:
            if x and y: pilha.append(c - 257)
            if x and y < 255: pilha.append(c + 255)
            if x < 255 and y: pilha.append(c - 255)
            if x < 255 and y < 255: pilha.append(c + 257)


def reconstruir_regioes(atributos, tiles, objetos, marcadores_tiles, largura, altura):
    classes = classificar_terreno(atributos, tiles, objetos, marcadores_tiles)
    regioes, quantidade = [0] * 65536, 0
    for c in range(65536):
        if regioes[c] == 0:
            quantidade += 1
            preencher_componente(classes, regioes, c, quantidade)
    if quantidade >= 0x4000:
        raise ValueError('Chemin_Remap excederia o limite de rótulos <0x4000')
    novos_atributos = bytearray(atributos)
    for y in range(256):
        for x in range(largura if y < altura else 0, 256):
            c = y * 256 + x
            regioes[c] = 0
            novos_atributos[c] = 1
    return regioes, novos_atributos, quantidade
