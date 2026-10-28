"""Unpatched CalculTroupe through cleanup or an explicit earlier dependency."""
from bancada_producao_solicitada import BancadaProducaoSolicitada
from bancada_limpeza_saida import TRECHOS_LIMPEZA
from emulador import RETORNO, x86
from producao import CONTROLE_X87_INICIAL


class BancadaProducaoLimpa(BancadaProducaoSolicitada):
    intervalos = BancadaProducaoSolicitada.intervalos + TRECHOS_LIMPEZA

    def __init__(self):
        super().__init__()
        self.paradas_mensagem = 0
        self.paradas_terreno = 0
        self.paradas_importacao_reset = 0

    def calcular_limpo(self, indice, *, parada=None):
        self.efeitos = []
        self.cpu.reg_write(x86.UC_X86_REG_FPCW, CONTROLE_X87_INICIAL)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW, 0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG, 0xffff)
        alvos = ({RETORNO,0x4211d3,0x42110c} if parada is None else
                 {RETORNO,{'som':0x440de7,'volume':0x440d9f,
                           'reset_reter':0x42116e,'reset_vazio':0x421097}[parada]})
        regs = self.executar(0x4259e6, self.intervalos, dict(EAX=indice),
                             parada=alvos, limite_instrucoes=1000000)
        self.retornos += regs['EIP'] == RETORNO
        self.paradas_mensagem += regs['EIP'] == 0x4211d3
        self.paradas_terreno += regs['EIP'] == 0x42110c
        self.paradas_volume += regs['EIP'] == 0x440d9f
        self.paradas_som += regs['EIP'] == 0x440de7
        self.paradas_importacao_reset += regs['EIP'] in (0x42116e,0x421097)
        return regs
