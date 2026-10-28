"""Export CalculPosition, all dispatch tables, and original geometry bytes."""
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    pe = struct.unpack_from('<I', raw, 60)[0]
    op, n = (struct.unpack_from('<H', raw, pe + o)[0] for o in (20, 6))
    secoes = [struct.unpack_from('<III', raw, pe + 24 + op + i * 40 + 12) for i in range(n)]

    def ler(a, tamanho):
        rva = a - 0x400000
        for base, size, offset in secoes:
            if offset and base <= rva and rva + tamanho <= base + size:
                return raw[offset + rva - base:offset + rva - base + tamanho]
        raise ValueError('Interval has no original PE bytes')

    pasta = RAIZ / 'evidencias/posicao-saida'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    intervalos = []
    for nome, inicio, fim in (('CalculPosition', 0x420698, 0x420ba5),
                              ('shared_stack_adjustment', 0x41dbe5, 0x41dbed),
                              ('shared_register_epilogue', 0x41db1e, 0x41db24)):
        bruto = ler(inicio, fim - inicio)
        ins = list(md.disasm(bruto, inicio))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError('Incomplete original disassembly')
        arquivo = f'{inicio:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        intervalos.append(dict(name=nome, start=hex(inicio), end_exclusive=hex(fim),
                               sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    tabelas = []
    for inicio in range(0x4202d0, 0x420698, 88):
        bruto = ler(inicio, 88)
        tabelas.append(dict(address=hex(inicio), bytes_hex=bruto.hex(),
                            sha256=hashlib.sha256(bruto).hexdigest(),
                            targets=[hex(a) for a in struct.unpack('<22I', bruto)]))
    dimensoes = []
    for tipo in range(22):
        inicio = 0x495d8c + tipo * 52
        bruto = ler(inicio, 4)
        dimensoes.append(dict(type=tipo, address=hex(inicio), bytes_hex=bruto.hex(),
                               width=struct.unpack_from('<H', bruto)[0],
                               height=struct.unpack_from('<H', bruto, 2)[0]))
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__,
                     intervals=intervalos, jump_tables=tabelas, dimensions=dimensoes,
                     scope='Complete CalculPosition and shared epilogues; no caller or unit conversion.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported CalculPosition and', len(extrair()['jump_tables']), 'jump tables')
