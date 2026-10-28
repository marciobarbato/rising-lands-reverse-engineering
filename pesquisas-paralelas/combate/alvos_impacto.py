"""Read-only ChercheIndiceEnginCible, using committed combat cell geometry."""
from dataclasses import dataclass

from alvos_alcance import ocupa_celula


def encontrar_vitima_impacto(unidades, celula, excluida=65535, flag=0):
    """0x4465df: AX=cell, DX=excluded ID, BL=flag; full EAX result.

    Scan 800 live 276-byte records in ascending ID order. The zero flag uses
    ContientCellule filter 1; every nonzero byte uses filter 2. Ground matches
    overwrite the candidate; elevated matches return immediately. No alliance,
    owner, life, distance or navigation filters are added. No memory is written.
    """
    if len(unidades) != 800 or any(len(u) != 276 for u in unidades):
        raise ValueError('Expected 800 readable 276-byte unit records')
    celula, excluida, flag = celula & 65535, excluida & 65535, flag & 255
    candidate = 65535
    for index, unit in enumerate(unidades):
        if index == excluida or unit[2] in (0, 4) or not unit[0x72]:
            continue
        if not ocupa_celula(unit, celula, 1 + int(bool(flag))):
            continue
        candidate = index
        if unit[0xab]:
            return index
    return candidate


@dataclass
class ConsultaAlvosImpacto:
    unidades: object
    outras: object = None

    def __call__(self, nome, args):
        if nome == 'ChercheIndiceEnginCible':
            return encontrar_vitima_impacto(self.unidades, *args)
        if self.outras is None:
            raise NotImplementedError('External impact query required: ' + nome)
        return self.outras(nome, args)
