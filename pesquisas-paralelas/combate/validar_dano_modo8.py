"""Validate mode 8 and rerun mode-1 regressions without changing old reports."""
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
    from test_dano_modo8 import ContratosDanoModo8, DiferencialDanoModo8
    from test_consumo_dano import ContratosConsumoDano, DiferencialConsumoDano
    from test_consumo_fisico import ContratosConsumoFisico, DiferencialConsumoFisico
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in
        (ContratosDanoModo8, DiferencialDanoModo8, ContratosConsumoDano,
         DiferencialConsumoDano, ContratosConsumoFisico, DiferencialConsumoFisico)))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        original_range='mode8 prefix0x450475..0x450494 and common tail in existing consumo-004502f0.asm',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        mode8_complete_returns=getattr(DiferencialDanoModo8, 'complete_returns', 0),
        expected_mode8_death_stops=getattr(DiferencialDanoModo8, 'death_stops', 0),
        expected_mode8_audio_stops=getattr(DiferencialDanoModo8, 'audio_stops', 0),
        mode1_regression_x86=sum(t['execucoes_x86_delimitadas'] for t in r.contagens if 'test_consumo_' in t['teste']),
        scope='Mode8 explicit special damage row, real loaded modifier6; common reduction/visibility/life and explicit lethal boundary; mode1 consumer/physical regressions',
        excluded='Mode8 lethal branch/uninitialized saved owner; other modes; loaded row construction/game meaning; mission/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-dano-modo8-'+('emulada' if args.emular else 'local')+'.json')
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
