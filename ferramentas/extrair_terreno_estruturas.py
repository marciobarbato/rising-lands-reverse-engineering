"""Extrai bytes/ASM das três rotinas de terreno e seus epílogos compartilhados.

Somente leitura do EXE identificado; Capstone é usado apenas nesta extração.
"""
import hashlib
import json
import struct
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
INTERVALOS = (
    ('ResetCheminTerrainModify', 0x41b78f, 0x41b888),
    ('ResetBatimentTerrainModify', 0x41b888, 0x41b9d6),
    ('BatimentModifyTerrain', 0x41ba49, 0x41bb8a),
    ('epilogo_ResetCheminTerrainModify', 0x41db1d, 0x41db24),
    ('epilogo_BatimentModifyTerrain', 0x41fd56, 0x41fd5e),
    ('epilogo_ResetBatimentTerrainModify', 0x42399a, 0x4239a0),
    ('atributos_e_tile', 0x47622e, 0x476263),
)


def extrair():
    import capstone
    dados = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Executável diferente do original identificado')
    pe = struct.unpack_from('<I', dados, 0x3c)[0]
    n, opcional = (struct.unpack_from('<H', dados, pe + off)[0] for off in (6, 20))
    secoes = [struct.unpack_from('<III', dados, pe + 24 + opcional + i * 40 + 12) for i in range(n)]
    def ler(endereco, tamanho):
        rva = endereco - 0x400000
        for base, comprimento, offset in secoes:
            if offset and base <= rva and rva + tamanho <= base + comprimento:
                return dados[offset + rva - base:offset + rva - base + tamanho]
        raise ValueError('Endereço fora das seções com dados do PE')
    pasta = RAIZ / 'evidencias/terreno-estruturas'
    pasta.mkdir(parents=True, exist_ok=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in INTERVALOS:
        bruto = ler(inicio, fim - inicio)
        instrucoes = list(md.disasm(bruto, inicio))
        if sum(i.size for i in instrucoes) != len(bruto):
            raise ValueError('Trecho não desmontado integralmente')
        nome_arquivo = f'{inicio:08x}.asm'
        linhas = [f'; {nome}; SHA-256 do EXE original: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in instrucoes]
        (pasta / nome_arquivo).write_text('\n'.join(linhas) + '\n', encoding='utf-8')
        trechos.append(dict(nome=nome, inicio=f'0x{inicio:08x}', fim_exclusivo=f'0x{fim:08x}',
                            tamanho=len(bruto), sha256=hashlib.sha256(bruto).hexdigest(), arquivo=nome_arquivo))
    tabelas = []
    for tipo in range(22):
        endereco = 0x495d8c + tipo * 52
        largura, altura = struct.unpack('<HH', ler(endereco, 4))
        ponteiro = struct.unpack('<I', ler(endereco + 8, 4))[0]
        mascara = None if tipo == 20 and ponteiro == 0x4dfb9c else list(ler(ponteiro, largura * altura))
        tabelas.append(dict(tipo=tipo, largura=largura, altura=altura, endereco=f'0x{endereco:08x}',
                            ponteiro_mascara=f'0x{ponteiro:08x}', mascara=mascara,
                            origem_mascara='RAM mutável; sem dados de arquivo' if mascara is None else 'dados do EXE'))
    manifesto = dict(sha256_original=HASH, capstone=capstone.__version__, trechos=trechos, tabelas=tabelas,
                     limite='Rotinas locais com dados iniciais dos tipos; não representa criação/demolição completa.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifesto


if __name__ == '__main__':
    print('Trechos extraídos:', len(extrair()['trechos']))
