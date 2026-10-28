"""Run the original complete market lifecycle or its first-row checkpoint."""
from bancada_mercado import BancadaMercado, TRECHOS_MERCADO
from ciclo_mercado import BUFFERS_CICLO
from emulador import RETORNO

TRECHOS_CICLO = TRECHOS_MERCADO + [(0x46027c, 0x4602cd), (0x46634e, 0x4663eb)]
BASE_ACEITES = 0x4e2968


class BancadaCicloMercado(BancadaMercado):
    def __init__(self):
        super().__init__()
        self.retornos = 0
        self.paradas_indice = 0

    def carregar_ciclo(self, ciclo, aceites):
        self.carregar_mercado(ciclo.mercado)
        for nome, (endereco, _) in BUFFERS_CICLO.items():
            self.cpu.mem_write(endereco, bytes(getattr(ciclo, nome)))
        self.cpu.mem_write(BASE_ACEITES - 4, b'\x85' * 4 + bytes(aceites) + b'\x58' * 4)
        self.vizinhos_antes = bytes(self.cpu.mem_read(0x4e2900, 0x700))
        self.contatos_antes = bytes(self.cpu.mem_read(0x496f84, 12 + 8))
        self.escritas.clear()
        self.acessos.clear()

    def chamar_ciclo(self, entrada, jogador=0, outro=0, *, parar_indice=False):
        self.escritas.clear()
        self.acessos.clear()
        regs = dict(EAX=jogador, EDX=outro, EBX=0x92345678, ECX=0x3456789a,
                    ESI=0x56789abc, EDI=0x6789abcd, EBP=0x789abcde)
        parada = 0x466395 if parar_indice else RETORNO
        resultado = self.executar(entrada, TRECHOS_CICLO, regs, parada=parada)
        self.retornos += resultado['EIP'] == RETORNO
        self.paradas_indice += resultado['EIP'] == 0x466395
        return resultado

    def estado_ciclo(self):
        return {nome: bytes(self.cpu.mem_read(endereco, tamanho))
                for nome, (endereco, tamanho) in BUFFERS_CICLO.items()}
