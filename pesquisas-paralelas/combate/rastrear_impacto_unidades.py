"""Hash and export the unit-impact wrapper's new reference ranges only."""
import hashlib
import json
from pathlib import Path
import struct

from extrair_evidencias import HASH, ler_imagem, Cs, CS_ARCH_X86, CS_MODE_32

RANGES = {
    'InfligeDegat': (0x450874, 0x4510dd, '00450874.asm'),
    'PlayerEstAllie': (0x46d838, 0x46d877, '0046d838.asm'),
    'PlayerAAttaqueSet': (0x46d600, 0x46d629, None),
    'PlayerResetAllie': (0x46d8cb, 0x46d927, None),
    'MAJSympathie': (0x475118, 0x475267, None),
    'CalculDirection': (0x477042, 0x4770ee, None),
    'CalculDirCase': (0x4770ee, 0x4772ec, None),
}


def main():
    im = ler_imagem()
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    out = Path(__file__).resolve().parent / 'evidencias'
    ranges = []
    for name, (a, b, existing) in RANGES.items():
        raw = bytes(im[a - 0x400000:b - 0x400000])
        filename = existing or f'impacto-{a:08x}.asm'
        if existing is None:
            lines = [f'; {name}; [0x{a:08x},0x{b:08x})', f'; Original EXE SHA-256: {HASH}']
            lines += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}'.rstrip()
                      for i in cs.disasm(raw, a)]
            (out / filename).write_text('\n'.join(lines) + '\n')
        ranges.append(dict(symbol=name, start=hex(a), end_exclusive=hex(b),
            sha256_bytes=hashlib.sha256(raw).hexdigest(), file=filename,
            predecessor_reused=existing is not None))
    table = bytes(im[0x450858 - 0x400000:0x450874 - 0x400000])
    report = dict(sha256_original=HASH, ranges=ranges,
        hit_dispatch=dict(address='0x450858', first_type=11, bytes=table.hex(),
            sha256_bytes=hashlib.sha256(table).hexdigest(),
            destinations=[hex(x) for x in struct.unpack('<7I', table)]),
        scope='Mode-1 unit wrapper; building branch remains unsupported; query/effect bodies are explicit providers')
    (out / 'impacto-unidades.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'Hashed {len(ranges)} original ranges; exported five new assembly files and the hit dispatch table')


if __name__ == '__main__':
    main()
