"""Read-only original building lookup from the loaded impact region grid."""
from dataclasses import dataclass
import struct


def encontrar_estrutura_impacto(grade, celula):
    """ChercheIndiceBatiment 0x41b54a: cell AX, full EAX ID or 0xffff.

    Bit 15 declares a structure. Bits 5..14 encode its ID; the low five bits
    are ignored. This query never validates the structure record allocation,
    so IDs 1000..1023 are returned too. It does not build or mutate the grid.
    """
    if len(grade) != 131072:
        raise ValueError('Expected a loaded 65536-word little-endian grid')
    value = struct.unpack_from('<H', grade, (celula & 65535)*2)[0]
    return (value & 0x7fe0) >> 5 if value & 0x8000 else 65535


@dataclass
class ConsultaGradeImpacto:
    grade: object
    outras: object = None

    def __call__(self, nome, args):
        if nome == 'ChercheIndiceBatiment':
            return encontrar_estrutura_impacto(self.grade, *args)
        if self.outras is None:
            raise NotImplementedError('External impact query required: ' + nome)
        return self.outras(nome, args)
