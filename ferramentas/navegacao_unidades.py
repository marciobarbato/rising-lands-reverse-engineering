"""Desvios locais e estados de caminho ligados ao avanço físico.

O cálculo geral é fornecido por um backend explícito. SolucionadorOriginal usa
os bytes originais em Unicorn; SolucionadorCaminhosPython executa as traduções
das classes 1..3 sem emulação, incluindo estruturas e desbloqueios.
"""
import struct
from avanco_unidades import MundoFisico
from movimento import direcao_entre_celulas, celula_vizinha, pode_avancar
from caminhos import proxima_celula, atualizar_espera
from passagem_unidades import consultar_passagem
from mensagens_chegada import notificar_estado
from regioes_mapa import reconstruir_regioes
from estruturas_caminhos import CoresEstruturas, modificar_regiao_estrutura


class MundoNavegacao(MundoFisico):
    def __init__(self, largura=16, altura=16, solucionador=None):
        super().__init__(largura, altura)
        self.rotas = [bytearray(512) for _ in range(800)]
        self.solucionador = solucionador
        self.marcadores_obstaculos_tiles = bytearray(702)
        self.resultados_busca = {}
        self.historico_navegacao = []
        self.semente_caminhos = 1
        self.mascaras_alianca = bytearray(5)
        self.permitir_aliados_parados = 0
        self.cores_estruturas = CoresEstruturas(largura, altura)
        self.ultimo_bloqueador = self.ultima_celula_livre = 0
        self.objeto_muro, self.objeto_portao = 254, 253  # bytes 0x495bf8/0x495bf9

    def modificar_regiao_estrutura(self, indice, subcelula, celula, inserir):
        return modificar_regiao_estrutura(self, indice, subcelula, celula, inserir)

    def aplicar_terreno_estrutura(self, indice, origem, primeiro_tile, mascara_tipo20=None):
        from terreno_estruturas import aplicar_terreno_estrutura
        return aplicar_terreno_estrutura(self, indice, origem, primeiro_tile, mascara_tipo20)

    def resetar_terreno_estrutura(self, indice, modo):
        from terreno_estruturas import resetar_terreno_estrutura
        return resetar_terreno_estrutura(self, indice, modo)

    def remover_regioes_estrutura(self, indice):
        from terreno_estruturas import remover_regioes_estrutura
        return remover_regioes_estrutura(self, indice)

    def colocar_estrutura(self, indice, mascara_tipo20=None):
        from colocacao_estruturas import colocar_estrutura
        return colocar_estrutura(self, indice, mascara_tipo20)

    def atualizar_muros_vizinhos(self, celula):
        from colocacao_estruturas import atualizar_muros_vizinhos
        return atualizar_muros_vizinhos(self, celula)

    def alternar_portoes(self, celula, indice):
        from portoes import alternar_portoes
        return alternar_portoes(self,celula,indice)

    def avancar_estado_portao(self, indice):
        from portoes import avancar_estado_portao
        return avancar_estado_portao(self,indice)

    def iniciar_remapeamento(self):
        from remapeamento_mundo import iniciar_remapeamento
        return iniciar_remapeamento(self)

    def refazer_regioes(self):
        """Reconstrói rótulos e reaplica ocupação; usar antes de executar a busca."""
        if any(v & 0x8000 for v in self.regioes):
            raise NotImplementedError('Refaça as regiões naturais antes de inserir estruturas; remapeamento integral ainda pendente')
        regioes, atributos, quantidade = reconstruir_regioes(self.atributos, self.tiles, self.objetos,
                                                             self.marcadores_obstaculos_tiles, self.largura, self.altura)
        vivas = getattr(self, 'grades_vivas', frozenset())
        if 'regioes' in vivas:
            self.regioes[:] = regioes          # a live grid keeps its identity
        else:
            self.regioes = regioes
        if 'atributos' in vivas:
            self.atributos[:] = atributos
        else:
            self.atributos = atributos
        self.busca.unidade = 0xffff
        self.busca.ocupada = self.busca.sucesso = self.busca.ponteiro_rota = 0
        for i in range(800):
            if self.viva(i):
                self.ocupar(i, self.palavra(i, 8), True)
                self.ocupar(i, self.palavra(i, 0x7c), True)
        return quantidade

    def _registrar_passo(self, indice, celula, direcao, candidatos):
        p = indice * 276
        if self.unidades[p + 1] in (12, 15) and any(i != 0xffff for i in candidatos):
            raise NotImplementedError('Passagem exige efeitos de atropelamento ainda não integrados')
        self.ocupar(indice, self.palavra(indice, 0x7c), False)
        self.ocupar(indice, self.palavra(indice, 8), True)
        self.ocupar(indice, celula, True)
        self.palavra(indice, 0x7c, celula)
        self.unidades[p + 0x90] = direcao

    def escolher_direto(self, indice):
        """EnginNextCase, 0x448d08: d, d-2, d; não supõe d+2."""
        p = indice * 276
        u = self.unidades
        origem, destino = self.palavra(indice, 8), self.palavra(indice, 0x7e)
        d = direcao_entre_celulas(origem, destino)
        for tentativa in range(3):
            c = celula_vizinha(origem, d, self.largura, self.altura)
            if c != 0xffff:
                permitido, candidatos = consultar_passagem(self, indice, c)
                if permitido:
                    self._registrar_passo(indice, c, d, candidatos)
                    u[p + 0x8b] = 0
                    return True
                if c == destino:
                    self.palavra(indice, 0x7e, self.palavra(indice, 0x7c))
                    self._liberar_busca(indice)
                    u[p + 0x88] = 0
                    return False
            d = ((d - 3) % 16) + 1 if tentativa == 0 else ((d + 1) % 16) + 1
        u[p + 0x88], u[p + 0x8b] = 3, 0
        return False

    def escolher_da_rota(self, indice):
        """EnginNextCaseChemin, 0x448b9f; bloqueio invalida a rota ativa."""
        p = indice * 276
        c = proxima_celula(self.rotas[indice])
        if c is None:
            self.unidades[p + 0x88] = self.unidades[p + 0x8b] = 0
            return False
        permitido, candidatos = consultar_passagem(self, indice, c)
        if not permitido:
            self.unidades[p + 0x88] = self.unidades[p + 0x8b] = 0
            return False
        d = direcao_entre_celulas(self.palavra(indice, 8), c)
        self._registrar_passo(indice, c, d, candidatos)
        return True

    def _aplicar_resultado(self, indice, resultado):
        self.resultados_busca[indice] = resultado
        self.rotas[indice] = bytearray(resultado['buffer_rota'])
        self.semente_caminhos = resultado['semente']
        for nome, valor in resultado['contexto'].items():
            setattr(self.busca, nome, valor)
        self.historico_navegacao.append(dict(unidade=indice, origem=self.palavra(indice, 8),
                                            destino=self.palavra(indice, 0x7e), status=resultado['status'],
                                            concluida=self.busca.concluida, sucesso=self.busca.sucesso,
                                            quantidade=struct.unpack_from('<H', self.rotas[indice])[0]))

    def atualizar_estado_caminho(self, indice):
        """Retorna True quando o ramo permite a etapa física nesta atualização."""
        p = indice * 276
        u = self.unidades
        estado = u[p + 0x88]
        if estado in (0, 5):
            if not u[p + 0x86] and not u[p + 0x87]:
                self.escolher_da_rota(indice) if estado == 5 else self.escolher_direto(indice)
            return True
        if estado == 1:
            u[p + 0x88] = 0
        elif estado == 3:
            if u[p + 0x86] or u[p + 0x87]:
                return True
            if not self.busca.ocupada:
                if self.solucionador is None:
                    raise NotImplementedError('Busca geral requer um solucionador explícito; use SolucionadorOriginal')
                self._aplicar_resultado(indice, self.solucionador.iniciar(self, indice))
                u[p + 0x88] = 4
        elif estado == 4:
            if not self.busca.concluida:
                self._aplicar_resultado(indice, self.solucionador.continuar(self, indice))
                return False
            r = self.resultados_busca[indice]
            if self.busca.sucesso:
                if u[p + 2] == 2 and r['status'] == 2:
                    self.palavra(indice, 0x7e, r['destino_alternativo'])
                u[p + 0x88] = 5
            elif r['status'] == 8:
                u[p + 0x88], u[p + 0x8b] = 6, 0
            else:
                # EnginDebloqueNextCase pode ordenar que um aliado saia da frente.
                # Ambos os backends aplicam as ordens e devolvem o resultado.
                mudancas = self.solucionador.desbloquear(self, indice)
                u = self.unidades
                if mudancas['desbloqueou']:
                    u[p + 0x88] = 0
                else:
                    self.palavra(indice, 0x7e, self.palavra(indice, 0x7c))
                    u[p + 0x88] = 0
            self._liberar_busca(indice)
        elif estado == 6:
            u[p + 0x88], u[p + 0x8b] = atualizar_espera(u[p + 0x8b])
        return False

    def animar_movimento(self, indice):
        """CalculNextCase 0x448fc3..0x449048: the walk-animation tick of a unit with a pending step.

        Every type but 16, 17 and those above 25 advances +0xa9; when it reaches the period +0xa7,
        +0xa9 = 0 and frame +0xa4 = (+0xa4 + 1) % frames +0xa5. Type 17 calls AnimBallonStatic instead.
        """
        p = indice * 276
        u = self.unidades
        tipo = u[p + 1]
        if tipo == 17:
            raise NotImplementedError('AnimBallonStatic 0x447b2f (type 17) is not translated')
        if tipo == 16 or tipo > 25:
            return
        u[p + 0xa9] = (u[p + 0xa9] + 1) & 255
        if u[p + 0xa9] == u[p + 0xa7]:
            if not u[p + 0xa5]:
                raise ValueError('Zero animation frame count: the original faults on IDIV at 0x449039')
            u[p + 0xa4] = (u[p + 0xa4] + 1) % u[p + 0xa5]
            u[p + 0xa9] = 0

    def _som_movimento(self, indice):
        """CalculNextCase 0x449060..0x4490fd: a local player's unit of type 11..16 on a discovered cell
        queries EnginGetVolume, sets +0xf9 and may post a sound; that branch is not translated."""
        p = indice * 276
        u = self.unidades
        local = self.jogador_local
        if u[p] == local and 11 <= u[p + 1] <= 16 and not self.descoberto[local][self.palavra(indice, 8)] & 0x1f:
            raise NotImplementedError('CalculNextCase local-player volume/sound 0x4490c3 is not translated')

    def calcular_proxima_celula(self, indice):
        """CalculNextCase 0x448f50, the step DeplaceEngin runs for path states 0/5 and moving units.

        With no pending offset (+0x86/+0x87), state 0 picks the direct step (EnginNextCase) and state
        5 the route step (EnginNextCaseChemin). Then, unless the reserved cell +0x7c is the current
        +8: the walk animation, RotateEngin when +0x91 != +0x90, the local-player sound test, and
        AvanceEngin when the orientation allows it.
        """
        p = indice * 276
        u = self.unidades
        if not u[p + 0x86] and not u[p + 0x87]:
            if u[p + 0x88] == 0:
                self.escolher_direto(indice)
            elif u[p + 0x88] == 5:
                self.escolher_da_rota(indice)
        if self.palavra(indice, 0x7c) == self.palavra(indice, 8):
            return
        self.animar_movimento(indice)
        if u[p + 0x91] != u[p + 0x90]:
            self.girar(indice)
        self._som_movimento(indice)
        if pode_avancar(u[p + 0x90], u[p + 0x91]):
            self.avancar_passo(indice)

    def deslocar(self, indice):
        """DeplaceEngin 0x44930c: the path-state switch on +0x88 (table 0x4492f0).

        States 0 and 5, and 3 with a pending offset, run CalculNextCase (``calcular_proxima_celula``);
        1, 3, 4 and 6 are ``atualizar_estado_caminho`` (3/4 need the path solver); 2 and above 6 do nothing.
        """
        p = indice * 276
        u = self.unidades
        estado = u[p + 0x88]
        if estado in (0, 5) or (estado == 3 and (u[p + 0x86] or u[p + 0x87])):
            self.calcular_proxima_celula(indice)
        elif estado in (1, 3, 4, 6):
            self.atualizar_estado_caminho(indice)

    def atualizar_movimento(self, indice, maquina=None, animacao=False):
        """DeplaceEngin's movement for state 2. With ``animacao=True`` it also runs CalculNextCase's walk
        animation and the local-player sound test (0x448fc3..0x4490fd); the default keeps the declared
        exclusion of continuous animation and sound used by the existing native pulse comparisons."""
        p = indice * 276
        u = self.unidades
        if self.viva(indice) and not self.concluir_movimento(indice) and u[p + 2] == 2:
            if self.palavra(indice, 8) == self.palavra(indice, 0x7e):
                if u[p + 0x90] != u[p + 0x91]:
                    self.girar(indice)
                return notificar_estado(self, indice, maquina)
            if self.atualizar_estado_caminho(indice) and self.palavra(indice, 8) != self.palavra(indice, 0x7c):
                if animacao:
                    self.animar_movimento(indice)
                if u[p + 0x90] != u[p + 0x91]:
                    self.girar(indice)
                if animacao:
                    self._som_movimento(indice)
                if pode_avancar(u[p + 0x90], u[p + 0x91]):
                    self.avancar_passo(indice)
        return notificar_estado(self, indice, maquina)
