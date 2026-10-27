"""Extrai bytes x86 do original; grava somente nesta pasta de pesquisa."""
import hashlib
import json
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
)
# O RET precede dados; não apresentá-los como instruções da função.
FINS_CONFIRMES = {0x41aace: 0x41ab04, 0x4283e2: 0x428691}
TRECHOS_AUXILIARES = {
    0x423025: ('epilogo_compartilhado_de_BatimentCalculResource', 0x42302d),
    0x41db1e: ('epilogo_compartilhado_de_BatimentInitCave', 0x41db24),
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
    for inicio, nome in exportacoes.items():
        if inicio in TRECHOS_AUXILIARES:
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
    for tipo in (2, 3, 4, 18, 21):
        endereco = 0x495d8c + tipo * 52
        registro = imagem[endereco-base:endereco-base + 52]
        tipos.append(dict(id=tipo, endereco=f'0x{endereco:08x}',
                          nome_original=registro[19:49].split(b'\0')[0].decode('cp1252'),
                          registro_hex=registro.hex()))
    manifesto = dict(sha256_exe=HASH, sha256_sbl=catalogo['sha256_sbl'], capstone=capstone.__version__,
                     rotinas={f'0x{a:08x}': n for a, n in alvos.items()},
                     trechos_auxiliares={f'0x{a:08x}': dict(nome=n, fim_exclusivo=f'0x{fim:08x}')
                                         for a, (n, fim) in TRECHOS_AUXILIARES.items()},
                     tipos_construcao_confirmados=tipos,
                     referencias_diretas_candidatas=referencias)
    (pasta / 'manifesto.json').write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(alvos)} rotinas, {len(TRECHOS_AUXILIARES)} trechos auxiliares e {len(referencias)} referências candidatas: {pasta}')


if __name__ == '__main__':
    extrair()
