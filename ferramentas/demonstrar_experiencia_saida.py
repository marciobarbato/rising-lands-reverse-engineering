"""Synthetic recovery handoff consumed through the live experience queue."""
import json
from pathlib import Path
import struct

from ordens_unidades import MundoUnidades
from recuperacao_unidades import RecuperacaoSaidaTropa
from experiencia_unidades import retomar_experiencia_saida


def demonstrar():
    mundo = MundoUnidades()
    tipos = bytearray(1300)
    mundo.unidades[799*276+1] = 4
    struct.pack_into('<H', tipos, 4*50+0x2e, 65535)
    mundo.experiencias_unidades[:10] = bytes((4, 0x81, 9, 3, 8, 4, 7, 5, 6, 6))
    pedido = RecuperacaoSaidaTropa(7, 799, 0x808, 4)
    resultado = retomar_experiencia_saida(mundo, pedido, tipos)
    return dict(x86_executed=False, experience_byte=mundo.unidades[799*276+0xaf],
                f8=mundo.unidades[799*276+0xf8], queue_after=list(mundo.experiencias_unidades[:10]),
                exit_cell=resultado.celula, pending_address=hex(resultado.endereco_dependencia),
                scope='Synthetic live owner queue and recovery handoff; stops before placement; no real mission.')


if __name__ == '__main__':
    destino = Path(__file__).resolve().parents[1] / 'relatorios/experiencia-saida-python.json'
    destino.write_text(json.dumps(demonstrar(), indent=2) + '\n')
    print(destino)
