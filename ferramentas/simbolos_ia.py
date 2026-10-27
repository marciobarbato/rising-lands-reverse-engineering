"""Leitores dos símbolos SBL e do programa RULE, sem executar o jogo."""
from dataclasses import dataclass
import struct


@dataclass(frozen=True)
class Simbolo:
    deslocamento: int
    nome: str


def ler_sbl(dados):
    """0x48d5fd: XOR 0xff, pares u32 até deslocamento 0xffffffff.

    Não há cabeçalho: o primeiro par também é um símbolo.
    """
    decodificado = bytes(b ^ 255 for b in dados)
    pares, posicao = [], 0
    while True:
        if posicao + 8 > len(decodificado):
            raise ValueError('SBL sem terminador de tabela')
        deslocamento, nome = struct.unpack_from('<II', decodificado, posicao)
        posicao += 8
        if deslocamento == 0xffffffff:
            break
        pares.append((deslocamento, nome))
    simbolos = []
    for deslocamento, nome in pares:
        if not posicao <= nome < len(decodificado):
            raise ValueError('Nome SBL fora da área de strings')
        fim = decodificado.find(b'\0', nome)
        if fim < 0:
            raise ValueError('Nome SBL sem terminador')
        simbolos.append(Simbolo(deslocamento, decodificado[nome:fim].decode('cp1252').rstrip(' ')))
    return simbolos


def enderecar_simbolos(simbolos, endereco_ancora=0x48ff7f):
    """0x48d74b usa _debugGetPC como âncora, não o ImageBase do PE."""
    ancoras = [s for s in simbolos if s.nome == '_debugGetPC']
    if len(ancoras) != 1:
        raise ValueError('SBL precisa de uma âncora _debugGetPC')
    base = endereco_ancora - ancoras[0].deslocamento
    enderecos = {}
    for simbolo in simbolos:
        enderecos.setdefault(simbolo.nome, base + simbolo.deslocamento)
    return base, enderecos


@dataclass(frozen=True)
class Instrucao:
    operacao: object  # nome original (str) ou tipo de subtarefa (int)
    formato: int
    sucesso: int
    falha: int
    constante: int

    @property
    def quantidade_argumentos(self):
        return (self.formato >> 4) & 15

    @property
    def variavel_resultado(self):
        return self.formato & 15

    def argumentos(self, variaveis):
        resultado = []
        for i in range(self.quantidade_argumentos):
            # SHR x86 mascara a contagem de deslocamento em cinco bits.
            origem = (self.formato >> ((8 + 4 * i) & 31)) & 15
            resultado.append(variaveis[origem - 1] if origem else self.constante)
        return resultado


@dataclass(frozen=True)
class ProgramaRegras:
    campo_04: int
    tamanho_strings: int
    instrucoes: tuple
    entradas: tuple


def ler_rul(dados):
    """0x47e437: cabeçalho de 16 bytes, registros de 20 e entradas u16."""
    if len(dados) < 16:
        raise ValueError('Cabeçalho RULE truncado')
    assinatura, campo_04, tamanho_strings, quantidade, tipos = struct.unpack_from('<4sIIHH', dados)
    if assinatura != b'RULE' or not 4 <= quantidade <= 1200 or tipos > 64:
        raise ValueError('Cabeçalho RULE inválido')
    fim_instrucoes = 16 + quantidade * 20
    inicio_strings = fim_instrucoes + tipos * 2
    if inicio_strings + tamanho_strings != len(dados):
        raise ValueError('Tamanho RULE divergente')
    entradas = struct.unpack_from('<' + 'H' * tipos, dados, fim_instrucoes)
    if any(i >= quantidade for i in entradas):
        raise ValueError('Entrada de tarefa fora do programa')
    strings = dados[inicio_strings:]
    instrucoes = []
    for i in range(quantidade):
        operacao, formato, sucesso, falha, constante = struct.unpack_from('<5I', dados, 16 + i * 20)
        if sucesso >= quantidade or falha >= quantidade:
            raise ValueError('Destino de desvio fora do programa')
        if operacao & 0x80000000:
            offset = operacao & 0x7fffffff
            fim = strings.find(b'\0', offset)
            if offset >= len(strings) or fim < 0:
                raise ValueError('Nome de operação RULE inválido')
            operacao = strings[offset:fim].decode('cp1252')
        elif operacao >= 64:
            raise ValueError('Operação numérica sem resolução suportada')
        instrucoes.append(Instrucao(operacao, formato, sucesso, falha, constante))
    return ProgramaRegras(campo_04, tamanho_strings, tuple(instrucoes), entradas)
