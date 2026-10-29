"""M2.2 coverage probe (Python only, no native run): N frames composed on one map, checked against Core's
native 0..128-frame survey.

    python3 -B pesquisas-paralelas/ia-runtime/percorrer_quadros_ia.py --quadros 128 \
        --saida .local/m2-2-percurso-128.json [--planejamento]

The composition is ``composicao_quadros_ia`` (mode 'prova', no crossing). At every frame end it compares
the indicators of ``evidencias/fundacoes-quadro/levantamento-quadros-exibicao.json`` (Core, ca5a7f3): the
counter, game frame, world and AI RNGs, CRT seed, permutation cursor 0x4e1d18 and view origin. The survey's
state hash covers display bytes too, so it is not compared.

Call counts: the composition's checkpoint routines (``PONTOS``) are counted per frame and compared with the
survey's entry counts of the same routines (entries anywhere in the frame phase).

AffGame check: the survey records the routines entered in each between-frames phase. In the original,
Cyclage is entered exactly when AffGame takes the +0x815 path that stores 1 into the HUD flag 0x4e05a2.
AffTerrain is entered exactly when the body is drawn, and not on the +0x28d early return. Both are compared
with ``affgame_hud_ia``'s result.

``--planejamento`` records a Graphics drawing-domain stop (``DependenciaExibicao``) and continues, taking the
drawing as writing nothing outside display. Such a run is coverage planning, not evidence. It is refused
for any output outside ``.local/``. Without the flag, the first stop of any owner ends the run.
"""
import argparse
import json
import subprocess
import sys
import time

from ambiente_ia_runtime import ROOT
from composicao_encadeada_ia import PONTOS
from composicao_quadros_ia import ComposicaoQuadros, carregar_cenario_exibicao, indicadores
from efeitos_logicos_exibicao import DependenciaExibicao
from reinicio_ia import DependenciaIA

LEVANTAMENTO = ROOT / 'evidencias/fundacoes-quadro/levantamento-quadros-exibicao.json'


def entradas_entre_quadros(quadro):
    """Routine entry counts of the between-frames phase that precedes frame k in the survey."""
    return next((v for f, v in quadro.get('entries', {}).items() if f.startswith('between_frames')), None)


def percorrer(n, planejamento=False):
    levantamento = json.loads(LEVANTAMENTO.read_bytes())
    por_quadro = {q['frame']: q for q in levantamento['frames']}
    estados, cap, entrada, m1 = carregar_cenario_exibicao()
    comp = ComposicaoQuadros(estados['s0'], cap, entrada, m1, planejamento=planejamento)
    quadros, hud, parada = [], [], None
    t0 = time.monotonic()
    try:
        for r in comp.executar(n):
            fase = r['phase']
            if fase.startswith('between_frames'):
                k = int(fase[len('between_frames'):] or 1)
                aff = [x for x in comp.ctx.raizes_nao_executadas if x['phase'] == fase and x['routine'] == 'AffGame'][-1]
                cicla = any(v == 1 for _, _, v in aff['writes'])
                nativo = entradas_entre_quadros(por_quadro.get(k, {}))
                hud.append(dict(frame=k, affgame_counter=dict(aff['reads'])['counter'], drew=aff['drew'],
                                hud_flag_writes=aff['writes'], eax=aff['eax'],
                                survey_cyclage=None if nativo is None else 'Cyclage' in nativo,
                                survey_drew=None if nativo is None else 'AffTerrain' in nativo,
                                equal=None if nativo is None else
                                ('Cyclage' in nativo) == cicla and ('AffTerrain' in nativo) == aff['drew']))
            elif fase.startswith('frame'):
                k = int(fase[len('frame'):])
                python, nativo = indicadores(comp.mapa), por_quadro.get(k)
                diferencas = None if nativo is None else {c: dict(python=python[c], survey=nativo[c])
                                                          for c in python if python[c] != nativo[c]}
                chamadas = {}
                for (f, rotina, _), n in comp.travessias.contagem.items():
                    if f == fase:
                        chamadas[rotina] = chamadas.get(rotina, 0) + n
                entradas = next((v for f, v in (nativo or {}).get('entries', {}).items() if f.startswith('frame')),
                                None)
                contagens = None if entradas is None else {
                    rotina: dict(python=chamadas.get(rotina, 0), survey=entradas.get(rotina, 0))
                    for rotina in sorted(set(chamadas) | (set(entradas) & set(PONTOS)))
                    if chamadas.get(rotina, 0) != entradas.get(rotina, 0)}
                quadros.append(dict(frame=k, indicators=python, equal=None if nativo is None else not diferencas,
                                    differences=diferencas, checkpoint_routine_calls=chamadas,
                                    call_count_differences=contagens))
                if diferencas:
                    parada = dict(kind='indicator_difference', phase=fase, differences=diferencas)
                    break
    except DependenciaIA as erro:
        parada = dict(kind='dependency', routine=erro.rotina, site=hex(erro.sitio))
    except DependenciaExibicao as erro:
        parada = dict(kind='graphics_dependency', routine=erro.rotina, site=hex(erro.sitio), reason=erro.motivo)
    except Exception as erro:  # reported, never swallowed: the run stops here
        import traceback
        parada = dict(kind=type(erro).__name__, message=str(erro)[:400], traceback=traceback.format_exc()[-2500:])
    ultimo = quadros[-1]['frame'] if quadros else 0
    return dict(
        schema='rising-lands/ai-runtime-m2.2-python-frames-probe/1', evidence=False, native_run=False,
        planning_bypass_of_graphics_stops=planejamento, frames_requested=n, frames_completed=ultimo,
        survey=dict(path=str(LEVANTAMENTO.relative_to(ROOT)), source_revision=levantamento['source_revision']),
        first_stop=parada, frames_equal=sum(1 for q in quadros if q['equal']),
        hud=dict(calls=len(hud), equal=sum(1 for h in hud if h['equal']), records=hud),
        graphics_planning_stops=comp.ctx.paradas_planejamento,
        graphics_planning_stop_summary=sorted({(p['site'], p['reason'].split(':')[0]) for p in
                                               comp.ctx.paradas_planejamento}),
        frames=quadros, seconds=round(time.monotonic() - t0, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, required=True)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--planejamento', action='store_true')
    a = ap.parse_args()
    saida = ROOT / a.saida
    if a.planejamento and not saida.resolve().is_relative_to((ROOT / '.local').resolve()):
        raise SystemExit('A planning run (Graphics stops bypassed) writes under .local/ only')
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    rel = percorrer(a.quadros, a.planejamento)
    rel['source_revision'] = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True,
                                            text=True).stdout.strip()
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1, default=str)
        f.write('\n')
    print(json.dumps({k: rel[k] for k in ('frames_completed', 'frames_equal', 'first_stop', 'seconds',
                                           'graphics_planning_stop_summary')} | dict(
        hud={k: rel['hud'][k] for k in ('calls', 'equal')}), indent=1, default=str))
    return 0


if __name__ == '__main__':
    sys.exit(main())
