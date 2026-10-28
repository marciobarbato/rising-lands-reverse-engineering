"""Export intact discovery/light bodies and the reachable vision-sum inventory."""
import bisect
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
HASH_NORMALIZADO = '26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0'
TRECHOS = (('DecouvreCase', 0x47670a, 0x476851), ('DecouvreTerrain', 0x476851, 0x47693a),
           ('IllumineCase', 0x476968, 0x476adc), ('IllumineTerrain', 0x476cb3, 0x476e82),
           ('Distance', 0x47954c, 0x479555), ('SetMiniMap', 0x46a388, 0x46a70c),
           ('TerrainGetColor', 0x4765f4, 0x476647), ('PlayerGetColor', 0x46003b, 0x460051),
           ('TerrainEstDecouvert', 0x4766f0, 0x47670a), ('TerrainEstIllumine', 0x476951, 0x476968),
           ('PlaceEngin_vision_sums', 0x456feb, 0x457040),
           ('SetSortEngin_vision_sums', 0x446118, 0x446171),
           ('BatimentHabitable_vision_radii', 0x41cd5d, 0x41cdcf),
           ('BatimentGetCase_prologue', 0x41aee2, 0x41aee7), ('BatimentGetCase_tail', 0x41aff0, 0x41aff8),
           ('BatimentGetCase_shared_epilogue', 0x41db1e, 0x41db24))
ROTULOS_HABITABLE = {0x41cd71: 20, 0x41cd78: 10, 0x41cd7f: 8, 0x41cd86: 4, 0x41cd8d: 5, 0x41cd94: 7}
# Every instruction-level store whose destination covers unit +0xbb/+0xf5.
ESCRITORES = ((0x44fa98, 'EnginSetNewExperience', 0xf5), (0x44fbfa, 'EnginSetLevelExperience', 0xf5),
              (0x44fc9d, 'EnginSetLevelExperience', 0xf5), (0x457241, 'EnginResetType', 0xbb),
              (0x457908, 'EnginSetTypeCaract', 0xbb), (0x457d55, 'EnginSetType', 0xbb),
              (0x457f7b, 'CreerEngin', 0xf5), (0x46adeb, 'LoadEngin', 0xbb),
              (0x46ae46, 'LoadEngin', 0xf5))
GRAVACOES = ('mov', 'add', 'sub', 'or', 'and', 'xor', 'inc', 'dec', 'adc', 'sbb', 'neg', 'not',
             'shl', 'shr', 'sar', 'rol', 'ror', 'xchg', 'pop')


def _secoes(raw):
    pe = struct.unpack_from('<I', raw, 60)[0]
    n, op = (struct.unpack_from('<H', raw, pe+o)[0] for o in (6, 20))
    return [struct.unpack_from('<IIII', raw, pe+24+op+i*40+8) for i in range(n)]


def _bytes(raw, secoes, inicio, fim):
    rva = inicio - 0x400000
    for _, base, tamanho, offset in secoes:
        if offset and base <= rva and rva + fim-inicio <= base+tamanho:
            return raw[offset+rva-base:offset+rva-base+fim-inicio]
    raise ValueError('No original PE bytes at address')


def varrer_escritores(raw, secoes, capstone):
    """Displacement stores over every Ghidra-listed body; returns sorted addresses."""
    from capstone import x86 as X
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    corpos = [(int(r['endereco'], 16), int(r['tamanho_corpo']))
              for r in csv.DictReader(open(RAIZ/'evidencias/ghidra/funcoes.tsv'), delimiter='\t')]
    achados = []
    for inicio, tamanho in corpos:
        for i in md.disasm(_bytes(raw, secoes, inicio, inicio+tamanho), inicio):
            if not i.operands or i.mnemonic not in GRAVACOES:
                continue
            op = i.operands[0]
            if op.type != X.X86_OP_MEM or op.mem.base in (X.X86_REG_ESP, X.X86_REG_EBP):
                continue
            d = op.mem.disp & 0xffffffff
            if any(d <= alvo < d+op.size for alvo in (0xbb, 0xf5)):
                achados.append(i.address)
    return sorted(set(achados)), len(corpos)


def chamadores(raw, secoes):
    """Every E8 rel32 call to the discovery/light bodies in the intact image."""
    nomes = {}
    for linha in open(RAIZ/'evidencias/simbolos-importados.tsv', encoding='utf-8'):
        campos = linha.rstrip('\n').split('\t')
        if len(campos) >= 2 and len(campos[0]) == 8:
            try:
                nomes[int(campos[0], 16)] = campos[1]
            except ValueError:
                pass
    inicios = sorted(nomes)
    alvos = {0x476851: 'DecouvreTerrain', 0x476cb3: 'IllumineTerrain',
             0x47670a: 'DecouvreCase', 0x476968: 'IllumineCase'}
    achados = []
    for _, base, tamanho, offset in secoes:
        dados = raw[offset:offset+tamanho]
        for i in range(len(dados)-4):
            if dados[i] != 0xe8:
                continue
            origem = 0x400000+base+i
            alvo = (origem+5+struct.unpack_from('<i', dados, i+1)[0]) & 0xffffffff
            if alvo in alvos:
                j = bisect.bisect_right(inicios, origem)-1
                achados.append(dict(target=alvos[alvo], call=hex(origem),
                                    routine=f'{nomes[inicios[j]]}+0x{origem-inicios[j]:x}'))
    return sorted(achados, key=lambda c: (c['target'], int(c['call'], 16)))


