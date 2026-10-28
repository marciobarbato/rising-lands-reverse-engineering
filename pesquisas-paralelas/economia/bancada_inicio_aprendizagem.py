"""Início, acessor de custos e término explícito da aprendizagem no x86."""
from bancada_aprendizagem import BancadaAprendizagem, TRECHOS_APRENDIZAGEM
from emulador import RETORNO, unicorn, x86

TRECHOS_INICIO_APRENDIZAGEM = TRECHOS_APRENDIZAGEM + [
    (0x422d9f, 0x422f08), (0x4746fe, 0x474734),
    (0x42399a, 0x4239a0), (0x421250, 0x4212f5),
]
SAIDAS_CUSTOS = 0x1200400


class BancadaInicioAprendizagem(BancadaAprendizagem):
    def __init__(self):
        super().__init__()
        self.acessos_inicio = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar_inicio)

    def _registrar_inicio(self, cpu, endereco, tamanho, _):
        if endereco in (0x4746fe, 0x4676e5):
            self.acessos_inicio.append(endereco)

    def chamar_inicio(self, entrada, eax=0, edx=0, registradores=None):
        regs = dict(registradores or {})
        regs.update(EAX=eax, EDX=edx)
        self.acessos_inicio.clear()
        self.acessos_aprendizagem.clear()
        self.chamadas.clear()
        return self.executar(entrada, TRECHOS_INICIO_APRENDIZAGEM, regs, parada=RETORNO)

    def custos(self, tipo):
        self.cpu.mem_write(SAIDAS_CUSTOS, b'\xa7' * 32)
        self.chamar_inicio(0x4746fe, tipo, SAIDAS_CUSTOS + 4,
                           dict(EBX=SAIDAS_CUSTOS + 12, ECX=SAIDAS_CUSTOS + 20))
        return bytes(self.cpu.mem_read(SAIDAS_CUSTOS, 32))
