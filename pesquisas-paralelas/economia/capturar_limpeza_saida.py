"""Add original production cleanup and BagVide evidence, preserving prior data."""
import hashlib
import json
from pathlib import Path
import sys

PASTA=Path(__file__).resolve().parent
RAIZ=PASTA.parents[1]
sys.dont_write_bytecode=True
sys.path.insert(0,str(RAIZ.parent/'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH


def main():
    dados=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest()!=HASH:
        raise ValueError('Original executable hash mismatch')
    pe=pefile.PE(data=dados)
    imagem,base=pe.get_memory_mapped_image(),pe.OPTIONAL_HEADER.ImageBase
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    captures=[]
    for inicio,fim,nome in ((0x420fb7,0x421250,'SortieTroupe cleanup context'),
                            (0x44724a,0x4472d3,'Complete BagVide unit-type predicate')):
        codigo=imagem[inicio-base:fim-base]
        arquivo=f'limpeza-saida-{inicio:08x}.asm'
        linhas=[f'; {nome}; exclusive end 0x{fim:08x}.',f'; Original EXE SHA-256: {HASH}',
                '; Context includes unsupported terrain/neutralization/AI calls; these are not skipped.']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo,inicio)]
        (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
        captures.append(dict(start=hex(inicio),end_exclusive=hex(fim),symbol=nome,
                             bytes_hex=codigo.hex(),sha256=hashlib.sha256(codigo).hexdigest(),listing=arquivo))
    reset=RAIZ/'evidencias/ciclo-estruturas/manifesto.json'
    if not reset.exists():
        raise ValueError('Missing committed core reset evidence')
    result=dict(sha256_exe=HASH,sha256_sbl='c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627',
                scope='Isolated cleanup continuation types1/2/13/16; stop before terrain query or unit AI message',
                captures=captures,core_reset_implementation='7a24e974384782e66d6c7454fe1343035e1178db',
                core_reset_manifest_sha256=hashlib.sha256(reset.read_bytes()).hexdigest(),
                frame=dict(entry='0x420fb7',esp_word0='building index u16',esp_word4='output unit u16',
                           EDI='0x49a0c8+building*276',preceding_unit_calls='assumed completed; not executed by this slice'),
                checkpoints={'0x42110c':'before BatimentGetPosition 0x41aee2; raw parameter10 type2/8 otherwise',
                             '0x4211d3':'before iagUnitSendMessage0x4829c8; AX unit, EDX70, EBX0'},
                caller_jump_table_hex=imagem[0x420df4-base:0x420e4c-base].hex())
    (PASTA/'evidencias/limpeza-saida.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Captured cleanup context, BagVide and committed reset identity.')


if __name__=='__main__':
    main()
