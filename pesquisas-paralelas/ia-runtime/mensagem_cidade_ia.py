"""iagVilleSendMessage 0x484808: original owner gate and exact returning registers.

S1 SortieTroupe CALL 0x4211e5 passes AX structure, DL 3 and EBX 0.
Non-AI owners return through 0x484919 without non-stack stores. AI dispatch
is a named stop at 0x48484c; no message body is replaced by an empty callback.
"""
from entrada_estruturas import ArgumentoNaoPassado
from reinicio_ia import DependenciaIA

REG7 = ('EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP')
M32 = 0xffffffff
ARGUMENTOS = {'EAX': 0xffff, 'EDX': 0xff, 'EBX': M32}


def mensagem_cidade(m, regs, chamada=0x4211e5):
    """Return seven registers and explicit unknown masks; optional entry ESP -> ESP+4.

    Structure index is protected to 0..999. PlayerGetType is Economy's live
    query, called only for owners 0..3. Owner >=4 returns that owner byte.
    Earlier caller effects remain on all exceptions; this prefix makes none.
    """
    masks = dict(regs.get('_incertos') or {})
    missing = [k for k, mask in ARGUMENTOS.items() if k not in regs or masks.get(k, 0) & mask]
    if missing:
        raise ArgumentoNaoPassado('iagVilleSendMessage', chamada, missing)
    if regs.get('_pilha'):
        raise ValueError('iagVilleSendMessage takes no pushed arguments')
    structure = regs['EAX'] & 65535
    if structure >= 1000:
        raise ValueError('City message requires structure AX in 0..999')
    owner = m.u8(0x49a0c8 + 276 * structure + 4)
    result = owner
    if owner < 4:
        # Reuse the committed Economy provider over this same live memory.
        from provedores_entrada_ia import _modulo_economia
        result = _modulo_economia('quadro_economia').tipo_jogador(m, owner) & 255
        if result == 2:
            raise DependenciaIA(f'iagVilleSendMessage AI owner {owner}, message 0x{regs["EDX"] & 255:x}, '
                                f'argument 0x{regs["EBX"] & M32:x}', 0x48484c)
    out = {k: regs.get(k, 0) & M32 for k in REG7}
    out.update(EAX=result, EBX=structure, EDX=regs['EBX'] & M32)
    unknown = {k: masks.get(k, 0) if k in regs else M32 for k in ('ECX', 'ESI', 'EDI', 'EBP')}
    unknown = {k: v & M32 for k, v in unknown.items() if v}
    if unknown:
        out['_incertos'] = unknown
    if 'ESP' in regs:
        out['ESP'] = (regs['ESP'] + 4) & M32
    return out
