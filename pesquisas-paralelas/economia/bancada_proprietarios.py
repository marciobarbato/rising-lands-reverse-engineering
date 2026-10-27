"""Referência original de efeitos de propriedade; movimento permanece dependência."""
import struct

from bancada_init_cave import BancadaInitCave, TRECHOS_INIT_CAVE
from construcoes import BASE_CAPACIDADES
from emulador import RETORNO, x86
from proprietarios import (BASE_BALOES, BASE_BIBLIOTECAS, BASE_JOGADOR_DEPOSITO,
                           BASE_NUMEROS_UNIDADES, BASE_PENDENCIAS, BASE_SORTILEGIOS,
                           PASSO_ORDENS_JOGADOR)

TABELA_ORDENS = 0x1400000
ORDENS = 0x1401000
TRECHOS_PROPRIEDADE = TRECHOS_INIT_CAVE + [
    (0x41be88, 0x41bfe6), (0x41c017, 0x41c18a), (0x41bb8a, 0x41be88),
    (0x441baa, 0x441d4f), (0x441d4f, 0x441e3b), (0x440d58, 0x440d5e),
    (0x456d92, 0x456db5), (0x447148, 0x447197), (0x4471b8, 0x44724a),
    (0x4472ea, 0x4473cf), (0x447483, 0x4474a6), (0x4474c7, 0x4474f3),
    (0x4749ca, 0x4749f2), (0x474a38, 0x474a95),
]


class BancadaProprietarios(BancadaInitCave):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(TABELA_ORDENS, 0x5000)
        self.cpu.mem_write(0x4e19b8, struct.pack('<I', TABELA_ORDENS))
        self.cpu.mem_write(TABELA_ORDENS, struct.pack('<4I', *(ORDENS + j * PASSO_ORDENS_JOGADOR for j in range(4))))
        self.paradas_dependencia = 0

    def _registrar(self, cpu, endereco, tamanho, contexto):
        super()._registrar(cpu, endereco, tamanho, contexto)
        if endereco in (0x441baa, 0x441d4f, 0x41bb8a, 0x4749ca, 0x474a38):
            r = {n: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + n)) for n in ('EAX', 'EDX', 'EBX', 'ECX')}
            self.chamadas.append(dict(entrada=endereco, **r))

    def carregar_propriedade(self, estado):
        self.carregar_mundo(estado.mundo)
        self.cpu.mem_write(BASE_BIBLIOTECAS, bytes(estado.bibliotecas))
        self.cpu.mem_write(BASE_BALOES, bytes(estado.baloes))
        self.cpu.mem_write(BASE_NUMEROS_UNIDADES, bytes(estado.numeros_unidades))
        self.cpu.mem_write(BASE_PENDENCIAS, bytes(estado.pendencias) + b'\xb2' * 8)
        self.cpu.mem_write(ORDENS - 8, b'\xf1' * 8 + bytes(estado.ordens) + b'\x1f' * 8)
        self.cpu.mem_write(BASE_SORTILEGIOS - 8, b'\xd3' * 8 + bytes(estado.sortilegios) + b'\x3d' * 8)
        self.cpu.mem_write(BASE_JOGADOR_DEPOSITO, bytes([estado.jogador_deposito]))

    def estado_propriedade(self):
        return dict(mundo=self.estado(),
                    bibliotecas=bytes(self.cpu.mem_read(BASE_BIBLIOTECAS, 4)),
                    baloes=bytes(self.cpu.mem_read(BASE_BALOES, 32)),
                    numeros_unidades=bytes(self.cpu.mem_read(BASE_NUMEROS_UNIDADES, 208)),
                    pendencias=bytes(self.cpu.mem_read(BASE_PENDENCIAS, 9152)),
                    ordens=bytes(self.cpu.mem_read(ORDENS, 10816)),
                    sortilegios=bytes(self.cpu.mem_read(BASE_SORTILEGIOS, 20)),
                    jogador_deposito=self.cpu.mem_read(BASE_JOGADOR_DEPOSITO, 1)[0])

    def guardas_propriedade(self):
        return (bytes(self.cpu.mem_read(BASE_CAPACIDADES - 8, 8)),
                bytes(self.cpu.mem_read(BASE_CAPACIDADES + 24, 4)),
                bytes(self.cpu.mem_read(BASE_PENDENCIAS + 9152, 8)),
                bytes(self.cpu.mem_read(ORDENS - 8, 8)),
                bytes(self.cpu.mem_read(ORDENS + 10816, 8)),
                bytes(self.cpu.mem_read(BASE_SORTILEGIOS - 8, 8)),
                bytes(self.cpu.mem_read(BASE_SORTILEGIOS + 20, 8)))

    def inicializar_jogador(self, indice, jogador):
        quantidade = struct.unpack('<H', self.cpu.mem_read(BASE_BALOES + (jogador & 255) * 8, 2))[0]
        paradas = {RETORNO, 0x441baa} if quantidade == 0 else {RETORNO}
        r = self.executar(0x41be88, TRECHOS_PROPRIEDADE, dict(EAX=indice, EDX=jogador),
                          parada=paradas, limite_instrucoes=1000000)
        self.paradas_dependencia += int(r['EIP'] == 0x441baa)
        return r

    def inicializar_neutro(self, indice, jogador):
        quantidade = struct.unpack('<H', self.cpu.mem_read(BASE_BALOES + (jogador & 255) * 8, 2))[0]
        paradas = {RETORNO, 0x441d4f} if quantidade == 1 else {RETORNO}
        r = self.executar(0x41c017, TRECHOS_PROPRIEDADE, dict(EAX=indice, EDX=jogador),
                          parada=paradas, limite_instrucoes=1000000)
        self.paradas_dependencia += int(r['EIP'] == 0x441d4f)
        return r