def raios_habitable(raw, secoes):
    tabela = struct.unpack('<22I', _bytes(raw, secoes, 0x41cc18, 0x41cc18+88))
    raios = {}
    for tipo, destino in enumerate(tabela):
        if tipo in (9, 12, 17):
            continue  # 0x41ccae..0x41ccc3 leave before discovery
        raios[str(tipo)] = ROTULOS_HABITABLE[destino]
    return dict(jump_table='0x41cc18', table_sha256=hashlib.sha256(struct.pack('<22I', *tabela)).hexdigest(),
                radius_by_type=raios, skipped_types=[9, 12, 17],
                discovery_dx='(R+3)&0xffff; BatimentGetCase pushes/pops EDX', light_dx='R',
                owner='structure +4 byte in BL', inherited_edi_types='type byte > 21 (ja 0x41cd99)',
                maximum_discovery_dx=max(raios.values())+3, maximum_light_dx=max(raios.values()))


def inventario_dominio():
    from analisar import dependencias
    from regras import extrair_regras
    from formatos import ler_eta
    pefile, _ = dependencias()
    cd = RAIZ.parent / 'source/cd'
    raw = (cd/'INSTALHD/RISING.EXE').read_bytes()
    ini = (cd/'INSTALHD/RISING.INI').read_bytes()
    pe = pefile.PE(data=raw)
    regras = extrair_regras(pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase, ini)
    tipos = b''.join(bytes.fromhex(r['registro_memoria_hex']) for r in regras['unidades'])
    rayon = [struct.unpack_from('<H', tipos, t*50+0x2a)[0] for t in range(26)]
    mapas = []
    for arquivo in sorted((cd/'WORLD').glob('*.ETA')):
        dados = arquivo.read_bytes()
        bloco = next(b for b in ler_eta(dados)['blocos'] if b['nome'] == 'unidades')
        n, tamanho = struct.unpack_from('<HH', dados, bloco['offset'])
        p, somas = bloco['offset']+4, {}
        for _ in range(n):
            registro = dados[p+2:p+2+tamanho]
            p += 2+tamanho
            dono, tipo, estado = registro[0], registro[1], registro[2]
            # LoadEngin: owner fixups 0x46afdc/0x46b015, then BB=type low byte, F5=0.
            dono = 0 if tipo == 16 else 4 if 20 <= tipo <= 24 else dono
            if estado and dono not in (4, 200):
                soma = rayon[tipo] & 255
                somas[soma] = somas.get(soma, 0)+1
        mapas.append(dict(file=arquivo.name, sha256=hashlib.sha256(dados).hexdigest(), units=n,
                          normal_owner_placed_sums={str(k): v for k, v in sorted(somas.items())}))
    return dict(rising_ini_sha256=hashlib.sha256(ini).hexdigest(), type_rayon_u16=rayon,
                type_bb_values=sorted({v & 255 for v in rayon} | {5}), f5_values=[0, 1],
                maps=mapas, map_count=len(mapas),
                map_sum_values=sorted({int(k) for m in mapas for k in m['normal_owner_placed_sums']}))


def extrair():
    import capstone
    raw = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest() != HASH:
        raise ValueError('Original executable SHA-256 mismatch')
    secoes = _secoes(raw)
    pasta = RAIZ / 'evidencias/descoberta-terreno'
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
    achados, corpos = varrer_escritores(raw, secoes, capstone)
    if achados != [a for a, _, _ in ESCRITORES]:
        raise ValueError(f'Unexpected +bb/+f5 writer set: {[hex(a) for a in achados]}')
    escritores = []
    for endereco, nome, campo in ESCRITORES:
        i = next(md.disasm(_bytes(raw, secoes, endereco, endereco+16), endereco))
        escritores.append(dict(address=hex(endereco), routine=nome, field=hex(campo),
                               bytes=i.bytes.hex(), instruction=f'{i.mnemonic} {i.op_str}'))
    dominio = inventario_dominio()
    maximo = max(dominio['type_bb_values']) + max(dominio['f5_values'])
    habitable = raios_habitable(raw, secoes)
    manifesto = dict(original_sha256=HASH, normalized_analysis_sha256=HASH_NORMALIZADO,
                     capstone=capstone.__version__, intervals=trechos,
                     writers=escritores, writer_scan_bodies=corpos, domain=dominio,
                     reachable_vision_sum_max=maximo, structure_caller=habitable,
                     direct_radius_max=dict(discovery=max(maximo+2, habitable['maximum_discovery_dx']),
                                            light=max(maximo, habitable['maximum_light_dx'])),
                     callers=chamadores(raw, secoes),
                     callers_covered=['PlaceEngin+0x73/0x95', 'SetSortEngin+0x18a/0x1b0',
                                      'BatimentHabitable+0x149/0x15a'],
                     caller_arithmetic='Both callers zero AH, load u8 BB, add 2 in 32 bits, add u8 F5 and pass DX; '
                                       'light reloads both bytes and passes u16 BB+F5. No 8-bit wrap.',
                     scope='Instruction-level displacement stores inside the 1,339 Ghidra-listed bodies '
                           '(function list from the normalized analysis copy; bytes from the intact oracle). '
                           'LoadEngin bulk disk copies are overwritten by 0x46adeb/0x46ae46 for every unit '
                           'ExisteEngin admits; GameLoad and other block restores are outside this inventory.')
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, indent=2, ensure_ascii=False) + '\n')
    return manifesto


if __name__ == '__main__':
    m = extrair()
    print('Exported discovery intervals:', len(m['intervals']), 'writers:', len(m['writers']),
          'reachable sum max:', m['reachable_vision_sum_max'], 'map sums:', m['domain']['map_sum_values'],
          'direct radii:', m['direct_radius_max'], 'callers:', len(m['callers']))
