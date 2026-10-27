"""Máquina parcial de tarefas de iaSolver (0x47d314), com memória reconstruída.

Executa controle de fluxo, subtarefas, listas e espera. Operações de mundo não
implementadas falham explicitamente; não se simulam sucesso ou recursos fictícios.
"""
import struct
from simbolos_ia import ProgramaRegras


def u32(v):
    return v & 0xffffffff


def i32(v):
    v &= 0xffffffff
    return v - 0x100000000 if v & 0x80000000 else v


def dividir(a, b):
    a, b = i32(a), i32(b)
    if b == 0 or (a == -0x80000000 and b == -1):
        raise ArithmeticError('Divisão inválida no domínio x86')
    return u32((abs(a) // abs(b)) * (-1 if (a < 0) != (b < 0) else 1))


class MaquinaTarefas:
    def __init__(self, programa: ProgramaRegras, operacoes=None, missao=0):
        self.programa = programa
        self.operacoes = operacoes or {}
        self.missao = missao
        self.memoria = bytearray(100 * 96)
        for i in range(100):
            self.gravar(i, 0, i + 1 if i < 99 else -1)
        self.livres = [0, 100]
        # 0x47cfd0 mantém o campo +4 em 100 também nas listas vazias.
        self.contextos = [[-1, 100] for _ in range(5)]
        self.ativas = 0

    def ler(self, indice, offset):
        return struct.unpack_from('<I', self.memoria, indice * 96 + offset)[0]

    def gravar(self, indice, offset, valor):
        struct.pack_into('<I', self.memoria, indice * 96 + offset, u32(valor))

    def byte(self, indice, offset, valor=None):
        p = indice * 96 + offset
        if valor is not None:
            self.memoria[p] = valor & 255
        return self.memoria[p]

    def palavra(self, indice, offset, valor=None):
        p = indice * 96 + offset
        if valor is not None:
            struct.pack_into('<H', self.memoria, p, valor & 65535)
        return struct.unpack_from('<H', self.memoria, p)[0]

    def nova(self, tipo):
        if not 1 <= tipo < len(self.programa.entradas) or tipo >= 64 or not self.programa.entradas[tipo]:
            return -1
        indice = self.livres[0]
        if indice == -1:
            return -1
        self.livres[0] = i32(self.ler(indice, 0))
        self.livres[1] -= 1
        self.gravar(indice, 0, -1)
        self.ativas += 1
        for offset, valor in [(4, -1), (8, -1), (12, self.programa.entradas[tipo]), (16, 0), (20, 0)]:
            self.gravar(indice, offset, valor)
        self.palavra(indice, 0x58, 0)
        self.palavra(indice, 0x5a, tipo)
        self.byte(indice, 0x5d, 255)
        self.byte(indice, 0x5e, 0)
        self.byte(indice, 0x5f, 0)
        return indice

    def postar(self, jogador, tipo, argumentos=()):
        if not 0 <= jogador < 5 or len(argumentos) > 6:
            raise ValueError('Jogador ou quantidade de argumentos inválidos')
        indice = self.nova(tipo)
        if indice == -1:
            return -1
        for i, valor in enumerate(tuple(argumentos) + (0,) * (6 - len(argumentos))):
            self.gravar(indice, 0x18 + i * 4, valor)
        self.byte(indice, 0x5c, jogador)
        contexto = self.contextos[jogador]
        anterior = contexto[0]
        if anterior == -1:
            contexto[0] = indice
        else:
            while i32(self.ler(anterior, 0)) != -1:
                anterior = i32(self.ler(anterior, 0))
            self.gravar(anterior, 0, indice)
        contexto[1] += 1
        return indice

    def remover(self, jogador, indice):
        pai = i32(self.ler(indice, 4))
        if pai != -1:
            self.byte(pai, 0x5e, 0)
            self.byte(pai, 0x5f, 1)
        contexto = self.contextos[jogador]
        anterior, atual = -1, contexto[0]
        while atual != indice:
            if atual == -1:
                raise ValueError('Tarefa fora da lista')
            anterior, atual = atual, i32(self.ler(atual, 0))
        seguinte = i32(self.ler(indice, 0))
        if anterior == -1:
            contexto[0] = seguinte
        else:
            self.gravar(anterior, 0, seguinte)
        contexto[1] -= 1
        self.gravar(indice, 0, self.livres[0])
        self.livres[0] = indice
        self.livres[1] += 1
        self.ativas -= 1

    def executar_operacao(self, nome, argumentos, jogador, indice):
        a = argumentos
        if nome == 'V_Attendre':
            self.byte(indice, 0x5e, 1)
            self.gravar(indice, 0x14, a[0])
            return 1
        if nome in ('B_Bidon', 'B_AccessibiliteChemin', 'B_AccessibiliteBatiment'):
            return 1  # Os três nomes apontam para 0x47f31c.
        if nome in ('B_GicleUniteAmieDeZone', 'B_TestUniteAmieSurZone', 'B_TestUniteEnnemieSurZone'):
            return 0xffffffff  # Aliases de 0x47f322.
        if nome == 'B_Egalite':
            return 1 if u32(a[0]) == u32(a[1]) else 0xffffffff
        if nome == 'B_Superieur':
            return 1 if i32(a[0]) > i32(a[1]) else 0xffffffff
        if nome == 'I_Addition':
            return u32(a[0] + a[1])
        if nome == 'I_Soustraction':
            return u32(a[0] - a[1]) if i32(a[0]) >= i32(a[1]) else 0
        if nome == 'I_PourcentageAB':
            return u32(dividir(a[0], a[1]) * 100)  # Divisão ANTES de multiplicar.
        if nome == 'I_Affecte':
            return u32(a[0])
        if nome == 'I_NumMission':
            return self.missao & 255
        if nome == 'I_Divise':
            return dividir(a[0], a[1]) if u32(a[1]) else 0xffffffff
        if nome not in self.operacoes:
            raise NotImplementedError('Operação de mundo ainda não reconstruída: ' + nome)
        return u32(self.operacoes[nome](self, argumentos, jogador, indice))

    def atualizar(self, jogador, limite=10000):
        if not 0 <= jogador < 5:
            raise ValueError('Jogador inválido')
        indice, passos = self.contextos[jogador][0], 0
        while indice != -1:
            seguinte = i32(self.ler(indice, 0))
            if self.byte(indice, 0x5e):
                tempo = i32(self.ler(indice, 0x14))
                if tempo <= 0:
                    indice = seguinte
                    continue
                self.gravar(indice, 0x14, tempo - 1)
                if tempo > 1:
                    indice = seguinte
                    continue
                self.byte(indice, 0x5e, 0)
                self.byte(indice, 0x5f, 1)
                self.gravar(indice, 0x54, 1)
            while True:
                passos += 1
                if passos > limite:
                    raise RuntimeError('Limite de instruções da máquina de tarefas')
                op = self.programa.instrucoes[self.ler(indice, 12)]
                if self.byte(indice, 0x5f):
                    if self.palavra(indice, 0x58):
                        self.palavra(indice, 0x58, 0)
                    elif op.variavel_resultado:
                        self.gravar(indice, 0x14 + op.variavel_resultado * 4, self.ler(indice, 0x54))
                    self.byte(indice, 0x5f, 0)
                    resultado = self.ler(indice, 0x54)
                else:
                    variaveis = [self.ler(indice, 0x18 + i * 4) for i in range(15)]
                    argumentos = op.argumentos(variaveis)
                    if isinstance(op.operacao, int) or op.operacao == 'NULL':
                        tipo = 0 if op.operacao == 'NULL' else op.operacao
                        filho = self.nova(tipo)
                        if filho == -1:
                            self.remover(jogador, indice)
                            break
                        for i, valor in enumerate(argumentos):
                            self.gravar(filho, 0x18 + i * 4, valor)
                        self.byte(filho, 0x5c, self.byte(indice, 0x5c))
                        self.gravar(filho, 0, self.ler(indice, 0))
                        self.gravar(indice, 0, filho)
                        self.gravar(filho, 4, indice)
                        self.gravar(filho, 0x14, 0)
                        self.byte(indice, 0x5e, 1)
                        self.palavra(indice, 0x58, tipo)
                        break
                    resultado = self.executar_operacao(op.operacao, argumentos, self.byte(indice, 0x5c), indice)
                    if self.byte(indice, 0x5e):
                        break
                    if op.variavel_resultado:
                        self.gravar(indice, 0x14 + op.variavel_resultado * 4, resultado)
                destino = op.falha if resultado == 0xffffffff else op.sucesso
                if destino <= 3:
                    pai = i32(self.ler(indice, 4))
                    if destino in (1, 2) and pai != -1:
                        self.gravar(pai, 0x54, 1 if destino == 1 else -1)
                    self.remover(jogador, indice)
                    break
                self.gravar(indice, 12, destino)
            indice = seguinte
        return 0 if self.ativas else 0x1a1a000e
