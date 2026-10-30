"""TuyauEstSortie 0x420c7c: exact S1 live structure query.

AX indexes a 276-byte structure at 0x49a0c8. AL is one iff byte +0x76
is exactly 15 and byte +0x75 is nonzero; EAX's upper 24 bits are the
structure pointer's. EDX and all other registers are preserved. No writes
or callbacks. This is a query, not the animation that changes those bytes.
"""
from lacunas_economia_s1 import REG7, M32, exigir

ROTINAS = {'TuyauEstSortie': 0x420c7c}


class TuyauEconomiaS1:
    def __init__(self, memoria):
        self.m = memoria

    def chamar(self, nome, regs):
        if nome not in ROTINAS:
            raise KeyError(nome)
        r = exigir(nome, ROTINAS[nome], regs)
        indice = r['EAX'] & 0xffff
        if indice >= 1000:
            raise ValueError('TuyauEstSortie requires a structure AX in 0..999')
        p = 0x49a0c8 + 276*indice
        valor = self.m.u8(p+0x76) == 15 and self.m.u8(p+0x75) != 0
        r['EAX'] = (p & 0xffffff00) | int(valor)
        if 'ESP' in r:
            r['ESP'] = (r['ESP']+4) & M32
        return r


def provedor_tuyau_economia_s1(consultas, outros=None):
    """All-seven-register external provider; missing registers fail before reads."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise KeyError(f'{nome} at {chamada:#x}: no Tuyau provider')
            return outros(nome, chamada, regs)
        r = exigir(nome, chamada, regs)
        if regs.get('_pilha'):
            raise ValueError(f'{nome} takes no pushed arguments')
        saida = consultas.chamar(nome,r)
        return {k:saida[k] for k in REG7}
    return externo
