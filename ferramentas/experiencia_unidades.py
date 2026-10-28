"""Original EnginSetNewExperience and per-owner experience queue consumption."""
from dataclasses import dataclass
import struct

TIPOS_F7 = frozenset((0, 1, 2, 3, 8, 11, 12, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25))


class DependenciaExperienciaUnidade(NotImplementedError):
    def __init__(self, unidade, nivel, endereco):
        self.unidade, self.nivel, self.endereco = unidade, nivel, endereco
        super().__init__(f'Loaded unit fatigue characteristic required at 0x{endereco:x}; '
                         'prior live stores retained')


def _registro(mundo, indice):
    indice &= 65535
    if (not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800
            or indice >= 800):
        raise ValueError('Experience requires a writable 800-record pool and unit 0..799')
    return indice * 276


def aplicar_nova_experiencia(mundo, indice, nivel, tipos_unidades=None):
    """0x44f9e0 local effects; does not change AF or physical world state."""
    p = _registro(mundo, indice)
    nivel &= 255
    if nivel == 2:
        mundo.unidades[p+0xf6] = 1
    elif nivel == 3:
        mundo.unidades[p+0xf5] = 1
    elif nivel in (1, 4):
        tipo = mundo.unidades[p+1]
        classe_f7 = tipo in TIPOS_F7
        if nivel == 1 and classe_f7:
            mundo.unidades[p+0xf7] = 1
            return
        endereco = 0x44fafa if nivel == 4 and not classe_f7 else 0x44fa71
        if tipos_unidades is None:
            raise DependenciaExperienciaUnidade(indice & 65535, nivel, endereco)
        if (not isinstance(tipos_unidades, (bytes, bytearray)) or len(tipos_unidades) != 1300
                or tipo >= 26):
            raise ValueError('Experience table read requires 1300 bytes and live type 0..25')
        palavra = struct.unpack_from('<H', tipos_unidades, tipo*50+0x2e)[0]
        multiplicador = 2 if nivel == 4 and not classe_f7 else 1
        mundo.unidades[p+0xf8] = (palavra*multiplicador // 100) & 255


def consumir_experiencia_unidade(mundo, indice, tipos_unidades=None):
    """0x44fe42: match first pair, write AF/apply effects, then shift queue.

    The raw 40-byte table supports owners 0..3. Missing table data at the
    nested read retains AF and leaves all queue bytes intact.
    """
    p = _registro(mundo, indice)
    fila = mundo.experiencias_unidades
    dono = mundo.unidades[p]
    if not isinstance(fila, bytearray) or len(fila) != 40 or dono >= 4:
        raise ValueError('Experience queue requires 40 writable bytes and owner 0..3')
    base = dono*10
    experiencia = fila[base+1]
    if experiencia == 0 or fila[base] != mundo.unidades[p+1]:
        return
    mundo.unidades[p+0xaf] = experiencia
    aplicar_nova_experiencia(mundo, indice, experiencia >> 5, tipos_unidades)
    for i in range(4):
        fila[base+i*2+1] = fila[base+i*2+3]
        fila[base+i*2] = fila[base+i*2+2]
    fila[base+9] = 0
    fila[base+8] = 255


@dataclass(frozen=True)
class ExperienciaSaidaTropa:
    indice: int
    unidade: int
    celula: int
    tipo_unidade: int
    endereco_dependencia: int = 0x420f8a


def retomar_experiencia_saida(mundo, pedido, tipos_unidades=None):
    """One-shot continuation from recovery through 0x420f81..0x420f8a."""
    if pedido.endereco_dependencia != 0x420f81:
        raise ValueError('Expected recovery handoff at 0x420f81')
    indice, unidade, celula = pedido.indice & 65535, pedido.unidade & 65535, pedido.celula & 65535
    consumir_experiencia_unidade(mundo, unidade, tipos_unidades)
    return ExperienciaSaidaTropa(indice, unidade, celula, mundo.unidades[unidade*276+1])
