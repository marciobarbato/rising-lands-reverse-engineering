"""Package and summarize an M3 probe: two native runs of one input file -> committed capture + findings report.

For probe P it reads the runs ``.local/m3/sondas/P-a`` and ``P-b`` (``entrada_roteirizada.py correr``) and writes
``sondas/P/``:

* ``replay.json``: the replay check (the four record files equal once ``seconds`` is dropped);
* run a's ``resumo.json`` and its record files as ``*.jsonl.xz`` (the capture);
* ``relatorio.json``: orders issued (SetPlayerOrdre/ProcessInputGame), routines first entered that the no-input
  run to frame 9,200 never enters (Core ``runs/core/coverage-9200`` 7193999, ``relatorios/
  cobertura-quadros-exibicao-9200.json``) with first frame, phase and caller, and the objective trace at the
  frames where it changes (resources, structures, the UI bytes and the followed units).

    python3 -B pesquisas-paralelas/missoes/m3/relatorio_sondas.py P1 --cobertura .local/m3/cobertura-9200.json
"""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import shutil
import sys

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import entrada_roteirizada as er  # noqa: E402

ROOT = er.ROOT
COBERTURA = dict(branch='runs/core/coverage-9200', commit='71939991cb06e9d23c059e1d422830ba996d2f23',
                 path='relatorios/cobertura-quadros-exibicao-9200.json')


def _linhas(caminho):
    with open(caminho) as f:
        for x in f:
            yield json.loads(x)


def replay(a, b):
    r = {}
    for nome in er.SAIDAS:
        la = [json.dumps({k: v for k, v in d.items() if k != 'seconds'}, sort_keys=True) for d in _linhas(a / nome)]
        lb = [json.dumps({k: v for k, v in d.items() if k != 'seconds'}, sort_keys=True) for d in _linhas(b / nome)]
        r[nome] = dict(lines=[len(la), len(lb)], equal=la == lb,
                       sha256=hashlib.sha256('\n'.join(la).encode()).hexdigest())
    r['equal'] = all(v['equal'] for v in r.values())
    return r


def mudancas(quadros):
    """Objective-trace values at the frames where they change (first frame listed)."""
    chaves = ('food', 'stone', 'parts', 'structures', 'ui', 'marks', 'al', 'victory_counter')
    saida, anterior = [], None
    for d in quadros:
        o = d['objective']
        atual = {k: o[k] for k in chaves}
        atual['units'] = {i: {c: u[c] for c in ('cell', 'state', 'target_b2', 'b7', 'b8', 'be', 'f110')}
                          for i, u in o['units'].items()}
        atual['selection'], atual['view_origin'] = d['selection'], d['view_origin']
        if atual != anterior:
            dif = atual if anterior is None else {k: v for k, v in atual.items() if v != anterior[k]}
            if 'units' in dif and anterior is not None:
                dif['units'] = {i: u for i, u in dif['units'].items() if u != anterior['units'][i]}
            saida.append(dict(frame=d['frame'], **dif))
        anterior = atual
    return saida


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('sonda')
    ap.add_argument('--cobertura', required=True, help='local copy of the no-input coverage summary')
    ap.add_argument('--execucoes', default='.local/m3/sondas')
    a = ap.parse_args()
    ra, rb = ROOT / a.execucoes / f'{a.sonda}-a', ROOT / a.execucoes / f'{a.sonda}-b'
    destino = AQUI / 'sondas' / a.sonda
    destino.mkdir(parents=True, exist_ok=True)
    resumo_a, resumo_b = (json.loads((r / 'resumo.json').read_text()) for r in (ra, rb))
    rep = replay(ra, rb)
    rep.update(runs=[dict(status=r['status'], frames=r['frames_run'], seconds=r['seconds'],
                          input_sha256=r['input_sha256']) for r in (resumo_a, resumo_b)])
    (destino / 'replay.json').write_text(json.dumps(rep, indent=1, sort_keys=True) + '\n')
    bruto_cob = Path(a.cobertura).read_bytes()
    base = set(json.loads(bruto_cob)['routines'])
    novas = {n: r for n, r in resumo_a['routines_first_entered'].items() if n not in base}
    quadros = list(_linhas(ra / 'quadros.jsonl'))
    comandos = list(_linhas(ra / 'comandos.jsonl'))
    relatorio = dict(
        schema='rising-lands/m3-probe-report/1', probe=a.sonda, evidence='original-only native capture',
        input=resumo_a['input_file'], input_sha256=resumo_a['input_sha256'], status=resumo_a['status'],
        frames=[quadros[0]['frame'], quadros[-1]['frame']] if quadros else [], replay_equal=rep['equal'],
        seconds=[resumo_a['seconds'], resumo_b['seconds']],
        baseline=dict(COBERTURA, sha256=hashlib.sha256(bruto_cob).hexdigest(), routines=len(base)),
        orders=[{k: c[k] for k in c if k not in ('phase',)} for c in comandos if c['event'] == 'SetPlayerOrdre'],
        process_input_game=[{k: c[k] for k in ('frame', 'tag', 'packet', 'jump_target', 'jump_target_routine')}
                            for c in comandos if c['event'] == 'ProcessInputGame'],
        routines_first_entered_beyond_no_input=dict(sorted(novas.items(), key=lambda x: (x[1]['first_frame'], x[0]))),
        routines_first_entered_total=len(resumo_a['routines_first_entered']),
        objective_changes=mudancas(quadros), stop=resumo_a.get('stop'))
    (destino / 'relatorio.json').write_text(json.dumps(relatorio, indent=1, sort_keys=True) + '\n')
    shutil.copy(ra / 'resumo.json', destino / 'resumo.json')
    for nome in er.SAIDAS:
        (destino / (nome + '.xz')).write_bytes(lzma.compress((ra / nome).read_bytes(), preset=9))
    print(json.dumps(dict(probe=a.sonda, replay_equal=rep['equal'], frames=relatorio['frames'],
                          orders=[(o['frame'], o['tag'], o['word2'], o['word4']) for o in relatorio['orders']],
                          new_beyond_no_input=len(novas)), indent=1))


if __name__ == '__main__':
    main()
