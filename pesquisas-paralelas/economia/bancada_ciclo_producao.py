"""Full CalculTroupe entry for shared production branches plus real exit prefix."""
from bancada_producao import BancadaProducao, TRECHOS_PRODUCAO
from bancada_saida_tropa import TRECHOS_SAIDA_TROPA
from emulador import RETORNO, unicorn, x86
from producao import CONTROLE_X87_INICIAL

TRECHOS_CICLO = TRECHOS_PRODUCAO + TRECHOS_SAIDA_TROPA + [
    (0x4259e6, 0x425c4e), (0x4263e5, 0x426418), (0x41db1d, 0x41db24),
    (0x41a4c4, 0x41a513), (0x41f3ed, 0x41f46e),
]


class BancadaCicloProducao(BancadaProducao):
    def __init__(self):
        super().__init__()
        self.saidas_tropa = []
        self.retornos = 0
        self.paradas_posicao = 0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar_ciclo)

    def _registrar_ciclo(self, cpu, endereco, tamanho, _):
        if endereco == 0x420e4c:
            self.saidas_tropa.append((cpu.reg_read(x86.UC_X86_REG_EAX) & 65535,
                                      cpu.reg_read(x86.UC_X86_REG_EDX) & 255))

    def calcular(self, indice, registradores=None):
        self.saidas_tropa.clear()
        self.cpu.reg_write(x86.UC_X86_REG_FPCW, CONTROLE_X87_INICIAL)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW, 0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG, 0xffff)
        regs = dict(registradores or {})
        regs['EAX'] = indice
        r = self.executar(0x4259e6, TRECHOS_CICLO, regs, parada={RETORNO, 0x420698, 0x41dde0},
                          limite_instrucoes=1000000)
        self.retornos += r['EIP'] == RETORNO
        self.paradas_posicao += r['EIP'] == 0x420698
        return r
