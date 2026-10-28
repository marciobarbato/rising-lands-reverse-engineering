"""Original structure lifecycle bodies with explicit non-economic stops."""
from emulador import BancadaX86, RETORNO
from collections import Counter

REGISTROS = 0x49a0c8
REALIZAVEIS = 0x49a070
SELECOES = 0x495be0


class BancadaCicloEstruturas(BancadaX86):
    def __init__(self):
        super().__init__()
        self.paradas_atingidas = Counter()

    def _executar_ate_parada(self, entrada, limite_instrucoes):
        regs = super()._executar_ate_parada(entrada, limite_instrucoes)
        self.paradas_atingidas[hex(regs['EIP'])] += 1
        return regs

    def carregar(self, registros, realizaveis, selecoes):
        self.cpu.mem_write(REGISTROS, bytes(registros))
        self.cpu.mem_write(REALIZAVEIS, bytes(realizaveis))
        self.cpu.mem_write(SELECOES, bytes(selecoes))

    def ler(self):
        return tuple(bytes(self.cpu.mem_read(endereco, tamanho)) for endereco, tamanho in
                     ((REGISTROS, 276000), (REALIZAVEIS, 88), (SELECOES, 8)))

    def inicializar(self):
        return self.executar(0x418e95, [(0x418e95, 0x419004)], parada=0x419004,
                             limite_instrucoes=200000)

    def resetar_todas(self):
        return self.executar(0x41a75c, [(0x41a75c, 0x41a860)], limite_instrucoes=100000)

    def resetar(self, indice):
        return self.executar(0x41b9d6, [(0x41b9d6, 0x41ba49)], dict(EAX=indice))

    def buscar_livre(self):
        regs = self.executar(0x41fea2, [(0x41fea2, 0x41ff04), (0x4202c1, 0x4202ce)],
                             parada=(0x41ff04, RETORNO), limite_instrucoes=50000)
        return regs['EAX'] & 0xffff
