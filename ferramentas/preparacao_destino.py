"""Chemin_Verouille (0x43b30b): contexto, ajuste por anéis e teste de região."""
import struct
from dataclasses import dataclass
from otimizacao_caminhos import ContextoLinha, direcao_busca, passagem_da_busca


@dataclass(frozen=True)
class PreparacaoDestino:
    contexto: ContextoLinha
    inicio: int
    solicitado: int
    destino: int
    alternativa: int
    status: int
    concluida: int
    sucesso: int
    retorno: bool
    flag_unidades: int = 0
    flag_estruturas: int = 0

    @property
    def registrar_extremos(self):
        # Os globais início/destino só são escritos no ramo não concluído.
        return not self.concluida


def regiao_preservada(mundo, celula):
    """Uma camada da codificação, como em Chemin_MemeZone (0x42d4f8)."""
    valor = mundo.regioes[celula & 65535]
    if valor & 0x8000:
        indice, sub = (valor & 0x7fe0) >> 5, valor & 31
        return struct.unpack_from('<H', mundo.estruturas, indice * 276 + 0xcc + sub * 2)[0]
    if valor & 0x4000:
        return mundo.palavra((valor & 0x3ff8) >> 3, 0xfa + (valor & 3) * 2)
    return valor


def mesma_regiao_mundo(mundo, a, b):
    a, b = a & 65535, b & 65535
    if any((c & 255) >= mundo.largura or (c >> 8) >= mundo.altura for c in (a, b)):
        return False
    return regiao_preservada(mundo, a) == regiao_preservada(mundo, b)


def celulas_do_anel(destino, raio, largura, altura):
    """Ordem e limites de 0x43bd87..0x43e091, incluindo as inconsistências.

    Horizontais admitem x==largura. Laterais verificam x+j-raio contra altura
    e começam uma célula acima do y usado na verificação. Não corrigir isso
    silenciosamente: a primeira célula aceita encerra a procura original.
    """
    x, y = destino & 255, destino >> 8
    superior = destino - raio - raio * 256
    if y - raio >= 0:
        for j in range(2 * raio + 1):
            if 0 <= x + j - raio <= largura:
                yield (superior + j) & 65535
    if y + raio < altura:
        for j in range(2 * raio + 1):
            if 0 <= x + j - raio <= largura:
                yield (superior + 2 * raio * 256 + j) & 65535
    if x - raio >= 0:
        for j in range(1, 2 * raio):
            if y + j - raio >= 0 and x + j - raio < altura:
                yield (superior + (j - 1) * 256) & 65535
    if x + raio < largura:
        for j in range(1, 2 * raio):
            if y + j - raio >= 0 and x + j - raio < altura:
                yield (superior + 2 * raio + (j - 1) * 256) & 65535


def ajustar_destino(contexto, inicio, destino):
    m = contexto.mundo
    if destino == inicio:
        return inicio
    if (destino & 255) >= m.largura or (destino >> 8) >= m.altura:
        return 0xffff
    distancia = max(abs((destino & 255) - (inicio & 255)), abs((destino >> 8) - (inicio >> 8)))
    d = direcao_busca(inicio, destino)
    for raio in range(1, 30):
        if distancia == raio:
            return inicio
        for celula in celulas_do_anel(destino, raio, m.largura, m.altura):
            if passagem_da_busca(contexto, celula, d):
                return celula
    return 0xffff


def preparar_destino(mundo, indice, inicio, destino, mascara=None, flag_unidades=0, flag_estruturas=0):
    """Calcula os efeitos da preparação, sem depender do EXE ou de Unicorn.

    O chamador zera a contagem ativa da rota e aplica os globais devolvidos.
    A cauda da rota e os extremos anteriores ficam preservados nos ramos de término.
    """
    inicio, destino = inicio & 65535, destino & 65535
    c = ContextoLinha.da_unidade(mundo, indice)
    if mascara is not None:
        c = ContextoLinha(mundo, indice, c.classe, mascara & 255, c.dono)
    solicitado, alternativa, status = destino, 0xffff, 1
    if not passagem_da_busca(c, destino, direcao_busca(inicio, destino)):
        destino = ajustar_destino(c, inicio, destino)
        alternativa, status = destino, 2
    if not mesma_regiao_mundo(mundo, inicio, destino):
        concluida, sucesso, retorno, status = 1, 0, False, 7
    elif destino == 0xffff:
        concluida, sucesso, retorno, status = 1, 0, False, 6
    elif inicio == destino:
        concluida, sucesso, retorno = 1, 1, True
    else:
        concluida, sucesso, retorno = 0, 0, True
    return PreparacaoDestino(c, inicio, solicitado, destino, alternativa, status, concluida, sucesso,
                             retorno, flag_unidades & 255, flag_estruturas & 255)
