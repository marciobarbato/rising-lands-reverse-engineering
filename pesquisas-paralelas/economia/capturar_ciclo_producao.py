"""Add original CalculTroupe shared-branch and return-dispatch evidence."""
import hashlib
import json
from pathlib import Path
import struct
import sys

PASTA=Path(__file__).resolve().parent
RAIZ=PASTA.parents[1]
sys.dont_write_bytecode=True
sys.path.insert(0,str(RAIZ.parent/'source/python'))
import capstone
import pefile
from capturar_saida_tropa import HASH


def main():
    data=(RAIZ.parent/'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(data).hexdigest()!=HASH:raise ValueError('Original executable hash mismatch')
    catalog=json.loads((RAIZ/'relatorios/simbolos-originais.json').read_text())
    sbl=(RAIZ.parent/'source/cd/INSTALHD/RISING.SBL').read_bytes()
    if hashlib.sha256(sbl).hexdigest()!=catalog['sha256_sbl']:raise ValueError('Original symbol hash mismatch')
    pe=pefile.PE(data=data)
    im,base=pe.get_memory_mapped_image(),pe.OPTIONAL_HEADER.ImageBase
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    captures=[]
    for a,b,n in ((0x4259e6,0x425c4e,'CalculTroupe entry and selected production branches'),
                  (0x4263e5,0x426418,'CalculTroupe low-type dispatch and common return'),
                  (0x41db1d,0x41db24,'CalculTroupe shared return epilogue')):
        raw=im[a-base:b-base]
        name=f'ciclo-producao-{a:08x}.asm'
        lines=[f'; {n}; exclusive end 0x{b:08x}.',f'; Original EXE SHA-256: {HASH}',
               '; Only building types 1/2/13/16 are in the implemented caller domain.']
        lines += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip() for i in md.disasm(raw,a)]
        (PASTA/'evidencias'/name).write_text('\n'.join(lines)+'\n')
        captures.append(dict(description=n,start=f'0x{a:08x}',end_exclusive=f'0x{b:08x}',
                             bytes_hex=raw.hex(),sha256=hashlib.sha256(raw).hexdigest(),listing=name))
    result=dict(sha256_exe=HASH,sha256_sbl=catalog['sha256_sbl'],capstone=capstone.__version__,
        scope='CalculTroupe types1/2/13/16 through real SortieTroupe preparation; no world completion',
        captures=captures,input='AX building index u16, protected 0..999',
        directions={'1':4,'2':4,'13':14,'16':4},
        progress=dict(offset='0x8c',width='u32',active_byte='0x74',time_type_offset='0x7b',
                      x87_control='0x127f',call_order='advance once if active, then SortieTroupe even below threshold'),
        coefficients=[dict(address=f'0x{a:08x}',bytes_hex=im[a-base:a-base+8].hex(),
                           value=struct.unpack_from('<d',im,a-base)[0]) for a in (0x494432,0x49443a)],
        prefix_evidence='saida-tropa.json',progress_support_evidence='parametros-producao.json')
    (PASTA/'evidencias/ciclo-producao.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Captured three original caller intervals and coefficient bytes.')


if __name__=='__main__':main()
