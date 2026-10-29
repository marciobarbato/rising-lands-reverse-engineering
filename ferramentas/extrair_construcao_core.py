"""Export the intact-original bodies of the Core construction routines (M3 groundwork).

Each interval runs from the routine entry to the next original symbol; the shared epilogues the
bodies jump to are exported as their own intervals, and the jump tables they index are recorded
with their entries. Reuses ``extrair_selecao_ordens``'s reader and format.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
INTERVALOS = (
    ('PlaceBatiment', 0x41c4ac, 0x41c652), ('BatimentModifyTerrain', 0x41ba49, 0x41bb8a),
    ('ResetCheminTerrainModify', 0x41b78f, 0x41b888), ('BatimentCollision', 0x41ab5c, 0x41ac8b),
    ('ValideHerse', 0x41ac8b, 0x41ad78), ('ChercheMurCombinaisons', 0x41c18a, 0x41c251),
    ('BatimentConstructible', 0x41fb12, 0x41fc40), ('BatimentPosable', 0x41fc40, 0x41fea2),
    ('epilogue 0x41db1d (PlaceBatiment, ResetCheminTerrainModify)', 0x41db1d, 0x41db24),
    ('epilogue 0x41a4ae (BatimentConstructible)', 0x41a4ae, 0x41a4b6),
    ('Chemin_ModifieZone', 0x43e138, 0x43e2a3), ('AlloueCouleur', 0x43e5a0, 0x43e5d5),
    ('LibereCouleur', 0x43e5d5, 0x43e616), ('MurAjoute', 0x43e616, 0x43e8b7), ('MurRetire', 0x43e8b7, 0x43eb64),
    ('Remplit', 0x43e464, 0x43e5a0), ('epilogue 0x42f1da (MurAjoute, MurRetire)', 0x42f1da, 0x42f1e1),
    ('SetTerrain', 0x476251, 0x476263), ('SetCollision', 0x47622e, 0x47623e), ('TerrainEnCollision', 0x4761d4, 0x4761f1),
    ('TerrainEstHerbe', 0x47636a, 0x4763c0), ('TerrainEstDecouvert', 0x4766f0, 0x47670a),
    ('EnginGetPlayer', 0x442045, 0x442064), ('EnginOccupeCase', 0x44246e, 0x442586),
    ('DeplaceEngin', 0x44930c, 0x449526), ('epilogue 0x440d58 (DeplaceEngin, CalculNextCase)', 0x440d58, 0x440d5e),
    ('CalculNextCase', 0x448f50, 0x449176))
TABELAS = (('PlaceBatiment first tile by structure type', 0x41c454, 22),
           ('BatimentCollision mask by structure type', 0x41ab04, 22),
           ('Chemin_ModifieZone by mode', 0x43e128, 4), ('DeplaceEngin by path state +0x88', 0x4492f0, 7),
           ('CalculNextCase local sound by unit type - 11', 0x448f38, 6))


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    secoes = [struct.unpack_from('<III', raw, pe+24+op+i*40+12) for i in range(n)]

    def ler(inicio, tamanho):
        rva = inicio - 0x400000
        for base, t, offset in secoes:
            if offset and base <= rva and rva + tamanho <= base + t:
                return raw[offset+rva-base:offset+rva-base+tamanho]
        raise ValueError('No original PE bytes at address')
    pasta = RAIZ / 'evidencias/construcao-core'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in INTERVALOS:
        bruto = ler(inicio, fim - inicio)
        ins = list(md.disasm(bruto, inicio))
        coberto = sum(i.size for i in ins)
        arquivo = f'{inicio:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        if coberto != len(bruto):
            linhas.append(f'; {len(bruto) - coberto} trailing bytes are not code (alignment/data): '
                          f'{bruto[coberto:].hex()}')
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(name=nome, start=hex(inicio), end_exclusive=hex(fim),
                            sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    tabelas = [dict(name=nome, address=hex(a), entries=[hex(x) for x in struct.unpack(f'<{k}I', ler(a, 4*k))])
               for nome, a, k in TABELAS]
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos, jump_tables=tabelas)
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported intervals:', len(extrair()['intervals']))
