"""Two synthetic conditional-request outcomes after the placement handoff."""
from dataclasses import asdict
import json
from pathlib import Path
import struct

from capturar_colocacao_saida import preparar_saida
from colocacao_saida import ColocacaoSaidaTropa
from voz_unidades import retomar_solicitacao_saida,DependenciaVozUnidade


def demonstrar():
    m=preparar_saida(tipo=7)
    m.palavra(7,8,0x808)
    m.descoberto[0][0x808]=0
    struct.pack_into('<I',m.unidades,7*276+0x104,0xffffffff)
    pedido=ColocacaoSaidaTropa(7,7,0x808,7,0x909)
    m.estruturas[7*276+4]=3
    final=retomar_solicitacao_saida(m,pedido)
    m.estruturas[7*276+4]=0
    try:
        retomar_solicitacao_saida(m,pedido,janela=(0,0,16,16))
    except DependenciaVozUnidade as d:
        pendente=dict(checkpoint=hex(d.checkpoint),dependency=hex(d.endereco),request=asdict(d.solicitacao))
    else:
        raise AssertionError('Inactive visible sound handle must retain a pending insertion')
    return dict(x86_executed=False,foreign_owner_cleanup_boundary=hex(final.endereco_dependencia),
                own_visible_request=pendente,flag_after=m.unidades[7*276+0xf9],
                scope='Two synthetic placement handoffs only; no audio insertion/playback or economic cleanup.')


if __name__ == '__main__':
    destino=Path(__file__).resolve().parents[1]/'relatorios/solicitacao-saida-python.json'
    destino.write_text(json.dumps(demonstrar(),indent=2)+'\n')
    print(destino)
