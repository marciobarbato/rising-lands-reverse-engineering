"""AvanceEngin e mensagens originais, com grades/visão/minimapa sintéticos."""
import struct
from bancada_ordens import BancadaOrdens
from emulador import UNIDADES
from ordens_unidades import BASE_GRUPOS

INTERVALOS_AVANCO = [
    (0x448704, 0x448b3f), (0x442cb4, 0x44302e), (0x43e138, 0x43e2a3),
    (0x47622e, 0x476251), (0x46a388, 0x46a70c),
    (0x4765f4, 0x476647), (0x4766f0, 0x47693e), (0x476951, 0x477042),
    (0x46003b, 0x460051), (0x47954c, 0x479555),
    (0x452cc8, 0x452ef7), (0x428cc0, 0x428e71), (0x440d58, 0x440d5e),
    (0x448194, 0x448270), (0x448599, 0x448699), (0x448b9f, 0x448d08), (0x44f29d, 0x44f2a3),
    (0x442668, 0x442bc9), (0x44246e, 0x442586), (0x4761d4, 0x4761f1),
    (0x477042, 0x4770ee), (0x4563da, 0x4564ef),
    (0x483ed7, 0x484135), (0x46d817, 0x46d838), (0x47da39, 0x47da7a),
    (0x4841f4, 0x484214), (0x481f1a, 0x481f2e), (0x481c93, 0x481c9b),
]


class BancadaAvanco(BancadaOrdens):
    intervalos = BancadaOrdens.intervalos + INTERVALOS_AVANCO

    def __init__(self):
        super().__init__()
        self.cpu.mem_map(0x1400000, 0x300000)
        proxima = 0x1400000
        self.grades = {}
        for nome, tamanho in [('atributos',65536),('regioes',131072),('tiles',131072),
                              ('donos_objetos',65536),('mini_final',65536),('mini_unidades',65536),('mini_estruturas',65536),
                              ('descoberto',262144),('luz_bordas',262144),('contagem_luz',262144),
                              ('sombra',4096),('jogadores',4096),('ponteiros_rotas',4096),('rotas',409600)]:
            self.grades[nome] = proxima
            proxima += (tamanho + 4095) & ~4095
        for global_,nome in [(0x507da8,'atributos'),(0x4e0f38,'regioes'),(0x507d70,'tiles'),
                             (0x507dac,'donos_objetos'),(0x507d5c,'mini_final'),(0x507d60,'mini_unidades'),
                             (0x507d64,'mini_estruturas'),(0x4e24b4,'sombra'),(0x5080a8,'jogadores'),
                             (0x4e1924,'ponteiros_rotas')]:
            self.cpu.mem_write(global_,struct.pack('<I',self.grades[nome]))
        for nome,global_ in [('descoberto',0x507d78),('luz_bordas',0x507d88),('contagem_luz',0x507d98)]:
            for i in range(4): self.cpu.mem_write(global_+i*4,struct.pack('<I',self.grades[nome]+i*65536))
        self.cpu.mem_write(self.grades['ponteiros_rotas'],struct.pack('<800I',*(self.grades['rotas']+i*512 for i in range(800))))

    def carregar_fisica(self, mundo):
        self.carregar_mundo(mundo)
        self.cpu.mem_write(0x497168,struct.pack('<HH',mundo.largura,mundo.altura))
        self.cpu.mem_write(0x496fe0,struct.pack('<HH',*mundo.tamanho_minimapa))
        self.cpu.mem_write(0x508041,bytes([mundo.jogador_local]))
        self.cpu.mem_write(0x4e24dc,bytes(mundo.cores_jogadores))
        self.cpu.mem_write(0x509694,bytes(mundo.cores_tiles))
        for i in range(4): self.cpu.mem_write(self.grades['jogadores']+i*20+1,bytes([mundo.controle_jogadores[i]]))
        for tipo,limite in enumerate(mundo.limites_fadiga):
            self.cpu.mem_write(0x4965dc+tipo*50,struct.pack('<H',limite))
            for dono in range(4):
                self.cpu.mem_write(0x4dfba0+dono*468+tipo*18,struct.pack('<H',mundo.bonus_fadiga[dono][tipo]))
        for nome in ('atributos','donos_objetos','mini_final','mini_unidades','mini_estruturas','sombra'):
            self.cpu.mem_write(self.grades[nome],bytes(getattr(mundo,nome)))
        for nome in ('regioes','tiles'):
            self.cpu.mem_write(self.grades[nome],struct.pack('<65536H',*getattr(mundo,nome)))
        for nome in ('descoberto','luz_bordas','contagem_luz'):
            self.cpu.mem_write(self.grades[nome],b''.join(bytes(g) for g in getattr(mundo,nome)))
        for i,rota in enumerate(mundo.rotas):
            self.cpu.mem_write(self.grades['rotas']+i*512,bytes(rota))

    def conferir_fisica(self, mundo):
        erros = self.conferir_mundo(mundo)
        for nome in ('atributos','donos_objetos','mini_final','mini_unidades','mini_estruturas','sombra','regioes','tiles',
                     'descoberto','luz_bordas','contagem_luz'):
            valor = getattr(mundo,nome)
            if nome in ('regioes','tiles'): esperado = struct.pack('<65536H',*valor)
            elif nome in ('descoberto','luz_bordas','contagem_luz'): esperado = b''.join(bytes(g) for g in valor)
            else: esperado = bytes(valor)
            atual = bytes(self.cpu.mem_read(self.grades[nome],len(esperado)))
            if atual != esperado:
                offsets=[i for i,(a,b) in enumerate(zip(atual,esperado)) if a!=b]
                erros.append(dict(regiao=nome,offsets=offsets[:10],valores=[(atual[i],esperado[i]) for i in offsets[:10]],total=len(offsets)))
        for i,rota in enumerate(mundo.rotas):
            if bytes(self.cpu.mem_read(self.grades['rotas']+i*512,len(rota))) != bytes(rota):
                erros.append(dict(rota=i))
        return erros

    def avancar(self, indice, desconto=0):
        self.executar(0x448704,self.intervalos,dict(EAX=indice,EDX=desconto),limite_instrucoes=1000000)

    def concluir(self, indice):
        return self.executar(0x4563da,self.intervalos,dict(ESI=UNIDADES+indice*276,EDI=indice),
                             parada=(0x454ccd,0x4555a7,0x455a6f))

    def notificar(self, indice):
        self.executar(0x483ed7,self.intervalos,dict(EAX=indice))

    def escolher_proximo(self, indice):
        self.executar(0x448b9f,self.intervalos,dict(EAX=indice),limite_instrucoes=1000000)

    def girar(self, indice):
        self.executar(0x448599,self.intervalos,dict(EAX=indice))
