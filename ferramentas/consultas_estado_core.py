"""Exact seven-register read-only queries, captured original-first in consultas-estado-original.json.xz.

EnginEstVivant 0x443dad..0x443ddd: AX index (protected 0..799), full EAX = state not 0/4. The address
0x4731d3 is a caller, not the entry. BatimentGetDecalageConstruction 0x41aea4..0x41aee2: AL type, full EAX
= table offset for 0..21, else zero. Reuse SelecaoOrdens._vivo and DECALAGEM; no duplicated game rule.
Every other register is preserved. No stores/callbacks. Optional entry ESP returns ESP+4 on chamar; the
externo provider uses the seven-register protocol and does not model control flow or flags.
Intact executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb.
"""
from entrada_estruturas import ArgumentoNaoPassado
from selecao_ordens import SelecaoOrdens, DECALAGEM

REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff
ROTINAS = {'EnginEstVivant': 0x443dad, 'BatimentGetDecalageConstruction': 0x41aea4}


def exigir_registradores(nome, chamada, regs, *, esp=False):
    exigidos = REG7 + (('ESP',) if esp else ())
    faltando = [k for k in exigidos if k not in regs]
    if faltando:
        raise ArgumentoNaoPassado(nome, chamada, faltando)
    entrada = {k: regs[k] & M32 for k in REG7}
    if 'ESP' in regs:
        entrada['ESP'] = regs['ESP'] & M32
    return entrada


class ConsultasEstadoCore:
    def __init__(self, memoria):
        self.ordens = SelecaoOrdens(memoria)

    def chamar(self, nome, regs, pilha=()):
        if nome not in ROTINAS:
            raise KeyError(nome)
        if pilha:
            raise ValueError(f'{nome} takes no pushed words')
        r = exigir_registradores(nome, ROTINAS[nome], regs)
        if nome == 'EnginEstVivant':
            if r['EAX'] & 0xffff >= 800:
                raise ValueError('EnginEstVivant protected unit index requires AX in 0..799')
            self.ordens._vivo(r)
        else:
            tipo = r['EAX'] & 0xff
            r['EAX'] = DECALAGEM[tipo] if tipo <= 0x15 else 0
        if 'ESP' in r:
            r['ESP'] = (r['ESP'] + 4) & M32
        return r


def provedor_consultas_estado(consultas, outros=None):
    """externo(nome, chamada, regs) -> all seven exact registers; missing inputs raise before reads."""
    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise KeyError(f'{nome} at 0x{chamada:x}: no Core state-query provider')
            return outros(nome, chamada, regs)
        entrada = exigir_registradores(nome, chamada, regs)
        if regs.get('_pilha'):
            raise ValueError(f'{nome} takes no pushed words')
        saida = consultas.chamar(nome, entrada)
        return {k: saida[k] for k in REG7}
    return externo
