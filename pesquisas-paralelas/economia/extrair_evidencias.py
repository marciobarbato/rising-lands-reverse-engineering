"""Extrai bytes x86 do original; grava somente nesta pasta de pesquisa."""
import hashlib
import json
import struct
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
REPOSITORIO = PASTA.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(REPOSITORIO.parent / 'source/python'))
import capstone
import pefile

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
NOMES = (
    'GetRessourceRMI', 'GetRessource', 'GetRessourceStock', 'TestRessource',
    'CalculMatiere', 'AjouteMatiere', 'EnleveMatiere', 'SetMatiere',
    'BatimentRessourceNecessaire', 'TroupeRessourceNecessaire',
    'EnginGetRessource', 'BatimentGetRessource', 'LoadRessource',
    'LoadGameRessource', 'SauveRessource', 'I_CombienCouteUnite',
    'I_CombienCouteBatiment', 'B_TestStock', 'B_TestRessource',
    'iagRessGetPlayerWealth', 'B_TestMaxRocheDansStock',
    'BatimentAjouteMatiere', 'BatimentEnleveMatiere', 'StockPossible',
    'BatimentCalculResource', 'InitRecruteTroupe', 'GarageCalculCoutReparation',
    'BagAccepte', 'BatimentRetireColon', 'TerrainDeposeSac', 'CreerSac',
    'InitBatimentPlayer', 'BatimentInitCave', 'BatimentRecalculRessource',
    'BatimentAlloc', 'BatimentInitTechnologie', 'SacCherchePlace',
    'TerrainAccepteSac', 'SacGetCapacite',
    'Random',
    'InitBatimentNeutre',
    'BallonPrepareArrivee', 'BallonPrepareSortie', 'TypeEnginGetNb',
    'BagInit', 'BagContient', 'BagPrend', 'BagRetire',
    'TypeEnginGetBagOrdre',
    'TerrainDeposeMatiere', 'SortilegeResetRealisable', 'SortilegeSetTechnologie',
    'LoadMine', 'LoadMissionMine', 'MineGetIndice', 'MineSetWork', 'MineEndWork',
    'MineDetruire', 'MineGetCapacite', 'MineRetire', 'MineRecolte',
    'TerrainRetireMatiere', 'TerrainRecolte', 'TerrainEstChampi',
    'PatateAugmentable', 'NouvellePatate', 'ScanNouvellePatate',
    'SetUpdateChamp', 'UpdateChamp',
    'SortEnRecrutement', 'EnginEnRecrutement', 'GetStatusRecrute',
    'CalculStatusRecrute', 'CalculNovaRecrute', 'EnginGetTimeRecrute',
    'SortilegeGetTimeAprentissage', 'EnginGetVieMax',
    'ConstruitPerso', 'ConstruitSort', '__CHP', '__init_8087', '__init_80x87',
    'CalculTroupe', 'BatimentGetColons', 'BatimentGetType', 'BatimentGetCapacite',
    'BatimentSetTechnologie', 'SortilegeEstRealisable', 'SortilegeSetRealisable',
    'SortilegeEstInvente', 'SortilegeSetInvention', 'SortilegeResetTechnologie',
    'SortilegeInitTechnologie',
    'InitApprentissage', 'ApprentissageSortTerminer', 'SortilegeGetCoutApprentissage',
    'EvalueCoutProposition', 'GetNbRessource', 'PlayerGetType',
    'PlayerEstAllie', 'PlayerGetSympathie',
    'VideMatiere',
)
# O RET precede dados; não apresentá-los como instruções da função.
FINS_CONFIRMES = {0x41aace: 0x41ab04, 0x4283e2: 0x428691, 0x478806: 0x478a01,
                  0x423e65: 0x423eb2, 0x48c43e: 0x48c45b}
