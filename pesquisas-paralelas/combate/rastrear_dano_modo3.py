"""Export focused original mode-3 source queries without prior evidence edits."""
import hashlib
import json
from pathlib import Path

from extrair_evidencias import HASH, ler_imagem, Cs, CS_ARCH_X86, CS_MODE_32

RANGES = {'TypeBatimentGetDegat_selector_bodies': (0x418b42, 0x418b97),
          'BatimentGetPlayer': (0x41a08c, 0x41a0ab),
          'BatimentGetType': (0x41a4f4, 0x41a513)}


def main():
    image = ler_imagem()
    root = Path(__file__).resolve().parent / 'evidencias'
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    ranges = []
    for name, (start, end) in RANGES.items():
        data = bytes(image[start-0x400000:end-0x400000])
        filename = f'dano-modo3-{start:08x}.asm'
        lines = [f'; {name}; [{start:#x},{end:#x})', f'; Original EXE SHA-256: {HASH}']
        lines += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}'.rstrip()
                  for i in cs.disasm(data, start)]
        (root / filename).write_text('\n'.join(lines)+'\n')
        ranges.append(dict(name=name, start=hex(start), end_exclusive=hex(end),
                           sha256_bytes=hashlib.sha256(data).hexdigest(), file=filename))
    (root / 'dano-modo3.json').write_text(json.dumps(dict(sha256_original=HASH, ranges=ranges,
        scope='Mode3 source getters and damage selector1; full EAX of record getters retains address bits, caller consumes AL'), indent=2)+'\n')
    print(f'Exported {len(ranges)} focused original ranges')


if __name__ == '__main__':
    main()
