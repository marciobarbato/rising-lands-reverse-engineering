"""Append original table-loader and unsupported-consumer evidence."""
import hashlib
import json
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO,dependencias


def exportar():
    pefile,capstone = dependencias()
    raw = (CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe = pefile.PE(data=raw)
    md = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    intervals = []
    for name,start,end in (('LoadFinMission',0x458b05,0x458b72),
                           ('LoadObjectif',0x47c404,0x47c4b7),
                           ('TestFinDeMission_NOT_IMPLEMENTED',0x458606,0x458ae6),
                           ('ObjectiveCursorQueries_NOT_IMPLEMENTED',0x47c39a,0x47c404)):
        code = pe.get_data(start-0x400000,end-start)
        ins = list(md.disasm(code,start))
        if sum(i.size for i in ins)!=len(code):
            raise ValueError('Incomplete original disassembly')
        filename = f'condicoes-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; intact original SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),
                              sha256=hashlib.sha256(code).hexdigest(),file=filename))
    result = dict(original_sha256=HASH_ESTUDADO,inspected_main='6a9168e42f917096af88fc6c510b3f25b7230516',
                  intervals=intervals,fin_layout='114 bytes at4e1d20:10x10 records,4 retained globals,10 statuses',
                  objective_layout='804 bytes at511ffc:4x100u16 IDs,4 retained cursor bytes',
                  native_consumer='TestFinDeMission458606 called by CalculGame42c868; 11 resolved native queries; unsupported',
                  scope='Load/reset/copy/retention only; no condition evaluation, cursor query, objective text, victory or event execution.')
    (OWNED/'evidencias/condicoes-manifesto.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    print('Condition evidence intervals:',len(exportar()['intervals']))
