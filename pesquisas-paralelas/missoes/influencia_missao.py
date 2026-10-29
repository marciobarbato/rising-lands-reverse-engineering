"""Influence-zone queries over the table LoadCadreInfluence 0x47c04a fills.

Translated after the original-only captures at the exact MONDE01 frame-1
inputs (evidencias/captura-influencia-quadro1.json).  The table is the live
4,000-byte view at 0x50c614: 400 records of 10 bytes, words +0 x0, +2 y0,
+4 x1, +6 y1 (+8/+9 are not read by these queries).  Every reference to the
table in the intact code lies in the Missions influence cluster
0x47bf2c..0x47c138 (InfluenceReset, CaseGetZoneInfluence, CaseInZoneInfluence,
LoadCadreInfluence, SaveCadreInfluence, GetTopLeftCaseZoneInfluence).
Importing this module executes nothing.
"""
REGISTROS, PASSO = 400, 10
NENHUMA = 0xff


def _tabela(influencia):
    try:
        v = memoryview(influencia)
    except TypeError as erro:
        raise ValueError('Influence queries require the explicit 4,000-byte table view at 0x50c614') from erro
    if v.ndim != 1 or not v.c_contiguous or v.itemsize != 1 or len(v) != REGISTROS*PASSO:
        raise ValueError('Influence queries require exactly 4,000 contiguous bytes at 0x50c614')
    return v.cast('B')


def _u16(v, o):
    return v[o] | v[o+1] << 8


def zona_influencia(influencia, celula):
    """CaseGetZoneInfluence 0x47bf66: EAX = first zone 0..399 (record 255 skipped) whose
    rectangle holds the cell, else 0xff.

    Only AX is consumed: x = AX & 0xff, y = AX >> 8 (the original's signed
    idiv/sar on a zero-extended u16).  Bounds are unsigned 16-bit and
    inclusive.  EBX/ECX/EDX are preserved by the original; no store.
    """
    v = _tabela(influencia)
    celula &= 0xffff
    x, y = celula & 0xff, celula >> 8
    for z in range(REGISTROS):
        if z == NENHUMA:
            continue
        o = PASSO*z
        if _u16(v, o) <= x <= _u16(v, o+4) and _u16(v, o+2) <= y <= _u16(v, o+6):
            return z
    return NENHUMA


def canto_zona_influencia(influencia, zona):
    """GetTopLeftCaseZoneInfluence 0x47c114: EAX = x0 + (y0 << 8) of record AX, as u32.

    EAX keeps the upper bits of 5*AX (the original indexes with ``eax*2`` after
    ``lea``-style 5*AX and only reloads AX), and the addition carries into
    them, e.g. an empty record (x0 = y0 = 0xffff) gives 0x0100feff.  The
    original reads beyond the table for AX >= 400; this API protects 0..399.
    EDX is preserved; no store.
    """
    v = _tabela(influencia)
    zona &= 0xffff
    if zona >= REGISTROS:
        raise ValueError('GetTopLeftCaseZoneInfluence protected record index is 0..399 (the original reads beyond)')
    o = PASSO*zona
    return (((5*zona) & 0xffff0000) | _u16(v, o)) + (_u16(v, o+2) << 8) & 0xffffffff
