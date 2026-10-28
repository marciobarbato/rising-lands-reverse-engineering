"""Unmodified original exchange callers, with explicit unit-loop stops."""
from bancada_transferencias_mercado import BancadaTransferenciasMercado, TRECHOS_TRANSFERENCIA
from emulador import RETORNO
from ordem_mercado import BASE_ACEITES

TRECHOS_ORDEM = TRECHOS_TRANSFERENCIA + [
    (0x461621, 0x461c4f), (0x46499f, 0x4649a7), (0x463617, 0x46361d),
]


class BancadaOrdemMercado(BancadaTransferenciasMercado):
    def __init__(self):
        super().__init__()
        self.paradas_unidades = 0
        self.retornos = 0

    def carregar_ordem(self, ordem):
        self.carregar_transferencia(ordem)
        self.cpu.mem_write(BASE_ACEITES - 4, b'\x85' * 4 + bytes(ordem.aceites) + b'\x58' * 4)
        self.vizinhos_antes = bytes(self.cpu.mem_read(0x4e2900, 0x700))

    def aceites(self):
        return bytes(self.cpu.mem_read(BASE_ACEITES, 4))

    def chamar_ordem(self, entrada, jogador, proponente):
        self.eventos.clear()
        self.escritas.clear()
        self.chamadas.clear()
        resultado = self.executar(entrada, TRECHOS_ORDEM, dict(EAX=jogador, EDX=proponente),
            parada={RETORNO, 0x46166b, 0x4618df})
        self.paradas_unidades += resultado['EIP'] in (0x46166b, 0x4618df)
        self.retornos += resultado['EIP'] == RETORNO
        return resultado
