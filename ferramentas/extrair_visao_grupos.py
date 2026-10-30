"""Export the intact-original bodies of the structure vision, group selection, minimap view and exit-position
routines (M3.1 round 2).

Each named routine runs from its entry to the next original symbol; the shared epilogues the bodies jump to and the
jump tables they index are exported as their own intervals. Same reader and format as ``extrair_entrada_estruturas``.
"""
import hashlib
import json
from pathlib import Path
import struct

RAIZ = Path(__file__).resolve().parents[1]
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
ROTINAS = ('BatimentIllumine', 'BatimentDecouvre', 'IllumineCase', 'EteintCase', 'DecouvreCase',
           'SauveSelectionGroupe', 'RestaureSelectionGroupe', 'EnginGetCentreGroupe', 'MiniMapRecentre',
           'MiniMapSetPos', 'CalculPosition', 'RechercheDecalageSortie', 'TypeEnginEstEnLoop', 'EnginEstVivant',
           'EnginGetEtat', 'EnginGetPlayer', 'EnginGetType')
EXTRAS = (('epilogue 0x419c43 (BatimentDecouvre)', 0x419c43, 0x419c4b),
          ('epilogue 0x4725eb (SauveSelectionGroupe)', 0x4725eb, 0x4725ee),
          ('epilogue 0x41dbe5 (CalculPosition)', 0x41dbe5, 0x41dbed),
          ('epilogue 0x41db1d (RechercheDecalageSortie, CalculPosition)', 0x41db1d, 0x41db24))
TABELAS = (('CalculPosition geometry by structure type', 0x420640, 22),
           ('RechercheDecalageSortie by structure type', 0x41d178, 22),
           ('TypeEnginEstEnLoop by type - 0xb', 0x440c2c, 6)) + tuple(
    (f'CalculPosition correction table {a:#x}', a, 22)
    for a in (0x4202d0, 0x420328, 0x420380, 0x4203d8, 0x420430, 0x420488, 0x4204e0, 0x420538, 0x420590, 0x4205e8))


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
    pasta = RAIZ / 'evidencias/visao-grupos'
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
