"""Export exact original bytes of the remaining L7 auxiliary loaders and caller chain."""
import hashlib
import json
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO,dependencias
from bancada_cadeia_auxiliar import CALLERS,CRT

ROUTINES=(('LoadBatimentGhost',0x47bcc7,0x47bd40),('LoadCadreInfluence',0x47c04a,0x47c0c3),
          ('LoadCalculMissionDivers',0x47c30f,0x47c359),('LoadEntrerMonstre',0x47ac30,0x47ad6a),
          ('InitEntrerMonstre',0x47a601,0x47a81d),('Random',0x4704dc,0x470520))
DATA=(('monstre_profile_strings',0x494e4c,0x494efe),('group_monster_types',0x498400,0x498408))


def exportar():
    pefile,capstone=dependencias();raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe=pefile.PE(data=raw);md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32);intervals=[]
    named=list(ROUTINES)+[(name+'_auxiliary_chain',a,b) for name,(a,b) in CALLERS.items()]
    for name,start,end in named:
        code=pe.get_data(start-0x400000,end-start);ins=list(md.disasm(code,start))
        if sum(i.size for i in ins)!=len(code):
            raise ValueError('Incomplete original disassembly')
        filename=f'cadeia-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; original SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),
                              sha256=hashlib.sha256(code).hexdigest(),file=filename))
    crt=[dict(start=hex(a),end_exclusive=hex(b),sha256=hashlib.sha256(pe.get_data(a-0x400000,b-a)).hexdigest())
         for a,b in CRT]
    data=[dict(name=name,start=hex(a),end_exclusive=hex(b),hex=pe.get_data(a-0x400000,b-a).hex())
          for name,a,b in DATA]
    ini=(CD/'INSTALHD/MONSTRE.INI').read_bytes()
    result=dict(original_sha256=HASH_ESTUDADO,inspected_main='f18b5a00a27e716fd3662d56f9482b67b110ef16',
        caller_order=['LoadMine 0x47534a','IALoadAttaqueIni 0x47c24d','LoadBatimentGhost 0x47bcc7',
                      'LoadCadreInfluence 0x47c04a','LoadFinMission 0x458b05','LoadCalculMissionDivers 0x47c30f',
                      'LoadObjectif 0x47c404','LoadEntrerMonstre 0x47ac30','next FileClose 0x45844c'],
        caller_call_sites=dict(MissionLoad=['0x46c57d','0x46c582','0x46c587','0x46c58c','0x46c591','0x46c596','0x46c59b','0x46c5a0','0x46c5a5'],
                               MissionLoadName=['0x46c946','0x46c94b','0x46c950','0x46c955','0x46c95a','0x46c95f','0x46c964','0x46c969','0x46c96e']),
        intervals=intervals,watcom_crt_bodies=crt,data=data,
        buffers=dict(ghost=dict(base='0x50b18c',bytes=5254,count='u16 +0',ids='750 u16 at +2',gap='+1502..+1504',values='750 u32 at +1504',flags='750 u8 at +4504'),
                     influence=dict(base='0x50c614',bytes=4000,records=400,stride=10,prefilled_words='+0,+2,+4,+6'),
                     monsters=dict(base='0x50a9bc',bytes=1220,human_only='u8 +0',profile_dwords='+4,+8,+12',count='u16 +18',records='100x12 at +20'),
                     groups=dict(base='0x50af84',bytes=432,type_counts='16x26 u8 at +0',group_counts='16 u8 at +416'),
                     random_seed='0x497164 u32'),
        external_bindings=dict(read='FileRead wrapper 0x458461 (fixture bytes)',
                               GetPrivateProfileIntA=dict(iat='0x5231ac',call_sites=['0x47a665','0x47a688','0x47a6a5','0x47a6c7']),
                               GetPrivateProfileStringA=dict(iat='0x5231b0',call_sites=['0x47a74d'])),
        shipped_profile=dict(path='INSTALHD/MONSTRE.INI',sha256=hashlib.sha256(ini).hexdigest(),bytes=len(ini)),
        scope='Raw L7 auxiliary loaders and their exact caller order in both callers. No monster spawning, AI, ghost/influence runtime, events or mission execution.')
    (OWNED/'evidencias/cadeia-auxiliar-manifesto.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    print('Auxiliary-chain intervals:',len(exportar()['intervals']))
