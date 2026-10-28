"""Original bonus producers, stopping before world-unit capacity refresh."""
from bancada_bonus_unidades import BancadaBonusUnidades, TRECHOS_BONUS
from emulador import RETORNO, unicorn, x86

TRECHOS_MUTACOES = TRECHOS_BONUS + [(0x428878, 0x428c8a), (0x428e71, 0x428eee),
                                   (0x428716, 0x42871a), (0x44230c, 0x442347)]


class BancadaMutacoesBonus(BancadaBonusUnidades):
    def __init__(self):
        super().__init__()
        self.paradas_capacidade = 0
        self.retornos = 0
        self.excecoes_esperadas = 0
        self.escritas_bonus = []
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._registrar_bonus)

    def _registrar_bonus(self, cpu, acesso, endereco, tamanho, valor, _):
        if 0x4dfb98 <= endereco < 0x4e0300:
            self.escritas_bonus.append((endereco, tamanho, valor & ((1 << (tamanho * 8)) - 1)))

    def carregar_mutacoes(self, b):
        self.carregar_bonus(b)
        self.cpu.mem_write(0x4965ae - 4, b'\xd5' * 4 + bytes(b.tipos_unidades) + b'\x5d' * 4)
        self.escritas_bonus.clear()

    def chamar_mutacao(self, entrada, jogador=0, tipo=0, seletor=0, valor=0):
        self.escritas_bonus.clear()
        regs = self.executar(entrada, TRECHOS_MUTACOES,
            dict(EAX=jogador, EBX=tipo, EDX=seletor, ECX=valor), parada={RETORNO, 0x4475ef})
        self.paradas_capacidade += regs['EIP'] == 0x4475ef
        self.retornos += regs['EIP'] == RETORNO
        return regs
