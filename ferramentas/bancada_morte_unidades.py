"""Original SetDyingEngin and verified no-effect nested calls; never patched."""
from collections import Counter
from bancada_avanco import BancadaAvanco
from emulador import RETORNO


class BancadaMorteUnidades(BancadaAvanco):
    intervalos = BancadaAvanco.intervalos + [
        (0x444938, 0x444dad), (0x467d97, 0x467da6),
        (0x4829c8, 0x482a51), (0x482c50, 0x482c58), (0x482eb5, 0x482ebc),
        (0x48aac0, 0x48aac5), (0x48a438, 0x48a446),
        (0x472648, 0x47268b), (0x442045, 0x442064),
    ]

    def __init__(self):
        super().__init__()
        self.paradas_atingidas = Counter()

    def morrer(self, indice, parada=RETORNO):
        regs = self.executar(0x444938, self.intervalos, dict(EAX=indice), parada=parada,
                             limite_instrucoes=100000)
        self.paradas_atingidas[hex(regs['EIP'])] += 1
        return regs
