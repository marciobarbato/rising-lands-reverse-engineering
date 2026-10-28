"""Synthetic remap reset with its explicit pending allocation boundary."""
from dataclasses import asdict
import json
from pathlib import Path

from capturar_remapeamento_mundo import preparar_remapeamento


def main():
    m = preparar_remapeamento()
    unidade,atributos = bytes(m.unidades),bytes(m.atributos)
    c = m.cores_estruturas
    aliases = (m.regioes,c.grade,c.livres,c.liberadas)
    pedido = m.iniciar_remapeamento()
    report = dict(scope='Synthetic pre-allocation reset only; no x86 or actual mission',
                  pending=asdict(pedido),search=vars(m.busca).copy(),
                  cleared_regions=not any(m.regioes),cleared_colors=not any(c.grade),
                  free_color_count=c.livres[0],released_status_values=sorted(set(c.liberadas)),
                  unit_pool_retained=bytes(m.unidades) == unidade,
                  terrain_attributes_retained=bytes(m.atributos) == atributos,
                  allocation_aliases_retained=all(a is b for a,b in zip(aliases,(m.regioes,c.grade,c.livres,c.liberadas))))
    p = Path(__file__).resolve().parents[1]/'relatorios/remapeamento-mundo-demonstracao.json'
    p.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
