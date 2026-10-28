"""Validate ProjectileReset 0x46e00a and the projectile-pool regression."""
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
    from test_reinicio_projeteis import ContratosReinicioProjeteis, DiferencialReinicioProjeteis
    from test_projeteis import ContratosProjeteis, DiferencialProjeteis
    cases = (ContratosReinicioProjeteis, DiferencialReinicioProjeteis, ContratosProjeteis, DiferencialProjeteis)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        sha256_normalized_analysis_only='26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0',
        original_ranges='ProjectileReset 0x46e00a..0x46e02c; CALL sites 0x46b5ac, 0x46b8c1, 0x46c373, 0x46c623',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        whole_state_comparisons=getattr(DiferencialReinicioProjeteis, 'comparacoes', 0),
        original_call_site_entries=getattr(DiferencialReinicioProjeteis, 'chamadas_originais', 0),
        compared_regions='Complete 2 MiB image (code, DGROUP, .bss, .idata) with poisoned DGROUP/.bss, 256 KiB unit area, 64 KiB stack, two 64 KiB pool regions, harness return page; registers and EFLAGS',
        regression_x86=sum(t['execucoes_x86_delimitadas'] for t in r.contagens if 'test_reinicio_projeteis.' not in t['teste']),
        scope='ProjectileReset from inherited dirty pool/global/stack/register state, direct and through the four original CALL instructions',
        excluded='Other MissionLoad reset-prefix routines and their order (missions composition), pool allocation/free, LoadProjectile/SaveProjectile, attack state machine',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-reinicio-projeteis-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
