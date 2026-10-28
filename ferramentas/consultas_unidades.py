"""Literal existence and raw in-world flag queries from original unit records."""


def _base(mundo,indice):
    indice &= 65535
    if not isinstance(mundo.unidades,bytearray) or len(mundo.unidades) != 220800 or indice >= 800:
        raise ValueError('Unit query requires a live 800-record pool and index 0..799')
    return indice*276


def existe_unidade(mundo,indice):
    """0x441fff, complete EAX boolean; state4 exists, no other guard."""
    return mundo.unidades[_base(mundo,indice)+2] != 0


def visibilidade_unidade(mundo,indice):
    """0x4465bf consumed AL only: raw +72, independent of terrain discovery."""
    return mundo.unidades[_base(mundo,indice)+0x72]


def tipo_unidade(mundo, indice):
    """EnginGetType 0x442025: consumed AL is raw +1, with no activity/type guard."""
    return mundo.unidades[_base(mundo, indice)+1]


def tipo_unidade_monstro(tipo):
    """TypeEnginEstMonstre 0x4422dd, AL input/result, shared true tail 0x4422da."""
    return 20 <= (tipo & 255) <= 24
