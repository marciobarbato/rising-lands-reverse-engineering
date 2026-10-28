"""Full original producer through request returns or exact dependency calls."""
from bancada_producao_colocada import BancadaProducaoColocada
from bancada_voz_unidades import BancadaVozUnidades
from emulador import RETORNO, x86
from producao import CONTROLE_X87_INICIAL


class BancadaProducaoSolicitada(BancadaProducaoColocada):
    intervalos = BancadaProducaoColocada.intervalos + list(BancadaVozUnidades.intervalos)
    pedido_som = BancadaVozUnidades.pedido_som

    def __init__(self):
        super().__init__()
        self.paradas_limpeza = 0
        self.paradas_volume = 0
        self.paradas_som = 0
        self.paradas_importacao_voz = 0

    def carregar_solicitado(self, p, mundo, bonus, janela):
        self.carregar_produtor(p, mundo, bonus)
        # Missing Python viewport data is compared before the original volume
        # call; these deterministic native words are never consumed there.
        BancadaVozUnidades.carregar_consulta(self, mundo, (0,0,0,0) if janela is None else janela)

    def calcular_solicitado(self, indice, *, parada='limpeza'):
        self.efeitos = []
        self.cpu.reg_write(x86.UC_X86_REG_FPCW, CONTROLE_X87_INICIAL)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW, 0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG, 0xffff)
        alvo = {'limpeza':0x420fb7, 'volume':0x440d9f, 'som':0x440de7, 'import':0x420f9e}[parada]
        regs = self.executar(0x4259e6, self.intervalos, dict(EAX=indice),
                             parada={RETORNO,alvo}, limite_instrucoes=1000000)
        self.retornos += regs['EIP'] == RETORNO
        self.paradas_limpeza += regs['EIP'] == 0x420fb7
        self.paradas_volume += regs['EIP'] == 0x440d9f
        self.paradas_som += regs['EIP'] == 0x440de7
        self.paradas_importacao_voz += regs['EIP'] == 0x420f9e
        return regs
