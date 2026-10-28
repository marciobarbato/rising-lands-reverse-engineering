"""Execução integral de ConstruitPerso/Sort e BagContient modo 1 no original."""
import struct

from bancada_recrutamento import BancadaRecrutamento, TRECHOS_RECRUTAMENTO
from construcoes import BASE_CONSTRUCOES
from emulador import RETORNO, unicorn, x86
from producao import BASE_TIPOS_CONSTRUCOES, BASE_AJUSTE_HOSPITAL, CONTROLE_X87_INICIAL

TRECHOS_PRODUCAO = TRECHOS_RECRUTAMENTO + [
    (0x423b9b, 0x423e65), (0x4471b8, 0x44724a), (0x48c43e, 0x48c45b),
    (0x41db1e, 0x41db24),
]


class BancadaProducao(BancadaRecrutamento):
    def __init__(self):
        super().__init__()
        self.acessos_producao = []
        self.conversao_inteira = None
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar_producao)

    def _registrar_producao(self, cpu, endereco, tamanho, _):
        if endereco in (0x4410b7, 0x47476a, 0x4471b8, 0x48c43e):
            self.acessos_producao.append(endereco)
        if endereco == 0x423cf4:
            esp = cpu.reg_read(x86.UC_X86_REG_ESP)
            self.conversao_inteira = struct.unpack('<I', cpu.mem_read(esp + 0x18, 4))[0]

    def carregar_producao(self, p):
        self.carregar_recrutamento(p.recrutamento)
        # 0x495be8 é dado vivo: substitui o primeiro byte da guarda de seleções.
        self.cpu.mem_write(BASE_AJUSTE_HOSPITAL, bytes([p.ajuste_hospital & 255]))
        self.cpu.mem_write(BASE_TIPOS_CONSTRUCOES - 4,
                           b'\xb2' * 4 + bytes(p.tipos_construcoes) + b'\x2b' * 4)

    def estado_producao(self):
        return dict(tipos_construcoes=bytes(self.cpu.mem_read(BASE_TIPOS_CONSTRUCOES, 1144)),
                    ajuste_hospital=self.cpu.mem_read(BASE_AJUSTE_HOSPITAL, 1)[0])

    def guardas_producao(self):
        return self.guardas_recrutamento() + tuple(bytes(self.cpu.mem_read(a, 4)) for a in
                                                 (BASE_TIPOS_CONSTRUCOES - 4, BASE_TIPOS_CONSTRUCOES + 1144))

    def executar_producao(self, entrada, registradores, controle=CONTROLE_X87_INICIAL):
        # Estado x87 conhecido por chamada; não modifica o código original.
        self.cpu.reg_write(x86.UC_X86_REG_FPCW, controle)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW, 0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG, 0xffff)
        self.acessos_producao.clear()
        self.conversao_inteira = None
        return self.executar(entrada, TRECHOS_PRODUCAO, registradores, parada=RETORNO)

    def avancar(self, indice, sortilegio=False, registradores=None, controle=CONTROLE_X87_INICIAL):
        regs = dict(registradores or {})
        regs['EAX'] = indice
        return self.executar_producao(0x423d14 if sortilegio else 0x423b9b, regs, controle)

    def contar(self, indice, tipo=9):
        return self.executar_producao(0x4471b8,
                                     dict(EAX=BASE_CONSTRUCOES + (indice & 65535) * 276 + 0xc,
                                          EDX=1, EBX=tipo))['EAX']
