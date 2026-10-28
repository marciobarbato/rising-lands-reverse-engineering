"""Complete original EnginResetAll, retaining untouched inherited state."""
import struct

from bolsas_inicializacao import resetar_bolsa


def resetar_todas_unidades(mundo):
    """0x441659: four owner/type Bag pools, then nonzero-state unit records."""
    u, tabelas = mundo.unidades, mundo.bolsas_tipos_unidades
    if (not isinstance(u,bytearray) or len(u) != 220800
            or not isinstance(tabelas,(tuple,list)) or len(tabelas) != 4
            or any(not isinstance(t,bytearray) or len(t) != 2704 for t in tabelas)
            or len({id(t) for t in tabelas}) != 4):
        raise ValueError('EnginResetAll requires 800 units and four distinct 2704-byte Bag pools')
    for tabela in tabelas:
        for tipo in range(26):
            resetar_bolsa(tabela,tipo*104,ordem='tabela')
    for indice in range(800):
        p=indice*276
        if u[p+2] == 0:
            continue
        struct.pack_into('<H',u,p+0x9a,0)
        u[p+2]=0
        u[p+0xaf]=0
        resetar_bolsa(u,p+0xa,ordem='unidade')
