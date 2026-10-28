"""Synthetic committed economy/conversion/recovery on shared live buffers."""
import json
from pathlib import Path
import struct

from demonstrar_saida_tropa import (MundoNavegacao, EconomiaConstrucoes, Recrutamento,
                                    SaidaTropa, BonusUnidades, capacidade_tipo, bag)
from conversao_unidades import retomar_conversao_saida
from recuperacao_unidades import retomar_recuperacao_saida


def demonstrar():
    mundo = MundoNavegacao()
    economico = EconomiaConstrucoes(estruturas=bytes(276000))
    economico.estruturas = mundo.estruturas
    recrutamento = Recrutamento(economico)
    recrutamento.unidades = mundo.unidades
    s, u = 7*276, 799*276
    mundo.estruturas[s+4], mundo.estruturas[s+8], mundo.estruturas[s+0x7b] = 0, 1, 7
    struct.pack_into('<H', mundo.estruturas, s+2, 0x505)
    struct.pack_into('<I', mundo.estruturas, s+0x8c, 1000)
    bag(mundo.estruturas, s+0xc, ((1, 799),))
    mundo.unidades[u], mundo.unidades[u+1], mundo.unidades[u+2] = 0, 9, 14
    mundo.palavra(799, 0x9a, 50)
    mundo.palavra(799, 0x74, 500)
    mundo.palavra(799, 0x76, 0x1234)
    bag(mundo.unidades, u+0xa, ((2, 2), (2, 1), (2, 0)))
    for off, valor in ((0, 10), (8, 100), (0x2a, 5), (0x2c, 36), (0x30, 100)):
        struct.pack_into('<H', recrutamento.tipos_unidades, 7*50+off, valor)
    economico.capacidades.configurar(0, 1, 100)
    pedido = SaidaTropa(recrutamento).preparar(7, 9)
    bonus = BonusUnidades(bytes(1872))
    convertido = retomar_conversao_saida(mundo, pedido, recrutamento.tipos_unidades,
                                        capacidade_tipo=capacidade_tipo, modificador=bonus.consultar)
    vida_antes = mundo.palavra(799, 0x9a)
    recuperado = retomar_recuperacao_saida(mundo, convertido, recrutamento.tipos_unidades)
    return dict(x86_executed=False, shares_unit_and_structure_buffers=True,
                life_before=vida_antes, life_after=mundo.palavra(799, 0x9a),
                fatigue_after=mundo.palavra(799, 0x74), copied_word=mundo.palavra(799, 4),
                unit_type=mundo.unidades[u+1], exit_cell=recuperado.celula,
                pending_address=hex(recuperado.endereco_dependencia),
                scope='Synthetic economy preparation, positioning, conversion, healing and fatigue; '
                      'stops before experience/placement/movement/audio/cleanup; no real mission.')


if __name__ == '__main__':
    destino = Path(__file__).resolve().parents[1] / 'relatorios/recuperacao-saida-python.json'
    destino.write_text(json.dumps(demonstrar(), indent=2) + '\n')
    print(destino)
