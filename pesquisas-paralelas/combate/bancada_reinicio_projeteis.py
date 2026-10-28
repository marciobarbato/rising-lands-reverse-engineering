"""ProjectileReset 0x46e00a on the intact EXE over inherited dirty memory.

Every mapped region is explicit input: the complete original image with
poisoned DGROUP/.bss, the unit area, the stack and two 64 KiB pool regions.
Registers, flags and stack contents are set before one unpatched entry, either
directly or through one of the four original CALL instructions. The routine
reaches no CALL, so no binding or stop is declared besides its return.
"""
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'ferramentas'))
from emulador import BancadaX86, BASE, UNIDADES, PILHA, RETORNO
from unicorn import x86_const as x86

ROTINA = (0x46e00a, 0x46e02c)
GLOBAIS = (0x494000, 0x523000)
PONTEIRO_POOL = 0x5080f0
REGIOES_POOL = (0x1200000, 0x1f000000)
TAMANHO_REGIAO = 0x10000
ESP_ENTRADA = PILHA + 0x8000
REGISTRADORES = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP', 'EIP', 'EFLAGS')


class BancadaReinicioProjeteis(BancadaX86):
    def __init__(self):
        super().__init__()
        for base in REGIOES_POOL:
            self.cpu.mem_map(base, TAMANHO_REGIAO)

    def regioes(self):
        r = {'imagem': (BASE, 0x200000), 'unidades': (UNIDADES, 0x40000),
             'pilha': (PILHA, 0x10000), 'retorno': (RETORNO, 0x1000)}
        r.update({f'pool_{base:#x}': (base, TAMANHO_REGIAO) for base in REGIOES_POOL})
        return r

    def instantaneo(self):
        return {nome: bytes(self.cpu.mem_read(a, t)) for nome, (a, t) in self.regioes().items()}

    def preparar(self, globais, unidades, pilha, regioes, ponteiro):
        """Write dirty DGROUP/.bss, units, stack and pool regions, then the pool pointer."""
        if len(globais) != GLOBAIS[1] - GLOBAIS[0] or len(unidades) != 0x40000 or len(pilha) != 0x10000:
            raise ValueError('Dirty inputs must cover DGROUP/.bss, the unit area and the stack exactly')
        if set(regioes) != set(REGIOES_POOL) or any(len(d) != TAMANHO_REGIAO for d in regioes.values()):
            raise ValueError('Both pool regions need 64 KiB of explicit bytes')
        if not any(b <= ponteiro and ponteiro + 5600 <= b + TAMANHO_REGIAO for b in REGIOES_POOL):
            raise ValueError('Pool pointer must address 5600 bytes inside one mapped pool region')
        self.cpu.mem_write(GLOBAIS[0], bytes(globais))
        self.cpu.mem_write(PONTEIRO_POOL, struct.pack('<I', ponteiro))
        self.cpu.mem_write(UNIDADES, bytes(unidades))
        self.cpu.mem_write(PILHA, bytes(pilha))
        for base, dados in regioes.items():
            self.cpu.mem_write(base, bytes(dados))

    def resetar(self, registradores, eflags, chamador=None):
        """Enter at 0x46e00a (return to RETORNO) or at the CALL `chamador` up to its return.

        Uses the harness's explicit-state entry so the dirty stack and flags
        prepared above are the routine's inherited state, not harness zeros.
        """
        if chamador is None:
            entrada, intervalos, parada = ROTINA[0], [ROTINA], RETORNO
            if bytes(self.cpu.mem_read(ESP_ENTRADA, 4)) != struct.pack('<I', RETORNO):
                raise ValueError('A direct entry needs the harness return address already on the prepared stack')
        else:
            entrada, intervalos, parada = chamador, [(chamador, chamador + 5), ROTINA], chamador + 5
        for nome in ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP'):
            self.cpu.reg_write(getattr(x86, 'UC_X86_REG_' + nome), registradores[nome] & 0xffffffff)
        self.cpu.reg_write(x86.UC_X86_REG_ESP, ESP_ENTRADA)
        self.cpu.reg_write(x86.UC_X86_REG_EFLAGS, eflags)
        self.retomar(entrada, intervalos, parada, limite_instrucoes=2000)
        return {nome: self.cpu.reg_read(getattr(x86, 'UC_X86_REG_' + nome)) for nome in REGISTRADORES}
