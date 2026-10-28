"""Record fresh original capacity/bonus query coverage separately from old suites."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA.parents[1].parent / 'source/python'))
sys.path.insert(0, str(PASTA.parents[1] / '.local/python'))
sys.path.insert(0, str(PASTA / 'testes'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    import test_bonus_unidades
    r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_bonus_unidades))
    n = getattr(test_bonus_unidades.DiferencialBonusUnidades.b, 'execucoes', 0)
    report = dict(scope='Complete read-only BonusGetValEngin and EnginTypeGetCapacite queries',
        mode='original x86 and Python' if args.emular else 'Python only', tests=r.testsRun,
        failures=len(r.failures), errors=len(r.errors),
        skips=[dict(test=str(t),reason=reason) for t,reason in r.skipped],
        bounded_x86_executions=n, complete_x86_returns=n, dependency_stops=0,
        expected_exceptions=0, expected_limits=0, success=r.wasSuccessful(),
        sha256_exe='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
    name = 'validacao-bonus-unidades-emulada.json' if args.emular else 'validacao-bonus-unidades-local.json'
    (PASTA / name).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
