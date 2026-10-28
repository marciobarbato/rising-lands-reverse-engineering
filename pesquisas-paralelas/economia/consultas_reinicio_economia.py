"""Small economy-owned leaves required by the real IaReset callback path.

Use explicit live buffers. No constructor, copying, defaults or cached value.
Missions owns BatimentExiste; combat's existing GetPlayer bridge is reused.
"""


def _vista(memoria, tamanho, nome, *, escrita=False):
    try:
        view = memoryview(memoria)
    except TypeError as erro:
        raise ValueError(f'{nome} requires an explicit byte buffer') from erro
    if (view.ndim != 1 or not view.c_contiguous or view.itemsize != 1
            or view.format not in ('B', 'b') or len(view) != tamanho):
        raise ValueError(f'{nome} requires exactly {tamanho} contiguous B/b bytes')
    if escrita and view.readonly:
        raise ValueError(f'{nome} requires writable inherited research memory')
    return view.cast('B') if view.format == 'b' else view


def _jogador(jogador):
    jogador &= 255
    if jogador >= 4:
        raise ValueError('Research player must be 0..3 after AL truncation')
    return jogador


def nivel_pesquisa(pesquisa, jogador, ramo):
    """RechercheGetNiveau4717c2: AL player, DX branch; unsigned byte in AX.

    Protected scope: four players and branches0..3 used by IaReset. The
    original has no index guard. Read the live64-byte range5080f4..508134;
    this is not a word field or a spell availability flag. No store occurs.
    """
    jogador, ramo = _jogador(jogador), ramo & 65535
    if ramo >= 4:
        raise ValueError('IaReset research branch must be 0..3 after DX truncation')
    return _vista(pesquisa, 64, 'RechercheGetNiveau')[jogador*16+ramo]


def definir_ramo_pesquisa(pesquisa, jogador, ramo):
    """RechercheSetBranche470b37: one DL byte at5080f8+16*AL; no other effect.

    Player protected0..3; all256 DL values are retained. Guards precede
    stores. Return None: IaReset ignores native EAX (which becomes AL*16).
    The actual mapped allocation observes the single write immediately.
    """
    jogador = _jogador(jogador)
    view = _vista(pesquisa, 64, 'RechercheSetBranche', escrita=True)
    view[jogador*16+4] = ramo & 255


def tipo_estrutura(estruturas, indice):
    """BatimentGetType41a4f4: raw byte+8 from the live276000-byte flat pool.

    AX truncates u16; protect0..999. Do not test state/owner or normalize
    unknown type bytes. This models consumed AL, not address-derived upper
    native EAX bits. No store or copied structure record is created.
    """
    view = _vista(estruturas, 276000, 'BatimentGetType')
    indice &= 65535
    if indice >= 1000:
        raise ValueError('Structure index must be 0..999 after AX truncation')
    return view[indice*276+8]
