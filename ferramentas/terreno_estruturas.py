"""Aplicação e limpeza do terreno de edifícios, traduzidas do x86 original.

Rotinas BatimentModifyTerrain, ResetBatimentTerrainModify e
ResetCheminTerrainModify. Não executa economia, criação ou demolição completa.
"""
import struct
from pegadas_estruturas import TAMANHOS_E_MASCARAS, tamanho_estrutura


def _dados(mundo, indice):
    indice &= 65535
    if indice >= 1000:
        raise ValueError('Índice de estrutura fora de 0..999')
    p = indice * 276
    tipo = mundo.estruturas[p + 8]
    largura, altura = tamanho_estrutura(tipo)
    return indice, p, largura, altura, TAMANHOS_E_MASCARAS[tipo][2], tipo


def aplicar_terreno_estrutura(mundo, indice, origem, primeiro_tile, mascara_tipo20=None):
    """BatimentModifyTerrain, 0x41ba49: tiles, colisão, regiões e objetos.

    Origem e primeiro tile vêm do chamador; não atualiza a origem no registro.
    Os slots de regiões salvas são compactos: só contam células com colisão.
    Uma inserção recusada por sobreposição também consome o número do slot.
    """
    indice, _, largura, altura, mascara, tipo = _dados(mundo, indice)
    mascara = bytes(int(v) for v in mascara)
    if tipo == 20:
        # A tabela de aplicação aponta para RAM mutável, 0x4dfb9c, enquanto
        # BatimentCollision usa a máscara estática do tipo 15. Não confundir.
        if mascara_tipo20 is None:
            raise NotImplementedError('Tipo 20 exige os 20 bytes da máscara de terreno em 0x4dfb9c')
        mascara = bytes(mascara_tipo20)
        if len(mascara) != largura * altura:
            raise ValueError('A máscara de terreno do tipo 20 deve ter 20 bytes')
    origem, primeiro_tile = origem & 65535, primeiro_tile & 65535
    slot = 0
    for linha in range(altura):
        for coluna in range(largura):
            sub = linha * largura + coluna
            celula = (origem + linha * 256 + coluna) & 65535
            mundo.tiles[celula] = (primeiro_tile + sub) & 65535
            if mascara[sub]:
                mundo.atributos[celula] |= 1
                mundo.modificar_regiao_estrutura(indice, slot, celula, True)
                slot += 1
            mundo.objetos[celula] = 0


def resetar_terreno_estrutura(mundo, indice, modo):
    """ResetBatimentTerrainModify, 0x41b888; dois efeitos separados.

    Modo u8 não zero limpa apenas o bit 0 nas células com colisão. Modo zero
    troca os tiles do retângulo pelo padrão de chão, sem liberar a colisão.
    Nenhum dos modos remove os rótulos, limpa objetos ou devolve tiles antigos.
    """
    _, p, largura, altura, mascara, _ = _dados(mundo, indice)
    origem = struct.unpack_from('<H', mundo.estruturas, p + 2)[0]
    x, y = origem & 255, origem >> 8
    for linha in range(altura):
        for coluna in range(largura):
            sub = linha * largura + coluna
            celula = (origem + linha * 256 + coluna) & 65535
            if modo & 255:
                if mascara[sub] == '1':
                    mundo.atributos[celula] &= 254
            else:
                # ESI continua crescendo entre linhas no original. Não
                # substituir por (x+coluna)%8: mudaria o padrão do piso.
                mundo.tiles[celula] = 0x15d + (x + sub) % 8 + ((y + linha) % 8) * 8


def remover_regioes_estrutura(mundo, indice):
    """ResetCheminTerrainModify, 0x41b78f: restaura regiões e divide cores.

    Não libera atributos físicos nem apaga a estrutura. Usa a origem armazenada,
    a máscara do tipo e a mesma numeração compacta da aplicação.
    """
    indice, p, largura, altura, mascara, _ = _dados(mundo, indice)
    origem = struct.unpack_from('<H', mundo.estruturas, p + 2)[0]
    slot = 0
    for linha in range(altura):
        for coluna in range(largura):
            if mascara[linha * largura + coluna] == '1':
                celula = (origem + linha * 256 + coluna) & 65535
                mundo.modificar_regiao_estrutura(indice, slot, celula, False)
                slot += 1
