"""Read-only owner proximity for the damage caller's fixed radius-10 query."""
from dataclasses import dataclass
import struct


def proximidade_dono_ataque(unidades, grade, dono, celula):
    """ChercheTypeEnginProximite 0x4500e4, only the caller's radius 10.

    Grid is 65,536 little-endian u16 words. Only words whose high two bits
    equal 01 encode a unit; low three bits are ignored. Owner is compared
    before squared distance, with no unit type/activity/alliance test.
    The original's desired-type EAX argument is not used in this body.
    """
    if len(unidades) != 800 or any(len(u) != 276 for u in unidades):
        raise ValueError('Expected 800 readable 276-byte unit records')
    if len(grade) != 131072:
        raise ValueError('Expected a loaded 65536-word little-endian grid')
    dono, celula = dono & 255, celula & 65535
    cx, cy = celula & 255, celula >> 8
    for y in range(max(0, cy - 10), min(256, cy + 11)):
        for x in range(max(0, cx - 10), min(256, cx + 11)):
            value = struct.unpack_from('<H', grade, (x + y * 256) * 2)[0]
            if value & 0xc000 != 0x4000:
                continue
            index = (value & 0x3ff8) >> 3
            if index >= 800:
                raise ValueError('Grid unit ID is outside the modeled 800-record allocation')
            if unidades[index][0] != dono:
                continue
            if (x - cx) ** 2 + (y - cy) ** 2 <= 100:
                return 1
    return 0


@dataclass
class ConsultaProximidadeAtaque:
    unidades: object
    grade: object
    outras: object = None

    def __call__(self, nome, args):
        if nome == 'ChercheTypeEnginProximite':
            tipo, dono, celula, raio = args
            if (tipo & 255) != 2 or (raio & 0xffffffff) != 10:
                raise NotImplementedError('Only the damage caller query (2, owner, cell, 10) is supported')
            return proximidade_dono_ataque(self.unidades, self.grade, dono, celula)
        if self.outras is None:
            raise NotImplementedError('External damage query required: ' + nome)
        return self.outras(nome, args)
