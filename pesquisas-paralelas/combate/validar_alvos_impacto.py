"""Validate impact victim selection and computed lookup in projectile callers."""
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
    from test_alvos_impacto import ContratosAlvosImpacto, DiferencialAlvosImpacto
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (ContratosAlvosImpacto, DiferencialAlvosImpacto))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        completed_original_lookup_returns=getattr(DiferencialAlvosImpacto, 'lookup_returns', 0),
        completed_projectile_impacts=getattr(DiferencialAlvosImpacto, 'completed_impacts', 0),
        original_range='0x4465df..0x446693; bytes SHA256 f3a9bd57f2fd9dfe18e7db9a992250068e0cd3754c14af65a62a940b262b81b3',
        scope='Read-only impact victim query; existing combat cell geometry; exact full EAX, unchanged whole unit buffers; computed selection in five complete occupied projectile impacts',
        expected_stops='None beyond ordinary declared returns',
        excluded='Building/grid lookup, other world query/effect bodies, navigation, lethal lifecycle, real mission/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-alvos-impacto-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
