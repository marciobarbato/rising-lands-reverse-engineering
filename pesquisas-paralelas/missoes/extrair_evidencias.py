"""Export intact loader instructions and a hash-only original mission inventory."""
import hashlib
import json
from collections import Counter
from ambiente_missoes import CD, OWNED, ROOT
from analisar import dependencias, HASH_ESTUDADO
from formatos import ler_eta

RANGES = (
    ('LoadEngin', 0x46acbf, 0x46b01e),
    ('LoadEngin_shared_return', 0x46b112, 0x46b119),
    ('MissionLoad', 0x46c2cf, 0x46c5e3),
    ('MissionLoadName', 0x46c5e3, 0x46c9a5),
    ('MissionPlaceTerrain', 0x46c122, 0x46c1b8),
    ('SelectionInit', 0x472555, 0x472576),
    ('FileReadSeek', 0x458461, 0x4584a3),
)


def exportar():
    pefile, capstone = dependencias()
    raw = (CD / 'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe = pefile.PE(data=raw)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    dest = OWNED / 'evidencias'
    dest.mkdir(parents=True, exist_ok=True)
    intervals = []
    for name, start, end in RANGES:
        code = pe.get_data(start - pe.OPTIONAL_HEADER.ImageBase, end-start)
        ins = list(md.disasm(code, start))
        if sum(i.size for i in ins) != len(code):
            raise ValueError('Incomplete original disassembly')
        filename = f'{start:08x}.asm'
        (dest / filename).write_text('\n'.join(
            [f'; {name}; intact original SHA-256 {HASH_ESTUDADO}'] +
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]) + '\n')
        intervals.append(dict(name=name, start=hex(start), end_exclusive=hex(end),
                              sha256=hashlib.sha256(code).hexdigest(), file=filename))
    manifest = dict(original_sha256=HASH_ESTUDADO, intervals=intervals,
                    analysis_sha256='26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0',
                    inspected_main='1f9019d8027f59e0fa304df29961b9c13ea5f4be',
                    provider_files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in (ROOT/'ferramentas/formatos.py', ROOT/'ferramentas/unidades.py',
                                              ROOT/'pesquisas-paralelas/combate/inicializacao_ataque.py')})
    (dest/'manifesto.json').write_text(json.dumps(manifest, indent=2)+'\n')
    assets = []
    for path in sorted(CD.rglob('*')):
        if not path.is_file() or 'WORLD' not in path.relative_to(CD).parts:
            continue
        data = path.read_bytes()
        row = dict(path=str(path.relative_to(CD)), size=len(data), sha256=hashlib.sha256(data).hexdigest())
        if path.suffix.upper() == '.ETA':
            parsed = ler_eta(data)
            row.update(width=parsed['largura'], height=parsed['altura'],
                       blocks=parsed['blocos'], suffix=parsed['sufixo'])
        assets.append(row)
    inventory = dict(original_sha256=HASH_ESTUDADO, asset_counts=dict(Counter(p['path'].split('.')[-1] for p in assets)),
                     assets=assets, scope='Disk inventory only; no commercial files copied or runtime initialization inferred.')
    (dest/'inventario.json').write_text(json.dumps(inventory, indent=2)+'\n')
    return manifest, inventory


if __name__ == '__main__':
    m, i = exportar()
    print('Original intervals:', len(m['intervals']), 'Mission assets:', i['asset_counts'])
