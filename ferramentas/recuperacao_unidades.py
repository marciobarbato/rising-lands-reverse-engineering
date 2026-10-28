"""Live original EnginAddVie/EnginResetFatigue and production continuation."""
from dataclasses import dataclass
import struct

from unidades import curar_com_limite


def _registro(mundo, indice):
    indice &= 65535
    if (not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800
            or indice >= 800):
        raise ValueError('Recovery requires a writable 800-record pool and unit 0..799')
    return indice * 276


def adicionar_vida_unidade(mundo, indice, acrescimo, tipos_unidades):
    """Complete 0x457122; return AL clamp flag, preserving u16 overflow.

    Supported preloaded type table is bytes/bytearray of length 1300 and the
    live type is 0..25. Protected invalid inputs fail before any store. The
    helper has no activity/owner guard and changes only u16 life +0x9a.
    """
    p = _registro(mundo, indice)
    if (not isinstance(tipos_unidades, (bytes, bytearray)) or len(tipos_unidades) != 1300
            or mundo.unidades[p+1] >= 26):
        raise ValueError('Healing requires 1300 preloaded type bytes and live type 0..25')
    vida = struct.unpack_from('<H', mundo.unidades, p+0x9a)[0]
    # Reuse the established arithmetic twice to retain the original sum store
    # before the live type/maximum read, without duplicating the wrapping rule.
    soma, _ = curar_com_limite(vida, acrescimo, 65535)
    struct.pack_into('<H', mundo.unidades, p+0x9a, soma)
    tipo = mundo.unidades[p+1]
    maximo = struct.unpack_from('<H', tipos_unidades, tipo*50+8)[0]
    nova, excedeu = curar_com_limite(soma, 0, maximo)
    if excedeu:
        struct.pack_into('<H', mundo.unidades, p+0x9a, nova)
    return excedeu


def resetar_fadiga_unidade(mundo, indice):
    """Complete 0x4530fd: clear +0x74, then copy u16 +0x76 to +0x04."""
    p = _registro(mundo, indice)
    struct.pack_into('<H', mundo.unidades, p+0x74, 0)
    valor = struct.unpack_from('<H', mundo.unidades, p+0x76)[0]
    struct.pack_into('<H', mundo.unidades, p+4, valor)


@dataclass(frozen=True)
class RecuperacaoSaidaTropa:
    indice: int
    unidade: int
    celula: int
    tipo_unidade: int
    endereco_dependencia: int = 0x420f81


def retomar_recuperacao_saida(mundo, pedido, tipos_unidades):
    """Resume conversion's 0x420f6e stop through healing/fatigue only.

    Uses literal increment 1000 and current live type; returns before experience
    at 0x420f81. One-shot handoff: replay would apply the addition again.
    """
    if pedido.endereco_dependencia != 0x420f6e:
        raise ValueError('Expected conversion handoff before healing at 0x420f6e')
    # Validate/normalize metadata before either live effect.
    indice, unidade, celula = pedido.indice & 65535, pedido.unidade & 65535, pedido.celula & 65535
    adicionar_vida_unidade(mundo, unidade, 1000, tipos_unidades)
    resetar_fadiga_unidade(mundo, unidade)
    return RecuperacaoSaidaTropa(indice, unidade, celula, mundo.unidades[unidade*276+1])
