"""Record only this bounded owner-leaf comparison; preserve older reports."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0,str(PASTA.parents[1]/'ferramentas'))
sys.path.insert(0,str(PASTA/'testes'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular',action='store_true')
    args = parser.parse_args()
    if args.emular:os.environ['RISING_EMULAR']='1'
    else:os.environ.pop('RISING_EMULAR',None)
    import test_consultas_reinicio_economia as tests
    tests.DiferencialConsultasReinicioEconomia.bancadas=[]
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
    bs=tests.DiferencialConsultasReinicioEconomia.bancadas
    report=dict(scope='Three economy IaReset leaves; exact live buffers, no whole mission claim',
                mode='fresh original x86 + Python + frozen capture' if args.emular else 'Python + frozen original capture only',
                tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),
                skips=[dict(test=str(t),reason=why) for t,why in r.skipped],
                fresh_original_entries=sum(b.execucoes for b in bs),fresh_real_returns=sum(b.retornos for b in bs),
                recorded_translated_leaf_calls=14,existing_get_player_observations=6,
                module_sha256=hashlib.sha256((PASTA/'consultas_reinicio_economia.py').read_bytes()).hexdigest(),
                success=r.wasSuccessful())
    suffix='emulada' if args.emular else 'local'
    (PASTA/('validacao-consultas-reinicio-economia-'+suffix+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
