"""Bind Combat's public state-1/24 body to the live AI/runtime dispatcher.

The original parent entry is committed before this adapter (9ce27f6).
DI is the u16 unit and ESI its live record at 0x456886; the body to 0x454ccd
is a void API. No attack algorithm, defaults or foreign effects live here.
"""
from reinicio_ia import DependenciaIA


class AtaqueDespacho:
    def __init__(self, memoria, mundo):
        self.m, self.mundo, self.combate = memoria, mundo, None

    def ramo(self, sitio, unidade):
        from combate_raid_vivo import CombateRaidVivo, DependenciaCombateRaid
        from ataque_vivo import DependenciaAtaqueVivo
        if not 0 <= unidade < 800:
            raise ValueError('Attack dispatcher requires a zero-extended unit in 0..799')
        if self.combate is None:
            self.combate = CombateRaidVivo(self.m, mundo=self.mundo)
        try:
            return self.combate.ramo(unidade)
        except (DependenciaCombateRaid, DependenciaAtaqueVivo) as error:
            raise DependenciaIA(str(error), error.endereco) from error
