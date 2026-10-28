"""Export new original market-lifecycle intervals without rewriting old evidence."""
import hashlib
import json
from pathlib import Path
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH

INTERVALOS = ((0x46027c, 0x4602cd, 'MarcheResetAll'),
              (0x46634e, 0x4663d6, 'ResetMarche'),
              (0x4663d6, 0x4663eb, 'MarcheQuitte'))


def main():
    dados = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    sbl = (RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes()
    catalogo = json.loads((RAIZ / 'relatorios/simbolos-originais.json').read_text())
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Original executable hash mismatch')
    if hashlib.sha256(sbl).hexdigest() != catalogo['sha256_sbl']:
        raise ValueError('Original symbol file hash mismatch')
    pe = pefile.PE(data=dados)
    imagem, base = pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    captures = []
    for inicio, fim, nome in INTERVALOS:
        codigo = imagem[inicio-base:fim-base]
        arquivo = f'ciclo-mercado-{inicio:08x}.asm'
        linhas = [f'; {nome}; exclusive end 0x{fim:08x}.', f'; Original EXE SHA-256: {HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo, inicio)]
        (PASTA / 'evidencias' / arquivo).write_text('\n'.join(linhas) + '\n')
        captures.append(dict(symbol=nome, start=f'0x{inicio:08x}', end_exclusive=f'0x{fim:08x}',
            bytes_hex=codigo.hex(), sha256=hashlib.sha256(codigo).hexdigest(), listing=arquivo))
    result = dict(sha256_exe=HASH, sha256_sbl=catalogo['sha256_sbl'], capstone=capstone.__version__,
        scope='Selective market lifecycle; protected u8 players 0..3; invalid second index stops after first row',
        captures=captures, invalid_second_checkpoint='0x00466395',
        reset_fields={'0x004e2e7c':'u8=0', '0x004e292c':'u8=1', '0x004e2928':'u8=0',
                      '0x00496f8c':'u8=255', '0x004e2930':'u16=0', '0x004e2938':'u16=0', '0x004e2940':'u16=0'},
        preserved='Proposals, approvals, difference, prices, economy, player records and all gaps',
        calling_convention='ResetMarche AL first, DL second; MarcheQuitte AL first reads live contact before reset')
    (PASTA / 'evidencias/ciclo-mercado.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'Captured {len(captures)} original intervals.')


if __name__ == '__main__':
    main()
