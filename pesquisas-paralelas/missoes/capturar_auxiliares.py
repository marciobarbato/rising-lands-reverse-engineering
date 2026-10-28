"""Original-only auxiliary loader observations before reconstruction."""
import hashlib
import json
import struct
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO
from formatos import ler_eta


def bloco_sintetico(mines,attacks):
    return (struct.pack('<H',mines)+bytes((i*43+7)&255 for i in range(mines*4))+
            struct.pack('<HH',attacks,8)+bytes((i*37+11)&255 for i in range(attacks*8)))


def capturar():
    from bancada_auxiliares import BancadaAuxiliares
    native=BancadaAuxiliares();mission=(CD/'WORLD/MONDE01.ETA').read_bytes()
    block=next(b for b in ler_eta(mission)['blocos'] if b['nome']=='tabela_47534a')
    cases=[]
    for name,data,offset,caller in (('MONDE01',mission,block['offset'],'MissionLoad'),
                                    ('MONDE01_name',mission,block['offset'],'MissionLoadName'),
                                    ('empty',bloco_sintetico(0,0),0,'MissionLoad'),
                                    ('full',bloco_sintetico(20,100),0,'MissionLoadName')):
        native.carregar(data,offset,b'\x63'*80,b'\xa5'*1004,caller)
        mines,attacks=native.estado()
        cases.append(dict(name=name,caller=caller,source_sha256=hashlib.sha256(data).hexdigest(),
                          offset=offset,cursor=native.cursor,reads=native.reads,
                          mines_hex=mines.hex(),attacks_hex=attacks.hex()))
    report=dict(original_sha256=HASH_ESTUDADO,calls=native.calls,bounded_segments=native.execucoes,
                inherited_mines='0x63',inherited_attacks='0xa5',cases=cases,
                scope='Original two-call post-unit prefixes, stopped before LoadBatimentGhost; no extraction or AI execution, explicit synthetic inherited arrays and caller stack scratch.')
    (OWNED/'evidencias/captura-auxiliares-original.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    print('Original auxiliary prefix segments:',capturar()['bounded_segments'])
