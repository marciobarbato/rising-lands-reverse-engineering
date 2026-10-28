"""Máquina de projéteis original em fatias, sem alterar instruções ou chamadas.

As paradas em Avance e em cada célula do tipo 30 só interrompem a CPU. A
retomada executa a instrução parada e conserva registradores, pilha e memória.
"""
import struct

from bancada_avanco_projeteis import BancadaAvanco, AVANCO, PROJETEIS, x86
from bancada_combate import RETORNO

EXPLOSOES, QUADROS_EXPLOSAO = 0x1180000, 0x1190000
MAQUINA = AVANCO + [(0x46fc0f, 0x46fc8b), (0x479555, 0x4795af),
    (0x475710, 0x475736), (0x474734, 0x47476a), (0x476e7b, 0x477042)]


class BancadaMaquinaProjeteis(BancadaAvanco):
    def __init__(self):
        self._ignorar_inicio = None
        super().__init__()
        self.cpu.mem_map(EXPLOSOES, 0x20000)
        self.cpu.mem_write(0x507d74, struct.pack('<I', EXPLOSOES))
        self.cpu.mem_write(0x507dac, struct.pack('<I', QUADROS_EXPLOSAO))
        self.atividades_efeitos = []
        self.indices_avanco = []

    def _conferir_endereco(self, cpu, endereco, tamanho, extra):
        if endereco == self._ignorar_inicio:
            self._ignorar_inicio = None
            if not any(a <= endereco and endereco + tamanho <= b for a, b in self.permitidos):
                raise RuntimeError('Retomada fora dos intervalos declarados')
            return
        super()._conferir_endereco(cpu, endereco, tamanho, extra)

    def _observar_avanco(self, cpu, endereco, tamanho, extra):
        super()._observar_avanco(cpu, endereco, tamanho, extra)
        if endereco == 0x46eaf8:
            self.indices_avanco.append((cpu.reg_read(x86.UC_X86_REG_EAX) - PROJETEIS) // 56)
        nomes = {0x475710: 'CreerExplosion', 0x47474f: 'SortilegeGetTempsFin',
                 0x474734: 'SortilegeGetRayonEffet', 0x476e82: 'EteintTerrain',
                 0x450874: 'InfligeDegat'}
        if endereco not in nomes:
            return
        esp = cpu.reg_read(x86.UC_X86_REG_ESP)
        retorno = struct.unpack('<I', cpu.mem_read(esp, 4))[0]
        if not 0x46eaf8 <= retorno < 0x46fc0f:
            return  # o wrapper de dano é registrado pela classe anterior
        a, d, b, c = (cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n))
                      for n in ('EAX', 'EDX', 'EBX', 'ECX'))
        if endereco == 0x450874:
            args = (a & 65535, d & 255, b & 65535, c & 255, cpu.mem_read(esp + 4, 1)[0])
        elif endereco == 0x475710:
            args = (a & 65535, d & 255)
        elif endereco == 0x476e82:
            args = (a & 65535, d & 65535, b & 255)
        else:
            args = (a & 255,)
        self.trilha.append((nomes[endereco], args))
        if endereco in (0x475710, 0x476e82):
            ptr = cpu.reg_read(x86.UC_X86_REG_ESI)
            self.atividades_efeitos.append((nomes[endereco], cpu.mem_read(ptr + 2, 1)[0]))

    def contexto_maquina(self, semente=1, incremento=1, tempo=32, raio=3, campo=0):
        self.contexto_avanco(semente, incremento, (0, 0))
        self.cpu.mem_write(0x497172, struct.pack('<H', tempo))
        self.cpu.mem_write(0x497170, struct.pack('<H', raio))
        self.cpu.mem_write(0x4dfb44, bytes([campo]))
        self.cpu.mem_write(EXPLOSOES, bytes(65536))
        self.cpu.mem_write(QUADROS_EXPLOSAO, b'\xad' * 65536)

    def _fatiado(self, entrada, registradores=None):
        self.limpar_trilha()
        self.atividades_efeitos = []
        self.indices_avanco = []
        paradas = {RETORNO, 0x46eaf8, 0x46f48a}
        self._ignorar_inicio = entrada
        r = self.executar(entrada, MAQUINA, registradores, parada=paradas, limite_instrucoes=500000)
        for _ in range(20000):
            if r['EIP'] == RETORNO:
                return r
            self._ignorar_inicio = r['EIP']
            r = self.retomar(r['EIP'], MAQUINA, parada=paradas, limite_instrucoes=500000)
        raise RuntimeError('Máquina excedeu 20000 retomadas')

    def avancar_completo(self, indice):
        return self._fatiado(0x46eaf8, dict(EAX=PROJETEIS + indice * 56))

    def calcular(self):
        return self._fatiado(0x46fc0f)

    def campo_tipo30(self):
        return self.cpu.mem_read(0x4dfb44, 1)[0]

    def ler_explosoes(self):
        return bytes(self.cpu.mem_read(EXPLOSOES, 65536)), bytes(self.cpu.mem_read(QUADROS_EXPLOSAO, 65536))
