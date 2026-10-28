"""Synthetic physical exit followed by the existing movement-order body."""
import json
from pathlib import Path
import struct

from capturar_colocacao_saida import preparar_saida
from experiencia_unidades import ExperienciaSaidaTropa
from colocacao_saida import retomar_colocacao_saida


def demonstrar():
    m = preparar_saida(tipo=7)
    struct.pack_into('<H', m.estruturas, 7*276+0x7c, 0x909)
    pedido = ExperienciaSaidaTropa(7,7,0x808,7)
    r = retomar_colocacao_saida(m,pedido)
    return dict(x86_executed=False, pending_address=hex(r.endereco_dependencia),
                current_cell=m.palavra(7,8), step_cell=m.palavra(7,0x7c), destination=m.palavra(7,0x7e),
                state=m.unidades[7*276+2], enabled=m.unidades[7*276+0x72],
                search_completion=m.busca.concluida,
                old_collision_retained=[m.atributos[c] for c in (0x505,0x506)],
                new_collision=m.atributos[0x808],
                scope='Synthetic original exit/order effects; no movement advancement, request/audio, '
                      'economic cleanup or real mission.')


if __name__ == '__main__':
    destino=Path(__file__).resolve().parents[1]/'relatorios/colocacao-saida-python.json'
    destino.write_text(json.dumps(demonstrar(),indent=2)+'\n')
    print(destino)
