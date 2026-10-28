"""Full original producer plus actual core physical harness and CPU resumptions."""
import struct
from types import SimpleNamespace

from bancada_colocacao_saida import BancadaColocacaoSaida
from bancada_ciclo_producao import TRECHOS_CICLO
from bancada_economia import BancadaEconomia
from bancada_recrutamento import BancadaRecrutamento
from bancada_producao import BancadaProducao
from construcoes import BASE_CAPACIDADES,BASE_CONSTRUCOES
from bonus_unidades import BASE_BONUS_UNIDADES
from emulador import RETORNO,unicorn,x86
from producao import CONTROLE_X87_INICIAL


class BancadaProducaoColocada(BancadaColocacaoSaida):
    intervalos=BancadaColocacaoSaida.intervalos+TRECHOS_CICLO
    guardas_recrutamento=BancadaRecrutamento.guardas_recrutamento

    def __init__(self):
        super().__init__(segmentar=True)
        self.retornos=0
        self.paradas_pedido=0
        self.paradas_visao=0
        self.paradas_importacao=0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE,self._deposito)

    def _deposito(self,cpu,endereco,tamanho,_):
        if endereco==0x42340f:
            self.efeitos.append(('deposit',*(cpu.reg_read(getattr(x86,'UC_X86_REG_'+r))&m
                  for r,m in (('EBX',255),('EAX',255),('EDX',65535),('ECX',65535)))))

    def _carregar_economia(self,mundo):
        BancadaEconomia.carregar(self,mundo.economia.memoria)
        self.cpu.mem_write(BASE_CAPACIDADES,bytes(mundo.capacidades.memoria))
        self.cpu.mem_write(BASE_CONSTRUCOES,bytes(mundo.estruturas))
        self.cpu.mem_write(0x497164,struct.pack('<I',mundo.terreno.semente))
        # 507d74/507dac stay core's actual raw objects/owner pointers. Do not
        # install the economy-only harness's different synthetic addresses.

    def carregar_produtor(self,p,mundo,bonus):
        self.carregar_saida(mundo,p.recrutamento.tipos_unidades)
        # Reuse only data-loading methods in a separate adapter; overriding
        # core's carregar_mundo would break its physical loader dispatch.
        dados=SimpleNamespace(cpu=self.cpu,carregar_mundo=self._carregar_economia)
        dados.carregar_recrutamento=lambda r:BancadaRecrutamento.carregar_recrutamento(dados,r)
        BancadaProducao.carregar_producao(dados,p)
        self.cpu.mem_write(BASE_BONUS_UNIDADES,bytes(bonus.memoria))
        self.cpu.mem_write(0x49a070,bytes(mundo.realizaveis_estruturas))
        self.efeitos=[]

    def estado_economico(self):
        r=BancadaRecrutamento.estado_recrutamento(self)
        r.update(BancadaProducao.estado_producao(self))
        r.update(economia=BancadaEconomia.memoria(self),
                 capacidades=bytes(self.cpu.mem_read(BASE_CAPACIDADES,24)),
                 semente=struct.unpack('<I',self.cpu.mem_read(0x497164,4))[0])
        return r

    def calcular_produtor(self,indice,*,parar_visao=False,parar_importacao=False):
        self.efeitos=[]
        self.cpu.reg_write(x86.UC_X86_REG_FPCW,CONTROLE_X87_INICIAL)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW,0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG,0xffff)
        alvo=0x446146 if parar_visao else (0x420f8a if parar_importacao else 0x420f9e)
        regs=self.executar(0x4259e6,self.intervalos,dict(EAX=indice),
                           parada={RETORNO,alvo},limite_instrucoes=1000000)
        self.retornos+=regs['EIP']==RETORNO
        self.paradas_pedido+=regs['EIP']==0x420f9e
        self.paradas_visao+=regs['EIP']==0x446146
        self.paradas_importacao+=regs['EIP']==0x420f8a
        return regs
