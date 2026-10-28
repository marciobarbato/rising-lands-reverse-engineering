"""Original remap reset/allocation/classification with two declared imports."""
from collections import Counter
import hashlib
import struct

from bancada_remapeamento_mundo import BancadaRemapeamentoMundo, CORES
from emulador import RETORNO, unicorn, x86
from vinculos_declarados import ParadaVinculoDeclarado

CLASSES, MARCADORES = 0x1900000, 0x1910000


class BancadaClassificacaoRemapeamento(BancadaRemapeamentoMundo):
    intervalos = BancadaRemapeamentoMundo.intervalos + [(0x4752b8, 0x475302)]
    pontos_retomada = (0x42eee1, 0x42ef22)

    def __init__(self):
        super().__init__()
        self.segmentar = True
        self.cpu.mem_map(CLASSES, 65536)
        self.cpu.mem_map(MARCADORES, 4096)
        self.cpu.mem_write(0x507db0, struct.pack('<I', MARCADORES))
        self.declarar_importacao(0x5231c0, 'GlobalAlloc', 2, self._alocar)
        self.declarar_importacao(0x5231d0, 'GlobalLock', 1, self._fixar)
        self.origens = Counter()
        self.consultas_naturais = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._observar_consulta)

    def _alocar(self, chamada):
        if chamada.argumentos != (0, 65536):
            raise ParadaVinculoDeclarado('Only the declared 65536-byte GMEM_FIXED class allocation is supported')
        return 0 if self.nula else CLASSES

    def _fixar(self, chamada):
        esperado = 0 if self.nula else CLASSES
        if chamada.argumentos != (esperado,):
            raise ParadaVinculoDeclarado('Unknown class allocation handle')
        if self.lock_desconhecido:
            raise ParadaVinculoDeclarado('Lock fixture deliberately unavailable; allocation retained')
        return esperado

    def _observar_consulta(self, cpu, endereco, tamanho, _):
        if endereco == 0x4752b8 and endereco not in self.paradas:
            self.consultas_naturais.append(cpu.reg_read(x86.UC_X86_REG_EAX) & 65535)

    def carregar_classificacao(self, mundo, nula=False, lock_desconhecido=False):
        self.carregar_remapeamento(mundo)
        self.nula, self.lock_desconhecido = nula, lock_desconhecido
        self.cpu.mem_write(CLASSES, b'\xa5'*65536)
        self.cpu.mem_write(MARCADORES, bytes(mundo.marcadores_obstaculos_tiles))
        self.consultas_naturais = []
        self.vinculos_declarados.eventos.clear()

    def classificar(self, parada=(RETORNO, 0x42ef8b), *, limite_vinculos=4):
        self.origens['0x42ee1c'] += 1
        return self.executar(0x42ee1c, self.intervalos, parada=parada,
                             limite_instrucoes=1000000, limite_vinculos=limite_vinculos)

    def classes(self): return bytes(self.cpu.mem_read(CLASSES, 65536))

    def resumo(self, mundo):
        from cenarios_classificacao_remapeamento import resumo_classificacao
        from capturar_remapeamento_mundo import resumo_original
        r = resumo_original(self)
        r.update(classes_sha256=hashlib.sha256(self.classes()).hexdigest(),
                 class_counts={str(v): self.classes().count(v) for v in set(self.classes())},
                 natural_query_count=len(self.consultas_naturais),
                 natural_query_order_sha256=hashlib.sha256(struct.pack('<%dH' % len(self.consultas_naturais),
                                                                      *self.consultas_naturais)).hexdigest())
        return r
