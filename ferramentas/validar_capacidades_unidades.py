"""Validate only the original unit-capacity refresh stage."""
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
    suite = unittest.defaultTestLoader.loadTestsFromNames(('test_capacidades_unidades', 'test_emulacao_capacidades_unidades'))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(), x86_enabled=args.emular, tests=r.testsRun,
                  failures=len(r.failures), errors=len(r.errors),
                  skips=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86, success=r.wasSuccessful(),
                  scope='Existing-unit Bag-capacity word refresh; no inventory removal or real mission.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_capacidades_unidades import DiferencialCapacidadesUnidades
        b = DiferencialCapacidadesUnidades.bancada
        report.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                      reached_stops=dict(b.paradas_atingidas), native_queries=dict(b.total_consultas),
                      expected_native_exceptions=0, expected_execution_limits=0,
                      expected_python_query_exceptions=6)
    nome = 'capacidades-unidades-emulada.json' if args.emular else 'capacidades-unidades-local.json'
    (RAIZ / 'relatorios' / nome).write_text(json.dumps(report, indent=2) + '\n')
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
