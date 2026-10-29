"""Referência original até RET; só autoriza o ramo biblioteca de CalculTroupe."""
import struct

from bancada_producao import BancadaProducao, TRECHOS_PRODUCAO
from bancada_proprietarios import TABELA_ORDENS, ORDENS
from emulador import RETORNO, unicorn, x86
from aprendizagem import BASE_INVENCOES
from producao import CONTROLE_X87_INICIAL
from proprietarios import (BASE_BIBLIOTECAS, BASE_BALOES, BASE_NUMEROS_UNIDADES,
                           BASE_PENDENCIAS, BASE_SORTILEGIOS, BASE_JOGADOR_DEPOSITO,
                           PASSO_ORDENS_JOGADOR, juntar_ordens)

TRECHOS_APRENDIZAGEM = TRECHOS_PRODUCAO + [
    (0x4259e6, 0x425a4b), (0x425e99, 0x4260aa), (0x4263e5, 0x426401),
    (0x42640d, 0x426418), (0x41db1d, 0x41db24),
    (0x41a4c4, 0x41a513), (0x41f3ed, 0x41f46e),
    (0x474958, 0x474b08), (0x447148, 0x447197),
    (0x447483, 0x4474a6), (0x4474c7, 0x4474f3),
    (0x41c76c, 0x41c7ea), (0x41cb01, 0x41cb4d), (0x41c87f, 0x41c887),
]


class BancadaAprendizagem(BancadaProducao):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(TABELA_ORDENS, 0x5000)
        self.cpu.mem_write(0x4e19b8, struct.pack('<I', TABELA_ORDENS))
        self.cpu.mem_write(TABELA_ORDENS, struct.pack('<4I', *(ORDENS + j * PASSO_ORDENS_JOGADOR for j in range(4))))
        self.acessos_aprendizagem = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE, self._registrar_aprendizagem)

    def _registrar_aprendizagem(self, cpu, endereco, tamanho, _):
        if endereco in (0x47476a, 0x474958, 0x474974, 0x474991, 0x474a38,
                        0x41c76c, 0x447148, 0x447483, 0x41a4c4, 0x41f3ed):
            self.acessos_aprendizagem.append(dict(entrada=endereco,
                **{r: cpu.reg_read(getattr(x86, 'UC_X86_REG_' + r)) for r in ('EAX', 'EDX', 'EBX')}))

    def carregar_aprendizagem(self, a):
        self.carregar_producao(a.producao)
        p = a.propriedade
        for base, bloco in ((BASE_BIBLIOTECAS, p.bibliotecas), (BASE_BALOES, p.baloes),
                            (BASE_NUMEROS_UNIDADES, p.numeros_unidades), (BASE_PENDENCIAS, p.pendencias)):
            self.cpu.mem_write(base, bytes(bloco))
        # Pendências começam imediatamente depois dos 1000 registros de construção.
        self.cpu.mem_write(BASE_PENDENCIAS + 9152, b'\xb2' * 8)
        # Native layout kept contiguous (owner stride 2,704); Python owns four pools.
        self.cpu.mem_write(ORDENS - 8, b'\xf1' * 8 + juntar_ordens(p.ordens) + b'\x1f' * 8)
        # A segunda tabela é dado vivo; não é a antiga guarda de sortilégios.
        self.cpu.mem_write(BASE_SORTILEGIOS - 8,
                           b'\xd3' * 8 + bytes(p.sortilegios) + bytes(a.inventados) + b'\x3d' * 8)
        self.cpu.mem_write(BASE_JOGADOR_DEPOSITO, bytes([p.jogador_deposito]))

    def estado_aprendizagem(self):
        return dict(bibliotecas=bytes(self.cpu.mem_read(BASE_BIBLIOTECAS, 4)),
                    baloes=bytes(self.cpu.mem_read(BASE_BALOES, 32)),
                    numeros_unidades=bytes(self.cpu.mem_read(BASE_NUMEROS_UNIDADES, 208)),
                    pendencias=bytes(self.cpu.mem_read(BASE_PENDENCIAS, 9152)),
                    ordens=bytes(self.cpu.mem_read(ORDENS, 10816)),
                    sortilegios=bytes(self.cpu.mem_read(BASE_SORTILEGIOS, 20)),
                    inventados=bytes(self.cpu.mem_read(BASE_INVENCOES, 20)),
                    jogador_deposito=self.cpu.mem_read(BASE_JOGADOR_DEPOSITO, 1)[0])

    def guardas_aprendizagem(self):
        return self.guardas_producao() + tuple(bytes(self.cpu.mem_read(a, 8)) for a in
            (BASE_PENDENCIAS + 9152, ORDENS - 8, ORDENS + 10816,
             BASE_SORTILEGIOS - 8, BASE_INVENCOES + 20))

    def chamar_aprendizagem(self, entrada, eax=0, edx=0, registradores=None):
        regs = dict(registradores or {})
        regs.update(EAX=eax, EDX=edx)
        self.cpu.reg_write(x86.UC_X86_REG_FPCW, CONTROLE_X87_INICIAL)
        self.cpu.reg_write(x86.UC_X86_REG_FPSW, 0)
        self.cpu.reg_write(x86.UC_X86_REG_FPTAG, 0xffff)
        self.acessos_aprendizagem.clear()
        self.acessos_producao.clear()
        return self.executar(entrada, TRECHOS_APRENDIZAGEM, regs, parada=RETORNO)
