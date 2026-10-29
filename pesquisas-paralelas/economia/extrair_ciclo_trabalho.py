"""Export the intact-original bodies of the work cycle, the lodging credit and the gates that lead to them.

Writes ``evidencias/ciclo-trabalho/*.asm`` and ``manifesto.json`` (interval bytes SHA-256, jump tables).

    python3 -B pesquisas-paralelas/economia/extrair_ciclo_trabalho.py
"""
import hashlib
import json
from pathlib import Path
import struct

from extrair_ordens_economia import HASH, ler_pe

PASTA = Path(__file__).resolve().parent
SAIDA = PASTA / 'evidencias/ciclo-trabalho'
INTERVALOS = (
    ('CalculWorkEngin', 0x44bc74, 0x44e34c), ('epilogue 0x44f29d -> 0x440d58 (CalculWorkEngin)', 0x44f29d, 0x44f2a3),
    ('MineEstSurTerrain', 0x475402, 0x475431), ('MineGetIndice', 0x47544c, 0x4754a7), ('MineSetWork', 0x4754a7, 0x4754de),
    ('MineEndWork', 0x4754de, 0x475515), ('MineRecolte', 0x4755a7, 0x475620), ('TerrainRecolte', 0x4781e8, 0x478247),
    ('AjouteMatiere', 0x4678f2, 0x46792c), ('BatimentAjouteMatiere', 0x42340f, 0x4235bd),
    ('BatimentLogeEngin', 0x41f76e, 0x41fb12), ('epilogue 0x42399a (BatimentLogeEngin)', 0x42399a, 0x4239a0),
    ('InitBatimentPlayer', 0x41be88, 0x41bfe6), ('BatimentConstruction', 0x41cf59, 0x41d02b),
    ('BatimentConstruit', 0x41c652, 0x41c692), ('BatimentEstEnnemi', 0x41a61c, 0x41a65c), ('BatimentEstNeutre', 0x41d02b, 0x41d057),
    ('EnginSelectPeutEntrer', 0x472b6c, 0x4730ae), ('TypeEnginEstTroupe', 0x442347, 0x442380),
    ('SetRecolteEngin', 0x444ebd, 0x444f48), ('SetEnginDecharge', 0x4447fa, 0x44491c), ('SetDechargeCaveEngin', 0x444dee, 0x444e7f),
    ('SetTransporteEngin', 0x444e7f, 0x444ebd), ('SetEnginRentreBatiment', 0x445b10, 0x445f2d),
    ('CalculEntreBatiment', 0x449716, 0x44a2ed), ('SetPlayerOrdre', 0x45ecd4, 0x45ed1e),
    ('InputGame building press with troops 0x42ac0c..0x42b26e', 0x42ac0c, 0x42b26e),
    ('InputGame food/stone press 0x42b311..0x42b64d', 0x42b311, 0x42b64d),
    ('InputGame mode-9 depot packets 0x429b92..0x429da1', 0x429b92, 0x429da1),
    ('ProcessInputGame tags 6/7/8/0x10/0x13/0x21 0x45efe2..0x45f22f', 0x45efe2, 0x45f22f))
TABELAS = (('CalculWorkEngin type 7 phases (and type 13 from +6)', 0x44bc38, 11), ('CalculWorkEngin type 5 phases', 0x44bc64, 4),
           ('InputGame mode-9 source kinds 0..3 (mine, field, sack, cave)', 0x42923c, 4),
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
    print('Exported intervals:', len(extrair()['intervals']))
