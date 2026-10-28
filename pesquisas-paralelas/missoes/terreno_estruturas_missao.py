"""MissionPlaceTerrain structure caller, composed through explicit providers.

The original eight-scan/four-query capture was committed before this module.
Core owns placement/minimap effects and Economy owns habitation. The
Missions-owned existence query is delegated through consultas_missao.
"""
from dataclasses import dataclass
import ambiente_missoes
from colocacao_estruturas import colocar_estrutura
from minimapa_estruturas import modificar_minimapa_estrutura
from terreno_unidades import preparar_unidades_no_terreno
from consultas_missao import existe_estrutura


CHAMADAS_ESTRUTURAS={
    'existe':(0x41a735,0x46c185),
    'colocar':(0x41c4ac,0x46c190),
    'habitada':(0x41a5b8,0x46c197),
    'habitar':(0x41cc70,0x46c1a2),
    'modificar_mapa':(0x419e97,0x46c1b1),
}


class DependenciaTerrenoEstruturas(NotImplementedError):
    def __init__(self,provedor,argumentos):
        self.provedor=provedor
        self.endereco,self.chamada=CHAMADAS_ESTRUTURAS[provedor]
        self.argumentos=argumentos
        super().__init__(f'MissionPlaceTerrain needs {provedor} at 0x{self.endereco:x} '
                         f'from CALL0x{self.chamada:x}; earlier effects retained: {argumentos}')


@dataclass(frozen=True)
class ProvedoresTerrenoEstruturas:
    existe:object
    colocar:object
    habitada:object
    habitar:object
    modificar_mapa:object


@dataclass(frozen=True)
class EstruturasNoTerreno:
    colocadas:tuple
    habitadas:tuple
    retorno_original:int=0x46b6f7


@dataclass(frozen=True)
class TerrenoMissaoPreparado:
    unidades:object
    estruturas:EstruturasNoTerreno
    retorno_original:int=0x46b6f7


def provedores_terreno_estruturas_core(mundo,*,habitacao=None,mascara_tipo20=None):
    """Bind actual committed lower providers to one explicit shared world.

    Existence delegates the single Missions-owned exact query. A missing
    habitation object raises only when its query is reached, after the
    completed placement; it is not replaced with a successful default.
    """
    if habitacao is not None:
        economia=getattr(habitacao,'construcoes',None)
        producao=getattr(habitacao,'producao',None)
        recrutamento=getattr(producao,'recrutamento',None)
        if (getattr(economia,'estruturas',None) is not mundo.estruturas or
                getattr(recrutamento,'unidades',None) is not mundo.unidades):
            raise ValueError('Habitation and Core must share the identical unit/structure pools')
    habitada=getattr(habitacao,'estrutura_habitada',None)
    habitar=getattr(habitacao,'tornar_habitavel',None)
    return ProvedoresTerrenoEstruturas(
        lambda indice:existe_estrutura(mundo.estruturas,indice),
        lambda indice:colocar_estrutura(mundo,indice,mascara_tipo20),
        habitada,(lambda indice:habitar(mundo,indice)) if callable(habitar) else None,
        lambda indice,modo:modificar_minimapa_estrutura(mundo,indice,modo))


def preparar_estruturas_no_terreno(provedores):
    """0x46c16d..shared RET46b6f7: live ascending scan of1000 slots.

    Query lowAL existence; place; query lowAL habitation; conditionally make
    habitable; modify the minimap with1 for every existing structure. Later
    queries see live effects. Exceptions preserve prior effects; replay from
    entry is not a continuation and can repeat discovery/light counts.
    """
    if not isinstance(provedores,ProvedoresTerrenoEstruturas):
        raise ValueError('Expected explicit structure terrain providers')
    def chamar(nome,*argumentos):
        provedor=getattr(provedores,nome)
        if not callable(provedor):
            raise DependenciaTerrenoEstruturas(nome,argumentos)
        return provedor(*argumentos)
    colocadas=[]
    habitadas=[]
    for indice in range(1000):
        if not (chamar('existe',indice)&255):
            continue
        chamar('colocar',indice)
        colocadas.append(indice)
        if chamar('habitada',indice)&255:
            chamar('habitar',indice)
            habitadas.append(indice)
        chamar('modificar_mapa',indice,1)
    return EstruturasNoTerreno(tuple(colocadas),tuple(habitadas))


def preparar_terreno_missao(provedores_unidades,provedores_estruturas):
    """Whole MissionPlaceTerrain caller only; explicit inherited world readiness required."""
    unidades=preparar_unidades_no_terreno(provedores_unidades)
    estruturas=preparar_estruturas_no_terreno(provedores_estruturas)
    return TerrenoMissaoPreparado(unidades,estruturas)
