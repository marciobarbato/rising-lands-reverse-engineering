"""Normaliza apenas VirtualSize em uma cópia PE para o importador do Ghidra.

O PE Watcom estudado informa VirtualSize=0 nas seis seções. O importador
Ghidra 12.2 registra Invalid file index ao resolver diretórios com esse layout.
Mantemos endereços, código, dados e original intactos; só a cópia é alterada.
"""
from pathlib import Path
import hashlib
import json
import struct

RAIZ = Path(__file__).resolve().parents[1]
HASH_ORIGINAL = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'


def preparar():
    original = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(original).hexdigest() != HASH_ORIGINAL:
        raise ValueError('Executável diferente do estudado')
    dados = bytearray(original)
    pe = struct.unpack_from('<I', dados, 0x3c)[0]
    numero = struct.unpack_from('<H', dados, pe + 6)[0]
    tamanho_opcional = struct.unpack_from('<H', dados, pe + 20)[0]
    tabela = pe + 24 + tamanho_opcional
    alteracoes = []
    permitidos = set()
    for indice in range(numero):
        offset = tabela + indice * 40
        nome = dados[offset:offset + 8].rstrip(b'\0').decode('ascii')
        virtual = struct.unpack_from('<I', dados, offset + 8)[0]
        tamanho_arquivo = struct.unpack_from('<I', dados, offset + 16)[0]
        if virtual != 0:
            raise ValueError('Seção já possui tamanho virtual: ' + nome)
        struct.pack_into('<I', dados, offset + 8, tamanho_arquivo)
        permitidos.update(range(offset + 8, offset + 12))
        alteracoes.append(dict(secao=nome, offset=offset + 8,
                               campo='VirtualSize', anterior=0, novo=tamanho_arquivo))
    diferencas = {i for i, (a, b) in enumerate(zip(original, dados)) if a != b}
    if not diferencas <= permitidos or len(dados) != len(original):
        raise AssertionError('Alteração fora dos campos autorizados')
    pasta = RAIZ / '.local/entrada'
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / 'RISING-analise.exe').write_bytes(dados)
    manifesto = dict(sha256_original=HASH_ORIGINAL,
                     sha256_copia=hashlib.sha256(dados).hexdigest(),
                     alteracoes=alteracoes, bytes_diferentes=len(diferencas),
                     finalidade='Somente importação estática; não executar a cópia normalizada.')
    (RAIZ / 'ghidra/entrada.json').write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print(json.dumps(preparar(), ensure_ascii=False, indent=2))
