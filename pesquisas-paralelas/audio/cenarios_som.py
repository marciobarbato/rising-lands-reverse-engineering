"""Shared fixture scenario constants and synthetic inputs (no Unicorn, no reconstruction).

Both the native captures and the Python replays build their inputs here, so
the same paths, arena, addresses and synthetic bytes are used on both sides.
"""
import hashlib
import struct
from ambiente_audio import LETRAS_BANCO, ler_original

DIRETORIO = b'C:\\RISING'
PREFIXO = DIRETORIO + b'\\SOUND\\'
ARENA, ARENA_TAMANHO = 0x4000000, 0x1000000
BANCOS = {'A': 0x521fc8, 'B': 0x521fe4, 'P': 0x522000}
NOME_LETRA = {'A': 0x495399, 'B': 0x49539b, 'P': 0x49539d}
NOME_ARQUIVO, NOME_ARQUIVO_BYTES = 0x5221c0, 104
DIRETORIO_SONS = 0x52201c
CONTADOR, COMPRIMIDO, ALOCACOES, DIRECTSOUND, JANELA = 0x5221bc, 0x52222c, 0x522230, 0x522228, 0x4e27e8
OBJETO_DIRECTSOUND = 0x3000900  # fixture IDirectSound object stored at 0x522228
HERDADO_HANDLE = 0xa5
ECX_INFO, ARGUMENTO_INFO, CONTADOR_INFO = 0x12345678, 0x55, 5
CONTADORES_VARIANTE = (0, 1, 2, 0x7ffffffe, 0xffffffff)
MAKE_ID = ((1, 0, 0), (0x11, 0x08, 0x00), (0xffff, 0xff, 0xff), (1, 0x1ff, 0x10000),
           (0x12345678, 0x9abcdef0, 0x0f0f0f0f), (0, 0, 0))
DIRETORIOS_TESTE = (b'C:\\RISING', b'C:\\', b'D:\\JOGOS\\RISING LANDS')
DECODIFICADOR_DIRETO = (('m16', 1, 512, 2048), ('m16', 2, 36, 1000), ('m16', 3, 512, 515),
                        ('m16', 4, 512, 3), ('m16', 5, 1024, 4096), ('m16', 6, 256, 777),
                        ('s16', 7, 512, 2048), ('s16', 8, 72, 720), ('s16', 9, 1024, 3072))


def sha(dados):
    return hashlib.sha256(bytes(dados)).hexdigest()


def entrada_sintetica(semente, tamanho):
    """Deterministic LCG bytes for synthetic fixture inputs (not game data)."""
    estado, saida = semente & 0xffffffff, bytearray()
    for _ in range(tamanho):
        estado = (estado * 1103515245 + 12345) & 0xffffffff
        saida.append(estado >> 16 & 255)
    return bytes(saida)


def arquivos_originais(letras=LETRAS_BANCO):
    return {PREFIXO + f'{l}.{e}'.encode(): ler_original(f'{l}.{e}') for l in letras for e in ('HED', 'SND')}


def hed_sintetico(entradas, cabecalhos, tamanho_dados, magia=b'ABCD', tamanho_declarado=None):
    corpo = b''.join(struct.pack('<IHHI', *e) for e in entradas) + b''.join(cabecalhos)
    declarado = len(corpo) if tamanho_declarado is None else tamanho_declarado
    return magia + struct.pack('<III', declarado, tamanho_dados, len(entradas)) + corpo


def banco_validacao():
    """Synthetic one-entry bank and its failure variants."""
    snd = entrada_sintetica(7, 4096)
    cab = struct.pack('<IIBBHBBH', 0, 2048, 1, 16, 22050, 4, 0, 512)
    hed_ok = hed_sintetico([(0x100, 0x100, 1, 12)], [cab], len(snd))
    variantes = {
        'bad_magic': (hed_sintetico([(0x100, 0x100, 1, 12)], [cab], 4096, magia=b'ABCE'), snd),
        'short_body': (hed_sintetico([(0x100, 0x100, 1, 12)], [cab], 4096, tamanho_declarado=200), snd),
        'missing_snd': (hed_ok, None),
        'missing_hed': (None, snd),
    }
    return hed_ok, snd, variantes


def arquivos_z(hed, snd):
    arquivos = {}
    if hed is not None:
        arquivos[PREFIXO + b'Z.HED'] = hed
    if snd is not None:
        arquivos[PREFIXO + b'Z.SND'] = snd
    return arquivos


def entrada_decodificador(tipo, semente, bloco, tamanho):
    origem = bytearray(entrada_sintetica(semente, tamanho))
    for b in range(0, tamanho, bloco):
        for c in range(1 if tipo == 'm16' else 2):
            if b + 4 * c + 3 <= tamanho:
                origem[b + 4 * c + 2] %= 89  # valid step index in each block header
    if semente == 6:
        origem[256 + 2] = 89  # invalid step index in the second block
    return bytes(origem)


def entradas_saturacao():
    sat = bytearray(entrada_sintetica(10, 512))
    sat[0:4] = struct.pack('<hBB', 32000, 88, 0)
    sat[4:] = b'\x77' * 508
    positivo = bytes(sat)
    sat[0:4] = struct.pack('<hBB', -32000, 88, 0)
    sat[4:] = b'\xff' * 508
    return (('m16', 10, 512, positivo), ('m16', 11, 512, bytes(sat)))


def banco_sintetico_superficies():
    """Stereo ADPCM, PCM, unsupported format 2 and a mono ADPCM header with byte13=200."""
    snd = bytearray(entrada_sintetica(20, 8192))
    for b in range(0, 4096, 512):
        snd[b + 2] %= 89
        snd[b + 6] %= 89
    cabecalhos = [struct.pack('<IIBBHBBH', 0, 4096, 2, 16, 22050, 4, 0, 512),
                  struct.pack('<IIBBHBBH', 4096, 3000, 1, 16, 11025, 0, 0, 0),
                  struct.pack('<IIBBHBBH', 4096, 1000, 1, 8, 22050, 2, 0, 0),
                  struct.pack('<IIBBHBBH', 1024, 2048, 1, 16, 44100, 4, 200, 256)]
    hed = hed_sintetico([(0x100 * i, 0x100, 1, 12 * 4 + 16 * i) for i in range(4)], cabecalhos, len(snd))
    return hed, bytes(snd)
