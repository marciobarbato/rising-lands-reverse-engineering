#!/usr/bin/env python3
"""Run the owned missions suite; optional native checks never run implicitly."""
import argparse
import json
import os
import unittest
from ambiente_missoes import OWNED


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    suite = unittest.defaultTestLoader.discover(str(OWNED/'testes'), pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.emular:
        from test_carga_unidades import DiferencialCarga
        from test_cabecalho import DiferencialCabecalho
        native = DiferencialCarga.native
        prelude = DiferencialCabecalho.native
        report = dict(tests=result.testsRun, skipped=len(result.skipped), errors=len(result.errors),
                      failures=len(result.failures), unit_bounded_segments=native.execucoes,
                      unit_native_fixtures=native.loads, unit_native_returns=native.returned,
                      expected_modifier_checkpoints=native.dependency_stops,
                      original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                      scope='Separate successful-open prelude and indexed-unit continuations; file I/O supplied. Original object normalization/resource/type/bonus/selection bodies unpatched. Inherited pools/bonus tables remain explicit synthetic inputs.',
                      native_faults=0 if not result.errors else 'see errors; not classified',
                      real_mission_runtime_tested=False,
                      prelude_native_calls=prelude.calls, prelude_bounded_segments=prelude.execucoes,
                      prelude_checkpoint='0x42ee1c, before Chemin_Remap executes')
        (OWNED/'validacao').mkdir(exist_ok=True)
        (OWNED/'validacao/stage2-suite-x86.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
