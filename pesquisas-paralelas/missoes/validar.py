#!/usr/bin/env python3
"""Run the owned missions suite; optional native checks never run implicitly."""
import argparse
import json
import os
import unittest
from caminhos import OWNED


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
        native = DiferencialCarga.native
        report = dict(tests=result.testsRun, skipped=len(result.skipped), errors=len(result.errors),
                      failures=len(result.failures), bounded_segments=native.execucoes,
                      native_loads=native.loads, native_returns=native.returned,
                      expected_modifier_checkpoints=native.dependency_stops,
                      original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                      scope='Successful indexed unit-load continuation only; real ETA blocks plus synthetic inherited state/loaded bonuses. File I/O substituted; native selection/type/bonus helpers unpatched.',
                      native_faults=0 if not result.errors else 'see errors; not classified',
                      real_mission_runtime_tested=False)
        (OWNED/'validacao').mkdir(exist_ok=True)
        (OWNED/'validacao/carga-unidades-x86.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
