"""Synthetic joined economy preparation and core conversion on shared buffers."""
import json
from pathlib import Path
import struct
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'pesquisas-paralelas/economia'))
try:
    from construcoes import EconomiaConstrucoes
    from recrutamento import Recrutamento
    from saida_tropa import SaidaTropa
    from bonus_unidades import BonusUnidades, capacidade_tipo
finally:
    sys.path.remove(str(RAIZ / 'pesquisas-paralelas/economia'))
from navegacao_unidades import MundoNavegacao
from ordens_unidades import ContextoBusca
from conversao_unidades import retomar_conversao_saida


def bag(memoria, base, entradas):
    struct.pack_into('<HH', memoria, base, len(entradas), 30)
    struct.pack_into('<H', memoria, base+0x66, len(entradas))
    for slot, (modo, valor) in enumerate(entradas):
        struct.pack_into('<H', memoria, base+6+slot*2, valor)
        memoria[base+0x42+slot] = modo


def demonstrar():
    mundo = MundoNavegacao()
    economico = EconomiaConstrucoes(estruturas=bytes(276000))
    economico.estruturas = mundo.estruturas
    recrutamento = Recrutamento(economico)
    recrutamento.unidades = mundo.unidades  # explicit shared identity, not copies
    s, u = 7*276, 799*276
    mundo.estruturas[s+4], mundo.estruturas[s+8], mundo.estruturas[s+0x7b] = 0, 1, 7
    struct.pack_into('<H', mundo.estruturas, s+2, 0x505)
    struct.pack_into('<I', mundo.estruturas, s+0x8c, 1000)
    bag(mundo.estruturas, s+0xc, ((1, 799),))
    mundo.unidades[u], mundo.unidades[u+1], mundo.unidades[u+2] = 0, 9, 14
    mundo.unidades[u+0x8a] = 2
    struct.pack_into('<H', mundo.unidades, u+0x9a, 50)
    bag(mundo.unidades, u+0xa, ((2, 2), (2, 1), (2, 0)))
    mundo.busca = ContextoBusca(799, 1, 1, 123, 77)
    for off, valor in ((0, 10), (0x2a, 5), (0x2c, 36), (0x30, 100)):
        struct.pack_into('<H', recrutamento.tipos_unidades, 7*50+off, valor)
    economico.capacidades.configurar(0, 1, 100)
    pedido = SaidaTropa(recrutamento).preparar(7, 9)
    eventos = [dict(stage='economic_preparation', unit_type=mundo.unidades[u+1],
                    balance=list(economico.economia.consultar(0)), pending_address=hex(pedido.endereco_dependencia))]
    # Actual committed economic query providers, with an explicitly synthetic
    # loaded zero bonus table. No competing query implementation lives here.
    bonus = BonusUnidades(bytes(1872))
    convertido = retomar_conversao_saida(mundo, pedido, recrutamento.tipos_unidades,
                                        capacidade_tipo=capacidade_tipo, modificador=bonus.consultar)
    eventos.append(dict(stage='local_conversion_before_healing', unit_type=mundo.unidades[u+1],
                        cell=convertido.celula, state=mundo.unidades[u+2],
                        life=struct.unpack_from('<H', mundo.unidades, u+0x9a)[0],
                        attack_phase=mundo.unidades[u+0x8a], wait_byte=mundo.unidades[u+0x8b],
                        search=[mundo.busca.unidade, mundo.busca.ocupada, mundo.busca.sucesso,
                                mundo.busca.ponteiro_rota, mundo.busca.concluida],
                        bag_count=struct.unpack_from('<H', mundo.unidades, u+0xa)[0],
                        bag_capacity=struct.unpack_from('<H', mundo.unidades, u+0xc)[0],
                        pending_address=hex(convertido.endereco_dependencia)))
    return dict(x86_executed=False, shares_unit_and_structure_buffers=True,
                scope='Synthetic integration stops before healing/fatigue/experience/exit/movement/cleanup; '
                      'no complete unit production, occupancy or mission execution.', events=eventos)


if __name__ == '__main__':
    destino = RAIZ / 'relatorios/saida-tropa-compartilhada-python.json'
    destino.write_text(json.dumps(demonstrar(), indent=2) + '\n')
    print(destino)
