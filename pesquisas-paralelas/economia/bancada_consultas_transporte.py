"""Full original read-only transport queries and actual structure-type getter."""
from bancada_recrutamento import BancadaRecrutamento,TRECHOS_RECRUTAMENTO
from emulador import RETORNO

TRECHOS_CONSULTAS=TRECHOS_RECRUTAMENTO+[(0x456cd9,0x456d92),(0x41a4f4,0x41a513)]


class BancadaConsultasTransporte(BancadaRecrutamento):
    def __init__(self):
        super().__init__()
        self.retornos=0
        self.paradas_indice=0

    def consultar(self,entrada,indice,argumento,modo=0,*,parar_indice=False):
        regs=self.executar(entrada,TRECHOS_CONSULTAS,
             dict(EAX=indice,EDX=argumento,EBX=modo,ECX=0x12345678,ESI=0x89abcdef,EDI=0x76543210,EBP=0xfedcba98),
             parada=0x41a4f4 if parar_indice else RETORNO)
        self.retornos+=regs['EIP']==RETORNO
        self.paradas_indice+=regs['EIP']==0x41a4f4
        return regs
