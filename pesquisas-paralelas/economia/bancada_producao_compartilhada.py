"""Original CalculTroupe through actual conversion/recovery, no call mocks."""
import struct
from types import SimpleNamespace

from bancada_ciclo_producao import BancadaCicloProducao, TRECHOS_CICLO
from bancada_recuperacao_unidades import BancadaRecuperacaoUnidades
from bancada_conversao_saida import BancadaConversaoSaida
from bonus_unidades import BASE_BONUS_UNIDADES
from emulador import RETORNO, unicorn, x86
from producao import CONTROLE_X87_INICIAL

TRECHOS_COMPARTILHADOS = TRECHOS_CICLO + list(BancadaRecuperacaoUnidades.intervalos)
CAMPOS_BUSCA = ((0x496304, 'H', 'unidade'), (0x4e0f36, 'B', 'ocupada'),
                (0x4e0f37, 'B', 'sucesso'), (0x4e0f3c, 'I', 'ponteiro_rota'),
                (0x496302, 'B', 'concluida'))


class BancadaProducaoCompartilhada(BancadaCicloProducao):
    def __init__(self):
        super().__init__()
        self.consultas = []
        self.paradas_experiencia = 0
        self.paradas_consulta = 0
        self.paradas_importacao = 0
        self.depositos = []
        # Reuse the committed core's read-only native-query observer.
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._consulta)

    def _consulta(self, cpu, endereco, tamanho, dados):
        if endereco in (0x4475ac, 0x428cc0):
            observador = SimpleNamespace(paradas=self.paradas, chamadas=self.consultas)
            BancadaConversaoSaida._consulta(observador, cpu, endereco, tamanho, dados)
        if endereco == 0x42340f:
            self.depositos.append(tuple(cpu.reg_read(getattr(x86, "UC_X86_REG_"+nome)) & mascara
                                        for nome, mascara in (("EBX",255),("EAX",255),("EDX",65535),("ECX",65535))))

    def carregar_compartilhado(self, p, mundo, bonus):
        self.carregar_producao(p)
        self.cpu.mem_write(BASE_BONUS_UNIDADES - 4, b'\x85'*4 + bytes(bonus.memoria) + b'\x58'*4)
        for endereco, formato, nome in CAMPOS_BUSCA:
            self.cpu.mem_write(endereco, struct.pack('<'+formato, getattr(mundo.busca, nome)))
        self.vizinhos_bonus = bytes(self.cpu.mem_read(BASE_BONUS_UNIDADES - 4, 1880))

    def calcular_compartilhado(self, indice, *, consulta_pendente=False, importacao_pendente=False):
        self.saidas_tropa.clear()
        self.chamadas.clear()
        self.consultas.clear()
        self.depositos.clear()
        self.cpu.reg_write(x86.UC_X86_REG_FPCW, CONTROLE_X87_INICIAL)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW, 0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG, 0xffff)
        parada = {RETORNO, 0x420f81, 0x41dde0}
        if consulta_pendente:
            parada.add(0x428cc0)
        if importacao_pendente:
            parada.add(0x420698)
        resultado = self.executar(0x4259e6, TRECHOS_COMPARTILHADOS,
                                  dict(EAX=indice), parada=parada, limite_instrucoes=1000000)
        self.retornos += resultado['EIP'] == RETORNO
        self.paradas_experiencia += resultado['EIP'] == 0x420f81
        self.paradas_consulta += resultado['EIP'] == 0x428cc0
        self.paradas_importacao += resultado['EIP'] == 0x420698
        return resultado

    def estado_busca(self):
        return tuple(struct.unpack('<'+formato, self.cpu.mem_read(endereco, struct.calcsize(formato)))[0]
                     for endereco, formato, _ in CAMPOS_BUSCA)
