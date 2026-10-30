"""Current pixel/argument/display-effect/logic-guard replay over immutable scripted probe recordings."""
import argparse,json
from pathlib import Path
import validar_colheita_graficos as chain
import validar_janelas_api18 as prior

chain.PARTS.update(prior.PARTS);chain.LIMITS.update(prior.LIMITS);chain.SHARED.update(prior.SHARED)

def main(a):
    reports={}
    for probe in a.probe:reports[probe]=chain.executar(probe,dependencies=reports)
    names=('render_quadro.py','quadro_jogo.py','hud_quadro.py','sobreposicoes_entrada_m3.py','cave_scriptada_m3.py',
        'hud_scriptado_m3.py','camadas_exibicao_m3.py','camadas_m3_api18.json','camadas_colheita_m3.json',
        'efeitos_logicos_exibicao.py','validar_colheita_graficos.py','validar_cadeia_exibicao_atual.py')
    result=dict(schema='rising-lands/current-display-chain-comparison/1',
        boundary_contract='strict recorded AffText non-execution; no default glyph provider',
        sources_sha256={n:chain.sha((chain.AQUI/n).read_bytes()) for n in names},windows=[chain.public(r) for r in reports.values()])
    Path(a.output).write_text(json.dumps(result,indent=1)+'\n')
    print([(w['probe'],w['equal'],w['drawn_total'],w['first_stop']) for w in result['windows']],flush=True)
    if any(w['equal']!=w['drawn_total'] or w['first_stop'] for w in result['windows']):raise SystemExit(1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--probe',action='append',choices=tuple(chain.PARTS),required=True)
    p.add_argument('--output',required=True);main(p.parse_args())
