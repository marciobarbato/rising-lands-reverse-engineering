"""Export complete original global unit reset and inline Bag fragments."""
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
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    secoes = [struct.unpack_from('<III', raw, pe+24+op+i*40+12) for i in range(n)]
    pasta = RAIZ / 'evidencias/ciclo-unidades'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in (('EnginResetAll', 0x441659, 0x441775),
                              ('table_bag_headers', 0x4416b1, 0x4416ce),
                              ('table_bag_entries', 0x441679, 0x441692),
                              ('unit_bag_headers', 0x44174d, 0x44176d),
                              ('unit_bag_entries', 0x4416d2, 0x4416eb)):
        rva = inicio - 0x400000
        for base, tamanho, offset in secoes:
            if offset and base <= rva and rva + fim-inicio <= base+tamanho:
                bruto = raw[offset+rva-base:offset+rva-base+fim-inicio]
                break
        else:
            raise ValueError('No original PE bytes at address')
        ins = list(md.disasm(bruto, inicio))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError('Incomplete original disassembly')
        arquivo = f'{inicio:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(name=nome, start=hex(inicio), end_exclusive=hex(fim),
                            sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos,
                     unit_pool_pointer='0x4e19a0', unit_count=800, stride=276,
                     owner_type_bags='0x4e19b8 pointer table; four pools of 26 records, stride104',
                     bag_preserved_offsets=['0x60','0x61','0x62','0x63','0x64','0x65'],
                     scope='Complete raw pool reset; no allocation, mission loading or physical teardown.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported unit reset intervals:', len(extrair()['intervals']))
