"""Isolated original cleanup frame and complete BagVide; no native mocks."""
import struct
from bancada_recrutamento import BancadaRecrutamento,TRECHOS_RECRUTAMENTO
from construcoes import BASE_CONSTRUCOES
from emulador import RETORNO,PILHA

TRECHOS_LIMPEZA=TRECHOS_RECRUTAMENTO+[(0x420fb7,0x421250),(0x4471b8,0x4472d3)]


class BancadaLimpezaSaida(BancadaRecrutamento):
    def __init__(self):
        super().__init__()
        self.retornos=0
        self.paradas_mensagem=0
        self.paradas_terreno=0

    def consultar_bag(self,indice):
        regs=self.executar(0x44724a,TRECHOS_LIMPEZA,
                           dict(EAX=BASE_CONSTRUCOES+(indice&65535)*276+0xc))
        self.retornos+=1
        return bool(regs['EAX']&255)

    def limpar(self,indice,unidade):
        # The actual original caller already allocated this frame. This isolated
        # fixture declares it explicitly; it does not pretend to run that prefix.
        regs=self.executar(0x420fb7,TRECHOS_LIMPEZA,
             dict(ESP=PILHA+0x8004,EDI=BASE_CONSTRUCOES+(indice&65535)*276,ESI=unidade&65535),
             pilha={4:struct.pack('<I',indice&0xffffffff),8:struct.pack('<I',unidade&0xffffffff)},
             parada={0x42110c,0x4211d3})
        self.paradas_mensagem+=regs['EIP']==0x4211d3
        self.paradas_terreno+=regs['EIP']==0x42110c
        return regs
