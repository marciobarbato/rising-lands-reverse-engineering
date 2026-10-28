"""Bancada original de recrutamento; saída geométrica não é substituída."""
import struct

from bancada_construcoes import BancadaConstrucoes, TRECHOS
from construcoes import BASE_CONSTRUCOES
from emulador import RETORNO, UNIDADES, unicorn, x86
from recrutamento import (BASE_SELECOES, BASE_TIPOS_UNIDADES,
                          BASE_TIPOS_SORTILEGIOS, BASE_PERIODO_NOVA)

TRECHOS_RECRUTAMENTO = TRECHOS + [
    (0x4283e2, 0x428691), (0x420ba5, 0x420c19), (0x423e65, 0x423fb9),
    (0x4410b7, 0x4410d2), (0x441108, 0x44113e), (0x47476a, 0x474785),
]


class BancadaRecrutamento(BancadaConstrucoes):
    def __init__(self):
        super().__init__()
        self.paradas_dependencia = 0
        self.sufixos_isolados = 0

    def carregar_recrutamento(self, r):
        self.carregar_mundo(r.mundo)
        for base, bloco in ((BASE_SELECOES, r.selecoes), (BASE_TIPOS_UNIDADES, r.tipos_unidades),
                            (BASE_TIPOS_SORTILEGIOS, r.tipos_sortilegios)):
            self.cpu.mem_write(base - 4, b'\xa9' * 4 + bytes(bloco) + b'\x9a' * 4)
        self.cpu.mem_write(BASE_PERIODO_NOVA - 2, b'\xc8' * 2 + struct.pack('<H', r.periodo_nova) + b'\x8c' * 2)
        self.cpu.mem_write(UNIDADES, bytes(r.unidades) + b'\xd7' * 8)

    def estado_recrutamento(self):
        return dict(selecoes=bytes(self.cpu.mem_read(BASE_SELECOES, 8)),
                    tipos_unidades=bytes(self.cpu.mem_read(BASE_TIPOS_UNIDADES, 1300)),
                    tipos_sortilegios=bytes(self.cpu.mem_read(BASE_TIPOS_SORTILEGIOS, 230)),
                    unidades=bytes(self.cpu.mem_read(UNIDADES, 220800)),
                    periodo_nova=struct.unpack('<H', self.cpu.mem_read(BASE_PERIODO_NOVA, 2))[0])

    def guardas_recrutamento(self):
        guardas = []
        for base, tamanho in ((BASE_SELECOES, 8), (BASE_TIPOS_UNIDADES, 1300),
                              (BASE_TIPOS_SORTILEGIOS, 230)):
            guardas.extend(bytes(self.cpu.mem_read(a, 4)) for a in (base - 4, base + tamanho))
        guardas.extend((bytes(self.cpu.mem_read(BASE_PERIODO_NOVA - 2, 2)),
                        bytes(self.cpu.mem_read(BASE_PERIODO_NOVA + 2, 2)),
                        bytes(self.cpu.mem_read(UNIDADES + 220800, 8))))
        return tuple(guardas)

    def chamar(self, entrada, eax=0, edx=0, registradores=None):
        regs = dict(registradores or {})
        regs.update(EAX=eax, EDX=edx)
        resultado = self.executar(entrada, TRECHOS_RECRUTAMENTO, regs,
                                  parada={RETORNO, 0x41d1d0})
        if resultado['EIP'] == 0x41d1d0:
            self.paradas_dependencia += 1
        return resultado

    def sufixo_isolado(self, indice, celula):
        """Executa 0x428640 com frame sintético, sem fingir executar a dependência.

        O sufixo grava AX e desmonta 0x44 bytes locais + quatro registradores.
        Esse teste separado não é retomada de um prefixo nem prova ponta a ponta.
        """
        self.sufixos_isolados += 1
        return self.executar(0x428640, TRECHOS_RECRUTAMENTO,
                              dict(ESI=BASE_CONSTRUCOES + (indice & 65535) * 276, EAX=celula),
                              pilha={0x54: struct.pack('<I', RETORNO)})
