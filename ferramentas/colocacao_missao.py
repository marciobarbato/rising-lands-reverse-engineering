"""Original physical PlaceEngin; mission scanning/loading remains external."""
from insercao_unidades import DependenciaInsercaoUnidade,_preparar_insercao,_aplicar_insercao


class DependenciaColocacaoMissao(DependenciaInsercaoUnidade):
    def __init__(self,unidade):
        super().__init__(unidade,0x457019)


def colocar_unidade_missao(mundo,indice):
    """0x456fa6: insert current cell, enable, discover/light/minimap only."""
    indice,celula,_=_preparar_insercao(mundo,indice)
    _aplicar_insercao(mundo,indice,celula,DependenciaColocacaoMissao)
