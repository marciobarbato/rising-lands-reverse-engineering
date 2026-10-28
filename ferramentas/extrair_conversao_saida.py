"""Export original caller bytes and callback-order evidence for shared conversion."""
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
    p = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, p+o)[0] for o in (6, 20))
    secoes = [struct.unpack_from('<III', raw, p+24+op+i*40+12) for i in range(n)]
    def ler(a, tamanho):
        rva = a - 0x400000
        for base, size, offset in secoes:
            if offset and base <= rva and rva + tamanho <= base + size:
                return raw[offset+rva-base:offset+rva-base+tamanho]
        raise ValueError('No original PE bytes at address')
    pasta = RAIZ / 'evidencias/conversao-saida'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    intervalos = []
    for nome, a, b in (('SortieTroupe_position_and_conversion', 0x420f5a, 0x420f6e),
                        ('type4_bonus12_then_frame', 0x45782b, 0x45785a)):
        bruto = ler(a, b-a)
        ins = list(md.disasm(bruto, a))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError('Incomplete original disassembly')
        arquivo = f'{a:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        intervalos.append(dict(name=nome, start=hex(a), end_exclusive=hex(b),
                               sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    referencias = []
    for a, b, arquivo in ((0x457b87, 0x457e0c, '00457b87.asm'),
                           (0x457350, 0x457b87, '00457350.asm'),
                           (0x4475ac, 0x4475ef, '004475ac.asm'),
                           (0x428cc0, 0x428e71, '00428cc0.asm')):
        referencias.append(dict(start=hex(a), end_exclusive=hex(b),
                                sha256=hashlib.sha256(ler(a, b-a)).hexdigest(),
                                existing_evidence='pesquisas-paralelas/combate/evidencias/' + arquivo))
    dados = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=intervalos,
                  existing_provider_evidence=referencias,
                  original_symbol_0x428cc0='BonusGetValEngin', established_alias='Modificateur',
                  scope='Core adapter reuses combat-owned local conversion; no economic query or world spawn body.')
    (pasta / 'manifesto.json').write_text(json.dumps(dados, indent=2) + '\n')
    return dados


if __name__ == '__main__':
    print('Exported caller/order intervals:', len(extrair()['intervals']))
