"""Validate the corrected type-4 callback boundary without historical reruns."""
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
    from test_ordem_tipo4 import ContratosOrdemTipo4, DiferencialOrdemTipo4
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (ContratosOrdemTipo4, DiferencialOrdemTipo4))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        expected_modifier_stops=getattr(DiferencialOrdemTipo4, 'modifier_stops', 0),
        successful_original_returns=getattr(DiferencialOrdemTipo4, 'successful_returns', 0),
        evidence='Existing 00457350.asm: call 0x457845; frame write 0x45784c; amount write 0x457850. Callers 0x457b87 and mission checkpoint 0x46ad8b.',
        scope='Type4: live whole 276-byte records and conversion search state at original modifier12 dependency entry, plus successful owner bypass parity',
        excluded='Other type changes, economic query provider body reconstruction, mission I/O/whole loading, runtime game',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-ordem-tipo4-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
