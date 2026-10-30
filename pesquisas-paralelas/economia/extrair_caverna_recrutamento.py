"""Export the intact-original bodies of the cave structure body, habitation and recruitment routines.

Writes ``evidencias/caverna-recrutamento/*.asm`` and ``manifesto.json`` (interval bytes SHA-256, jump tables).

    python3 -B pesquisas-paralelas/economia/extrair_caverna_recrutamento.py
"""
import hashlib
import json
from pathlib import Path
import struct

from extrair_ordens_economia import HASH, ler_pe

PASTA = Path(__file__).resolve().parent
SAIDA = PASTA / 'evidencias/caverna-recrutamento'
INTERVALOS = (
    ('BatimentNextEtape prelude 0x4268d4..0x426918', 0x4268d4, 0x426918),
    ('BatimentNextEtape type-3 (CAVE) body 0x426aff..0x426c10', 0x426aff, 0x426c10),
    ('BatimentNextEtape exit 0x4281c0..0x4281c7', 0x4281c0, 0x4281c7), ('shared tail 0x41db1d', 0x41db1d, 0x41db24),
    ('BatimentHabitable', 0x41cc70, 0x41cde0), ('BatimentSetTechnologie', 0x41c76c, 0x41cb9a),
    ('InitBatimentPlayer', 0x41be88, 0x41bfe6), ('InitBatimentNeutre', 0x41c017, 0x41c18a),
    ('InitRecruteTroupe', 0x4283e2, 0x428691), ('CalculTroupe types 1/2 0x4259e6..0x425b5e', 0x4259e6, 0x425b5e),
    ('CalculTroupe dispatch and exit 0x4263e5..0x426418', 0x4263e5, 0x426418),
    ('SortieTroupe', 0x420e4c, 0x421250), ('epilogue 0x42399a (SortieTroupe)', 0x42399a, 0x4239a0),
    ('EnginGetTimeRecrute', 0x4410b7, 0x4410d2), ('EnginGetRessource', 0x4410d2, 0x441108),
    ('TypeEnginEstRealisable', 0x44228e, 0x4422b0), ('BatimentGetColons', 0x41a4c4, 0x41a4f4),
    ('BatimentGetCapacite', 0x41f3ed, 0x41f46e), ('BatimentSelection', 0x41b673, 0x41b78f),
    ('ProcessInputGame tag 17 0x45f19f..0x45f1b3', 0x45f19f, 0x45f1b3),
    ('BatimentTuyauCave / BatimentPorteCave (the +0x75 writers)', 0x41a65c, 0x41a6a7))
TABELAS = (('BatimentNextEtape by structure type - 1', 0x426880, 21),
           ('BatimentHabitable radius by structure type', 0x41cc18, 22),
           ('SortieTroupe abandonment radius by structure type', 0x420df4, 22),
           ('ProcessInputGame by packet tag', 0x45ed20, 0x28))


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
    m = extrair()
    print(json.dumps(dict(intervals=len(m['intervals']), tables=len(m['jump_tables'])), indent=1))
