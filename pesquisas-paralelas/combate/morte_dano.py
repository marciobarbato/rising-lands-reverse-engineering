"""Opt-in lethal tails of EnginInfligeDegat, delegating world lifecycle.

Opt in through ConsumidorDanoUnidade.morte for mode 1, or the separate
morte_sem_experiencia callback for modes 3/4. Default death stops are unchanged.
Level/lifecycle/sympathy are original named effect requests;
none are treated as successful when their provider is missing.
"""
from dataclasses import dataclass

from projeteis import por16


@dataclass
class MorteDanoUnidade:
    unidades: object
    pool: object
    efeito: object = None

    def _effect(self, name, *args):
        if self.efeito is None:
            raise NotImplementedError('External lethal effect required: ' + name)
        self.efeito(name, args)

    def _apos_dying(self, vitima, dono_fonte):
        target = self.unidades[vitima]
        flag = int(target[1] == 3 or 11 <= target[1] <= 17)
        self._effect('MAJSympathie', target[0], dono_fonte & 255, flag)

    def __call__(self, vitima, atacante, dano, celula_entrada, dono_fonte):
        """Internal consumer handoff: u16 IDs/cell, signed damage, u8 owner.

        Life is zeroed only after the optional level callback succeeds. The
        victim's type is reread after that callback and after SetDyingEngin.
        The victim-type-1 child uses the cell saved at consumer entry. The
        damage value is retained in this handoff for diagnostics; this tail
        does not subtract it a second time or reinterpret other damage modes.
        """
        vitima, atacante = vitima & 65535, atacante & 65535
        if vitima >= 800 or atacante >= 800:
            raise ValueError('Lethal consumer IDs must be in 0..799')
        source = self.unidades[atacante]
        if source[1] <= 10 or source[1] == 25:
            old = source[0xaf]
            # In the supported byte domain, (old & 31)+10 is always >=10.
            # Preserve the observed unconditional promotion request, even
            # at encoded level 7; the level provider owns any level clamp.
            source[0xaf] &= 0xe0
            self._effect('EnginSetLevelExperience', atacante, (old >> 5) + 1)
        return self.sem_experiencia(vitima, atacante, dano, celula_entrada, dono_fonte)

    def sem_experiencia(self, vitima, atacante, dano, celula_entrada, dono_fonte):
        """Original common tail after the mode-1-only award branch.

        Opt in only for modes with a defined saved owner (3/4). The consumer
        excludes 8/9. No source AF write or level request occurs in this tail.
        """
        vitima, atacante = vitima & 65535, atacante & 65535
        if vitima >= 800 or atacante >= 800:
            raise ValueError('Lethal consumer IDs must be in 0..799')
        target = self.unidades[vitima]
        por16(target, 0x9a, 0)
        if target[1] == 1:
            cell = celula_entrada & 65535
            self.pool.iniciar(6, cell, cell, 0, 0, 0, 0, 0, 0)
        self._effect('SetDyingEngin', vitima)
        self._apos_dying(vitima, dono_fonte)
