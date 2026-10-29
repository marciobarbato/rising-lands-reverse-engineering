"""Intact structure scan and joined MissionPlaceTerrain, on committed harnesses.

No engine routine is substituted. This module defines the harness only;
importing it does not construct Unicorn or execute original instructions.
"""
import hashlib
import struct
import ambiente_missoes
from bancada_reset_terreno import BancadaResetTerreno,INTERVALOS_ESTRUTURA
from bancada_colocacao_estruturas import BancadaColocacaoEstruturas
from bancada_capacidades_unidades import BancadaCapacidadesUnidades
from bancada_habitaveis import INTERVALOS_HABITAVEIS
from emulador import BASE,DESCRITORES,PILHA,RETORNO,UNIDADES,unicorn,x86
from bancada_ordens import OBJETOS
from ordens_unidades import BASE_GRUPOS

DATA=(0x494000,0x523000)
BAG_POINTERS=0x1a00000
BAG_POOLS=tuple(BAG_POINTERS+(j+1)*4096 for j in range(4))
ENTRADAS={'structures':0x46c16d,'joined':0x46c122,'predicate':0x41a735}
CHAMADAS={0x441fff:'unit_exists',0x4465bf:'unit_visible',0x456fa6:'unit_place',
          0x4475ef:'capacity_refresh',0x41a735:'structure_exists',0x41c4ac:'structure_place',
          0x41a5b8:'structure_inhabited',0x41cc70:'structure_habitable',0x419e97:'structure_map'}


