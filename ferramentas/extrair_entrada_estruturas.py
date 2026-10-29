"""Export the intact-original bodies of the structure-entry, lodging and Bag routines (M3/M4 groundwork).

Each named routine runs from its entry to the next original symbol; unit state 13's body inside EnginNextEtape,
the shared epilogues the bodies jump to and the jump tables they index are exported as their own intervals.
Same reader and format as ``extrair_construcao_core``.
"""
import hashlib
import json
from pathlib import Path
import struct

RAIZ = Path(__file__).resolve().parents[1]
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
ROTINAS = ('BagVide', 'BagPlein', 'BagAccepte', 'BagGetNbContenu', 'BagContient', 'BagContientTroupe', 'BagGetCode',
           'BagGetType', 'BagRetire', 'BagPrend', 'EnginGetBag', 'PlaceLibre', 'BatimentAdjacent', 'GetCaseCentrale',
           'BatimentGetCaseEntrer', 'BatimentGetModeEtat', 'BatimentGetType', 'BatimentGetPlayer',
           'BatimentGetVolume', 'BatimentEnDestruction', 'BatimentGetCase', 'RetireEngin', 'AnimWorkEngin',
           'CalculEntreBatiment', 'SetEnginRentreBatiment', 'SetEnginSelectRentreBatiment', 'EnginSelectPeutEntrer',
           'BatimentRetireColon', 'EnginResetType', 'EnginGetVie', 'EnginGetVieMax', 'EnginEstVivant',
           'EnginEstMiroir', 'EnginEstBlesse', 'EnginBombeEstMax', 'TypeEnginEstTroupe', 'TypeEnginEstAPied',
           'TypeEnginEstEngin', 'EnginGetType', 'EnginGetPlayer')
EXTRAS = (('EnginNextEtape state 13 body', 0x4558e4, 0x455a61),
          ('EnginNextEtape state-13 refusal 0x454d97 (SetDeplaceEngin, +0xc0 = 0xffff)', 0x454d97, 0x454db5),
          ('EnginNextEtape continuation 0x454ccd', 0x454ccd, 0x454cd5),
          ('epilogue 0x44f29d / 0x440d58 (CalculEntreBatiment)', 0x44f29d, 0x44f2a3),
          ('epilogue 0x440d58', 0x440d58, 0x440d5e),
          ('epilogue 0x41a054 (PlaceLibre)', 0x41a054, 0x41a05c),
          ('epilogue 0x41b31f (BatimentRetireColon)', 0x41b31f, 0x41b328),
          ('epilogue 0x41db1e (BatimentGetCase, BatimentGetVolume)', 0x41db1e, 0x41db24),
          ('epilogue 0x44507b (BagRetireInd)', 0x44507b, 0x445082))
TABELAS = (('BagContient by tag - 1', 0x44719c, 7), ('SetEnginRentreBatiment type-14 unit types 0xb..0x11', 0x445af4, 7),
           ('AnimWorkEngin type 13 by phase', 0x447f34, 5), ('AnimWorkEngin type 5 by phase', 0x447f48, 4),
           ('TypeEnginEstEngin 0xb..0x11', 0x442418, 7), ('BatimentRetireColon light radius by type', 0x41dd88, 22),
           ('EnginNextEtape by unit state', 0x4543c8, 25))


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
    simbolos = sorted((int(e['endereco'], 16), e['nome_original']) for e in
                      json.loads((RAIZ / 'relatorios/simbolos-originais.json').read_text())['simbolos'])
    por_nome = {nome: i for i, (_, nome) in enumerate(simbolos)}
    intervalos = [(nome, simbolos[por_nome[nome]][0], simbolos[por_nome[nome] + 1][0]) for nome in ROTINAS] + \
        list(EXTRAS)
    pasta = RAIZ / 'evidencias/entrada-estruturas'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in intervalos:
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
