"""Intact native Engin_RetrieveExperimente 0x441623 with full write logging.

Only original bytes execute; no binding, patch or substituted body is used.
Engin_ResetExperience 0x441470 and Engin_StoreExperimente 0x4414f8 may run
before it as original provenance producers of the saved buffer; Core does not
translate those two routines.
"""
import struct

import unicorn
from unicorn import x86_const as x86

from emulador import BancadaX86, BASE, PILHA, RETORNO, UNIDADES

ATUAL, GUARDADA, FIM = 0x4e19c4, 0x4e19ec, 0x4e1a14
# Neighbourhood written with distinct bytes around both queues. 0x4e19a0 (unit
# pool pointer used only by the Store producer) stays outside it.
VIZINHANCA = (0x4e19a4, 0x4e1a40)
IMAGEM = (BASE, BASE+0x200000)
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
SAIDA = REGISTROS + ('ESP', 'EIP', 'EFLAGS')

RECUPERAR = ((0x441623, 0x441659), (0x440d59, 0x440d5e))
RESETAR = ((0x441470, 0x4414ad), (0x440d5a, 0x440d5e))
ARMAZENAR = ((0x4414f8, 0x441623), (0x440d55, 0x440d5e))


class BancadaRecuperacaoExperiencia(BancadaX86):
    def __init__(self, arquivo=None):
        super().__init__(arquivo)
        self.escritas = []
        self.instrucoes = 0
        self.maximo_instrucoes = 0
        self.entradas_originais = {}
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._registrar_escrita)
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._contar)

    def _registrar_escrita(self, cpu, acesso, endereco, tamanho, valor, _):
        self.escritas.append((endereco, tamanho, valor & ((1 << 8*tamanho)-1)))

    def _contar(self, cpu, endereco, tamanho, _):
        self.instrucoes += 1

    def ler(self, inicio, fim):
        return bytes(self.cpu.mem_read(inicio, fim-inicio))

    def carregar(self, atual, guardada, vizinhanca):
        if len(atual) != 40 or len(guardada) != 40 or len(vizinhanca) != VIZINHANCA[1]-VIZINHANCA[0]:
            raise ValueError('Queues must be 40 bytes and the neighbourhood its declared size')
        self.cpu.mem_write(VIZINHANCA[0], bytes(vizinhanca))
        self.cpu.mem_write(ATUAL, bytes(atual))
        self.cpu.mem_write(GUARDADA, bytes(guardada))

    def carregar_unidades(self, pool):
        if len(pool) != 220800:
            raise ValueError('Unit pool must be 800 x 276 bytes')
        self.cpu.mem_write(UNIDADES, bytes(pool))
        self.cpu.mem_write(0x4e19a0, struct.pack('<I', UNIDADES))

    def _segmento(self, entrada, intervalos, registradores, limite):
        imagem = self.ler(*IMAGEM)
        self.escritas, self.instrucoes = [], 0
        regs = self.executar(entrada, intervalos, registradores, parada=RETORNO, limite_instrucoes=limite)
        regs['EFLAGS'] = self.cpu.reg_read(x86.UC_X86_REG_EFLAGS)
        self.maximo_instrucoes = max(self.maximo_instrucoes, self.instrucoes)
        self.entradas_originais[hex(entrada)] = self.entradas_originais.get(hex(entrada), 0)+1
        depois = self.ler(*IMAGEM)
        mudancas = [(IMAGEM[0]+i, imagem[i], depois[i]) for i in range(len(imagem)) if imagem[i] != depois[i]]
        pilha = [e for e in self.escritas if PILHA <= e[0] < PILHA+0x10000]
        return dict(registers=regs, instructions=self.instrucoes, image_changes=mudancas,
                    writes=list(self.escritas), stack_writes=pilha)

    def recuperar(self, registradores, limite=2000):
        return self._segmento(0x441623, RECUPERAR, registradores, limite)

    def resetar(self, registradores, limite=2000):
        return self._segmento(0x441470, RESETAR, registradores, limite)

    def armazenar(self, registradores, limite=1000000):
        return self._segmento(0x4414f8, ARMAZENAR, registradores, limite)
