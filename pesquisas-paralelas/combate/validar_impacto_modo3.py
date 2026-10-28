"""Validate mode-3 cell/type-1/physical callers and affected caller regressions."""
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
    from test_impacto_modo3 import ContratosImpactoModo3, DiferencialImpactoModo3, DiferencialPipelineModo3
    from test_impacto_modo4 import ContratosImpactoModo4, DiferencialImpactoModo4, DiferencialPipelineModo4
    from test_impacto_unidades import ContratosImpactoUnidades, DiferencialImpactoUnidades
    from test_morte_sem_experiencia import ContratosMorteSemExperiencia, DiferencialMorteSemExperiencia
    from test_morte_dano import ContratosMorteDano, DiferencialMorteDano
    from test_dano_modo3 import ContratosDanoModo3, DiferencialDanoModo3
    from test_dano_modo4 import ContratosDanoModo4, DiferencialDanoModo4
    from test_dano_modo9 import ContratosDanoModo9, DiferencialDanoModo9
    from test_dano_modo8 import ContratosDanoModo8, DiferencialDanoModo8
    from test_consumo_dano import ContratosConsumoDano, DiferencialConsumoDano
    from test_consumo_fisico import ContratosConsumoFisico, DiferencialConsumoFisico
    cases = (ContratosImpactoModo3, DiferencialImpactoModo3, DiferencialPipelineModo3,
             ContratosImpactoModo4, DiferencialImpactoModo4, DiferencialPipelineModo4,
             ContratosImpactoUnidades, DiferencialImpactoUnidades, ContratosMorteSemExperiencia,
             DiferencialMorteSemExperiencia, ContratosMorteDano, DiferencialMorteDano,
             ContratosDanoModo3, DiferencialDanoModo3, ContratosDanoModo4, DiferencialDanoModo4,
             ContratosDanoModo9, DiferencialDanoModo9, ContratosDanoModo8, DiferencialDanoModo8,
             ContratosConsumoDano, DiferencialConsumoDano, ContratosConsumoFisico, DiferencialConsumoFisico)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        original_ranges='mode3 source-cell0x450cef, building-owner suffix0x450e8f, msg4c guard0x482db6..0x482dbe; original type1 projectile and physical callers',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        complete_mode3_wrappers=getattr(DiferencialImpactoModo3, 'complete_impacts', 0),
        expected_wrapper_stops=getattr(DiferencialImpactoModo3, 'dependency_stops', {}),
        complete_shared_world_impacts=getattr(DiferencialPipelineModo3, 'complete_impacts', 0),
        complete_shared_world_type1_arrivals=getattr(DiferencialPipelineModo3, 'complete_projectiles', 0),
        expected_shared_navigation_stops=getattr(DiferencialPipelineModo3, 'navigation_stops', 0),
        original_projectile_impact_requests=getattr(DiferencialPipelineModo3, 'projectile_requests', 0),
        original_projectile_rng_returns=getattr(DiferencialPipelineModo3, 'projectile_rng', 0),
        synthetic_owner_mutation_cases=1 if args.emular else 0,
        regression_x86=sum(t['execucoes_x86_delimitadas'] for t in r.contagens if 'test_impacto_modo3.' not in t['teste']),
        scope='Mode3 building-cell/owner requests, message4c null-group guard, shared neutral hidden ordinary prepared type1 arrivals; explicit synthetic owner mutation; affected mode regressions',
        excluded='Building cell query body, mode8/9 wrapper, building-target damage, active AI, general navigation/audio/diplomacy/RNG providers, natural mission dispatch/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-impacto-modo3-'+('emulada' if args.emular else 'local')+'.json')
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
