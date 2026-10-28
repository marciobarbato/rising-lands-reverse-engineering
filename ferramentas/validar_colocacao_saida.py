"""Validate this stage without rewriting historical differential reports."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'testes'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    from validar import Resultado
    suite = unittest.defaultTestLoader.loadTestsFromNames(('test_colocacao_saida', 'test_emulacao_colocacao_saida'))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(), x86_enabled=args.emular, tests=r.testsRun,
                  failures=len(r.failures), errors=len(r.errors),
                  skips=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86, success=r.wasSuccessful(),
                  scope='Physical exit and joined movement-order caller; stops before conditional request.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_colocacao_saida import DiferencialColocacaoSaida
        b = getattr(DiferencialColocacaoSaida, 'bancada', None)
        segmentada = getattr(DiferencialColocacaoSaida, 'bancada_segmentada', None)
        report.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                      reached_stops=dict(b.paradas_atingidas) if b else {},
                      expected_native_exceptions=0, expected_execution_limits=0,
                      expected_python_dependency_exceptions_in_differential=6,
                      native_instruction_cap=1000000,
                      maximum_native_instructions_per_segment=getattr(b,'maximo_instrucoes',None),
                      failed_native_segment=getattr(b,'ultima_falha',None),
                      segmented_radius_entries=dict(segmentada.entradas_originais) if segmentada else {},
                      preserved_minimap_resumptions=segmentada.retomadas_minimapa if segmentada else 0,
                      segmented_stops=dict(segmentada.paradas_atingidas) if segmentada else {},
                      segmented_max_instructions=getattr(segmentada,'maximo_instrucoes',None),
                      interval_guard='Bisect over exact union of declared intervals; original bytes unchanged',
                      native_subcalls='Unpatched position/conversion/query/recovery/experience/collision/vision/minimap/order calls')
    nome = 'colocacao-saida-emulada.json' if args.emular else 'colocacao-saida-local.json'
    (RAIZ / 'relatorios' / nome).write_text(json.dumps(report, indent=2) + '\n')
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
