"""Export original filename routine, read-only query, strings and suffix table."""
import hashlib
import json
import struct
from ambiente_missoes import CD,OWNED,ROOT
from analisar import HASH_ESTUDADO,dependencias


def exportar():
    pefile,capstone=dependencias()
    raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe=pefile.PE(data=raw);md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    intervals=[]
    for name,start,end in (('MakeMissionName',0x46c1b8,0x46c2cf),('PlayerGetSympathie',0x46dc6c,0x46dc90)):
        code=pe.get_data(start-0x400000,end-start);ins=list(md.disasm(code,start))
        if sum(i.size for i in ins)!=len(code):
            raise ValueError('Incomplete original disassembly')
        filename=f'nome-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; original SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),sha256=hashlib.sha256(code).hexdigest(),file=filename))
    pointers=struct.unpack('<4I',pe.get_data(0x97154,16))
    strings=[]
    for address in (0x494b27,0x494b36,*pointers):
        data=pe.get_data(address-0x400000,32).split(b'\0',1)[0]+b'\0'
        strings.append(dict(address=hex(address),bytes_hex=data.hex()))
    source=ROOT/'pesquisas-paralelas/economia/mercado.py'
    result=dict(original_sha256=HASH_ESTUDADO,inspected_main='82a0468f5482ef00357bc077a75947c01b44aec4',
                intervals=intervals,strings=strings,suffix_pointer_table=dict(address='0x497154',pointers=[hex(p) for p in pointers]),
                economy_provider=dict(path=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest()),
                inputs='number lowAL; explicit writable destination; number9 raw4e1d85 index0..3; numbers10/12/17 use real read-only sympathy(owner1..3,other0)',
                comparison='CMP CL,AL / signed JLE; initial CL90, CH1; consume signed low8 only; retain initial choice on ties',
                scope='Filename bytes and query order/partial effects only; no default player/result state, file opening, formal mission title or campaign advancement.')
    (OWNED/'evidencias/nome-manifesto.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    print('Filename intervals:',len(exportar()['intervals']))
