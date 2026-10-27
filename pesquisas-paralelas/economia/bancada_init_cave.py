"""Executa BatimentInitCave e seu epílogo original, sem substituir chamadas."""
from bancada_construcoes import BancadaConstrucoes, TRECHOS
from construcoes import (BASE_CONTAGENS_TIPOS, BASE_CONTAGENS_TIPO18,
                         BASE_CONSTRUCOES, TOTAL_CONSTRUCOES, PASSO_CONSTRUCAO)

TRECHOS_INIT_CAVE = TRECHOS + [(0x419112, 0x4191c9), (0x41db1e, 0x41db24)]


class BancadaInitCave(BancadaConstrucoes):
    def carregar_mundo(self, mundo):
        if len(mundo.estruturas) != TOTAL_CONSTRUCOES * PASSO_CONSTRUCAO:
            raise ValueError('A bancada de InitCave exige 1000 estruturas')
        super().carregar_mundo(mundo)
        # A tabela de contagens acaba exatamente onde começam as estruturas:
        # a guarda anterior de BancadaConstrucoes seria sobrescrita legitimamente.
        self.cpu.mem_write(BASE_CONTAGENS_TIPOS - 8, b'\x8b' * 8 + bytes(mundo.contagens_por_tipo))
        self.cpu.mem_write(BASE_CONTAGENS_TIPO18, bytes(mundo.contagens_tipo18) + b'\x4d' * 4)

    def estado(self):
        estado = super().estado()
        estado.update(contagens_por_tipo=bytes(self.cpu.mem_read(BASE_CONTAGENS_TIPOS, 88)),
                      contagens_tipo18=bytes(self.cpu.mem_read(BASE_CONTAGENS_TIPO18, 4)))
        return estado

    def guardas_contagens(self):
        return (bytes(self.cpu.mem_read(BASE_CONTAGENS_TIPOS - 8, 8)),
                bytes(self.cpu.mem_read(BASE_CONTAGENS_TIPO18 + 4, 4)),
                bytes(self.cpu.mem_read(BASE_CONSTRUCOES + self.tamanho_estruturas, 8)))

    def inicializar_armazens(self, registradores=None):
        return self.executar(0x419112, TRECHOS_INIT_CAVE, registradores,
                             limite_instrucoes=1000000)
