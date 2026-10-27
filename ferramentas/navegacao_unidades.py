"""Desvios locais e estados de caminho ligados ao avanço físico.

O cálculo geral é fornecido por um backend explícito. SolucionadorOriginal usa
os bytes originais em Unicorn; SolucionadorCaminhosPython executa as traduções
das classes 1..3 sem emulação, com limites para estruturas e desbloqueios.
"""
import struct
from avanco_unidades import MundoFisico
from movimento import direcao_entre_celulas, celula_vizinha, pode_avancar
from caminhos import proxima_celula, atualizar_espera
from passagem_unidades import consultar_passagem
from mensagens_chegada import notificar_estado
from regioes_mapa import reconstruir_regioes


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

    def refazer_regioes(self):
        """Reconstrói rótulos e reaplica ocupação; usar antes de executar a busca."""
        regioes, atributos, quantidade = reconstruir_regioes(self.atributos, self.tiles, self.objetos,
                                                             self.marcadores_obstaculos_tiles, self.largura, self.altura)
        self.regioes, self.atributos = regioes, atributos
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
                # O backend original conserva esse ramo e devolve as unidades alteradas.
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

    def atualizar_movimento(self, indice, maquina=None):
        p = indice * 276
        u = self.unidades
        if self.viva(indice) and not self.concluir_movimento(indice) and u[p + 2] == 2:
            if self.palavra(indice, 8) == self.palavra(indice, 0x7e):
                if u[p + 0x90] != u[p + 0x91]:
                    self.girar(indice)
                return notificar_estado(self, indice, maquina)
            if self.atualizar_estado_caminho(indice) and self.palavra(indice, 8) != self.palavra(indice, 0x7c):
                if u[p + 0x90] != u[p + 0x91]:
                    self.girar(indice)
                if pode_avancar(u[p + 0x90], u[p + 0x91]):
                    self.avancar_passo(indice)
        return notificar_estado(self, indice, maquina)
