"""Início de recrutamento e consultas econômicas de ocupação/progresso.

A escolha da posição de saída é dependência explícita de geometria/ocupação.
Este módulo não cria unidades, movimenta tropas ou implementa uma fila FIFO.
"""
import struct

from construcoes import EconomiaConstrucoes, PASSO_CONSTRUCAO
from economia import custos_unidade

BASE_SELECOES = 0x495be0
BASE_TIPOS_UNIDADES = 0x4965ae
BASE_TIPOS_SORTILEGIOS = 0x497174
BASE_PERIODO_NOVA = 0x495bf0
TIPOS_RECRUTADORES = frozenset((1, 2, 5, 13, 15, 16, 18, 20))
TIPOS_STATUS_UNIDADE = TIPOS_RECRUTADORES - {18}


def _word(bloco, offset):
    return struct.unpack_from('<H', bloco, offset)[0]


class SaidaRecrutamentoPendente(RuntimeError):
    """Cobrança e estado já aplicados; falta RechercheDecalageSortie 0x41d1d0."""
    endereco = 0x41d1d0

    def __init__(self, indice, jogador, tipo_unidade):
        self.indice, self.jogador, self.tipo_unidade = indice, jogador, tipo_unidade
        super().__init__(f'Escolha da saída pendente para construção {indice}; cobrança já aplicada')


