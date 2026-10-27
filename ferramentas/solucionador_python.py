"""Busca independente para as classes 1..3: sem EXE, Unicorn ou JIT.

Usa as traduções de preparação, contorno, seleção e otimização. Recusa estruturas
codificadas e ordens de desbloqueio a aliados.
"""
import struct
from candidatos_rota import iniciar_candidatos, selecionar_candidato
from caminhos import serializar_rota
from contornos_caminhos import construir_contornos, vizinha_contorno
from movimento import direcao_entre_celulas
from otimizacao_caminhos import ContextoLinha, otimizar_rota
from passagem_unidades import procurar_ocupante
from preparacao_destino import preparar_destino


class SolucionadorCaminhosPython:
    def __init__(self, identificadores_rotas=None):
        # A simulação não desreferencia esse campo. Por padrão usa IDs lógicos;
        # a comparação x86 pode fornecer os endereços da memória sintética.
        self.identificadores_rotas = tuple(identificadores_rotas or range(1, 801))
        if len(self.identificadores_rotas) != 800:
            raise ValueError('São necessários 800 identificadores de rota')
        self.buffers = (bytes(512), bytes(512))
        self.regioes = bytes(510)
        self.registros = (bytes(10), bytes(10))
        self.inicio_calculado = self.destino_calculado = 0
        self.preparacoes_python = []
        self.inicios_candidatos_python = []
        self.contornos_python = []
        self.escolhas_python = []
        self.otimizacoes_python = []
        self._resultado = None

    def iniciar(self, mundo, indice):
        contexto = ContextoLinha.da_unidade(mundo, indice)
        if contexto.classe not in (1, 2, 3):
            raise NotImplementedError('Busca independente disponível para classes 1..3')
        if any(v & 0x8000 for v in mundo.regioes):
            raise NotImplementedError('Busca com estruturas exige a grade auxiliar de cores')
        if len(mundo.rotas[indice]) != 512:
            raise ValueError('A rota da unidade deve ter 512 bytes')
        p = preparar_destino(mundo, indice, mundo.palavra(indice, 8), mundo.palavra(indice, 0x7e))
        self.preparacoes_python.append(dict(unidade=indice, inicio=p.inicio, solicitado=p.solicitado,
                                            destino=p.destino, status=p.status, concluida=p.concluida))
        rota = bytearray(mundo.rotas[indice])
        struct.pack_into('<H', rota, 0, 0)
        status, sucesso, semente = p.status, p.sucesso, mundo.semente_caminhos
        if p.registrar_extremos:
            self.inicio_calculado, self.destino_calculado = p.inicio, p.destino
            dados = iniciar_candidatos(contexto, p.inicio, p.destino)
            self.inicios_candidatos_python.append(dict(unidade=indice, obstaculo_proximo=dados.obstaculo_proximo,
                                                        todos_bloqueados=dados.todos_bloqueados, regioes=list(dados.regioes)))
            contorno = construir_contornos(contexto, dados, self.buffers, self.regioes, self.registros)
            self.buffers, self.regioes, self.registros = contorno.buffers, contorno.regioes, contorno.registros
            self.contornos_python.append(dict(unidade=indice, custos=list(contorno.custos),
                                              contagens=[struct.unpack_from('<H', b)[0] for b in contorno.buffers]))
            if contorno.status_falha is not None:
                status, sucesso = contorno.status_falha, 0
            else:
                escolha = selecionar_candidato(self.buffers, contorno.custos, self.registros, semente,
                                                status=status, flags=(p.flag_unidades, p.flag_estruturas))
                self.buffers, semente, status = escolha.buffers, escolha.semente, escolha.status
                self.escolhas_python.append(dict(custos=list(contorno.custos), escolhido=escolha.escolhido,
                                                 status=status, motivo=escolha.motivo))
                antes = self.buffers[escolha.escolhido]
                depois = otimizar_rota(contexto, antes)
                novos = list(self.buffers)
                novos[escolha.escolhido] = depois
                self.buffers = tuple(novos)
                quantidade = struct.unpack_from('<H', depois)[0]
                celulas = struct.unpack_from('<' + 'H' * quantidade, depois, 2)
                serializada = serializar_rota(celulas)
                rota[:len(serializada)] = serializada
                self.otimizacoes_python.append(dict(unidade=indice, celulas_antes=struct.unpack_from('<H', antes)[0],
                                                    celulas_depois=quantidade))
                sucesso = 1
        self._resultado = dict(buffer_rota=bytes(rota),
                               contexto=dict(unidade=indice, ocupada=1, sucesso=sucesso,
                                             ponteiro_rota=self.identificadores_rotas[indice], concluida=1),
                               status=status, destino_alternativo=p.alternativa,
                               destino_calculado=self.destino_calculado, semente=semente)
        return self._resultado

    def continuar(self, mundo, indice):
        if self._resultado is None or self._resultado['contexto']['unidade'] != indice:
            raise RuntimeError('Não existe busca iniciada para essa unidade')
        return self._resultado

    def desbloquear(self, mundo, indice):
        d = direcao_entre_celulas(mundo.palavra(indice, 8), mundo.palavra(indice, 0x7e))
        for tentativa in range(3):
            c = vizinha_contorno(mundo, mundo.palavra(indice, 8), d)
            if c != 0xffff:
                outro = procurar_ocupante(mundo, c)
                if (outro != 0xffff and mundo.unidades[outro * 276] == mundo.unidades[indice * 276] and
                        mundo.palavra(outro, 8) == mundo.palavra(outro, 0x7e)):
                    raise NotImplementedError('Ordenar deslocamento a um aliado bloqueador ainda exige o original')
            d = ((d - 3) % 16) + 1 if tentativa == 0 else ((d + 1) % 16) + 1
        mundo.unidades[indice * 276 + 0x88], mundo.unidades[indice * 276 + 0x8b] = 1, 0
        return dict(desbloqueou=False)
