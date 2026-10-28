"""Stage 16 original-byte inventory: economy-owned MissionLoad initializer tails.

Exports both loader tails, EnginInitTechnologie with EnginSetTechnologie,
BatimentInitCave, PlayerRetrieve, MarcheResetAll and, for ownership only,
RechercheCalculNew. Writes only economy-owned evidence files.
"""
import hashlib
import json
from pathlib import Path
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
    (0x46c5a5, 0x46c5d8, 'MissionLoad', 'Tail: FileClose, MissionPlaceTerrain, then the six initializers'),
    (0x46c969, 0x46c99a, 'MissionLoadName', 'Tail: RechercheCalculNew replaces Engin_RetrieveExperimente/PlayerRetrieve'),
    (0x441459, 0x441470, 'EnginInitTechnologie', 'EnginSetTechnologie for DL owners 0..3'),
    (0x4411e1, 0x441459, 'EnginSetTechnologie', 'Unit-order Bags 7 (buildings), 14 and 8 of one owner'),
    (0x440d58, 0x440d5e, 'EnginGetVolume', 'Shared pop edi..ebx/ret epilogue of EnginSetTechnologie'),
    (0x418a93, 0x418ad3, 'TypeBatimentEstRealisable', 'Network flag excludes types 8/12; else byte 0x4dfad4+22*owner+type'),
    (0x42c3b0, 0x42c3b6, 'ReseauActif', 'Byte 0x4e0730'),
    (0x419112, 0x4191c9, 'BatimentInitCave', 'Per-owner active type counts 0x49a070, CAVE count to 0x4dfb2c, type 18 to 0x4dfb4c'),
    (0x41db1e, 0x41db24, 'BatimentEnleveUneTroupeHospi', 'Shared epilogue of BatimentInitCave'),
    (0x46df41, 0x46dfa0, 'PlayerRetrieve', 'Copies +6 and +0x0c..+0x13 of four 20-byte players from [0x5080ac] to [0x5080a8]'),
    (0x46dad6, 0x46dadb, 'PlayerInitAllianceCompteur', 'Shared pop esi..ebx/ret epilogue of PlayerRetrieve'),
    (0x46027c, 0x4602cd, 'MarcheResetAll', 'Seven stores per player, ascending'),
    (0x47150f, 0x4716fe, 'RechercheCalculNew', 'Inventory only (MissionLoadName tail); not reconstructed in Stage 16'),
    (0x4709f3, 0x4709f9, 'InventionLoadCaract', 'Shared epilogue of RechercheCalculNew'),
)


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
        arquivo = f'cauda-carga-{inicio:08x}.asm'
        linhas = [f'; {simbolo}: {papel}; exclusive end 0x{fim:08x}.', f'; Original EXE SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo, inicio)]
        (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
        capturas.append(dict(start=hex(inicio), end_exclusive=hex(fim), symbol=simbolo, role=papel,
                             bytes_hex=codigo.hex(), sha256=hashlib.sha256(codigo).hexdigest(), listing=arquivo))
    referencias = [dict(path=rel, sha256=hashlib.sha256((PASTA/rel).read_bytes()).hexdigest())
                   for rel in ('evidencias/habitaveis.json', 'evidencias/manifesto.json', 'evidencias/ciclo-mercado.json',
                               '../../relatorios/simbolos-originais.json')]
    r = dict(
        sha256_exe=HASH, sha256_analysis_pe_not_executed=HASH_ANALISE, sha256_sbl=catalogo['sha256_sbl'],
        scope='Economy-owned MissionLoad initializer tails; RechercheCalculNew inventoried for ownership only',
        mission_load_tail=['0x46c5aa MissionPlaceTerrain (missions)', '0x46c5af EnginInitTechnologie (economy)',
                           '0x46c5b4 BatimentInitCave (economy)', '0x46c5b9 Engin_RetrieveExperimente 0x441623 (core)',
                           '0x46c5be PlayerRetrieve (economy)', '0x46c5c3..0x46c5cc iaReset 0x47f36e AL=[esp+0x128] (ai-runtime)',
                           '0x46c5d1 MarcheResetAll (economy)', '0x46c5d6 AL=1'],
        mission_load_name_tail=['0x46c973 MissionPlaceTerrain', '0x46c978 EnginInitTechnologie', '0x46c97d BatimentInitCave',
                                '0x46c982 RechercheCalculNew 0x47150f (economy)', '0x46c987..0x46c98e iaReset AL=[0x496fe4]',
                                '0x46c993 MarcheResetAll', '0x46c998 AL=1'],
        engin_set_technologie=dict(
            order_table='[0x4e19b8] -> four owner pointers -> 26 unit-type Bags of 104 bytes',
            bags=['unit 7: inline reset, capacity 22; tag 3 value t for t 0..21 except 20 when TypeBatimentEstRealisable',
                  'unit 14: inline reset, capacity 1; tag 7 value 6',
                  'unit 8: inline reset, capacity 4; tag 2 values 0,1,2,3'],
            inline_reset='Same bytes as BagInit 0x447148: header, 30 values, 30 tags; +0x60..+0x65 kept'),
        recherche_calcul_new=dict(
            calls=['TechnologieReset 0x46b517', 'BonusReset 0x428e71', 'InventionSetEffet 0x470f98',
                   'MissionGetNum 0x46c11a (missions)'],
            copies='16 bytes per owner 0x508134 -> 0x5080f4 before the research loops',
            owner='economy (research/technology); reached only by MissionLoadName, not by MissionLoad/MONDE01'),
        captures=capturas, committed_evidence=referencias)
    (PASTA/'evidencias/cauda-carga.json').write_text(json.dumps(r, indent=2)+'\n')
    print('Captured', len(capturas), 'intervals for the economy load tails.')


if __name__ == '__main__':
    main()
