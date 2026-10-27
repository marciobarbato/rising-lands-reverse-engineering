"""Executa criação, espera, subtarefas e conclusão no x86 original, sem mocks."""
import struct
from pathlib import Path
from emulador import BancadaX86
from simbolos_ia import ler_sbl, enderecar_simbolos

TAREFAS = 0x512320
CONTEXTO = 0x5148b0
INTERVALOS = [(0x47cfd0, 0x47d03a), (0x47d03a, 0x47d059),
              (0x47d07a, 0x47d0e5), (0x47d11a, 0x47d171),
              (0x47d220, 0x47d26e), (0x47d2fd, 0x47d304),
              (0x47d314, 0x47d5ac), (0x47d7ec, 0x47d882),
              (0x47d920, 0x47d98b), (0x47da7a, 0x47daa1),
              (0x47f31c, 0x47f328), (0x481280, 0x481328), (0x46c11a, 0x46c122)]


class BancadaTarefas(BancadaX86):
    intervalos = INTERVALOS

    def __init__(self):
        super().__init__()
        sbl = Path(__file__).resolve().parents[2] / 'source/cd/INSTALHD/RISING.SBL'
        self.simbolos = enderecar_simbolos(ler_sbl(sbl.read_bytes()))[1]

    def carregar(self, programa, missao=0):
        self.cpu.mem_write(TAREFAS, bytes(100 * 96))
        self.cpu.mem_write(0x5148a0, bytes(0x70))
        self.cpu.mem_write(0x514910, bytes(1200 * 20))
        self.cpu.mem_write(0x51a720, bytes(128))
        self.cpu.mem_write(0x496fe4, struct.pack('<H', missao))
        for i, op in enumerate(programa.instrucoes):
            operacao = self.simbolos[op.operacao] if isinstance(op.operacao, str) and op.operacao != 'NULL' else (0 if op.operacao == 'NULL' else op.operacao)
            self.cpu.mem_write(0x514910 + i * 20, struct.pack('<5I', operacao, op.formato, op.sucesso, op.falha, op.constante))
        self.cpu.mem_write(0x51a720, struct.pack('<' + 'H' * len(programa.entradas), *programa.entradas))
        self.executar(0x47d220, self.intervalos)

    def postar(self, jogador, tipo, argumentos=()):
        args = tuple(argumentos) + (0,) * (6 - len(argumentos))
        r = self.executar(0x47d920, self.intervalos, dict(EAX=jogador, EDX=tipo, EBX=args[0], ECX=args[1]),
                          pilha={4: struct.pack('<4I', *(a & 0xffffffff for a in args[2:]))})
        return r['EAX'] if r['EAX'] != 0xffffffff else -1

    def atualizar(self, jogador):
        return self.executar(0x47d314, self.intervalos, dict(EAX=CONTEXTO + jogador * 16))['EAX']

    def memoria_tarefas(self):
        return bytes(self.cpu.mem_read(TAREFAS, 9600))

    def estado_listas(self):
        def lista(endereco):
            return list(struct.unpack('<ii', self.cpu.mem_read(endereco, 8)))
        return dict(livres=lista(0x5148a0), contextos=[lista(CONTEXTO + j * 16) for j in range(5)],
                    ativas=struct.unpack('<I', self.cpu.mem_read(0x514904, 4))[0])
