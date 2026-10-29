"""Record only the economy M2 frame comparison over the M1 state; preserve older reports."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA.parents[1] / 'ferramentas'))
sys.path.insert(0, str(PASTA / 'testes'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    import test_quadro_economia as tests
    import test_quadro1_economia as tests1
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(tests),
                                unittest.defaultTestLoader.loadTestsFromModule(tests1)])
    r = unittest.TextTestRunner(verbosity=2).run(suite)
    frozen = tests.evidencia()
    frame = tests1.evidencia()
    report = dict(
        scope='Economy routines reached by the MONDE01 M2 frames: isolated calls at the exact frame-0/1 inputs '
              'of the committed first-frame path, plus economy-only sequences and RechercheGetNbInvention over '
              'the frozen M1 post-load state; no whole-frame claim',
        mode='fresh original x86 + Python + frozen capture' if args.emular else 'Python + frozen original capture only',
        tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skips=[dict(test=str(t), reason=why) for t, why in r.skipped],
        frozen_capture=dict(path='evidencias/captura-quadro-m2-original-v2.json', scenarios=frozen['scenarios'],
                            original_entries=frozen['original_entries'], returns=frozen['returns'],
                            dependency_stops=frozen['dependency_stops']),
        exact_frame_capture=dict(path='evidencias/captura-quadro1-economia-original-v2.json',
                                 isolated_calls=len(frame['calls']), call_counts=frame['call_counts'],
                                 path_reproduction_passed=frame['path_reproduction']['passed']),
        python_calls_compared=frozen['original_entries'] + len(frame['calls']) + 1024,
        fresh_original_entries=tests.DiferencialQuadroEconomia.execucoes,
        fresh_isolated_frame_calls=tests1.DiferencialQuadro1Economia.execucoes,
        module_sha256=hashlib.sha256((PASTA / 'quadro_economia.py').read_bytes()).hexdigest(),
        success=r.wasSuccessful())
    suffix = 'emulada' if args.emular else 'local'
    (PASTA / ('validacao-quadro-economia-' + suffix + '.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
