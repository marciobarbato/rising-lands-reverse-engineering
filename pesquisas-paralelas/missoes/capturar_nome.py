"""Original-only filename and query-checkpoint observations before translation."""
import json
import struct
from ambiente_missoes import OWNED
from analisar import HASH_ESTUDADO


def jogadores_sinteticos(values):
    players=bytearray((i*13+0x53)&255 for i in range(80))
    for owner,value in enumerate(values,1):
        struct.pack_into('<H',players,owner*20+12,value&65535)
    return players


def capturar():
    from bancada_nome import BancadaNomeMissao
    native=BancadaNomeMissao()
    cases=[]
    for number,variant,values,stop in ((1,3,(90,90,90),None),(9,0,(90,90,90),None),
                                       (9,3,(90,90,90),None),(10,2,(90,90,90),None),
                                       (12,1,(127,-128,-1),None),(17,0,(-1,-2,-3),2),
                                       (0x12340104,2,(0,0,0),None),(255,0,(0,0,0),None)):
        players=jogadores_sinteticos(values)
        regs=native.nome(number,variant,players,b'\xa5'*64,stop_query=stop)
        output,after_players=native.estado()
        if after_players!=players:
            raise ValueError('Unexpected original player-table mutation')
        cases.append(dict(number=number,variant=variant,values=values,stop_query=stop,
                          output_hex=output.hex(),queries=native.queries,checkpoint=hex(regs['EIP'])))
    report=dict(original_sha256=HASH_ESTUDADO,native_calls=native.calls,bounded_segments=native.execucoes,
                returns=native.returned,expected_query_stops=native.dependency_stops,cases=cases,
                scope='Original filename bytes and real read-only sympathy queries; synthetic inherited destination and loaded player table. No file-open or campaign execution.')
    (OWNED/'evidencias/captura-nome-original.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    r=capturar();print('Original filename calls:',r['native_calls'],'query stops:',r['expected_query_stops'])
