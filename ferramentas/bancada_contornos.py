"""Corpo original de contorno, parado antes da seleção dos candidatos."""
import struct
from bancada_preparacao import BancadaPreparacao


class BancadaContornos(BancadaPreparacao):
    def contornar_original(self, mundo, indice, inicio, destino):
        self.preparar_original(mundo, indice, inicio, destino)
        anteriores = tuple(bytes(self.cpu.mem_read(a, 512)) for a in (0x4e116a, 0x4e136a))
        residuos = bytes(self.cpu.mem_read(0x4e0f6a, 510))
        registros = tuple(bytes(self.cpu.mem_read(a, 10)) for a in (0x4e0f54, 0x4e0f5e))
        r = self.executar(0x42f214, self.intervalos, parada=(0x43b073, 0x43b300), limite_instrucoes=1000000)
        ler = self.cpu.mem_read
        return dict(custos=tuple(struct.unpack('<H', ler(r['ESP'] + off, 2))[0] for off in (0xec, 0x108)),
                    buffers=tuple(bytes(ler(a, 512)) for a in (0x4e116a, 0x4e136a)),
                    registros=tuple(bytes(ler(a, 10)) for a in (0x4e0f54, 0x4e0f5e)),
                    regioes=bytes(ler(0x4e0f6a, 510)), quantidade_regioes=ler(0x4e0f68, 1)[0],
                    fase=ler(0x4e0f40, 1)[0],
                    status_falha=ler(0x4e0f4c, 1)[0] if r['EIP'] == 0x43b300 else None), anteriores, residuos, registros
