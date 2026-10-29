"""Export the intact-original bodies of the selection and order-setter routines (M3 groundwork).

Each interval runs from the routine entry to the next original symbol; shared epilogues that a
body jumps to are exported as their own intervals. Jump tables the bodies index are recorded
with their entries.
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
    ('SelectionEngin', 0x4742dc, 0x474610), ('EnginAddSelection', 0x4741cd, 0x4742dc),
    ('EnginSelectionnable', 0x474169, 0x4741cd), ('SelectionAddEngin', 0x4725ee, 0x472648),
    ('RetireSelectionEngin', 0x472576, 0x4725ee), ('DeselectionEngin', 0x472648, 0x47268b),
    ('DeSelectionGroupe', 0x47268b, 0x4726f7), ('epilogue 0x472251 (DeSelectionGroupe)', 0x472251, 0x472258),
    ('Deselection', 0x429180, 0x4291bc), ('BatimentSelection', 0x41b673, 0x41b78f),
    ('BatimentDeselectionner', 0x41b663, 0x41b673), ('BagContientTroupe', 0x44724a, 0x4472d3),
    ('BagContient', 0x4471b8, 0x44724a), ('BatimentGetVolume', 0x41a0ab, 0x41a18f),
    ('epilogue 0x41db1e (BatimentGetVolume)', 0x41db1e, 0x41db24),
    ('SetDeplaceEnginSelect', 0x473e6e, 0x473f4b), ('epilogue 0x472903 (Select setters)', 0x472903, 0x47290b),
    ('SetAttaqueEnginSelect', 0x473dbf, 0x473e6e), ('SetConstruitBatimentSelect', 0x473a07, 0x473ac0),
    ('SetEnginConstruitBatiment', 0x4454ce, 0x44564c), ('SetRecolteEnginSelect', 0x473290, 0x473324),
    ('SetRecolteEngin', 0x444ebd, 0x444f48), ('SetTransporteEnginSelect', 0x473212, 0x473290),
    ('SetTransporteEngin', 0x444e7f, 0x444ebd), ('tail 0x443222 (SetTransporteEngin)', 0x443222, 0x44325d),
    ('EnginInZone', 0x4461f4, 0x4463ef), ('EnginVisible', 0x4465bf, 0x4465df), ('EnginGetEtat', 0x440e11, 0x440e31),
    ('TypeEnginEstEnLoop', 0x440c44, 0x440c5d), ('TypeEnginEstVehicule', 0x442394, 0x4423b0),
    ('TypeEnginEstAerien', 0x4422cf, 0x4422dd), ('shared AL=1 return 0x4422cc', 0x4422cc, 0x4422cf),
    ('SwapWORD', 0x467cc0, 0x467cd1), ('BatimentTailleGet', 0x41a996, 0x41a9c3),
    ('BatimentGetDecalageConstruction', 0x41aea4, 0x41aee2), ('EnginAsk', 0x440d5e, 0x440df0),
    ('EnginGetVolume', 0x440c5d, 0x440d5e), ('EnginEstSelectionne', 0x472174, 0x4721a8),
    ('Distance2d', 0x479555, 0x4795af))
TABELAS = (('EnginInZone by unit type', 0x44618c, 26), ('BagContient by mode-1', 0x44719c, 7),
           ('TypeEnginEstEnLoop by type-11', 0x440c2c, 6), ('TypeEnginEstVehicule by type-11', 0x442380, 5),
           ('BatimentGetDecalageConstruction by structure type', 0x41ae4c, 22))


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
    pasta = RAIZ / 'evidencias/selecao-ordens'
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
