"""Export only this slice's original bytes; leave predecessor evidence intact."""
import hashlib
import json
from pathlib import Path

from extrair_evidencias import HASH, ler_imagem, Cs, CS_ARCH_X86, CS_MODE_32

PASTA = Path(__file__).resolve().parent
TRECHOS = {
    'EnginInfligeDegat': (0x4502f0, 0x450856),
    'ChercheTypeEnginProximite': (0x4500e4, 0x450286),
    'ChercheIndiceEnginCible': (0x4465df, 0x446693),
    'TerrainEstDecouvert': (0x4766f0, 0x47670a),
    'EnginGetVolume': (0x440c5d, 0x440d5e),
    'EnginEstSelectionne': (0x472174, 0x4721a8),
    'PlayerGetType': (0x46d817, 0x46d838),
    'iagUnitSendMessage_entry': (0x4829c8, 0x482a14),
    'iagUnitSendMessage_non_ai_return': (0x482eb5, 0x482ebc),
}


def main():
    imagem = ler_imagem()
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    trechos = []
    for nome, (inicio, fim) in TRECHOS.items():
        dados = bytes(imagem[inicio - 0x400000:fim - 0x400000])
        arquivo = 'consumo-' + f'{inicio:08x}.asm'
        linhas = [f'; {nome}; [0x{inicio:08x}, 0x{fim:08x})', f'; Original EXE SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24s} {i.mnemonic:8s} {i.op_str}'.rstrip()
                   for i in cs.disasm(dados, inicio)]
        (PASTA / 'evidencias' / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(symbol=nome, start=f'0x{inicio:08x}', end_exclusive=f'0x{fim:08x}',
                            sha256_bytes=hashlib.sha256(dados).hexdigest(), file=arquivo))
    manifesto = dict(sha256_original=HASH, ranges=trechos,
                    scope='Mode 1 unit consumer; non-AI message return, no audio backend or death branch execution')
    (PASTA / 'evidencias/consumo-dano.json').write_text(json.dumps(manifesto, indent=2) + '\n')
    print(f'Exported {len(trechos)} original-byte ranges')


if __name__ == '__main__':
    main()
