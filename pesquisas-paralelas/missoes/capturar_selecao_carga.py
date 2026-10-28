"""Capture full original unit loading with explicit inherited selection lists."""
import hashlib
import json
import struct
from ambiente_missoes import CD,OWNED
from analisar import HASH_ESTUDADO
from entradas import tipos_originais,bloco_unidades
from capturar_original import sparse_fixture


def capturar():
    from bancada_unidades import BancadaCargaUnidades
    native = BancadaCargaUnidades()
    types = tipos_originais()
    bonuses = bytes((i*19+71)&255 for i in range(1872))
    mission = (CD/'WORLD/MONDE01.ETA').read_bytes()
    cases = []
    for name,data,offset,stop in (('MONDE01',mission,bloco_unidades(mission)['offset'],False),
                                 ('sparse',sparse_fixture(),0,False),
                                 ('empty',struct.pack('<HH',0,784),0,False),
                                 ('missing_modifier',sparse_fixture(),0,True)):
        selections = bytes((i*23+0x53)&255 for i in range(2048))
        native.carregar(data,offset,b'\xa5'*220800,b'\x11\x22\x33\x44',types,bonuses,
                        parar_bonus=stop,selecoes=selections)
        pool,flags = native.estado()
        cases.append(dict(name=name,input_sha256=hashlib.sha256(data).hexdigest(),offset=offset,
                          dependency_stop=stop,cursor=native.cursor,selections_hex=native.estado_selecoes().hex(),
                          unit_pool_sha256=hashlib.sha256(pool).hexdigest(),loader_bytes_hex=flags.hex()))
    report = dict(original_sha256=HASH_ESTUDADO,cases=cases,native_fixtures=native.loads,
                  returns=native.returned,expected_modifier_stops=native.dependency_stops,
                  bounded_segments=native.execucoes,selection_pattern='(i*23+0x53)&255',
                  scope='Complete LoadEngin entry with actual SelectionInit; successful I/O only; explicit inherited pools, loaded types/bonuses. No world/mission initialization.')
    (OWNED/'evidencias/captura-selecao-carga-original.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    r=capturar()
    print('Original selection/load fixtures:',r['native_fixtures'],'segments:',r['bounded_segments'])
