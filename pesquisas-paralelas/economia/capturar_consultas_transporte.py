"""Capture complete read-only transport status routines from original bytes."""
import hashlib
import json
from pathlib import Path
import sys

PASTA=Path(__file__).resolve().parent
RAIZ=PASTA.parents[1]
sys.path.insert(0,str(RAIZ.parent/'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH


def main():
    dados=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(dados).hexdigest()!=HASH:raise ValueError('Original executable hash mismatch')
    pe=pefile.PE(data=dados)
    imagem,base=pe.get_memory_mapped_image(),pe.OPTIONAL_HEADER.ImageBase
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    captures=[]
    for a,z,n in ((0x456cd9,0x456d35,'EnginRentreMatiere'),(0x456d35,0x456d92,'EnginApporteMatiere'),
                  (0x41a4f4,0x41a513,'BatimentGetType')):
        codigo=imagem[a-base:z-base]
        arquivo=f'consultas-transporte-{a:08x}.asm'
        linhas=[f'; {n}; exclusive end0x{z:x}.',f'; Original EXE SHA-256:{HASH}']
        linhas += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip()
                   for i in md.disasm(codigo,a)]
        (PASTA/'evidencias'/arquivo).write_text('\n'.join(linhas)+'\n')
        captures.append(dict(symbol=n,start=hex(a),end_exclusive=hex(z),bytes_hex=codigo.hex(),
                             sha256=hashlib.sha256(codigo).hexdigest(),listing=arquivo))
    r=dict(sha256_exe=HASH,sha256_sbl='c3a5411255847d36161aea1aeef06ab280265c55fa5a6626cfeb7bab523cc627',
           scope='Complete read-only status queries; no cargo/order/transport state-machine effects',captures=captures,
           inputs=dict(AX='unit index u16 protected0..799',DL='comparison byte',BL='Apporte mode byte,0 wildcard'),
           conditional_building_guard='Rentre reads target+80 only after state5/17/18 and+82byte2; protected target0..999',
           mutation='none; AL returns0/1')
    (PASTA/'evidencias/consultas-transporte.json').write_text(json.dumps(r,indent=2)+'\n')
    print('Captured three complete original intervals.')


if __name__=='__main__':main()
