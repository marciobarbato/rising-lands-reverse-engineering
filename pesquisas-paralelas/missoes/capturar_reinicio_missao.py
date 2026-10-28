"""Original-only reset-prefix captures, taken before the Python translation."""
import hashlib
import json
import random
import struct
from ambiente_missoes import OWNED
from analisar import HASH_ESTUDADO
from capturar_cadeia_auxiliar import DATA_BASE,imagem_base
from capturar_nome import jogadores_sinteticos
from bancada_reinicio_missao import ponteiros

# Every global the prefixes can write or read, as explicit inherited state.
REGIONS={'counters':(0x4e1a38,4),'icons':(0x4e2410,60),'icons_changed':(0x4e05a2,1),
         'message_boxes':(0x4e7754,0x507d5a-0x4e7754),'balloons':(0x4e1a14,32),
         'structures':(0x49a0c8,276000),'structure_flags':(0x49a070,88),'structure_selections':(0x495be0,8),
         'unit_realizable':(0x4e1934,104),'structure_realizable':(0x4dfad4,88),
         'spells':(0x508f30,20),'inventions':(0x508f44,20),'network':(0x4e0730,1),
         'directory_net':(0x509494,256),'directory':(0x509594,256),'mission':(0x496fe4,1),'variant':(0x4e1d85,1)}
ICON=struct.pack('<HHH',0x29b1,1,0)


def regiao(image,name):
    address,size=REGIONS[name]
    return image[address-DATA_BASE:address-DATA_BASE+size]


def imagem_reinicio(seed,*,number=1,variant=0,directory=b'C:\\RISING',directory_net=b'',network=0,icons=None):
    image=bytearray(imagem_base());rng=random.Random(0x7e5e0000+seed)
    for name,(address,size) in REGIONS.items():
        image[address-DATA_BASE:address-DATA_BASE+size]=rng.randbytes(size)
    for name,text in (('directory',directory),('directory_net',directory_net)):
        address,_=REGIONS[name];image[address-DATA_BASE:address-DATA_BASE+len(text)+1]=text+b'\0'
    image[0x496fe4-DATA_BASE]=number&255;image[0x4e1d85-DATA_BASE]=variant&255;image[0x4e0730-DATA_BASE]=network&255
    if icons is not None:
        image[0x4e2410-DATA_BASE:0x4e2410-DATA_BASE+60]=icons
    return ponteiros(image)


def pools(seed):
    rng=random.Random(0x900d0000+seed)
    return rng.randbytes(220800),tuple(rng.randbytes(2704) for _ in range(4)),rng.randbytes(5600)


def resumo(state,extra):
    image=state['image']
    return dict(image_sha256=hashlib.sha256(image).hexdigest(),
                region_sha256={n:hashlib.sha256(bytes(regiao(image,n))).hexdigest() for n in REGIONS},
                units_sha256=hashlib.sha256(state['units']).hexdigest(),
                bags_sha256=[hashlib.sha256(b).hexdigest() for b in state['bags']],
                projectiles_sha256=hashlib.sha256(state['projectiles']).hexdigest(),
                **{k:v.decode('latin-1') for k,v in extra.items()})


def casos_folhas():
    variants=[ICON*10,bytes(60),ICON*9+struct.pack('<HHH',0x29b1,1,1)]
    for record in range(10):
        for field,value in ((0,0x29b0),(1,0),(2,0xffff)):
            data=bytearray(ICON*10);struct.pack_into('<H',data,record*6+field*2,value);variants.append(bytes(data))
    return variants


def capturar():
    from bancada_reinicio_missao import BancadaReinicioMissao
    native=BancadaReinicioMissao();cases=[]
    def run(kind,seed,image,call,**info):
        units,bags,projectiles=pools(seed)
        native.carregar(image,units,bags,projectiles,jogadores_sinteticos(info.pop('values',(0,0,0))))
        regs,extra=call()
        cases.append(dict(kind=kind,seed=seed,input_image_sha256=hashlib.sha256(bytes(image)).hexdigest(),
                          stop=hex(regs['EIP']),output=resumo(native.estado(),extra),**info))
    for index,icons in enumerate(casos_folhas()):
        for flag in (0,1,0xa5):
            image=imagem_reinicio(index*3+flag%7,icons=icons);image[0x4e05a2-DATA_BASE]=flag
            run('IconeReset',index,image,lambda:(native.folha('IconeReset'),{}),icon_case=index,flag=flag)
    for name in ('MessageBoxInit','BallonInit'):
        for seed in range(3):
            run(name,seed,imagem_reinicio(40+seed),lambda name=name:(native.folha(name),{}))
    numbers=list(range(0,41))+[99,100,127,128,200,255]
    for number in numbers:
        for variant in ((0,1,2,3) if number==9 else (0,)):
            values=(100,-20 & 255,90) if number in (10,12,17) else (0,0,0)
            directory=(b'',b'C:\\RISING',b'D:'+b'\\x'*100)[number%3]
            image=imagem_reinicio(200+number,number=number,variant=variant,directory=directory)
            run('MissionLoad_prefix',number,image,lambda number=number:native.prefixo('MissionLoad',number=number),
                number=number,variant=variant,values=values,directory=directory.decode('latin-1'))
    for seed,path in enumerate((b'\\World\\Monde01.ETA',b'C:\\RISING\\World\\Monde12a.ETA',b'')):
        run('MissionLoad_tail',seed,imagem_reinicio(300+seed),
            lambda path=path:native.continuacao('MissionLoad',path=path),path=path.decode('latin-1'))
    for seed,name in enumerate((b'MONDE01.ETA',b'partida.net',b'SAVE.NeT',b'abcd')):
        run('MissionLoadName_prefix',seed,imagem_reinicio(400+seed),
            lambda name=name:native.prefixo('MissionLoadName',name=name),name=name.decode('latin-1'))
        for network in (0,1):
            run('MissionLoadName_tail',seed,imagem_reinicio(500+seed*2+network,network=network),
                lambda name=name:native.continuacao('MissionLoadName',name=name),name=name.decode('latin-1'),network=network)
    report=dict(original_sha256=HASH_ESTUDADO,entries=native.entries,stops=native.stops,
                bounded_segments=native.execucoes,cases=cases,
                scope='Original-only reset prefixes: three UI leaf resets, both caller prologues to the TerrainReset CALL (no provider), the MissionLoad tail from 0x46c369 to the FileOpen 0x458420 stop and the MissionLoadName tail from 0x46c619 to the RechercheReset CALL 0x46c68c. Inherited globals, pools and directories are explicit synthetic patterns.')
    (OWNED/'evidencias/captura-reinicio-original.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    r=capturar();print('Original reset entries:',sum(r['entries'].values()),'stops:',r['stops'],'segments:',r['bounded_segments'])
