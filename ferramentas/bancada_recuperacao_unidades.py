"""Intact original recovery helpers and joined conversion caller prefix."""
from bancada_conversao_saida import BancadaConversaoSaida
from emulador import RETORNO


class BancadaRecuperacaoUnidades(BancadaConversaoSaida):
    intervalos = BancadaConversaoSaida.intervalos + (
        (0x457122, 0x45718a), (0x4530fd, 0x453129), (0x420f6e, 0x420f81))

    def adicionar_vida(self, indice, acrescimo, parada=RETORNO):
        return self.executar(0x457122, self.intervalos,
                             dict(EAX=indice, EDX=acrescimo, EBX=0xfedcba98, ECX=0x76543210),
                             parada=parada)

    def resetar_fadiga(self, indice, parada=RETORNO):
        return self.executar(0x4530fd, self.intervalos,
                             dict(EAX=indice, EDX=0xabcd1234), parada=parada)

    def recuperar_saida(self, pedido, parada=0x420f81):
        return self.executar(0x420f6e, self.intervalos,
                             dict(ESI=pedido.unidade, EBP=pedido.celula), parada=parada)
