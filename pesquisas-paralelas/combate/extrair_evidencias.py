"""Exporta bytes e assembly do EXE original; escreve apenas nesta pesquisa."""
import hashlib
import json
import struct
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
REPO = PASTA.parents[1]
sys.path.insert(0, str(REPO.parent / 'source/python'))
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
# Os fins vêm do próximo símbolo original ou de um limite explícito de trecho.
TRECHOS = {
    'EnginAPortee': (0x446cb5, 0x446eed),
    'EnginAPorteeMinimale': (0x446eed, 0x446fbf),
    'EnginEstEnnemi': (0x446fbf, 0x447021),
    'TypeEnginPeutAttaquer': (0x453d7d, 0x453da2),
    'EnginTrouveCibleScan': (0x453da2, 0x453f74),
    'EnginTrouveCible': (0x453f74, 0x454235),
    'EnginEstCharge': (0x45173f, 0x4517a2),
    'EnginRechargeArme': (0x4516d3, 0x45173f),
    'EnginLigneDeTir': (0x4517a2, 0x45189c),
    'CalculAttaqueEngin': (0x451914, 0x452c94),
    'SetAttaqueEngin': (0x445a36, 0x445af1),
    'ContactUnite': (0x4468e4, 0x446b0c),
    'ContactCellule': (0x446b0c, 0x446c94),
    'ContientCellule': (0x44246e, 0x442586),
    'PlayerEstAllie': (0x46d838, 0x46d877),
    'Distance2d': (0x479555, 0x4795af),
    'TypeCaseBloqueTir': (0x47653c, 0x47656b),
    'EpiloguePortee': (0x440f94, 0x440f9c),
    'EpilogueScan': (0x44f29a, 0x44f2a3),
    'EpilogueRegistres': (0x440d58, 0x440d5e),
    'EpilogueContact': (0x443468, 0x443470),
    'Modificateur': (0x428cc0, 0x428e71),
    'SortilegeGetPortee': (0x4746c9, 0x4746e4),
    'BatimentGetCase': (0x41aee2, 0x41aff8),
    'BatimentAdjacent': (0x42381f, 0x4239a0),
    'BatimentCollision': (0x41ab5c, 0x41ac8b),
    'EpilogueBatiment': (0x41db1e, 0x41db24),
    'EnginNextEtape_selection': (0x4546bc, 0x4547e0),
    'EnginNextEtape_validite': (0x45673b, 0x4568a8),
    'EnginViseCible': (0x451464, 0x4516d3),
    'AngleQuart': (0x479610, 0x4796cb),
    'AngleCalcul': (0x4796cb, 0x4798b0),
    'EpilogueMira': (0x44f33c, 0x44f344),
    'BatimentGetCaseAdjacent': (0x4239a0, 0x423b27),
    'RuntimeAcos': (0x48d5ce, 0x48d5f1),
    'RuntimeTruncar': (0x48c43e, 0x48c45b),
    'RuntimeAtan': (0x48fee7, 0x48fefc),
    'RuntimeRaiz': (0x48ff4a, 0x48ff7f),
    'AnimAttaqueEngin': (0x4479c4, 0x447acf),
    'AnimAttaqueTermineEngin': (0x447977, 0x4479b4),
    'ProjectileInit': (0x46e44c, 0x46e4ca),
    'ProjectileSet': (0x46e208, 0x46e422),
    'ProjectileLineaire': (0x46e049, 0x46e17f),
    'ProjectileReset': (0x46e00a, 0x46e02c),
    'ProjectileExiste': (0x46e02c, 0x46e049),
    'ProjectileGetLibre': (0x46e422, 0x46e44c),
    'ProjectileCalculLineaire': (0x46e4ca, 0x46e52c),
    'ProjectileAlloc': (0x46dfa0, 0x46dfb0),
    'LoadProjectile': (0x46dfba, 0x46dfe2),
    'SaveProjectile': (0x46dfe2, 0x46e00a),
    'SortilegeGetRayonEffet': (0x474734, 0x47474f),
    'DecouvreTerrain': (0x476851, 0x47693a),
    'IllumineTerrain': (0x476cb3, 0x476e82),
    'ProjectileAvance_contador_e_passo': (0x46ef66, 0x46f07c),
    'ProjectileCalcul': (0x46fc0f, 0x46fc8b),
    'ProjectileAnim': (0x46e52c, 0x46e5fe),
    'ProjectileInfligeDegat': (0x46e5fe, 0x46eaf8),
    'ProjectileAvance': (0x46eaf8, 0x46fc0f),
    'Random': (0x4704dc, 0x470520),
    'TypeEnginGetSortieProjectile': (0x4511a5, 0x4513c7),
    'AffCorpsEnginDecalage': (0x410fcc, 0x4110bf),
    'GiroTorre': (0x4484a7, 0x448599),
    'ChercheIndiceBatiment': (0x41b54a, 0x41b579),
    'InfligeDegat': (0x450874, 0x4510dd),
    'EpilogueCible': (0x4462aa, 0x4462b0),
    'EpilogueProjectile': (0x46fc09, 0x46fc0f),
    'EnginSetTypeCaract': (0x457350, 0x457b87),
    'EnginSetType': (0x457b87, 0x457e0c),
    'EpilogueCaracteristicas': (0x4570f0, 0x4570f4),
    'EnginTypeGetCapacite': (0x4475ac, 0x4475ef),
    'EpilogueCapacidade': (0x4474c5, 0x4474c7),
    'LoadEngin': (0x479d10, 0x479d7f),
    'SauveEngin': (0x479d7f, 0x479e12),
    'CreerEngin': (0x457e6c, 0x458088),
    'ResetOrdre': (0x44357c, 0x443688),
    'SetEnginLanceSortilege': (0x4459c4, 0x445a36),
    'EnginRestaureEtat_magia': (0x45315f, 0x453232),
    'EnginAlloc': (0x441a1b, 0x441ade),
    'MemAlloc': (0x467ea6, 0x467ecb),
    'LoadEngin_missao': (0x46acbf, 0x46b01e),
    'LoadEnginGame': (0x46b01e, 0x46b119),
    'SauveEngin_game': (0x46b119, 0x46b1fb),
    'ExisteEngin_EnginGetType': (0x441fff, 0x442045),
    'TypeEnginEstMonstre': (0x4422dd, 0x4422eb),
    'EpiloguePredicadoMonstre': (0x4422da, 0x4422dd),
}
DADOS = ((0x446aa4, 0x446b0c),)


