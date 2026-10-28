"""Original mode-1 wrapper, observing queries/effects and dependency stops."""
import struct

from bancada_consumo_dano import BancadaConsumoDano, CONSUMO
from bancada_combate import RETORNO, x86
from bancada_avanco_projeteis import BancadaAvanco
from bancada_dano_modo3 import observar_fonte, INTERVALOS as SOURCE_INTERVALS

WRAPPER = CONSUMO + SOURCE_INTERVALS + [(0x46d838, 0x46d877), (0x477042, 0x4772ec),
                     (0x46d600, 0x46d629), (0x46e422, 0x46e4ca),
                     (0x475118, 0x475267), (0x46d8cb, 0x46d927)]
QUERIES = {0x41b54a: 'ChercheIndiceBatiment', 0x4465df: 'ChercheIndiceEnginCible',
    0x46d817: 'PlayerGetType', 0x4539f3: 'ChercheBatimentProximiteCaveOuSanctuaire',
    0x41aee2: 'BatimentGetCase', 0x477042: 'CalculDirection', 0x4770ee: 'CalculDirCase',
    0x4704dc: 'Random', 0x46d838: 'PlayerEstAllie', 0x41a08c: 'BatimentGetPlayer'}
EFFECTS = {0x4457d3: 'SetDeplaceEngin', 0x445a36: 'SetAttaqueEngin',
    0x475118: 'MAJSympathie', 0x46d8cb: 'PlayerResetAllie',
    0x46d600: 'PlayerAAttaqueSet', 0x48aa79: 'PlaySnd_PostSound',
    0x4502f0: 'EnginInfligeDegat'}
DEPENDENCIES = {0x4457d3, 0x445a36, 0x475118, 0x46d8cb, 0x48aa79, 0x4539f3, 0x41aee2}


