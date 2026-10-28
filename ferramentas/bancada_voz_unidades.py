"""Original volume/request routines; sound insertion stops before its CALL."""
import struct

from bancada_colocacao_saida import BancadaColocacaoSaida
from bancada_posicao_saida import REGISTROS
from emulador import RETORNO, UNIDADES


class BancadaVozUnidades(BancadaColocacaoSaida):
    intervalos = BancadaColocacaoSaida.intervalos + [
        (0x472174,0x4721a8),(0x440c5d,0x440df0),(0x420f9e,0x420fb7),
        (0x479555,0x4795af)]

    def carregar_voz(self,mundo,janela=(0,0,0,0),tipos=None):
        self.carregar_saida(mundo,tipos)
        self.cpu.mem_write(0x508720,struct.pack('<4H',*(v & 65535 for v in janela)))

    def carregar_consulta(self,mundo,janela=(0,0,0,0)):
        self.cpu.mem_write(UNIDADES,bytes(mundo.unidades))
        self.cpu.mem_write(0x508041,bytes([mundo.jogador_local]))
        self.cpu.mem_write(0x508720,struct.pack('<4H',*(v & 65535 for v in janela)))

    def selecionada(self,dono,indice):
        return self.executar(0x472174,self.intervalos,dict(EAX=dono,EDX=indice))['EAX'] & 255

    def volume(self,indice):
        return self.executar(0x440c5d,self.intervalos,dict(EAX=indice,EDX=0x12340010))['EAX']

    def solicitar(self,indice,modo,flag,parada=RETORNO):
        return self.executar(0x440d5e,self.intervalos,dict(EAX=indice,EDX=modo,EBX=flag),parada=parada)

    def retomar_solicitacao(self,pedido,parada=0x420fb7):
        return self.executar(0x420f9e,self.intervalos,
                             dict(EDI=REGISTROS+(pedido.indice & 65535)*276,ESI=pedido.unidade),parada=parada)

    def pedido_som(self,regs):
        return dict(opcode=regs['EAX'],codigo=regs['EDX'],flag=regs['ECX'],
                    volume=struct.unpack('<I',self.cpu.mem_read(regs['ESP'],4))[0],
                    offset_handle=regs['EBX']-UNIDADES)
