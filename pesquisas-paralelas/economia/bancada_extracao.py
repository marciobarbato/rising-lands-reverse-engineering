"""Referência de extração/regeneração executando bytes originais, sem mocks."""
import struct

from bancada_construcoes import BancadaConstrucoes, TRECHOS, TIPOS, QUANTIDADES
from extracao import BASE_MINAS

MOSAICOS = 0x1501000
ATRIBUTOS = 0x1531000
TRECHOS_EXTRACAO = TRECHOS + [
    (0x475328, 0x47534a), (0x47544c, 0x475620),
    (0x476662, 0x4766b1), (0x4781e8, 0x478a01),
]


class BancadaExtracao(BancadaConstrucoes):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(MOSAICOS - 0x1000, 0x42000)
        self.cpu.mem_write(0x507d70, struct.pack('<I', MOSAICOS))
        self.cpu.mem_write(0x507da8, struct.pack('<I', ATRIBUTOS))

    def carregar_extracao(self, mundo, recursos):
        if recursos.terreno is not mundo.terreno:
            raise ValueError('A bancada exige o mesmo terreno nos dois modelos')
        self.carregar_mundo(mundo)
        self.cpu.mem_write(BASE_MINAS - 4, b'\xa7' * 4 + bytes(recursos.minas) + b'\x7a' * 8)
        self.cpu.mem_write(0x509952, bytes([recursos.atualizar]))
        self.cpu.mem_write(0x4973e4, b'\x6d' * 4 + struct.pack('<HH', recursos.linha, recursos.periodo) + b'\xd6' * 4)
        self.cpu.mem_write(0x508f78, b'\x3e' * 4 + struct.pack('<I', recursos.tempo) + b'\xe3' * 4)
        for base, bloco in ((MOSAICOS, recursos.mosaicos), (ATRIBUTOS, recursos.atributos)):
            self.cpu.mem_write(base - 8, b'\xa1' * 8 + bytes(bloco) + b'\x1a' * 8)
        self.cpu.mem_write(TIPOS - 8, b'\xb2' * 8)
        self.cpu.mem_write(QUANTIDADES + 65536, b'\x2b' * 8)

    def estado_extracao(self):
        return dict(minas=bytes(self.cpu.mem_read(BASE_MINAS, 80)),
                    mosaicos=bytes(self.cpu.mem_read(MOSAICOS, 131072)),
                    atributos=bytes(self.cpu.mem_read(ATRIBUTOS, 65536)),
                    linha=struct.unpack('<H', self.cpu.mem_read(0x4973e8, 2))[0],
                    periodo=struct.unpack('<H', self.cpu.mem_read(0x4973ea, 2))[0],
                    tempo=struct.unpack('<I', self.cpu.mem_read(0x508f7c, 4))[0],
                    atualizar=self.cpu.mem_read(0x509952, 1)[0])

    def guardas_extracao(self):
        posicoes = [(BASE_MINAS - 4, 2), (BASE_MINAS - 1, 1), (BASE_MINAS + 80, 8),
                    (0x4973e4, 4), (0x4973ec, 4), (0x508f78, 4), (0x508f80, 4),
                    (MOSAICOS - 8, 8), (MOSAICOS + 131072, 8),
                    (ATRIBUTOS - 8, 8), (ATRIBUTOS + 65536, 8),
                    (TIPOS - 8, 8), (QUANTIDADES + 65536, 8)]
        return tuple(bytes(self.cpu.mem_read(a, n)) for a, n in posicoes)

    def chamar(self, entrada, eax=0, edx=0, registradores=None):
        regs = dict(registradores or {})
        regs.update(EAX=eax, EDX=edx)
        return self.executar(entrada, TRECHOS_EXTRACAO, regs, limite_instrucoes=1000000)
