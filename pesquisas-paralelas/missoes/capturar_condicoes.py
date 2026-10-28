"""Retain original-only table initialization observations before translation."""
import hashlib
import json
import struct
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO
from formatos import ler_eta


def objetivo_sintetico():
    return b''.join(struct.pack('<HB',(i*307)&65535,(i*71)&255) for i in range(400))


def capturar():
    from bancada_condicoes import BancadaCondicoes
    native = BancadaCondicoes()
    mission = (CD/'WORLD/MONDE01.ETA').read_bytes()
    metadata = ler_eta(mission)
    fin_block = next(b for b in metadata['blocos'] if b['nome']=='tabela_458b05')
    obj_block = next(b for b in metadata['blocos'] if b['nome']=='listas_por_jogador')
    fin = bytes((i*13+0x63)&255 for i in range(114))
    objectives = bytes((i*17+0x52)&255 for i in range(804))
    cases = []
    for name,entry,data,offset in (
            ('MONDE01_fin',0x458b05,mission,fin_block['offset']),
            ('empty_fin',0x458b05,struct.pack('<HH',0,10),0),
            ('MONDE01_objectives',0x47c404,mission,obj_block['offset']),
            ('synthetic_objectives',0x47c404,objetivo_sintetico(),0)):
        native.carregar(entry,data,offset,fin,objectives)
        out_fin,out_obj = native.estado()
        cases.append(dict(name=name,entry=hex(entry),source_sha256=hashlib.sha256(data).hexdigest(),
                          offset=offset,cursor=native.cursor,reads=native.reads,
                          fin_hex=out_fin.hex(),objectives_hex=out_obj.hex()))
    report = dict(original_sha256=HASH_ESTUDADO,calls={hex(a):v for a,v in native.calls.items()},
                  bounded_segments=native.execucoes,fin_pattern='(i*13+0x63)&255',
                  objectives_pattern='(i*17+0x52)&255',scope='Original-only loader effects; no condition evaluation, objective text or mission execution.',cases=cases)
    (OWNED/'evidencias/captura-condicoes-original.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    print('Original-only condition table segments:',capturar()['bounded_segments'])
