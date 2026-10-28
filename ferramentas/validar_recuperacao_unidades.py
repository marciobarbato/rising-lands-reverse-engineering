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
    suite = unittest.defaultTestLoader.loadTestsFromNames(('test_recuperacao_unidades', 'test_emulacao_recuperacao_unidades'))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(), x86_enabled=args.emular, tests=r.testsRun,
                  failures=len(r.failures), errors=len(r.errors),
                  skips=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86, success=r.wasSuccessful(),
                  scope='Complete live healing/fatigue; production caller prefix stops before experience.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_recuperacao_unidades import DiferencialRecuperacaoUnidades
        b = getattr(DiferencialRecuperacaoUnidades, 'bancada', None)
        report.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                      reached_stops=dict(b.paradas_atingidas) if b else {},
                      expected_native_exceptions=0, expected_execution_limits=0,
                      expected_python_dependency_exceptions=0,
                      native_subcalls='Unpatched conversion/position/query/healing/fatigue calls')
    nome = 'recuperacao-unidades-emulada.json' if args.emular else 'recuperacao-unidades-local.json'
    (RAIZ / 'relatorios' / nome).write_text(json.dumps(report, indent=2) + '\n')
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
