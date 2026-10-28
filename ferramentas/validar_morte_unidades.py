"""Validate bounded physical SetDyingEngin paths and dependency stops."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'testes'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    from validar import Resultado
    suite = unittest.defaultTestLoader.loadTestsFromNames(('test_morte_unidades', 'test_emulacao_morte_unidades'))
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    dados = dict(python=platform.python_version(), x86_enabled=args.emular, tests=r.testsRun,
                 failures=len(r.failures), errors=len(r.errors),
                 skips=[dict(test=t.id(), reason=s) for t, s in r.skipped],
                 bounded_x86_executions=r.execucoes_x86, success=r.wasSuccessful(),
                 scope='Ordinary hidden-unit physical dying transition; explicit unresolved branches; no complete lifecycle/mission.')
    if args.emular:
        from emulador import HASH_ORIGINAL, unicorn
        from test_emulacao_morte_unidades import DiferencialMorteUnidades
        dados.update(original_sha256=HASH_ORIGINAL, unicorn=unicorn.__version__,
                     reached_stops=dict(DiferencialMorteUnidades.bancada.paradas_atingidas),
                     expected_native_exceptions=0, expected_execution_limits=0)
    nome = 'morte-unidades-emulada.json' if args.emular else 'morte-unidades-local.json'
    (RAIZ / 'relatorios' / nome).write_text(json.dumps(dados, indent=2) + '\n')
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
