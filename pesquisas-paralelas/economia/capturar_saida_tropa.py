"""Capture only the new SortieTroupe evidence; preserve predecessor evidence."""
import hashlib
import json
from pathlib import Path
import struct
import sys

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RAIZ.parent / 'source/python'))
import capstone
import pefile

HASH = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CAPTURAS = (
    (0x420e4c, 0x420f5f, 'SortieTroupe economic prefix, through call to CalculPosition'),
    (0x420f5f, 0x420fb7, 'SortieTroupe world-call context; outside implemented prefix'),
    (0x4211ea, 0x4211f2, 'SortieTroupe return path'),
    (0x4474a6, 0x4474c7, 'EnginGetBag'),
)
SUPORTE = ((0x4410b7, 0x4410d2), (0x4471b8, 0x44724a), (0x4472ea, 0x4473cf),
           (0x42340f, 0x4235bd), (0x42399a, 0x4239a0))


def main():
    dados = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest() != HASH:
        raise ValueError('Original executable hash does not match this research')
    pe = pefile.PE(data=dados)
    imagem, base = pe.get_memory_mapped_image(), pe.OPTIONAL_HEADER.ImageBase
    sbl = (RAIZ.parent / 'source/cd/INSTALHD/RISING.SBL').read_bytes()
    catalogo = json.loads((RAIZ / 'relatorios/simbolos-originais.json').read_text())
    if hashlib.sha256(sbl).hexdigest() != catalogo['sha256_sbl']:
        raise ValueError('Original SBL hash does not match the committed symbol catalog')
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    pasta = PASTA / 'evidencias'
    trechos = []
    for inicio, fim, nome in CAPTURAS:
        codigo = imagem[inicio-base:fim-base]
        linhas = [f'; {nome}; exclusive end 0x{fim:08x}.', f'; Original EXE SHA-256: {HASH}',
                  '; Capstone instruction listing, not inferred pseudocode.']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo, inicio)]
        arquivo = f'saida-tropa-{inicio:08x}.asm'
        (pasta / arquivo).write_text('\n'.join(linhas) + '\n')
        trechos.append(dict(start=f'0x{inicio:08x}', end_exclusive=f'0x{fim:08x}',
                            description=nome, bytes_hex=codigo.hex(),
                            sha256=hashlib.sha256(codigo).hexdigest(), listing=arquivo))
    tabela = imagem[0x44719c-base:0x4471b8-base]
    resultado = dict(sha256_exe=HASH, sha256_sbl=catalogo['sha256_sbl'], capstone=capstone.__version__,
        scope='Unmodified original bytes; synthetic state; prefix only, not a completed spawn.',
        captures=trechos,
        support=[dict(start=f'0x{a:08x}', end_exclusive=f'0x{b:08x}',
                      sha256=hashlib.sha256(imagem[a-base:b-base]).hexdigest()) for a,b in SUPORTE],
        bag_contient_jump_table=dict(address='0x0044719c', bytes_hex=tabela.hex(),
                                    entries=[f'0x{x:08x}' for x in struct.unpack('<7I', tabela)]),
        dependency=dict(call='0x00420f5a', stop='0x00420698', symbol='CalculPosition',
                        inputs=dict(AX='building index u16', BL='direction u8'), output='AX position u16'),
        next_dependency=dict(call='0x00420f69', target='0x00457b87', symbol='EnginSetType',
                             inputs=dict(EAX='existing unit index', DX='position from CalculPosition',
                                         CL='building +0x7b requested type')))
    (pasta / 'saida-tropa.json').write_text(json.dumps(resultado, indent=2) + '\n')
    print(f'Captured {len(trechos)} original intervals and {len(SUPORTE)} support hashes.')


if __name__ == '__main__':
    main()
