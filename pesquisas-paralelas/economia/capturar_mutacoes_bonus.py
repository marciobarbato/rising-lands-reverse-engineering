"""Add original setter/reset producer evidence; leave prior captures untouched."""
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
    for a,b,n in ((0x428878,0x428c8a,'BonusSetEngin'),(0x428e71,0x428eee,'BonusReset'),
                  (0x428716,0x42871a,'shared BonusReset return'),(0x44230c,0x442347,'TypeEnginEstArmee')):
        raw=im[a-base:b-base]
        file=f'mutacoes-bonus-{a:08x}.asm'
        lines=[f'; {n}; exclusive end 0x{b:08x}.',f'; Original EXE SHA-256: {HASH}',
               '; Original instruction listing; capacity refresh remains an explicit dependency.']
        lines += [f'{i.address:08x}  {i.bytes.hex():24} {i.mnemonic:8} {i.op_str}'.rstrip() for i in md.disasm(raw,a)]
        (PASTA/'evidencias'/file).write_text('\n'.join(lines)+'\n')
        captures.append(dict(symbol=n,start=f'0x{a:08x}',end_exclusive=f'0x{b:08x}',bytes_hex=raw.hex(),
                             sha256=hashlib.sha256(raw).hexdigest(),listing=file))
    raw=im[0x428844-base:0x428878-base]
    result=dict(sha256_exe=HASH,sha256_sbl=catalog['sha256_sbl'],capstone=capstone.__version__,
        scope='Complete BonusReset and protected BonusSetEngin table mutation; capacity refresh pending',
        captures=captures,selector_dispatch=dict(address='0x00428844',bytes_hex=raw.hex(),
            sha256=hashlib.sha256(raw).hexdigest(),targets=[f'0x{a:08x}' for a in struct.unpack('<13I',raw)]),
        input_widths=dict(AL='owner u8',BL='type u8 or branch-specific sentinel30',DL='selector u8',CX='value u16'),
        dependency=dict(selector=1,call='0x00428c60',stop='0x004475ef',symbol='EnginResetCapacite',AL='owner u8'),
        reset_preserved_record_offsets=[3,7,15,16,17])
    (PASTA/'evidencias/mutacoes-bonus.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Captured four original intervals and one selector table.')


if __name__=='__main__':main()
