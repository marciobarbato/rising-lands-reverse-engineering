"""Live-memory register providers for the two original turret input leaves.

The seven Watcom general registers are required, with no invented defaults.
Optional ESP/EFLAGS and an explicit return address expose the leaf ABI too.
No game bytes are initialized and foreign read-only queries use their owners.
"""
from ambiente_combate_raid import ROOT  # noqa: F401
from bonus_unidades import BonusUnidades
from chamadas_quadro_core import caso_estrutura

REGISTERS = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
STRUCTURES = 0x49a0c8
SELECTION = 0x495be0
MASK = 0xffffffff


def _flags(a, b, width, *, add=False):
    mask = (1 << width) - 1
    a &= mask; b &= mask
    result = (a + b if add else a - b) & mask
    sign = 1 << (width - 1)
    carry = a + b > mask if add else a < b
    overflow = (~(a ^ b) & (a ^ result) if add else (a ^ b) & (a ^ result)) & sign
    return (int(carry) | (int(bin(result & 255).count('1') % 2 == 0) << 2)
            | ((a ^ b ^ result) & 16) | (int(result == 0) << 6)
            | (int(bool(result & sign)) << 7) | (int(bool(overflow)) << 11))


class OrdensTorresCombate:
    """BatimentPeutAttaquer/InitAttaqueSelect on the caller's live address space.

    Turret target modes 1/3/5 are initialized. Other turret modes read native
    uninitialized stack locals and raise instead of inventing a target cell.
    Non-turret prefixes accept every mode. Setter accepts every mode byte.
    """
    def __init__(self, memoria, *, bonus=None):
        self.m = memoria
        self.bonus = BonusUnidades.da_memoria(memoria) if bonus is None else bonus

    @staticmethod
    def _id(value, maximum, kind):
        value &= 65535
        if value >= maximum:
            raise ValueError(f'Protected {kind} index requires 0..{maximum-1}')
        return value

    @staticmethod
    def _finish(regs, out, arithmetic, retorno):
        if 'EFLAGS' in regs:
            out['EFLAGS'] = ((regs['EFLAGS'] & ~0x8d5) | arithmetic) & MASK
        if 'ESP' in regs:
            out['ESP'] = (regs['ESP'] + 4) & MASK
        if retorno is not None:
            out['EIP'] = retorno & MASK
        return out

    def batiment_init_attaque_select(self, regs, *, retorno=None):
        """0x4242cc; AL player, DL mode, BX reference; reference store then mode."""
        out = {k: regs[k] & MASK for k in REGISTERS}
        player = regs['EAX'] & 255
        if player >= 4:
            raise ValueError('Protected selection requires player 0..3')
        selected = self._id(self.m.u16(SELECTION + 2 * player), 1000, 'structure')
        mode, reference = regs['EDX'] & 255, regs['EBX'] & 65535
        record = STRUCTURES + 276 * selected
        arithmetic = _flags(mode, 3, 32)
        if mode == 3:
            arithmetic = _flags(reference, selected, 16)
        if mode != 3 or reference != selected:
            self.m.u16(record + 0x86, reference)
            self.m.u8(record + 0x7b, mode)
        out.update(EAX=record, EBX=mode, EDX=2 * player)
        return self._finish(regs, out, arithmetic, retorno)

    def batiment_peut_attaquer(self, regs, *, retorno=None):
        """0x42436c; AX source, DL mode, BX target; bool is only low AL."""
        out = {k: regs[k] & MASK for k in REGISTERS}
        if 'EFLAGS' in regs and 'ESP' not in regs:
            raise ValueError('BatimentPeutAttaquer EFLAGS requires actual entry ESP')
        source = self._id(regs['EAX'], 1000, 'structure')
        record = STRUCTURES + 276 * source
        kind, mode = self.m.u8(record + 8), regs['EDX'] & 255
        out.update(EAX=0, EBX=record, EDX=source)

        def finish():
            # All paths share ADD ESP,14h after the four saved registers.
            arithmetic = _flags((regs['ESP'] - 36) & MASK, 20, 32, add=True) if 'EFLAGS' in regs else 0
            return self._finish(regs, out, arithmetic, retorno)

        if kind not in (10, 11):
            return finish()
        if mode not in (1, 3, 5):
            raise ValueError('Turret modes outside 1/3/5 read uninitialized native stack locals at 0x424590')
        target = regs['EBX'] & 65535
        if mode == 1:
            target = self._id(target, 800, 'unit')
            unit = self.m.u32(0x4e19a0) + 276 * target
            out['EDX'] = target
            if self.m.u8(unit) == 200:
                return finish()
            if self.m.u8(unit + 1) in (16, 17):
                out['EDX'] = source
                if kind == 10:
                    return finish()
        elif mode == 3:
            target = self._id(target, 1000, 'structure')
            out['EDX'] = target
            if self.m.u8(STRUCTURES + 276 * target + 4) == 200:
                return finish()

        origin = self.m.u16(record + 2)
        owner = self.m.u8(record + 4)
        bonus = self.bonus.consultar(owner, 11, 4, ecx=7) & MASK
        out.update(EAX=bonus & 0xffffff00, EBX=mode, EDX=4 if owner in (4, 200) else 11)
        if mode == 5:
            return finish()
        # The intact caller repeats both original getters. Preserve that order.
        def cell():
            return (self.m.u16(unit + 0x7c) if mode == 1 else caso_estrutura(self.m, target)['EAX'] & 65535)
        target_x = cell() & 255
        target_y = cell() >> 8
        source_x, source_y = origin & 255, origin >> 8
        distance_x = abs(source_x - target_x)
        distance_y = abs(source_y - target_y)
        distance = (distance_x * distance_x + distance_y * distance_y) & MASK
        # Distance2d's EBX/EDX survive the caller, including its asymmetric Y branch.
        if source_y > target_y:
            out.update(EBX=target_y, EDX=distance_y * distance_y)
        else:
            out.update(EBX=distance_y, EDX=distance_y * distance_y)
        radius = (7 + bonus) & 65535
        out['EAX'] = (distance & 0xffffff00) | int(distance <= radius * radius)
        return finish()

    def provedores(self):
        """Update AI/runtime's funcoes dict with these named register callables."""
        return {'BatimentPeutAttaquer': self.batiment_peut_attaquer,
                'BatimentInitAttaqueSelect': self.batiment_init_attaque_select}

    def chamar(self, nome, regs, *, retorno=None):
        return self.provedores()[nome](regs, retorno=retorno)
