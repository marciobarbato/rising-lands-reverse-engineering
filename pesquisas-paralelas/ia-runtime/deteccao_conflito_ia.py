"""S1's iabDetection_AjouteEnnemiOuAlerteConflit 0x489b5a adapter.

Original-first real call: s1-deteccao-conflito-original.json, frame11663.
Reuse Combat's committed synchronous behaviour9 message model and Core's
ResetOrdre; do not fork their battle insertion, targeting or task stores.
The scalar dispatcher discards exit registers; the raw API preserves all
handler registers except its actual EAX/EDX results. No frame/solver advances.
"""
from entrada_estruturas import ArgumentoNaoPassado
from reinicio_ia import DependenciaIA

REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff


class _Units:
    def __init__(self, m):
        self.m = m

    def __getitem__(self, index):
        if not 0 <= index < 800:
            raise ValueError('S1 unit index outside 0..799')
        return self.m.vista(self.m.u32(0x4e19a0)+276*index, 276)


class _Bonus:
    def __init__(self, m):
        self.m = m

    def consultar(self, player, kind, selector):
        from provedores_entrada_ia import _modulo_economia
        cls = _modulo_economia('bonus_unidades').BonusUnidades
        # The actual public neutral-owner branch reads no bonus buffer.
        # Other owners bind the live buffers before their first table lookup.
        owner = cls.__new__(cls) if player & 255 in (4, 200) else cls.da_memoria(self.m)
        return owner.consultar(player, kind, selector)


class _ByteRegion:
    def __init__(self, m, base, size):
        self.m, self.base, self.size = m, base, size

    def __getitem__(self, offset):
        if not 0 <= offset < self.size:
            raise IndexError(offset)
        return self.m.u8(self.base+offset)

    def __setitem__(self, offset, value):
        if not 0 <= offset < self.size:
            raise IndexError(offset)
        self.m.u8(self.base+offset, value)


def _order_world(m):
    """Core's ResetOrdre with its required live fields only, no world setup."""
    from ordens_unidades import MundoUnidades
    from mundo_vivo import BuscaViva

    class LiveReset(MundoUnidades):
        def __init__(self):
            self.unidades = _ByteRegion(m, m.u32(0x4e19a0), 800*276)
            self.estruturas = _ByteRegion(m, 0x49a0c8, 1000*276)
            self.busca = BuscaViva(m)

        def palavra(self, index, offset, value=None):
            return m.u16(m.u32(0x4e19a0)+276*self._indice(index)+offset, value)
    return LiveReset()


class _Combat:
    def __init__(self, m):
        self.unidades, self.bonus = _Units(m), _Bonus(m)
        self.core = _order_world(m)

    def definir_ataque(self, unit, mode, target):
        from ataque_vivo import definir_ataque
        return definir_ataque(self.unidades, unit, mode, target,
                              self.core.redefinir_ordem)


def detectar_alvo(m, unidade, alvo):
    """Effect-only semantic call used by iagUnitSendMessage's resolved handler.

    S1's monster owner4, behaviour9, normal mapped records/groups/battles.
    Combat owns its protected nested domains. Exceptions retain prior effects.
    """
    from mensagens_luta_combate import MensagensLuta
    from abi_luta_fatal_combate import DependenciaLutaFatal
    if not 0 <= unidade < 800:
        raise ValueError('Detection handler requires zero-extended EAX in 0..799')
    record = m.u32(0x4e19a0)+276*unidade
    if m.u8(record) != 4:
        raise DependenciaIA('Detection handler for non-monster AI owner', 0x489b8f)
    try:
        # Public synchronous message composition; repeated outer reads have no
        # stores. Only EAX/EDX are the resolved handler's exit values.
        return MensagensLuta(m, _Combat(m)).mensagem(unidade, 0x49, alvo)
    except DependenciaLutaFatal as error:
        raise DependenciaIA(str(error), error.endereco) from error


def detectar_registradores(m, regs):
    """Exact returning register adapter; optional ESP advances by four."""
    missing = [k for k in REG7 if k not in regs or (regs.get('_incertos') or {}).get(k)]
    if missing:
        raise ArgumentoNaoPassado('iabDetection_AjouteEnnemiOuAlerteConflit', 0x482e2e, missing)
    result = detectar_alvo(m, regs['EAX'], regs['EDX'])
    out = {k: regs[k] & M32 for k in REG7}
    out.update({k: result[k] & M32 for k in ('EAX', 'EDX')})
    if 'ESP' in regs:
        out['ESP'] = (regs['ESP']+4) & M32
    return out
