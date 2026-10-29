"""Normal body of unit types 1 (``GARDIEN DU FEU``) and 8 (``VOLEUR``), pure Python.

Original path, all inside the intact ``RISING.EXE`` (SHA-256 6c556520...43fb):

* ``AffEngin 0x41591F`` routes states 2 and 7 to ``AffDeplaceEngin 0x412390``.
* The prefix adds the signed-i8 shifts ``+0x86/+0x87`` to x/y and reads the anchor through
  ``AffCorpsEnginDecalage 0x410FCC`` (table ``0x410F64``: slot 1 -> ``0x411001`` = (23, 9); slot 8 -> ``0x410FDD`` = (32, 30)).
  With ``+0x99 = 0`` no random oscillation is drawn; with ``+0xBD = 0`` no selection marker.
* Body jump table ``0x412328``: slot 1 -> ``0x412D4C``, slot 8 -> ``0x412962``.  Each branch issues
  ``PasteOmbreCmp(10784)`` at ``(x+2, y+26)``, then joins ``0x412CB8`` with
  ``id = base + (floor((direction+1)/2) - 1) * count + phase`` (count u8 ``+0xA5``, phase u8 ``+0xA4``;
  base 0x8F2 = 2290 for type 1, 0x992 = 2450 for type 8) and calls ``AffCorpsEngin 0x411147``.
* ``AffCorpsEngin`` for owner 0 with effects byte ``+0xDC = 0`` (mirror/terror/armour bits clear) issues one
  ``PasteBobCmp`` at ``(x - anchor_x, y - anchor_y)``; its type tests (4, 12, 15) do not match types 1/8.
* The common tail ``0x412A53`` then goes to ``0x413568`` (tired icon, composed by ``quadro_jogo``) when no selection
  overlay is due.

Domain = what the native capture ``evidencias/captura-corpos-tipos1-8-m22-v2.json`` covers: owner 0 under camera 0,
states 2/7, the type's initialized count (8 for type 1, 10 for type 8), direction 1..16, phase below the count,
``+0x99 = +0xBA = +0xBD = +0xDC = 0``, not the selected unit, selection mode 0.  Anything else raises
``NotImplementedError`` (the frame turns it into the named stop ``0x41591F``); nothing is defaulted.
"""
import struct
from graficos import localizar, compor_indices
from composicao import compor_sombra

SOMBRA_ID = 10784   # 0x2A20, PasteOmbreCmp at (x+2, y+26)
CORPOS = {
    1: dict(chave_ini='GARDIEN DU FEU', base=0x8f2, ancora=(23, 9), contagem=8, ramo=0x412d4c, ancora_ramo=0x411001),
    8: dict(chave_ini='VOLEUR', base=0x992, ancora=(32, 30), contagem=10, ramo=0x412962, ancora_ramo=0x410fdd),
}
ESTADOS = (2, 7)


def _inteiro(v, nome, minimo, maximo):
    if type(v) is not int or not minimo <= v <= maximo:
        raise ValueError(f'{nome} must be an integer in {minimo}..{maximo}')
    return v


def consultar_corpo_tipos1_8(registro276, *, x, y, indice_u16, camera_u8, indice_selecionado_u16, modo_selecao_u8, sobreposicoes_compostas=False):
    """Ordered body layers. ``sobreposicoes_compostas=True`` delegates overlay validation/drawing to the 1.5 frame.

    The standalone default retains the 1.3 strict domain; the body arithmetic and pixels are unchanged.
    """
    if not isinstance(registro276, (bytes, bytearray)) or len(registro276) != 276:
        raise ValueError('registro276 must be 276 bytes')
    _inteiro(x, 'x', -32768, 32767); _inteiro(y, 'y', -32768, 32767)
    _inteiro(indice_u16, 'indice_u16', 0, 799); _inteiro(camera_u8, 'camera_u8', 0, 255)
    _inteiro(indice_selecionado_u16, 'indice_selecionado_u16', 0, 65535); _inteiro(modo_selecao_u8, 'modo_selecao_u8', 0, 255)
    r = bytes(registro276)
    dono, tipo, estado = r[0], r[1], r[2]
    if tipo not in CORPOS: raise NotImplementedError(f'type {tipo} is not a type-1/type-8 body')
    t = CORPOS[tipo]
    falhas = []
    if dono != 0 or camera_u8 != 0: falhas.append(f'owner {dono} / camera {camera_u8} (captured: owner 0 under camera 0)')
    if estado not in ESTADOS: falhas.append(f'state {estado} (captured: 2, 7)')
    if not sobreposicoes_compostas and (r[0xba] or r[0xbd] or indice_selecionado_u16 == indice_u16 or modo_selecao_u8):
        falhas.append('selection/experience overlay (+0xBA, +0xBD, selected unit or selection mode)')
    if r[0x99]: falhas.append('oscillation +0x99 (random displacement, RNG cursor)')
    if r[0xdc]: falhas.append('effects byte +0xDC (mirror/terror/armour)')
    direcao, fase, contagem = r[0x91], r[0xa4], r[0xa5]
    if contagem != t['contagem']: falhas.append(f'count +0xA5 = {contagem} (captured: {t["contagem"]})')
    if not 1 <= direcao <= 16: falhas.append(f'direction {direcao} (captured: 1..16)')
    if fase >= contagem: falhas.append(f'phase {fase} not below count {contagem}')
    if falhas: raise NotImplementedError('outside the captured type-1/8 body domain: '+'; '.join(falhas))
    dx, dy = struct.unpack_from('<bb', r, 0x86)
    i16 = lambda v: ((v + 0x8000) & 0xffff) - 0x8000
    id_corpo = (t['base'] + ((direcao+1)//2 - 1)*contagem + fase) & 0xffff
    ax, ay = t['ancora']
    sombra = dict(**localizar(SOMBRA_ID), x=i16(x+dx+2), y=i16(y+dy+26), operacao='remapear_destino')
    corpo = dict(**localizar(id_corpo), x=i16(x+dx-ax), y=i16(y+dy-ay), operacao='copiar_opacos')
    return dict(tipo=tipo, estado_u8=estado, ramo=hex(t['ramo']), deslocamento=(dx, dy), camadas=[sombra, corpo])


def compor_corpo_tipos1_8(catalogo, destino, largura, altura, registro276, *, x, y, indice_u16, camera_u8,
                          indice_selecionado_u16, modo_selecao_u8, tabela_sombra, recorte=None, sobreposicoes_compostas=False):
    """(new indexed bytes, plan): shadow remap under the 10784 mask, then the opaque body copy."""
    if len(destino) != largura*altura: raise ValueError('Surface size does not match its dimensions')
    if len(tabela_sombra) != 256: raise ValueError('tabela_sombra must be 256 bytes')
    plano = consultar_corpo_tipos1_8(registro276, x=x, y=y, indice_u16=indice_u16, camera_u8=camera_u8,
                                     indice_selecionado_u16=indice_selecionado_u16, modo_selecao_u8=modo_selecao_u8,
                                     sobreposicoes_compostas=sobreposicoes_compostas)
    sombra, corpo = plano['camadas']
    saida = compor_sombra(bytes(destino), largura, altura, catalogo.quadro(SOMBRA_ID), sombra['x'], sombra['y'], bytes(tabela_sombra), recorte)
    saida = compor_indices(saida, largura, altura, catalogo.quadro(corpo['id_motor']), corpo['x'], corpo['y'], recorte)
    return saida, plano
