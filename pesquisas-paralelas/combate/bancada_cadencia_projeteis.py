"""Trechos originais de cadência e apresentação; para antes de APIs gráficas."""
import struct

from bancada_maquina_projeteis import BancadaMaquinaProjeteis, MAQUINA
from bancada_combate import PILHA
from cadencia_projeteis import PreparacaoImpacto


class BancadaCadenciaProjeteis(BancadaMaquinaProjeteis):
    def portao_menu(self, entrada, atual, flag):
        self.cpu.mem_write(0x4e2f78, bytes([atual & 255]))
        self.cpu.mem_write(0x4e0730, bytes([flag & 255]))
        r = self.executar(0x42d14c, [(0x42d14c, 0x42d184)],
            parada={0x42d2de, 0x42d4e2}, pilha={0x104: bytes([entrada & 255])})
        return r['EIP'] == 0x42d2de

    def portao_evento(self, flag):
        self.cpu.mem_write(0x4e1b0e, bytes([flag & 255]))
        r = self.executar(0x42d2e3, [(0x42d2e3, 0x42d2f0), (0x4581b6, 0x4581bc)],
            parada={0x42d2f0, 0x42d4ea})
        return r['EIP'] == 0x42d2f0

    def portao_bloco(self, atual, flag):
        self.cpu.mem_write(0x4e2f78, bytes([atual & 255]))
        self.cpu.mem_write(0x4e0730, bytes([flag & 255]))
        r = self.executar(0x42d3c0, [(0x42d3c0, 0x42d3e1)],
            parada={0x42d3e1, 0x42d4e2})
        return r['EIP'] == 0x42d3e1

    def contadores(self, ciclo, metade, terco):
        self.cpu.mem_write(0x508f7c, struct.pack('<3I', ciclo, metade, terco))

    def incrementar_contadores(self):
        self.executar(0x475014, [(0x475014, 0x475041)], parada=0x475041)
        return struct.unpack('<3I', self.cpu.mem_read(0x508f7c, 12))

    def calcular_no_chamador(self):
        # O CALL original de CalculGame executa Calcul até voltar ao ponto
        # imediatamente anterior ao CALL de CalculEnginNextEtape.
        return self._fatiado(0x42d3f0, intervalos=MAQUINA + [(0x42d3f0, 0x42d3f5)],
                            saida=0x42d3f5)

    def contexto_apresentacao(self, campo, indice, ciclo, tabela, largura=640,
                             campo_508f8d=0, largura_celulas=20, altura_celulas=15):
        self.cpu.mem_write(0x4dfb44, bytes([campo & 255]))
        self.cpu.mem_write(0x4e1d18, bytes([indice & 255]))
        self.cpu.mem_write(0x508f7c, struct.pack('<I', ciclo & 0xffffffff))
        self.cpu.mem_write(0x4e1c18, bytes(tabela))
        self.cpu.mem_write(0x49a018, struct.pack('<H', largura & 65535))
        self.cpu.mem_write(0x508f8d, struct.pack('<I', campo_508f8d & 0xffffffff))
        self.cpu.mem_write(0x508724, struct.pack('<HH', largura_celulas & 65535,
                                               altura_celulas & 65535))

    def preparar_apresentacao(self):
        campo = self.campo_tipo30()
        indice = self.cpu.mem_read(0x4e1d18, 1)[0]
        self.executar(0x43f14f, [(0x43f14f, 0x43f220)], parada=0x43f220)
        # Seis pushes e 0x14 bytes locais, a partir do ESP da entrada.
        retangulo = struct.unpack('<4i', self.cpu.mem_read(PILHA + 0x8000 - 44, 16))
        deslocamento = retangulo[1] - retangulo[0]
        assert not campo or self.cpu.mem_read(0x4e1d18, 1)[0] == (indice + 1) & 255
        return PreparacaoImpacto(self.campo_tipo30(), self.cpu.mem_read(0x4e1d18, 1)[0],
                                 deslocamento, retangulo)
