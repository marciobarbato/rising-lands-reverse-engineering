"""Primitivas reconstruídas do x86; não substituem o solucionador completo."""
import struct
from dataclasses import dataclass

CLASSES_OCUPACAO = (1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                    3, 1, 1, 1, 1, 1, 1, 1, 3, 3)


def aliados(origem, destino, mascaras):
    """0x46d838: relação direcional, inclusive igualdade de IDs especiais."""
    origem, destino = origem & 255, destino & 255
    return origem == destino or (origem <= 4 and destino <= 4 and
                                 bool(mascaras[origem] & (1 << destino)))


def resolver_regiao(valor, regioes_unidades, regioes_estruturas):
    """0x42d4f8: remove uma camada de ocupação, sem resolução recursiva."""
    valor &= 65535
    if valor & 0x8000:
        return regioes_estruturas[(valor & 0x7fe0) >> 5][valor & 31]
    if valor & 0x4000:
        return regioes_unidades[(valor & 0x3ff8) >> 3][valor & 3]
    return valor


def mesma_regiao(a, b, largura, altura, grade, unidades, estruturas):
    """Compara rótulos preservados sob ocupantes; não garante rota livre."""
    a, b = a & 65535, b & 65535
    if any((c & 255) >= largura or (c >> 8) >= altura for c in (a, b)):
        return False
    return resolver_regiao(grade[a], unidades, estruturas) == resolver_regiao(grade[b], unidades, estruturas)


@dataclass(frozen=True)
class Ocupante:
    dono: int
    tipo: int
    atual: int
    destino: int
    direcao: int
    estado: int = 0
    campo_89: int = 0
    campo_8a: int = 0


def classificar_passagem(dono, tipo, ocupante, direcao, mascaras, permitir_parados=False,
                        variante_booleana=False):
    """0x42eba4 retorna 0/1/2; 0x42ece0 converte os dois casos positivos em 1.

    1: exceção entre tipos adversários; 2: orientação/flag permite passagem.
    Não presume que a exceção seja atropelamento ou ataque.
    """
    diferenca = ocupante.direcao - direcao
    diferenca = (abs(diferenca) // 2) * (-1 if diferenca < 0 else 1)
    if diferenca < -4:
        diferenca += 8
    if diferenca > 4:
        diferenca -= 8
    alinhado = -2 < diferenca < 2
    movendo = ocupante.atual != ocupante.destino
    if ((ocupante.tipo in (0, 1, 20, 21) and ocupante.estado == 1 and ocupante.campo_8a == 1) or
        (ocupante.tipo in (6, 7) and ocupante.estado == 15 and ocupante.campo_89 == 1)):
        movendo = False
    amigo = aliados(dono, ocupante.dono, mascaras)
    # 0x442409 e 0x4423d5, limitados aos 26 tipos válidos do jogo.
    if not 0 <= tipo < 26 or not 0 <= ocupante.tipo < 26:
        raise ValueError('Tipo fora do domínio reconstruído (0..25)')
    excecao = tipo in (12, 15) and ocupante.tipo in (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 18, 19, 22)
    if amigo:
        resultado = 2 if (alinhado if movendo else permitir_parados) else 0
    elif excecao:
        resultado = 1
    else:
        resultado = 2 if movendo and alinhado else 0
    return int(bool(resultado)) if variante_booleana else resultado


def serializar_rota(celulas):
    """0x43b2be..0x43b300: count + células invertidas para consumo como pilha."""
    if len(celulas) > 255 or any(not 0 <= c <= 65535 for c in celulas):
        raise ValueError('Rota deve conter até 255 células u16')
    return struct.pack('<' + 'H' * (len(celulas) + 1), len(celulas), *reversed(celulas))


def proxima_celula(buffer):
    """Leitura da rota em 0x448b9f, sem efeitos de movimento/ocupação."""
    quantidade = struct.unpack_from('<H', buffer)[0]
    if not quantidade:
        return None
    return struct.unpack_from('<H', buffer, quantidade * 2)[0]


def atualizar_espera(contador):
    """Estado de caminho 6, 0x4494fc: igualdade em 20, com overflow u8."""
    contador = (contador + 1) & 255
    return (3, 0) if contador == 20 else (6, contador)


def testar_mascara_celula(objeto, atributo, mascara):
    """0x43ec0c: objeto 0xfd usa bit 0 da máscara e ignora o atributo."""
    return bool((mascara & 1) if (objeto & 255) == 0xfd else (atributo & mascara & 255))


def pertence_a_propria_ocupacao(atual, consultada, classe, estado, campo_ab, mascara):
    """0x43eb64: exceção de ocupação própria; subtrações sem wrap em 16 bits."""
    atual, consultada = atual & 65535, consultada & 65535
    if (campo_ab == 50 and mascara == 1) or (campo_ab == 0 and mascara == 2) or estado == 14:
        return False
    celulas = (atual,) if classe == 1 else (atual, atual - 1, atual - 257, atual - 256)
    return consultada in celulas
