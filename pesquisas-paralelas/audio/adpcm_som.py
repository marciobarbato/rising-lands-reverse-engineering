"""Original sample-buffer creation and IMA ADPCM decoding.

Reconstructs ``PSB_CreateMySurfaceWithSound 0x48aad4``, ``DSB_CreateEmptySoundBuffer
0x48b7b1``, the ``LoadSoundBuffer_*`` family 0x48c070..0x48c202 and
``imaadpcmDecode4Bit_M16 0x48b8c9``/``_S16 0x48ba96``. DirectSound is an
explicit provider (``criar``/``travar``/``destravar`` on numbered buffers);
the decoded bytes are written into the provider's buffer as the original
writes through the locked pointer.

The decode tables are the original words at 0x498f6c (16 index steps) and
0x498f8c (89 step sizes); tests compare them with the exported image bytes.
"""
import struct
from bancos_som import DependenciaSom, TEXTOS, alocar

INDICE_IMA = (-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8)
PASSO_IMA = (
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73,
    80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494,
    544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499,
    2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487,
    12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767)
COMPRIMIDO_BYTES = 0x27100  # LoadSoundBuffer_InitCompressedBuffer allocation
FLAGS_BUFFER = 0xe0


def _delta(passo, nibble):
    diferenca = passo >> 3
    if nibble & 4:
        diferenca += passo
    if nibble & 2:
        diferenca += passo >> 1
    if nibble & 1:
        diferenca += passo >> 2
    return -diferenca if nibble & 8 else diferenca


# Per (step index, nibble): signed difference and next step index.
DELTAS = tuple(tuple(_delta(PASSO_IMA[i], n) for n in range(16)) for i in range(89))
PROXIMOS = tuple(tuple(min(88, max(0, i + INDICE_IMA[n])) for n in range(16)) for i in range(89))


def _cabecalho_bloco(origem, posicao):
    preditor, indice = struct.unpack_from('<hB', origem, posicao)
    return preditor, indice


def _empacotar(amostras):
    return struct.pack(f'<{len(amostras)}h', *amostras)


def decodificar_ima_mono16(origem, bloco):
    """imaadpcmDecode4Bit_M16: returns ``(bytes written, EAX)``.

    Blocks of ``min(remaining, bloco)`` bytes while at least 4 remain: the
    header sample (i16 predictor, u8 step index, ignored byte), then low and
    high nibble of each following byte. A step index above 88 stops with
    EAX 0 and keeps earlier output. ``bloco`` below 4 is unsupported.
    """
    origem, bloco = bytes(origem), bloco & 0xffffffff
    resto, posicao, saida = len(origem), 0, []
    if resto >= 4 and bloco < 4:
        raise DependenciaSom(0x48b8fe, 'block alignment below 4 wraps the per-block byte count')
    while resto >= 4:
        quantidade = min(resto, bloco)
        resto -= quantidade
        preditor, indice = _cabecalho_bloco(origem, posicao)
        posicao += 4
        if indice > 88:
            return _empacotar(saida), 0
        saida.append(preditor)
        for byte in origem[posicao:posicao + quantidade - 4]:
            for nibble in (byte & 15, byte >> 4):
                preditor = max(-32768, min(32767, preditor + DELTAS[indice][nibble]))
                indice = PROXIMOS[indice][nibble]
                saida.append(preditor)
        posicao += quantidade - 4
    dados = _empacotar(saida)
    return dados, len(dados)


