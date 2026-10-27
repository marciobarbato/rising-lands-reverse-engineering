"""Extrai dimensões/máscaras iniciais dos 22 tipos; não executa o binário."""
import hashlib
import json
import struct
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
BASES_MASCARAS = (0x495c04,0x495c10,0x495c30,0x495c50,0x495cec,0x495c80,
                 0x495d6c,0x495d30,0x495cf8,0x495d8a,0x495d64,0x495d5c,
                 0x495d8b,0x495c6c,0x495ca4,0x495d1c,0x495cd4,0x495ce8,
                 0x495d48,0x495cbc,0x495d1c,0x495cc8)


def extrair():
    dados = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('EXE diferente do original identificado')
    pe = struct.unpack_from('<I',dados,60)[0]
    n = struct.unpack_from('<H',dados,pe+6)[0]
    opcional = struct.unpack_from('<H',dados,pe+20)[0]
    secoes = [struct.unpack_from('<III',dados,pe+24+opcional+i*40+12) for i in range(n)]
    def ler(endereco, tamanho):
        rva = endereco - 0x400000
        for base, comprimento, offset in secoes:
            if offset and base <= rva and rva+tamanho <= base+comprimento:
                return dados[offset+rva-base:offset+rva-base+tamanho]
        raise ValueError('Endereço sem dados na imagem PE')
    tipos = []
    for tipo, base in enumerate(BASES_MASCARAS):
        largura, altura = struct.unpack('<HH',ler(0x495d8c+tipo*52,4))
        mascara = list(ler(base,largura*altura))
        tipos.append(dict(tipo=tipo, largura=largura, altura=altura,
                          endereco_mascara=f'0x{base:08x}', mascara=mascara))
    return dict(sha256_original=HASH, tabela_dimensoes='0x00495d8c', passo=52, tipos=tipos)


if __name__ == '__main__':
    destino = RAIZ / 'relatorios/pegadas-estruturas.json'
    destino.write_text(json.dumps(extrair(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(destino)
