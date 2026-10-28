"""Complete original unit reset and isolated inline Bag contexts, unpatched."""
from collections import Counter
import struct

from emulador import BancadaX86,UNIDADES,unicorn

PONTEIROS=0x1100000
TABELAS=tuple(0x1200000+i*0x10000 for i in range(4))


class BancadaCicloUnidades(BancadaX86):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(PONTEIROS,0x1000)
        for p in TABELAS:
            self.cpu.mem_map(p,0x1000)
        self.cpu.mem_write(0x4e19b8,struct.pack('<I',PONTEIROS))
        self.cpu.mem_write(PONTEIROS,struct.pack('<4I',*TABELAS))
        self.paradas_atingidas=Counter()
        self.rastrear=False
        self.escritas=[]
        self.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE,self._escrita)

    def _escrita(self,cpu,acesso,endereco,tamanho,valor,_):
        if not self.rastrear:
            return
        for nome,base,limite in [('units',UNIDADES,220800)]+[(f'table{i}',p,2704) for i,p in enumerate(TABELAS)]:
            if base <= endereco and endereco+tamanho <= base+limite:
                self.escritas.append((nome,endereco-base,tamanho,valor & ((1 << (tamanho*8))-1)))
                return

    def _executar_ate_parada(self,entrada,limite_instrucoes):
        r=super()._executar_ate_parada(entrada,limite_instrucoes)
        self.paradas_atingidas[hex(r['EIP'])]+=1
        return r

    def carregar_mundo(self,mundo):
        self.cpu.mem_write(UNIDADES,bytes(mundo.unidades))
        for p,tabela in zip(TABELAS,mundo.bolsas_tipos_unidades):
            self.cpu.mem_write(p,bytes(tabela))
        self.escritas=[]

    def resetar(self):
        return self.executar(0x441659,((0x441659,0x441775),),limite_instrucoes=1000000)

    def resetar_bolsa(self,dados,offset,ordem):
        self.cpu.mem_write(UNIDADES,bytes(dados))
        self.escritas=[]
        if ordem == 'tabela':
            return self.executar(0x4416b1,((0x4416b1,0x4416ce),(0x441679,0x441692)),
                                 dict(EAX=UNIDADES+offset),parada=0x441692)
        return self.executar(0x44174d,((0x44174d,0x44176d),(0x4416d2,0x4416eb)),
                             dict(EAX=UNIDADES+offset),parada=0x4416eb)

    def estado(self):
        return bytes(self.cpu.mem_read(UNIDADES,220800)),tuple(bytes(self.cpu.mem_read(p,2704)) for p in TABELAS)
