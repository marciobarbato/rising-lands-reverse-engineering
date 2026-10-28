"""Record fresh structure-habitation comparisons (local or original x86)."""
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
    p.add_argument('--diagnostico-limites', nargs=2, type=int, metavar=('DESCOBERTA', 'LUZ'),
                   help='Diagnostic only: override core vision gates; separate report')
    args = p.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    import test_construcoes_habitaveis as t
    import construcoes_habitaveis as ch
    t.DiferencialHabitaveis.bancadas = []
    if args.diagnostico_limites:
        limites = tuple(args.diagnostico_limites)
        ch.limites_visao = lambda: limites
    r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(t))
    bs = t.DiferencialHabitaveis.bancadas
    entradas, resultados = {}, {}
    for b in bs:
        for k, v in b.entradas.items():
            entradas[k] = entradas.get(k, 0)+v
        for (rotulo, eip), v in b.resultados.items():
            chave = f'{rotulo}@{eip}'
            resultados[chave] = resultados.get(chave, 0)+v
    descoberta, luz = ch.limites_visao()
    result = dict(
        scope='BatimentEstHabiter 0x41a5b8, BatimentHabitable 0x41cc70 (MissionPlaceTerrain caller 0x46c195..0x46c1a7), '
              'BatimentSetTechnologie 0x41c76c and BatimentGetCase 0x41aee2 against Python on core physical state',
        mode='original x86 and Python' if args.emular else 'Python only', tests=r.testsRun,
        failures=len(r.failures), errors=len(r.errors),
        skips=[dict(test=str(x), reason=y) for x, y in r.skipped],
        core_vision_gates=dict(discovery=descoberta, light=luz,
                               overridden_for_diagnostic=bool(args.diagnostico_limites)),
        original_entries=entradas, outcomes=resultados,
        bounded_x86_executions=sum(b.execucoes for b in bs),
        preserved_minimap_resumptions=sum(b.retomadas_minimapa for b in bs),
        expected_original_division_faults=sum(b.falhas for b in bs), expected_x86_limits=0,
        success=r.wasSuccessful(), sha256_exe='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb')
    sufixo = 'emulada' if args.emular else 'local'
    if args.diagnostico_limites:
        sufixo += '-diagnostico-limites-{}-{}'.format(*args.diagnostico_limites)
    (PASTA/('validacao-habitaveis-'+sufixo+'.json')).write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    return 0 if r.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
