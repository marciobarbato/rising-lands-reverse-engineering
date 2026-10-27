"""Bancada das ordens de movimento, com chamadas originais e memória sintética."""
import struct
from bancada_tarefas import BancadaTarefas, INTERVALOS
from emulador import UNIDADES
from ordens_unidades import BASE_GRUPOS

OBJETOS = 0x1300000
ARGUMENTOS = 0x1310000
BASE_ESTRUTURAS = 0x49a0c8
INTERVALOS_ORDENS = [
    (0x481110, 0x481173), (0x440e11, 0x440e31), (0x442025, 0x442045),
    (0x443dad, 0x443ddd), (0x44357c, 0x443688),
    (0x4457d3, 0x445947), (0x445f27, 0x445f2d),
    (0x47610f, 0x476134), (0x4237ff, 0x42381f),
    (0x420c7c, 0x420cae), (0x41a65c, 0x41a67d),
    (0x481f4c, 0x481fb4), (0x481e46, 0x481e4f),
    (0x4837f0, 0x483867),
]


class BancadaOrdens(BancadaTarefas):
    intervalos = INTERVALOS + INTERVALOS_ORDENS

    def __init__(self):
        super().__init__()
        self.cpu.mem_map(OBJETOS, 0x11000)
        self.cpu.mem_write(0x507d74, struct.pack('<I', OBJETOS))

    def carregar_mundo(self, mundo):
        self.cpu.mem_write(UNIDADES, bytes(mundo.unidades))
        self.cpu.mem_write(BASE_ESTRUTURAS, bytes(mundo.estruturas))
        self.cpu.mem_write(BASE_GRUPOS, bytes(mundo.grupos))
        self.cpu.mem_write(OBJETOS, bytes(mundo.objetos))
        for endereco, formato, valor in [
            (0x496304, 'H', mundo.busca.unidade),
            (0x4e0f36, 'B', mundo.busca.ocupada),
            (0x4e0f37, 'B', mundo.busca.sucesso),
            (0x4e0f3c, 'I', mundo.busca.ponteiro_rota),
            (0x496302, 'B', mundo.busca.concluida),
            (0x51b844, 'I', mundo.grupo_em_iteracao),
            (0x51b848, 'H', mundo.unidade_em_iteracao),
        ]:
            self.cpu.mem_write(endereco, struct.pack('<' + formato, valor))

    def chamar(self, nome, argumentos):
        if nome in ('ResetOrdre', 'SetDeplaceEngin'):
            registradores = dict(EAX=argumentos[0], EDX=argumentos[1] if len(argumentos) > 1 else 0)
        else:
            self.cpu.mem_write(ARGUMENTOS, struct.pack('<' + 'I' * len(argumentos), *(a & 0xffffffff for a in argumentos)))
            registradores = dict(EAX=ARGUMENTOS)
        return self.executar(self.simbolos[nome], self.intervalos, registradores)['EAX']

    def conferir_mundo(self, mundo):
        """Retorna diferenças observáveis; o chamador decide como reportá-las."""
        diferencas = []
        for nome, endereco, esperado in [('unidades', UNIDADES, mundo.unidades),
                                         ('estruturas', BASE_ESTRUTURAS, mundo.estruturas),
                                         ('grupos', BASE_GRUPOS, mundo.grupos),
                                         ('objetos', OBJETOS, mundo.objetos)]:
            atual = bytes(self.cpu.mem_read(endereco, len(esperado)))
            if atual != bytes(esperado):
                offsets = [i for i, (a, b) in enumerate(zip(atual, esperado)) if a != b]
                diferencas.append(dict(regiao=nome, primeiros_offsets=offsets[:12], quantidade=len(offsets)))
        for nome, endereco, formato, esperado in [
            ('busca_unidade', 0x496304, 'H', mundo.busca.unidade),
            ('busca_ocupada', 0x4e0f36, 'B', mundo.busca.ocupada),
            ('busca_sucesso', 0x4e0f37, 'B', mundo.busca.sucesso),
            ('busca_ponteiro', 0x4e0f3c, 'I', mundo.busca.ponteiro_rota),
            ('busca_concluida', 0x496302, 'B', mundo.busca.concluida),
            ('grupo_iteracao', 0x51b844, 'I', mundo.grupo_em_iteracao),
            ('unidade_iteracao', 0x51b848, 'H', mundo.unidade_em_iteracao),
        ]:
            atual = struct.unpack('<' + formato, self.cpu.mem_read(endereco, struct.calcsize(formato)))[0]
            if atual != esperado:
                diferencas.append(dict(campo=nome, atual=atual, esperado=esperado))
        return diferencas