TRECHOS_AUXILIARES = {
    0x423025: ('epilogo_compartilhado_de_BatimentCalculResource', 0x42302d),
    0x41db1e: ('epilogo_compartilhado_de_BatimentInitCave', 0x41db24),
    0x440d58: ('epilogo_compartilhado_de_BallonPrepareArrivee', 0x440d5e),
    0x423eb2: ('corpo_compartilhado_de_CalculStatusRecrute', 0x423f83),
    0x41db1d: ('epilogo_compartilhado_de_CalculTroupe', 0x41db24),
    0x42399a: ('epilogo_compartilhado_de_InitApprentissage', 0x4239a0),
    0x4661d3: ('epilogo_compartilhado_de_EvalueCoutProposition', 0x4661da),
}
TRECHOS_CONTEXTO = {
    0x42bec6: ('InputGame_custos_e_comando_de_aprendizagem', 0x42bf92),
    0x45f246: ('ProcessInputGame_despacho_de_InitApprentissage', 0x45f257),
    0x45e1d6: ('IconeFillContenu_teste_de_custos_de_aprendizagem', 0x45e210),
    0x464bee: ('MatiereEstDemander_ordem_pecas_comida_pedra', 0x464c1a),
    0x4674b1: ('CalculMarcheProposition_comparacao_do_indicador', 0x4674c6),
}


