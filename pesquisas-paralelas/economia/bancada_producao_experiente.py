"""Actual original production entry through recruitment queue consumption."""
from bancada_producao_compartilhada import BancadaProducaoCompartilhada,TRECHOS_COMPARTILHADOS
from bancada_experiencia_unidades import BancadaExperienciaUnidades
from emulador import RETORNO,x86
from producao import CONTROLE_X87_INICIAL

TRECHOS_EXPERIENTES=TRECHOS_COMPARTILHADOS+list(BancadaExperienciaUnidades.intervalos)


class BancadaProducaoExperiente(BancadaProducaoCompartilhada):
    def __init__(self):
        super().__init__()
        self.paradas_colocacao=0
        self.paradas_pos_recuperacao=0

    def carregar_experiente(self,p,mundo,bonus):
        self.carregar_compartilhado(p,mundo,bonus)
        # Invalid protected Python queues are compared before their native use.
        fila=mundo.experiencias_unidades
        self.cpu.mem_write(0x4e19c0,b'\x39'*4+bytes(fila[:40]).ljust(40,b'\xa5')+b'\x93'*4)
        self.fila_antes=bytes(self.cpu.mem_read(0x4e19c0,48))

    def calcular_experiente(self,indice,*,parar_recuperacao=False):
        self.saidas_tropa.clear()
        self.chamadas.clear()
        self.consultas.clear()
        self.depositos.clear()
        self.cpu.reg_write(x86.UC_X86_REG_FPCW,CONTROLE_X87_INICIAL)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW,0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG,0xffff)
        alvo=0x420f81 if parar_recuperacao else 0x420f8a
        regs=self.executar(0x4259e6,TRECHOS_EXPERIENTES,dict(EAX=indice),
                           parada={RETORNO,alvo},limite_instrucoes=1000000)
        self.retornos+=regs['EIP']==RETORNO
        self.paradas_colocacao+=regs['EIP']==0x420f8a
        self.paradas_pos_recuperacao+=regs['EIP']==0x420f81
        return regs
