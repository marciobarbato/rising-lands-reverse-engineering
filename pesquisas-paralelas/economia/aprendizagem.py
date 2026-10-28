"""Custos, início e conclusão da aprendizagem e listas de sortilégios.

CalculTroupe 0x4259e6: somente o ramo tipo 6. Os outros ramos, incluindo
criação/saída/movimento de unidades, não são executados por esta API.
"""
import struct

from producao import Producao
from economia import Saldos
from proprietarios import (PropriedadeConstrucoes, PASSO_BAG, PASSO_ORDENS_JOGADOR,
                           PASSO_PENDENCIAS_JOGADOR, inicializar_bag)

BASE_INVENCOES = 0x508f44


def _lista_sortilegios(memoria, offset, tipos):
    """BagInit capacidade 5 e BagPrend modo 4 após o reset, sem slots pré-existentes."""
    inicializar_bag(memoria, offset, 5)
    for posicao, tipo in enumerate(tipos):
        memoria[offset + 0x42 + posicao] = 4
        struct.pack_into('<H', memoria, offset + 6 + 2 * posicao, tipo)
        struct.pack_into('<H', memoria, offset, posicao + 1)
        struct.pack_into('<H', memoria, offset + 0x66, posicao + 1)


class Aprendizagem:
    def __init__(self, producao=None, propriedade=None, *, inventados=None):
        self.producao = Producao() if producao is None else producao
        mundo = self.producao.recrutamento.mundo
        self.propriedade = PropriedadeConstrucoes(mundo) if propriedade is None else propriedade
        if self.propriedade.mundo is not mundo:
            raise ValueError('Produção e propriedade devem compartilhar o mesmo mundo')
        self.inventados = bytearray(20 if inventados is None else inventados)
        if len(self.inventados) != 20:
            raise ValueError('Invenções devem conter 20 bytes: quatro jogadores × cinco tipos')

    @staticmethod
    def _jogador(jogador):
        jogador &= 255
        if jogador >= 4:
            raise ValueError('Jogador fora de 0..3 após truncar AL')
        return jogador

    def _indice(self, jogador, tipo):
        jogador = self._jogador(jogador)
        tipo &= 65535  # DX, não DL, nos quatro acessores de flags.
        if tipo >= 5:
            raise ValueError('Sortilégio fora de 0..4 após truncar DX')
        return jogador * 5 + tipo

    def disponivel(self, jogador, tipo):
        """SortilegeEstRealisable 0x474958: retorna o byte, sem normalizar para bool."""
        return self.propriedade.sortilegios[self._indice(jogador, tipo)]

    def liberar(self, jogador, tipo):
        """SortilegeSetRealisable 0x474974: grava 1; não modifica as listas."""
        self.propriedade.sortilegios[self._indice(jogador, tipo)] = 1

    def inventado(self, jogador, tipo):
        """SortilegeEstInvente 0x474991: outra tabela, em 0x508f44."""
        return self.inventados[self._indice(jogador, tipo)]

    def marcar_inventado(self, jogador, tipo):
        """SortilegeSetInvention 0x4749ad: grava 1; não libera nem refaz listas."""
        self.inventados[self._indice(jogador, tipo)] = 1

    def zerar_disponiveis(self, jogador):
        """SortilegeResetRealisable 0x4749ca: cinco bytes, mantendo invenções/listas."""
        o = self._jogador(jogador) * 5
        self.propriedade.sortilegios[o:o + 5] = bytes(5)

    def zerar_tecnologia(self):
        """SortilegeResetTechnologie 0x4749f2: zera as duas tabelas de 20 bytes."""
        self.propriedade.sortilegios[:] = bytes(20)
        self.inventados[:] = bytes(20)

    def atualizar_ordens(self, jogador):
        """SortilegeSetTechnologie 0x474a38: refaz a Bag de ordens do tipo de unidade 4."""
        j = self._jogador(jogador)
        tipos = (t for t in range(5) if self.propriedade.sortilegios[j * 5 + t] != 0)
        _lista_sortilegios(self.propriedade.ordens, j * PASSO_ORDENS_JOGADOR + 4 * PASSO_BAG, tipos)

    def inicializar_ordens(self):
        """SortilegeInitTechnologie 0x474a95: refaz as quatro Bags, sem zerar flags."""
        for j in range(4):
            self.atualizar_ordens(j)

    def atualizar_pesquisas_biblioteca(self, jogador):
        """BatimentSetTechnologie 0x41c76c, somente DL=6.

        Refaz a Bag tipo 6 com invenções ainda não disponíveis. AL>=4 é um
        retorno antecipado original, preservado aqui. Outros tipos não estão
        cobertos por este método.
        """
        j = jogador & 255
        if j >= 4:
            return
        tipos = (t for t in range(5) if self.inventados[j * 5 + t] != 0
                 and self.propriedade.sortilegios[j * 5 + t] == 0)
        _lista_sortilegios(self.propriedade.pendencias, j * PASSO_PENDENCIAS_JOGADOR + 6 * PASSO_BAG, tipos)

    def custos(self, tipo):
        """SortilegeGetCoutApprentissage 0x4746fe: AL=tipo; words +4/+2/+6.

        Retorna comida, pedra, peças (e quarto=0), na ordem dos ponteiros
        EDX/EBX/ECX. A chamada original só grava dois bytes por saída.
        """
        tipo &= 255
        if tipo >= 5:
            raise ValueError('Sortilégio fora de 0..4 após truncar AL')
        pedra, comida, pecas = struct.unpack_from('<3H', self.producao.recrutamento.tipos_sortilegios, tipo * 46 + 2)
        return Saldos(comida, pedra, pecas)

    def iniciar(self, jogador, tipo):
        """InitApprentissage 0x422d9f: AL=jogador, DL=tipo; sem retorno semântico.

        Resolve a construção selecionada e recusa apenas se +0x74 != 0.
        Não verifica suficiência, dono, tipo da construção ou flags de pesquisa.
        Debita comida e pedra, recalculando após cada uma; não debita peças.
        Uma exceção de recálculo pode deixar somente o primeiro débito aplicado.
        """
        r = self.producao.recrutamento
        jogador, indice = r._selecao(jogador)
        o = r._offset(indice)
        s = r.mundo.estruturas
        if s[o + 0x74] != 0:
            return
        tipo &= 255
        custos = self.custos(tipo)
        r.mundo.retirar(jogador, 1, custos.comida)
        r.mundo.retirar(jogador, 2, custos.pedra)
        s[o + 0x74], s[o + 5], s[o + 0x7b] = 1, 4, tipo
        struct.pack_into('<I', s, o + 0x8c, 1)

    def terminar_biblioteca(self, indice):
        """ApprentissageSortTerminer 0x421250, domínio tipo 6.

        Conclui incondicionalmente, sem verificar flag, tempo ou progresso.
        Outros tipos têm efeitos de tecnologia ainda não cobertos nesta API.
        """
        r = self.producao.recrutamento
        o = r._offset(indice)
        s = r.mundo.estruturas
        if s[o + 8] != 6:
            raise NotImplementedError('ApprentissageSortTerminer: somente o domínio tipo 6 foi traduzido')
        self.liberar(s[o + 4], s[o + 0x7b])
        self.atualizar_ordens(s[o + 4])
        self.atualizar_pesquisas_biblioteca(s[o + 4])
        struct.pack_into('<H', s, o + 0x78, 65535)
        s[o + 0x7b] = 255
        for campo in (0x7c, 0x7e, 0x80, 0x82):
            struct.pack_into('<H', s, o + campo, 0)
        struct.pack_into('<H', s, o + 0x86, 65535)
        s[o + 0x74] = 0
        struct.pack_into('<I', s, o + 0x8c, 0)
        if s[o + 5] != 3:
            s[o + 5] = 5

    def calcular_biblioteca(self, indice):
        """CalculTroupe 0x4259e6, ramo tipo 6 completo, incluindo conclusão.

        Sem retorno semântico: a rotina original usa EAX como registrador de
        trabalho. Flag +0x74 zero retorna antes até da primeira consulta de
        tempo. A conclusão pode ocorrer na mesma chamada que cruza o limite.
        """
        r = self.producao.recrutamento
        o = r._offset(indice)
        s = r.mundo.estruturas
        if s[o + 8] != 6:
            raise NotImplementedError('CalculTroupe: somente o ramo da biblioteca foi traduzido')
        if s[o + 0x74] == 0:
            return
        if not self.producao.avancar_sortilegio(indice):
            return
        tipo = s[o + 0x7b]
        limite = r.tempo_sortilegio(tipo) * 100
        if struct.unpack_from('<I', s, o + 0x8c)[0] < limite:
            return
        # O original tem esse corpo inline; a reutilização é apenas no Python.
        self.terminar_biblioteca(indice)
