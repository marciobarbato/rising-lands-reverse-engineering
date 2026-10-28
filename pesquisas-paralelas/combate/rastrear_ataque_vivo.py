"""Export the attack-state branch, its declared fragments and the +0x8A writer trace.

Reads the intact executable and the committed field audit only. Writes
`evidencias/ataque-vivo.json` and `evidencias/ataque-vivo.asm`.
"""
import bisect
import hashlib
import json
import struct
from pathlib import Path

from extrair_evidencias import HASH, ler_imagem, Cs, CS_ARCH_X86, CS_MODE_32

PASTA = Path(__file__).resolve().parent
REPO = PASTA.parents[1]
NORMALIZADO = '26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0'
BASE, TEXTO = 0x400000, (0x401000, 0x493c00)
TABELA_ESTADOS = 0x4543c8
TRECHOS = {
    'EnginNextEtape_ramo_ataque': (0x45673b, 0x4568ad),
    'EnginNextEtape_saida': (0x454ccd, 0x454cd5),
    'EnginNextEtape_prelude_recarga': (0x45442c, 0x454591),
    'SetAttaqueEngin': (0x445a36, 0x445af1),
    'PlayerGetType': (0x46d817, 0x46d838),
    'PlayerEstAllie': (0x46d838, 0x46d877),
    'PlayerAAttaqueSet': (0x46d600, 0x46d629),
    'BatimentEnDestruction': (0x41a70b, 0x41a735),
    'BatimentGetPlayer': (0x41a08c, 0x41a0ab),
}
RAMO_ESPERADO_FIM = [('mov', 'al, byte ptr [esi + 0xb7]'), ('cmp', 'al, 1'), ('jb', '0x45689e'),
    ('jbe', '0x4567ce'), ('cmp', 'al, 3'), ('je', '0x45673b'), ('xor', 'eax, eax'),
    ('mov', 'ax, di'), ('call', '0x451914'), ('jmp', '0x454ccd')]
ESCRITORES_8A = {0x445a05: 0, 0x445ab3: 0, 0x445ad1: 0, 0x451e08: 1,
                 0x452a3a: 0, 0x452af6: 1, 0x452b6c: 0, 0x4531fe: 0}


def simbolos():
    tabela = []
    for linha in (REPO / 'relatorios/simbolos-originais.tsv').read_text().splitlines():
        partes = linha.split('\t')
        try:
            tabela.append((int(partes[0], 16), partes[1].strip()))
        except (ValueError, IndexError):
            continue
    tabela.sort()
    inicios = [a for a, _ in tabela]

    def nome(endereco):
        i = bisect.bisect_right(inicios, endereco) - 1
        return f'{tabela[i][1]}+{endereco - tabela[i][0]:#x}'
    return nome, sorted({a for a in inicios if TEXTO[0] <= a < TEXTO[1]} | set(TEXTO))


def varrer(imagem, limites):
    """Symbol-restarted linear sweep with skipdata, as in the earlier field audit."""
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    cs.skipdata = True
    for a, z in zip(limites, limites[1:]):
        for i in cs.disasm(bytes(imagem[a - BASE:z - BASE]), a):
            if i.id:
                yield i


def chamadores(imagem, alvo):
    codigo = bytes(imagem[TEXTO[0] - BASE:TEXTO[1] - BASE])
    return [TEXTO[0] + k for k in range(len(codigo) - 4) if codigo[k] in (0xe8, 0xe9)
            and (TEXTO[0] + k + 5 + struct.unpack_from('<i', codigo, k + 1)[0]) & 0xffffffff == alvo]


