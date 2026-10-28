"""Record only fresh shared production caller comparisons."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA.parents[1].parent / 'source/python'))
sys.path.insert(0, str(PASTA.parents[1] / '.local/python'))
sys.path.insert(0, str(PASTA / 'testes'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    import test_producao_compartilhada
    classe = test_producao_compartilhada.DiferencialProducaoCompartilhada
    classe.bancadas = []
    r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_producao_compartilhada))
    bs = classe.bancadas
    n = sum(b.execucoes for b in bs)
    result = dict(scope='CalculTroupe actual entry through preparation, conversion and recovery; stops before experience',
        mode='original x86 and Python' if args.emular else 'Python only', tests=r.testsRun,
        failures=len(r.failures), errors=len(r.errors),
        skips=[dict(test=str(t), reason=reason) for t,reason in r.skipped],
        bounded_x86_executions=n, declared_stops=n-sum(b.excecoes_esperadas for b in bs), completed_returns=sum(b.retornos for b in bs),
        experience_dependency_stops=sum(b.paradas_experiencia for b in bs),
        bonus_query_stops=sum(b.paradas_consulta for b in bs),
        core_import_stops=sum(b.paradas_importacao for b in bs),
        expected_x86_exceptions=sum(b.excecoes_esperadas for b in bs),
        expected_x86_limits=0, success=r.wasSuccessful(),
        sha256_exe='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
    nome = 'validacao-producao-compartilhada-emulada.json' if args.emular else 'validacao-producao-compartilhada-local.json'
    (PASTA / nome).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
