"""Validate original building-priority lookup, preserving prior reports."""
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
    from test_grade_impacto import ContratosGradeImpacto, DiferencialGradeImpacto
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (ContratosGradeImpacto, DiferencialGradeImpacto)))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        original_range='0x41b54a..0x41b579; unchanged evidencias/0041b54a.asm and manifesto.json',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        complete_queries=getattr(DiferencialGradeImpacto, 'lookup_returns', 0),
        expected_building_stops=getattr(DiferencialGradeImpacto, 'building_stops', 0),
        complete_projectiles=getattr(DiferencialGradeImpacto, 'complete_projectiles', 0),
        scope='Read-only tagged-grid building lookup; computed building/unit priority in mode1 impact; complete nonlethal projectile fixtures',
        excluded='Building damage/geometry/world initialization; general external callback bodies; other modes; mission/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-grade-impacto-'+('emulada' if args.emular else 'local')+'.json')
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
