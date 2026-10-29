"""Original-only leaf input fixtures; no reconstructed game rule."""

PESQUISA = 0x5080f4
ESTRUTURAS = 0x49a0c8
PASSO = 276
FUNCOES_ESTRUTURA = (0x41a08c, 0x41a4f4)


def cenarios():
    """Return 14 inherited-input scenarios, containing 20 original calls."""
    pesquisa_base = bytes((i*29+7) & 255 for i in range(64))
    estruturas_base = bytes(range(256))*1078 + bytes(range(32))
    assert len(estruturas_base) == 276000
    casos = []
    for j, valor in enumerate((0, 1, 128, 255)):
        pesquisa = bytearray(pesquisa_base)
        pesquisa[j*16+j] = valor
        casos.append(dict(nome=f'research-read-owner-{j}', pesquisa=bytes(pesquisa),
                          estruturas=estruturas_base,
                          chamadas=[dict(entrada=0x4717c2, regs=dict(EAX=0xaced1200|j, EDX=0xbeef0000|j))]))
    for j, valor in enumerate((0, 3, 128, 255)):
        casos.append(dict(nome=f'research-write-owner-{j}', pesquisa=pesquisa_base,
                          estruturas=estruturas_base,
                          chamadas=[dict(entrada=0x470b37, regs=dict(EAX=0xaced1200|j, EDX=0xbeef1200|valor))]))
    for indice in (0, 999):
        for estado, dono, tipo in ((0, 0, 2), (3, 200, 3), (5, 255, 255)):
            estruturas = bytearray(estruturas_base)
            p = indice*PASSO
            estruturas[p+4], estruturas[p+5], estruturas[p+8] = dono, estado, tipo
            casos.append(dict(nome=f'structure-{indice}-state-{estado}', pesquisa=pesquisa_base,
                              estruturas=bytes(estruturas),
                              chamadas=[dict(entrada=a, regs=dict(EAX=0xa55a0000|indice, EDX=0xbeefcafe))
                                        for a in FUNCOES_ESTRUTURA]))
    return casos
