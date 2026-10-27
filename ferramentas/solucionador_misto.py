"""Busca original com OptimiseChemin/TestLigneOptimise substituídos por Python.

Backend experimental explícito. A referência SolucionadorOriginal continua
executando todas as funções originais, sem essa substituição.
"""
import struct
from emulador import RETORNO, x86
from otimizacao_caminhos import ContextoLinha, otimizar_rota
from solucionador_original import BancadaNavegacao, SolucionadorOriginal


class BancadaMista(BancadaNavegacao):
    def __init__(self):
        super().__init__()
        self.otimizacoes_python = []

    def calcular(self, mundo, indice):
        r = self.executar(0x42f214, self.intervalos, parada=(RETORNO, 0x42e890), limite_instrucoes=1000000)
        if r['EIP'] == 0x42e890:
            # Único chamador observado em CheminCalcul. OptimiseChemin conserva
            # EBX/ECX/EDX/ESI/EDI/EBP; o chamador zera EAX antes de utilizá-lo.
            retorno = struct.unpack('<I', self.cpu.mem_read(r['ESP'], 4))[0]
            if retorno != 0x43b2be or r['EAX'] not in (0x4e116a, 0x4e136a):
                raise NotImplementedError('Checkpoint de otimização diferente do chamador reconstruído')
            unidade = struct.unpack('<H', self.cpu.mem_read(0x496304, 2))[0]
            contexto = ContextoLinha(mundo, unidade, self.cpu.mem_read(0x4e0f48, 1)[0],
                                     self.cpu.mem_read(0x4e0f42, 1)[0], self.cpu.mem_read(0x4e0f41, 1)[0])
            mundo.permitir_aliados_parados = self.cpu.mem_read(0x4e1771, 1)[0]
            antes = bytes(self.cpu.mem_read(r['EAX'], 512))
            depois = otimizar_rota(contexto, antes)
            self.cpu.mem_write(r['EAX'], depois)
            self.cpu.mem_write(0x4e1771, bytes([mundo.permitir_aliados_parados]))
            self.otimizacoes_python.append(dict(unidade=unidade,
                                                celulas_antes=struct.unpack_from('<H', antes)[0],
                                                celulas_depois=struct.unpack_from('<H', depois)[0]))
            self.cpu.reg_write(x86.UC_X86_REG_ESP, r['ESP'] + 4)
            self.retomar(retorno, self.intervalos, limite_instrucoes=1000000)
        return self.resultado(indice)


class SolucionadorComOtimizacaoPython(SolucionadorOriginal):
    def __init__(self):
        self.bancada = BancadaMista()
