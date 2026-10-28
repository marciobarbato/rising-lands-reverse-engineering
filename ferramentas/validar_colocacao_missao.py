"""Validate mission primitives and refactored exit without rewriting old reports."""
import argparse
import json
import os
from pathlib import Path
import platform
import sys
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'testes'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular',action='store_true')
    args = p.parse_args()
    os.environ['RISING_EMULAR'] = '1' if args.emular else '0'
    from validar import Resultado
    suite = unittest.defaultTestLoader.loadTestsFromNames(('test_colocacao_missao','test_emulacao_colocacao_missao','test_colocacao_saida'))
    r = unittest.TextTestRunner(verbosity=2,resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(),x86_enabled=args.emular,tests=r.testsRun,
                  failures=len(r.failures),errors=len(r.errors),
                  skips=[dict(test=t.id(),reason=s) for t,s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86,success=r.wasSuccessful(),
                  scope='Physical mission PlaceEngin, raw predicates and shared-tail SetSortEngin regression; no mission wrapper.')
    if args.emular:
        from emulador import HASH_ORIGINAL,unicorn
        from test_emulacao_colocacao_missao import DiferencialColocacaoMissao
        b = DiferencialColocacaoMissao.bancada
        report.update(original_sha256=HASH_ORIGINAL,unicorn=unicorn.__version__,
                      original_entries=dict(b.entradas_originais),reached_stops=dict(b.paradas_atingidas),
                      preserved_minimap_resumptions=b.retomadas_minimapa,
                      expected_native_exceptions=0,expected_execution_limits=0,
                      expected_python_dependency_exceptions=12,native_instruction_cap=1000000,
                      maximum_native_instructions_per_segment=getattr(b,'maximo_instrucoes',None),
                      failed_native_segment=getattr(b,'ultima_falha',None),
                      native_subcalls='Unpatched collision/discovery/light/minimap; same instruction/CPU/stack at each resume')
    nome = 'colocacao-missao-emulada.json' if args.emular else 'colocacao-missao-local.json'
    (RAIZ/'relatorios'/nome).write_text(json.dumps(report,indent=2)+'\n')
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