class BancadaImpactoUnidades(BancadaConsumoDano):
    def __init__(self):
        self.random_wrapper = False
        super().__init__()
        import unicorn
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_wrapper)
        self.eventos_wrapper, self.retornos_wrapper = [], []

    def _observar_consumo(self, cpu, at, size, data):
        BancadaConsumoDano._observar_consumo(self, cpu, at, size, data)
        observar_fonte(self, cpu, at)

    def _observar_avanco(self, cpu, endereco, tamanho, _):
        # The predecessor observer restricts RNG to ProjectileAvance callers.
        # Wrapper RNG is independently captured by _observar_wrapper below.
        if endereco == 0x4704dc:
            sp = cpu.reg_read(x86.UC_X86_REG_ESP)
            ret = struct.unpack('<I', cpu.mem_read(sp, 4))[0]
            if 0x450874 <= ret < 0x4510dd:
                self.random_wrapper = True
                return
        elif endereco == 0x47051c and self.random_wrapper:
            self.random_wrapper = False
            return
        BancadaAvanco._observar_avanco(self, cpu, endereco, tamanho, _)

    def _observar_wrapper(self, cpu, endereco, tamanho, _):
        if self.retornos_wrapper and endereco == self.retornos_wrapper[-1][0]:
            _, event = self.retornos_wrapper.pop()
            event.append(cpu.reg_read(x86.UC_X86_REG_EAX))
        if endereco not in {*QUERIES, *EFFECTS}:
            return
        sp = cpu.reg_read(x86.UC_X86_REG_ESP)
        ret = struct.unpack('<I', cpu.mem_read(sp, 4))[0]
        if not 0x450874 <= ret < 0x4510dd:
            return
        a, d, b, c = (cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n))
                      for n in ('EAX', 'EDX', 'EBX', 'ECX'))
        name = QUERIES.get(endereco) or EFFECTS[endereco]
        if name in ('ChercheIndiceBatiment', 'BatimentGetCase', 'BatimentGetPlayer'):
            args = (a & 65535,)
        elif name == 'ChercheIndiceEnginCible':
            args = (a & 65535, d & 65535, b & 255)
        elif name == 'PlayerGetType':
            args = (a & 255,)
        elif name in ('PlayerEstAllie', 'PlayerResetAllie', 'PlayerAAttaqueSet'):
            args = (a & 255, d & 255)
        elif name == 'ChercheBatimentProximiteCaveOuSanctuaire':
            args = (a & 65535, d & 255)
        elif name == 'CalculDirection':
            args = (a & 65535, d & 65535)
        elif name == 'CalculDirCase':
            args = (a & 65535, d & 255)
        elif name == 'Random':
            args = (a,)
        elif name == 'SetDeplaceEngin':
            args = (a & 65535, d & 65535)
        elif name == 'SetAttaqueEngin':
            args = (a & 65535, d & 255, b & 65535)
        elif name == 'MAJSympathie':
            args = (a & 255, d & 255, b)
        elif name == 'EnginInfligeDegat':
            args = (a & 65535, d & 255, b & 65535, c & 255)
        else:
            volume = struct.unpack('<I', cpu.mem_read(sp + 4, 4))[0]
            args = (a, d, c, volume, '0x496ac8')
        event = [name, args]
        self.eventos_wrapper.append(event)
        if endereco in QUERIES and endereco not in DEPENDENCIES:
            self.retornos_wrapper.append((ret, event))

    def preparar_wrapper(self, unidades, danos, contador=0, anterior=0, local=0,
                          aliado=False, tipo_jogador=1, modo4=None, **kwargs):
        self.preparar_consumo(unidades, danos, jogador=local, **kwargs)
        if modo4 is not None:
            self.cpu.mem_write(0x49716c, bytes([modo4[0]]))
            self.cpu.mem_write(0x49716e, bytes([modo4[1]]))
        from bancada_combate import JOGADORES
        self.cpu.mem_write(JOGADORES + 20 * unidades[1][0] + 1, bytes([tipo_jogador]))
        self.cpu.mem_write(JOGADORES + 20 * unidades[0][0] + 6, bytes([2 if aliado else 0]))
        for addr, value in ((0x508f7c, contador), (0x4e19c0, anterior), (0x497164, 12345)):
            self.cpu.mem_write(addr, struct.pack('<I', value & 0xffffffff))
        self.cpu.mem_write(0x496acc, b'\x34\x12')
        self.cpu.mem_write(0x51a990, b'\1')
        self.cpu.mem_write(0x51a9a0, b'\1')  # native MAJSympathie inactive no-op
        self.eventos_wrapper, self.retornos_wrapper = [], []
        self.random_wrapper = False

    def impacto(self, cell, flag=0, direction=0, parar_consumidor=False, diplomacia_completa=False, mode=1):
        stops = {RETORNO, 0x4508af, 0x4506a1, *DEPENDENCIES}
        if diplomacia_completa:
            stops -= {0x475118, 0x46d8cb}
        if parar_consumidor:
            stops.add(0x4502f0)
        r = self.executar(0x450874, WRAPPER,
            dict(EAX=cell | 0xabcd0000, EDX=0xface0000 | mode, EBX=0xbeef0000,
                 ECX=direction | 0xcafe0000), parada=stops,
            pilha={4: struct.pack('<I', flag | 0xa5a50000)}, limite_instrucoes=100000)
        if r['EIP'] in {*DEPENDENCIES, 0x4502f0}:
            self._observar_wrapper(self.cpu, r['EIP'], 0, None)
        return r

    def avancar_ate_fim(self, indice=37):
        from bancada_projeteis import PROJETEIS
        return self.executar(0x46eaf8, WRAPPER,
            dict(EAX=PROJETEIS + 56 * indice), parada={RETORNO, *DEPENDENCIES, 0x4506a1},
            limite_instrucoes=100000)

    def ler_alerta(self):
        return (struct.unpack('<I', self.cpu.mem_read(0x4e19c0, 4))[0],
                struct.unpack('<H', self.cpu.mem_read(0x496acc, 2))[0])
