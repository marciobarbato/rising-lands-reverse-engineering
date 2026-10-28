"""Portões x86 com checkpoints entre blocos da varredura dos 1.000 registros."""
from bancada_colocacao_estruturas import BancadaColocacaoEstruturas
from emulador import RETORNO,x86


class BancadaPortoes(BancadaColocacaoEstruturas):
    intervalos=BancadaColocacaoEstruturas.intervalos+[
        (0x4191fd,0x419233),(0x41934f,0x4199a3),(0x41c87f,0x41c887),
        (0x4268d4,0x426918),(0x427bb7,0x427d5d),(0x4281c0,0x4281c7),
    ]

    def __init__(self):
        self._checkpoints_portoes=False
        self._ultimo_bloco_portoes=-1
        super().__init__()

    def _conferir_endereco(self,cpu,endereco,tamanho,dados):
        if self._checkpoints_portoes and endereco in (0x41977a,0x4198cb):
            i=cpu.reg_read(x86.UC_X86_REG_ESI)
            if i%32==0 and i!=self._ultimo_bloco_portoes:
                self._ultimo_bloco_portoes=i
                self.paradas.add(endereco)
                cpu.emu_stop()
                return
        super()._conferir_endereco(cpu,endereco,tamanho,dados)

    def _com_checkpoints(self,entrada,registradores):
        self._checkpoints_portoes=True
        self._ultimo_bloco_portoes=-1
        try:
            r=self.executar(entrada,self.intervalos,registradores,limite_instrucoes=1000000)
            for _ in range(40):
                if r['EIP']==RETORNO:return r
                r=self.retomar(r['EIP'],self.intervalos,limite_instrucoes=1000000)
            raise RuntimeError('Varredura de portões excedeu os checkpoints declarados')
        finally:self._checkpoints_portoes=False

    def predicado(self,endereco,indice):
        return bool(self.executar(endereco,self.intervalos,dict(EAX=indice))['EAX']&255)

    def liberar(self,celula,indice):
        return self._com_checkpoints(0x4193d4,dict(EAX=celula,EDX=indice))

    def bloquear(self,celula,indice):
        return self._com_checkpoints(0x4195ca,dict(EAX=celula,EDX=indice))

    def alternar(self,celula,indice):
        return self._com_checkpoints(0x419917,dict(EAX=celula,EDX=indice))

    def avancar_portao(self,indice):
        # Entradas reais com a ação de mouse desativada. O despacho de tipo,
        # o ramo do portão e seus auxiliares são executados integralmente.
        self.cpu.mem_write(0x5099af,b'\0')
        return self.executar(0x4268d4,self.intervalos,dict(EAX=indice),limite_instrucoes=1000000)
