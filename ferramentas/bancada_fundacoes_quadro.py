"""Intact native frame-foundation routines over the frozen M1 post-load state.

The bench loads the DGROUP block (0x494000..0x523000) and the CRT thread-data
block (0x3400000) from Missions' frozen original MissionLoad capture (final
blocks at the real return 0x42d22d). This is M1 post-load input, not yet frame-1
input. GlobalAlloc blocks are deliberately left unmapped: any access to them
faults instead of reading invented bytes. Only original bytes execute; the one
declared boundary is WINMM.timeGetTime for iaRandom(0), answered by an explicit
per-case clock value.
"""
import hashlib
import struct

import unicorn
from unicorn import x86_const as x86

from emulador import BancadaX86, BASE, PILHA
from estado_m1_quadro import carregar_m1, DGROUP, THREAD  # noqa: F401 (re-exported)

IMAGEM = (BASE, BASE + 0x200000)
CODIGO = (0x401000, 0x401000 + 601088)
REGISTROS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
IAT_TIME_GET_TIME = 0x5234a4

# (entry, intervals, stop) per Core-owned routine; ranges are end exclusive.
ROTINAS = {
    'GameNextFrame': (0x45d015, ((0x45d015, 0x45d01c),), None),
    'Random': (0x4704dc, ((0x4704dc, 0x470520),), None),
    'Randomize': (0x470520, ((0x470520, 0x470527),), None),
    'SetRandomSeed': (0x470527, ((0x470527, 0x47054c),), None),
    'GetRandomSeed': (0x47054c, ((0x47054c, 0x470552),), None),
    'iaRandom': (0x489728, ((0x489728, 0x4897a4), (0x493a24, 0x493a2a)), None),
    'LongRand': (0x45841b, ((0x45841b, 0x458420), (0x48c51d, 0x48c541), (0x48c513, 0x48c51d),
                            (0x48e7c7, 0x48e7cd)), None),
    'ProgIteration_counter_prefix': (0x475014, ((0x475014, 0x475041),), 0x475041),
    'CalculGame_load_counter_reset': (0x42d2ab, ((0x42d2ab, 0x42d2d0),), 0x42d2d0),
    'CalculGame_cd_permutation_draw': (0x42d2f9, ((0x42d2f9, 0x42d328),), 0x42d328),
}


class BancadaFundacoesQuadro(BancadaX86):
    def __init__(self, arquivo=None):
        super().__init__(arquivo)
        self.cpu.mem_map(THREAD[0], 0x1000)
        self.escritas = []
        self.instrucoes = 0
        self.maximo_instrucoes = 0
        self.entradas_originais = {}
        self.relogio = None
        self.eventos_relogio = []
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._registrar_escrita)
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._contar)
        self.declarar_importacao(IAT_TIME_GET_TIME, 'WINMM.timeGetTime', 0, self._atender_relogio)
        self.hash_codigo_inicial = self.hash_codigo()

    def _atender_relogio(self, chamada):
        if self.relogio is None:
            from vinculos_declarados import ParadaVinculoDeclarado
            raise ParadaVinculoDeclarado('No declared timeGetTime value for this case')
        self.eventos_relogio.append(dict(return_address=hex(chamada.retorno), value=hex(self.relogio)))
        return self.relogio

    def _registrar_escrita(self, cpu, acesso, endereco, tamanho, valor, _):
        self.escritas.append((endereco, tamanho, valor & ((1 << 8*tamanho)-1)))

    def _contar(self, cpu, endereco, tamanho, _):
        self.instrucoes += 1

    def hash_codigo(self):
        return hashlib.sha256(bytes(self.cpu.mem_read(CODIGO[0], CODIGO[1]-CODIGO[0]))).hexdigest()

    def ler(self, inicio, fim):
        return bytes(self.cpu.mem_read(inicio, fim-inicio))

    def carregar_estado(self, dgroup, thread, sobrescritas=()):
        """Load M1 blocks, then explicit derived overrides [(address, bytes)]."""
        self.cpu.mem_write(DGROUP[0], bytes(dgroup))
        self.cpu.mem_write(THREAD[0], bytes(thread))
        for endereco, dados in sobrescritas:
            if not (DGROUP[0] <= endereco and endereco+len(dados) <= DGROUP[1]
                    or THREAD[0] <= endereco and endereco+len(dados) <= THREAD[1]):
                raise ValueError('Derived overrides must stay inside the loaded M1 blocks')
            self.cpu.mem_write(endereco, bytes(dados))

    def estado(self):
        return self.ler(*DGROUP), self.ler(*THREAD)

    def chamar(self, nome, registradores, *, relogio=None, limite=10000):
        entrada, intervalos, parada = ROTINAS[nome]
        antes = self.estado()
        self.escritas, self.instrucoes, self.relogio, self.eventos_relogio = [], 0, relogio, []
        regs = (self.executar(entrada, intervalos, registradores, limite_instrucoes=limite) if parada is None
                else self.executar(entrada, intervalos, registradores, parada=parada, limite_instrucoes=limite))
        regs['EFLAGS'] = self.cpu.reg_read(x86.UC_X86_REG_EFLAGS)
        self.maximo_instrucoes = max(self.maximo_instrucoes, self.instrucoes)
        self.entradas_originais[hex(entrada)] = self.entradas_originais.get(hex(entrada), 0)+1
        depois = self.estado()
        mudancas = []
        for (base, _), a, d in ((DGROUP, antes[0], depois[0]), (THREAD, antes[1], depois[1])):
            mudancas += [(base+i, a[i], d[i]) for i in range(len(a)) if a[i] != d[i]]
        pilha = [e for e in self.escritas if PILHA <= e[0] < PILHA+0x10000]
        fora = [e for e in self.escritas if not PILHA <= e[0] < PILHA+0x10000]
        return dict(registers=regs, instructions=self.instrucoes, state_changes=mudancas, writes=fora,
                    stack_writes=pilha, clock=list(self.eventos_relogio))


def u32(dados, endereco, base=DGROUP[0]):
    return struct.unpack_from('<I', dados, endereco-base)[0]
