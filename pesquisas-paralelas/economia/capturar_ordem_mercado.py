"""Add original bytes for consuming market callers without rewriting old evidence."""
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

INTERVALOS = ((0x461621, 0x46189a, 'MarcheEchangePrend'),
              (0x46189a, 0x461bea, 'MarcheEchangeDonne'),
              (0x461bea, 0x461c4f, 'MarcheOrdreEchange'),
              (0x463617, 0x46361d, 'shared return epilogue'),
              (0x46499f, 0x4649a7, 'MarcheEchangePrend shared return path'))


def main():
    dados = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Original executable hash mismatch')
    catalogo = json.loads((RAIZ / 'relatorios/simbolos-originais.json').read_text())
    sbl = (RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes()
    if hashlib.sha256(sbl).hexdigest() != catalogo['sha256_sbl']:
        raise ValueError('Original symbol file hash mismatch')
    pe = pefile.PE(data=dados)
    imagem, base = pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    trechos = []
    for inicio, fim, nome in INTERVALOS:
        codigo = imagem[inicio-base:fim-base]
        arquivo = f'ordem-mercado-{inicio:08x}.asm'
        linhas = [f'; {nome}; exclusive end 0x{fim:08x}.', f'; Original EXE SHA-256: {HASH}',
                  '; Original instruction listing; unit branches are captured but unsupported.']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo, inicio)]
        (PASTA / 'evidencias' / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(symbol=nome, start=f'0x{inicio:08x}', end_exclusive=f'0x{fim:08x}',
            bytes_hex=codigo.hex(), sha256=hashlib.sha256(codigo).hexdigest(), listing=arquivo))
    resultado = dict(sha256_exe=HASH, sha256_sbl=catalogo['sha256_sbl'], capstone=capstone.__version__,
        scope='Resource-only consuming callers; original zero-unit loops; explicit nonzero-unit stops',
        captures=trechos, inputs=dict(AL='recipient/accepting player u8, protected 0..3',
                                     DL='proposal row owner u8, protected 0..3'),
        approvals=dict(address='0x004e2968', size=4, width='u8'),
        offered_resources=dict(address='0x004e2cfc', size=24, row_stride=6, width='u16'),
        requested_resources=dict(address='0x004e2d14', size=24, row_stride=6, width='u16'),
        pending_unit_checkpoints=['0x0046166b', '0x004618df'])
    (PASTA / 'evidencias/ordem-mercado.json').write_text(json.dumps(resultado, indent=2) + '\n')
    print(f'Captured {len(trechos)} original intervals.')


if __name__ == '__main__':
    main()
