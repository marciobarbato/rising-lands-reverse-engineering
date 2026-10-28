"""Run only the new prefix suite and record its own fresh x86 coverage."""
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    import test_saida_tropa
    classe = test_saida_tropa.DiferencialSaidaTropa
    classe.bancadas = []
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_saida_tropa)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    bs = classe.bancadas
    execucoes = sum(b.execucoes for b in bs)
    excecoes = sum(b.excecoes_esperadas for b in bs)
    relatorio = dict(scope='SortieTroupe economic prefix before CalculPosition; no world conversion',
        mode='original x86 and Python' if args.emular else 'Python only', tests=resultado.testsRun,
        failures=len(resultado.failures), errors=len(resultado.errors),
        skips=[dict(test=str(t), reason=r) for t,r in resultado.skipped],
        bounded_x86_executions=execucoes, declared_x86_stops=execucoes-excecoes,
        early_returns=sum(b.retornos_antecipados for b in bs),
        position_dependency_stops=sum(b.paradas_posicao for b in bs),
        deposit_dependency_stops=sum(b.paradas_dependencia for b in bs),
        expected_x86_exceptions=excecoes, expected_x86_limits=sum(b.limites_esperados for b in bs),
        success=resultado.wasSuccessful(),
        sha256_exe='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
    arquivo = 'validacao-saida-tropa-emulada.json' if args.emular else 'validacao-saida-tropa-local.json'
    (PASTA / arquivo).write_text(json.dumps(relatorio, indent=2) + '\n')
    print(json.dumps(relatorio, indent=2))
    return 0 if resultado.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
