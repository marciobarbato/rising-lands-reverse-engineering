"""Adaptador local para a bancada x86 existente, lida sem alterações.

Não inicia o Windows, não intercepta chamadas internas e não usa o Ghidra.
"""
import struct
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA.parents[1] / 'ferramentas'))
from emulador import BancadaX86
from economia import BASE_RECURSOS

SAIDAS = 0x1200000
ARGUMENTOS = SAIDAS + 0x100
INTERVALOS = [
    (0x467640, 0x467718), (0x4678f2, 0x4679d0),
    (0x4410d2, 0x441108), (0x41aace, 0x41ab04),
    (0x45d753, 0x45d80d), (0x481372, 0x481426), (0x485fb9, 0x485ff9),
]


class BancadaEconomia(BancadaX86):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(SAIDAS, 0x1000)

    def carregar(self, memoria):
        if len(memoria) != 128:
            raise ValueError('Tabela deve ter 128 bytes')
        self.cpu.mem_write(BASE_RECURSOS - 16, b'\xa6' * 16 + bytes(memoria) + b'\x6a' * 16)

    def memoria(self):
        return bytes(self.cpu.mem_read(BASE_RECURSOS, 128))

    def guardas(self):
        return (bytes(self.cpu.mem_read(BASE_RECURSOS - 16, 16)),
                bytes(self.cpu.mem_read(BASE_RECURSOS + 128, 16)))

    def mutacao(self, entrada, jogador, recurso, quantidade):
        self.executar(entrada, INTERVALOS, dict(EAX=recurso, EBX=jogador, EDX=quantidade))

    def consulta(self, entrada, jogador):
        self.cpu.mem_write(SAIDAS, b'\xa5' * 16)
        self.executar(entrada, INTERVALOS,
                      dict(EAX=SAIDAS, EDX=SAIDAS + 4, EBX=SAIDAS + 8, ECX=SAIDAS + 12),
                      pilha={4: struct.pack('<I', jogador & 0xffffffff)})
        bruto = bytes(self.cpu.mem_read(SAIDAS, 16))
        return tuple(struct.unpack_from('<H', bruto, i)[0] for i in (0, 4, 8, 12)), bruto

    def suficiente(self, jogador, comida, pedra, pecas):
        r = self.executar(0x4676e5, INTERVALOS, dict(EAX=comida, EDX=pedra, EBX=pecas),
                          pilha={4: struct.pack('<I', jogador & 0xffffffff)})
        return bool(r['EAX'] & 0xff)

    def operacao_ia(self, entrada, jogador, indice, limiar):
        self.cpu.mem_write(ARGUMENTOS, struct.pack('<8I', indice, limiar & 0xffffffff,
                                                  0, 0, 0, 0, 0, jogador))
        r = self.executar(entrada, INTERVALOS, dict(EAX=ARGUMENTOS))
        return r['EAX'] if r['EAX'] < 0x80000000 else r['EAX'] - 0x100000000

    def riqueza(self, jogador):
        return self.executar(0x485fb9, INTERVALOS, dict(EAX=jogador))['EAX']

    def custos(self, entrada, tipo):
        self.cpu.mem_write(SAIDAS, b'\xa5' * 16)
        self.executar(entrada, INTERVALOS,
                      dict(EAX=tipo, EDX=SAIDAS, EBX=SAIDAS + 4, ECX=SAIDAS + 8))
        bruto = bytes(self.cpu.mem_read(SAIDAS, 16))
        return tuple(struct.unpack_from('<H', bruto, i)[0] for i in (0, 4, 8)) + (0,)

    def necessario(self, entrada, jogador, tipo):
        return self.executar(entrada, INTERVALOS, dict(EAX=tipo, EDX=jogador))['EAX'] & 0xff
