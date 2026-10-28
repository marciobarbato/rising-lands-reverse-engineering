"""Original MissionPlaceTerrain unit/capacity prefix, using core's harness."""
import struct
import ambiente_missoes
from bancada_colocacao_saida import BancadaColocacaoSaida
from bancada_capacidades_unidades import BancadaCapacidadesUnidades
from bancada_unidades import BancadaCargaUnidades
from emulador import UNIDADES,x86,unicorn

INTERVALS=list(BancadaColocacaoSaida.intervalos)+list(BancadaCapacidadesUnidades.intervalos)+[
    (0x46c122,0x46c16d),(0x441fff,0x442025),(0x4465bf,0x4465df),(0x456fa6,0x457058)]


class BancadaTerrenoUnidades(BancadaColocacaoSaida):
    def __init__(self):
        super().__init__(segmentar=True)
        self.loads=self.returned=self.dependency_stops=0
        self.prefixes=0
        self.prefix_returns=self.prefix_dependency_stops=0
        self.unit_load_segments=self.prefix_segments=0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE,self._parent_call)

    def _parent_call(self,cpu,address,size,_):
        if (address==getattr(self,'stop_address',None) and
                (self.stop_unit_index is None or self.current_place_index==self.stop_unit_index)):
            self.paradas.add(address)
            cpu.emu_stop()
            return
        names={0x441fff:'exists',0x4465bf:'visible',0x456fa6:'place',0x4475ef:'capacity_refresh'}
        if address in names and address not in self.paradas:
            value=cpu.reg_read(x86.UC_X86_REG_EAX)
            if address==0x456fa6:
                self.current_place_index=value&65535
            self.parent_calls.append((names[address],value&(255 if address==0x4475ef else 65535)))

    def carregar_caso(self,world,data,offset,types,bonuses,loader_bytes):
        self.stop_address=None
        self.stop_unit_index=self.current_place_index=None
        self.parent_calls=[]
        self.carregar_saida(world,types)
        before=self.execucoes
        BancadaCargaUnidades.carregar(self,bytes(data),offset,world.unidades,loader_bytes,types,bonuses,
                                      selecoes=world.selecoes_unidades)
        self.unit_load_segments+=self.execucoes-before
        self.efeitos=[];self.parent_calls=[]

    def prefixo(self,stop_address=None,stop_unit_index=None):
        self.prefixes+=1
        self.stop_address=stop_address
        self.stop_unit_index=stop_unit_index
        before=self.execucoes
        regs=self.executar(0x46c122,INTERVALS,parada=0x46c16d,limite_instrucoes=1000000)
        self.prefix_segments+=self.execucoes-before
        if regs['EIP']==0x46c16d:
            self.prefix_returns+=1
        else:
            self.prefix_dependency_stops+=1
        return regs

    def selecoes(self):
        return bytes(self.cpu.mem_read(0x508728,2048))

    def busca_original(self):
        return [struct.unpack('<'+fmt,self.cpu.mem_read(address,struct.calcsize(fmt)))[0]
                for address,fmt in ((0x496304,'H'),(0x4e0f36,'B'),(0x4e0f37,'B'),
                                     (0x4e0f3c,'I'),(0x496302,'B'))]
