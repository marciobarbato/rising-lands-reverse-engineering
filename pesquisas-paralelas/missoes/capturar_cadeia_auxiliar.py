"""Original-only L7 auxiliary-chain captures, taken before the Python translation."""
import hashlib
import json
import random
import struct
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO
from formatos import ler_eta
from perfil_privado_missao import PerfilPrivado

DATA_BASE,DATA_END=0x494000,0x523000
# Every table the chain writes, plus the gaps between them, as explicit inherited state.
REGIONS={'mines':(0x509954,80),'end_conditions':(0x4e1d20,114),'objectives':(0x511ffc,804),
         'monster_to_attack_span':(0x50a9bc,0x50d9a0-0x50a9bc),'random_seed':(0x497164,4)}
INI_NAME=b'./monstre.ini'


def imagem_base():
    """Data/.bss image exactly as BancadaX86 maps it (raw sections, unit-pool pointer), no Unicorn."""
    raw=(CD/'INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=HASH_ESTUDADO:
        raise ValueError('Original EXE SHA-256 mismatch')
    memory=bytearray(0x200000);pe=struct.unpack_from('<I',raw,0x3c)[0]
    sections=struct.unpack_from('<H',raw,pe+6)[0];optional=struct.unpack_from('<H',raw,pe+20)[0]
    for index in range(sections):
        header=pe+24+optional+index*40
        rva,size,offset=struct.unpack_from('<III',raw,header+12)
        if offset and size:
            memory[rva:rva+size]=raw[offset:offset+size]
    struct.pack_into('<I',memory,0x4e19a0-0x400000,0x1000000)
    return memory[DATA_BASE-0x400000:DATA_END-0x400000]


def mapas():
    return sorted((CD/'WORLD').glob('*.ETA'))


def inicio_cadeia(data):
    return next(b['offset'] for b in ler_eta(data)['blocos'] if b['nome']=='tabela_47534a')


def imagem_herdada(base,seed_index,seed=None):
    """Synthetic inherited data image: poisoned tables/gaps and an explicit Random seed."""
    image=bytearray(base);rng=random.Random(0x5eed0000+seed_index)
    for name,(address,size) in REGIONS.items():
        image[address-DATA_BASE:address-DATA_BASE+size]=rng.randbytes(size)
    if seed is not None:
        struct.pack_into('<I',image,0x497164-DATA_BASE,seed&0xffffffff)
    return image


def perfil_original(absent=False):
    return PerfilPrivado({INI_NAME:None if absent else (CD/'INSTALHD/MONSTRE.INI').read_bytes()})


def fluxo(*,mines=(),attacks=(),ghosts=(),influence=(0,10,()),ends=(),divers=bytes(range(16)),
          objectives=None,monsters=None):
    out=bytearray(struct.pack('<H',len(mines)))
    for record in mines:
        out+=record
    out+=struct.pack('<HH',len(attacks),8)+b''.join(attacks)
    out+=struct.pack('<H',len(ghosts))+b''.join(struct.pack('<HI',a,b) for a,b in ghosts)
    count,size,records=influence
    out+=struct.pack('<HH',count,size)+b''.join(records)
    out+=struct.pack('<HH',len(ends),10)+b''.join(ends)
    out+=divers
    out+=objectives if objectives is not None else bytes(i*7&255 for i in range(1200))
    if monsters is None:
        monsters=(100,6,[struct.pack('<HHH',0xffff if i%9==4 else i*0x101,1<<(i%16),i) for i in range(100)])
    count,size,records=monsters
    out+=struct.pack('<HH',count,size)+b''.join(records)
    return bytes(out)


def _registros(rng,count,size):
    return [rng.randbytes(size) for _ in range(count)]


def casos_sinteticos():
    """(name, stream, profile files, seed) with streams covering the supported domains."""
    rng=random.Random(9)
    monstre=(CD/'INSTALHD/MONSTRE.INI').read_bytes()
    tokens=(b'[GENERAL]\r\nHumanOnly=1\r\nProbaCaveJoueur=9\r\nProbaCaveIA=0\r\nProbaEmbuscade=77\r\n'
            b'GROUPE00=7\r\nGROUPE01=0,1\r\nGROUPE02=+3\r\nGROUPE03=-0\r\nGROUPE04=x\r\nGROUPE05=,,5,\r\n'
            b'GROUPE06=7 ,\t2\r\nGROUPE07=1,2,3,4,5,6,7,0,1,2,3\r\nGROUPE08=\r\nGROUPE09=4 4\r\n'
            b'GROUPE10=6x,5\r\nGROUPE15=6\r\nGROUPE11='+b','.join(b'%d'%(i%8) for i in range(140))+b'\r\n')
    masks=[0,1,0x8000,0xffff,0x0101,0x4000,0x0003,0x8001]
    compact=[]
    for i in range(100):
        word0=0xffff if i in (0,3,4,50,97,98,99) else i*37&0xfffe
        compact.append(struct.pack('<HHH',word0,masks[i%8],(i*0x0889)&0xffff))
    cases=[('absent_profile_empty_tables',fluxo(),{INI_NAME:None},0x12345678),
           ('profile_tokens_and_seed0',fluxo(),{INI_NAME:tokens},0),
           ('ghost750_influence400',fluxo(ghosts=[(rng.getrandbits(16),rng.getrandbits(32)) for _ in range(750)],
                                          influence=(400,10,_registros(rng,400,10))),{INI_NAME:monstre},0x7fffffff),
           ('ghost1_influence_size6',fluxo(ghosts=[(5,0xdeadbeef)],influence=(3,6,_registros(rng,3,6))),{INI_NAME:monstre},0xffffffff),
           ('influence_size0_and_size12',fluxo(influence=(2,0,[])),{INI_NAME:monstre},1),
           ('influence_overlap12',fluxo(influence=(399,12,_registros(rng,399,12))),{INI_NAME:monstre},2),
           ('monster_compaction',fluxo(monsters=(100,6,compact)),{INI_NAME:monstre},0x2468ace),
           ('monster_count7_size12',fluxo(monsters=(7,12,_registros(rng,7,12))),{INI_NAME:monstre},3),
           ('monster_count0_size2',fluxo(monsters=(0,2,[])),{INI_NAME:monstre},4),
           ('monster_size2_trailing_empty',fluxo(monsters=(5,2,[b'\x01\x00',b'\xff\xff',b'\x02\x00',b'\xff\xff',b'\xff\xff'])),{INI_NAME:monstre},5)]
    return cases


def resumo_imagem(image,cursor,reads,calls,eip):
    regions={name:hashlib.sha256(bytes(image[a-DATA_BASE:a-DATA_BASE+s])).hexdigest()
             for name,(a,s) in REGIONS.items()}
    return dict(image_sha256=hashlib.sha256(bytes(image)).hexdigest(),region_sha256=regions,
                cursor=cursor,read_count=len(reads),
                read_sizes_sha256=hashlib.sha256(json.dumps([s for _,s in reads]).encode()).hexdigest(),
                profile_calls=len(calls),
                profile_calls_sha256=hashlib.sha256(repr(calls).encode()).hexdigest(),
                stop=hex(eip))


def capturar():
    from bancada_cadeia_auxiliar import BancadaCadeiaAuxiliar,CALLERS
    native=BancadaCadeiaAuxiliar();base=native.imagem();cases=[]
    for index,path in enumerate(mapas()):
        data=path.read_bytes();offset=inicio_cadeia(data)
        for caller in CALLERS:
            image=imagem_herdada(base,index,0x1000+index);profile=perfil_original()
            eip=native.carregar(data,offset,image,profile,caller)
            after=native.imagem()
            case=dict(name=path.stem,caller=caller,source_sha256=hashlib.sha256(data).hexdigest(),offset=offset,
                      input_image_sha256=hashlib.sha256(bytes(image)).hexdigest(),
                      output=resumo_imagem(after,native.cursor,native.reads,profile.chamadas,eip))
            if path.stem=='MONDE01':
                a,s=REGIONS['monster_to_attack_span']
                case['monde01_span_hex']=after[a-DATA_BASE:a-DATA_BASE+s].hex()
                case['monde01_seed']=struct.unpack_from('<I',after,0x497164-DATA_BASE)[0]
            cases.append(case)
    synthetic=[]
    for index,(name,data,files,seed) in enumerate(casos_sinteticos()):
        for caller in CALLERS:
            image=imagem_herdada(base,100+index,seed);profile=PerfilPrivado(files)
            eip=native.carregar(data,0,image,profile,caller)
            synthetic.append(dict(name=name,caller=caller,source_sha256=hashlib.sha256(data).hexdigest(),
                                  input_image_sha256=hashlib.sha256(bytes(image)).hexdigest(),
                                  output=resumo_imagem(native.imagem(),native.cursor,native.reads,profile.chamadas,eip)))
    report=dict(original_sha256=HASH_ESTUDADO,caller_entries=native.calls,returns=native.returned,
                bounded_segments=native.execucoes,read_bindings=native.read_stops,profile_bindings=native.profile_stops,
                cases=cases,synthetic=synthetic,
                scope='Original-only complete L7 chain from LoadMine through LoadEntrerMonstre in both callers, stopped before FileClose 0x45844c. Whole DGROUP+.bss image hashed. Inherited tables, gaps and Random seed are explicit synthetic patterns; the shipped MONSTRE.INI or declared synthetic profiles answer the KERNEL32 binding. No AI, monster spawning, events or mission execution.')
    (OWNED/'evidencias/captura-cadeia-auxiliar-original.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    r=capturar();print('Original chain entries:',r['caller_entries'],'returns:',r['returns'],'segments:',r['bounded_segments'])
