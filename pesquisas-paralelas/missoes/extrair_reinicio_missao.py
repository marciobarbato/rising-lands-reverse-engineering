"""Export the original MissionLoad/MissionLoadName reset prefixes and UI leaf resets."""
import hashlib
import json
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO,dependencias

OWN=(('MissionLoad_reset_prefix',0x46c2cf,0x46c396),('MissionLoadName_reset_prefix',0x46c5e3,0x46c76c),
     ('IconeReset',0x45e88f,0x45e90b),('MessageBoxInit',0x469908,0x46994b),('BallonInit',0x441b6c,0x441baa))
# Callees composed or named here; their bodies belong to the listed owner.
CALLEES=(('TerrainReset',0x46b315,0x46b38f,'core, pending'),('MiniMapReset',0x469f00,0x469f68,'core, pending'),
         ('BatimentResetAll',0x41a75c,0x41a860,'core ciclo_estruturas.resetar_todas_estruturas'),
         ('EnginResetAll',0x441659,0x441775,'core ciclo_unidades.resetar_todas_unidades'),
         ('ProjectileReset',0x46e00a,0x46e02c,'combat reinicio_projeteis.resetar_projeteis'),
         ('SortilegeResetTechnologie',0x4749f2,0x474a38,'economy AprendizagemEconomia.zerar_tecnologia'),
         ('RechercheReset',0x470b46,0x470b9c,'requested from economy'),
         ('Engin_ResetExperience',0x441470,0x4414ad,'requested from core; tail jumps to 0x440d5a'),
         ('ReseauActif',0x42c3b0,0x42c3b6,'AL=[0x4e0730]; explicit inherited byte'),
         ('MakeMissionName',0x46c1b8,0x46c2cf,'missions Stage 6'))


def exportar():
    pefile,capstone=dependencias();raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    pe=pefile.PE(data=raw);md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32);intervals=[]
    for name,start,end in OWN:
        code=pe.get_data(start-0x400000,end-start);ins=list(md.disasm(code,start))
        if sum(i.size for i in ins)!=len(code):
            raise ValueError('Incomplete original disassembly')
        filename=f'reinicio-{start:08x}.asm'
        (OWNED/'evidencias'/filename).write_text('\n'.join(
            [f'; {name}; original SHA-256 {HASH_ESTUDADO}']+
            [f'{i.address:08x}  {i.bytes.hex():<24} {i.mnemonic} {i.op_str}'.rstrip() for i in ins])+'\n')
        intervals.append(dict(name=name,start=hex(start),end_exclusive=hex(end),
                              sha256=hashlib.sha256(code).hexdigest(),file=filename))
    callees=[dict(name=n,start=hex(a),end_exclusive=hex(b),owner=o,
                  sha256=hashlib.sha256(pe.get_data(a-0x400000,b-a)).hexdigest()) for n,a,b,o in CALLEES]
    strings={hex(a):pe.get_data(a-0x400000,12).split(b'\0')[0].decode('latin-1') for a in (0x494b3b,0x494b3e,0x494b43,0x494b4b)}
    result=dict(original_sha256=HASH_ESTUDADO,inspected_main='7b7b96960cee0ec7868914e811f51b851fc27dba',
        intervals=intervals,callees=callees,strings=strings,
        mission_load_order=['AL=[0x496fe4] -> MakeMissionName 0x46c1b8 (local+0x100)','strcpy(local, 0x509594)','strcat(local, local+0x100)',
                            'u16 [0x4e1a38]=[0x4e1a3a]=0xffff','IconeReset @0x46c35a','TerrainReset @0x46c35f','MiniMapReset @0x46c364',
                            'BatimentResetAll @0x46c369','EnginResetAll @0x46c36e','ProjectileReset @0x46c373','MessageBoxInit @0x46c378',
                            'BallonInit @0x46c37d','FileOpen(local, "rb") @0x46c389'],
        mission_load_name_order=['u16 [0x4e1a38]=[0x4e1a3a]=0xffff','IconeReset @0x46c60a','TerrainReset @0x46c60f','MiniMapReset @0x46c614',
                                 'BatimentResetAll @0x46c619','EnginResetAll @0x46c61e','ProjectileReset @0x46c623','MessageBoxInit @0x46c628',
                                 'zero 4x26 @0x4e1934','zero 4x22 @0x4dfad4','SortilegeResetTechnologie @0x46c687','RechercheReset @0x46c68c',
                                 'Engin_ResetExperience @0x46c691','u8 [0x496fe4]=0x32','ReseauActif @0x46c69d',
                                 'if AL: RechercheCheat 0x4716fe @0x46c6a6, RechercheStore 0x4714f0 @0x46c6ab','BallonInit @0x46c6b0',
                                 'dir = stricmp(name+len-4, ".NET")==0 ? 0x509494 : 0x509594','path = dir + "\\WORLD\\" + name','FileOpen(path, "rb") @0x46c75f'],
        leaf_buffers=dict(IconeReset='10x6 at 0x4e2410 (u16 0x29b1,u16 1,u16 0); changed flag u8 0x4e05a2',
                          MessageBoxInit='256x518 records at 0x4e7754 (byte +0); u16 0x507d54,0x507d56; u8 0x507d58,0x507d59',
                          BallonInit='4x8 at 0x4e1a14: u16 +4/+6=ffff, u16 +0=0, u8 +2=0, +3 kept'),
        scope='Reset prefixes of both callers to FileOpen, UI leaf resets owned by missions, and the callee inventory. No terrain/minimap/research/experience body is reconstructed here.')
    (OWNED/'evidencias/reinicio-manifesto.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    print('Reset intervals:',len(exportar()['intervals']))
