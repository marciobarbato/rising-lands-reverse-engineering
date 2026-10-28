"""Export byte-grounded structure lifecycle intervals from the original PE."""
import hashlib
import json
import struct
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
INTERVALOS = (
    ('BatimentAlloc_prefix', 0x418e95, 0x419004),
    ('BatimentResetAll', 0x41a75c, 0x41a860),
    ('ResetBatiment', 0x41b9d6, 0x41ba49),
    ('CreerBatiment_first_free_scan', 0x41fea2, 0x41ff04),
    ('CreerBatiment_failure_epilogue', 0x4202c1, 0x4202ce),
)


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe + off)[0] for off in (6, 20))
    secoes = [struct.unpack_from('<III', raw, pe + 24 + op + i * 40 + 12) for i in range(n)]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    pasta = RAIZ / 'evidencias/ciclo-estruturas'
    pasta.mkdir(exist_ok=True, parents=True)
    trechos = []
    for nome, a, b in INTERVALOS:
        rva = a - 0x400000
        for base, tamanho, offset in secoes:
            if offset and base <= rva and rva + b - a <= base + tamanho:
                bruto = raw[offset + rva - base:offset + rva - base + b - a]
                break
        else:
            raise ValueError('Interval has no original PE bytes')
        ins = list(md.disasm(bruto, a))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError('Incomplete disassembly')
        arquivo = f'{a:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n', encoding='utf-8')
        trechos.append(dict(name=nome, start=hex(a), end_exclusive=hex(b), size=len(bruto),
                           sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos,
                     record_base='0x49a0c8', record_stride=276, record_count=1000,
                     flags_base='0x49a070', flags_size=88, selections_base='0x495be0',
                     scope='Synthetic memory; startup stops at 0x419004 before economic effects. '
                           'Free scan stops at 0x41ff04 or the original failure return. '
                           'No whole-game or mission-loader validation.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported intervals:', len(extrair()['intervals']))
