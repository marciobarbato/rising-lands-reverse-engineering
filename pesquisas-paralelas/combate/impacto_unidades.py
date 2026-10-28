"""InfligeDegat mode-1/3/4 unit branches, with explicit world-effect providers.

Original [0x450874,0x4510dd). Building damage is a named stop. World lookup,
navigation, diplomacy and sound remain callbacks; the unit consumer and live
projectile pool can be supplied directly from the other combat modules.
"""
from dataclasses import dataclass
import struct

from projeteis import u16

RETALIATION_TYPES = frozenset((0, 1, 2, 3, 8, 11, 12, 15, 16, *range(18, 26)))
SMALL_HIT_TYPES = frozenset((0, 1, 2, *range(4, 11), *range(18, 25)))


class LimiteImpactoBatiment(NotImplementedError):
    endereco = 0x4508af


@dataclass
class ImpactoUnidades:
    unidades: object
    pool: object
    consumir: object = None
    consulta: object = None
    efeito: object = None
    contador: int = 0
    jogador_local: int = 0
    ultimo_alerta: int = 0
    celula_alerta: int = 0

    def __post_init__(self):
        if len(self.unidades) != 800 or any(len(u) != 276 for u in self.unidades):
            raise ValueError('Expected 800 live 276-byte unit records')

    def _query(self, name, *args):
        if self.consulta is None:
            raise NotImplementedError('External impact query required: ' + name)
        return self.consulta(name, args)

    def _effect(self, name, *args):
        if self.efeito is None:
            raise NotImplementedError('External impact effect required: ' + name)
        self.efeito(name, args)

    def receber(self, name, args):
        """PoolProjeteis.efeito_externo adapter; only accepts InfligeDegat."""
        if name != 'InfligeDegat':
            raise NotImplementedError('Unsupported projectile effect: ' + name)
        return self.infligir(*args)

    def _reagir(self, victim, attacker, owner, kind, mode=1):
        target, source = self.unidades[victim], self.unidades[attacker]
        if owner == 200:
            return
        player_type = self._query('PlayerGetType', owner) & 255
        if player_type == 1 and target[2] in (5, 18):
            building = self._query('ChercheBatimentProximiteCaveOuSanctuaire',
                                   u16(target, 8), target[0]) & 65535
            if building != 65535:
                cell = self._query('BatimentGetCase', building) & 65535
                self._effect('SetDeplaceEngin', victim, cell)
            return
        eligible = (mode == 1 and kind in RETALIATION_TYPES and not target[0xdc] & 2
                    and source[1] not in (10, 17)
                    and (source[1] != 16 or kind in (2, 8))
                    and source[0] != owner)
        if eligible:
            player_type = self._query('PlayerGetType', owner) & 255
            if player_type == 1:
                previous = struct.unpack_from('<I', target, 0x110)[0]
                if target[2] == 7 or ((self.contador - previous) & 0xffffffff) > 250:
                    self._effect('SetAttaqueEngin', victim, 1, attacker)
            elif self._query('PlayerGetType', owner) & 255 == 2 and target[2] == 7:
                self._effect('SetAttaqueEngin', victim, 1, attacker)
            return
        origin = (self._query('BatimentGetCase', attacker) & 65535) if mode == 3 else (
            0 if mode == 4 else u16(source, 0x7c))
        direction = self._query('CalculDirection', origin, u16(target, 0x7c)) & 255
        cell = self._query('CalculDirCase', u16(target, 0x7c), direction) & 65535
        if cell != 65535:
            self._effect('SetDeplaceEngin', victim, cell)

    def _apresentar(self, cell, kind):
        if kind in SMALL_HIT_TYPES:
            self.pool.iniciar(14, cell, cell, 0, 0, 0, 0, 0, 0)
        elif 11 <= kind <= 17:
            value = self._query('Random', 0x22) & 0xffffffff
            self.pool.iniciar(15 + (value & 1), cell, cell, 0, 0, 0, 0, 0, int(kind == 16))

    def _diplomacia(self, victim, attacker, mode=1):
        target, source = self.unidades[victim], self.unidades[attacker]
        owner = (self._query('BatimentGetPlayer', attacker) & 255) if mode == 3 else source[0]
        if self._query('PlayerEstAllie', owner, target[0]) & 255:
            self._effect('MAJSympathie', target[0], owner, 10)
            self._effect('MAJSympathie', target[0], owner, 6)
            self._effect('PlayerResetAllie', owner, target[0])
            self._effect('PlayerResetAllie', target[0], owner)
        self._effect('PlayerAAttaqueSet', owner, target[0])
        if mode == 3:
            return  # Original building-source suffix has no unit alert block.
        if target[0] == owner or target[0] != (self.jogador_local & 255):
            return
        now, previous = self.contador & 0xffffffff, self.ultimo_alerta & 0xffffffff
        if previous <= now and now - previous < 200:
            return
        self.ultimo_alerta = self.contador & 0xffffffff
        self.celula_alerta = u16(target, 0x7c)
        # Final token identifies original pointer 0x496ac8 (cell at +4),
        # instead of pretending it is a pointer into a Python unit record.
        self._effect('PlaySnd_PostSound', 0x50, (target[1] << 16) | 0x700,
                     0, 0x100, '0x496ac8')

    def infligir(self, cell, mode, attacker, direction, flag):
        """AX/DL/BX/CL/stack-byte inputs; modes 1/3/4 (4 needs CL 29/30).

        Input widths truncate first. Empty unit lookup returns None. Building,
        missing providers and consumer exceptions stop without rollback.
        Query-return IDs/types are checked before dereferencing live records.
        """
        cell, mode, attacker = cell & 65535, mode & 255, attacker & 65535
        direction, flag = direction & 255, flag & 255
        if mode not in (1, 3, 4):
            raise NotImplementedError('Only InfligeDegat mode 1, 3 or 4 is supported')
        if mode == 4 and direction not in (29, 30):
            raise NotImplementedError('Mode-4 impact requires initialized direction byte 29/30')
        if not 0 <= attacker < 800:
            raise ValueError('Expected an attacker ID in 0..799')
        if not flag and self._query('ChercheIndiceBatiment', cell) & 65535 != 65535:
            raise LimiteImpactoBatiment('Building branch at 0x4508af is external')
        victim = self._query('ChercheIndiceEnginCible', cell, 65535, flag) & 65535
        if victim == 65535:
            return
        if victim >= 800:
            raise ValueError('Resolved victim ID must be in 0..799 or 0xffff')
        target = self.unidades[victim]
        owner, kind = target[0], target[1]
        if kind >= 26 or self.unidades[attacker][1] >= 26:
            raise ValueError('Supported unit types are 0..25')
        self._reagir(victim, attacker, owner, kind, mode)
        if self.consumir is None:
            raise NotImplementedError('External consumer required: EnginInfligeDegat')
        self.consumir(victim, mode, attacker, direction)
        self._apresentar(cell, kind)
        self._diplomacia(victim, attacker, mode)
