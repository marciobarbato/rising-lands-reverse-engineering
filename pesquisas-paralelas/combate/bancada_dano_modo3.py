"""Original mode-3 source getter calls, observed without substituting returns."""
import struct

from bancada_consumo_dano import BancadaConsumoDano, CONSUMO
from bancada_combate import RETORNO, x86

QUERIES = {0x41a4f4: 'BatimentGetType', 0x418b8a: 'TypeBatimentGetDegat',
           0x41a08c: 'BatimentGetPlayer'}
INTERVALOS = CONSUMO + [(0x418b42, 0x418b97), (0x41a08c, 0x41a0ab), (0x41a4f4, 0x41a513)]
ESTRUTURAS = 0x49a0c8


class BancadaDanoModo3(BancadaConsumoDano):
    def _observar_consumo(self, cpu, at, size, data):
        super()._observar_consumo(cpu, at, size, data)
        if at not in QUERIES:
            return
        sp = cpu.reg_read(x86.UC_X86_REG_ESP)
        ret = struct.unpack('<I', cpu.mem_read(sp, 4))[0]
        if not 0x4502f0 <= ret < 0x450856:
            return
        a, d, b = (cpu.reg_read(getattr(x86, 'UC_X86_REG_'+n)) for n in ('EAX', 'EDX', 'EBX'))
        args = (a & 255, d & 255, b & 255) if at == 0x418b8a else (a & 65535,)
        event = [QUERIES[at], args]
        self.eventos_consumo.append(event)
        self.pendentes.append((ret, event))

    def carregar_fonte(self, structures, row10, row11):
        self.cpu.mem_write(ESTRUTURAS, bytes(structures))
        self.cpu.mem_write(0x4dfb80, bytes(row10))
        self.cpu.mem_write(0x4dfb64, bytes(row11))

    def consumir(self, victim=1, source=0):
        result = self.executar(0x4502f0, INTERVALOS,
            dict(EAX=victim | 0xabcd0000, EDX=0xface0003,
                 EBX=source | 0xbeef0000, ECX=0xcafe00ff),
            parada={RETORNO, 0x4506a1, 0x48aa79}, limite_instrucoes=100000)
        if result['EIP'] == 0x48aa79:
            self._observar_consumo(self.cpu, 0x48aa79, 0, None)
        return result
