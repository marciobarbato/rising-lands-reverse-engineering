"""Economy-owned MissionLoad initializer tails over shared world state.

EnginInitTechnologie 0x441459, BatimentInitCave 0x419112 in tail position,
PlayerRetrieve 0x46df41 and MarcheResetAll 0x46027c. Core's
Engin_RetrieveExperimente 0x441623 and ai-runtime's iaReset 0x47f36e sit
between them; missions composes the whole tail and enters neither here.
"""
from construcoes_habitaveis import bag_prend
from proprietarios import PASSO_BAG, PASSO_ORDENS_JOGADOR, inicializar_bag


def estrutura_realizavel(estruturas_realizaveis, rede, jogador, tipo):
    """TypeBatimentEstRealisable 0x418a93: AL owner, DL type, AL byte result.

    ReseauActif 0x42c3b0 (byte 0x4e0730) nonzero makes types 8 and 12 return
    0; otherwise byte 0x4dfad4 + 22*owner + type. Protected 0..3/0..21.
    """
    jogador, tipo = jogador & 255, tipo & 255
    if jogador >= 4 or tipo >= 22:
        raise ValueError('TypeBatimentEstRealisable protected owner/type is 0..3/0..21')
    if rede[0] and tipo in (8, 12):
        return 0
    return estruturas_realizaveis[jogador*22+tipo]


class CaudaCargaEconomia:
    """Shared-state tail provider; every buffer is used by identity.

    habitacao: Stage 15 HabitacaoConstrucoes (economy world, unit-order Bags
    propriedade.ordens at [0x4e19b8], structure realizability 0x4dfad4).
    ciclo_mercado: CicloMercado over the loaded market and the live player
    table [0x5080a8]. rede: one byte at 0x4e0730. jogadores_guardados: the
    80-byte source table [0x5080ac] written by InitPlayer/LoadPlayer/PlayerStore.
    """
    def __init__(self, habitacao, ciclo_mercado, *, rede, jogadores_guardados):
        self.habitacao = habitacao
        self.construcoes = habitacao.construcoes
        self.ciclo = ciclo_mercado
        self.rede = rede
        self.jogadores_guardados = jogadores_guardados
        for bloco, tamanho in ((habitacao.propriedade.ordens, 4*PASSO_ORDENS_JOGADOR), (rede, 1),
                               (jogadores_guardados, 80), (ciclo_mercado.mercado.jogadores, 80),
                               (self.construcoes.contagens_por_tipo, 88), (self.construcoes.contagens_tipo18, 4)):
            if len(bloco) != tamanho:
                raise ValueError(f'Load-tail buffer must have {tamanho} bytes')
        if ciclo_mercado.mercado.economia is not self.construcoes.economia:
            raise ValueError('Market and structures must share one resource table')

    def definir_tecnologia_unidades(self, jogador):
        """EnginSetTechnologie 0x4411e1: AL owner, protected 0..3.

        Unit 7 Bag: reset to capacity 22, then tag 3 value t for every
        structure type 0..21 except 20 that is realizable. Unit 14 Bag:
        capacity 1, tag 7 value 6. Unit 8 Bag: capacity 4, tag 2 values 0..3.
        The inline resets equal BagInit; Bag bytes +0x60..+0x65 are kept.
        """
        jogador &= 255
        if jogador >= 4:
            raise ValueError('EnginSetTechnologie protected owner is 0..3')
        ordens = self.habitacao.propriedade.ordens
        base = jogador*PASSO_ORDENS_JOGADOR
        construtor = base+7*PASSO_BAG
        inicializar_bag(ordens, construtor, 22)
        for tipo in range(22):
            if estrutura_realizavel(self.habitacao.estruturas_realizaveis, self.rede, jogador, tipo) and tipo != 20:
                bag_prend(ordens, construtor, 3, tipo)
        bag = base+14*PASSO_BAG
        inicializar_bag(ordens, bag, 1)
        bag_prend(ordens, bag, 7, 6)
        bag = base+8*PASSO_BAG
        inicializar_bag(ordens, bag, 4)
        for valor in range(4):
            bag_prend(ordens, bag, 2, valor)

    def inicializar_tecnologia_unidades(self):
        """EnginInitTechnologie 0x441459: owners 0..3 ascending."""
        for jogador in range(4):
            self.definir_tecnologia_unidades(jogador)

    def inicializar_cavernas(self, mundo):
        """BatimentInitCave 0x419112 in tail position on the shared world.

        Delegates to EconomiaConstrucoes.inicializar_armazens. Its 88-byte
        count table must be core's world table at 0x49a070 (core's raw name
        realizaveis_estruturas) and the structure pool the same object.
        """
        c = self.construcoes
        if (getattr(mundo, 'estruturas', None) is not c.estruturas
                or getattr(mundo, 'realizaveis_estruturas', None) is not c.contagens_por_tipo):
            raise ValueError('BatimentInitCave requires the shared structure pool and 0x49a070 table')
        c.inicializar_armazens()

    def recuperar_jogadores(self):
        """PlayerRetrieve 0x46df41: from [0x5080ac] into live [0x5080a8].

        First byte +6 (alliance mask) of the four 20-byte players, then
        bytes +0x0c..+0x13 (four signed16 sympathies). Nothing else moves.
        """
        vivos, guardados = self.ciclo.mercado.jogadores, self.jogadores_guardados
        for j in range(4):
            vivos[j*20+6] = guardados[j*20+6]
        for j in range(4):
            vivos[j*20+12:j*20+20] = guardados[j*20+12:j*20+20]

    def resetar_mercado(self):
        """MarcheResetAll 0x46027c: the committed complete all-player reset."""
        self.ciclo.resetar_todos()
