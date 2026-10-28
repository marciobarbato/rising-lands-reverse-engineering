"""Efeitos de ordens da IA sobre a RAM das unidades, reconstruídos do x86.

Preserva os campos que a ordem não escreve. O avanço físico por células ocorre
noutras rotinas; emitir a ordem não altera imediatamente a posição atual.
"""
import struct
from dataclasses import dataclass

PASSO = 276
BASE_GRUPOS = 0x51a9e0
OPERACOES = frozenset(('V_DeplacerUnite', 'V_DeplaceGroupe',
                       'I_DonneTypeUnite', 'B_TestUniteFaitRien', 'I_AttenteMessageGroupe'))


@dataclass
class ContextoBusca:
    unidade: int = 0xffff  # 0x496304
    ocupada: int = 0       # 0x4e0f36
    sucesso: int = 0       # 0x4e0f37
    ponteiro_rota: int = 0 # 0x4e0f3c
    concluida: int = 0     # 0x496302; a emissão de ordem NÃO limpa este byte


class MundoUnidades:
    def __init__(self):
        self.unidades = bytearray(800 * PASSO)
        self.estruturas = bytearray(1000 * PASSO)
        self.realizaveis_estruturas = bytearray(88)  # raw table 0x49a070
        self.selecoes_estruturas = bytearray(8)     # four u16 at 0x495be0
        self.experiencias_unidades = bytearray(40) # raw four-owner queue at 0x4e19c4
        self.selecoes_unidades = bytearray(2048)   # raw four selection lists at 0x508728
        self.grupos = bytearray(100 * 32)
        for grupo in range(100):
            struct.pack_into('<H', self.grupos, grupo * 32 + 0x10, 0xffff)
        self.objetos = bytearray(65536)
        self.busca = ContextoBusca()
        self.grupo_em_iteracao = 0  # ponteiro global 0x51b844
        self.unidade_em_iteracao = 0  # u16 global 0x51b848

    def inicializar_registros_estruturas(self):
        from ciclo_estruturas import inicializar_registros_estruturas
        return inicializar_registros_estruturas(self.estruturas, self.realizaveis_estruturas)

    def resetar_todas_estruturas(self):
        from ciclo_estruturas import resetar_todas_estruturas
        return resetar_todas_estruturas(self.estruturas, self.realizaveis_estruturas, self.selecoes_estruturas)

    def resetar_estrutura(self, indice):
        from ciclo_estruturas import resetar_estrutura
        return resetar_estrutura(self.estruturas, indice)

    def buscar_estrutura_livre(self):
        from ciclo_estruturas import buscar_estrutura_livre
        return buscar_estrutura_livre(self.estruturas)

    def calcular_posicao_saida(self, indice, direcao=0, dimensoes=None):
        from posicao_saida import calcular_posicao_saida
        return calcular_posicao_saida(self, indice, direcao, dimensoes)

    def converter_unidade(self, indice, celula, direcao, tipo, tipos_unidades,
                         *, capacidade_tipo=None, modificador=None):
        from conversao_unidades import converter_unidade
        return converter_unidade(self, indice, celula, direcao, tipo, tipos_unidades,
                                 capacidade_tipo=capacidade_tipo, modificador=modificador)

    def atualizar_capacidades_unidades(self, jogador, *, capacidade_tipo=None, modificador=None):
        from capacidades_unidades import atualizar_capacidades_unidades
        return atualizar_capacidades_unidades(self, jogador, capacidade_tipo=capacidade_tipo,
                                              modificador=modificador)

    def adicionar_vida_unidade(self, indice, acrescimo, tipos_unidades):
        from recuperacao_unidades import adicionar_vida_unidade
        return adicionar_vida_unidade(self, indice, acrescimo, tipos_unidades)

    def resetar_fadiga_unidade(self, indice):
        from recuperacao_unidades import resetar_fadiga_unidade
        return resetar_fadiga_unidade(self, indice)

    def aplicar_nova_experiencia(self, indice, nivel, tipos_unidades=None):
        from experiencia_unidades import aplicar_nova_experiencia
        return aplicar_nova_experiencia(self, indice, nivel, tipos_unidades)

    def consumir_experiencia_unidade(self, indice, tipos_unidades=None):
        from experiencia_unidades import consumir_experiencia_unidade
        return consumir_experiencia_unidade(self, indice, tipos_unidades)

    def inicializar_selecoes_unidades(self):
        from selecao_unidades import inicializar_selecoes_unidades
        return inicializar_selecoes_unidades(self.selecoes_unidades)

    @staticmethod
    def _indice(indice):
        indice &= 65535
        if indice >= 800:
            raise ValueError('Unidade fora da tabela reconstruída (0..799)')
        return indice

    def escrever_unidade(self, indice, dados):
        indice = self._indice(indice)
        if len(dados) != PASSO:
            raise ValueError('Registro de unidade deve conter 276 bytes')
        self.unidades[indice * PASSO:(indice + 1) * PASSO] = dados

    def ler_unidade(self, indice):
        indice = self._indice(indice)
        return bytes(self.unidades[indice * PASSO:(indice + 1) * PASSO])

    def palavra(self, indice, offset, valor=None):
        p = self._indice(indice) * PASSO + offset
        if valor is not None:
            struct.pack_into('<H', self.unidades, p, valor & 65535)
        return struct.unpack_from('<H', self.unidades, p)[0]

    def viva(self, indice):
        """EnginEstVivant, 0x443dad: estado diferente de 0 e 4."""
        return self.unidades[self._indice(indice) * PASSO + 2] not in (0, 4)

    def _liberar_busca(self, indice):
        if self.busca.unidade == indice:
            self.busca.unidade = 0xffff
            self.busca.ocupada = self.busca.sucesso = self.busca.ponteiro_rota = 0

    def redefinir_ordem(self, indice):
        """ResetOrdre, 0x44357c; inclui a liberação de estrutura pelo tipo 13."""
        indice = self._indice(indice)
        p = indice * PASSO
        tipo = self.unidades[p + 1]
        if self.unidades[p + 0x86] == 0 and self.unidades[p + 0x87] == 0 and tipo != 16:
            self.unidades[p + 0xa9] = self.unidades[p + 0xa4] = 0
        estrutura = self.palavra(indice, 0xc0)
        if tipo == 13 and estrutura != 0xffff:
            if estrutura >= 1000:
                raise ValueError('Estrutura fora da tabela reconstruída (0..999)')
            e = estrutura * PASSO
            self.estruturas[e + 0x74] = 0  # BatimentDelocke
            if self.estruturas[e + 0x76] == 15 and self.estruturas[e + 0x75] != 0:
                self.estruturas[e + 0x75] = 0  # BatimentTuyauCave, DL=0
        self.palavra(indice, 0x7e, self.palavra(indice, 0x7c))
        self._liberar_busca(indice)
        self.unidades[p + 0x88] = self.unidades[p + 0x82] = 0
        self.palavra(indice, 0xb2, 0xffff)
        self.unidades[p + 2] = 2

    def definir_movimento(self, indice, destino):
        """SetDeplaceEngin, 0x4457d3; não aplica o predicado de atividade do wrapper."""
        indice, destino = self._indice(indice), destino & 65535
        p = indice * PASSO
        self.redefinir_ordem(indice)
        self.unidades[p + 0x88] = 0
        self._liberar_busca(indice)
        if self.unidades[p + 1] == 6 and self.objetos[destino] in (0x36, 0x42):
            self.redefinir_ordem(indice)
            self.unidades[p + 2] = 5
            self.unidades[p + 0x89] = 1
            self.palavra(indice, 0x7e, destino)
            self._liberar_busca(indice)
            self.unidades[p + 0x88] = 0
            self.palavra(indice, 0xb2, destino)
            return
        self.palavra(indice, 0x7e, destino)
        self._liberar_busca(indice)
        self.unidades[p + 0x88] = 0
        self.unidades[p + 2] = 2
        self.palavra(indice, 0xb8, 0xffff)
        self.palavra(indice, 0xb2, 0xffff)
        self.unidades[p + 0xbe] = 255
        self.palavra(indice, 0xc0, 0xffff)

    def mover_unidade(self, destino, indice):
        """V_DeplacerUnite: destino antes do índice; sempre retorna 1."""
        indice = self._indice(indice)
        if self.viva(indice):
            self.definir_movimento(indice, destino)
        return 1

    def definir_grupo(self, grupo, indices):
        """Prepara cabeça e encadeamento +0x108, sem simular inclusão administrativa."""
        if not 0 <= grupo < 100:
            raise ValueError('Grupo fora da tabela reconstruída (0..99)')
        indices = [self._indice(i) for i in indices]
        if len(indices) != len(set(indices)):
            raise ValueError('Grupo não pode repetir unidades')
        struct.pack_into('<H', self.grupos, grupo * 32 + 0x10, indices[0] if indices else 0xffff)
        for i, indice in enumerate(indices):
            self.palavra(indice, 0x108, indices[i + 1] if i + 1 < len(indices) else 0xffff)

    def mover_grupo(self, grupo, destino):
        """V_DeplaceGroupe: percorre a lista, preservando estado 1 com vínculo b8."""
        if not 0 <= grupo < 100:
            raise ValueError('Grupo fora da tabela reconstruída (0..99)')
        self.grupo_em_iteracao = BASE_GRUPOS + grupo * 32
        indice = struct.unpack_from('<H', self.grupos, grupo * 32 + 0x10)[0]
        self.unidade_em_iteracao = indice
        visitadas = set()
        while indice != 0xffff:
            indice = self._indice(indice)
            if indice in visitadas:
                raise ValueError('Ciclo no encadeamento de unidades do grupo')
            visitadas.add(indice)
            p = indice * PASSO
            if self.viva(indice) and (self.unidades[p + 2] != 1 or self.palavra(indice, 0xb8) == 0xffff):
                self.definir_movimento(indice, destino)
            indice = self.palavra(indice, 0x108)
            self.unidade_em_iteracao = indice
        return 1

    def aguardar_mensagem_grupo(self, maquina, tarefa, grupo, mascara):
        """iagMessSetWait, 0x4841f4; contador zero aguarda evento externo."""
        if not 0 <= grupo < 100:
            raise ValueError('Grupo fora da tabela reconstruída')
        struct.pack_into('<I', self.grupos, grupo * 32 + 0x1c, mascara & 0xffffffff)
        struct.pack_into('<I', self.grupos, grupo * 32 + 8, tarefa)
        maquina.suspender(tarefa)
        return 1

    def executar_operacao(self, nome, argumentos):
        if nome == 'V_DeplacerUnite':
            return self.mover_unidade(argumentos[0], argumentos[1])
        if nome == 'V_DeplaceGroupe':
            return self.mover_grupo(argumentos[0], argumentos[1])
        if nome == 'I_DonneTypeUnite':
            return self.unidades[self._indice(argumentos[0]) * PASSO + 1]
        if nome == 'B_TestUniteFaitRien':
            return 1 if self.unidades[self._indice(argumentos[0]) * PASSO + 2] == 7 else 0xffffffff
        raise NotImplementedError(nome)
