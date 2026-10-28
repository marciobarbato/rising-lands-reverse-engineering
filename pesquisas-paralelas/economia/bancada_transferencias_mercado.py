"""VideMatiere e dependências reais, com observação de chamadas e escritas."""
import struct

from bancada_construcoes import BancadaConstrucoes, TRECHOS
from bancada_mercado import JOGADORES, TRECHOS_MERCADO
from mercado import BUFFERS
from emulador import unicorn, x86

TRECHOS_TRANSFERENCIA = TRECHOS + TRECHOS_MERCADO + [(0x4663eb, 0x466533)]


class BancadaTransferenciasMercado(BancadaConstrucoes):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(JOGADORES - 0x100, 0x1000)
        self.cpu.mem_write(0x5080a8, struct.pack('<I', JOGADORES))
        self.eventos = []
        self.escritas = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_transferencia)
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._observar_escrita)

    def _observar_transferencia(self, cpu, endereco, tamanho, _):
        if endereco in (0x46d817, 0x4235bd, 0x46792c, 0x46769d, 0x4678f2, 0x42340f, 0x4676e5):
            r = {n: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n))
                 for n in ('EAX', 'EDX', 'EBX')}
            self.eventos.append(dict(entrada=endereco, **r))

    def _observar_escrita(self, cpu, acesso, endereco, tamanho, valor, _):
        if 0x400000 <= endereco < 0x600000 or JOGADORES - 8 <= endereco < JOGADORES + 88:
            self.escritas.append((cpu.reg_read(x86.UC_X86_REG_EIP), endereco, tamanho,
                                  valor & ((1 << (tamanho * 8)) - 1)))

    def carregar_transferencia(self, transferencia):
        m = transferencia.mercado
        self.carregar_mundo(transferencia.mundo)
        for nome, (endereco, _) in BUFFERS.items():
            self.cpu.mem_write(endereco, bytes(getattr(m, nome)))
        self.cpu.mem_write(JOGADORES - 8, b'\xc3' * 8 + bytes(m.jogadores) + b'\x3c' * 8)
        self.vizinhos_antes = bytes(self.cpu.mem_read(0x4e2900, 0x700))
        self.eventos.clear()
        self.escritas.clear()

    def chamar(self, entrada, eax, edx=0, registradores=None):
        self.eventos.clear()
        self.escritas.clear()
        self.chamadas.clear()
        regs = dict(registradores or {})
        regs.update(EAX=eax, EDX=edx)
        return self.executar(entrada, TRECHOS_TRANSFERENCIA, regs)

    def buffers_mercado(self):
        return {nome: bytes(self.cpu.mem_read(endereco, tamanho))
                for nome, (endereco, tamanho) in BUFFERS.items()}
