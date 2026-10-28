"""Gate facade plus the verified type-12 shared-tail observable effects."""
from portoes_graficos import consultar_portao, compor_portao


def consultar_portao_completo(*, terreno_u16, recorte_entrada, **campos):
    """Return a gate plan and the clip after the actual AffBatiments return.

    A prepared type-12/object-253 record remains required. Terrain 0x356 is
    excluded: it invokes a whole-pool workshop lookup with external records.
    Selection/hover and habitation do not change pixels for this type; the
    original helpers themselves reject type 12 before drawing their overlays.
    """
    if type(terreno_u16) is not int or not 0 <= terreno_u16 <= 65535:
        raise ValueError('terreno_u16 must be an integer in 0..65535')
    if len(recorte_entrada)!=4 or any(type(v) is not int or not 0<=v<=65535 for v in recorte_entrada):
        raise ValueError('recorte_entrada must contain four u16 values, left/top/right/bottom')
    if terreno_u16==0x356:
        raise NotImplementedError('Workshop-trigger terrain requires the external structure-pool lookup')
    plan=consultar_portao(**campos)
    plan.update(terreno_u16=terreno_u16,recorte_entrada=list(recorte_entrada),
        recorte_saida=list(recorte_entrada),
        cauda='type12_no_additional_pixels',
        evidencia_cauda='AffBatiments 0x40f342..0x40f49c through RET')
    return plan


def compor_portao_completo(catalogo,destino,largura,altura,plano):
    """Return (new indexed bytes, restored inclusive clip); no global state."""
    return (compor_portao(catalogo,destino,largura,altura,plano),
        tuple(plano['recorte_saida']))
