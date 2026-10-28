"""Export intact original experience queue and local level-effect bytes."""
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
    pasta = RAIZ / 'evidencias/experiencia-unidades'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in (('EnginSetNewExperience', 0x44f9e0, 0x44fb09),
                              ('level_shared_epilogue', 0x44f987, 0x44f98a),
                              ('EnginSetExperimente', 0x44fe42, 0x44ff1d),
                              ('queue_shared_epilogue', 0x440d58, 0x440d5e),
                              ('SortieTroupe_experience_prefix', 0x420f81, 0x420f8a)):
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
    rva = 0x44f9cc - 0x400000
    for base, tamanho, offset in secoes:
        if offset and base <= rva and rva+20 <= base+tamanho:
            table = raw[offset+rva-base:offset+rva-base+20]
            break
    else:
        raise ValueError('No original level jump table')
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos,
                     unit_pool_pointer='0x4e19a0', unit_count=800, stride=276,
                     type_table='0x4965ae, 26 records of 50 bytes; fatigue word at +0x2e',
                     queue='0x4e19c4, supported four owners of ten bytes',
                     level_jump_table=dict(address='0x44f9cc', bytes=table.hex(),
                                           sha256=hashlib.sha256(table).hexdigest(),
                                           entries=[hex(v) for v in struct.unpack('<5I', table)]),
                     scope='Complete local level effects and queue consumption; production stops before placement.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported experience intervals:', len(extrair()['intervals']))
