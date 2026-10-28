"""Original mission insertion and raw predicates with preserved-state stepping."""
from bancada_colocacao_saida import BancadaColocacaoSaida
from emulador import RETORNO,UNIDADES


class BancadaColocacaoMissao(BancadaColocacaoSaida):
    intervalos=BancadaColocacaoSaida.intervalos+[(0x456fa6,0x457058),(0x441fff,0x442025),(0x4465bf,0x4465df)]

    def colocar_missao(self,indice,parada=RETORNO):
        return self.executar(0x456fa6,self.intervalos,dict(EAX=indice),parada=parada,limite_instrucoes=1000000)

    def carregar_consulta(self,mundo):
        self.cpu.mem_write(UNIDADES,bytes(mundo.unidades))

    def existe(self,indice):
        return self.executar(0x441fff,self.intervalos,dict(EAX=indice,EDX=0xabcd1234))

    def visibilidade(self,indice):
        return self.executar(0x4465bf,self.intervalos,dict(EAX=indice,EDX=0xabcd1234))
