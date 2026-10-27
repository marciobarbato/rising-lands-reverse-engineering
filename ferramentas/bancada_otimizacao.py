"""Referência original de TestLigneOptimise/OptimiseChemin, sem substituições."""
import struct
from solucionador_original import BancadaNavegacao

CONTADOR = 0x1800000
BUFFER = 0x1801000


class BancadaOtimizacao(BancadaNavegacao):
    def carregar_contexto(self, contexto):
        self.carregar_navegacao(contexto.mundo)
        self.cpu.mem_write(0x496304, struct.pack('<H', contexto.unidade))
        for endereco, valor in ((0x4e0f48, contexto.classe), (0x4e0f42, contexto.mascara),
                                 (0x4e0f41, contexto.dono)):
            self.cpu.mem_write(endereco, bytes([valor]))

    def linha(self, origem, destino, buffer, contador=0xa5a5a5a5):
        self.cpu.mem_write(CONTADOR, struct.pack('<I', contador))
        self.cpu.mem_write(BUFFER, bytes(buffer))
        r = self.executar(0x42d674, self.intervalos,
                          dict(EAX=origem, EDX=destino, EBX=BUFFER, ECX=CONTADOR),
                          limite_instrucoes=1000000)
        return (bool(r['EAX'] & 255), struct.unpack('<I', self.cpu.mem_read(CONTADOR, 4))[0],
                bytes(self.cpu.mem_read(BUFFER, len(buffer))))

    def otimizar(self, buffer):
        self.cpu.mem_write(BUFFER, bytes(buffer))
        self.executar(0x42e890, self.intervalos, dict(EAX=BUFFER), limite_instrucoes=1000000)
        return bytes(self.cpu.mem_read(BUFFER, len(buffer)))
