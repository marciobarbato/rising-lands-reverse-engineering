"""Export intact original physical exit and production caller bytes."""
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
    pasta = RAIZ / 'evidencias/colocacao-saida'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in (('SetSortEngin', 0x445fbc, 0x446189),
                              ('shared_epilogue', 0x4431fb, 0x443203),
                              ('SortieTroupe_placement_movement', 0x420f8a, 0x420f9e)):
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
                     physical_calls=['SetEnginCollision 0x442cb4','DecouvreTerrain 0x476851', 'IllumineTerrain 0x476cb3','SetMiniMap 0x46a388'],
                     scope='Complete exit body plus movement caller; stop before conditional request.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported physical exit intervals:', len(extrair()['intervals']))
