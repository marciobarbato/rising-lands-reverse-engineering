"""Validate only the new remap prefix, keeping predecessor reports intact."""
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
    suite = unittest.defaultTestLoader.loadTestsFromNames(('test_remapeamento_mundo','test_emulacao_remapeamento_mundo'))
    r = unittest.TextTestRunner(verbosity=2,resultclass=Resultado).run(suite)
    report = dict(python=platform.python_version(),x86_enabled=args.emular,tests=r.testsRun,
                  failures=len(r.failures),errors=len(r.errors),success=r.wasSuccessful(),
                  skips=[dict(test=t.id(),reason=s) for t,s in r.skipped],
                  bounded_x86_executions=r.execucoes_x86,
                  scope='Ordered Chemin_Remap reset, stop before first GlobalAlloc; no Windows imports substituted')
    if args.emular:
        from emulador import HASH_ORIGINAL,unicorn
        from test_emulacao_remapeamento_mundo import DiferencialRemapeamentoMundo
        b = DiferencialRemapeamentoMundo.bancada
        report.update(original_sha256=HASH_ORIGINAL,unicorn=unicorn.__version__,
                      original_entries=dict(b.entradas_originais),reached_stops=dict(b.paradas_atingidas),
                      expected_native_exceptions=0,expected_execution_limits=0,
                      expected_python_dependency_exceptions=0,
                      compared_ordered_events=getattr(DiferencialRemapeamentoMundo,'eventos_ordenados',None),
                      maximum_native_instructions=getattr(b,'maximo_instrucoes',None),
                      failed_native_segment=getattr(b,'ultima_falha',None),
                      native_subcalls='Three intact memset calls, each executing its original fill leaf',
                      reached_windows_imports=0)
    nome = 'remapeamento-mundo-emulada.json' if args.emular else 'remapeamento-mundo-local.json'
    (RAIZ/'relatorios'/nome).write_text(json.dumps(report,indent=2)+'\n')
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