def ler_imagem():
    """Imagem somente leitura; valida o hash antes de qualquer extração."""
    dados = (REPO.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('EXE incompatível')
    pe = struct.unpack_from('<I', dados, 0x3c)[0]
    n = struct.unpack_from('<H', dados, pe + 6)[0]
    opt = struct.unpack_from('<H', dados, pe + 20)[0]
    imagem = bytearray(0x200000)
    for i in range(n):
        cab = pe + 24 + opt + i * 40
        rva, tam, off = struct.unpack_from('<III', dados, cab + 12)
        if off and tam:
            imagem[rva:rva + tam] = dados[off:off + tam]
    return imagem


def main():
    imagem = ler_imagem()
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    saida = PASTA / 'evidencias'
    saida.mkdir(exist_ok=True)
    manifesto = {'sha256_original': HASH, 'trechos': [], 'constantes_mira': {}, 'despachos_ataque': {}}
    for endereco, n in ((0x4479b4, 4), (0x451904, 4), (0x45189c, 26)):
        valores = struct.unpack_from('<' + 'I' * n, imagem, endereco - 0x400000)
        manifesto['despachos_ataque'][f'0x{endereco:08x}'] = [f'0x{v:08x}' for v in valores]
    manifesto['despacho_caracteristicas'] = [f'0x{v:08x}' for v in
        struct.unpack_from('<26I', imagem, 0x4572e8 - 0x400000)]
    manifesto['despacho_projeteis'] = dict(endereco='0x0046e184', primeiro_tipo=1,
        destinos=[f'0x{v:08x}' for v in struct.unpack_from('<33I', imagem, 0x46e184 - 0x400000)])
    fontes_saidas = {2: (0x496af0, 8), 8: (0x496b10, 8), 18: (0x496b30, 8),
        23: (0x496b50, 8), 24: (0x496b70, 8), 21: (0x496b90, 8),
        22: (0x496bb0, 8), 15: (0x496bd0, 32), 12: (0x496c50, 32)}
    dados_disparo = dict(sha256_original=HASH, saidas={}, deslocamento_corpo=[])
    for tipo, (endereco, n) in fontes_saidas.items():
        pares = [struct.unpack_from('<hh', imagem, endereco - 0x400000 + i * 4) for i in range(n)]
        dados_disparo['saidas'][str(tipo)] = dict(endereco=f'0x{endereco:08x}', pares=pares)
    for i in range(26):
        entrada = struct.unpack_from('<I', imagem, 0x410f64 - 0x400000 + i * 4)[0]
        instrucoes = list(cs.disasm(bytes(imagem[entrada - 0x400000:entrada - 0x400000 + 14]), entrada))
        if instrucoes[0].mnemonic == 'ret':
            par = (0, 0)
        else:
            assert all(j.mnemonic == 'sub' for j in instrucoes[:2])
            par = tuple(-int(j.op_str.rsplit(', ', 1)[1], 0) for j in instrucoes[:2])
        dados_disparo['deslocamento_corpo'].append(par)
    (saida / 'dados-disparo.json').write_text(json.dumps(dados_disparo, ensure_ascii=False, indent=2) + '\n')
    for endereco in range(0x494e04, 0x494e2c, 8):
        valor = bytes(imagem[endereco - 0x400000:endereco - 0x400000 + 8])
        manifesto['constantes_mira'][f'0x{endereco:08x}'] = dict(bytes=valor.hex(), double=struct.unpack('<d', valor)[0])
    baixo = struct.unpack_from('<I', imagem, 0x479717 - 0x400000)[0]
    alto = struct.unpack_from('<I', imagem, 0x47971c - 0x400000)[0]
    valor = struct.pack('<II', baixo, alto)
    manifesto['constantes_mira']['pi_imediato'] = dict(bytes=valor.hex(), double=struct.unpack('<d', valor)[0],
        enderecos_imediatos=['0x00479717', '0x0047971c'])
    for nome, (inicio, fim) in TRECHOS.items():
        trecho = bytes(imagem[inicio - 0x400000:fim - 0x400000])
        linhas = [f'; {nome}; intervalo [0x{inicio:08x}, 0x{fim:08x})',
                  f'; EXE original SHA-256: {HASH}']
        cursor = inicio
        for da, db in (*[p for p in DADOS if inicio <= p[0] < fim], (fim, fim)):
            code = bytes(imagem[cursor - 0x400000:da - 0x400000])
            linhas += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}'.rstrip()
                       for i in cs.disasm(code, cursor)]
            for endereco in range(da, db, 4):
                valor = struct.unpack_from('<I', imagem, endereco - 0x400000)[0]
                linhas.append(f'{endereco:08x}  {valor.to_bytes(4, "little").hex():24s} dd       0x{valor:08x} ; tabela de saltos')
            cursor = db
        arquivo = f'{inicio:08x}.asm'
        (saida / arquivo).write_text('\n'.join(linhas) + '\n', encoding='utf-8')
        manifesto['trechos'].append(dict(nome=nome, inicio=f'0x{inicio:08x}',
            fim_exclusivo=f'0x{fim:08x}', sha256_bytes=hashlib.sha256(trecho).hexdigest(),
            arquivo=arquivo))
    (saida / 'manifesto.json').write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(TRECHOS)} intervalos exportados do EXE original para {saida}')


if __name__ == '__main__':
    main()
