"""Synthetic physical mission insertion using a prepared shared world."""
import json
from pathlib import Path

from capturar_colocacao_saida import preparar_saida


def main():
    mundo = preparar_saida(tipo=1,dono=0,estado=4)
    antes = dict(current=mundo.palavra(7,8),step=mundo.palavra(7,0x7c),
                 destination=mundo.palavra(7,0x7e),search=vars(mundo.busca).copy())
    mundo.colocar_unidade_missao(7)
    depois = dict(current=mundo.palavra(7,8),step=mundo.palavra(7,0x7c),
                  destination=mundo.palavra(7,0x7e),search=vars(mundo.busca).copy())
    resultado = dict(scope='Synthetic prepared record, no mission loader or x86',
                     exists=mundo.existe_unidade(7),raw_visibility=mundo.visibilidade_unidade(7),
                     state=mundo.unidades[7*276+2],before=antes,after=depois,
                     orders_and_search_preserved=antes == depois,
                     current_collision=mundo.atributos[0x505],old_step_collision=mundo.atributos[0x506])
    destino = Path(__file__).resolve().parents[1]/'relatorios/colocacao-missao-demonstracao.json'
    destino.write_text(json.dumps(resultado,indent=2)+'\n')
    print(json.dumps(resultado,indent=2))


if __name__ == '__main__':
    main()