def main():
    imagem = ler_imagem()
    nome, limites = simbolos()
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    linhas, trechos = [f'; Stage 18 attack branch and declared fragments; original SHA-256 {HASH}'], {}
    for rotulo, (inicio, fim) in TRECHOS.items():
        dados = bytes(imagem[inicio - BASE:fim - BASE])
        ins = list(cs.disasm(dados, inicio))
        assert ins[-1].address + ins[-1].size == fim, rotulo
        linhas.append(f'; {rotulo} [{inicio:#x},{fim:#x})')
        linhas += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}' for i in ins]
        trechos[rotulo] = dict(inicio=hex(inicio), fim_exclusivo=hex(fim), sha256_bytes=hashlib.sha256(dados).hexdigest(),
                               chamadas=[i.op_str for i in ins if i.mnemonic == 'call'])
    (PASTA / 'evidencias/ataque-vivo.asm').write_text('\n'.join(linhas) + '\n')
    ramo = list(cs.disasm(bytes(imagem[0x456886 - BASE:0x4568ad - BASE]), 0x456886))
    assert [(i.mnemonic, i.op_str) for i in ramo] == RAMO_ESPERADO_FIM
    pilha = [f'{i.address:08x} {i.op_str}' for i in cs.disasm(bytes(imagem[0x45673b - BASE:0x4568ad - BASE]), 0x45673b)
             if 'esp' in i.op_str or 'ebp' in i.op_str]
    assert pilha == []

    tabela = struct.unpack_from('<25I', imagem, TABELA_ESTADOS - BASE)
    assert tabela[1] == tabela[24] == 0x456886 and tabela.count(0x456886) == 2

    # +0x8A trace. 1) committed direct-writer audit, rechecked against the bytes.
    auditoria = json.loads((PASTA / 'evidencias/rastreio-campos.json').read_text())['codigo']
    unidades = [c for c in auditoria['candidatos_escrita'] if '0x8a' in c['campos'] and c['classificacao'] == 'registro de unidade']
    assert {int(c['endereco'], 16) for c in unidades} == set(ESCRITORES_8A)
    # 2) The only non-immediate unit writer stores AH; enumerate every branch to it.
    instrucoes = list(varrer(imagem, limites))
    para_ah = [i for i in instrucoes if i.mnemonic.startswith('j') and i.op_str == '0x452a3a']
    antes = next(i for i in instrucoes if i.address + i.size == 0x452a3a)
    origem = list(cs.disasm(bytes(imagem[0x452461 - BASE:0x45246f - BASE]), 0x452461))
    assert [(i.address, i.mnemonic) for i in para_ah] == [(0x452469, 'je')]
    assert antes.mnemonic == 'jmp' and [(i.mnemonic, i.op_str) for i in origem] == [
        ('mov', 'ah, byte ptr [esi + 0x8b]'), ('test', 'ah, ah'), ('je', '0x452a3a')]
    # 3) By-byte dword candidates in hangar code are word stores after a 66 prefix.
    hangar = []
    for c in auditoria['candidatos_8a_por_byte']:
        a = int(c['endereco'], 16)
        if not c['fronteira_na_primeira_passagem'] and imagem[a - 1 - BASE] == 0x66:
            i = next(cs.disasm(bytes(imagem[a - 1 - BASE:a + 15 - BASE]), a - 1, 1))
            ia = c['simbolo'] == 'iagRessReset'
            hangar.append(dict(endereco_auditoria=hex(a), simbolo=c['simbolo'], decodificacao_real=f'{i.mnemonic} {i.op_str}',
                               objeto='AI resource record loop (ebp+2k+0x8a)' if ia else 'structure/hangar record word +0x88'))
            assert i.mnemonic == 'mov' and i.op_str.startswith('word ptr') and ('+ 0x8a]' if ia else '+ 0x88]') in i.op_str
    # 4) Block operations and file loaders that can write whole records.
    blocos = [dict(endereco=hex(i.address), simbolo=nome(i.address), instrucao=f'{i.mnemonic} {i.op_str}')
              for i in instrucoes if i.mnemonic.startswith('rep') and ('movs' in i.mnemonic + i.op_str or 'stos' in i.mnemonic + i.op_str)]
    # Market/player/network/graphics routines only; none is a unit-record routine.
    assert not any('Engin' in b['simbolo'] for b in blocos)
    def rotinas(alvo):
        return sorted({nome(a).split('+')[0] for a in chamadores(imagem, alvo)})

    relatorio = dict(
        sha256_original=HASH, sha256_pe_normalizado_somente_analise=NORMALIZADO,
        tabela_estados=dict(endereco=hex(TABELA_ESTADOS), entradas=[hex(x) for x in tabela],
                            sha256_bytes=hashlib.sha256(bytes(imagem[TABELA_ESTADOS - BASE:TABELA_ESTADOS - BASE + 100])).hexdigest(),
                            estados_ramo_ataque=[1, 24]),
        trechos=trechos,
        ramo=dict(entrada='0x456886', registradores='ESI = unit record, DI = u16 unit index; no esp/ebp access in [0x45673b,0x4568ad)',
                  modo_alvo='+0xB7: 1 -> 0x4567ce, 3 -> 0x45673b, other -> CalculAttaqueEngin 0x451914(eax=u16 unit)',
                  invalido='PlayerGetType(owner)==2 -> iagUnitSendMessage(unit, dl=0x4a, ebx=0); else SetDeplaceEngin(unit, u16 +0x7e) then u16 +0xb8=0xffff',
                  saida='0x454ccd: add esp,0x64; jmp epilogue 0x44f29d', chamadores_CalculAttaqueEngin=[hex(a) for a in chamadores(imagem, 0x451914)]),
        rastreio_8a=dict(
            escritores_diretos_unidade=[dict(endereco=hex(a), simbolo=nome(a), valor=v) for a, v in ESCRITORES_8A.items()],
            prova_ah_0x452a3a=dict(unico_desvio='0x452469 je', instrucao_anterior=f'{antes.address:#x} {antes.mnemonic} {antes.op_str}',
                                   origem=[f'{i.address:#x} {i.mnemonic} {i.op_str}' for i in origem], valor=0),
            falsos_positivos_hangar=hangar,
            operacoes_bloco_rep=blocos,
            chamadores_memset=rotinas(0x48c3b0),
            chamadores_fileread=rotinas(0x458461),
            conclusao=('Every executable writer of a unit +0x8A stores 0 or 1. 2/3 can enter only through FileRead loaders '
                       '(mission ETA, saved games, other loaders) of external bytes. No rep movs/stos occurs in a unit routine; '
                       'the generic memset callers that allocate or reset tables (Load on open failure, calloc) fill with zero. '
                       'Network/multiplayer receive buffers and arbitrary pointer aliasing are not proven by this static trace.')),
    )
    destino = PASTA / 'evidencias/ataque-vivo.json'
    destino.write_text(json.dumps(relatorio, indent=1, ensure_ascii=False) + '\n')
    print(destino)


if __name__ == '__main__':
    main()
