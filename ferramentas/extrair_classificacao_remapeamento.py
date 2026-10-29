"""Export intact remap classification, initialization queries and binding caller evidence."""
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
TRECHOS = (('Chemin_Remap',0x42ee1c,0x42f1e1),('TerrainEstObstacleNaturel',0x4752b8,0x475302),
 ('EnginGetType',0x442025,0x442045),('TypeEnginEstMonstre',0x4422dd,0x4422e8),
 ('monster_true_tail',0x4422da,0x4422dd),('FileOpen',0x458420,0x45844c),
 ('FileClose',0x45844c,0x458461),('FileRead',0x458461,0x45848b))
def _secoes(raw):
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    return [struct.unpack_from('<III', raw, pe+24+op+i*40+12) for i in range(n)]


def _bytes(raw, secoes, inicio, fim):
    rva = inicio - 0x400000
    for base, tamanho, offset in secoes:
        if offset and base <= rva and rva + fim-inicio <= base+tamanho:
            return raw[offset+rva-base:offset+rva-base+fim-inicio]
    raise ValueError('No original PE bytes at address')


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    secoes = _secoes(raw)
    pasta = RAIZ / 'evidencias/classificacao-remapeamento'
    pasta.mkdir(exist_ok=True, parents=True)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for nome, inicio, fim in TRECHOS:
        bruto = _bytes(raw, secoes, inicio, fim)
        ins = list(md.disasm(bruto, inicio))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError('Incomplete original disassembly')
        arquivo = f'{inicio:08x}.asm'
        linhas = [f'; {nome}; original executable SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins]
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(name=nome, start=hex(inicio), end_exclusive=hex(fim),
                            sha256=hashlib.sha256(bruto).hexdigest(), file=arquivo))
    from vinculos_declarados import importacoes_pe
    slots=importacoes_pe(raw,0x400000)
    manifesto=dict(original_sha256=HASH,capstone=capstone.__version__,intervals=trechos,
        imports={hex(a):slots[a] for a in (0x5231c0,0x5231d0)},
        calls=dict(allocate='0x42eebd',lock='0x42eec5',classification_stop='0x42ef8b'),
        marker_source=dict(path='INSTALHD/TABLEAU.COL',size=702,
          sha256=hashlib.sha256((RAIZ.parent/'source/cd/INSTALHD/TABLEAU.COL').read_bytes()).hexdigest()),
        scope='No component allocation, region labels, cleanup, final success or full MissionLoad claim')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    print('Exported Stage16 intervals:',len(extrair()['intervals']))
