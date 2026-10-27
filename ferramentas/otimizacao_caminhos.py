"""TestLigneOptimise e OptimiseChemin traduzidos das instruções originais.

Recebem o contexto já preparado pela busca. A preparação do destino e a
construção dos candidatos estão em preparacao_destino.py/contornos_caminhos.py.
"""
import struct
from dataclasses import dataclass
from typing import Optional, Tuple
from caminhos import (CLASSES_OCUPACAO, Ocupante, classificar_passagem,
                      pertence_a_propria_ocupacao, testar_mascara_celula)
from movimento import VETORES


@dataclass(frozen=True)
class ContextoLinha:
    mundo: object
    unidade: int
    classe: int
    mascara: int
    dono: int

    @classmethod
    def da_unidade(cls, mundo, indice):
        p = indice * 276
        return cls(mundo, indice, CLASSES_OCUPACAO[mundo.unidades[p + 1]],
                   1 + int(mundo.unidades[p + 0xab] != 0), mundo.unidades[p])


@dataclass(frozen=True)
class ResultadoLinha:
    permitido: bool
    celulas: Tuple[int, ...]
    # A recusa da primeira consulta não escreve o contador fornecido.
    contador: Optional[int]


def direcao_busca(origem, destino):
    """Tabelas 0x496388..93: células iguais produzem 5, diferentemente de GetDir."""
    dx = (destino & 255) - (origem & 255)
    dy = ((destino & 65535) >> 8) - ((origem & 65535) >> 8)
    indice = int(dx > 0) + 2 * int(dy > 0)
    tabela = (5, 5, 13, 13) if dx == 0 else ((1, 9, 1, 9) if dy == 0 else (3, 7, 15, 11))
    return tabela[indice]


def _vizinha(mundo, celula, direcao):
    dx, dy = VETORES[direcao]
    x, y = (celula & 255) + dx, ((celula & 65535) >> 8) + dy
    return x + 256 * y if 0 <= x < mundo.largura and 0 <= y < mundo.altura else 0xffff


def passagem_da_busca(contexto, celula, direcao):
    """Predicado embutido em TestLigneOptimise; não é EnginPeutPasser."""
    m, indice = contexto.mundo, contexto.unidade
    if contexto.classe not in (1, 2, 3):
        return True
    if contexto.classe in (2, 3) and ((celula & 255) == 0 or (celula >> 8) == 0):
        return False
    p, u = indice * 276, m.unidades
    deltas = (0,) if contexto.classe == 1 else (0, 1, 257, 256)
    for delta in deltas:
        c = (celula - delta) & 65535
        if not testar_mascara_celula(m.objetos[c], m.atributos[c], contexto.mascara):
            continue
        if pertence_a_propria_ocupacao(m.palavra(indice, 8), c, contexto.classe,
                                       u[p + 2], u[p + 0xab], contexto.mascara):
            continue
        valor = m.regioes[c]
        if valor & 0xc000 != 0x4000:
            return False
        outro = (valor & 0x3ff8) >> 3
        q = outro * 276
        ocupante = Ocupante(u[q], u[q + 1], m.palavra(outro, 8), m.palavra(outro, 0x7e),
                            u[q + 0x90], u[q + 2], u[q + 0x89], u[q + 0x8a])
        if not classificar_passagem(contexto.dono, u[p + 1], ocupante, direcao,
                                    m.mascaras_alianca, permitir_parados=m.permitir_aliados_parados,
                                    variante_booleana=True):
            return False
    return True


def testar_linha(contexto, origem, destino):
    """0x42d674: caminha pelos sinais, inclui origem e exclui destino.

    Preserva o prefixo escrito em caso de falha e o limite original de 255
    iterações. Um retorno positivo sozinho não garante que alcançou o destino.
    """
    m = contexto.mundo
    origem, destino = origem & 65535, destino & 65535
    m.permitir_aliados_parados = 0
    d = direcao_busca(origem, destino)
    primeira = _vizinha(m, origem, d)
    if not passagem_da_busca(contexto, primeira, d):
        return ResultadoLinha(False, (), None)
    atual, escritas = origem, []
    for _ in range(255):
        if atual == destino:
            break
        if not passagem_da_busca(contexto, atual, d):
            return ResultadoLinha(False, tuple(escritas), len(escritas))
        escritas.append(atual)
        d = direcao_busca(atual, destino)
        atual = _vizinha(m, atual, d)
        if atual == 0xffff:
            return ResultadoLinha(False, tuple(escritas), len(escritas))
    return ResultadoLinha(True, tuple(escritas), len(escritas))


def compactar_lacos(celulas):
    """Primeira passagem de 0x42e890; adjacência usa diferenças em oito bits."""
    compactas, cursor = [], 0
    while cursor < len(celulas):
        for final in range(len(celulas) - 1, cursor + 1, -1):
            a, b = celulas[cursor], celulas[final]
            if (((b & 255) + 1 - (a & 255)) & 255) < 3 and (((b >> 8) + 1 - (a >> 8)) & 255) < 3:
                compactas.append(a)
                cursor = final
                break
        compactas.append(celulas[cursor])
        cursor += 1
    return compactas


def otimizar_rota(contexto, buffer):
    """0x42e890: contador + células em ordem direta, antes da serialização.

    Devolve todos os 512 bytes, inclusive resíduos de tentativas recusadas.
    O domínio suportado usa buffers originais e rotas cuja escrita cabe neles.
    """
    if len(buffer) != 512:
        raise ValueError('OptimiseChemin exige buffer de 512 bytes')
    quantidade = struct.unpack_from('<H', buffer)[0]
    if quantidade > 255:
        raise ValueError('Contagem original fora do domínio 0..255')
    celulas = list(struct.unpack_from('<' + 'H' * quantidade, buffer, 2))
    compactas = compactar_lacos(celulas)
    saida = bytearray(buffer)
    cursor, contagem = 0, 0
    struct.pack_into('<H', saida, 0, 0)
    while cursor < len(compactas):
        encontrou = False
        for final in range(len(compactas) - 2, cursor, -1):
            teste = testar_linha(contexto, compactas[cursor], compactas[final])
            if contagem + len(teste.celulas) > 255:
                raise NotImplementedError('Escrita da otimização excederia o buffer original')
            for i, celula in enumerate(teste.celulas, contagem + 1):
                struct.pack_into('<H', saida, i * 2, celula)
            if teste.permitido:
                cursor = final
                contagem += teste.contador
                encontrou = True
                break
        if not encontrou:
            contagem += 1
            if contagem > 255:
                raise NotImplementedError('Escrita da otimização excederia o buffer original')
            struct.pack_into('<H', saida, contagem * 2, compactas[cursor])
            cursor += 1
        struct.pack_into('<H', saida, 0, contagem)
    return bytes(saida)