class Recrutamento:
    def __init__(self, mundo=None, *, selecoes=None, tipos_unidades=None,
                 tipos_sortilegios=None, unidades=None, periodo_nova=50):
        self.mundo = EconomiaConstrucoes() if mundo is None else mundo
        # Valores sintéticos, não equivalem a executar os carregadores do jogo.
        self.selecoes = bytearray(b'\xff' * 8 if selecoes is None else selecoes)
        self.tipos_unidades = bytearray(26 * 50 if tipos_unidades is None else tipos_unidades)
        self.tipos_sortilegios = bytearray(5 * 46 if tipos_sortilegios is None else tipos_sortilegios)
        self.unidades = bytearray(800 * 276 if unidades is None else unidades)
        for bloco, tamanho in ((self.selecoes, 8), (self.tipos_unidades, 1300),
                               (self.tipos_sortilegios, 230), (self.unidades, 220800)):
            if len(bloco) != tamanho:
                raise ValueError(f'Buffer de recrutamento deve ter {tamanho} bytes')
        self.periodo_nova = periodo_nova & 65535

    def _selecao(self, jogador):
        jogador &= 255
        if jogador >= 4:
            raise ValueError('Jogador fora de 0..3 após truncar DL')
        return jogador, _word(self.selecoes, jogador * 2)

    def _offset(self, indice):
        indice &= 65535
        offset = indice * PASSO_CONSTRUCAO
        if offset + PASSO_CONSTRUCAO > len(self.mundo.estruturas):
            raise ValueError('Índice de construção fora do buffer protegido')
        return offset

    def _tipo_unidade(self, tipo):
        tipo &= 255
        if tipo >= 26:
            raise ValueError('Tipo de unidade fora de 0..25 após truncar AL')
        return memoryview(self.tipos_unidades)[tipo * 50:(tipo + 1) * 50]

    def tempo_unidade(self, tipo):
        """EnginGetTimeRecrute 0x4410b7: word +0 do tipo de 50 bytes."""
        return _word(self._tipo_unidade(tipo), 0)

    def tempo_sortilegio(self, tipo):
        """SortilegeGetTimeAprentissage 0x47476a: word +0, passo 46."""
        tipo &= 255
        if tipo >= 5:
            raise ValueError('Tipo de sortilégio fora de 0..4 após truncar AL')
        return _word(self.tipos_sortilegios, tipo * 46)

    def vida_maxima_unidade(self, indice):
        """EnginGetVieMax 0x441108: tipo no byte +1 da unidade, vida no tipo +8."""
        indice &= 65535
        if indice >= 800:
            raise ValueError('Unidade fora de 0..799 após truncar AX')
        return _word(self._tipo_unidade(self.unidades[indice * 276 + 1]), 8)

    def iniciar(self, tipo_unidade, jogador, *, escolher_saida=None):
        """InitRecruteTroupe 0x4283e2: AL=tipo, DL=jogador; AL=0/1.

        Recusa sem cobrar quando faltam saldos, tipo de construção é inadequado
        ou +0x74 está ocupado. Não confere dono, +5, tecnologia ou compatibilidade
        entre tipo de unidade e construção. Debita comida, pedra, peças, nesta
        ordem, recalculando o indicador após cada débito, inclusive valor zero.

        Sem callback, lança SaidaRecrutamentoPendente APÓS cobrança e mudança
        de estado. Não chamar iniciar novamente para retomar: usar concluir_saida
        após resolver a dependência. O callback recebe o índice e deve executar
        RechercheDecalageSortie inteira, retornando sua célula u16.
        """
        jogador, indice = self._selecao(jogador)
        tipo_unidade &= 255
        custos = custos_unidade(self._tipo_unidade(tipo_unidade))
        if not self.mundo.economia.suficiente(jogador, *custos[:3]):
            return False
        # No original o ponteiro é calculado antes, mas dereferenciado só aqui.
        o = self._offset(indice)
        s = self.mundo.estruturas
        if s[o + 8] not in TIPOS_RECRUTADORES or s[o + 0x74]:
            return False
        for recurso, custo in zip((1, 2, 0), custos[:3]):
            self.mundo.retirar(jogador, recurso, custo)
        s[o + 0x74], s[o + 0x7a], s[o + 5], s[o + 0x7b] = 1, 0, 4, tipo_unidade
        struct.pack_into('<I', s, o + 0x8c, 1)
        struct.pack_into('<H', s, o + 0x7e, 0)
        if s[o + 8] != 20:
            struct.pack_into('<HH', s, o + 0x80, 0, 0)
        _, indice_saida = self._selecao(jogador)
        if escolher_saida is None:
            raise SaidaRecrutamentoPendente(indice_saida, jogador, tipo_unidade)
        return self.concluir_saida(indice, escolher_saida(indice_saida))

    def concluir_saida(self, indice, celula):
        """Sufixo 0x428640: grava AX em +0x7c e retorna AL=1.

        API de continuação, não uma função original independente. Não valida
        célula, não recobra recursos e não verifica novamente os pré-requisitos.
        """
        struct.pack_into('<H', self.mundo.estruturas, self._offset(indice) + 0x7c, celula & 65535)
        return True

    def unidade_em_recrutamento(self, tipo, jogador):
        """EnginEnRecrutement 0x420bdf: só compara +0x7b da seleção com AL.

        Não verifica +0x74, +5, proprietário ou progresso. Seleção 0xffff é falsa.
        """
        _, indice = self._selecao(jogador)
        return indice != 65535 and self.mundo.estruturas[self._offset(indice) + 0x7b] == (tipo & 255)

    def sortilegio_em_recrutamento(self, tipo, jogador):
        """SortEnRecrutement 0x420ba5: corpo equivalente à consulta de unidade."""
        return self.unidade_em_recrutamento(tipo, jogador)

    def calcular_status(self, indice, tipo):
        """CalculStatusRecrute 0x423f9d: AX=índice, DL=tipo; EAX=quociente u32.

        Divide o progresso +0x8c pelo tempo ou pela vida máxima de uma unidade
        referenciada. Não usa o tipo solicitado armazenado em +0x7b nem verifica
        atividade. Não satura em 100. Divisor zero levanta ZeroDivisionError.
        """
        indice &= 65535
        if indice == 65535:
            return 0
        o = self._offset(indice)
        s = self.mundo.estruturas
        construcao = s[o + 8]
        if construcao in TIPOS_STATUS_UNIDADE or (construcao == 18 and s[o + 0x7a] == 0):
            divisor = self.tempo_unidade(tipo)
        elif construcao == 6:
            divisor = self.tempo_sortilegio(tipo)
        elif construcao == 14 or construcao == 18:
            divisor = self.vida_maxima_unidade(_word(s, o + 0x88))
        else:
            return 0
        return struct.unpack_from('<I', s, o + 0x8c)[0] // divisor

    def status(self, tipo, jogador):
        """GetStatusRecrute 0x423f83: AL=tipo, DL=jogador; resolve a seleção."""
        _, indice = self._selecao(jogador)
        return self.calcular_status(indice, tipo)

    def progresso_nova(self, indice):
        """CalculNovaRecrute 0x423e65: (+0x108 * 100) em u32 / período u16."""
        indice &= 65535
        if indice == 65535:
            return 0
        progresso = struct.unpack_from('<I', self.mundo.estruturas, self._offset(indice) + 0x108)[0]
        return ((progresso * 100) & 0xffffffff) // (self.periodo_nova & 65535)
