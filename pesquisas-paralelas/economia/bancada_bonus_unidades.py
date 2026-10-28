"""Complete original query bodies and dispatch data, without patches/callbacks."""
from bancada_economia import BancadaEconomia
from bonus_unidades import BASE_BONUS_UNIDADES, TAMANHO_BONUS_UNIDADES
from emulador import RETORNO

TRECHOS_BONUS = [(0x428cc0, 0x428e71), (0x4475ac, 0x4475ef), (0x4474c5, 0x4474c7)]


class BancadaBonusUnidades(BancadaEconomia):
    def carregar_bonus(self, bonus):
        self.cpu.mem_write(BASE_BONUS_UNIDADES - 8, b'\xa7' * 8 + bytes(bonus.memoria) + b'\x7a' * 8)
        self.antes = bytes(self.cpu.mem_read(BASE_BONUS_UNIDADES - 8, TAMANHO_BONUS_UNIDADES + 16))

    def consultar(self, jogador, tipo, seletor, ecx=0):
        return self.executar(0x428cc0, TRECHOS_BONUS,
            dict(EAX=jogador, EBX=tipo, EDX=seletor, ECX=ecx))

    def capacidade(self, tipo, edx=0):
        return self.executar(0x4475ac, TRECHOS_BONUS, dict(EAX=tipo, EDX=edx))

    def conferir_memoria(self):
        return bytes(self.cpu.mem_read(BASE_BONUS_UNIDADES - 8, TAMANHO_BONUS_UNIDADES + 16)) == self.antes
