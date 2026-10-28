"""Avanço físico em terreno comum, ocupação, visão e conclusão de movimento.

Armadilhas hostis e fome sem provisões exigem efeitos de combate/economia ainda
não integrados e são recusados explicitamente antes de iniciar o avanço.
"""
import struct
from ordens_unidades import MundoUnidades
from visao_movimento import VisaoMovimento
from movimento import integrar_prefixo_passo, direcao_entre_celulas, celula_vizinha, atualizar_orientacao, pode_avancar
from caminhos import CLASSES_OCUPACAO, serializar_rota, proxima_celula, consumir_passo_concluido
from mensagens_chegada import notificar_estado

QUADRUPLOS = frozenset((3, 11, 12, 13, 14, 15, 16, 25))
QUADROS_FINAIS = (2, 3, 7, 7, 3, 5, 2, 3, 0, 5, 6, None, None, None, None, None, 6, None, 3, 3, 1, 0, 0, 3, 3, 7)


class MundoFisico(MundoUnidades, VisaoMovimento):
    def __init__(self, largura=16, altura=16):
        super().__init__()
        if not 1 <= largura <= 256 or not 1 <= altura <= 256:
            raise ValueError('Dimensões do mapa devem estar em 1..256')
        self.largura, self.altura = largura, altura
        self.atributos = bytearray(65536)
        self.regioes = [0] * 65536
        self.tiles = [0] * 65536
        self.donos_objetos = bytearray(65536)
        self.descoberto = [bytearray([31]) * 65536 for _ in range(4)]
        self.luz_bordas = [bytearray([31]) * 65536 for _ in range(4)]
        self.contagem_luz = [bytearray(65536) for _ in range(4)]
        self.mini_final, self.mini_unidades, self.mini_estruturas = (bytearray(65536) for _ in range(3))
        self.tamanho_minimapa = (128, 128)
        self.jogador_local = 0
        self.cores_jogadores = bytearray([10, 20, 30, 40, 50] + [0] * 27)
        self.cores_tiles = bytearray((i % 256 for i in range(702)))
        self.sombra = bytearray((i // 2 for i in range(256)))
        self.controle_jogadores = bytearray([2] * 4)
        self.limites_fadiga = [100] * 26
        self.bonus_fadiga = [[0] * 26 for _ in range(4)]
        self.rotas = [bytearray(b'\0\0') for _ in range(800)]

    def iniciar_morte_unidade(self, indice):
        from morte_unidades import iniciar_morte_unidade
        return iniciar_morte_unidade(self, indice)

    def _pegada(self, tipo, celula):
        return [(celula - d) & 65535 for d in ((0, 1, 257, 256) if tipo in QUADRUPLOS else (0,))]

    def ocupar(self, indice, celula, inserir):
        p = indice * 276
        tipo = self.unidades[p + 1]
        if not 0 <= tipo < 26:
            return
        mascara = 2 if tipo in (16, 17) else 1
        for sub, c in enumerate(self._pegada(tipo, celula)):
            if inserir:
                self.atributos[c] |= mascara
            else:
                self.atributos[c] &= 255 ^ mascara
            if tipo in (16, 17):
                continue
            tag = 0x4000 | (indice << 3) | sub | (4 if CLASSES_OCUPACAO[tipo] != 1 else 0)
            if inserir and self.regioes[c] < 0x4000:
                self.palavra(indice, 0xfa + sub * 2, self.regioes[c])
                self.regioes[c] = tag
            elif not inserir and self.regioes[c] == tag:
                self.regioes[c] = self.palavra(indice, 0xfa + sub * 2)

    def iniciar_passo(self, indice, celula):
        """Reserva um passo adjacente já escolhido; não faz busca ou desvio."""
        p = indice * 276
        atual = self.palavra(indice, 8)
        d = direcao_entre_celulas(atual, celula)
        if not d or celula_vizinha(atual, d, self.largura, self.altura) != celula:
            raise ValueError('Próxima célula deve ser adjacente e estar dentro do mapa')
        mascara = 2 if self.unidades[p + 1] in (16, 17) else 1
        for c in self._pegada(self.unidades[p + 1], celula):
            valor = self.regioes[c]
            propria = (valor & 0xc000) == 0x4000 and ((valor & 0x3ff8) >> 3) == indice
            if self.atributos[c] & mascara and not propria:
                raise NotImplementedError('Passo bloqueado exige seleção/desvio de caminho')
        self.ocupar(indice, self.palavra(indice, 0x7c), False)
        self.ocupar(indice, atual, True)
        self.ocupar(indice, celula, True)
        self.palavra(indice, 0x7c, celula)
        self.unidades[p + 0x90] = d

    def avancar_passo(self, indice, desconto=0):
        indice = self._indice(indice)
        p = indice * 276
        u = self.unidades
        tipo, dono = u[p + 1], u[p]
        destino = self.palavra(indice, 0x7c)
        fatiga = self.viva(indice) and u[p + 0x72] and tipo in tuple(range(11)) + (25,)
        limite = (self.limites_fadiga[tipo] + u[p + 0xf8] + (self.bonus_fadiga[dono][tipo] if dono < 4 else 0)) & 65535
        contador = (self.palavra(indice, 0x74) + 1) & 65535
        if fatiga and contador >= limite and self.palavra(indice, 4) == 0:
            raise NotImplementedError('Fome sem provisões exige inventário/dano ainda não integrados')
        if self.objetos[destino] == 0x46 and self.donos_objetos[destino] != dono and tipo not in (16, 17):
            raise NotImplementedError('Armadilha hostil exige dano e efeitos ainda não integrados')
        r = integrar_prefixo_passo(u[p + 0x86], u[p + 0x87], u[p + 0x97], u[p + 0x90], u[p + 0x98], desconto)
        u[p + 0x86], u[p + 0x87], u[p + 0x97] = r['deslocamento_x_u8'], r['deslocamento_y_u8'], r['progresso']
        if not r['chegou']:
            self._aplicar_fadiga(indice, fatiga, contador, limite)
            return False
        u[p + 0x86] = u[p + 0x87] = u[p + 0x97] = 0
        atual = self.palavra(indice, 8)
        self.ocupar(indice, atual, False)
        self.ocupar(indice, destino, True)
        self.minimapa(dono, atual, 5)
        raio = u[p + 0xbb] + u[p + 0xf5]
        if dono not in (4, 200):
            self.apagar_area(atual, raio, dono)
        self.palavra(indice, 8, destino)
        if dono not in (4, 200):
            self.descobrir_area(destino, raio + 2, dono)
            self.iluminar_area(destino, raio, dono)
        self.minimapa(dono, destino, 4)
        self.rotas[indice] = bytearray(consumir_passo_concluido(self.rotas[indice]))
        self._aplicar_fadiga(indice, fatiga, contador, limite)
        return True

    def _aplicar_fadiga(self, indice, habilitada, contador, limite):
        if habilitada:
            self.palavra(indice, 0x74, contador)
            if contador >= limite:
                self.palavra(indice, 0x74, 0)
                self.palavra(indice, 4, self.palavra(indice, 4) - 1)

    def concluir_movimento(self, indice):
        """Ramo do estado 2 em 0x4563da, até retornar ao despacho."""
        p = indice * 276
        u = self.unidades
        if u[p + 2] != 2 or self.palavra(indice, 8) != self.palavra(indice, 0x7e) or u[p + 0x91] != u[p + 0x90]:
            return False
        quadro = QUADROS_FINAIS[u[p + 1]]
        if quadro is not None:
            u[p + 0xa4] = quadro
        if self.viva(indice):
            u[p + 2] = 7
            self._liberar_busca(indice)
        return True

    def girar(self, indice):
        """RotateEngin, 0x448599, incluindo o byte auxiliar dos tipos 12/15."""
        p = indice * 276
        u = self.unidades
        if u[p + 1] in (12, 15):
            u[p + 0xda] = (2 * (u[p + 0x90] - 1) + 1) & 255
        u[p + 0x91], u[p + 0x92] = atualizar_orientacao(u[p + 0x90], u[p + 0x91], u[p + 0x92], u[p + 0x93])

    def atualizar_movimento(self, indice, maquina=None):
        """Coordena uma rota já escolhida, avanço e notificação; sem relógio fixo."""
        p = indice * 276
        u = self.unidades
        if not self.viva(indice):
            return notificar_estado(self, indice, maquina)
        if not self.concluir_movimento(indice) and u[p + 2] == 2:
            if not u[p + 0x86] and not u[p + 0x87] and self.palavra(indice, 8) == self.palavra(indice, 0x7c):
                proxima = proxima_celula(self.rotas[indice])
                if proxima is not None:
                    self.iniciar_passo(indice, proxima)
            desejada, atual = u[p + 0x90], u[p + 0x91]
            if desejada != atual:
                self.girar(indice)
            if pode_avancar(u[p + 0x90], u[p + 0x91]) and self.palavra(indice, 8) != self.palavra(indice, 0x7c):
                self.avancar_passo(indice)
        return notificar_estado(self, indice, maquina)
