"""Export ProjectileReset bytes, its callers and the L2 combat-state inventory.

Reads the intact executable only. Writes `evidencias/reinicio-projeteis.json`
and the caller-context listings; never reads the Python reconstruction.
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
ROTINA = (0x46e00a, 0x46e02c)
# Caller contexts: reset prefixes and the two other entries, ending after the next call.
CONTEXTOS = {
    'MissionLoad': (0x46c34c, 0x46c382),
    'MissionLoadName': (0x46c5f5, 0x46c62d),
    'MissionReStart': (0x46b57f, 0x46b5b8),
    'GameLoad': (0x46b895, 0x46b8cb),
}
# Combat runtime globals observed by the committed combat modules.
GLOBAIS = {
    0x5080f0: 'projectile pool pointer (dword)',
    0x4e19c0: 'last local alert counter (dword)',
    0x496acc: 'last local alert cell (dword store, u16 consumer)',
    0x4dfb44: 'impact presentation displacement input',
}
ESPERADO = [
    ('push', 'ebx'), ('push', 'edx'), ('xor', 'eax, eax'), ('jmp', '0x46e01f'),
    ('imul', 'ebx, edx, 0x38'), ('mov', 'edx, dword ptr [0x5080f0]'), ('inc', 'eax'),
    ('mov', 'byte ptr [edx + ebx + 2], 0'), ('xor', 'edx, edx'), ('mov', 'dx, ax'),
    ('cmp', 'edx, 0x64'), ('jl', '0x46e010'), ('pop', 'edx'), ('pop', 'ebx'), ('ret', ''),
]
LEITURA = {'cmp', 'test', 'push', 'bt'}


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
    return nome


def listar(cs, imagem, inicio, fim):
    return list(cs.disasm(bytes(imagem[inicio - BASE:fim - BASE]), inicio))


def chamadas_diretas(imagem, alvo):
    codigo = bytes(imagem[TEXTO[0] - BASE:TEXTO[1] - BASE])
    achados = []
    for k in range(len(codigo) - 4):
        if codigo[k] in (0xe8, 0xe9):
            va = TEXTO[0] + k
            if (va + 5 + struct.unpack_from('<i', codigo, k + 1)[0]) & 0xffffffff == alvo:
                achados.append((va, 'call' if codigo[k] == 0xe8 else 'jmp'))
    return achados


def referencias(cs, imagem, alvo, nome):
    """Every decoded instruction whose memory operand displacement is `alvo`."""
    cs.detail = True
    codigo = bytes(imagem[TEXTO[0] - BASE:TEXTO[1] - BASE])
    padrao, pos, vistos, saida = struct.pack('<I', alvo), 0, set(), []
    while (k := codigo.find(padrao, pos)) >= 0:
        pos = k + 1
        for recuo in range(1, 9):
            inicio = k - recuo
            ins = next(cs.disasm(codigo[inicio:inicio + 16], TEXTO[0] + inicio, 1), None)
            if ins is None or ins.address + ins.size < TEXTO[0] + k + 4:
                continue
            ops = [o for o in ins.operands if o.type == 3 and o.mem.disp & 0xffffffff == alvo]
            if ops and ins.address not in vistos:
                vistos.add(ins.address)
                escreve = ins.operands[0].type == 3 and ins.mnemonic not in LEITURA
                saida.append(dict(endereco=hex(ins.address), rotina=nome(ins.address),
                                  instrucao=f'{ins.mnemonic} {ins.op_str}',
                                  acesso='write' if escreve else 'read'))
                break
    cs.detail = False
    return saida


def main():
    imagem = ler_imagem()
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    nome = simbolos()
    saida = PASTA / 'evidencias'

    corpo = bytes(imagem[ROTINA[0] - BASE:ROTINA[1] - BASE])
    instrucoes = listar(cs, imagem, *ROTINA)
    assert [(i.mnemonic, i.op_str) for i in instrucoes] == ESPERADO

    chamadores = chamadas_diretas(imagem, ROTINA[0])
    assert [a for a, _ in chamadores] == [0x46b5ac, 0x46b8c1, 0x46c373, 0x46c623]
    assert all(t == 'call' for _, t in chamadores)
    ponteiros = [hex(BASE + k) for k in range(len(imagem) - 3)
                 if imagem[k:k + 4] == struct.pack('<I', ROTINA[0])]

    contextos, linhas = {}, []
    for rotulo, (inicio, fim) in CONTEXTOS.items():
        dados = bytes(imagem[inicio - BASE:fim - BASE])
        ins = listar(cs, imagem, inicio, fim)
        assert ins[-1].address + ins[-1].size == fim
        linhas.append(f'; {rotulo} context [{inicio:#x},{fim:#x}); original SHA-256 {HASH}')
        linhas += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}' for i in ins]
        contextos[rotulo] = dict(inicio=hex(inicio), fim_exclusivo=hex(fim), sha256_bytes=hashlib.sha256(dados).hexdigest(),
            chamadas=[dict(endereco=hex(i.address), alvo=i.op_str, rotina=nome(int(i.op_str, 16)).split('+')[0])
                      for i in ins if i.mnemonic == 'call'])
    (saida / 'reinicio-projeteis-chamadores.asm').write_text('\n'.join(linhas) + '\n')

    alocacao = bytes(imagem[0x46dfa0 - BASE:0x46dfb0 - BASE])
    assert [(i.mnemonic, i.op_str) for i in listar(cs, imagem, 0x46dfa0, 0x46dfb0)] == [
        ('mov', 'eax, 0x15e0'), ('call', '0x467ea6'), ('mov', 'dword ptr [0x5080f0], eax'), ('ret', '')]

    reset_unidades = [dict(endereco=hex(i.address), instrucao=f'{i.mnemonic} {i.op_str}')
                      for i in listar(cs, imagem, 0x441659, 0x441775)
                      if i.mnemonic == 'mov' and i.op_str.split(',')[0].endswith(']')]

    relatorio = dict(
        sha256_original=HASH,
        sha256_pe_normalizado_somente_analise=NORMALIZADO,
        identidade='All bytes and addresses come from the intact executable; the normalized PE is named only as the analysis identity and is not read here.',
        rotina=dict(nome='ProjectileReset', inicio=hex(ROTINA[0]), fim_exclusivo=hex(ROTINA[1]), tamanho=len(corpo),
            sha256_bytes=hashlib.sha256(corpo).hexdigest(), bytes_hex=corpo.hex(), arquivo='0046e00a.asm',
            instrucoes=[f'{i.address:08x} {i.mnemonic} {i.op_str}'.strip() for i in instrucoes]),
        contrato=dict(
            entradas='None: EAX/EBX/ECX/EDX/ESI/EDI/EBP and stack arguments are not read; dword [0x5080f0] is reread before every store',
            stores=[dict(ordem=i + 1, endereco=f'[0x5080f0]+{i * 56 + 2:#x}', largura='u8', valor=0) for i in range(100)],
            outros_bytes='The other 55 bytes of every 56-byte record and every global are not written',
            pilha='push ebx; push edx scratch at [entry_esp-4],[entry_esp-8]; restored by pop; plain ret',
            retorno='EAX=0x64; EBX/EDX restored; ECX/ESI/EDI/EBP untouched; flags from final cmp edx(0x64),0x64',
            chamadas=[], dominio='The pool pointer must address 5600 mapped writable bytes; ProjectileAlloc 0x46dfa0 provides it once at ProgInit'),
        chamadores=[dict(endereco=hex(a), rotina=nome(a), retorno=hex(a + 5)) for a, _ in chamadores],
        ponteiros_absolutos_para_rotina=ponteiros,
        contextos=contextos,
        alocacao_pool=dict(rotina='ProjectileAlloc', inicio='0x46dfa0', fim_exclusivo='0x46dfb0',
            sha256_bytes=hashlib.sha256(alocacao).hexdigest(), bytes_hex=alocacao.hex(), tamanho_bytes=0x15e0,
            chamadores=[dict(endereco=hex(a), rotina=nome(a)) for a, _ in chamadas_diretas(imagem, 0x46dfa0)],
            liberacao=[dict(endereco=hex(a), rotina=nome(a)) for a, _ in chamadas_diretas(imagem, 0x46dfb0)]),
        globais_combate={hex(a): dict(descricao=d, referencias=referencias(cs, imagem, a, nome))
                         for a, d in GLOBAIS.items()},
        engin_reset_all_stores=dict(rotina='EnginResetAll', inicio='0x441659', fim_exclusivo='0x441775',
            proprietario='core', stores=reset_unidades),
        conclusao=('ProjectileReset is the only combat-owned reset in the MissionLoad/MissionLoadName prefixes. '
                   'EnginResetAll writes Bag words, +2, +0x9A and +0xAF; attack fields are retained. '
                   'The combat globals above have no writer inside the prefix callees.'),
    )
    destino = saida / 'reinicio-projeteis.json'
    destino.write_text(json.dumps(relatorio, indent=2, ensure_ascii=False) + '\n')
    print(destino)


if __name__ == '__main__':
    main()
