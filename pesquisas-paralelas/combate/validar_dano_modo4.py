"""Validate initialized mode 4 plus mode-9/8/1 regressions in new reports."""
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
    from test_dano_modo4 import ContratosDanoModo4, DiferencialDanoModo4
    from test_dano_modo9 import ContratosDanoModo9, DiferencialDanoModo9
    from test_dano_modo8 import ContratosDanoModo8, DiferencialDanoModo8
    from test_consumo_dano import ContratosConsumoDano, DiferencialConsumoDano
    from test_consumo_fisico import ContratosConsumoFisico, DiferencialConsumoFisico
    cases = (ContratosDanoModo4, DiferencialDanoModo4, ContratosDanoModo9, DiferencialDanoModo9,
             ContratosDanoModo8, DiferencialDanoModo8, ContratosConsumoDano, DiferencialConsumoDano,
             ContratosConsumoFisico, DiferencialConsumoFisico)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        original_ranges='prefix0x4504c6..0x450588; table0x450288..0x4502f0; common original tail',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        mode4_complete_returns=getattr(DiferencialDanoModo4, 'complete_returns', 0),
        expected_mode4_death_stops=getattr(DiferencialDanoModo4, 'death_stops', 0),
        expected_mode4_audio_stops=getattr(DiferencialDanoModo4, 'audio_stops', 0),
        regression_x86=sum(t['execucoes_x86_delimitadas'] for t in r.contagens if 'test_dano_modo4.' not in t['teste']),
        scope='Mode4 loaded damage bytes for directions29/30; original signed quarter classification; common tail and mode9/8/1 regressions',
        excluded='Uninitialized mode4 directions; mode4 lethal/world caller completion or game meaning; other unsupported modes; mission/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-dano-modo4-'+('emulada' if args.emular else 'local')+'.json')
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
