"""Validate discovery beyond vision sum 8 plus the 0..8 insertion regressions."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ/'testes'))
MODULOS = ('test_descoberta_terreno', 'test_emulacao_descoberta_terreno', 'test_colocacao_missao',
           'test_emulacao_colocacao_missao', 'test_colocacao_saida', 'test_emulacao_colocacao_saida')


def _bancada(b):
    return dict(original_entries=dict(b.entradas_originais), reached_stops=dict(b.paradas_atingidas),
                bounded_segments=b.execucoes, preserved_minimap_resumptions=b.retomadas_minimapa,
                preserved_loop_head_resumptions=b.retomadas_laco,
                maximum_native_instructions_per_segment=getattr(b, 'maximo_instrucoes', None),
                failed_native_segment=getattr(b, 'ultima_falha', None))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    from validar import Resultado
    suite = unittest.defaultTestLoader.loadTestsFromNames(MODULOS)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(), x86_enabled=args.emular, tests=r.testsRun,
                  failures=len(r.failures), errors=len(r.errors),
                  skips=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86, success=r.wasSuccessful(),
                  scope='DecouvreTerrain/IllumineTerrain/SetMiniMap for insertion sums 9..11 and direct '
                        'radii 0..23/0..20, stops above the domain, and the existing 0..8 PlaceEngin/'
                        'SetSortEngin regression; no mission scan, structure caller or Windows runtime.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_descoberta_terreno import DiferencialDescobertaTerreno
        from test_emulacao_colocacao_missao import DiferencialColocacaoMissao
        from test_emulacao_colocacao_saida import DiferencialColocacaoSaida
        benches = dict(discovery=DiferencialDescobertaTerreno.bancada,
                       mission_regression=DiferencialColocacaoMissao.bancada,
                       exit_regression=DiferencialColocacaoSaida.bancada)
        segmentada = getattr(DiferencialColocacaoSaida, 'bancada_segmentada', None)
        if segmentada is not None:
            benches['exit_regression_segmented'] = segmentada
        report.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                      benches={k: _bancada(b) for k, b in benches.items()},
                      expected_native_exceptions=0, expected_execution_limits=0,
                      native_instruction_cap=1000000, native_segment_timeout_us=1000000,
                      native_subcalls='Unpatched collision/discovery/light/minimap; same instruction/CPU/stack '
                                      'at each SetMiniMap-entry or pixel-loop-head resume')
    nome = 'descoberta-terreno-emulada.json' if args.emular else 'descoberta-terreno-local.json'
    (RAIZ/'relatorios'/nome).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('skips', 'benches')}, indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
