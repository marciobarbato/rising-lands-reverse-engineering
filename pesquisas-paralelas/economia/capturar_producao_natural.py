"""Stage 17 original-byte inventory: natural production start and dispatcher branch.

Exports the BatimentNextEtape prologue/switch and production branch,
InitRecruteTroupe's exit search RechercheDecalageSortie, TerrainEnCollision,
the empty-Bag cleanup tail after 0x42110c and BatimentLoadCaract (which INI
fields reach the structure-type table). Writes only economy evidence files.
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
from capturar_habitaveis import HASH_ANALISE

CODIGO = (
    (0x4268d4, 0x426918, 'BatimentNextEtape', 'Prologue and type switch (EDI = AX index, EBP frame)'),
    (0x426918, 0x42698d, 'BatimentNextEtape', 'Branch for types 1/2/13/16: inline BatimentEstHabiter, then CalculTroupe'),
    (0x4281c0, 0x4281c7, 'BatimentNextEtape', 'Shared branch exit into 0x41db1d'),
    (0x4283e2, 0x428691, 'InitRecruteTroupe', 'Recruitment start; exit search at 0x42863b'),
    (0x41d1d0, 0x41d2fc, 'RechercheDecalageSortie', 'CalculPosition, then radius-1 ring with TerrainEnCollision(cell, 1)'),
    (0x4761d4, 0x4761f1, 'TerrainEnCollision', '(byte [0x507da8]+AX & DL) != 0'),
    (0x4210f7, 0x4211f2, 'SortieTroupe', 'Empty-Bag cleanup: GetCase, EteintTerrain, deselect, owner 200, ModifyMap, reset, messages'),
    (0x45f19a, 0x45f1ae, 'ProcessInputGame', 'Player-input caller of InitRecruteTroupe'),
    (0x48073a, 0x48074e, 'V_BatimentRecruteUnite', 'AI-operation caller of InitRecruteTroupe'),
    (0x418c70, 0x418e95, 'BatimentLoadCaract', 'INI loader: TMPSCONSTRUCTION +4, COUTPATATE +0x0c, COUTROCHE +0x0e, NAME +0x13, DIVERS globals'),
)
TABELAS = ((0x426880, 21, 'BatimentNextEtape type-1 switch'), (0x41d178, 22, 'RechercheDecalageSortie type switch'),
           (0x420df4, 22, 'Cleanup radius switch (same mapping as BatimentHabitable)'))


def main():
    dados = (RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Original executable hash mismatch')
    catalogo = json.loads((RAIZ/'relatorios/simbolos-originais.json').read_text())
    if hashlib.sha256((RAIZ.parent/'source/cd/INSTALHD/RISING.SBL').read_bytes()).hexdigest() != catalogo['sha256_sbl']:
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
        arquivo = f'producao-natural-{inicio:08x}.asm'
        linhas = [f'; {simbolo}: {papel}; exclusive end 0x{fim:08x}.', f'; Original EXE SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo, inicio)]
        (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
        capturas.append(dict(start=hex(inicio), end_exclusive=hex(fim), symbol=simbolo, role=papel,
                             bytes_hex=codigo.hex(), sha256=hashlib.sha256(codigo).hexdigest(), listing=arquivo))
    tabelas = []
    for inicio, n, papel in TABELAS:
        bruto = imagem[inicio-base:inicio-base+4*n]
        tabelas.append(dict(start=hex(inicio), entries=[hex(v) for v in struct.unpack(f'<{n}I', bruto)],
                            role=papel, sha256=hashlib.sha256(bruto).hexdigest()))
    tipos = imagem[0x495d8c-base:0x495d8c-base+22*52]
    referencias = [dict(path=rel, sha256=hashlib.sha256((PASTA/rel).read_bytes()).hexdigest())
                   for rel in ('evidencias/limpeza-saida.json', 'evidencias/producao-limpa.json',
                               'evidencias/habitaveis.json', 'evidencias/cauda-carga.json',
                               '../../relatorios/simbolos-originais.json')]
    ini = (RAIZ.parent/'source/cd/INSTALHD/RISING.INI').read_bytes()
    r = dict(
        sha256_exe=HASH, sha256_analysis_pe_not_executed=HASH_ANALISE, sha256_sbl=catalogo['sha256_sbl'],
        sha256_ini=hashlib.sha256(ini).hexdigest(),
        scope='Natural production: InitRecruteTroupe exit search, BatimentNextEtape branch 0x426918, '
              'CalculTroupe chain and the empty-Bag cleanup continuation after 0x42110c',
        callers_of_init_recrute=['ProcessInputGame 0x45f1a9 (player input)', 'V_BatimentRecruteUnite 0x480749 (AI operation)'],
        dispatcher_branch=dict(types=[1, 2, 13, 16], entry='0x426918', exit='0x4281c0 (mov esp,ebp; jmp 0x41db1d)',
                               body='inline BatimentEstHabiter (identical predicate to 0x41a5b8), then CalculTroupe(AX) if AL'),
        recherche_decalage_sortie=dict(
            radius=1, base='CalculPosition 0x420698 (core) with AX index, BL 0',
            ring='dy -1..1 outer, dx -1..1 inner, skip (0,0), x+dx and y+dy within 0..255 (not map size)',
            test='TerrainEnCollision(cell, DL=1) false selects the cell; otherwise the CalculPosition cell',
            unreached_types='9/12/17 read uninitialised stack; InitRecruteTroupe only reaches recruiting types'),
        empty_cleanup_order=['BatimentGetCase 0x41aee2 (AX building, DX R ignored)',
                             'EteintTerrain 0x476e82 (AX cell, DX R, BL owner +4) — core',
                             'if word [0x495be0+2*owner] == building: store 0xffff', 'byte +4 = 200',
                             'BatimentModifyMap 0x419e97 (AX building, EDX 1) — core',
                             'inline reset 0x421153..0x4211c5 (same stores as core resetar_estrutura)',
                             'iagUnitSendMessage 0x4829c8 (AX unit, DL 0x46, EBX 0) — ai-runtime',
                             'iagVilleSendMessage 0x484808 (AX building, DL 3, EBX 0) — ai-runtime'],
        structure_type_table=dict(
            static_sha256=hashlib.sha256(tipos).hexdigest(),
            ini_loaded_fields='BatimentLoadCaract: +4 TMPSCONSTRUCTION (default 300), +0x0c COUTPATATE (5), '
                              '+0x0e COUTROCHE (5), +0x13 NAME (30-byte buffer, default the static name)',
            consumed_by_production='+0/+2 dimensions and +0x12 divisor are static; LOGEMENT is not a string in the EXE',
            runtime_names='[SANCTUAIRE] NAME=SANTUÁRIO and [CAVE] NAME=ARMAZÉM in RISING.INI'),
        captures=capturas, jump_tables=tabelas, committed_evidence=referencias)
    (PASTA/'evidencias/producao-natural.json').write_text(json.dumps(r, indent=2, ensure_ascii=False)+'\n')
    print('Captured', len(capturas), 'intervals and', len(tabelas), 'jump tables.')


if __name__ == '__main__':
    main()
