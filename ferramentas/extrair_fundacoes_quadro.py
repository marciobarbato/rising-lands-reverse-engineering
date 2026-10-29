"""Export intact frame-foundation intervals of CalculGame 0x42c868 (M2 Core inventory).

Static analysis only: no instruction is executed. The intact executable is the
byte source; the normalized analysis PE is not read here. For every interval the
manifest records the SHA-256 of the original bytes, the absolute globals read and
written (from capstone operand access flags), the grid pointers dereferenced, the
direct callees, and a whole-code inventory of the other routines that reference
each written global or grid pointer.
"""
import bisect
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / '.local/python'))
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CODIGO = (0x401000, 0x401000 + 601088)
PASTA = RAIZ / 'evidencias/fundacoes-quadro'

# Grid pointers in DGROUP; the routines below load them and index by cell.
GRADES = {0x507d70: 'tile_grid_u16', 0x507d74: 'object_grid_u8', 0x507da8: 'attribute_grid_u8',
          0x507dac: 'animation_grid_u8'}

# (owner, role, name, start, end_exclusive)
TRECHOS = (
    ('core', 'counter', 'ProgIteration_counter_prefix', 0x475014, 0x475041),
    ('core', 'caller', 'ProgIteration', 0x47500e, 0x47509d),
    ('core', 'counter', 'GameNextFrame', 0x45d015, 0x45d01c),
    ('core', 'rng', 'Random', 0x4704dc, 0x470520),
    ('core', 'rng', 'Randomize', 0x470520, 0x470527),
    ('core', 'rng', 'SetRandomSeed', 0x470527, 0x47054c),
    ('core', 'rng', 'GetRandomSeed', 0x47054c, 0x470552),
    ('core', 'rng', 'iaRandom', 0x489728, 0x4897a4),
    ('core', 'rng_clock_thunk', 'timeGetTime_thunk', 0x493a24, 0x493a2a),
    ('core', 'rng_provenance', 'InitRand', 0x4583bc, 0x45841b),
    ('core', 'rng', 'LongRand', 0x45841b, 0x458420),
    ('core', 'rng', 'CRT_rand', 0x48c51d, 0x48c541),
    ('core', 'rng', 'CRT_srand', 0x48c541, 0x48c551),
    ('core', 'rng', 'CRT_thread_seed_pointer', 0x48c513, 0x48c51d),
    ('core', 'rng', 'CRT_thread_data_getter', 0x48e7c7, 0x48e7cd),
    ('core', 'world', 'SetUpdateChamp', 0x475328, 0x47534a),
    ('core', 'world', 'UpdateChamp', 0x478806, 0x478a01),
    ('core', 'world', 'ScanNouvellePatate', 0x478319, 0x478806),
    ('core', 'world', 'NextAnimVeget', 0x4772ec, 0x4774fa),
    ('core', 'world', 'NextAnimVegetFullMap', 0x4774fa, 0x477700),
    ('core', 'world', 'NextAnimTerrain', 0x477700, 0x47790d),
    ('core', 'shared_epilogue', 'SacCherchePlace_epilogue_0x475bf8', 0x475bf8, 0x475bfe),
    ('ai-runtime', 'wrapper', 'CalculNextReflect', 0x47fbea, 0x47fbfd),
    ('graphics', 'display', 'SetClipping', 0x40f519, 0x40f535),
    ('macos', 'ui_input', 'InitGameZone', 0x471830, 0x472047),
    ('macos', 'ui_input', 'MouseSetZone', 0x479c50, 0x479c9e),
    ('macos', 'ui_input', 'MouseTestZone', 0x479c9e, 0x479cac),
    ('ai-runtime', 'empty', 'PlayerAttaqueReset', 0x46d628, 0x46d629),
    ('ai-runtime', 'caller', 'CalculGame_load_and_frame_body', 0x42d1da, 0x42d4f5),
)
TABELA_ESTADOS = (0x42c804, 25)   # CalculGame state jump table, u32 entries
SEGUIDORES = ((0x45e944, 'CalculIconeAction'), (0x467718, 'CalculMatiere'),
              (0x46d629, 'PlayerAttaqueCalculSympa'), (0x4774fa, 'NextAnimVegetFullMap'))


def _secoes(raw):
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    for i in range(n):
        cab = pe+24+op+i*40
        rva, tamanho, offset = struct.unpack_from('<III', raw, cab+12)
        yield rva, tamanho, offset


def _bytes(raw, inicio, fim):
    rva = inicio - 0x400000
    for base, tamanho, offset in _secoes(raw):
        if offset and base <= rva and rva + fim-inicio <= base+tamanho:
            return raw[offset+rva-base:offset+rva-base+fim-inicio]
    raise ValueError(f'No original PE bytes at 0x{inicio:x}')


