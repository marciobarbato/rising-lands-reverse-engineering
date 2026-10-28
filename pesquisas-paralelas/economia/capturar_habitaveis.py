"""Stage 15 original-byte inventory: MissionPlaceTerrain structure habitation.

Exports intact intervals, jump tables and the static structure-type table
(names at +0x13) with hashes. Writes only economy-owned evidence files.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RAIZ.parent/'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH

HASH_ANALISE = '26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0'
# (start, exclusive end, original SBL symbol, role). Data tables are listed separately.
CODIGO = (
    (0x46c16d, 0x46c1b8, 'MissionPlaceTerrain', 'Structure scan after the unit scan; caller order'),
    (0x46b6f5, 0x46b6f8, 'LoadVar', 'Shared pop edx/pop ebx/ret epilogue reached by the MissionPlaceTerrain scan exit 0x46c17d'),
    (0x41a5b8, 0x41a61c, 'BatimentEstHabiter', 'Caller predicate before BatimentHabitable'),
    (0x41cc70, 0x41cde0, 'BatimentHabitable', 'Complete body'),
    (0x41db1d, 0x41db24, 'BatimentEnleveUneTroupeHospi', 'Shared epilogue (inside this symbol) entered at 0x41db1d by BatimentHabitable and at 0x41db1e by BatimentGetCase'),
    (0x41c76c, 0x41cb9a, 'BatimentSetTechnologie', 'Complete technology-Bag producer'),
    (0x41aee2, 0x41aff8, 'BatimentGetCase', 'Pure footprint-centre query; EDX/EBX are not inputs'),
    (0x41ab5c, 0x41ac8b, 'BatimentCollision', 'Static masks; tables owned by core pegadas_estruturas'),
    (0x447148, 0x447197, 'BagInit', 'Bag reset'),
    (0x447483, 0x4474a6, 'BagPrend', 'Unchecked append'),
    (0x4471b8, 0x44724a, 'BagContient', 'Mode-1 type count used by the predicate'),
    (0x44724a, 0x4472d3, 'BagContientTroupe', 'Unit-type predicate (erratum: not BagVide)'),
    (0x44228e, 0x4422b0, 'TypeEnginEstRealisable', 'Byte table 0x4e1934 + 26*owner + type'),
    (0x42c3b0, 0x42c3b6, 'ReseauActif', 'Called by type 15; AL result discarded'),
    (0x474958, 0x474974, 'SortilegeEstRealisable', 'Type-6 branch'),
    (0x474991, 0x4749ad, 'SortilegeEstInvente', 'Type-6 branch'),
    (0x46769d, 0x4676e5, 'GetRessourceStock', 'Type-3 level recomputation'),
    (0x423355, 0x4233d8, 'BatimentCalculResource', 'Same level formula as the inline type-3 block'),
    (0x418af7, 0x418b15, 'BatimentGetTypeName', 'Returns 0x495d8c + type*52 + 0x13'),
    (0x419112, 0x4191c9, 'BatimentInitCave', 'Counts type 3 (CAVE) into warehouse word 0x4dfb2c'),
)
TABELAS = (
    (0x41cc18, 22, 'BatimentHabitable radius jump table, types 0..21'),
    (0x41ab04, 22, 'BatimentCollision mask jump table, types 0..21'),
    (0x44719c, 7, 'BagContient tag jump table, tags 0..6'),
)
RAIOS = {0x41cd71: 20, 0x41cd78: 10, 0x41cd7f: 8, 0x41cd86: 4, 0x41cd8d: 5, 0x41cd94: 7}


def main():
    dados = (RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Original executable hash mismatch')
    catalogo = json.loads((RAIZ/'relatorios/simbolos-originais.json').read_text())
    sbl = (RAIZ.parent/'source/cd/INSTALHD/RISING.SBL').read_bytes()
    if hashlib.sha256(sbl).hexdigest() != catalogo['sha256_sbl']:
        raise ValueError('Original SBL hash mismatch')
    nomes = {}
    for s in catalogo['simbolos']:
        nomes.setdefault(int(s['endereco'], 16), []).append(s['nome_original'])
    pe = pefile.PE(data=dados)
    imagem, base = pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    capturas = []
    for inicio, fim, simbolo, papel in CODIGO:
        dono = max(a for a in nomes if a <= inicio)
        if simbolo not in nomes[dono]:
            raise ValueError(f'Unexpected original symbol at 0x{inicio:x}: {nomes[dono]}')
        codigo = imagem[inicio-base:fim-base]
        arquivo = f'habitaveis-{inicio:08x}.asm'
        linhas = [f'; {simbolo}: {papel}; exclusive end 0x{fim:08x}.', f'; Original EXE SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo, inicio)]
        (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
        capturas.append(dict(start=hex(inicio), end_exclusive=hex(fim), symbol=simbolo, role=papel,
                             bytes_hex=codigo.hex(), sha256=hashlib.sha256(codigo).hexdigest(), listing=arquivo))
    tabelas = []
    for inicio, quantidade, papel in TABELAS:
        bruto = imagem[inicio-base:inicio-base+4*quantidade]
        tabelas.append(dict(start=hex(inicio), entries=[hex(v) for v in struct.unpack(f'<{quantidade}I', bruto)],
                            role=papel, sha256=hashlib.sha256(bruto).hexdigest()))
    alvos = struct.unpack('<22I', imagem[0x41cc18-base:0x41cc18-base+88])
    raios = [RAIOS.get(a) for a in alvos]
    tipos = imagem[0x495d8c-base:0x495d8c-base+22*52]
    registros = []
    for tipo in range(22):
        r = tipos[tipo*52:(tipo+1)*52]
        registros.append(dict(type=tipo, width=struct.unpack_from('<H', r, 0)[0],
                              height=struct.unpack_from('<H', r, 2)[0],
                              name=r[0x13:].split(b'\0')[0].decode('ascii'), record_hex=r.hex()))
    if registros[2]['name'] != 'SANCTUAIRE' or registros[3]['name'] != 'CAVE':
        raise ValueError('Unexpected structure-type names')
    referencias = []
    for rel in ('evidencias/manifesto.json', 'evidencias/limpeza-saida.json',
                'evidencias/limpeza-saida-symbol-erratum.json', '../../evidencias/colocacao-estruturas/manifesto.json',
                '../../evidencias/colocacao-saida/manifesto.json', '../../relatorios/simbolos-originais.json'):
        referencias.append(dict(path=rel, sha256=hashlib.sha256((PASTA/rel).read_bytes()).hexdigest()))
    r = dict(
        sha256_exe=HASH, sha256_analysis_pe_not_executed=HASH_ANALISE, sha256_sbl=catalogo['sha256_sbl'],
        scope='MissionPlaceTerrain structure habitation: BatimentEstHabiter predicate, BatimentHabitable with '
              'complete BatimentSetTechnologie and BatimentGetCase; core DecouvreTerrain/IllumineTerrain called directly',
        caller_order=['for AX/EDX index 0..999 ascending (u16 loop, exit 0x46c17d -> 0x46b6f5)',
                      'BatimentExiste 0x41a735 (AL)', 'PlaceBatiment 0x41c4ac (core)',
                      'BatimentEstHabiter 0x41a5b8 (AL)', 'if AL: BatimentHabitable 0x41cc70',
                      'BatimentModifyMap 0x419e97 AX=index EDX=1 (core), for every existing structure'],
        habitable_order=['BatimentSetTechnologie AL=owner +4 DL=type +8',
                         'types 17/9/12: word +0x84=200, return',
                         'type 4: word +0x78=0', 'type 3 and owner<4: inline BatimentCalculResource level',
                         'R = radius jump table (types >21 keep the inherited EDI)',
                         'BatimentGetCase AX=index (EDX=R, EBX=0 ignored and preserved)',
                         'DecouvreTerrain 0x476851 AX=cell DX=(R+3)&0xffff BL=owner +4',
                         'IllumineTerrain 0x476cb3 AX=cell DX=R BL=owner +4', 'word +0x84=200'],
        radius_by_type=raios, captures=capturas, jump_tables=tabelas,
        structure_type_table=dict(
            start='0x495d8c', stride=52, name_offset='0x13', accessor='BatimentGetTypeName 0x418af7',
            hover_callers=['InputGame 0x429ad1', 'InputGame 0x42c141'],
            sha256=hashlib.sha256(tipos).hexdigest(), records=registros),
        cave_identity=dict(
            conclusion='Structure type 3 is the original CAVE; type 2 is SANCTUAIRE. MONDE01 serializes one type-2 structure.',
            evidence=['0x495d8c type-name table: 2=SANCTUAIRE, 3=CAVE',
                      'BatimentInitCave 0x419112 copies byte 0x49a073+22*owner (type-3 count) to word 0x4dfb2c+6*owner',
                      'BatimentCalculResource 0x423355 and BatimentAjouteMatiere use that word as warehouse count',
                      'TEXTES.TXT building list (70->91) gives Armazém at position 3 and Santuário at 2; no code path '
                      'adding 70 to a structure type was found, so that list is corroborating, not decisive'],
            not_inferred='The PT-BR briefing wording and the mission objective evaluation (TestFinDeMission) are not used'),
        symbol_erratum=dict(address='0x44724a', original_symbol=nomes[0x44724a], informal_label_used_before='BagVide',
                            bagvide_actual_address='0x4470b9', effect='Naming only; Stage 9/14 code, bytes and behaviour unchanged'),
        core_calls=dict(DecouvreTerrain='0x476851', IllumineTerrain='0x476cb3', SetMiniMap='0x46a388',
                        gate='R+3 <= visao_movimento.RAIO_DESCOBERTA_MAXIMO_VALIDADO and R <= RAIO_LUZ_MAXIMO_VALIDADO '
                             '(fallback 10/8 while absent); owners 0..3 only'),
        committed_evidence=referencias)
    (PASTA/'evidencias/habitaveis.json').write_text(json.dumps(r, indent=2, ensure_ascii=False)+'\n')
    print('Captured', len(capturas), 'intervals,', len(tabelas), 'jump tables and the 22 structure-type records.')


if __name__ == '__main__':
    main()
