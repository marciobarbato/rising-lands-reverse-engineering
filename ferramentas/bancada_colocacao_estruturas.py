"""PlaceBatiment e auxiliares x86 com chamadas internas originais."""
import struct
from bancada_terreno_estruturas import BancadaTerrenoEstruturas


class BancadaColocacaoEstruturas(BancadaTerrenoEstruturas):
    intervalos = BancadaTerrenoEstruturas.intervalos + [
        (0x41ac8b,0x41ad78),(0x41c18a,0x41c451),(0x41c4ac,0x41c652),
    ]

    def carregar_navegacao(self,mundo):
        super().carregar_navegacao(mundo)
        self.cpu.mem_write(0x495bf8,bytes([mundo.objeto_muro&255,mundo.objeto_portao&255]))

    def combinacao(self,celula):
        return self.executar(0x41c18a,self.intervalos,dict(EAX=celula))['EAX']&255

    def validar_portao(self,celula):
        return self.executar(0x41ac8b,self.intervalos,dict(EAX=celula))['EAX']&255

    def colocar(self,indice,mascara_tipo20=None):
        if mascara_tipo20 is not None:
            if len(mascara_tipo20)!=20:raise ValueError('São necessários 20 bytes da máscara em RAM')
            self.cpu.mem_write(0x4dfb9c,bytes(mascara_tipo20))
        return self.executar(0x41c4ac,self.intervalos,dict(EAX=indice),limite_instrucoes=1000000)

    def atualizar_vizinhos(self,celula):
        return self.executar(0x41c251,self.intervalos,dict(EAX=celula),limite_instrucoes=1000000)
