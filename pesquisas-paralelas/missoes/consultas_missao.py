"""Read-only Missions queries over explicit live original-width buffers."""


def _vista_consulta(memoria,tamanho,nome):
    try:
        view=memoryview(memoria)
    except TypeError as error:
        raise ValueError(f'{nome} requires an explicit byte buffer') from error
    if (view.ndim!=1 or not view.c_contiguous or view.format not in ('B','b')
            or view.itemsize!=1 or len(view)!=tamanho):
        raise ValueError(f'{nome} requires exactly{tamanho} contiguous B/b bytes')
    return view.cast('B') if view.format=='b' else view


def numero_missao(missao_u8):
    """MissionGetNum0x46c11a: semantic AX result, from exactly byte0x496fe4.

    The intact body clears AH, reads AL and retains highEAX16. This API
    returns AX0..255, not the caller's unrelated upper register bits. The
    one-byte view is read at each call; no copy, cache, neighbor or default.
    Read-only byte views are valid because the original performs no store.
    """
    return _vista_consulta(missao_u8,1,'MissionGetNum')[0]


def existe_estrutura(estruturas,indice):
    """BatimentExiste0x41a735: AX index, AL1 iff the actual state byte+5 !=0.

    Read the caller's live276000-byte pool, including states1/4/5/255.
    Protect index0..999 after the original low16 truncation. No generic
    alive predicate, compact index, copied pool or constructor default.
    """
    view=_vista_consulta(estruturas,276000,'BatimentExiste')
    indice &= 65535
    if indice>=1000:
        raise ValueError('BatimentExiste protected index is0..999 after low16')
    return int(view[indice*276+5]!=0)
