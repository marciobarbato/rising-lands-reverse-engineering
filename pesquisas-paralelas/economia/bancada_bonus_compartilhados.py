"""Whole original BonusSetEngin -> refresh -> real economic queries."""
from bancada_mutacoes_bonus import TRECHOS_MUTACOES
from bancada_capacidades_unidades import BancadaCapacidadesUnidades
from emulador import RETORNO,UNIDADES,unicorn,x86


class BancadaBonusCompartilhados(BancadaCapacidadesUnidades):
    intervalos=tuple(TRECHOS_MUTACOES)+BancadaCapacidadesUnidades.intervalos

    def __init__(self):
        super().__init__()
        self.retornos=0
        self.paradas_consulta=0
        self.escritas=[]
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE,self._escrita)

    def _escrita(self,cpu,acesso,endereco,tamanho,valor,_):
        if 0x4dfb98<=endereco<0x4e0300 or UNIDADES<=endereco<UNIDADES+220808:
            self.escritas.append((endereco,tamanho,valor&((1<<(8*tamanho))-1)))

    def carregar_compartilhado(self,bonus,mundo):
        self.carregar(mundo.unidades,bonus.memoria)
        self.cpu.mem_write(UNIDADES+220800,b'\x36'*8)
        self.cpu.mem_write(0x4dfb98,b'\xa7'*8+bytes(bonus.memoria)+b'\x7a'*8)
        self.cpu.mem_write(0x4965ae-4,b'\xd5'*4+bytes(bonus.tipos_unidades)+b'\x5d'*4)
        self.escritas=[]

    def definir(self,jogador,tipo,seletor,valor,checkpoint=None):
        self.checkpoint=checkpoint
        r=self.executar(0x428878,self.intervalos,dict(EAX=jogador,EBX=tipo,EDX=seletor,ECX=valor),
                        limite_instrucoes=200000)
        self.retornos+=r['EIP']==RETORNO
        self.paradas_consulta+=r['EIP']!=RETORNO
        return r
