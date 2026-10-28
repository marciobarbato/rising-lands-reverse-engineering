"""Connect damage's legacy Modificateur callback to a loaded bonus provider.

Economy owns BonusGetValEngin/BonusUnidades. This adapter only permutes the
established callback arguments; it creates no default table or bonus values.
Selectors outside the damage consumer's 5/6 contract are explicit boundaries.
"""
from dataclasses import dataclass


@dataclass
class ConsultaBonusCombate:
    bonus: object
    outras: object = None

    def __call__(self, nome, args):
        if nome == 'Modificateur':
            dono, seletor, tipo = args
            if (seletor & 255) not in (5, 6):
                raise NotImplementedError('Damage bonus adapter supports selectors 5/6 only')
            if self.bonus is None:
                raise NotImplementedError('Loaded unit bonus provider required')
            # Preserve provider u16 selector5; the original damage caller
            # consumes its low byte. No ecx=0 fallback for inherited selectors.
            return self.bonus.consultar(dono, tipo, seletor)
        if self.outras is None:
            raise NotImplementedError('External damage query required: ' + nome)
        return self.outras(nome, args)