def decodificar_ima_estereo16(origem, bloco):
    """imaadpcmDecode4Bit_S16: returns ``(bytes written, EAX)``.

    Each block holds left then right 4-byte headers, then 8-byte groups of
    one left and one right dword, decoded nibble-interleaved as L,R pairs.
    The original subtracts whole blocks and 8-byte groups without bounds,
    so the supported domain is ``len % bloco == 0`` and ``(bloco-8) % 8 == 0``.
    """
    origem, bloco = bytes(origem), bloco & 0xffffffff
    if origem and (bloco < 8 or len(origem) % bloco or (bloco - 8) % 8):
        raise DependenciaSom(0x48babd, 'stereo size/alignment outside the whole-block domain')
    posicao, saida = 0, []
    for _ in range(len(origem) // bloco if origem else 0):
        esquerdo, indice_e = _cabecalho_bloco(origem, posicao)
        if indice_e > 88:
            return _empacotar(saida), 0
        direito, indice_d = _cabecalho_bloco(origem, posicao + 4)
        if indice_d > 88:
            return _empacotar(saida), 0
        posicao += 8
        saida += (esquerdo, direito)
        for _ in range((bloco - 8) // 8):
            palavra_e, palavra_d = struct.unpack_from('<II', origem, posicao)
            posicao += 8
            for deslocamento in range(0, 32, 4):
                nibble = palavra_e >> deslocamento & 15
                esquerdo = max(-32768, min(32767, esquerdo + DELTAS[indice_e][nibble]))
                indice_e = PROXIMOS[indice_e][nibble]
                nibble = palavra_d >> deslocamento & 15
                direito = max(-32768, min(32767, direito + DELTAS[indice_d][nibble]))
                indice_d = PROXIMOS[indice_d][nibble]
                saida += (esquerdo, direito)
    dados = _empacotar(saida)
    return dados, len(dados)


def iniciar_buffer_comprimido(sistema, globais):
    """LoadSoundBuffer_InitCompressedBuffer 0x48c16c: returns 1 when allocated."""
    globais.comprimido = alocar(sistema, globais, COMPRIMIDO_BYTES, TEXTOS['comprimido_alocar'])
    return int(globais.comprimido != 0)


def criar_buffer_vazio(directsound, globais, canais, frequencia, bits, tamanho):
    """DSB_CreateEmptySoundBuffer 0x48b7b1: PCM format, flags 0xe0; 0 without DirectSound."""
    if globais.directsound == 0:
        return 0
    alinhamento = ((canais * bits) >> 3) & 0xffff
    formato = struct.pack('<HHIIHH', 1, canais & 0xffff, frequencia & 0xffffffff,
                          (frequencia * alinhamento) & 0xffffffff, alinhamento, bits & 0xffff)
    descricao = struct.pack('<IIIII', 20, FLAGS_BUFFER, tamanho & 0xffffffff, 0, 0)
    return directsound.criar(descricao, formato)


def _escrever(directsound, objeto, dados):
    directsound.buffers[objeto][:len(dados)] = dados


def _travado(directsound, objeto, quantidade, escrita):
    inicio = directsound.travar(objeto, 0, quantidade, 0)
    resultado = escrita(inicio)
    directsound.destravar(objeto, inicio, quantidade, 0, 0)
    return resultado


def criar_superficie_som(sistema, globais, banco, cabecalho_dados):
    """PSB_CreateMySurfaceWithSound 0x48aad4 for one 16-byte data header.

    Returns ``(buffer object or 0, decoder EAX values)``. File-backed banks
    first seek the data file to 0. Format 0 copies raw bytes; format 4 locks
    only the compressed size yet decodes about four times as many bytes
    through the same pointer; other formats create nothing.
    """
    directsound = sistema.directsound
    deslocamento, tamanho, canais, bits, frequencia, formato, _, bloco = struct.unpack(
        '<IIBBHBBH', bytes(cabecalho_dados))
    if banco.em_memoria == 0:
        sistema.arquivos.posicionar(banco.arquivo, 0, 0)
    if formato not in (0, 4):
        return 0, []
    objeto = criar_buffer_vazio(directsound, globais, canais, frequencia, bits,
                                tamanho if formato == 0 else tamanho << 2)
    if objeto == 0:
        return 0, []
    if formato == 0:
        if banco.em_memoria == 1:
            fonte = _memoria(banco, deslocamento, tamanho)
            _travado(directsound, objeto, tamanho, lambda inicio: _escrever(directsound, objeto, fonte))
        else:
            sistema.arquivos.posicionar(banco.arquivo, deslocamento, 0)
            _travado(directsound, objeto, tamanho, lambda inicio: _escrever(
                directsound, objeto, sistema.arquivos.ler(banco.arquivo, tamanho)))
        return objeto, []
    if banco.em_memoria == 1:
        fonte = _memoria(banco, deslocamento, tamanho)
    else:
        sistema.arquivos.posicionar(banco.arquivo, deslocamento, 0)
        fonte = carregar_dados_comprimidos(sistema, globais, banco.arquivo, tamanho)
    decodificar = decodificar_ima_mono16 if canais == 1 else decodificar_ima_estereo16

    def decodificar_travado(inicio):
        dados, eax = decodificar(fonte, bloco)
        _escrever(directsound, objeto, dados)
        return eax
    return objeto, [_travado(directsound, objeto, tamanho, decodificar_travado)]


def _memoria(banco, deslocamento, tamanho):
    if banco.ponteiro_dados == 0 or banco.dados is None:
        raise DependenciaSom(0x48ab80, 'in-memory bank with a NULL data pointer')
    if deslocamento + tamanho > len(banco.dados):
        raise DependenciaSom(0x48ab83, 'data header outside the resident bank data')
    return banco.dados[deslocamento:deslocamento + tamanho]


def carregar_dados_comprimidos(sistema, globais, handle, tamanho):
    """LoadSoundBuffer_LoadCompactedData 0x48c141 into the 160,000-byte buffer.

    Without the buffer, or after a short read, the original returns NULL and
    the decoder then reads address 0; both are reported as dependencies.
    """
    if globais.comprimido == 0:
        raise DependenciaSom(0x48c14f, 'compressed buffer not initialized; decoder would read NULL')
    if tamanho > COMPRIMIDO_BYTES:
        raise DependenciaSom(0x48c156, 'sample larger than the compressed buffer overflows the heap')
    dados = sistema.arquivos.ler(handle, tamanho)
    if len(dados) != tamanho:
        raise DependenciaSom(0x48c15f, 'short compressed read; decoder would read NULL')
    return dados
