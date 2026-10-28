"""Run only optional mode-1 lethal sequencing checks, preserving old reports."""
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
    from test_morte_dano import ContratosMorteDano, DiferencialMorteDano
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (ContratosMorteDano, DiferencialMorteDano))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        expected_level_stops=getattr(DiferencialMorteDano, 'level_stops', 0),
        expected_dying_stops=getattr(DiferencialMorteDano, 'dying_stops', 0),
        separate_post_dying_fragment_stops=getattr(DiferencialMorteDano, 'sympathy_fragment_stops', 0),
        projectile_dying_stops=getattr(DiferencialMorteDano, 'projectile_dying_stops', 0),
        original_range='0x4506a1..0x45084f, existing consumo-dano.json and consumo-004502f0.asm',
        scope='Optional mode1 lethal sequencing; whole units/projectile pool at level/lifecycle boundaries, separate synthetic post-lifecycle sympathy fragment',
        excluded='Level/lifecycle/sympathy provider bodies, complete lethal return, whole mission/runtime, other damage modes',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-morte-dano-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
