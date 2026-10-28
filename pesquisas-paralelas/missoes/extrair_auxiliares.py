"""Append exact original first-auxiliary loader bodies and caller prefixes."""
import hashlib
import json
from ambiente_missoes import CD,OWNED,ROOT
from analisar import HASH_ESTUDADO,dependencias


def exportar():
    pefile,capstone=dependencias();raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe=pefile.PE(data=raw);md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32);intervals=[]
    for name,start,end in (('LoadMine',0x47534a,0x47539c),('IALoadAttaqueIni',0x47c24d,0x47c2ec),
                           ('MissionLoad_first_auxiliaries',0x46c57d,0x46c587),
                           ('MissionLoadName_first_auxiliaries',0x46c946,0x46c950)):
        code=pe.get_data(start-0x400000,end-start);ins=list(md.disasm(code,start))
        if sum(i.size for i in ins)!=len(code):
            raise ValueError('Incomplete original disassembly')
        filename=f'auxiliares-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; original SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),sha256=hashlib.sha256(code).hexdigest(),file=filename))
    source=ROOT/'pesquisas-paralelas/economia/extracao.py'
    result=dict(original_sha256=HASH_ESTUDADO,inspected_main='189c94eac6700c5d0fb24dc547d5da015734b06d',
                intervals=intervals,mine_buffer=dict(base='0x509954',bytes=80,records=20,stride=4),
                attack_buffer=dict(base='0x50d5b4',bytes=1004,records=100,stride=10,disk_stride=8,counter='0x50d99c'),
                economy_consumer=dict(path=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest()),
                scope='Two complete raw auxiliary loaders and exact caller order; stop before LoadBatimentGhost. No resource extraction, shared AI interpreter, events or mission execution.',
                import_boundary='Economic and graphics flat construcoes modules collide; actual economy-object regression runs in a separate Python process without modifying providers.')
    (OWNED/'evidencias/auxiliares-manifesto.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    print('Auxiliary intervals:',len(exportar()['intervals']))
