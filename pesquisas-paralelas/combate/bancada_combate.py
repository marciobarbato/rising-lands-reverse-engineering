"""Adaptador local da bancada x86 existente; nenhuma chamada é substituída."""
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'ferramentas'))
from emulador import BancadaX86, UNIDADES, RETORNO, PILHA
from unicorn import x86_const as x86

GRADE, JOGADORES, TERRENO = 0x1100000, 0x1120000, 0x1140000
DISTANCIA = [(0x479555, 0x4795af)]
ALIANCA = [(0x46d838, 0x46d877)]
EPILOGOS = [(0x440d58, 0x440d5e), (0x44f29a, 0x44f2a3)]
SCAN = [(0x453da2, 0x454235)] + DISTANCIA + ALIANCA + EPILOGOS
CONTATO = [(0x4468e4, 0x446aA1), (0x446b0c, 0x446c94),
           (0x44246e, 0x442586), (0x443468, 0x443470)]
ALCANCE = [(0x446cb5, 0x446fbf), (0x440f94, 0x440f9c),
           (0x428cc0, 0x428e71), (0x4746c9, 0x4746e4),
           (0x41aee2, 0x41aff8), (0x42381f, 0x4239a0),
           (0x41ab5c, 0x41ac8b), (0x41db1e, 0x41db24)] + DISTANCIA + CONTATO
LINHA = [(0x4517a2, 0x45189c), (0x477042, 0x4772ec), (0x47653c, 0x47656b)]
RECARGA = [(0x45173f, 0x4517a2), (0x428cc0, 0x428e71)]
ANGULO = [(0x4796cb, 0x4798b0), (0x48d5ce, 0x48d5f1),
          (0x48c43e, 0x48c45b), (0x48fee7, 0x48fefc), (0x48ff4a, 0x48ff7f)]
MIRA = [(0x451464, 0x4516d3), (0x44f33c, 0x44f344),
        (0x4239a0, 0x423b27), (0x423997, 0x4239a0)] + ANGULO + ALCANCE + EPILOGOS


class BancadaCombate(BancadaX86):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(GRADE, 0x60000)
        self.cpu.mem_write(0x4e0f38, struct.pack('<I', GRADE))
        self.cpu.mem_write(0x5080a8, struct.pack('<I', JOGADORES))
        self.cpu.mem_write(0x507d70, struct.pack('<I', TERRENO))
        self.cpu.mem_write(0x497168, struct.pack('<HH', 256, 256))
        # Configuração sintética explícita: x87, precisão estendida, exceções
        # mascaradas, arredondamento ao mais próximo. Sem workaround de FPATAN.
        self.cpu.reg_write(x86.UC_X86_REG_FPCW, 0x037f)
        self.cpu.mem_write(0x49946c, b'\0')

    def mundo(self, unidades, grade=None, mascaras=(0, 0, 0, 0, 0), terreno=None):
        if len(unidades) != 800 or any(len(u) != 276 for u in unidades):
            raise ValueError('Tabela deve conter 800 registros de 276 bytes')
        self.cpu.mem_write(UNIDADES, b''.join(unidades))
        buf = bytearray(b'\xff' * 0x20000)
        for celula, valor in (grade or {}).items():
            struct.pack_into('<H', buf, celula * 2, valor)
        self.cpu.mem_write(GRADE, bytes(buf))
        for i, mascara in enumerate(mascaras):
            self.cpu.mem_write(JOGADORES + 20 * i + 6, bytes([mascara]))
        buf = bytearray(0x20000)
        for celula, valor in (terreno or {}).items():
            struct.pack_into('<H', buf, celula * 2, valor)
        self.cpu.mem_write(TERRENO, bytes(buf))

    def modificadores(self, dono, tipo, mod3=0, mod4=0):
        base = 0x4dfba0 + dono * 468 + tipo * 18
        self.cpu.mem_write(base + 4, struct.pack('<H', mod3 & 65535))
        self.cpu.mem_write(base + 6, bytes([mod4 & 255]))

    def selecionar(self, indice, scan=False):
        r = self.executar(0x453da2 if scan else 0x453f74, SCAN,
                         dict(EAX=indice), limite_instrucoes=1000000)
        return r['EAX'] & 65535

    def alcance(self, indice, modo, referencia, minimo=False):
        r = self.executar(0x446eed if minimo else 0x446cb5, ALCANCE,
                         dict(EAX=indice, EDX=modo, EBX=referencia))
        return bool(r['EAX'] & 255)

    def linha(self, indice, modo, referencia):
        r = self.executar(0x4517a2, LINHA + [(0x41aee2, 0x41aff8)],
                         dict(EAX=indice, EDX=modo, EBX=referencia), limite_instrucoes=100000)
        return bool(r['EAX'] & 255)

    def angulo(self, x1, y1, x2, y2, setores):
        r = self.executar(0x4796cb, ANGULO, dict(EAX=x1, EDX=y1, EBX=x2, ECX=y2),
                         pilha={4: struct.pack('<I', setores)})
        return r['EAX'] & 65535

    def mira(self, indice, edi_entrada=0):
        return bool(self.executar(0x451464, MIRA, dict(EAX=indice, EDI=edi_entrada))['EAX'] & 255)
