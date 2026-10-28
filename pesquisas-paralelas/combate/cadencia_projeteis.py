"""Portões locais de CalculGame e preparação visual do impacto, sem integração.

Não reproduz o laço Windows, menus, jogadores ou desenho. Os portões devem
ser usados nos pontos indicados: não formam um predicado global de tick.
O contador global e seu incremento já estão em ferramentas/cadencia.py.
"""
from dataclasses import dataclass


def continuar_apos_menu(estado_entrada, estado_atual, campo_4e0730):
    """0x42d14c: estado salvo na entrada, flag atual e estado relido."""
    return ((estado_entrada & 255) == 16 and (campo_4e0730 & 255) != 0
            and (estado_atual & 255) in (16, 18))


def continuar_apos_evento(campo_4e1b0e):
    """0x42d2e3: EvenementEnCours lê o byte 0x4e1b0e; não zero bloqueia."""
    return (campo_4e1b0e & 255) == 0


def permitir_bloco_projeteis(estado_atual, campo_4e0730):
    """0x42d3c0: revalidação depois dos comandos/jogadores, antes do bloco."""
    estado_atual &= 255
    return estado_atual == 18 or (estado_atual == 16 and (campo_4e0730 & 255) != 0)


@dataclass(frozen=True)
class PreparacaoImpacto:
    campo_4dfb44: int
    indice_4e1d18: int
    deslocamento_y: int
    retangulo_origem: tuple


def preparar_apresentacao_impacto(campo_4dfb44, indice_4e1d18, ciclo, tabela,
                                 largura_tela, campo_508f8d, largura_celulas,
                                 altura_celulas):
    """0x43f15c..0x43f220, antes do primeiro pedido de cópia de DDFlipPage.

Retorna os dois bytes atualizados e o retângulo (left, top, right, bottom).
Não desenha, não aplica um RNG novo nem avança o contador global. A tabela
compartilhada em 0x4e1c18 deve ser fornecida pelo caller; só é lida se o byte
do impacto não zero. campo_508f8d é o dword bruto da leitura desalinhada.
"""
    intensidade = campo_4dfb44 & 255
    indice = indice_4e1d18 & 255
    deslocamento = 0
    if intensidade:
        if tabela is None:
            raise NotImplementedError('Tabela necessária: 0x4e1c18')
        if len(tabela) != 256:
            raise ValueError('Tabela 0x4e1c18 deve conter 256 bytes')
        deslocamento = (tabela[indice] & 255) % intensidade
        indice = (indice + 1) & 255
        if not (ciclo & 1):
            intensidade -= 1
    margem = 0
    if (largura_tela & 65535) == 800:
        alto = (campo_508f8d >> 24) & 255
        margem = (alto - 256 if alto & 128 else alto) * 32
    retangulo = (margem, margem + deslocamento,
                 (largura_celulas & 65535) * 32 - margem,
                 (altura_celulas & 65535) * 32 - margem)
    return PreparacaoImpacto(intensidade, indice, deslocamento, retangulo)