class BancadaTerrenoEstruturasMissao(BancadaResetTerreno,BancadaColocacaoEstruturas):
    intervalos=(list(BancadaResetTerreno.intervalos)+list(BancadaColocacaoEstruturas.intervalos)
                +list(BancadaCapacidadesUnidades.intervalos)+list(INTERVALOS_HABITAVEIS)
                +list(INTERVALOS_ESTRUTURA)+[(0x46c122,0x46c1b8),(0x41a735,0x41a75c),
                                            (0x46b6f5,0x46b6f8)])

    def __init__(self):
        super().__init__()
        self.cpu.mem_map(BAG_POINTERS,5*4096)
        self.cpu.mem_write(0x4e19b8,struct.pack('<I',BAG_POINTERS))
        self.cpu.mem_write(BAG_POINTERS,struct.pack('<4I',*BAG_POOLS))
        self.blocos={'data':DATA}
        for inicio,fim,_ in self.cpu.mem_regions():
            if inicio not in (BASE,PILHA,RETORNO,DESCRITORES):
                self.blocos[f'arena_{inicio:08x}']=(inicio,fim+1)
        self.pristino=self.estado()
        self.chamadas=[]
        self.parada=None
        self.indice_estrutura=None
        self.entradas={nome:0 for nome in ENTRADAS}
        self.retornos=self.dependencias=0
        self.cpu.hook_add(unicorn.UC_HOOK_CODE,self._chamada_missao)

    def _chamada_missao(self,cpu,endereco,tamanho,_):
        if self.parada and endereco==self.parada[0] and self.indice_estrutura==self.parada[1]:
            self.paradas.add(endereco)
            cpu.emu_stop()
            return
        if endereco not in CHAMADAS or endereco in self.paradas:
            return
        eax=cpu.reg_read(x86.UC_X86_REG_EAX)
        valor=eax&(255 if endereco==0x4475ef else 65535)
        if endereco==0x41a735:
            self.indice_estrutura=valor
        chamada=(CHAMADAS[endereco],valor)
        if endereco==0x419e97:
            chamada+=(cpu.reg_read(x86.UC_X86_REG_EDX)&255,)
        self.chamadas.append(chamada)

    def estado(self):
        return {nome:bytes(self.cpu.mem_read(inicio,fim-inicio))
                for nome,(inicio,fim) in self.blocos.items()}

    def patches_modelo(self,caso):
        """Serialize declared Python buffers only; never compute engine effects."""
        m,e=caso.mundo,caso.economico
        for endereco,valor in ((UNIDADES,m.unidades),(0x49a0c8,m.estruturas),
                (OBJETOS,m.objetos),(BASE_GRUPOS,m.grupos),(0x4e19c4,m.experiencias_unidades),
                (0x508728,m.selecoes_unidades),(0x4dd6e8,e.pendencias),
                (0x4dfad4,e.estruturas_realizaveis),(0x4dfb2c,e.capacidades.memoria),
                (0x4e2ea8,e.economia.memoria),(0x4e1934,e.unidades_realizaveis),
                (0x508f30,e.sortilegios),(0x508f44,e.inventados),(0x4e0730,bytes([e.rede])),
                (0x4965ae,caso.tipos),(0x4dfb9c,caso.regras_runtime),
                (0x4e1570,m.cores_estruturas.livres),(0x4e1670,m.cores_estruturas.liberadas),
                (0x4e0732,struct.pack('<1024H',*m.cores_estruturas.pilha))):
            yield endereco,bytes(valor)
        yield self.grades['cores_estruturas'],bytes(m.cores_estruturas.grade)
        for base,bag in zip(BAG_POOLS,m.bolsas_tipos_unidades):
            yield base,bytes(bag)
        for nome in ('atributos','donos_objetos','mini_final','mini_unidades','mini_estruturas','sombra'):
            yield self.grades[nome],bytes(getattr(m,nome))
        for nome in ('regioes','tiles'):
            yield self.grades[nome],struct.pack('<65536H',*getattr(m,nome))
        for nome in ('descoberto','luz_bordas','contagem_luz'):
            yield self.grades[nome],b''.join(bytes(g) for g in getattr(m,nome))
        for j,rota in enumerate(m.rotas):
            yield self.grades['rotas']+j*512,bytes(rota)

    def carregar_caso(self,caso):
        for nome,dados in self.pristino.items():
            self.cpu.mem_write(self.blocos[nome][0],dados)
        self.carregar_navegacao(caso.mundo)
        for endereco,dados in self.patches_modelo(caso):
            self.cpu.mem_write(endereco,dados)
        self.chamadas=[]
        self.efeitos=[]
        self.celulas=[]
        self.indice_estrutura=None
        self.parada=caso.parada
        self.antes=self.estado()

    def estado_modelo(self,caso):
        """Overlay changed buffers on captured *input*; unknown native writes fail equality."""
        result={nome:bytearray(dados) for nome,dados in self.antes.items()}
        for endereco,dados in self.patches_modelo(caso):
            destinos=[nome for nome,(inicio,fim) in self.blocos.items()
                      if inicio<=endereco and endereco+len(dados)<=fim]
            if len(destinos)!=1:
                raise ValueError(f'Ambiguous/unmapped model buffer 0x{endereco:x}')
            nome=destinos[0]
            offset=endereco-self.blocos[nome][0]
            result[nome][offset:offset+len(dados)]=dados
        return {nome:bytes(dados) for nome,dados in result.items()}

    def resumo(self):
        return dict(sha256={nome:hashlib.sha256(dados).hexdigest() for nome,dados in self.estado().items()},
                    calls=[list(c) for c in self.chamadas],effects=[list(e) for e in self.efeitos])

    def executar_caso(self,caso,*,indice_predicado=0):
        self.entradas[caso.entrada]+=1
        if caso.entrada=='structures':
            # Original caller already pushed EBX then EDX. The shared tail
            # pops both before RET. Offset ESP by four so all three words
            # can be supplied through the base harness's declared stack API.
            pilha={4:struct.pack('<3I',0x5a5a5a5a,0xa5a5a5a5,RETORNO)}
        else:
            pilha=None
        registradores=dict(EAX=indice_predicado,EDX=0x5a5a5a5a,EBX=0xa5a5a5a5)
        if caso.entrada=='structures':
            registradores['ESP']=PILHA+0x8004
        regs=self.executar(ENTRADAS[caso.entrada],self.intervalos,registradores,
            pilha=pilha,limite_instrucoes=1000000)
        if regs['EIP']==RETORNO:
            self.retornos+=1
        else:
            self.dependencias+=1
        return regs
