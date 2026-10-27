"""Extrai bytes/assembly somente da cópia conferida do executável brasileiro."""
from pathlib import Path
import hashlib
import json
import struct
import sys

RAIZ = Path(__file__).resolve().parent
COMMIT = '1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e'
HASH_EXE = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'


def exigir_area_editavel():
    if RAIZ.parent.name == 'entregas':
        raise RuntimeError('Entrega congelada: copie para uma nova pasta de trabalho dentro de graficos-animacao antes de gerar arquivos.')


def imagem_pe(caminho=None):
    dados = Path(caminho or RAIZ / 'fontes/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH_EXE:
        raise ValueError('SHA-256 do executável incompatível')
    pe = struct.unpack_from('<I', dados, 0x3c)[0]
    n = struct.unpack_from('<H', dados, pe + 6)[0]
    opcional = struct.unpack_from('<H', dados, pe + 20)[0]
    base = struct.unpack_from('<I', dados, pe + 52)[0]
    imagem = bytearray(struct.unpack_from('<I', dados, pe + 80)[0])
    for i in range(n):
        cab = pe + 24 + opcional + i * 40
        rva, tamanho, offset = struct.unpack_from('<III', dados, cab + 12)
        if tamanho and offset:
            imagem[rva:rva+tamanho] = dados[offset:offset+tamanho]
    return base, bytes(imagem)


def simbolos():
    resultado = {}
    for linha in (RAIZ / 'snapshot' / COMMIT / 'relatorios/simbolos-originais.tsv').read_text().splitlines():
        endereco, nome = linha.split('\t')
        try:
            resultado[int(endereco, 16)] = nome
        except ValueError:
            pass
    return resultado


def extrair():
    exigir_area_editavel()
    sys.path.insert(0, str(RAIZ / 'dependencias'))
    import capstone
    base, imagem = imagem_pe()
    nomes = simbolos()
    ordenados = sorted(nomes)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    cs.detail = True
    pasta = RAIZ / 'evidencias'
    pasta.mkdir(exist_ok=True)
    selecionados = [a for a in ordenados if
                   0x410fcc <= a < 0x415acf or 0x4478ee <= a < 0x448194 or
                   a in (0x41877a, 0x418590, 0x457350, 0x45b247, 0x45b796, 0x45c455,
                         0x477042, 0x4770ee, 0x448599, 0x448194, 0x448f50, 0x416864,
                         0x467d97, 0x442025, 0x442045, 0x44fffe, 0x45002e, 0x474beb)]
    registros = []
    for a in selecionados:
        fim = {0x448088:0x44812b}.get(a, ordenados[ordenados.index(a)+1])
        bruto = imagem[a-base:fim-base]
        linhas = [f'; {nomes[a]} [{a:#x}, {fim:#x})', f'; SHA-256 EXE: {HASH_EXE}',
                  '; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.']
        for ins in cs.disasm(bruto, a):
            extra = ''
            if ins.mnemonic in ('call', 'jmp') and ins.operands[0].type == capstone.x86.X86_OP_IMM:
                extra = ' ; ' + nomes.get(ins.operands[0].imm, '')
            linhas.append(f'{ins.address:08x}  {ins.bytes.hex():22} {ins.mnemonic:8} {ins.op_str}{extra}')
        arquivo = pasta / f'{a:08x}.asm'
        arquivo.write_text('\n'.join(linhas)+'\n')
        registros.append(dict(nome=nomes[a],inicio=hex(a),fim=hex(fim),sha256_bytes=hashlib.sha256(bruto).hexdigest(),arquivo=arquivo.name))
    (pasta / 'manifesto.json').write_text(json.dumps(dict(commit=COMMIT,exe_sha256=HASH_EXE,capstone=capstone.__version__,trechos=registros),indent=2)+'\n')
    tabelas=[]
    for a,n,papel in [(0x495bc8,6,'nomes dos bancos'),(0x410f64,26,'ancoragem por tipo'),
                       (0x412328,26,'desenho por tipo'),(0x4572e8,26,'parametros por tipo'),
                       (0x44812c,26,'fase de parada por tipo')]:
        bruto=imagem[a-base:a-base+n*4]
        vals=struct.unpack('<'+'I'*n,bruto)
        registro=dict(endereco=hex(a),papel=papel,ponteiros=[hex(v) for v in vals],
                      bytes_hex=bruto.hex(),sha256=hashlib.sha256(bruto).hexdigest())
        if a==0x495bc8:
            registro['nomes']=[imagem[v-base:].split(b'\0')[0].decode('ascii') for v in vals]
        tabelas.append(registro)
    (pasta/'tabelas.json').write_text(json.dumps(tabelas,indent=2)+'\n')
    print('Trechos extraídos:', len(registros))


if __name__ == '__main__':
    extrair()
