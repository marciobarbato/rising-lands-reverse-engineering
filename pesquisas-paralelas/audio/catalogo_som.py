"""Sample catalogue keyed by original bank letter, sound ID and variant.

Built with the validated Python reconstruction over the read-only banks. It
records identities and hashes only: no label is invented and no decoded audio
is written. ``decoded_sha256`` covers the bytes the original decoder writes;
``buffer_sha256`` covers the whole DirectSound buffer with the fixture's 0xcd
fill in the unwritten tail, which is what the native captures compare.
"""
import json
import struct
from ambiente_audio import IDENTIDADES, LETRAS_BANCO, ORIGINAL_SHA256, OWNED, ler_original
from cenarios_som import sha
from reproduzir_som import reproduzir_banco

SELETOR = {'A': 0x41, 'B': 0x42, 'P': 0x50}
DESTINO = OWNED / 'catalogo-amostras.json'


def variantes_alcancaveis(quantidade):
    """Variant indices UseBank_GetDataHeader can return: subsets of the bits of n-1."""
    if quantidade - 1 <= 0:
        return [0]
    return sorted({(quantidade - 1) & contador for contador in range(1 << (quantidade - 1).bit_length())})


def catalogar(letra):
    conteudos = {}
    caso = reproduzir_banco(letra, conteudos=conteudos)
    snd = ler_original(f'{letra}.SND')
    hed = ler_original(f'{letra}.HED')
    entradas = {}
    for i in range(struct.unpack_from('<I', hed, 12)[0]):
        ident, palavra, variantes, _ = struct.unpack_from('<IHHI', hed, 16 + 12 * i)
        entradas[i] = (ident, palavra, variantes)
    registros = []
    for som in caso['surfaces_from_file']:
        ident, palavra, variantes = entradas[som['index']]
        deslocamento, tamanho, canais, bits, frequencia, formato, byte_0d, bloco = struct.unpack(
            '<IIBBHBBH', bytes.fromhex(som['data_header_hex']))
        decodificado = som['decoder_returns'][0] if som['decoder_returns'] else tamanho
        conteudo = conteudos[(som['index'], som['variant'])]
        registros.append(dict(
            bank=letra, post_sound_selector=hex(SELETOR[letra]), index=som['index'], id=f'0x{ident:08x}',
            id_bytes=[ident >> 16, ident >> 8 & 255, ident & 255], entry_word_4=palavra, variants=variantes,
            variant=som['variant'], reachable_by_get_data_header=som['variant'] in variantes_alcancaveis(variantes),
            data_header_hex=som['data_header_hex'], snd_offset=deslocamento, snd_bytes=tamanho,
            snd_sha256=sha(snd[deslocamento:deslocamento + tamanho]), format=formato, channels=canais,
            bits=bits, sample_rate=frequencia, byte_0d=byte_0d, block_align=bloco,
            buffer_bytes=som['buffer_bytes'], decoded_bytes=decodificado,
            decoded_sha256=sha(conteudo[:decodificado]), buffer_sha256=som['buffer_sha256'],
            decoded_seconds=round(decodificado / (2 * max(canais, 1)) / frequencia, 4)))
    return registros


def construir():
    sons = [registro for letra in LETRAS_BANCO for registro in catalogar(letra)]
    return dict(
        original_sha256=ORIGINAL_SHA256,
        banks={nome: dict(bytes=tamanho, sha256=sha256) for nome, (tamanho, sha256) in IDENTIDADES.items()},
        meaning='Keys are original identities only (bank letter, PlaySnd_PostSound selector, 32-bit sound ID, '
                'variant). Names, speakers, events and PT-BR wording are not inferred. decoded_seconds is derived '
                'from decoded_bytes and the header sample rate.',
        reachability='UseBank_GetDataHeader selects (n-1) & counter; variants outside that set are present in the '
                     'bank but never selected by the original request path.',
        sounds=sons)


def gerar():
    resultado = construir()
    DESTINO.write_text(json.dumps(resultado, indent=1, ensure_ascii=False) + '\n')
    return resultado


if __name__ == '__main__':
    resultado = gerar()
    print('Catalogued sounds:', len(resultado['sounds']))
