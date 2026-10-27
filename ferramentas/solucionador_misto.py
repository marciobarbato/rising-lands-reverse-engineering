"""Busca com preparação, início/seleção dos candidatos e otimização em Python.

Backend experimental explícito. A referência SolucionadorOriginal continua
executando todas as funções originais, sem essa substituição.
"""
import struct
from emulador import RETORNO
from bancada_preparacao import gravar_preparacao, gravar_inicio_candidatos
from candidatos_rota import iniciar_candidatos, selecionar_candidato
from caminhos import serializar_rota
from otimizacao_caminhos import ContextoLinha, otimizar_rota
from preparacao_destino import preparar_destino
from solucionador_original import BancadaNavegacao, SolucionadorOriginal


class BancadaMista(BancadaNavegacao):
    def __init__(self):
        super().__init__()
        self.otimizacoes_python = []
        self.preparacoes_python = []
        self.inicios_candidatos_python = []
        self.escolhas_python = []

    def preparar_busca(self, mundo, indice):
        self.carregar_navegacao(mundo)
        p = preparar_destino(mundo, indice, mundo.palavra(indice, 8), mundo.palavra(indice, 0x7e))
        gravar_preparacao(self, p, self.grades['rotas'] + indice * 512)
        self.preparacoes_python.append(dict(unidade=indice, inicio=p.inicio, solicitado=p.solicitado,
                                            destino=p.destino, status=p.status, concluida=p.concluida))
        return self.calcular(mundo, indice)

    def calcular(self, mundo, indice):
        # Executa só o prólogo e as três guardas. A inspeção da vizinhança
        # e a inicialização dos dados/locais são feitas pela tradução Python.
        r = self.executar(0x42f214, self.intervalos, parada=(RETORNO, 0x42f247), limite_instrucoes=1000000)
        if r['EIP'] == 0x42f247:
            inicio, destino = struct.unpack('<HH', self.cpu.mem_read(0x4e0f44, 4))
            unidade = struct.unpack('<H', self.cpu.mem_read(0x496304, 2))[0]
            contexto = ContextoLinha(mundo, unidade, self.cpu.mem_read(0x4e0f48, 1)[0],
                                     self.cpu.mem_read(0x4e0f42, 1)[0], self.cpu.mem_read(0x4e0f41, 1)[0])
            mundo.permitir_aliados_parados = self.cpu.mem_read(0x4e1771, 1)[0]
            dados = iniciar_candidatos(contexto, inicio, destino)
            gravar_inicio_candidatos(self, dados, r['ESP'])
            self.inicios_candidatos_python.append(dict(unidade=unidade,
                                                        obstaculo_proximo=dados.obstaculo_proximo,
                                                        todos_bloqueados=dados.todos_bloqueados,
                                                        regioes=list(dados.regioes)))
            if dados.todos_bloqueados:
                rota = struct.unpack('<I', self.cpu.mem_read(0x4e0f3c, 4))[0]
                self.cpu.mem_write(rota, b'\0\0')
                self.cpu.mem_write(0x496302, b'\1')
                self.cpu.mem_write(0x4e0f37, b'\0')
                self.cpu.mem_write(0x4e0f4c, bytes([8]))
                r = self.retomar(0x43b300, self.intervalos, limite_instrucoes=1000000)
            else:
                r = self.retomar(0x430b7e, self.intervalos, parada=(RETORNO, 0x43b073), limite_instrucoes=1000000)
        if r['EIP'] == 0x43b073:
            buffers = tuple(bytes(self.cpu.mem_read(a, 512)) for a in (0x4e116a, 0x4e136a))
            custos = tuple(struct.unpack('<H', self.cpu.mem_read(r['ESP'] + off, 2))[0] for off in (0xec, 0x108))
            registros = tuple(bytes(self.cpu.mem_read(a, 10)) for a in (0x4e0f54, 0x4e0f5e))
            semente = struct.unpack('<I', self.cpu.mem_read(0x497164, 4))[0]
            escolha = selecionar_candidato(buffers, custos, registros, semente,
                                            status=self.cpu.mem_read(0x4e0f4c, 1)[0],
                                            flags=tuple(self.cpu.mem_read(0x4e0f34, 2)))
            for endereco, buffer in zip((0x4e116a, 0x4e136a), escolha.buffers): self.cpu.mem_write(endereco, buffer)
            self.cpu.mem_write(0x4e0f4c, bytes([escolha.status]))
            self.cpu.mem_write(0x497164, struct.pack('<I', escolha.semente))
            self.cpu.mem_write(0x496302, b'\1')
            self.cpu.mem_write(0x4e0f37, b'\1')
            self.escolhas_python.append(dict(custos=list(custos), escolhido=escolha.escolhido,
                                             status=escolha.status, motivo=escolha.motivo))
            unidade = struct.unpack('<H', self.cpu.mem_read(0x496304, 2))[0]
            contexto = ContextoLinha(mundo, unidade, self.cpu.mem_read(0x4e0f48, 1)[0],
                                     self.cpu.mem_read(0x4e0f42, 1)[0], self.cpu.mem_read(0x4e0f41, 1)[0])
            mundo.permitir_aliados_parados = self.cpu.mem_read(0x4e1771, 1)[0]
            ponteiro = (0x4e116a, 0x4e136a)[escolha.escolhido]
            antes = escolha.buffers[escolha.escolhido]
            depois = otimizar_rota(contexto, antes)
            self.cpu.mem_write(ponteiro, depois)
            self.cpu.mem_write(0x4e1771, bytes([mundo.permitir_aliados_parados]))
            self.otimizacoes_python.append(dict(unidade=unidade,
                                                celulas_antes=struct.unpack_from('<H', antes)[0],
                                                celulas_depois=struct.unpack_from('<H', depois)[0]))
            quantidade = struct.unpack_from('<H', depois)[0]
            celulas = struct.unpack_from('<' + 'H' * quantidade, depois, 2)
            saida = serializar_rota(celulas)
            rota = struct.unpack('<I', self.cpu.mem_read(0x4e0f3c, 4))[0]
            self.cpu.mem_write(rota, saida)
            self.retomar(0x43b300, self.intervalos, limite_instrucoes=1000000)
        return self.resultado(indice)


class SolucionadorParcialPython(SolucionadorOriginal):
    def __init__(self):
        self.bancada = BancadaMista()


# Mantém a API da etapa anterior; agora também traduz preparação e início.
SolucionadorComOtimizacaoPython = SolucionadorParcialPython
