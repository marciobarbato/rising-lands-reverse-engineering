"""Validate opt-in modes3/4 physical death and all affected lethal regressions."""
import argparse
import json
import os
from pathlib import Path
import unittest

from validar import Resultado


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emular', action='store_true')
    args = p.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    from test_morte_sem_experiencia import ContratosMorteSemExperiencia, DiferencialMorteSemExperiencia
    from test_morte_dano import ContratosMorteDano, DiferencialMorteDano
    from test_dano_modo3 import ContratosDanoModo3, DiferencialDanoModo3
    from test_dano_modo4 import ContratosDanoModo4, DiferencialDanoModo4
    from test_dano_modo9 import ContratosDanoModo9, DiferencialDanoModo9
    from test_dano_modo8 import ContratosDanoModo8, DiferencialDanoModo8
    from test_consumo_dano import ContratosConsumoDano, DiferencialConsumoDano
    from test_consumo_fisico import ContratosConsumoFisico, DiferencialConsumoFisico
    cases = (ContratosMorteSemExperiencia, DiferencialMorteSemExperiencia,
             ContratosMorteDano, DiferencialMorteDano, ContratosDanoModo3, DiferencialDanoModo3,
             ContratosDanoModo4, DiferencialDanoModo4, ContratosDanoModo9, DiferencialDanoModo9,
             ContratosDanoModo8, DiferencialDanoModo8, ContratosConsumoDano, DiferencialConsumoDano,
             ContratosConsumoFisico, DiferencialConsumoFisico)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        original_ranges='mode dispatch0x4506a1..0x4506b1; common lethal0x450754..0x45084f; actual SetDyingEngin0x444938',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        mode34_complete_consumers=getattr(DiferencialMorteSemExperiencia, 'complete_consumers', 0),
        expected_mode34_sympathy_stops=getattr(DiferencialMorteSemExperiencia, 'sympathy_stops', 0),
        expected_mode34_physical_stops=getattr(DiferencialMorteSemExperiencia, 'physical_stops', {}),
        regression_x86=sum(t['execucoes_x86_delimitadas'] for t in r.contagens if 'test_morte_sem_experiencia.' not in t['teste']),
        scope='Explicit modes3/4 no-award lethal callback over shared Core world, real source/bonus queries, whole physical buffers and child pool; unchanged default stops and mode8/9 boundaries',
        excluded='General sympathy/AI/audio providers, special physical completion, mode3/4 world-wrapper callers, undefined mode8/9 owner/death, mission/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-morte-sem-experiencia-'+('emulada' if args.emular else 'local')+'.json')
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
