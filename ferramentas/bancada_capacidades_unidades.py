"""Complete native capacity refresh, including original economic subcalls."""
from collections import Counter
from emulador import BancadaX86, UNIDADES, unicorn, x86


class BancadaCapacidadesUnidades(BancadaX86):
    intervalos = ((0x4475ef, 0x447676), (0x440d55, 0x440d5e),
                  (0x4475ac, 0x4475ef), (0x4474c5, 0x4474c7), (0x428cc0, 0x428e71))

    def __init__(self):
        super().__init__()
        self.consultas = []
        self.checkpoint = None
        self.paradas_atingidas = Counter()
        self.total_consultas = Counter()
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._consultar)

    def _consultar(self, cpu, endereco, tamanho, _):
        if self.checkpoint is not None and endereco == self.checkpoint[0]:
            indice = cpu.reg_read(x86.UC_X86_REG_ECX) & 65535
            if indice == self.checkpoint[1]:
                self.paradas.add(endereco)
                cpu.emu_stop()
                return
        if endereco == 0x4475ac:
            self.consultas.append(('capacity', cpu.reg_read(x86.UC_X86_REG_EAX) & 255))
            self.total_consultas['capacity'] += 1
        elif endereco == 0x428cc0:
            self.consultas.append(('bonus', cpu.reg_read(x86.UC_X86_REG_EAX) & 255,
                                   cpu.reg_read(x86.UC_X86_REG_EBX) & 255, 1))
            self.total_consultas['bonus'] += 1

    def carregar(self, unidades, bonus):
        self.cpu.mem_write(UNIDADES, bytes(unidades))
        self.cpu.mem_write(0x4dfba0, bytes(bonus))
        self.consultas = []

    def atualizar(self, jogador, checkpoint=None):
        self.checkpoint = checkpoint
        regs = self.executar(0x4475ef, self.intervalos, dict(EAX=jogador), limite_instrucoes=100000)
        self.paradas_atingidas[hex(regs['EIP'])] += 1
        return regs

    def unidades(self):
        return bytes(self.cpu.mem_read(UNIDADES, 220800))
