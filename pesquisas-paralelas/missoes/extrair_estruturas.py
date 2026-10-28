"""Append exact original inline structure-copy intervals and input provenance."""
import hashlib
import json
from ambiente_missoes import CD,OWNED,ROOT
from analisar import HASH_ESTUDADO,dependencias


def exportar():
    pefile,capstone=dependencias()
    raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe=pefile.PE(data=raw);md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    intervals=[]
    for name,start,end in (('MissionLoad_inline_structures',0x46c517,0x46c578),
                           ('MissionLoadName_inline_structures',0x46c8e0,0x46c941)):
        code=pe.get_data(start-0x400000,end-start);ins=list(md.disasm(code,start))
        if sum(i.size for i in ins)!=len(code):
            raise ValueError('Incomplete original disassembly')
        filename=f'estruturas-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; original SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),
                              sha256=hashlib.sha256(code).hexdigest(),file=filename))
    manifest=dict(original_sha256=HASH_ESTUDADO,inspected_main='37629edc282367702811f9b7060d2026b6ba9b47',
                  intervals=intervals,pool=dict(base='0x49a0c8',count=1000,stride=276,copied=204,retained=72),
                  header='u16 count,size; size204; count need not be<=1000 because disk IDs may repeat',
                  providers={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (ROOT/'ferramentas/formatos.py',ROOT/'pesquisas-paralelas/graficos-animacao/construcoes.py')},
                  scope='Inline copies only, after explicit preceding remap/reset and before unit load; no physical state/type/owner initialization or insertion.')
    (OWNED/'evidencias/estruturas-manifesto.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    print('Structure-copy intervals:',len(exportar()['intervals']))
