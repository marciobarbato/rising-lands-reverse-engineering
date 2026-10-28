"""Unpatched original prefix, with a real dependency stop before CalculPosition."""
from bancada_recrutamento import BancadaRecrutamento, TRECHOS_RECRUTAMENTO
from emulador import RETORNO, unicorn, x86

TRECHOS_SAIDA_TROPA = TRECHOS_RECRUTAMENTO + [
    (0x420e4c, 0x420f5f), (0x4211ea, 0x4211f2), (0x42399a, 0x4239a0),
    (0x44719c, 0x44724a), (0x4472ea, 0x4473cf), (0x4474a6, 0x4474c7),
]


class BancadaSaidaTropa(BancadaRecrutamento):
    def __init__(self):
        super().__init__()
        self.depositos_saida = []
        self.paradas_posicao = 0
        self.retornos_antecipados = 0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar_saida)

    def _registrar_saida(self, cpu, endereco, tamanho, _):
        if endereco == 0x42340f:
            self.depositos_saida.append(tuple(cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n)) & mask
                for n, mask in (('EBX', 255), ('EAX', 255), ('EDX', 65535), ('ECX', 65535))))

    def preparar(self, indice, direcao):
        self.depositos_saida.clear()
        resultado = self.executar(0x420e4c, TRECHOS_SAIDA_TROPA,
            dict(EAX=indice, EDX=direcao), parada={RETORNO, 0x420698, 0x41dde0},
            limite_instrucoes=1000000)
        self.retornos_antecipados += resultado['EIP'] == RETORNO
        self.paradas_posicao += resultado['EIP'] == 0x420698
        self.paradas_dependencia += resultado['EIP'] == 0x41dde0
        return resultado
