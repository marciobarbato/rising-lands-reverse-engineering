"""Shared raw Bag reset from the two inline EnginResetAll contexts."""
import struct


def resetar_bolsa(memoria, offset=0, *, ordem='tabela'):
    """Clear original fields/30 entries, preserving reserved bytes +60..+65.

    Field offsets in this docstring are hexadecimal. The two header orders
    come from the owner/type-table and unit-record native fragments.
    """
    gravavel = isinstance(memoria, bytearray) or (
        isinstance(memoria, memoryview) and not memoria.readonly and memoria.c_contiguous
        and memoria.ndim == 1 and memoria.itemsize == 1 and memoria.format in ('B','b'))
    if (not gravavel or not isinstance(offset,int) or offset < 0 or offset+104 > len(memoria)
            or ordem not in ('tabela','unidade')):
        raise ValueError('Bag reset requires 104 writable bytes, valid offset and original header order')
    cabecalhos = (0,0x66,4,2) if ordem == 'tabela' else (0x66,4,2,0)
    for campo in cabecalhos:
        struct.pack_into('<H',memoria,offset+campo,0)
    for slot in range(30):
        struct.pack_into('<H',memoria,offset+6+slot*2,0)
        memoria[offset+0x42+slot]=0
