"""Export Stage 19 static building damage evidence from the intact executable.

This does not execute x86, capture runtime state, or translate game behavior.
Only the two new Stage 19 evidence files are written. --verificar compares
the export without changing those files or any predecessor evidence.
"""
import argparse
import bisect
import hashlib
import json
import struct
from pathlib import Path

from extrair_evidencias import HASH, ler_imagem, Cs, CS_ARCH_X86, CS_MODE_32

PASTA = Path(__file__).resolve().parent
REPO = PASTA.parents[1]
BASE = 0x400000
NORMALIZADO = '26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0'
TRECHOS = {
    'InfligeDegat_building_branch': (0x450874, 0x450a9d),
    'InfligeDegat_return': (0x4510d5, 0x4510dd),
    'BatimentInfligeDegat': (0x41a2c1, 0x41a4b6),
    'TypeBatimentGetDegat_shared_bodies': (0x418b42, 0x418b97),
    'BatimentGetVolume': (0x41a0ab, 0x41a18f),
    'Batiment_shared_return': (0x41db1e, 0x41db24),
    'VoixOffAsk': (0x41a1ac, 0x41a255),
    'CibleTourelleValide': (0x424624, 0x42484b),
    'RechercheDecalageProjectile': (0x425100, 0x425516),
    'BatimentNextEtape_type10': (0x426e43, 0x427549),
    'BatimentNextEtape_type11': (0x427549, 0x427bb7),
}
FAITS = {
    0x4508f1: ('add', 'eax, 0x1a'),
    0x45090c: ('add', 'ecx, eax'),
    0x450919: ('mov', 'eax, ebp'),
    0x45094c: ('call', '0x418b8a'),
    0x450990: ('mov', 'dx, word ptr [0x49716c]'),
    0x4509a0: ('mov', 'dx, word ptr [0x49716e]'),
    0x4509c2: ('call', '0x41a2c1'),
    0x41a2fa: ('mov', 'word ptr [esi + 6], bx'),
    0x41a3ce: ('idiv', 'ebx'),
    0x41a3ee: ('idiv', 'ebx'),
    0x41a3f0: ('cmp', 'ax, word ptr [esp + 4]'),
    0x41a3f5: ('jae', '0x41a4ae'),
    0x41a411: ('call', '0x484808'),
    0x41a422: ('mov', 'byte ptr [ecx + 5], 3'),
    0x41a45a: ('call', '0x475118'),
}


def exportar():
    imagem = ler_imagem()  # Verifies the complete intact EXE SHA-256 first.
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    simbolos = []
    for linha in (REPO / 'relatorios/simbolos-originais.tsv').read_text().splitlines():
        p = linha.split('\t')
        try:
            simbolos.append((int(p[0], 16), p[1]))
        except (ValueError, IndexError):
            continue
    simbolos.sort()
    inicios = [a for a, _ in simbolos]

    def simbolo(alvo):
        a, nome = simbolos[bisect.bisect_right(inicios, alvo) - 1]
        return f'{nome}+{alvo-a:#x}'

    trechos, instrucoes = {}, {}
    linhas = [f'; Stage 19 static inventory only; intact EXE SHA-256 {HASH}']
    for nome, (a, z) in TRECHOS.items():
        dados = bytes(imagem[a-BASE:z-BASE])
        ins = list(cs.disasm(dados, a))
        assert ins and ins[-1].address + ins[-1].size == z, nome
        instrucoes.update({i.address: (i.mnemonic, i.op_str) for i in ins})
        chamadas = []
        for i in ins:
            if i.mnemonic == 'call':
                alvo = int(i.op_str, 16)
                chamadas.append(dict(call=hex(i.address), target=hex(alvo), symbol=simbolo(alvo)))
        trechos[nome] = dict(start=hex(a), end_exclusive=hex(z),
                            sha256_bytes=hashlib.sha256(dados).hexdigest(), direct_calls=chamadas)
        linhas.append(f'; {nome} [{a:#x},{z:#x})')
        linhas += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}' for i in ins]
    for a, esperado in FAITS.items():
        assert instrucoes[a] == esperado, (hex(a), instrucoes[a], esperado)

    tabela = bytes(imagem[0x426880-BASE:0x4268d4-BASE])
    entradas = struct.unpack('<21I', tabela)
    assert entradas[9:11] == (0x426e43, 0x427549)
    caract = bytes(imagem[0x495d8c-BASE:0x495d8c-BASE+22*52])
    manifesto = dict(
        status='STATIC INVENTORY ONLY; no runtime capture or translation',
        sha256_original=HASH, sha256_normalized_analysis_only=NORMALIZADO,
        original_execution_oracle='intact EXE only; no execution in this stage yet',
        ranges=trechos,
        instruction_assertions={hex(a): ' '.join(v) for a, v in FAITS.items()},
        structure_dispatch=dict(address='0x426880', index='structure type minus 1; NOT state +5',
                                sha256_bytes=hashlib.sha256(tabela).hexdigest(),
                                entries=[dict(type=t+1, target=hex(a)) for t, a in enumerate(entradas)]),
        initial_pe_characteristics=dict(address='0x495d8c', stride=52, types=22,
            sha256_bytes=hashlib.sha256(caract).hexdigest(),
            maximum_life_words=[struct.unpack_from('<H', caract, 52*t+4)[0] for t in range(22)],
            warning='Initial PE words only. Runtime loaded characteristics must be explicit inputs.'),
        dependency_boundaries=dict(
            wrapper='iagVilleSendMessage(mode1), damage consumer, Random(0x21), ProjectileInit, alliance/diplomacy/statistics',
            consumer='damage accumulator store precedes volume/audio/voice; city message precedes destruction stores; sympathy precedes final voice',
            turret='types10/11 inventoried for future dispatcher contract; neither branch translated here'),
        validation=dict(static_identity_and_instruction_assertions='passed', native_captures='not run',
                        python_translation='not implemented', native_comparison='not run',
                        heavy_domain_checks='not run; coordinator heavy lease required',
                        main_integration='not delivered', real_mission='not run'))
    return {
        'dano-batiment-stage19.json': json.dumps(manifesto, indent=2) + '\n',
        'dano-batiment-stage19.asm': '\n'.join(linhas) + '\n',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verificar', action='store_true')
    args = parser.parse_args()
    for nome, conteudo in exportar().items():
        destino = PASTA / 'evidencias' / nome
        if args.verificar:
            assert destino.read_text() == conteudo, f'Static export differs: {destino}'
        else:
            destino.write_text(conteudo)
        print(('Verified ' if args.verificar else 'Exported ') + nome)


if __name__ == '__main__':
    main()
