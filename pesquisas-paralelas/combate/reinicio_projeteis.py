"""ProjectileReset 0x46e00a for the MissionLoad reset prefix and its other callers.

The original rereads the pool pointer at dword 0x5080f0 before each store and
writes u8 zero at byte +2 of the 100 records of 56 bytes, in index order. It
takes no register input, reaches no call and writes no global; the other 55
bytes of every record stay inherited. It returns EAX=0x64 and restores EBX/EDX.
"""
ENTRADA = 0x46e00a
# Original CALL sites; each returns to the next instruction (call + 5).
CHAMADAS = {'MissionReStart': 0x46b5ac, 'GameLoad': 0x46b8c1,
            'MissionLoad': 0x46c373, 'MissionLoadName': 0x46c623}
REGISTROS, TAMANHO_REGISTRO = 100, 56
TAMANHO_POOL = REGISTROS * TAMANHO_REGISTRO
EAX_RETORNO = 0x64


def resetar_projeteis(pool):
    """Clear the active byte of every live projectile record; return EAX.

    `pool` is the live 5,600-byte allocation the original reaches through
    0x5080f0: a bytearray or a writable C-contiguous one-dimensional u8/s8
    memoryview. Shape is checked before the first store, so a rejected
    buffer keeps every byte; the original would fault on an unmapped pool.
    """
    gravavel = isinstance(pool, bytearray) or (
        isinstance(pool, memoryview) and not pool.readonly and pool.c_contiguous
        and pool.ndim == 1 and pool.itemsize == 1 and pool.format in ('B', 'b'))
    if not gravavel or len(pool) != TAMANHO_POOL:
        raise ValueError('ProjectileReset requires the writable 5600-byte projectile pool')
    for indice in range(REGISTROS):
        pool[indice * TAMANHO_REGISTRO + 2] = 0
    return EAX_RETORNO
