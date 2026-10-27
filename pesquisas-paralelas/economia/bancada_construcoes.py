"""Rotinas econômicas de construções executadas no x86 original, sem mocks.

O ramo que exige BatimentRetireColon para na entrada dessa dependência.
Ganchos adicionais apenas registram argumentos; não alteram o fluxo da CPU.
"""
import struct

from bancada_economia import BancadaEconomia, INTERVALOS
from construcoes import BASE_CAPACIDADES, BASE_CONSTRUCOES
from emulador import PILHA, RETORNO, unicorn, x86

TIPOS = 0x1301000
QUANTIDADES = 0x1311000
TRECHOS = INTERVALOS + [
    (0x42340f, 0x4235bd), (0x4470d2, 0x447107),
    (0x4235bd, 0x423643), (0x423355, 0x4233d8), (0x423025, 0x42302d),
    (0x4757af, 0x475bfe), (0x47605d, 0x4760f3),
    (0x4761a9, 0x4761d4), (0x4704dc, 0x470520), (0x475763, 0x4757af),
]


class BancadaConstrucoes(BancadaEconomia):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(TIPOS - 0x1000, 0x22000)
        self.cpu.mem_write(0x507d74, struct.pack('<I', TIPOS))
        self.cpu.mem_write(0x507dac, struct.pack('<I', QUANTIDADES))
        self.chamadas = []
        self.sujeira_pilha = None
        self.excecoes_esperadas = 0
        self.limites_esperados = 0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar)

    def _registrar(self, cpu, endereco, tamanho, _):
        if endereco in (0x4678f2, 0x46792c, 0x46769d, 0x4761a9, 0x4757af, 0x41dde0):
            r = {n: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n)) for n in ('EAX', 'EDX', 'EBX', 'ECX')}
            if endereco == 0x46769d:
                esp = cpu.reg_read(x86.UC_X86_REG_ESP)
                r['jogador_pilha'] = cpu.mem_read(esp + 4, 1)[0]
            self.chamadas.append(dict(entrada=endereco, **r))

    def _executar_ate_parada(self, entrada, limite_instrucoes):
        if self.sujeira_pilha is not None:
            self.cpu.mem_write(PILHA + 0x7000, bytes([self.sujeira_pilha]) * 0x1000)
        return super()._executar_ate_parada(entrada, limite_instrucoes)

    def carregar_mundo(self, mundo):
        self.carregar(mundo.economia.memoria)
        self.cpu.mem_write(BASE_CAPACIDADES - 8, b'\xc7' * 8 + bytes(mundo.capacidades.memoria) + b'\x7c' * 8)
        self.tamanho_estruturas = len(mundo.estruturas)
        self.cpu.mem_write(BASE_CONSTRUCOES - 8, b'\xe9' * 8 + bytes(mundo.estruturas) + b'\x9e' * 8)
        self.cpu.mem_write(TIPOS, bytes(mundo.terreno.tipos))
        self.cpu.mem_write(QUANTIDADES, bytes(mundo.terreno.quantidades))
        self.cpu.mem_write(0x497164, struct.pack('<I', mundo.terreno.semente))
        self.cpu.mem_write(0x498db4, struct.pack('<I', 0x12345678))
        self.chamadas.clear()

    def estado(self):
        return dict(economia=self.memoria(), capacidades=bytes(self.cpu.mem_read(BASE_CAPACIDADES, 24)),
                    estruturas=bytes(self.cpu.mem_read(BASE_CONSTRUCOES, self.tamanho_estruturas)),
                    tipos=bytes(self.cpu.mem_read(TIPOS, 65536)),
                    quantidades=bytes(self.cpu.mem_read(QUANTIDADES, 65536)),
                    semente=struct.unpack('<I', self.cpu.mem_read(0x497164, 4))[0])

    def outras_guardas(self):
        return (bytes(self.cpu.mem_read(BASE_CAPACIDADES - 8, 8)),
                bytes(self.cpu.mem_read(BASE_CAPACIDADES + 24, 8)),
                bytes(self.cpu.mem_read(BASE_CONSTRUCOES - 8, 8)),
                bytes(self.cpu.mem_read(BASE_CONSTRUCOES + self.tamanho_estruturas, 8)),
                struct.unpack('<I', self.cpu.mem_read(0x498db4, 4))[0])

    def adicionar(self, jogador, recurso, quantidade, indice):
        return self.executar(0x42340f, TRECHOS,
                              dict(EAX=recurso, EDX=quantidade, EBX=jogador, ECX=indice),
                              parada={RETORNO, 0x41dde0}, limite_instrucoes=1000000)

    def retirar(self, jogador, recurso, quantidade):
        return self.executar(0x4235bd, TRECHOS, dict(EAX=recurso, EDX=quantidade, EBX=jogador))

    def recalcular_recursos(self, jogador):
        return self.executar(0x423355, TRECHOS, dict(EAX=jogador))

    def procurar(self, celula, tipo):
        return self.executar(0x4757af, TRECHOS, dict(EAX=celula, EDX=tipo))['EAX'] & 65535

    def criar(self, celula, recurso):
        return self.executar(0x47605d, TRECHOS, dict(EAX=celula, EDX=recurso))

    def depositar(self, celula, recurso, quantidade):
        return self.executar(0x4761a9, TRECHOS, dict(EAX=celula, EDX=recurso, EBX=quantidade),
                              limite_instrucoes=1000000)
