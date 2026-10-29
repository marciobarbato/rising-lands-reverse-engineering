"""Static Stage 11 inventory; never instantiate the native execution harness."""
import hashlib
import json
from ambiente_missoes import CD,OWNED,ROOT
from analisar import HASH_ESTUDADO,dependencias

BASE_INSPECIONADA='8810b3730a0fb788af3eac2b447dea65372f597f'
TRECHOS=(('MissionPlaceTerrain_structure_scan',0x46c16d,0x46c1b8),
         ('BatimentExiste',0x41a735,0x41a75c),
         ('MissionPlaceTerrain_shared_return',0x46b6f5,0x46b6f8))
PROVEDORES=('ferramentas/colocacao_estruturas.py',
            'pesquisas-paralelas/economia/construcoes_habitaveis.py')


def exportar():
    pefile,capstone=dependencias()
    raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Intact executable SHA-256 mismatch')
    pe=pefile.PE(data=raw)
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    intervals=[]
    for name,start,end in TRECHOS:
        code=pe.get_data(start-0x400000,end-start)
        instructions=list(md.disasm(code,start))
        if sum(i.size for i in instructions)!=len(code):
            raise ValueError(f'Incomplete disassembly: {name}')
        filename=f'terreno-estruturas-missao-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; intact executable SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip()
             for i in instructions])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),
                              sha256=hashlib.sha256(code).hexdigest(),file=filename))
    report=dict(original_sha256=HASH_ESTUDADO,inspected_main=BASE_INSPECIONADA,
                status='Static inventory only; no native capture or implementation in this stage yet',
                intervals=intervals,
                structure_pool=dict(base='0x49a0c8',bytes=276000,records=1000,stride=276,
                                    existence='u8 +5 !=0; AX index; returns AL 0/1'),
                scan_order=[dict(call='0x46c185',target='0x41a735',name='BatimentExiste',gate='lowAL'),
                            dict(call='0x46c190',target='0x41c4ac',name='PlaceBatiment'),
                            dict(call='0x46c197',target='0x41a5b8',name='BatimentEstHabiter',gate='lowAL'),
                            dict(call='0x46c1a2',target='0x41cc70',name='BatimentHabitable',conditional=True),
                            dict(call='0x46c1b1',target='0x419e97',name='BatimentModifyMap',EDX=1)],
                providers=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest())
                           for p in PROVEDORES],
                pending_provider='Core Stage15 BatimentModifyMap: wait for committed main SHA and its exact public contract; no live-sibling imports',
                scope='L8 structure traversal after the integrated unit/capacity prefix. Native whole-state validation and original-only captures require a coordinator heavy grant. No full MissionLoad, natural remap, frame or mission runtime claim.')
    (OWNED/'evidencias/terreno-estruturas-missao-inventario.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    print('Static original intervals:',len(exportar()['intervals']))
