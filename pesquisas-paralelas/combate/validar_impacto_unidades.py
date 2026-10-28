"""Validate only the mode-1 unit wrapper; preserve earlier stage reports."""
import argparse
import json
import os
from pathlib import Path
import unittest

from validar import Resultado


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    from test_impacto_unidades import ContratosImpactoUnidades, DiferencialImpactoUnidades
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (ContratosImpactoUnidades, DiferencialImpactoUnidades))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        expected_dependency_stops=getattr(DiferencialImpactoUnidades, 'dependency_stops', {}),
        completed_projectiles=getattr(DiferencialImpactoUnidades, 'completed_projectiles', 0),
        scope='Mode-1 unit InfligeDegat wrapper; complete unit/projectile buffers, query/effect order, alert fields, five original occupied projectile completions',
        dependencies='World lookup, direction, RNG, non-AI unit message, damage and hit allocation execute natively. MAJSympathie uses native inactive return. Navigation/refuge/audio are explicit stops. Diplomacy/statistic effect bodies remain providers in Python.',
        excluded='Building damage, other damage modes, lethal effects, AI message body, navigation implementation, audio backend, real mission/game runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-impacto-unidades-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
