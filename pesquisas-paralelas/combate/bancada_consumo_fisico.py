"""Intact original damage, physical death and projectile callers in one world."""
import struct

from consumo_dano import ConsumidorDanoUnidade  # establish committed Core path
from bancada_morte_unidades import BancadaMorteUnidades
from bancada_consumo_dano import BancadaConsumoDano
from bancada_impacto_unidades import BancadaImpactoUnidades, WRAPPER
from bancada_dano_modo3 import observar_fonte, INTERVALOS as SOURCE_INTERVALS
from emulador import RETORNO, x86

PROJETEIS, TIPOS, MATRIZES = 0x5000000, 0x5002000, 0x5003000
INTERVALOS = BancadaMorteUnidades.intervalos + WRAPPER + SOURCE_INTERVALS


class BancadaConsumoFisico(BancadaMorteUnidades):
    def __init__(self):
        super().__init__()
        import unicorn
        self.cpu.mem_map(PROJETEIS, 0x5000)
        self.cpu.mem_write(0x5080f0, struct.pack('<I', PROJETEIS))
        self.cpu.mem_write(0x4e199c, struct.pack('<I', TIPOS))
        self.cpu.mem_write(TIPOS, struct.pack('<26I', *(MATRIZES+32*i for i in range(26))))
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observe)

    def preparar(self, mundo, danos, pool, modo4=None, fonte10=None, fonte11=None):
        self.carregar_fisica(mundo)
        self.cpu.mem_write(PROJETEIS, bytes(pool.memoria))
        self.cpu.mem_write(0x4dfba0, bytes(1872))
        if modo4 is not None:
            self.cpu.mem_write(0x49716c, bytes([modo4[0]]))
            self.cpu.mem_write(0x49716e, bytes([modo4[1]]))
        if fonte10 is not None:
            self.cpu.mem_write(0x4dfb80, bytes(fonte10))
            self.cpu.mem_write(0x4dfb64, bytes(fonte11))
        self.cpu.mem_write(0x4965ac, b'\0')
        self.cpu.mem_write(0x508f7c, bytes(4))
        self.cpu.mem_write(0x4e19c0, bytes(4))
        self.cpu.mem_write(0x496acc, b'\x34\x12')
        self.cpu.mem_write(0x497164, struct.pack('<I', 12345))
        self.cpu.mem_write(0x508044, bytes(80))
        for owner in range(4):
            # Declared original inactive-diplomacy guard for complete fixtures.
            self.cpu.mem_write(0x51a990+16*owner, b'\1')
            self.cpu.mem_write(self.grades['jogadores']+20*owner+6, b'\0')
        for i, row in enumerate(danos):
            self.cpu.mem_write(MATRIZES+32*i, bytes(row))
        self.eventos_consumo, self.pendentes, self.entradas_consumo = [], [], []
        self.eventos_wrapper, self.retornos_wrapper, self.eventos_morte = [], [], []
        self.on_message = None
        self.after_dying = False

    def _observe(self, cpu, at, size, data):
        BancadaConsumoDano._observar_consumo(self, cpu, at, size, data)
        observar_fonte(self, cpu, at)
        BancadaImpactoUnidades._observar_wrapper(self, cpu, at, size, data)
        if at == 0x4507af:
            self.after_dying = True
        if at not in (0x44fb20, 0x444938, 0x475118):
            return
        a, d, b = (cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n))
                   for n in ('EAX', 'EDX', 'EBX'))
        sp = cpu.reg_read(x86.UC_X86_REG_ESP)
        ret = struct.unpack('<I', cpu.mem_read(sp, 4))[0]
        if not 0x4502f0 <= ret < 0x450856:
            return
        name, args = (('EnginSetLevelExperience', (a & 65535, d & 255))
            if at == 0x44fb20 else ('SetDyingEngin', (a & 65535,))
            if at == 0x444938 else ('MAJSympathie', (a & 255, d & 255, b)))
        self.eventos_morte.append((name, args))

    def consumir(self, victim=1, attacker=0, checkpoint=RETORNO, projectile=False,
                 mode=1, direction=255):
        result = self.executar(0x46eaf8 if projectile else 0x4502f0, INTERVALOS,
            dict(EAX=PROJETEIS+37*56) if projectile else
            dict(EAX=victim, EDX=mode, EBX=attacker, ECX=direction),
            parada={RETORNO, checkpoint, 0x44fb20, 0x48aa79},
            limite_instrucoes=500000)
        if result['EIP'] in (0x475118, 0x44fb20, 0x48aa79):
            # Stop hook runs before observers; read the untouched entry state.
            self._observe(self.cpu, result['EIP'], 0, None)
        return result

    def ler_pool(self):
        return bytes(self.cpu.mem_read(PROJETEIS, 5600))
