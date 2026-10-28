"""Capture the original header/resource/view prelude before translating it."""
import hashlib
import json
from ambiente_missoes import CD, OWNED
from analisar import HASH_ESTUDADO


def capturar():
    from bancada_cabecalho import BancadaCabecalho
    native = BancadaCabecalho()
    cases = []
    mission = (CD/'WORLD/MONDE01.ETA').read_bytes()
    resources = bytes((i*17+0x53) & 255 for i in range(128))
    for camera in (0, 3, 4, 255):
        regs = native.carregar(mission, camera=camera, resources=resources,
                              dimensions=b'\xa5'*4, view=b'\x11\x22\x33\x44')
        layers = native.estado()
        cases.append(dict(camera=camera, source_sha256=hashlib.sha256(mission).hexdigest(),
                          output_sha256=[hashlib.sha256(s).hexdigest() for s in layers],
                          resources_hex=layers[4].hex(), dimensions_hex=layers[5].hex(),
                          view_hex=layers[6].hex(), cursor=native.cursor, io=native.io,
                          resource_calls=native.resource_calls, checkpoint=hex(regs['EIP'])))
    result = dict(original_sha256=HASH_ESTUDADO, scope='Original-only MissionLoad after successful open, before remap. File I/O supplied; SetMatiere and object normalization execute unpatched.',
                  native_calls=native.calls, bounded_segments=native.execucoes,
                  inherited_resource_pattern='byte[i]=(i*17+0x53)&255', cases=cases)
    (OWNED/'evidencias/captura-cabecalho-original.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    r = capturar()
    print('Original-only prelude captures:', r['native_calls'], 'segments:', r['bounded_segments'])