def extrair():
    import capstone
    from capstone import x86 as cx
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    simbolos = sorted((int(r['endereco'], 16), r['nome_original']) for r in
                      csv.DictReader((RAIZ / 'evidencias/simbolos-importados.tsv').open(), delimiter='\t'))
    enderecos = [s[0] for s in simbolos]

    def rotina(a):
        i = bisect.bisect_right(enderecos, a)-1
        return simbolos[i][1]

    def simbolo(a):
        i = bisect.bisect_right(enderecos, a)-1
        return simbolos[i][1] if simbolos[i][0] == a else f'{simbolos[i][1]}+0x{a-simbolos[i][0]:x}'

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    PASTA.mkdir(parents=True, exist_ok=True)
    trechos, escritos = [], set()
    for dono, papel, nome, inicio, fim in TRECHOS:
        bruto = _bytes(raw, inicio, fim)
        ins = list(md.disasm(bruto, inicio))
        if sum(i.size for i in ins) != len(bruto):
            raise ValueError(f'{nome}: interval does not decode to instruction boundaries')
        lidos, gravados, grades, chamadas, saltos_externos = set(), set(), set(), [], set()
        for i in ins:
            for o in i.operands:
                if o.type == cx.X86_OP_MEM and o.mem.base == 0 and o.mem.index == 0 and o.mem.segment in (0, cx.X86_REG_CS):
                    alvo = o.mem.disp & 0xffffffff
                    if not (CODIGO[0] <= alvo < CODIGO[1]):
                        texto = f'0x{alvo:06x}/{o.size}'
                        if o.access & capstone.CS_AC_READ:
                            lidos.add(texto)
                        if o.access & capstone.CS_AC_WRITE:
                            gravados.add(texto)
                            escritos.add(alvo)
                        if alvo in GRADES:
                            grades.add(GRADES[alvo])
                elif o.type == cx.X86_OP_MEM and o.mem.base == 0 and o.mem.disp and o.mem.index:
                    lidos.add(f'0x{o.mem.disp & 0xffffffff:06x}+index/{o.size}')
            if i.mnemonic == 'call':
                chamadas.append(dict(site=hex(i.address), target=(simbolo(int(i.op_str, 16)) if i.op_str.startswith('0x')
                                                                 else i.op_str)))
            if i.mnemonic.startswith('j') and i.op_str.startswith('0x'):
                alvo = int(i.op_str, 16)
                if not inicio <= alvo < fim:
                    saltos_externos.add(simbolo(alvo) + f' (0x{alvo:x})')
        asm = PASTA / f'{inicio:08x}.asm'
        asm.write_text(''.join(f'{i.address:08x}  {i.bytes.hex():<20} {i.mnemonic} {i.op_str}\n' for i in ins))
        trechos.append(dict(owner=dono, role=papel, name=nome, start=hex(inicio), end_exclusive=hex(fim),
                            bytes=len(bruto), sha256=hashlib.sha256(bruto).hexdigest(), instructions=len(ins),
                            reads=sorted(lidos), writes=sorted(gravados), grids=sorted(grades), calls=chamadas,
                            external_jumps=sorted(saltos_externos), asm=asm.name))
    # Whole-code reference inventory of every written global and grid pointer.
    codigo = _bytes(raw, *CODIGO)
    referencias = {}
    for alvo in sorted(escritos | set(GRADES) | {0x4e1c18, 0x4e1d18, 0x508724, 0x508726, 0x508720, 0x508722,
                                                  0x4e0730, 0x4e2f28, 0x4973ea, 0x522244}):
        rotinas = sorted({rotina(CODIGO[0]+m.start()) for m in re.finditer(re.escape(struct.pack('<I', alvo)), codigo)})
        referencias[hex(alvo)] = rotinas
    tabela = struct.unpack(f'<{TABELA_ESTADOS[1]}I', _bytes(raw, TABELA_ESTADOS[0], TABELA_ESTADOS[0]+4*TABELA_ESTADOS[1]))
    seguidores = []
    for endereco, nome in SEGUIDORES:
        bruto = _bytes(raw, endereco, endereco+24)
        seguidores.append(dict(name=nome, entry=hex(endereco), sha256_first_24=hashlib.sha256(bruto).hexdigest(),
                               first=[f'{i.mnemonic} {i.op_str}' for i in md.disasm(bruto, endereco)][:8]))
    manifesto = dict(original_sha256=HASH, capstone=capstone.__version__, scope='static only; no execution',
                     intervals=trechos, grid_pointers={hex(k): v for k, v in GRADES.items()},
                     code_references=referencias,
                     calculgame_state_table=dict(address=hex(TABELA_ESTADOS[0]),
                                                 entries=[dict(state=i, target=simbolo(v)) for i, v in enumerate(tabela)]),
                     next_callee_entries=seguidores)
    (PASTA / 'manifesto.json').write_text(json.dumps(manifesto, indent=1, ensure_ascii=False) + '\n')
    return manifesto


if __name__ == '__main__':
    m = extrair()
    print(json.dumps(dict(intervals=len(m['intervals']), files=len(list(PASTA.glob('*.asm')))), indent=1))
