"""Validate only the fixed-radius proximity provider and real query composition."""
import argparse
import json
import os
from pathlib import Path
import unittest

from validar import Resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    from test_proximidade_ataque import ContratosProximidadeAtaque, DiferencialProximidadeAtaque
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (ContratosProximidadeAtaque, DiferencialProximidadeAtaque))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        completed_original_query_returns=getattr(DiferencialProximidadeAtaque, 'proximity_returns', 0),
        completed_composed_damage_returns=getattr(DiferencialProximidadeAtaque, 'composed_damage_returns', 0),
        original_range='0x4500e4..0x450286; bytes SHA256 0584acae56bc982e07a85107b3c0948046b4b88edf378cb491d3c1e00eb1a7c9',
        scope='Radius10 owner proximity AL, unchanged complete unit/grid buffers, original unused type argument and 5 damage consumers with actual proximity/economy results',
        expected_stops='None beyond declared native returns',
        excluded='Other radii/caller domains, invalid grid IDs, physical grid construction, world effects and real mission/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-proximidade-ataque-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
