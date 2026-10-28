"""Declared Stage 11 inputs; no structure-traversal translation is called here."""
from dataclasses import dataclass
import struct
import ambiente_missoes
from integracao.providers import load_economy_resources

# Bind the committed economic namespace before importing its fixture builders.
load_economy_resources()
from casos_habitaveis import caso_monde01,caso_sintetico
from navegacao_unidades import MundoNavegacao
from entradas import tipos_originais


class MundoRastreadoEstruturasMissao(MundoNavegacao):
    """Trace delegations only; every physical effect remains in Core."""
    def __init__(self,*args):
        self.efeitos=[]
        super().__init__(*args)

    def ocupar(self,indice,celula,inserir):
        self.efeitos.append(('collision' if inserir else 'remove',indice,celula))
        return super().ocupar(indice,celula,inserir)

    def descobrir_area(self,celula,raio,dono):
        self.efeitos.append(('discovery',celula,raio,dono))
        return super().descobrir_area(celula,raio,dono)

    def iluminar_area(self,celula,raio,dono):
        self.efeitos.append(('light',celula,raio,dono))
        return super().iluminar_area(celula,raio,dono)

    def minimapa(self,dono,celula,modo):
        self.efeitos.append(('minimap',dono,celula,modo))
        return super().minimapa(dono,celula,modo)


@dataclass
class CasoTerrenoEstruturasMissao:
    nome:str
    economico:object
    tipos:bytes
    regras_runtime:bytearray  # 0x4dfb9c: four mask bytes then the live 1872-byte bonus view
    entrada:str='structures'
    parada:object=None       # (original CALL site, current structure index)

    @property
    def mundo(self):
        return self.economico.mundo

    @property
    def bonus(self):
        return memoryview(self.regras_runtime)[4:]

    @property
    def mascara_tipo20(self):
        return memoryview(self.regras_runtime)[:20]


def preparar_terreno_estruturas_missao(nome,*,tipo=2,dono=0,indice=7,estado=5,
                                     habitantes=True,entrada='structures',parada=None,
                                     padrao='zero'):
    """Actual MONDE01 records or one declared synthetic structure.

    Prior integrated loaders may prepare the input records. Physical region,
    color, vision, selection, Bag and rule state is explicitly synthetic.
    No current-stage engine traversal is executed while making these inputs.
    """
    if nome.startswith('MONDE01') or nome=='missing_map':
        economia=caso_monde01(nome,padrao=padrao,classe=MundoRastreadoEstruturasMissao)
    else:
        economia=caso_sintetico(nome,tipo,dono,0x4040,indice=indice,
            unidades=(20,) if habitantes else (),tipos_unidades=(9,) if habitantes else (),
            padrao=padrao,armazens=(2,100),classe=MundoRastreadoEstruturasMissao)
        economia.mundo.estruturas[indice*276+5]=estado
    m=economia.mundo
    # Declared inherited patterns, not a claim that TerrainReset was executed.
    for grupo,valor in ((m.descoberto,31),(m.luz_bordas,31),(m.contagem_luz,0)):
        for grade in grupo:
            grade[:]=bytes([valor])*65536
    m.mini_final[:]=b'\x02'*65536
    m.mini_unidades[:]=bytes(65536)
    m.mini_estruturas[:]=bytes(65536)
    m.selecoes_unidades[:]=bytes((i*23+0x53)&255 for i in range(2048))
    for jogador,bag in enumerate(m.bolsas_tipos_unidades):
        bag[:]=bytes([(0x61+jogador)&255])*2704
    m.efeitos=[]
    return CasoTerrenoEstruturasMissao(nome,economia,tipos_originais(),
                                     bytearray(b'\x01'*4+b'\x31'*1872),entrada,parada)


def casos_captura_terreno_estruturas():
    """Eight bounded original-only cases, to execute only under a heavy grant."""
    yield preparar_terreno_estruturas_missao('MONDE01_structure_tail')
    yield preparar_terreno_estruturas_missao('MONDE01_joined',entrada='joined',padrao='um')
    yield preparar_terreno_estruturas_missao('empty_pool',estado=0,habitantes=False)
    yield preparar_terreno_estruturas_missao('edge_uninhabited',tipo=1,dono=3,indice=999,
                                          estado=255,habitantes=False)
    yield preparar_terreno_estruturas_missao('state1_inhabited',tipo=21,indice=0,estado=1)
    esparso=preparar_terreno_estruturas_missao('sparse_slots',indice=0)
    record=bytearray(esparso.mundo.estruturas[:276])
    struct.pack_into('<H',record,2,0x8080)
    record[4],record[5],record[8]=3,255,17
    struct.pack_into('<H',record,0x0c,0)
    esparso.mundo.estruturas[999*276:1000*276]=record
    yield esparso
    yield preparar_terreno_estruturas_missao('missing_map',parada=(0x46c1b1,0))
    yield preparar_terreno_estruturas_missao('owner4_discovery',tipo=4,dono=4,
                                          parada=(0x41cdb9,7))
