"""Export intact TerrainReset, MiniMapReset and BatimentModifyMap evidence."""
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
TRECHOS = (('TerrainReset', 0x46b315, 0x46b38f), ('Random', 0x4704dc, 0x470520),
           ('MiniMapReset', 0x469f00, 0x469f68), ('memset', 0x48c3b0, 0x48c3c8),
           ('memset_fill_leaf', 0x48d890, 0x48d933), ('BatimentModifyMap', 0x419e97, 0x419fc8),
           ('BatimentModifyMap_shared_epilogue', 0x42399a, 0x4239a0),
           ('SetMiniMap', 0x46a388, 0x46a70c))
# CALL sites of BatimentModifyMap and the DL value each one loads (bytes checked below).
CHAMADAS = ((0x41d021, 'BatimentConstruction', 0x41d019, 'ba01000000', 1),
            (0x41e12c, 'BatimentRetireColon', 0x41e121, 'ba01000000', 1),
            (0x41f26b, 'DemonteBatiment', 0x41f267, '31d2', 0),
            (0x41fa88, 'BatimentLogeEngin', 0x41fa7c, 'ba01000000', 1),
            (0x42114e, 'SortieTroupe', 0x421141, 'ba01000000', 1),
            (0x422cc3, 'CalculTrajectoire', 0x422cb7, 'ba01000000', 1),
            (0x46c1b1, 'MissionPlaceTerrain', 0x46c1a9, 'ba01000000', 1))


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
    pasta = RAIZ / 'evidencias/reset-terreno-minimapa'
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
    chamadas = []
    for chamada, rotina, carga, esperado, dl in CHAMADAS:
        alvo = chamada + 5 + struct.unpack('<i', _bytes(raw, secoes, chamada+1, chamada+5))[0]
        if _bytes(raw, secoes, chamada, chamada+1) != b'\xe8' or alvo != 0x419e97:
            raise ValueError(f'Not a BatimentModifyMap CALL at 0x{chamada:x}')
        if _bytes(raw, secoes, carga, carga+len(esperado)//2).hex() != esperado:
            raise ValueError(f'Unexpected DL load at 0x{carga:x}')
        chamadas.append(dict(call=hex(chamada), routine=rotina, dl_load=hex(carga), dl_bytes=esperado, dl=dl,
                             minimap_mode=6 if dl else 7))
    tabela = struct.unpack('<7I', _bytes(raw, secoes, 0x46a36c, 0x46a36c+28))
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, intervals=trechos,
                     setminimap_jump_table=dict(address='0x46a36c', index='mode-1 (u8; >6 skips)',
                                                targets=[hex(t) for t in tabela]),
                     batimentmodifymap_calls=chamadas,
                     globals=dict(objects='[0x507d74]', object_aux='[0x507dac]', attributes='[0x507da8]',
                                  light_counts='[0x507d98+4p]', light_edges='[0x507d88+4p]',
                                  discovered='[0x507d78+4p]', mines='0x509954 (20 x (origin u16, reserve u16))',
                                  random_state='0x497164 u32', minimap_size='u16 0x496fe0/0x496fe2',
                                  minimap_layers='[0x507d5c] final, [0x507d60] units, [0x507d64] structures',
                                  structure_pool='0x49a0c8 + index*276 (+2 origin, +4 owner, +8 type)',
                                  structure_geometry='u16 0x495d8c/0x495d8e + type*52 (width, height)',
                                  player_colors='0x4e24dc[owner]; owner 200 -> 0x1e'),
                     scope='Bodies and caller variants only; MissionLoad/MissionLoadName orchestration, '
                           'BatimentHabitable and the structure scan belong to missions/economy.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    return manifesto


if __name__ == '__main__':
    m = extrair()
    print('Exported intervals:', len(m['intervals']), 'BatimentModifyMap calls:',
          [(c['routine'], c['dl']) for c in m['batimentmodifymap_calls']])
