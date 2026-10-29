"""Core frame foundations of CalculGame 0x42c868: counters and random sources.

Translations over caller-owned live buffers, validated against the intact
executable (see docs/core/FRAME_FOUNDATIONS.md). Every buffer is the original
global itself (a writable bytearray or a one-dimensional contiguous byte
memoryview over DGROUP/thread data), never a copy or a constructed default.
All inputs are checked before the first store.

Register contract: each translated routine returns the EAX its callers consume;
every other general register is preserved by the original. The arithmetic flags
on return are not reproduced: no caller reads them before overwriting them.
"""
from cadencia import avancar_contadores
from candidatos_rota import aleatorio_caminhos

CONTADOR_QUADRO_JOGO = 0x496d40      # GameNextFrame u32
SEMENTE_MUNDO = 0x497164             # Random u32
SEMENTE_IA = 0x498db4                # iaRandom u32
CONTADORES_ITERACAO = 0x508f7c       # 3 x u32: cycle, half, third
TABELA_PERMUTACAO, CURSOR_PERMUTACAO = 0x4e1c18, 0x4e1d18
DESLOCAMENTO_SEMENTE_CRT = 0xc       # CRT rand seed inside the thread block at [0x522244]
CHAMADA_RELOGIO_IA = 0x489789        # iaRandom: CALL 0x493a24 -> jmp [0x5234a4] WINMM.timeGetTime
MODULO = 0x7fffffff


class DependenciaRelogioIA(NotImplementedError):
    """iaRandom(0) needs a declared timeGetTime value; nothing was written."""
    def __init__(self, endereco=CHAMADA_RELOGIO_IA):
        self.endereco = endereco
        super().__init__(f'iaRandom limit 0 reads WINMM.timeGetTime at 0x{endereco:x}; '
                         f'supply relogio, AI seed 0x{SEMENTE_IA:x} unchanged')


def _bytes_vivos(buffer, tamanho, nome, *, gravavel=True):
    if isinstance(buffer, memoryview):
        if (buffer.ndim != 1 or not buffer.c_contiguous or buffer.format not in ('B', 'b', 'c')
                or buffer.nbytes != tamanho or (gravavel and buffer.readonly)):
            raise ValueError(f'{nome} must be a writable contiguous {tamanho}-byte view')
        return buffer.cast('B') if buffer.format != 'B' else buffer
    tipos = (bytearray,) if gravavel else (bytes, bytearray)
    if type(buffer) not in tipos or len(buffer) != tamanho:
        raise ValueError(f'{nome} must be the live {tamanho}-byte {"bytearray" if gravavel else "buffer"}')
    return buffer


def _ler32(b, o=0):
    return b[o] | b[o+1] << 8 | b[o+2] << 16 | b[o+3] << 24


def _gravar32(b, valor, o=0):
    valor &= 0xffffffff
    b[o:o+4] = bytes((valor & 255, valor >> 8 & 255, valor >> 16 & 255, valor >> 24))


def avancar_quadro_jogo(contador):
    """GameNextFrame 0x45d015: INC u32 0x496d40 (wraps). No register output."""
    c = _bytes_vivos(contador, 4, 'GameNextFrame counter 0x496d40')
    _gravar32(c, _ler32(c) + 1)


def aleatorio_mundo(semente):
    """Random 0x4704dc: advance the world seed 0x497164 and return it as EAX."""
    s = _bytes_vivos(semente, 4, 'World seed 0x497164')
    novo = aleatorio_caminhos(_ler32(s))
    _gravar32(s, novo)
    return novo


def randomizar_mundo(semente, eax):
    """Randomize 0x470520: INC EAX; store it as the world seed; EAX out = EAX+1."""
    s = _bytes_vivos(semente, 4, 'World seed 0x497164')
    valor = (eax + 1) & 0xffffffff
    _gravar32(s, valor)
    return valor


def definir_semente_mundo(semente, eax):
    """SetRandomSeed 0x470527: zero stores 1 (EAX 0); otherwise unsigned EAX mod
    0x7fffffff is stored and the quotient is left in EAX."""
    s = _bytes_vivos(semente, 4, 'World seed 0x497164')
    eax &= 0xffffffff
    if eax == 0:
        _gravar32(s, 1)
        return 0
    quociente, resto = divmod(eax, MODULO)
    _gravar32(s, resto)
    return quociente


def obter_semente_mundo(semente):
    """GetRandomSeed 0x47054c: EAX = u32 0x497164 (no store)."""
    return _ler32(_bytes_vivos(semente, 4, 'World seed 0x497164', gravavel=False))


