"""Append Stage2 original prelude evidence without rewriting Stage1 records."""
import hashlib
import json
from ambiente_missoes import CD, OWNED, ROOT
from analisar import HASH_ESTUDADO, dependencias


def exportar():
    pefile, capstone = dependencias()
    original = (CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(original).hexdigest() != HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe = pefile.PE(data=original)
    md = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    intervals = []
    for name,start,end in (('MissionLoad_successful_open_prelude',0x46c396,0x46c517),
                            ('SetMatiere',0x46799c,0x4679d0)):
        raw = pe.get_data(start-0x400000,end-start)
        ins = list(md.disasm(raw,start))
        if sum(i.size for i in ins) != len(raw):
            raise ValueError('Incomplete original disassembly')
        filename = f'cabecalho-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; original SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),
                              sha256=hashlib.sha256(raw).hexdigest(),file=filename))
    result = dict(original_sha256=HASH_ESTUDADO, inspected_main='8fd9c41ce6e3b8709cc0d7235e8c31d9b6a68b8d',
                  intervals=intervals, prerequisite='MissionLoad successful open and prior global resets are caller-owned',
                  stop='0x42ee1c, before every Chemin_Remap effect',
                  providers={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (ROOT/'pesquisas-paralelas/economia/economia.py',
                                       ROOT/'pesquisas-paralelas/graficos-animacao/sequenciais.py')},
                  original_dependencies=[dict(path='INSTALHD/'+name,size=(CD/'INSTALHD'/name).stat().st_size,
                                              sha256=hashlib.sha256((CD/'INSTALHD'/name).read_bytes()).hexdigest())
                                         for name in ('RISING.INI','RISING.SBL','RISING.RUL')],
                  buffers={'attributes':65536,'terrain_le_u16':131072,'objects':65536,'auxiliary':65536,
                           'economy':128,'dimensions_le_u16':4,'selected_view_le_u16':4},
                  scope='Raw layer/resource/view preparation; no natural regions, collision, selection, units or mission execution.')
    (OWNED/'evidencias/cabecalho-manifesto.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    print('Prelude evidence intervals:',len(exportar()['intervals']))
