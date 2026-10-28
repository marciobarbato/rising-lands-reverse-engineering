"""Run this bounded slice without overwriting predecessor validation reports."""
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
    from test_consumo_dano import ContratosConsumoDano, DiferencialConsumoDano
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
        for c in (ContratosConsumoDano, DiferencialConsumoDano))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(success=r.wasSuccessful(), tests=r.testsRun,
        failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens),
        per_test=r.contagens,
        expected_death_stops=getattr(DiferencialConsumoDano, 'expected_death_stops', 0),
        expected_audio_stops=getattr(DiferencialConsumoDano, 'expected_audio_stops', 0),
        pipeline_checkpoints=getattr(DiferencialConsumoDano, 'pipeline_checkpoints', 0),
        scope='Original mode 1 consumer; 800 whole unit records; callback order/arguments; live projectile buffer at consumer-return boundary',
        dependencies='Non-AI message path executed natively; volume/proximity/modifiers/visibility execute natively; audio stops at 0x48aa79 and death at 0x4506a1, no instruction replacement',
        excluded='Other damage modes, world wrapper reaction/diplomacy/presentation implementation, AI message bodies, audio backend, death, navigation, attack phase producers, whole game',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    name = 'validacao-consumo-dano-' + ('emulada' if args.emular else 'local') + '.json'
    path = Path(__file__).resolve().parent / name
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
