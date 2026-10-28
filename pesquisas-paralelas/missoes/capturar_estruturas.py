"""Capture both original structure-copy paths before their translation."""
import hashlib
import json
import struct
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO
from formatos import ler_eta


def bloco_sintetico():
    return struct.pack('<HH',3,204)+b''.join(struct.pack('<H',i)+bytes((j*17+i)&255 for j in range(204))
                                           for i in (999,7,999))


def capturar():
    from bancada_estruturas import BancadaCargaEstruturas
    native=BancadaCargaEstruturas()
    mission=(CD/'WORLD/MONDE01.ETA').read_bytes()
    block=ler_eta(mission)['blocos'][0]
    cases=[]
    for name,data,offset,caller in (('MONDE01',mission,block['offset'],'MissionLoad'),
                                    ('MONDE01_name',mission,block['offset'],'MissionLoadName'),
                                    ('sparse_repeated',bloco_sintetico(),0,'MissionLoad'),
                                    ('empty',struct.pack('<HH',0,204),0,'MissionLoadName')):
        pool=b'\xa5'*276000
        native.carregar(data,offset,pool,caller)
        output=native.estado()
        cases.append(dict(name=name,caller=caller,source_sha256=hashlib.sha256(data).hexdigest(),
                          offset=offset,cursor=native.cursor,reads=native.reads,
                          output_pool_sha256=hashlib.sha256(output).hexdigest(),
                          changed=[dict(index=i,record_hex=output[i*276:(i+1)*276].hex())
                                   for i in range(1000) if output[i*276:(i+1)*276]!=pool[i*276:(i+1)*276]]))
    report=dict(original_sha256=HASH_ESTUDADO,calls=native.calls,bounded_segments=native.execucoes,
                inherited_pool='0xa5 in every byte',scope='Original inline copies only; explicit synthetic caller stack scratch; stop before unit loading. No remap, reset, allocation, insertion or mission execution.',cases=cases)
    (OWNED/'evidencias/captura-estruturas-original.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    print('Original structure-copy segments:',capturar()['bounded_segments'])
