"""Original GetNumBob cache lifecycle: allocation, initialization, fill and release.

ProgInit runs LoadSTRATBank, SetBank, then CacheAlloc 0x40FA18. InitCache
0x40FA38 runs at game start (CalculGame, before MissionLoad/MissionLoadName)
and before GameLoad (MenuNewSelect). GetNumBob misses fill/replace slots
through cache_terreno. ProgExit calls CacheFree 0x40FA2E. Windows memory
imports are explicit bindings; the only startup values are the image's own
.bss zeros and DGROUP capacity word.
"""
from cache_terreno import CacheTerreno, SLOTS, RAW_BLOCK, FIRST_CACHED_ID

CAPACIDADE_U16 = 256  # DGROUP word 0x495BC4; the image never writes it


class DependenciaCicloCache(NotImplementedError):
    def __init__(self, endereco, detalhe):
        self.endereco, self.detalhe = endereco, detalhe
        super().__init__(f'Terrain cache lifecycle dependency at 0x{endereco:08x}: {detalhe}')


def _u32(valor, nome):
    if type(valor) is not int or not 0 <= valor <= 0xFFFFFFFF:
        raise ValueError(nome+' must be u32')


class MemoriaMotor:
    """MemAlloc 0x467EA6 / MemFree 0x467ECB over explicit KERNEL32 bindings.

    contador_u32 is the byte counter 0x4E2F3C, inherited (MemInit zeroes it at
    the start of ProgInit). MemAlloc adds the request before GlobalAlloc and
    MemFree never subtracts. vinculos supplies global_alloc(flags, bytes),
    global_lock(handle), global_handle(pointer), global_unlock(handle) and
    global_free(handle), each returning u32. A missing binding raises at its
    original call site, retaining earlier counter/binding effects.
    """
    def __init__(self, *, contador_u32, vinculos):
        _u32(contador_u32, 'contador_u32')
        self.contador_u32, self.vinculos = contador_u32, vinculos

    def _chamar(self, nome, endereco, *argumentos):
        funcao = getattr(self.vinculos, nome, None)
        if not callable(funcao):
            raise DependenciaCicloCache(endereco, f'KERNEL32 binding {nome}{argumentos} is not supplied')
        valor = funcao(*argumentos); _u32(valor, nome+' result')
        return valor

    def mem_alloc(self, tamanho_u32):
        _u32(tamanho_u32, 'tamanho_u32')
        self.contador_u32 = (self.contador_u32+tamanho_u32) & 0xFFFFFFFF
        handle = self._chamar('global_alloc', 0x467EB9, 0, tamanho_u32)  # GMEM_FIXED
        return self._chamar('global_lock', 0x467EC1, handle)

    def mem_free(self, ponteiro_u32):
        _u32(ponteiro_u32, 'ponteiro_u32')
        handle = self._chamar('global_handle', 0x467ED1, ponteiro_u32)
        self._chamar('global_unlock', 0x467ED9, handle)  # result ignored
        handle = self._chamar('global_handle', 0x467EE1, ponteiro_u32)
        return self._chamar('global_free', 0x467EE9, handle)  # EAX at return


def blocos_banco_cache(catalogo):
    """Raw payloads of IDs 1090..1345 exactly as LoadSTRATBank reads BLOCS.CMP."""
    partes = []
    for id_motor in range(FIRST_CACHED_ID, FIRST_CACHED_ID+SLOTS):
        quadro = catalogo.quadro(id_motor)
        if (quadro.largura, quadro.altura, len(quadro.comprimido)) != (32, 32, RAW_BLOCK):
            raise NotImplementedError('Cached bank frame outside the verified 32x32/1056 domain')
        partes.append(bytes(quadro.comprimido))
    return b''.join(partes)


class CicloCacheTerreno:
    """Key pointer 0x49A050, 256 keys, cursor 0x49A04E and bank payloads 1090..1345.

    Construct after LoadSTRATBank/SetBank and before CacheAlloc. Payloads are
    bank-owned bytes that GetNumBob overwrites in place; nothing in the
    lifecycle restores them. The key pointer starts as the .bss zero.
    """
    def __init__(self, blocos_crus, *, proximo_u16):
        if len(blocos_crus) != SLOTS*RAW_BLOCK:
            raise ValueError('Expected 256 raw 1056-byte bank payloads')
        if type(proximo_u16) is not int or not 0 <= proximo_u16 < SLOTS:
            raise ValueError('Expected inherited cursor 0..255')
        self.ponteiro_chaves_u32, self.estado = 0, 'sem_tabela'
        self._blocos, self._proximo, self._cache = bytearray(blocos_crus), proximo_u16, None

    @classmethod
    def apos_carregar_banco(cls, catalogo):
        """First ProgInit: real BLOCS.CMP payloads and the .bss cursor zero."""
        return cls(blocos_banco_cache(catalogo), proximo_u16=0)

    @property
    def proximo_u16(self):
        return self._cache.proximo_u16 if self._cache is not None else self._proximo

    @property
    def blocos_crus(self):
        return bytes(self._cache.blocos_crus if self._cache is not None else self._blocos)

    @property
    def registros(self):
        """Key bytes after InitCache; None while undefined (GMEM_FIXED) or freed."""
        return bytes(self._cache.registros) if self.estado == 'iniciada' else None

    @property
    def cache(self):
        """Live CacheTerreno for GetNumBob, only between InitCache and CacheFree."""
        if self.estado != 'iniciada':
            raise DependenciaCicloCache(0x40FE50, f'GetNumBob key table read in lifecycle state {self.estado}')
        return self._cache

    def alocar(self, memoria):
        """CacheAlloc: MemAlloc(capacity<<2), then store the pointer at 0x49A050."""
        if not isinstance(memoria, MemoriaMotor):
            raise ValueError('Expected explicit MemoriaMotor')
        if self.estado != 'sem_tabela':
            raise DependenciaCicloCache(0x40FA18, f'CacheAlloc in state {self.estado}; ProgInit allocates once')
        self.ponteiro_chaves_u32 = memoria.mem_alloc(CAPACIDADE_U16 << 2)
        self.estado = 'alocada'
        return self.ponteiro_chaves_u32

    def iniciar(self):
        """InitCache: zero every key; cursor and payloads stay as inherited."""
        if self.estado not in ('alocada', 'iniciada') or self.ponteiro_chaves_u32 == 0:
            raise DependenciaCicloCache(0x40FA49, f'InitCache writes through key pointer 0x{self.ponteiro_chaves_u32:08x} '
                f'in state {self.estado}; the original faults or writes undefined memory')
        if self._cache is None:
            self._cache = CacheTerreno(bytes(SLOTS*4), self._blocos, proximo_u16=self._proximo)
            self._blocos = None
        else:
            # Per entry the original writes word +0, byte +2, byte +3; only
            # the final zero table is observable without faults.
            self._cache.registros[:] = bytes(SLOTS*4)
        self.estado = 'iniciada'
        return CAPACIDADE_U16  # EAX at the original return; callers ignore it

    def liberar(self, memoria):
        """CacheFree: MemFree(pointer); 0x49A050 keeps the stale pointer."""
        if not isinstance(memoria, MemoriaMotor):
            raise ValueError('Expected explicit MemoriaMotor')
        if self.estado not in ('alocada', 'iniciada'):
            raise DependenciaCicloCache(0x40FA2E, f'CacheFree in state {self.estado}')
        resultado = memoria.mem_free(self.ponteiro_chaves_u32)
        self.estado = 'liberada'
        return resultado
