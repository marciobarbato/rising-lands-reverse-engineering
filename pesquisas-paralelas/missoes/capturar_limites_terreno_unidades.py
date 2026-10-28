"""Original-only placement-prefix query/vision boundary observations."""
import json
import struct
from ambiente_missoes import OWNED
from analisar import HASH_ESTUDADO
from capturar_terreno_unidades import preparar_caso,resumo_original


def capturar(chamador=False):
    from bancada_terreno_unidades import BancadaTerrenoUnidades
    native=BancadaTerrenoUnidades();cases=[]
    for name,address in (('missing_bonus',0x428cc0),('vision9',0x457019 if chamador else 0x476851)):
        args=list(preparar_caso('ordinary'))
        if name=='vision9':
            types=bytearray(args[3]);struct.pack_into('<H',types,42,9);args[3]=types
        native.carregar_caso(*args)
        regs=native.prefixo(address)
        cases.append(dict(name=name,checkpoint=hex(regs['EIP']),output=resumo_original(native)))
    report=dict(original_sha256=HASH_ESTUDADO,cases=cases,bounded_segments=native.execucoes,
                vision_stop='before caller CALL' if chamador else 'at callee entry; trace includes attempted discovery entry',
                scope='Original-only intentional bonus/discovery entry stops; explicit synthetic physical fixture, no dependency effect substituted or mission completion.')
    filename='captura-terreno-unidades-limites-chamador.json' if chamador else 'captura-terreno-unidades-limites.json'
    (OWNED/'evidencias'/filename).write_text(json.dumps(report,indent=2)+'\n')
    return report


def capturar_monde01():
    """Align the real stream's radius10 dependency with its caller checkpoint."""
    from bancada_terreno_unidades import BancadaTerrenoUnidades
    native=BancadaTerrenoUnidades()
    native.carregar_caso(*preparar_caso('MONDE01'))
    regs=native.prefixo(0x457019,15)
    report=dict(original_sha256=HASH_ESTUDADO,name='MONDE01',unit_index=15,
                checkpoint=hex(regs['EIP']),output=resumo_original(native),
                bounded_segments=native.execucoes,
                scope='Actual MONDE01 unit stream, synthetic inherited physical state; stop before radius10 discovery CALL for unit15, after its collision and visibility stores. Earlier seven insertions retained; no replay or wider provider claim.')
    (OWNED/'evidencias/captura-terreno-unidades-monde01-limite.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    print('Original placement boundaries:',len(capturar()['cases']))
    print('Original caller-aligned boundaries:',len(capturar(True)['cases']))
    print('MONDE01 dependency:',capturar_monde01()['checkpoint'])
