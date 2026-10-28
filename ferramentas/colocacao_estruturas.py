"""PlaceBatiment e consultas de muros/portões, sem executar o EXE.

Coloca no terreno uma estrutura cujo registro já foi preparado pelo chamador.
Não cria registros, não debita recursos e não implementa a ordem de construir.
"""
import struct

# Tabela de saltos 0x41c454, selecionada por PlaceBatiment (0x41c4ac).
# Muros/portões seguem caminhos de objetos e não escolhem um tile aqui.
PRIMEIROS_TILES = (0x2fa,0x2be,0x2dc,0x306,0x393,0x333,0x415,0x3d7,
                  0x39f,None,0x403,0x433,None,0x31f,0x357,0x3c3,
                  0x36f,0x38f,0x3ef,0x383,0x3c3,0x409)


def _objeto(mundo, indice_linear):
    # Os auxiliares originais fazem leituras lineares, inclusive nas margens
    # entre linhas. Não envolver índices negativos/bordas com &65535.
    if not 0 <= indice_linear < 65536:
        raise NotImplementedError('Consulta além da grade de objetos exige bytes adjacentes ainda não modelados')
    return mundo.objetos[indice_linear]


def combinacao_muro(mundo, celula):
    """ChercheMurCombinaisons, 0x41c18a: O=8, S=4, L=2, N=1, menos um."""
    celula &= 65535
    muro, portao = mundo.objeto_muro & 255, mundo.objeto_portao & 255
    bits = 0
    for delta, bit in ((-1,8),(256,4),(1,2),(-256,1)):
        if _objeto(mundo,celula+delta) in (muro,portao):
            bits |= bit
    if _objeto(mundo,celula) == portao:
        return 0
    return bits-1 if bits else 0


def validar_portao(mundo, celula):
    """ValideHerse, 0x41ac8b: horizontal=0, vertical=1, sem encaixe=255.

    Conserva os testes contra 256: x=255 pode ler a próxima linha e y=255
    pode exigir dados além da grade. Horizontal tem preferência sobre vertical.
    """
    celula &= 65535
    x, y = celula & 255, celula >> 8
    vizinhos = (mundo.objeto_muro & 255,mundo.objeto_portao & 255)
    if x>0 and _objeto(mundo,celula-1) in vizinhos and x<256 and _objeto(mundo,celula+1) in vizinhos:
        return 0
    if y>0 and _objeto(mundo,celula-256) in vizinhos and y<256 and _objeto(mundo,celula+256) in vizinhos:
        return 1
    return 255


def colocar_estrutura(mundo, indice, mascara_tipo20=None):
    """PlaceBatiment, 0x41c4ac: seleciona tiles ou coloca muro/portão.

    A origem vem do u16 +2 e o tipo do byte +8. Um portão inválido não aplica
    efeitos. A atualização dos muros ao redor é outra chamada, como no x86.
    """
    indice &= 65535
    if indice >= 1000:
        raise ValueError('Índice de estrutura fora de 0..999')
    p = indice*276
    tipo = mundo.estruturas[p+8]
    if tipo >= len(PRIMEIROS_TILES):
        raise ValueError('Tipo de estrutura fora de 0..21')
    origem = struct.unpack_from('<H',mundo.estruturas,p+2)[0]
    if tipo not in (9,12):
        mundo.aplicar_terreno_estrutura(indice,origem,PRIMEIROS_TILES[tipo],mascara_tipo20)
        return
    if tipo == 9:
        combinacao = combinacao_muro(mundo,origem)
        struct.pack_into('<H',mundo.estruturas,p+0x7c,combinacao)
        mundo.objetos[origem] = mundo.objeto_muro & 255
        mundo.atributos[origem] |= 1
    else:
        orientacao = validar_portao(mundo,origem)
        if orientacao == 255:
            return
        struct.pack_into('<H',mundo.estruturas,p+0x7c,orientacao)
        mundo.objetos[origem] = mundo.objeto_portao & 255
        struct.pack_into('<H',mundo.estruturas,p+0x86,0)
        mundo.atributos[origem] |= 1
    mundo.modificar_regiao_estrutura(indice,0,origem,True)


def atualizar_muros_vizinhos(mundo, celula):
    """SetMurAllentour, 0x41c251: recalcula +7c dos muros O, L, N e S.

    Exige objeto de muro e rótulo de estrutura. Não testa o tipo do registro
    encontrado, nem atualiza portões ou recoloca o próprio centro.
    """
    celula &= 65535
    for delta in (-1,1,-256,256):
        if _objeto(mundo,celula+delta) != mundo.objeto_muro & 255:
            continue
        vizinha = (celula+delta)&65535
        valor = mundo.regioes[vizinha]
        if valor & 0x8000:
            indice = (valor & 0x7fe0)>>5
            if indice >= 1000:
                raise ValueError('Rótulo com índice fora da tabela de estruturas')
            struct.pack_into('<H',mundo.estruturas,indice*276+0x7c,combinacao_muro(mundo,vizinha))
