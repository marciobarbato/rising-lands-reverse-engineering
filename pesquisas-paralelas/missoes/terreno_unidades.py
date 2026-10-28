"""MissionPlaceTerrain unit scan/capacity prefix through exact core providers."""
from dataclasses import dataclass
import ambiente_missoes
from consultas_unidades import existe_unidade,visibilidade_unidade
from colocacao_missao import colocar_unidade_missao
from capacidades_unidades import atualizar_capacidades_unidades
from bonus_unidades import capacidade_tipo


class DependenciaTerrenoUnidades(NotImplementedError):
    def __init__(self,endereco,argumentos):
        self.endereco,self.argumentos=endereco,argumentos
        super().__init__(f'Unit initialization dependency at 0x{endereco:08x}: {argumentos}')


@dataclass(frozen=True)
class ProvedoresTerrenoUnidades:
    existe:object
    visibilidade:object
    colocar:object
    capacidades:object


@dataclass(frozen=True)
class UnidadesNoTerreno:
    colocadas:tuple
    endereco_dependencia:int=0x46c16d


def provedores_terreno_core(mundo,*,bonus_unidades=None):
    """Bind actual committed providers to one explicit inherited world.

    Bonus state is never defaulted. Missing bonus raises at its first actual
    selector1 query after prior insertion effects; if no query is reached,
    no table is manufactured. Every callback keeps live buffer identities.
    """
    def modifier(owner,kind,selector):
        query=getattr(bonus_unidades,'consultar',None)
        if not callable(query):
            raise DependenciaTerrenoUnidades(0x428cc0,(owner,kind,selector))
        return query(owner,kind,selector)
    return ProvedoresTerrenoUnidades(
        lambda index:existe_unidade(mundo,index),
        lambda index:visibilidade_unidade(mundo,index),
        lambda index:colocar_unidade_missao(mundo,index),
        lambda owner:atualizar_capacidades_unidades(mundo,owner,
                        capacidade_tipo=capacidade_tipo,modificador=modifier))


def preparar_unidades_no_terreno(provedores):
    """0x46c122..0x46c16d: live ascending scan, then four capacity calls.

    Required callbacks are explicit; no missing effect is a successful no-op.
    Query results consume lowAL. Exceptions preserve all earlier callback
    effects; entry replay is not continuation and can repeat vision counts.
    Structure placement and later mission execution are not entered here.
    """
    if not isinstance(provedores,ProvedoresTerrenoUnidades):
        raise ValueError('Expected explicit unit initialization providers')
    def call(provider,address,value):
        if not callable(provider):
            raise DependenciaTerrenoUnidades(address,(value,))
        return provider(value)
    placed=[]
    for index in range(800):
        if not (call(provedores.existe,0x441fff,index)&255):
            continue
        if not (call(provedores.visibilidade,0x4465bf,index)&255):
            continue
        call(provedores.colocar,0x456fa6,index)
        placed.append(index)
    for owner in range(4):
        call(provedores.capacidades,0x4475ef,owner)
    return UnidadesNoTerreno(tuple(placed))
