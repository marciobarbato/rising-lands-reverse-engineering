"""Export the original unit/capacity caller prefix and consumed provider identities."""
import hashlib
import json
from ambiente_missoes import CD,OWNED,ROOT
from analisar import HASH_ESTUDADO,dependencias


def exportar():
    pefile,capstone=dependencias()
    raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe=pefile.PE(data=raw)
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
    start,end=0x46c122,0x46c16d
    code=pe.get_data(start-0x400000,end-start)
    instructions=list(md.disasm(code,start))
    if sum(i.size for i in instructions)!=len(code):
        raise ValueError('Incomplete original disassembly')
    filename='terreno-unidades-0046c122.asm'
    (OWNED/'evidencias'/filename).write_text('\n'.join(
        [f'; MissionPlaceTerrain unit/capacity prefix; original SHA-256 {HASH_ESTUDADO}']+
        [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in instructions])+'\n')
    paths=('ferramentas/consultas_unidades.py','ferramentas/colocacao_missao.py',
           'ferramentas/insercao_unidades.py','ferramentas/capacidades_unidades.py',
           'pesquisas-paralelas/economia/bonus_unidades.py','integracao/providers.py')
    report=dict(original_sha256=HASH_ESTUDADO,
                inspected_main='6b15be1c96348d51dac7a46208126e6974290eca',
                start=hex(start),end_exclusive=hex(end),file=filename,
                prefix_sha256=hashlib.sha256(code).hexdigest(),
                providers=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths],
                call_order=['exists(index) lowAL','visible(index) lowAL if exists',
                            'place(index) if visible','capacity_refresh(owner0..3) after all800 slots'],
                boundaries=dict(structures='0x46c16d',missing_bonus='0x428cc0',
                                unsupported_vision_callsite='0x457019',unsupported_vision_target='0x476851'),
                capture_correction='Original-v1 input parent_calls aliased its later output trace. V2 freezes that list and asserts every original output dictionary unchanged; v1 retained.',
                scope='Exact caller order with actual committed providers and explicit inherited physical state. Real MONDE01 reaches radius10 at unit15 after seven complete insertions; preserve the dependency. No full startup/remap, structure insertion, condition execution or running mission.')
    (OWNED/'evidencias/terreno-unidades-manifesto.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    print('Placement prefix:',exportar()['prefix_sha256'])
