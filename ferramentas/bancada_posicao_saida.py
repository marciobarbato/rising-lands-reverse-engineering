"""Complete original CalculPosition, including both shared epilogues."""
from emulador import BancadaX86
import struct

REGISTROS = 0x49a0c8


class BancadaPosicaoSaida(BancadaX86):
    intervalos = ((0x420698, 0x420ba5), (0x41dbe5, 0x41dbed), (0x41db1e, 0x41db24))

    def carregar(self, registros):
        self.cpu.mem_write(REGISTROS, bytes(registros))

    def dimensoes(self, tipo, largura, altura):
        self.cpu.mem_write(0x495d8c + tipo * 52, struct.pack('<HH', largura, altura))

    def calcular(self, indice, direcao):
        return self.executar(0x420698, self.intervalos, dict(EAX=indice, EBX=direcao))['EAX'] & 65535

    def registros(self):
        return bytes(self.cpu.mem_read(REGISTROS, 276000))
