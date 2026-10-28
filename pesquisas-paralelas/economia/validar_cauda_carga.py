"""Record fresh economy load-tail comparisons (local or original x86)."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(PASTA.parents[1].parent/'source/python'))
sys.path.insert(0, str(PASTA.parents[1]/'.local/python'))
sys.path.insert(0, str(PASTA/'testes'))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    import test_cauda_carga as t
    t.DiferencialCaudaCarga.bancadas = []
    r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(t))
    bs = t.DiferencialCaudaCarga.bancadas
    entradas, resultados = {}, {}
    for b in bs:
        for k, v in b.entradas.items():
            if v:
                entradas[k] = entradas.get(k, 0)+v
        for (rotulo, eip), v in b.resultados.items():
            resultados[f'{rotulo}@{eip}'] = resultados.get(f'{rotulo}@{eip}', 0)+v
    result = dict(
        scope='MissionLoad 0x46c5af..0x46c5b9 (EnginInitTechnologie, BatimentInitCave), 0x46c5be..0x46c5c3 '
              '(PlayerRetrieve), 0x46c5d1..0x46c5d6 (MarcheResetAll), MissionLoadName 0x46c978..0x46c982, '
              'direct EnginSetTechnologie and TypeBatimentEstRealisable, against Python on shared world state',
        mode='original x86 and Python' if args.emular else 'Python only', tests=r.testsRun,
        failures=len(r.failures), errors=len(r.errors), skips=[dict(test=str(x), reason=y) for x, y in r.skipped],
        original_entries=entradas, outcomes=resultados, bounded_x86_executions=sum(b.execucoes for b in bs),
        preserved_minimap_resumptions=sum(b.retomadas_minimapa for b in bs), expected_x86_exceptions=0,
        expected_x86_limits=0, success=r.wasSuccessful(),
        sha256_exe='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
    (PASTA/('validacao-cauda-carga-'+('emulada' if args.emular else 'local')+'.json')).write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
