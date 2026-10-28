"""Intact native local experience and queue/caller execution."""
from bancada_recuperacao_unidades import BancadaRecuperacaoUnidades
from emulador import RETORNO


class BancadaExperienciaUnidades(BancadaRecuperacaoUnidades):
    intervalos = BancadaRecuperacaoUnidades.intervalos + (
        (0x44f9e0, 0x44fb09), (0x44f987, 0x44f98a), (0x44fe42, 0x44ff1d),
        (0x440d58, 0x440d5e), (0x420f81, 0x420f8a))

    def carregar_mundo(self, mundo, tipos, **kwargs):
        super().carregar_mundo(mundo, tipos, **kwargs)
        self.cpu.mem_write(0x4e19c4, bytes(mundo.experiencias_unidades))

    def aplicar(self, indice, nivel, parada=RETORNO):
        return self.executar(0x44f9e0, self.intervalos, dict(EAX=indice, EDX=nivel), parada=parada)

    def consumir(self, indice, celula=0xabcd8080, parada=RETORNO):
        return self.executar(0x44fe42, self.intervalos, dict(EAX=indice, EDX=celula), parada=parada)

    def experiencia_saida(self, pedido, parada=0x420f8a):
        return self.executar(0x420f81, self.intervalos,
                             dict(ESI=pedido.unidade, EBP=pedido.celula), parada=parada)

    def estado(self):
        return super().estado() + (bytes(self.cpu.mem_read(0x4e19c4, 40)),)
