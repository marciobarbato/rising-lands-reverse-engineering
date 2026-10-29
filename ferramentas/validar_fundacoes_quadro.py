"""Validate Core frame foundations (M1 post-load input) without rewriting historical reports."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import time
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'testes'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    from validar import Resultado
    inicio = time.monotonic()
    suite = unittest.defaultTestLoader.loadTestsFromNames(('test_fundacoes_quadro', 'test_emulacao_fundacoes_quadro'))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(), x86_enabled=args.emular, tests=r.testsRun,
                  failures=len(r.failures), errors=len(r.errors),
                  skips=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86, success=r.wasSuccessful(),
                  seconds=round(time.monotonic()-inicio, 3),
                  input='M1 post-load input, not yet frame-1 input',
                  scope='GameNextFrame, Random/Randomize/SetRandomSeed/GetRandomSeed, iaRandom (all paths), '
                        'LongRand->CRT rand, ProgIteration counter prefix, CalculGame load counter reset and CD '
                        'permutation draw: frozen original replay, input protection and fresh intact differential.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_fundacoes_quadro import DiferencialFundacoesQuadro as D
        b = getattr(D, 'bancada', None)
        report.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                      original_entries=dict(b.entradas_originais) if b else {},
                      bounded_segments=b.execucoes if b else 0,
                      declared_clock_bindings=b.retomadas_vinculos if b else 0,
                      python_native_comparisons=getattr(D, 'comparacoes', 0),
                      maximum_native_instructions_per_segment=b.maximo_instrucoes if b else 0,
                      code_section_unchanged=(b.hash_codigo() == b.hash_codigo_inicial) if b else None,
                      expected_native_exceptions=0, expected_execution_limits=0, patches=0)
    nome = 'fundacoes-quadro-emulada.json' if args.emular else 'fundacoes-quadro-local.json'
    (RAIZ / 'relatorios' / nome).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'skips'}, indent=1))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
