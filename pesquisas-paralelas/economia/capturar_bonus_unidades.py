"""Capture original query code and dispatch tables as new immutable evidence."""
import hashlib
import json
from pathlib import Path
import struct
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH

INTERVALOS = ((0x428cc0, 0x428e71, 'BonusGetValEngin'),
              (0x4475ac, 0x4475ef, 'EnginTypeGetCapacite'),
              (0x4474c5, 0x4474c7, 'shared capacity return'))


def main():
    original = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(original).hexdigest() != HASH:
        raise ValueError('Original executable hash mismatch')
    catalogo = json.loads((RAIZ / 'relatorios/simbolos-originais.json').read_text())
    sbl = (RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes()
    if hashlib.sha256(sbl).hexdigest() != catalogo['sha256_sbl']:
        raise ValueError('Original symbol file hash mismatch')
    pe = pefile.PE(data=original)
    im, base = pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    captures = []
    for a,b,n in INTERVALOS:
        raw = im[a-base:b-base]
        name = f'bonus-unidades-{a:08x}.asm'
        lines = [f'; {n}; exclusive end 0x{b:08x}.', f'; Original EXE SHA-256: {HASH}',
                 '; Original instructions, including the incoming-ECX return path.']
        lines += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                  for i in md.disasm(raw,a)]
        (PASTA / 'evidencias' / name).write_text('\n'.join(lines)+'\n')
        captures.append(dict(symbol=n, start=f'0x{a:08x}', end_exclusive=f'0x{b:08x}',
                             bytes_hex=raw.hex(), sha256=hashlib.sha256(raw).hexdigest(), listing=name))
    tables = []
    for a,n in ((0x428c8c,13),(0x447544,26)):
        raw = im[a-base:a-base+n*4]
        tables.append(dict(address=f'0x{a:08x}', bytes_hex=raw.hex(),
                           targets=[f'0x{t:08x}' for t in struct.unpack('<'+'I'*n,raw)],
                           sha256=hashlib.sha256(raw).hexdigest()))
    result = dict(sha256_exe=HASH, sha256_sbl=catalogo['sha256_sbl'], capstone=capstone.__version__,
        scope='Complete read-only unit bonus/capacity queries; no bonus initialization or world conversion',
        captures=captures, dispatch_tables=tables,
        bonus_state=dict(address='0x004dfba0', players=4, types=26, record_bytes=18, player_stride=468),
        callback_consumers=dict(core_selectors=[1,12], combat_selectors=[5,6],
                                established_callback_identifier='Modificateur'),
        default_return='For non-neutral owners, selectors 8 or >12 return incoming ECX as u32 without table reads')
    (PASTA / 'evidencias/bonus-unidades.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'Captured {len(captures)} original code intervals and {len(tables)} dispatch tables.')


if __name__ == '__main__':
    main()
