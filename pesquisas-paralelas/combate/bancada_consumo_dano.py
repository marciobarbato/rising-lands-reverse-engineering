"""Execute original consumers; callbacks are observed, never replaced.

Full calls use a non-AI recipient so iagUnitSendMessage takes its original
no-op return. Audio and death are named dependency stops. Native projectile
impact -> cell wrapper -> unit consumer is captured before its first byte.
"""
import struct

from bancada_avanco_projeteis import BancadaAvanco, AVANCO, PROJETEIS, x86
from bancada_combate import UNIDADES, JOGADORES, GRADE, RETORNO, DISTANCIA
from bancada_animacao import VISIBILIDADE

TIPOS, MATRIZES = 0x1180000, 0x1181000
CONSUMO = AVANCO + DISTANCIA + [(0x4502f0, 0x450856), (0x428cc0, 0x428e71),
    (0x4500e4, 0x450286), (0x442bbe, 0x442bc5), (0x44271b, 0x442722),
    (0x4766f0, 0x47670a), (0x440c5d, 0x440d5e), (0x472174, 0x4721a8),
    (0x4829c8, 0x482a14), (0x482eb5, 0x482ebc), (0x46d817, 0x46d838),
    (0x467d97, 0x467da6), (0x44246e, 0x442586)]
CONSULTAS = {0x428cc0: 'Modificateur', 0x4500e4: 'ChercheTypeEnginProximite',
             0x4766f0: 'TerrainEstDecouvert', 0x440c5d: 'EnginGetVolume'}


class BancadaConsumoDano(BancadaAvanco):
    def __init__(self):
        super().__init__()
        import unicorn
        self.cpu.mem_map(TIPOS, 0x2000)
        self.cpu.mem_write(0x4e199c, struct.pack('<I', TIPOS))
        self.cpu.mem_write(TIPOS, struct.pack('<26I', *(MATRIZES + 32 * i for i in range(26))))
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_consumo)
        self.eventos_consumo, self.pendentes = [], []
        self.entradas_consumo = []
        self.on_message = None

    def _observar_consumo(self, cpu, endereco, tamanho, _):
        # Observe native returns without changing EIP, registers or stack.
        if self.pendentes and endereco == self.pendentes[-1][0]:
            _, item = self.pendentes.pop()
            item.append(cpu.reg_read(x86.UC_X86_REG_EAX))
        if endereco not in {*CONSULTAS, 0x4829c8, 0x48aa79, 0x4502f0}:
            return
        a, d, b, c = (cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n))
                      for n in ('EAX', 'EDX', 'EBX', 'ECX'))
        if endereco == 0x4502f0:
            self.entradas_consumo.append((a & 65535, d & 255, b & 65535, c & 255))
        if endereco not in {*CONSULTAS, 0x4829c8, 0x48aa79}:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
        if not 0x4502f0 <= retorno < 0x450856:
            return
        if endereco in CONSULTAS:
            nome = CONSULTAS[endereco]
            if nome == 'Modificateur':
                args = (a & 255, d & 255, b & 255)
            elif nome == 'ChercheTypeEnginProximite':
                args = (a & 255, d & 255, b & 65535, c & 65535)
            elif nome == 'TerrainEstDecouvert':
                args = (a & 65535, d & 255)
            else:
                args = (a & 65535,)
            item = [nome, args]
            self.eventos_consumo.append(item)
            self.pendentes.append((retorno, item))
        elif endereco == 0x4829c8:
            self.eventos_consumo.append(['iagUnitSendMessage', (a & 65535, d & 255, b & 65535)])
            if self.on_message:
                self.on_message()
        else:
            volume = struct.unpack('<I', cpu.mem_read(esp + 4, 4))[0]
            self.eventos_consumo.append(['PlaySnd_PostSound',
                (a, d, c, volume, (b - UNIDADES - 0x104) // 276)])

    def preparar_consumo(self, unidades, danos, mod5=0, mod6=0, bonus=0,
                          grade=None, visivel=False, jogador=0):
        self.mundo(unidades)  # natural zero is empty for both wrapper lookups
        for cell, value in (grade or {}).items():
            self.cpu.mem_write(GRADE + 2 * cell, struct.pack('<H', value))
        # Fixtures use owners 0..3, all non-AI. Native message implementation
        # executes its early return, not a fabricated callback return.
        for dono in range(4):
            self.cpu.mem_write(JOGADORES + 20 * dono + 1, b'\1')
        self.cpu.mem_write(0x4dfba0, bytes(468 * 5))
        for dono in range(4):
            for tipo in range(26):
                base = 0x4dfba0 + dono * 468 + tipo * 18
                self.cpu.mem_write(base + 8, struct.pack('<H', mod5 & 65535))
                self.cpu.mem_write(base + 10, bytes([mod6 & 255]))
        for i, row in enumerate(danos):
            self.cpu.mem_write(MATRIZES + 32 * i, bytes(row))
        self.cpu.mem_write(0x4965ac, bytes([bonus & 255]))
        self.cpu.mem_write(0x508041, bytes([jogador & 255]))
        self.cpu.mem_write(0x507d78 + jogador * 4, struct.pack('<I', VISIBILIDADE))
        self.cpu.mem_write(VISIBILIDADE, bytes([0 if visivel else 1]) * 65536)
        self.cpu.mem_write(0x508720, bytes(8))
        self.eventos_consumo, self.pendentes, self.entradas_consumo = [], [], []
        self.on_message = None

    def infligir_unidade(self, vitima, atacante, direcao=0, parar_em=()):
        stops = {RETORNO, 0x4506a1, 0x48aa79, *parar_em}
        r = self.executar(0x4502f0, CONSUMO,
            dict(EAX=vitima | 0xabcd0000, EDX=0xface0001,
                 EBX=atacante | 0xbeef0000, ECX=direcao | 0xcafe0000),
            parada=stops, limite_instrucoes=100000)
        if r['EIP'] == 0x48aa79 or r['EIP'] in parar_em:
            self._observar_consumo(self.cpu, r['EIP'], 0, None)
        return r

    def capturar_impacto(self, indice=37):
        """Run real ProjectileAvance/InfligeDegat, stop at unit consumer entry."""
        r = self.executar(0x46eaf8, CONSUMO,
            dict(EAX=PROJETEIS + 56 * indice), parada={0x4502f0}, limite_instrucoes=100000)
        self._observar_consumo(self.cpu, r['EIP'], 0, None)
        return r

    def retomar_consumidor(self):
        """Keep native wrapper stack; stop immediately after the consumer call."""
        return self.retomar(0x4502f0, CONSUMO,
            parada={0x450da5, 0x4506a1, 0x48aa79}, limite_instrucoes=100000)

    def ler_unidades(self):
        return bytes(self.cpu.mem_read(UNIDADES, 800 * 276))
