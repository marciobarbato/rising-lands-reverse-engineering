"""Economic prefix of SortieTroupe, ending before world position/type conversion.

The result is a pending dependency, never evidence that a unit has spawned.
Only Bag modes 1 (unit type) and 2 (resource ID) are needed by this prefix.
"""
from dataclasses import dataclass
import struct

from recrutamento import Recrutamento, _word


@dataclass(frozen=True)
class PreparacaoSaidaTropa:
    """Arguments at call 0x420f5a; no world callback has executed yet.

    CalculPosition 0x420698 receives AX=indice and BL=direcao, returns AX=cell.
    The next call is EnginSetType 0x457b87 with EAX=unidade, DX=cell,
    CL=tipo_unidade. This is a snapshot: the original reloads building +0x7b
    after CalculPosition returns. All later effects remain outside this API.
    """
    indice: int
    direcao: int
    unidade: int
    tipo_unidade: int
    endereco_dependencia: int = 0x420698


def _bag(bloco, base):
    quantidade, capacidade = struct.unpack_from('<HH', bloco, base)
    if quantidade > 30 or capacidade > 30:
        raise ValueError('Protected Bag domain requires count/capacity in 0..30')
    return quantidade, capacidade


def _alvo(bloco, base, slot, modo, tipo, unidades):
    if bloco[base + 0x42 + slot] != modo:
        return False
    valor = _word(bloco, base + 6 + slot * 2)
    if modo == 1:
        if valor >= 800:
            raise ValueError('Protected unit reference must be in 0..799')
        return unidades[valor * 276 + 1] == tipo
    return valor == tipo


def _contem_recurso(bloco, base, recurso):
    # BagContient mode 2 counts matches over capacity, not live count.
    _, capacidade = _bag(bloco, base)
    return sum(_alvo(bloco, base, i, 2, recurso, None) for i in range(capacidade))


def _retirar(bloco, base, modo, tipo, unidades=None):
    """BagRetire 0x4472ea for the two modes used here; no other Bag API."""
    quantidade, _ = _bag(bloco, base)
    for slot in range(quantidade):
        if not _alvo(bloco, base, slot, modo, tipo, unidades):
            continue
        valor = _word(bloco, base + 6 + slot * 2)
        # The original decrements +0x66 even for resource entries, wrapping u16.
        struct.pack_into('<H', bloco, base + 0x66, (_word(bloco, base + 0x66) - 1) & 65535)
        for seguinte in range(slot, quantidade - 1):
            bloco[base + 0x42 + seguinte] = bloco[base + 0x43 + seguinte]
            struct.pack_into('<H', bloco, base + 6 + seguinte * 2,
                             _word(bloco, base + 8 + seguinte * 2))
        bloco[base + 0x42 + quantidade - 1] = 0
        struct.pack_into('<H', bloco, base + 6 + (quantidade - 1) * 2, 0)
        struct.pack_into('<H', bloco, base, quantidade - 1)
        return valor
    return 65535


class SaidaTropa:
    def __init__(self, recrutamento=None):
        self.recrutamento = Recrutamento() if recrutamento is None else recrutamento

    def preparar(self, indice, direcao):
        """SortieTroupe 0x420e4c..0x420f5a, stopping BEFORE CalculPosition.

        AX/ DL truncate to u16/u8. Below time(type u8)*100 returns None without
        mutations. There is no active/owner/building-type eligibility test here.
        At the threshold, remove the first tagged type-9 unit, then repeatedly
        remove resource ID 2 and credit 2 stone per entry; next ID 1 and credit
        1 food per entry. Each removal precedes its deposit. Deposits use the
        building owner byte and building index and retain existing partial
        failure semantics. No costs, conversion, cleanup or messages follow.

        Missing/invalid unit references and malformed Bags are protected-domain
        ValueErrors, not invented original returns. A stale matching resource
        beyond live count is rejected when removal fails, after earlier effects.
        Do not retry this prefix after failure or after receiving the handoff.
        """
        indice &= 65535
        direcao &= 255
        r = self.recrutamento
        o = r._offset(indice)
        s = r.mundo.estruturas
        tipo = s[o + 0x7b]
        if struct.unpack_from('<I', s, o + 0x8c)[0] < r.tempo_unidade(tipo) * 100:
            return None
        unidade = _retirar(s, o + 0xc, 1, 9, r.unidades)
        if unidade >= 800:
            raise ValueError('SortieTroupe requires an existing type-9 unit in the building Bag')
        base = unidade * 276 + 0xa  # EnginGetBag 0x4474a6.
        for recurso in (2, 1):
            while _contem_recurso(r.unidades, base, recurso):
                quantidade = _retirar(r.unidades, base, 2, recurso)
                if quantidade == 65535:
                    raise ValueError('Resource tag beyond live Bag count is outside the terminating domain')
                r.mundo.adicionar(s[o + 4], recurso, quantidade, indice)
        return PreparacaoSaidaTropa(indice, direcao, unidade, s[o + 0x7b])
