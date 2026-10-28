"""Original conversion and caller fragment; no native subcall is substituted."""
import struct
from collections import Counter
from bancada_posicao_saida import BancadaPosicaoSaida, REGISTROS
from emulador import UNIDADES, RETORNO, unicorn, x86


class BancadaConversaoSaida(BancadaPosicaoSaida):
    intervalos = BancadaPosicaoSaida.intervalos + (
        (0x457350, 0x457e0c), (0x4570f0, 0x4570f4), (0x4475ac, 0x4475ef),
        (0x4474c5, 0x4474c7), (0x428cc0, 0x428e71), (0x420f5a, 0x420f6e))

    def __init__(self):
        super().__init__()
        self.chamadas = []
        self.paradas_atingidas = Counter()
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._consulta)

    def _executar_ate_parada(self, entrada, limite_instrucoes):
        regs = super()._executar_ate_parada(entrada, limite_instrucoes)
        self.paradas_atingidas[hex(regs['EIP'])] += 1
        return regs

    def _consulta(self, cpu, endereco, tamanho, _):
        if endereco in self.paradas:
            return
        if endereco == 0x4475ac:
            self.chamadas.append(('capacity', cpu.reg_read(x86.UC_X86_REG_EAX) & 255))
        elif endereco == 0x428cc0:
            dono = cpu.reg_read(x86.UC_X86_REG_EAX) & 255
            if dono not in (4, 200):
                self.chamadas.append(('bonus', dono, cpu.reg_read(x86.UC_X86_REG_EBX) & 255,
                                       cpu.reg_read(x86.UC_X86_REG_EDX) & 255))

    def carregar_mundo(self, mundo, tipos, *, mod1=0, mod12=0, tipo=0, dono=0):
        self.cpu.mem_write(UNIDADES, bytes(mundo.unidades))
        self.carregar(mundo.estruturas)
        self.cpu.mem_write(0x4965ae, bytes(tipos))
        for endereco, formato, valor in ((0x496304, 'H', mundo.busca.unidade),
                                        (0x4e0f36, 'B', mundo.busca.ocupada),
                                        (0x4e0f37, 'B', mundo.busca.sucesso),
                                        (0x4e0f3c, 'I', mundo.busca.ponteiro_rota),
                                        (0x496302, 'B', mundo.busca.concluida)):
            self.cpu.mem_write(endereco, struct.pack('<' + formato, valor))
        self.cpu.mem_write(0x4dfba0, bytes(4 * 468))
        if dono not in (4, 200):
            base = 0x4dfba0 + dono * 468 + tipo * 18
            self.cpu.mem_write(base + 11, bytes([mod1 & 255]))
            self.cpu.mem_write(base + 16, bytes([mod12 & 255]))
        self.chamadas = []

    def converter(self, indice, celula, direcao, tipo, parada=RETORNO):
        return self.executar(0x457b87, self.intervalos,
                             dict(EAX=indice, EDX=celula, EBX=direcao, ECX=tipo), parada=parada)

    def retomar_saida(self, pedido, parada=0x420f6e):
        return self.executar(0x420f5a, self.intervalos,
                             dict(EAX=pedido.indice, EBX=pedido.direcao, ESI=pedido.unidade,
                                  EDI=REGISTROS + (pedido.indice & 65535) * 276), parada=parada)

    def estado(self):
        busca = tuple(struct.unpack('<' + fmt, self.cpu.mem_read(a, struct.calcsize(fmt)))[0]
                      for a, fmt in ((0x496304, 'H'), (0x4e0f36, 'B'), (0x4e0f37, 'B'),
                                     (0x4e0f3c, 'I'), (0x496302, 'B')))
        return bytes(self.cpu.mem_read(UNIDADES, 220800)), self.registros(), busca
