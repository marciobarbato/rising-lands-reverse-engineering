"""Exact-register Economy queries observed in the replay-checked S1 trajectory.

SacGetCapacite 0x475736 (InputGame CALL 0x4299da): AX is a cell into
[0x507d74]. Types 0x42..0x44 return the quantity byte from [0x507dac]
in AX, keeping that pointer's upper half in EAX; other types return EAX=0.
EDX and the other six registers are preserved; no stores or callbacks.
The original-first capture includes every object byte and quantity edges.
Memory is live u8/u16/u32; grids must hold all 65,536 cells, like the original.
"""
from entrada_estruturas import ArgumentoNaoPassado

REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff
ROTINAS = {'SacGetCapacite': 0x475736}


def exigir(nome, chamada, regs):
    faltando = [k for k in REG7 if k not in regs]
    if faltando:
        raise ArgumentoNaoPassado(nome, chamada, faltando)
    return {k: regs[k] & M32 for k in REG7 + (('ESP',) if 'ESP' in regs else ())}


class LacunasEconomiaS1:
    def __init__(self, memoria):
        self.m = memoria

    def chamar(self, nome, regs):
        if nome not in ROTINAS:
            raise KeyError(nome)
        r = exigir(nome, ROTINAS[nome], regs)
        celula = r['EAX'] & 0xffff
        tipo = self.m.u8(self.m.u32(0x507d74) + celula)
        if 0x42 <= tipo <= 0x44:
            quantidades = self.m.u32(0x507dac)
            r['EAX'] = (quantidades & 0xffff0000) | self.m.u8(quantidades + celula)
        else:
            r['EAX'] = 0
        if 'ESP' in r:
            r['ESP'] = (r['ESP'] + 4) & M32
        return r


def provedor_lacunas_economia_s1(consultas, outros=None):
    """externo(name, CALL address, all seven registers) -> all seven exact exit registers.

    ESP is optional control state, omitted from the provider result. Any missing
    register raises ArgumentoNaoPassado before memory is read. Unknown names are
    passed to outros or raise KeyError; no unknown result is synthesized.
    """
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise KeyError(f'{nome} at {chamada:#x}: no Economy S1 query provider')
            return outros(nome, chamada, regs)
        entrada = exigir(nome, chamada, regs)
        if regs.get('_pilha'):
            raise ValueError(f'{nome} takes no pushed arguments')
        saida = consultas.chamar(nome, entrada)
        return {k: saida[k] for k in REG7}
    return externo
