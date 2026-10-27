"""Etapas de CheminCalcul: vizinhança, obstáculos e escolha dos candidatos.

O contorno que estende os dois buffers continua no backend original. Esta
etapa traduz 0x42f247..0x430b7e e 0x43b073..0x43b2a9. O corpo que constrói
os dois percursos ainda é original emulado.
"""
import struct
from dataclasses import dataclass
from caminhos import aliados
from movimento import VETORES
from otimizacao_caminhos import ContextoLinha, direcao_busca, passagem_da_busca

VIZINHOS_GRANDES = ((-2, 1), (-2, 0), (-2, -1), (-2, -2), (-1, -2), (0, -2),
                    (1, -2), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1))
DIRECAO_PARA_DOZE = (1, 3, 5, 7, 8, 9, 10, 11)


@dataclass(frozen=True)
class InicioCandidatos:
    inicio: int
    destino: int
    direcao: int
    regiao_origem: int
    obstaculo_proximo: int
    todos_bloqueados: bool
    regioes: tuple
    registro_ocupantes: bytes


@dataclass(frozen=True)
class EscolhaCandidato:
    escolhido: int
    buffers: tuple
    status: int
    semente: int
    motivo: str


def aleatorio_caminhos(estado):
    """0x4704dc, incluindo DIV sem sinal e overflow das operações de 32 bits."""
    quociente, resto = divmod(estado & 0xffffffff, 127773)
    novo = (resto * 16807 - quociente * 2836) & 0xffffffff
    if novo == 0 or novo & 0x80000000:
        novo = (novo + 0x7fffffff) & 0xffffffff
    return novo


def selecionar_candidato(buffers, custos, registros, semente, status=1, flags=(0, 0)):
    """0x43b073..0x43b2a9: custos u16, exceções de ocupantes e desempate.

    Preserva a escrita do contador no segundo buffer mesmo quando o primeiro
    é selecionado nos ramos de status 4/5. As comparações CMP AL,AL do original
    fazem o primeiro registro prevalecer quando os dois são elegíveis.
    """
    if (len(buffers) != 2 or len(custos) != 2 or len(registros) != 2 or len(flags) != 2 or
            any(len(b) != 512 for b in buffers) or any(len(r) != 10 for r in registros)):
        raise ValueError('São necessários dois buffers de 512 bytes e registros de 10 bytes')
    saidas = [bytearray(b) for b in buffers]
    custos = [v & 65535 for v in custos]
    for i in range(2):
        if custos[i] == 0xffff:
            struct.pack_into('<H', saidas[i], 0, 255)
    contagens = [struct.unpack_from('<H', b)[0] for b in saidas]
    if any(n > 255 for n in contagens):
        raise ValueError('Contagem de candidato fora de 0..255')
    if contagens == [255, 255]:
        for campo, contador, estado, flag in ((4, 8, 4, flags[0]), (5, 9, 5, flags[1])):
            if flag:
                continue
            for i in range(2):
                if custos[i] != 0xffff and registros[i][campo]:
                    struct.pack_into('<H', saidas[1], 0, registros[i][contador])
                    return EscolhaCandidato(i, tuple(bytes(b) for b in saidas), estado,
                                             semente, 'ocupante_unidade' if campo == 4 else 'ocupante_estrutura')
    if custos[0] == custos[1]:
        semente = aleatorio_caminhos(semente)
        escolhido = 0 if semente & 3 == 0 else 1
        motivo = 'desempate_aleatorio'
    else:
        escolhido = int(custos[1] < custos[0])
        motivo = 'menor_custo'
    if struct.unpack_from('<H', saidas[escolhido])[0] == 255:
        status = 3
    return EscolhaCandidato(escolhido, tuple(bytes(b) for b in saidas), status, semente, motivo)


def iniciar_candidatos(contexto, inicio, destino):
    """Examina oito vizinhos na classe 1 ou o perímetro de doze nas demais."""
    m, indice = contexto.mundo, contexto.unidade
    inicio, destino = inicio & 65535, destino & 65535
    d = direcao_busca(inicio, destino)
    origem_regiao = m.palavra(indice, 0xfa)
    proximo, melhor, todos = 0xffff, 1, True
    regioes, registro = [], bytearray(10)
    if contexto.classe == 1:
        vizinhos = [(i, *VETORES[i]) for i in range(1, 16, 2)]
        desejada, circulo = d, 16
    else:
        vizinhos = [(i, *v) for i, v in enumerate(VIZINHOS_GRANDES)]
        desejada, circulo = DIRECAO_PARA_DOZE[d // 2], 12
    for direcao, dx, dy in vizinhos:
        x, y = (inicio & 255) + dx, (inicio >> 8) + dy
        if not (0 <= x < m.largura and 0 <= y < m.altura):
            continue
        celula = x + y * 256
        if celula == 0xffff:
            continue
        if passagem_da_busca(contexto, celula, direcao):
            todos = False
            continue
        distancia = direcao - desejada
        if distancia < -circulo // 2:
            distancia += circulo
        if distancia > circulo // 2:
            distancia -= circulo
        distancia = abs(distancia)
        if proximo == 0xffff or distancia < melhor:
            proximo, melhor = celula, distancia
        valor = m.regioes[celula]
        if valor & 0x8000:
            raise NotImplementedError('Candidatos com estruturas exigem a grade auxiliar de cores')
        if valor in (0, origem_regiao) or valor in regioes:
            continue
        if valor & 0x4000:
            outro = (valor & 0x3ff8) >> 3
            if outro == indice:
                continue
            # A aliança consultada para o registro tem o ocupante como origem.
            inimigo = int(not aliados(m.unidades[outro * 276], contexto.dono, m.mascaras_alianca))
            if registro[4] == 0 or inimigo > registro[6]:
                struct.pack_into('<H', registro, 0, outro)
                registro[4], registro[6], registro[8] = 1, inimigo, 0
            if valor & 4:
                if len(regioes) < 0xfb:
                    regioes.extend((valor & 0xfffc) + j for j in range(4))
            elif len(regioes) < 0xff:
                regioes.append(valor)
        elif len(regioes) < 0xff:
            regioes.append(valor)
    return InicioCandidatos(inicio, destino, d, origem_regiao, proximo, todos, tuple(regioes), bytes(registro))