def aleatorio_ia(semente, limite, relogio=None):
    """iaRandom 0x489728 with the signed EAX limit; returns EAX.

    limite > 0: Park-Miller advance of 0x498db4 (same arithmetic as Random),
    then unsigned state mod limit. limite < 0: state = (-limite) signed remainder
    by 0x7fffffff, EAX 0. limite == 0: state = timeGetTime() unsigned mod
    0x7fffffff, EAX 0; `relogio()` must return that declared u32, otherwise
    DependenciaRelogioIA is raised before any store.
    """
    s = _bytes_vivos(semente, 4, 'AI seed 0x498db4')
    limite &= 0xffffffff
    if limite and not limite & 0x80000000:
        novo = aleatorio_caminhos(_ler32(s))
        _gravar32(s, novo)
        return novo % limite
    if limite:
        dividendo = -(limite - (1 << 32)) if limite != 0x80000000 else -(1 << 31)
        resto = abs(dividendo) % MODULO
        _gravar32(s, -resto if dividendo < 0 else resto)
        return 0
    if relogio is None:
        raise DependenciaRelogioIA()
    tempo = relogio()
    if type(tempo) is not int or not 0 <= tempo <= 0xffffffff:
        raise ValueError('Declared timeGetTime value must be an explicit u32 integer')
    _gravar32(s, tempo % MODULO)
    return 0


def aleatorio_crt(dados_thread):
    """LongRand 0x45841b -> CRT rand 0x48c51d over the live CRT thread block.

    The block is the one [0x522244] points to (0x3400000 in the frozen M1
    capture); its u32 seed at +0xc becomes seed*0x41c64e6d+0x3039 and EAX is
    (seed'>>16)&0x7fff. Only the seed's four bytes are written.
    """
    if isinstance(dados_thread, memoryview):
        if dados_thread.ndim != 1 or not dados_thread.c_contiguous or dados_thread.readonly:
            raise ValueError('CRT thread data must be a writable contiguous view')
        t = dados_thread.cast('B') if dados_thread.format != 'B' else dados_thread
    elif type(dados_thread) is bytearray:
        t = dados_thread
    else:
        raise ValueError('CRT thread data must be the live writable thread block')
    if len(t) < DESLOCAMENTO_SEMENTE_CRT + 4:
        raise ValueError('CRT thread data must contain the seed at +0xc')
    novo = (_ler32(t, DESLOCAMENTO_SEMENTE_CRT) * 0x41c64e6d + 0x3039) & 0xffffffff
    _gravar32(t, novo, DESLOCAMENTO_SEMENTE_CRT)
    return novo >> 16 & 0x7fff


def consumir_permutacao(tabela, cursor):
    """Shared draw: byte = 0x4e1c18[u8 0x4e1d18]; then the cursor is stored +1 (u8).

    Used inline by NextAnimTerrain/NextAnimVeget(FullMap), by CalculGame's CD
    branch and by rendering (AffBatiments, AffCorpsEngin, AffDeplaceEngin,
    AffVeget, DDFlipPage). Returns the byte; the caller applies its own modulus.
    """
    t = _bytes_vivos(tabela, 256, 'Permutation table 0x4e1c18', gravavel=False)
    c = _bytes_vivos(cursor, 1, 'Permutation cursor 0x4e1d18')
    valor = t[c[0]]
    c[0] = (c[0] + 1) & 255
    return valor


def avancar_contadores_iteracao(contadores):
    """ProgIteration counter prefix 0x475014..0x475041 over 12 live bytes at 0x508f7c.

    Ordered stores: cycle+1 always; half+1 if the new cycle is even; third+1 if
    it is divisible by 3. Returns the offsets stored, in order.
    """
    c = _bytes_vivos(contadores, 12, 'Iteration counters 0x508f7c..0x508f88')
    ciclo, metade, terco = avancar_contadores(_ler32(c), _ler32(c, 4), _ler32(c, 8))
    gravados = [0]
    _gravar32(c, ciclo)
    if ciclo % 2 == 0:
        _gravar32(c, metade, 4)
        gravados.append(4)
    if ciclo % 3 == 0:
        _gravar32(c, terco, 8)
        gravados.append(8)
    return tuple(gravados)


def zerar_contadores_carga(contadores):
    """CalculGame load case 0x42d2be..0x42d2ca: u32 zeros at +0, +4, +8 in order."""
    c = _bytes_vivos(contadores, 12, 'Iteration counters 0x508f7c..0x508f88')
    for o in (0, 4, 8):
        _gravar32(c, 0, o)
    return (0, 4, 8)
