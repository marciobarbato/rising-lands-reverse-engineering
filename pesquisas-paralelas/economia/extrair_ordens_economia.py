"""Export the intact-original bodies of the economy order setters and construction gates (M3 groundwork).

Each interval runs from the routine entry to the next original symbol (CreerBatiment ends at its
epilogue; the bytes after it are data); shared epilogues the bodies jump to are their own
intervals. Writes ``evidencias/ordens-economia/*.asm`` and ``manifesto.json``.

    python3 -B pesquisas-paralelas/economia/extrair_ordens_economia.py
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
SAIDA = PASTA / 'evidencias/ordens-economia'
INTERVALOS = (
    ('EnginTravailSelectionne', 0x47248f, 0x47253d), ('epilogue 0x47234f (EnginTravailSelectionne)', 0x47234f, 0x472355),
    ('SetMineEnginSelect', 0x473324, 0x4733b8), ('epilogue 0x472903 (Select setters)', 0x472903, 0x47290b),
    ('SetMineEngin', 0x444f48, 0x444fdb), ('SetDepotEnginSelect', 0x47312c, 0x473194),
    ('SetDepotEngin', 0x444dad, 0x444dee), ('SetRamasseEnginSelect', 0x473d2c, 0x473dbf),
    ('SetRamasseEngin', 0x445947, 0x4459c4), ('tail 0x444f3c (SetRamasseEngin)', 0x444f3c, 0x444f48),
    ('GetRessourceStock', 0x46769d, 0x4676e5), ('tail 0x467666 (GetRessourceStock)', 0x467666, 0x467670),
    ('TestRessource', 0x4676e5, 0x467718), ('EnleveMatiere', 0x46792c, 0x46799c),
    ('CreerBatiment', 0x41fea2, 0x4202ce), ('BagReset', 0x44710b, 0x447148), ('BagInit', 0x447148, 0x447197),
    ('CalculConstruireBatiment', 0x44ab60, 0x44b595), ('epilogue 0x44f29d (CalculConstruireBatiment)', 0x44f29d, 0x44f2a3),
    ('epilogue 0x440d58 (CalculConstruireBatiment)', 0x440d58, 0x440d5e),
    ('call site 0x45efe2..0x45f041 (ProcessInputGame tag 6)', 0x45efe2, 0x45f041),
    ('call site 0x45f20f..0x45f221 (ProcessInputGame tag 0x12)', 0x45f20f, 0x45f221))
TABELAS = (('ProcessInputGame by packet tag', 0x45ed20, 0x28),)


def ler_pe():
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe + o)[0] for o in (6, 20))
    secoes = [struct.unpack_from('<III', raw, pe + 24 + op + i * 40 + 12) for i in range(n)]

    def ler(inicio, tamanho):
        rva = inicio - 0x400000
        for base, t, offset in secoes:
            if offset and base <= rva and rva + tamanho <= base + t:
                return raw[offset + rva - base:offset + rva - base + tamanho]
        raise ValueError('No original PE bytes at address')
    return ler


def extrair():
    import capstone
    ler = ler_pe()
    SAIDA.mkdir(exist_ok=True, parents=True)
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
            linhas.append(f'; {len(bruto) - coberto} trailing bytes are not code: {bruto[coberto:].hex()}')
        (SAIDA / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(name=nome, start=hex(inicio), end_exclusive=hex(fim),
                            sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    tabelas = [dict(name=nome, address=hex(a), entries=[hex(x) for x in struct.unpack(f'<{k}I', ler(a, 4 * k))])
               for nome, a, k in TABELAS]
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos, jump_tables=tabelas)
    (SAIDA / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported intervals:', len(extrair()['intervals']))
