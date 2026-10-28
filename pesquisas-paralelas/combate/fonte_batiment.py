"""Mode-3 read-only source bridge over public structures and loaded damage rows.

Core owns the flat structure pool; no structure lifecycle or state is copied.
These callbacks provide the AL values consumed by damage, not a full-EAX ABI
for the original address-retaining record getters.
"""
from dataclasses import dataclass


@dataclass
class ConsultaFonteBatiment:
    estruturas: object
    danos_tipo10: object
    danos_tipo11: object
    outras: object = None

    def __post_init__(self):
        if len(self.estruturas) != 276000:
            raise ValueError('Expected the loaded 1000-record structure pool')
        if any(len(row) < 26 for row in (self.danos_tipo10, self.danos_tipo11)):
            raise ValueError('Expected two explicitly loaded 26-byte building damage rows')

    def __call__(self, nome, args):
        if nome in ('BatimentGetType', 'BatimentGetPlayer'):
            index, = args
            index &= 65535
            if index >= 1000:
                raise ValueError('Source structure ID is outside 0..999')
            return self.estruturas[index*276+(8 if nome == 'BatimentGetType' else 4)]
        if nome == 'TypeBatimentGetDegat':
            kind, selector, victim_type = (v & 255 for v in args)
            if selector != 1:
                raise NotImplementedError('Mode-3 source bridge supports damage selector 1 only')
            if victim_type >= 26:
                raise ValueError('Victim type must be in 0..25')
            if kind == 10:
                return self.danos_tipo10[victim_type]
            if kind == 11:
                return self.danos_tipo11[victim_type]
            return 0
        if self.outras is None:
            raise NotImplementedError('External damage query required: '+nome)
        return self.outras(nome, args)
