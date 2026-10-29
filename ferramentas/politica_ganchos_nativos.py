"""Comparison policy pass 2 with native hooks: runtime injection into Missions' tooling, and validation.

Missions owns ``politica_comparacao_quadros`` and ``segmentos_quadros_missao``;
this Core script reuses them read-only.  Both look ``ganchos`` up on the
policy module at call time (``passo2`` and ``politica_segmento``), so
replacing ``politica_comparacao_quadros.ganchos`` with
``ganchos_nativos.ganchos_politica`` in this process swaps the Python hook
closures for the native library; nothing else changes.  ``--metodo python``
keeps Missions' own closures (the reference method, for timing).

    # whole run (pass 1 + native pass 2), compared with the committed M2.2 report
    python3 -B ferramentas/politica_ganchos_nativos.py sequencial --quadros 128 \
        --saida .local/nativo-politica/m2-2-nativo.json
    # one policy segment of a Missions segment directory (passo-a + preparar-politica done)
    python3 -B ferramentas/politica_ganchos_nativos.py segmento --dir .local/nativo-politica/seg-nativo \
        --de 0 --ate 32 --metodo nativo
    # join the segments and compare with the committed report
    python3 -B ferramentas/politica_ganchos_nativos.py comparar --dir .local/nativo-politica/seg-nativo

Outputs stay under ``.local/`` (not evidence).  Native processes end with
``encerramento_captura.encerrar_captura``.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

RAIZ = Path(__file__).resolve().parents[1]
MISSOES = RAIZ / 'pesquisas-paralelas/missoes'
for caminho in (RAIZ / 'ferramentas', MISSOES):
    if str(caminho) not in sys.path:
        sys.path.insert(0, str(caminho))
import ambiente_missoes  # noqa: E402,F401  (Missions' provider paths)

REFERENCIA = MISSOES / 'validacao/m2-2-politica-comparacao-128-quadros.json'
SHA_REFERENCIA = 'bf36e6e8f6a38202fa3248256d3de9f768497caa835a563a3ef119be994127f0'
IGNORADOS = ('schema', 'source_revision', 'translation_executed', 'evidence', 'seconds')


def injetar(metodo, modo='agrupado'):
    """Select the pass-2 hook mechanism of ``politica_comparacao_quadros`` in this process."""
    import politica_comparacao_quadros as pol
    if metodo == 'python':
        return pol
    if metodo != 'nativo':
        raise ValueError(metodo)
    import ganchos_nativos
    ganchos_nativos.carregar()      # missing or stale library: fail before any emulation

    def ganchos(b, alvos):
        return ganchos_nativos.ganchos_politica(b, alvos, modo=modo)
    pol.ganchos = ganchos
    return pol


def carregar_referencia(caminho=REFERENCIA, sha=SHA_REFERENCIA):
    bruto = Path(caminho).read_bytes()
    obtido = hashlib.sha256(bruto).hexdigest()
    if sha and obtido != sha:
        raise SystemExit(f'Reference {caminho} has sha256 {obtido}, expected {sha}')
    return json.loads(bruto), obtido


def comparar_relatorios(referencia, corpo):
    """Field-by-field comparison of a policy body with the committed report (provenance fields ignored)."""
    ref = {k: v for k, v in referencia.items() if k not in IGNORADOS}
    novo = json.loads(json.dumps({k: v for k, v in corpo.items() if k not in IGNORADOS}))
    diferentes = sorted(k for k in set(ref) | set(novo) if ref.get(k) != novo.get(k))
    glb_ref, glb = ref['game_logic_bytes'], novo.get('game_logic_bytes', {})
    return dict(
        differing_fields=diferentes,
        body_json_equal=json.dumps(ref) == json.dumps(novo),
        exclusion_mask_equal=ref['cumulative']['exclusion_mask'] == novo['cumulative']['exclusion_mask'],
        game_logic_bytes_equal=glb_ref == glb,
        game_logic_writers_readers_equal=all(glb_ref[a]['writers'] == glb.get(a, {}).get('writers') and
                                             glb_ref[a]['readers'] == glb.get(a, {}).get('readers') for a in glb_ref)
        and set(glb_ref) == set(glb),
        totals=novo['cumulative']['totals'], reference_totals=ref['cumulative']['totals'],
        surfaces_equal=ref['surfaces'] == novo['surfaces'],
        surface_verdict=dict(excluded_with_proof=novo['surfaces']['excluded_with_proof'],
                             logic_context_accesses=len(novo['surfaces']['logic_context_accesses'])),
        windows_equal=ref['windows'] == novo['windows'],
        passed=novo.get('passed'),
        result='equal' if not diferentes else 'different')


def sequencial(a):
    pol = injetar(a.metodo, a.modo)
    referencia, sha = carregar_referencia()
    saida = RAIZ / a.saida
    if '.local' not in saida.relative_to(RAIZ).parts:
        raise SystemExit('Outputs of this tool stay under .local/')
    if saida.exists():
        raise SystemExit(f'Refusing to overwrite {saida}')
    # Time each pass's bench start (program start + MissionLoad, no hooks) apart from its phase loop.
    partida, bancada = [], pol.bancada

    def bancada_medida():
        t = time.monotonic()
        b = bancada()
        partida.append(time.monotonic()-t)
        return b
    pol.bancada = bancada_medida
    t0 = time.monotonic()
    fases, alterados, resumos1, liberados = pol.passo1(a.quadros)
    t1 = time.monotonic()
    alvos, origem = pol.alvos_de(alterados)
    acessos, superficie, resumos2 = pol.passo2(a.quadros, alvos)
    t2 = time.monotonic()
    pol.bancada = bancada
    corpo = pol.relatorio(a.quadros, fases, alterados, resumos1, liberados, alvos, origem, acessos, superficie,
                          resumos2)
    comparacao = comparar_relatorios(referencia, corpo) if a.quadros == referencia['frames'] else None
    laco1, laco2 = t1-t0-partida[0], t2-t1-partida[1]
    tempos = dict(pass1_seconds=round(t1-t0, 1), pass2_seconds=round(t2-t1, 1),
                  bench_start_seconds=[round(x, 1) for x in partida],
                  pass1_phase_loop_seconds=round(laco1, 1), pass2_phase_loop_seconds=round(laco2, 1),
                  pass1_seconds_per_frame=round(laco1/a.quadros, 3), pass2_seconds_per_frame=round(laco2/a.quadros, 3),
                  note='per frame = phase loop (load_tail + every between_frames/frame) / frames; '
                       'pass 2 loop includes the per-phase image summary and, natively, the per-phase drain')
    rel = dict(schema='rising-lands/core-native-policy-hooks-run/1', method=a.metodo,
               mode=a.modo if a.metodo == 'nativo' else None, frames=a.quadros,
               reference=dict(path=str(REFERENCIA.relative_to(RAIZ)), sha256=sha), timings=tempos,
               comparison=comparacao, report=json.loads(json.dumps(corpo)))
    saida.parent.mkdir(parents=True, exist_ok=True)
    with open(saida, 'x') as f:
        json.dump(rel, f, indent=1)
        f.write('\n')
    print(json.dumps(dict(timings=tempos, comparison=comparacao), indent=1))
    return [saida], comparacao is None or comparacao['result'] == 'equal'


def segmento(a):
    import segmentos_quadros_missao as seg
    injetar(a.metodo, a.modo)
    # Time the phase loop alone (restored bench, hooks installed; per-phase collect and summary included).
    laco, fases_segmento = [], seg._fases_segmento

    def fases_medidas(*args):
        t = time.monotonic()
        yield from fases_segmento(*args)
        laco.append(time.monotonic()-t)
    seg._fases_segmento = fases_medidas
    t0 = time.monotonic()
    caminhos = seg.politica_segmento(argparse.Namespace(dir=a.dir, de=a.de, ate=a.ate,
                                                       segundos_quadro=a.segundos_quadro))
    segundos = time.monotonic()-t0
    seg._fases_segmento = fases_segmento
    tempo = RAIZ / a.dir / f'tempo-{a.de:05d}-{a.ate:05d}.json'
    tempo.write_text(json.dumps(dict(method=a.metodo, mode=a.modo if a.metodo == 'nativo' else None, segment=[a.de, a.ate], seconds=round(segundos, 1),
                                     phase_loop_seconds=round(laco[0], 1),
                                     seconds_per_frame=round(laco[0]/(a.ate-a.de), 3))) + '\n')
    print(tempo.read_text(), end='')
    return list(caminhos) + [tempo], True


def comparar(a):
    """Join a directory's policy segments (Missions' comparar_politica) and compare with the committed report."""
    import pickle
    import politica_comparacao_quadros as pol
    referencia, sha = carregar_referencia()
    pasta = RAIZ / a.dir
    p1 = pickle.loads((pasta/'politica-passo1.pickle').read_bytes())
    acessos, superficie, resumos2, partes = {}, {}, {}, []
    for p in sorted(pasta.glob('politica-0*.pickle')):
        parte = pickle.loads(p.read_bytes())
        partes.append(p.name)
        for endereco, chaves in parte['acessos'].items():
            d = acessos.setdefault(endereco, {})
            for k, n in chaves.items():
                d[k] = d.get(k, 0)+n
        for k, n in parte['superficie'].items():
            superficie[k] = superficie.get(k, 0)+n
        resumos2.update(parte['resumos'])
    corpo = pol.relatorio(p1['frames'], p1['fases'], p1['alterados'], p1['resumos'], p1['liberados'], p1['alvos'],
                          p1['origem'], acessos, superficie, resumos2)
    tempos = [json.loads(p.read_text()) for p in sorted(pasta.glob('tempo-*.json'))]
    resultado = dict(parts=partes, reference=dict(path=str(REFERENCIA.relative_to(RAIZ)), sha256=sha),
                     segment_timings=tempos,
                     seconds_per_frame=round(sum(t['phase_loop_seconds'] for t in tempos) /
                                             max(1, sum(t['segment'][1]-t['segment'][0] for t in tempos)), 3),
                     comparison=comparar_relatorios(referencia, corpo))
    (pasta/'comparacao-nativa.json').write_text(json.dumps(resultado, indent=1)+'\n')
    print(json.dumps(resultado, indent=1))
    return resultado['comparison']['result'] == 'equal'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='modo_cli', required=True)
    for nome in ('sequencial', 'segmento'):
        p = sub.add_parser(nome)
        p.add_argument('--metodo', choices=('nativo', 'python'), default='nativo')
        p.add_argument('--modo', choices=('agrupado', 'por_faixa'), default='agrupado')
        if nome == 'sequencial':
            p.add_argument('--quadros', type=int, required=True)
            p.add_argument('--saida', required=True)
        else:
            p.add_argument('--dir', required=True)
            p.add_argument('--de', type=int, required=True)
            p.add_argument('--ate', type=int, required=True)
            p.add_argument('--segundos-quadro', type=float, default=600.0)
    pc = sub.add_parser('comparar')
    pc.add_argument('--dir', required=True)
    a = ap.parse_args()
    if a.modo_cli == 'comparar':
        return 0 if comparar(a) else 1
    caminhos, ok = sequencial(a) if a.modo_cli == 'sequencial' else segmento(a)
    from encerramento_captura import encerrar_captura
    encerrar_captura(0 if ok else 1, *caminhos)


if __name__ == '__main__':
    sys.exit(main())