def extrair():
    original = REPOSITORIO.parent / 'source/cd/INSTALHD/RISING.EXE'
    dados = original.read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Executável incompatível')
    pe = pefile.PE(data=dados)
    imagem = pe.get_memory_mapped_image()
    base = pe.OPTIONAL_HEADER.ImageBase
    catalogo = json.loads((REPOSITORIO / 'relatorios/simbolos-originais.json').read_text())
    sbl = (REPOSITORIO.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes()
    if hashlib.sha256(sbl).hexdigest() != catalogo['sha256_sbl']:
        raise ValueError('SBL incompatível com o catálogo de nomes')
    simbolos = catalogo['simbolos']
    limites = sorted({int(s['endereco'], 16) for s in simbolos})
    alvos = {int(s['endereco'], 16): s['nome_original'] for s in simbolos if s['nome_original'] in NOMES}
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    pasta = PASTA / 'evidencias'
    pasta.mkdir(exist_ok=True)
    exportacoes = dict(alvos)
    exportacoes.update({a: n for a, (n, _) in TRECHOS_AUXILIARES.items()})
    exportacoes.update({a: n for a, (n, _) in TRECHOS_CONTEXTO.items()})
    for inicio, nome in exportacoes.items():
        if inicio in TRECHOS_CONTEXTO:
            fim = TRECHOS_CONTEXTO[inicio][1]
            criterio = 'trecho de contexto; não é função independente nem execução até RET'
        elif inicio in TRECHOS_AUXILIARES:
            fim = TRECHOS_AUXILIARES[inicio][1]
            criterio = 'trecho auxiliar até RET; não é uma função independente'
        else:
            fim = FINS_CONFIRMES.get(inicio, next(a for a in limites if a > inicio))
            criterio = 'RET antes dos dados seguintes' if inicio in FINS_CONFIRMES else 'próximo símbolo SBL'
        linhas = [f'; {nome}: limite por {criterio}, fim exclusivo 0x{fim:08x}.',
                  f'; SHA-256 original: {HASH}', '; Gerado por Capstone; não é pseudocódigo nem prova de semântica.']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(imagem[inicio-base:fim-base], inicio)]
        (pasta / f'{inicio:08x}.asm').write_text('\n'.join(linhas) + '\n')
    # Chamadas diretas: varredura linear não cobre ponteiros/tabelas nem prova alcançabilidade.
    referencias = []
    md.skipdata = True
    for secao in pe.sections:
        if not secao.Characteristics & 0x20000000:
            continue
        for i in md.disasm(secao.get_data(), base + secao.VirtualAddress):
            if i.mnemonic not in ('call', 'jmp') or not i.op_str.startswith('0x'):
                continue
            alvo = int(i.op_str, 16)
            if alvo in alvos:
                dono = max((a for a in limites if a <= i.address), default=None)
                nomes = [s['nome_original'] for s in simbolos if int(s['endereco'], 16) == dono]
                referencias.append(dict(endereco=f'0x{i.address:08x}', instrucao=i.mnemonic,
                                        alvo=f'0x{alvo:08x}', nome=alvos[alvo],
                                        simbolo_anterior=nomes))
    tipos = []
    for tipo in (2, 3, 4, 6, 18, 20, 21):
        endereco = 0x495d8c + tipo * 52
        registro = imagem[endereco-base:endereco-base + 52]
        tipos.append(dict(id=tipo, endereco=f'0x{endereco:08x}',
                          nome_original=registro[19:49].split(b'\0')[0].decode('cp1252'),
                          registro_hex=registro.hex()))
    manifesto = dict(sha256_exe=HASH, sha256_sbl=catalogo['sha256_sbl'], capstone=capstone.__version__,
                     rotinas={f'0x{a:08x}': n for a, n in alvos.items()},
                     trechos_auxiliares={f'0x{a:08x}': dict(nome=n, fim_exclusivo=f'0x{fim:08x}')
                                         for a, (n, fim) in TRECHOS_AUXILIARES.items()},
                     trechos_contexto={f'0x{a:08x}': dict(nome=n, fim_exclusivo=f'0x{fim:08x}')
                                       for a, (n, fim) in TRECHOS_CONTEXTO.items()},
                     tipos_construcao_confirmados=tipos,
                     referencias_diretas_candidatas=referencias)
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n')
    parametros = dict(
        sha256_exe=HASH,
        controle_x87=dict(endereco='0x4993dc', valor=struct.unpack_from('<H', imagem, 0x4993dc-base)[0]),
        ajuste_hospital=dict(endereco='0x495be8', valor=imagem[0x495be8-base]),
        coeficientes=[dict(endereco=f'0x{a:08x}', valor=struct.unpack_from('<d', imagem, a-base)[0],
                           bytes_hex=imagem[a-base:a-base+8].hex())
                      for a in (0x4943e7, 0x4943ef, 0x494402, 0x49440a, 0x494432, 0x49443a)],
        tipos=[dict(id=t, endereco=f'0x{0x495d8c+t*52:08x}',
                    nome=imagem[0x495d8c+t*52+19-base:0x495d8c+t*52+49-base].split(b'\0')[0].decode('cp1252'),
                    divisor_bruto=imagem[0x495d8c+t*52+18-base],
                    registro_hex=imagem[0x495d8c+t*52-base:0x495d8c+(t+1)*52-base].hex())
               for t in range(22)],
        tipos_sortilegios=[dict(id=t, endereco=f'0x{0x497174+t*46:08x}',
                                nome=imagem[0x497174+t*46+12-base:0x497174+t*46+42-base].split(b'\0')[0].decode('cp1252'),
                                registro_hex=imagem[0x497174+t*46-base:0x497174+(t+1)*46-base].hex())
                           for t in range(5)])
    (pasta / 'parametros-producao.json').write_text(json.dumps(parametros, ensure_ascii=False, indent=2) + '\n')
    mercado = dict(sha256_exe=HASH,
                   origem='Valores estáticos da imagem PE; não são custos de recrutamento nem carga INI',
                   precos_unidades=dict(endereco='0x496fb0',
                                         bytes_hex=imagem[0x496fb0-base:0x496fca-base].hex()),
                   precos_recursos=dict(endereco='0x496fcc', ordem=['pecas', 'comida', 'pedra'],
                                        bytes_hex=imagem[0x496fcc-base:0x496fcf-base].hex()))
    (pasta / 'parametros-mercado.json').write_text(json.dumps(mercado, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(alvos)} rotinas, {len(TRECHOS_AUXILIARES)} trechos auxiliares, '
          f'{len(TRECHOS_CONTEXTO)} contextos e {len(referencias)} referências candidatas: {pasta}')


if __name__ == '__main__':
    extrair()
