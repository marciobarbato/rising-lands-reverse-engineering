"""Export only mode-4's original classification table; preserve old evidence."""
import hashlib
import json
import struct
from pathlib import Path

from extrair_evidencias import HASH, ler_imagem


def main():
    image = ler_imagem()
    start, end = 0x450288, 0x4502f0
    data = bytes(image[start-0x400000:end-0x400000])
    targets = struct.unpack('<26I', data)
    assert set(targets) == {0x4504e6, 0x4504f2}
    report = dict(sha256_original=HASH, start=hex(start), end_exclusive=hex(end),
        sha256_bytes=hashlib.sha256(data).hexdigest(), bytes_hex=data.hex(),
        entries=[dict(victim_type=i, target=hex(target), class_value=1 if target == 0x4504e6 else 2)
                 for i, target in enumerate(targets)],
        scope='Mode4 victim classification only; prefix and division reuse unchanged consumo-004502f0.asm')
    path = Path(__file__).resolve().parent / 'evidencias/dano-modo4-tabela.json'
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(path)


if __name__ == '__main__':
    main()
