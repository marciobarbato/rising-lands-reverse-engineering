"""Bounded physical SetDyingEngin path, with explicit unresolved native branches.

The caller supplies the prior life mutation. This callee changes state and
collision for supported ordinary units; it never silently drops a dependency.
"""
import struct


class DependenciaMorteUnidade(NotImplementedError):
    def __init__(self, unidade, efeito, endereco, checkpoint):
        self.unidade, self.efeito = unidade, efeito
        self.endereco, self.checkpoint = endereco, checkpoint
        super().__init__(f'{efeito} required for unit {unidade} at 0x{endereco:08x}; '
                         'earlier effects retained, entry retry is not a continuation')


def iniciar_morte_unidade(mundo, indice):
    """Original SetDyingEngin, with complete ordinary hidden-unit returns.

    Supports core physical worlds, unit AX 0..799 and known participating types
    0..25. Common complete path needs no AI group effect, sound handle -1,
    hidden current cell, empty Bag, unselected record, and type outside 11..17.
    Unsupported branches stop at documented original boundaries. No life,
    inventory, selection-count, sound, projectile or special-flag effect is
    synthesized. All prior local/physical changes survive a dependency stop.
    """
    indice = mundo._indice(indice)
    if not isinstance(mundo.unidades, bytearray) or len(mundo.unidades) != 220800:
        raise ValueError('SetDyingEngin requires the writable 800-record unit pool')
    p, u = indice * 276, mundo.unidades
    if u[p+0xdc] & 4:
        raise DependenciaMorteUnidade(indice, 'SetDyingEngin +dc bit-2 branch', 0x444c7e, 0x444c7e)
    if not mundo.viva(indice):
        return
    tipo, dono = u[p+1], u[p]
    if tipo >= 26 or not 0 <= mundo.jogador_local < 4:
        raise ValueError('Participating death requires known unit type and local camera 0..3')
    grupo = struct.unpack_from('<I', u, p+0x10c)[0]
    # Original message 0x44 returns without effects for non-AI control, or
    # the null group. Group mutations/task wakeups remain a separate provider.
    if (dono >= 4 or mundo.controle_jogadores[dono] == 2) and grupo != 0xffffffff:
        raise DependenciaMorteUnidade(indice, 'iagUnitSendMessage group effect', 0x4829c8, 0x482c58)
    if struct.unpack_from('<I', u, p+0x104)[0] != 0xffffffff:
        raise DependenciaMorteUnidade(indice, 'PlaySnd_StopSound active handle', 0x48aac0, 0x48a446)
    atual = struct.unpack_from('<H', u, p+8)[0]
    if mundo._visivel(atual):
        raise DependenciaMorteUnidade(indice, 'EnginGetVolume/death sound', 0x440c5d, 0x440c5d)
    u[p+2] = 4
    mundo._liberar_busca(indice)
    if struct.unpack_from('<H', u, p+0xa)[0] != 0:
        raise DependenciaMorteUnidade(indice, 'EnginRetire nonempty Bag', 0x443dfc, 0x443dfc)
    u[p+0xa4] = 0
    struct.pack_into('<H', u, p+0xc2, 0)
    if u[p+0xbd] != 0:
        # DeselectionEngin clears this byte before its owner/counter helper.
        u[p+0xbd] = 0
        raise DependenciaMorteUnidade(indice, 'RetireSelectionEngin counters', 0x472576, 0x472683)
    mundo.ocupar(indice, atual, False)
    passo = struct.unpack_from('<H', u, p+0x7c)[0]
    if passo != atual:
        mundo.ocupar(indice, passo, False)
    if 11 <= tipo <= 17:
        if tipo == 16:
            raise DependenciaMorteUnidade(indice, 'ProjectileInit type 34 effect', 0x46e44c, 0x46e44c)
        raise DependenciaMorteUnidade(indice, 'Vehicle death random/effect', 0x4704dc, 0x4704dc)
