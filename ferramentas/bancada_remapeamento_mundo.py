"""Intact original remap reset, stopping before the first Windows allocation."""
import struct

from bancada_colocacao_saida import BancadaColocacaoSaida
from emulador import x86, unicorn

CORES = 0x1800000


class BancadaRemapeamentoMundo(BancadaColocacaoSaida):
    intervalos = BancadaColocacaoSaida.intervalos + [
        (0x42ee1c,0x42f1e1),(0x48c3b0,0x48c3c8),(0x48d890,0x48d933)]

    def __init__(self):
        super().__init__()
        self.cpu.mem_map(CORES,65536)
        self.cpu.mem_write(0x4e156c,struct.pack('<I',CORES))
        self.preenchimentos = []
        self.rastrear = False
        self.escritas = []
        self.cpu.hook_add(unicorn.UC_HOOK_CODE,self._observar_preenchimento)
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE,self._observar_escrita)

    def _observar_preenchimento(self,cpu,endereco,tamanho,_):
        if endereco == 0x48c3b0 and endereco not in self.paradas:
            eax,edx,ebx = (cpu.reg_read(getattr(x86,'UC_X86_REG_'+r)) for r in ('EAX','EDX','EBX'))
            nomes = {CORES:'colors',0x4e1670:'released',self.grades['regioes']:'regions'}
            self.preenchimentos.append((nomes[eax],edx & 255,ebx))
            if self.rastrear:
                self.escritas.append(('fill',nomes[eax],edx & 255,ebx))

    def _observar_escrita(self,cpu,acesso,endereco,tamanho,valor,_):
        if not self.rastrear:
            return
        valor &= (1 << (tamanho*8))-1
        nomes = {0x4e0f36:'ocupada',0x4e0f37:'sucesso',0x4e0f3c:'ponteiro_rota',0x496304:'unidade'}
        if endereco in nomes:
            self.escritas.append(('search',nomes[endereco],valor))
        elif 0x4e1570 <= endereco < 0x4e1670:
            self.escritas.append(('free',endereco-0x4e1570,valor))

    def carregar_remapeamento(self,mundo):
        self.carregar_saida(mundo)
        self.cpu.mem_write(CORES,bytes(mundo.cores_estruturas.grade))
        self.cpu.mem_write(0x4e1570,bytes(mundo.cores_estruturas.livres))
        self.cpu.mem_write(0x4e1670,bytes(mundo.cores_estruturas.liberadas))
        self.preenchimentos = []
        self.escritas = []

    def iniciar(self,parada=0x42eebd):
        return self.executar(0x42ee1c,self.intervalos,parada=parada,limite_instrucoes=1000000)

    def conferir_remapeamento(self,mundo):
        erros = self.conferir_saida(mundo)
        for nome,endereco in (('grade',CORES),('livres',0x4e1570),('liberadas',0x4e1670)):
            esperado = bytes(getattr(mundo.cores_estruturas,nome))
            if bytes(self.cpu.mem_read(endereco,len(esperado))) != esperado:
                erros.append(dict(region='colors_'+nome))
        return erros
