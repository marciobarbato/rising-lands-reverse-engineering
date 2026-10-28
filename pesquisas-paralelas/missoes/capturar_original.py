"""Capture original-only MONDE01 and sparse-index behavior before translation."""
import hashlib
import json
import struct
from ambiente_missoes import CD, OWNED
from entradas import bloco_unidades, tipos_originais
from analisar import HASH_ESTUDADO as HASH_ORIGINAL


def sparse_fixture():
    records = []
    for index, kind, owner, state in ((799, 4, 0, 7), (7, 16, 3, 14),
                                       (7, 20, 2, 4), (0, 25, 200, 0)):
        disk = bytearray((j*17+index) & 255 for j in range(784))
        disk[0:3] = bytes((owner, kind, state))
        records.append(struct.pack('<H', index) + disk)
    return struct.pack('<HH', len(records), 784) + b''.join(records)


def capturar():
    from bancada_unidades import BancadaCargaUnidades
    b = BancadaCargaUnidades()
    types = tipos_originais()
    bonuses = bytes((i*19+71) & 255 for i in range(1872))
    mission = (CD/'WORLD/MONDE01.ETA').read_bytes()
    block = bloco_unidades(mission)
    cases = []
    for name, data, offset in (('MONDE01', mission, block['offset']),
                               ('synthetic_sparse_repeated', sparse_fixture(), 0)):
        pool = bytes([0xa5]) * 220800
        b.carregar(data, offset, pool, b'\x11\x22\x33\x44', types, bonuses)
        output, flags = b.estado()
        # Store changed records and whole-pool hash; no complete media is copied.
        changed = [dict(index=i, output_hex=output[i*276:(i+1)*276].hex())
                   for i in range(800) if output[i*276:(i+1)*276] != pool[i*276:(i+1)*276]]
        cases.append(dict(name=name, input_sha256=hashlib.sha256(data).hexdigest(),
                          offset=offset, cursor=b.cursor, io=b.io, changed=changed,
                          output_pool_sha256=hashlib.sha256(output).hexdigest(), flags_hex=flags.hex()))
    report = dict(original_sha256=HASH_ORIGINAL, scope='Original-only successful-I/O unit loader; synthetic inherited pool 0xa5 and explicit patterned loaded bonuses.',
                  translated_scope='0x46acca through original return; SelectionInit executes but has no reconstructed provider here.',
                  native_loads=b.loads, bounded_segments=b.execucoes, native_returns=b.returned,
                  dependency_stops=b.dependency_stops, cases=cases)
    (OWNED/'evidencias/captura-original.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    r = capturar()
    print('Original-only loads:', r['native_loads'], 'segments:', r['bounded_segments'])
