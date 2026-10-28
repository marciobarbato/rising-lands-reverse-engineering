"""Run only this lifecycle slice; preserve historical aggregate reports."""
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    from validar import Resultado
    suite = unittest.defaultTestLoader.loadTestsFromNames(
        ('test_ciclo_estruturas', 'test_emulacao_ciclo_estruturas'))
    result = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(), x86_enabled=args.emular,
                  tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                  skips=[dict(test=t.id(), reason=r) for t, r in result.skipped],
                  bounded_x86_executions=result.execucoes_x86, success=result.wasSuccessful(),
                  expected_x86_exceptions=0, expected_execution_limits=0,
                  scope='Structure record lifecycle with synthetic full-pool buffers; no mission/game run.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_ciclo_estruturas import DiferencialCicloEstruturas
        bancada = getattr(DiferencialCicloEstruturas, 'bancada', None)
        report.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                      reached_stops=dict(bancada.paradas_atingidas) if bancada else {})
    destino = RAIZ / 'relatorios' / ('ciclo-estruturas-emulado.json' if args.emular else 'ciclo-estruturas-local.json')
    destino.write_text(json.dumps(report, indent=2) + '\n')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
