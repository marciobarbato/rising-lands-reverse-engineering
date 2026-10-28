"""Mercado no x86 original: entrada até RET, sem substituir dependências."""
import struct

from bancada_economia import BancadaEconomia, INTERVALOS
from emulador import unicorn, x86
from mercado import BUFFERS

JOGADORES = 0x1400100
TRECHOS_MERCADO = INTERVALOS + [
    (0x462a58, 0x462abd), (0x466bac, 0x466dd1), (0x4661d3, 0x4661da),
    (0x46d817, 0x46d877), (0x46dc6c, 0x46dc90),
]


class BancadaMercado(BancadaEconomia):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(JOGADORES - 0x100, 0x1000)
        self.cpu.mem_write(0x5080a8, struct.pack('<I', JOGADORES))
        self.excecoes_esperadas = 0
        self.acessos = []
        self.escritas = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar)
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._escrita)

    def _registrar(self, cpu, endereco, tamanho, _):
        if endereco in (0x46d817, 0x46d838, 0x46dc6c, 0x467670, 0x4676e5, 0x46792c, 0x4678f2):
            self.acessos.append((endereco, cpu.reg_read(x86.UC_X86_REG_EAX) & 255,
                                 cpu.reg_read(x86.UC_X86_REG_EDX) & 255))

    def _escrita(self, cpu, acesso, endereco, tamanho, valor, _):
        # Pilha é observada pela bancada comum; aqui rastreiam-se todas as
        # escritas na imagem PE e no buffer de jogadores, não só saídas esperadas.
        if 0x400000 <= endereco < 0x600000 or JOGADORES - 8 <= endereco < JOGADORES + 88:
            # Unicorn pode entregar os bits altos do registrador mesmo num MOV word.
            self.escritas.append((endereco, tamanho, valor & ((1 << (tamanho * 8)) - 1)))

    def carregar_mercado(self, mercado):
        self.carregar(mercado.economia.memoria)
        # Snapshot de um intervalo contínuo detecta escritas em lacunas e vizinhos
        # de tabelas adjacentes, onde guardas independentes se sobreporiam.
        for nome, (endereco, _) in BUFFERS.items():
            self.cpu.mem_write(endereco, bytes(getattr(mercado, nome)))
        self.cpu.mem_write(JOGADORES - 8, b'\xc3' * 8 + bytes(mercado.jogadores) + b'\x3c' * 8)
        self.antes = bytes(self.cpu.mem_read(0x4e2900, 0x600))
        self.acessos.clear()
        self.escritas.clear()

    def chamar(self, entrada, eax, edx=0, registradores=None):
        regs = dict(registradores or {})
        regs.update(EAX=eax, EDX=edx)
        return self.executar(entrada, TRECHOS_MERCADO, regs)

    def estado(self):
        return {nome: bytes(self.cpu.mem_read(endereco, tamanho))
                for nome, (endereco, tamanho) in BUFFERS.items()}
