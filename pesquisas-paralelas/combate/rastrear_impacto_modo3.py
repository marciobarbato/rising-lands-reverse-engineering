"""Export the exact message-4C null-group guard and dispatch-table provenance."""
import hashlib
import json
import struct
from pathlib import Path

from extrair_evidencias import HASH, ler_imagem, Cs, CS_ARCH_X86, CS_MODE_32


def main():
    image = ler_imagem()
    root = Path(__file__).resolve().parent / 'evidencias'
    table = bytes(image[0x482998-0x400000:0x4829c8-0x400000])
    targets = struct.unpack('<12I', table)
    assert targets[11] == 0x482db6
    start, end = 0x482db6, 0x482dbe
    guard = bytes(image[start-0x400000:end-0x400000])
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = list(cs.disasm(guard, start))
    assert [(i.mnemonic, i.op_str) for i in instructions] == [('test', 'ecx, ecx'), ('je', '0x482eb5')]
    lines = [f'; message 0x4c null-group guard; [{start:#x},{end:#x})', f'; Original EXE SHA-256: {HASH}']
    lines += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}' for i in instructions]
    filename = 'impacto-modo3-00482db6.asm'
    (root / filename).write_text('\n'.join(lines)+'\n')
    report = dict(sha256_original=HASH, guard=dict(start=hex(start), end_exclusive=hex(end),
        sha256_bytes=hashlib.sha256(guard).hexdigest(), bytes_hex=guard.hex(), file=filename),
        dispatch_table=dict(start='0x482998', end_exclusive='0x4829c8',
            sha256_bytes=hashlib.sha256(table).hexdigest(), bytes_hex=table.hex(),
            entries=[dict(message=hex(0x41+i), target=hex(target)) for i, target in enumerate(targets)]),
        scope='Only message4c ECX-null return through existing0x482eb5 epilogue; no active group or other handler implementation')
    (root / 'impacto-modo3.json').write_text(json.dumps(report, indent=2)+'\n')
    print(root / 'impacto-modo3.json')


if __name__ == '__main__':
    main()
