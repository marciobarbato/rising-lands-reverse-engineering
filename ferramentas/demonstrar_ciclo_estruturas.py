"""Demonstrate explicit pool lifecycle and caller-prepared gate placement."""
import hashlib
import json
from pathlib import Path
import struct
from navegacao_unidades import MundoNavegacao


def demonstrar():
    mundo = MundoNavegacao()
    mundo.estruturas[:] = b'\xa5' * 276000
    mundo.inicializar_registros_estruturas()
    eventos = [dict(stage='startup_prefix', first_free=mundo.buscar_estrutura_livre(),
                    pool_sha256=hashlib.sha256(mundo.estruturas).hexdigest())]
    indice = mundo.buscar_estrutura_livre()
    assert mundo.buscar_estrutura_livre() == indice == 0  # query does not reserve
    # Explicit fixture, not a reconstruction of CreerBatiment's remaining body.
    struct.pack_into('<H', mundo.estruturas, 2, 0x505)
    mundo.estruturas[4], mundo.estruturas[5], mundo.estruturas[8] = 1, 2, 12
    mundo.objetos[0x504] = mundo.objetos[0x506] = mundo.objeto_muro
    mundo.colocar_estrutura(indice)

    def registrar(nome):
        eventos.append(dict(stage=nome, first_free=mundo.buscar_estrutura_livre(),
                            record_state=mundo.estruturas[5], record_type=mundo.estruturas[8],
                            counter=mundo.estruturas[0x76],
                            orientation=struct.unpack_from('<H', mundo.estruturas, 0x7c)[0],
                            object=mundo.objetos[0x505], attributes=mundo.atributos[0x505],
                            region=mundo.regioes[0x505]))

    registrar('caller_prepared_gate_placed')
    mundo.estruturas[0x76] = 7
    mundo.resetar_estrutura(indice)
    registrar('single_reset_retains_counter_and_terrain')
    mundo.resetar_todas_estruturas()
    registrar('pool_reset_requires_separate_world_teardown')
    return dict(x86_executed=False,
                scope='Synthetic caller-prepared gate; pool reset is not demolition or terrain teardown.',
                events=eventos)


if __name__ == '__main__':
    destino = Path(__file__).resolve().parents[1] / 'relatorios/ciclo-estruturas-python.json'
    destino.write_text(json.dumps(demonstrar(), indent=2) + '\n')
    print(destino)
