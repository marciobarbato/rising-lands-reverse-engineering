"""Consume the committed ETA and type-table readers without rebuilding them."""
import hashlib
from ambiente_missoes import CD
from analisar import dependencias, HASH_ESTUDADO
from formatos import ler_eta
from regras import extrair_regras


def tipos_originais():
    pefile, _ = dependencias()
    original = (CD / 'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(original).hexdigest() != HASH_ESTUDADO:
        raise ValueError('Executável original incompatível')
    pe = pefile.PE(data=original)
    rules = extrair_regras(pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase,
                         (CD / 'INSTALHD/RISING.INI').read_bytes())
    return b''.join(bytes.fromhex(row['registro_memoria_hex']) for row in rules['unidades'])


def bloco_unidades(dados):
    """Return the existing reader's boundaries; no runtime readiness is implied."""
    parsed = ler_eta(dados)
    return next(block for block in parsed['blocos'] if block['nome'] == 'unidades')
