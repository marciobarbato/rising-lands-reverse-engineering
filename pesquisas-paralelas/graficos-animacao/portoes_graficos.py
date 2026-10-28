"""Pure indexed HERSE facade, bounded before AffBatiments' shared tail.

Consumes prepared runtime fields; never advances the physical gate counter.
"""
from graficos import localizar, compor_indices


def _integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'{name} must be an integer in {low}..{high}')


def _i16(value):
    return (value + 32768) % 65536 - 32768


def consultar_portao(*, contador_u8, orientacao_u16, valor_0a_u16,
                     jogador, camera, modo_u8, visibilidade_u8, descoberta_u8,
                     x, y, janela_celulas):
    """Plan for object 253 referring to a prepared type-12 runtime record.

    x/y are signed 16-bit projected cell origins. janela_celulas is the u16
    width/height pair at 0x508724, restricted to 1..1024 cells per dimension.
    valor_0a_u16 is the raw +0x0a word, without an economic interpretation.
    visibilidade_u8 is this record's +0x110+camera byte; descoberta_u8 is the
    separate per-camera map byte. The caller resolves the occupancy label.
    """
    for value, high, name in ((contador_u8,255,'contador_u8'),
            (orientacao_u16,65535,'orientacao_u16'),
            (valor_0a_u16,65535,'valor_0a_u16'), (jogador,4,'jogador'),
            (camera,3,'camera'), (modo_u8,255,'modo_u8'),
            (visibilidade_u8,255,'visibilidade_u8'),
            (descoberta_u8,255,'descoberta_u8')):
        _integer(value,0,high,name)
    _integer(x,-32768,32767,'x'); _integer(y,-32768,32767,'y')
    if len(janela_celulas) != 2:
        raise ValueError('janela_celulas must contain width and height')
    for value in janela_celulas:
        _integer(value,1,1024,'window cells')
    if contador_u8 > 31:
        raise NotImplementedError('Only counter 0..31 belongs to the verified gate strips')
    plano = dict(tipo=12, chave_ini='HERSE', contador_u8=contador_u8,
        orientacao_u16=orientacao_u16, estado_u16=None, recorte=None, camadas=[],
        evidencia='AffBatiments 0x407dd3..0x4080e8 -> 0x408418..0x408422')
    # Owner/mode rejection precedes the map discovery query in the original.
    if modo_u8 != 3 and jogador != camera and visibilidade_u8 == 0:
        plano['motivo'] = 'hidden_record'
        return plano
    if descoberta_u8 & 16:
        plano['motivo'] = 'undiscovered_cell'
        return plano
    # BatimentGetEtat returns 200 * raw / the original type parameter (70).
    # AffBatiments consumes its low word; IDIV truncates toward zero.
    estado = (valor_0a_u16 * 200 // 70) & 65535
    delta = (100 - estado) * 32
    shift = (abs(delta) // 100) * (-1 if delta < 0 else 1)
    top = max(0, _i16(y + shift))
    recorte = [max(0,x), top, janela_celulas[0]*32-1, janela_celulas[1]*32-1]
    vertical = orientacao_u16 != 0
    camada = dict(**localizar((7608 if vertical else 7576) + contador_u8),
        x=_i16(x+5) if vertical else x,
        y=_i16(y+4) if vertical else y, operacao='copiar', ordem=0)
    plano.update(estado_u16=estado,recorte=recorte,camadas=[camada],motivo='draw')
    return plano


def compor_portao(catalogo, destino, largura, altura, plano):
    """Copy opaque indices under the original temporary clip; pure buffer API.

    The caller supplies an already rendered background matching the window.
    Incoming clip is deliberately replaced by the original facade branch.
    No player recoloring, shadow table, callback, or world mutation occurs.
    """
    if len(destino) != largura*altura or largura <= 0 or altura <= 0:
        raise ValueError('Invalid indexed surface')
    saida = bytes(destino)
    for camada in plano['camadas']:
        if plano['recorte'][2:] != [largura-1,altura-1]:
            raise ValueError('Surface dimensions must match the planned window')
        saida = compor_indices(saida,largura,altura,catalogo.quadro(camada['id_motor']),
            camada['x'],camada['y'],plano['recorte'])
    return saida
