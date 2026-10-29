"""Original-only captures of four waiting-slot helpers, before translation.

Synthetic inherited buffers are explicit fixtures, not MONDE01 game state.
No sound/DirectSound handler, callback or queue implementation is imported.
Run through the shared heavy lease; maximum native job duration is five minutes.
"""
import base64
import hashlib
import json
import signal
import struct
import time
import zlib

import ambiente_audio
from ambiente_audio import OWNED, ORIGINAL_SHA256
from emulador import BancadaX86

INDEX=0x498f68
TABLE=0x52137c
STRIDE=44
PLAYING=20
ROUTINES={'reserve':0x48aef8,'give_back':0x48afd0,'maximum':0x48afe9,'find_place':0x48afef}


def encode(data):return base64.b64encode(zlib.compress(bytes(data),9)).decode()


def scenarios():
    table=bytearray((i*31+7)&255 for i in range(STRIDE*PLAYING))
    for i in range(PLAYING):table[i*STRIDE+8]=1
    for operation in ('reserve','give_back'):
        for maximum in range(19,71):yield dict(operation=operation,maximum=maximum,table=bytes(table))
    for maximum in (0,19,20,69,70,71,0xffffffff):yield dict(operation='maximum',maximum=maximum,table=bytes(table))
    for hole in range(PLAYING):
        current=bytearray(table);current[hole*STRIDE+8]=0
        yield dict(operation='find_place',maximum=19,table=bytes(current))
    yield dict(operation='find_place',maximum=19,table=bytes(table))
    for i in range(PLAYING):table[i*STRIDE+8]=255
    yield dict(operation='find_place',maximum=19,table=bytes(table))


def capture():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('Five-minute queue capture limit')))
    signal.alarm(300)
    bench=BancadaX86();cases=[];start=time.monotonic()
    for fixture in scenarios():
        table=fixture['table'];bench.cpu.mem_write(TABLE,table)
        bench.cpu.mem_write(INDEX,struct.pack('<I',fixture['maximum']))
        regs=bench.executar(ROUTINES[fixture['operation']],[(0x48aef8,0x48b01b)],
                            registradores=dict(EAX=0xa1b2c3d4,EDX=0x11223344,ECX=0x55667788),
                            limite_instrucoes=1000)
        final=bytes(bench.cpu.mem_read(TABLE,len(table)))
        cases.append(dict(operation=fixture['operation'],entry=hex(ROUTINES[fixture['operation']]),
            input_maximum=fixture['maximum'],input_table_zlib_base64=encode(table),
            output_maximum=struct.unpack('<I',bench.cpu.mem_read(INDEX,4))[0],eax=hex(regs['EAX']),
            output_table_zlib_base64=encode(final),output_table_sha256=hashlib.sha256(final).hexdigest()))
    result=dict(schema='rising-lands/audio-waiting-slot-original-capture/1',original_sha256=ORIGINAL_SHA256,
                translation_executed=False,fixture='Explicit synthetic 20 x 44-byte playing table and inherited u32 maximum index',
                index_address=hex(INDEX),table_address=hex(TABLE),stride=STRIDE,playing_records=PLAYING,
                cases=cases,native_calls=len(cases),seconds=round(time.monotonic()-start,3))
    return result


if __name__=='__main__':
    path=OWNED/'evidencias/captura-indices-fila-audio-original.json'
    if path.exists():raise ValueError('Refusing to overwrite original evidence')
    result=capture();path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(path=str(path),native_calls=result['native_calls'],seconds=result['seconds'])))
