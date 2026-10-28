"""Synthetic unit pool reset while inherited physical/search state remains."""
import json
from pathlib import Path

from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca


def demonstrar():
    m=MundoNavegacao()
    p=7*276
    m.unidades[p+1],m.unidades[p+2],m.unidades[p+0xaf],m.unidades[p+0xbd]=7,4,53,1
    m.palavra(7,8,0x505);m.palavra(7,0x9a,123)
    m.unidades[p+0x6a:p+0x70]=b'\xa5'*6
    m.palavra(0,0x9a,222)
    m.unidades[0xaf]=99
    m.bolsas_tipos_unidades=[bytearray(b'\xa5'*2704) for _ in range(4)]
    m.busca=ContextoBusca(7,1,1,0x12345678,77)
    m.ocupar(7,0x505,True)
    m.resetar_todas_unidades()
    return dict(x86_executed=False,nonzero_record=dict(state=m.unidades[p+2],life=m.palavra(7,0x9a),
                  experience=m.unidades[p+0xaf],selection_flag=m.unidades[p+0xbd],
                  bag_reserved_hex=m.unidades[p+0x6a:p+0x70].hex()),
                zero_state_record=dict(life=m.palavra(0,0x9a),experience=m.unidades[0xaf]),
                inherited_collision=m.atributos[0x505],inherited_region=m.regioes[0x505],
                inherited_search=vars(m.busca).copy(),
                last_table_reserved_hex=m.bolsas_tipos_unidades[3][25*104+0x60:25*104+0x66].hex(),
                scope='Synthetic complete raw pool reset; physical/search/selection retained, '
                      'no mission loading, remap, teardown or insertion.')


if __name__ == '__main__':
    destino=Path(__file__).resolve().parents[1]/'relatorios/ciclo-unidades-python.json'
    destino.write_text(json.dumps(demonstrar(),indent=2)+'\n')
    print(destino)
