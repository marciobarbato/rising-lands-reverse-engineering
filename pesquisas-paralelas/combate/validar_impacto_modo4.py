"""Validate mode-4 cell/physical/projectile callers and all affected regressions."""
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
    cases = (ContratosImpactoModo4, DiferencialImpactoModo4, DiferencialPipelineModo4,
             ContratosImpactoUnidades, DiferencialImpactoUnidades,
             ContratosMorteSemExperiencia, DiferencialMorteSemExperiencia, ContratosMorteDano, DiferencialMorteDano,
             ContratosDanoModo3, DiferencialDanoModo3, ContratosDanoModo4, DiferencialDanoModo4,
             ContratosDanoModo9, DiferencialDanoModo9, ContratosDanoModo8, DiferencialDanoModo8,
             ContratosConsumoDano, DiferencialConsumoDano, ContratosConsumoFisico, DiferencialConsumoFisico)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        original_ranges='unit wrapper0x450a9d..0x4510d5, original ProjectileAvance/InfligeDegat, mode4 consumer and actual physical dying',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        complete_mode4_wrappers=getattr(DiferencialImpactoModo4, 'complete_impacts', 0),
        expected_wrapper_stops=getattr(DiferencialImpactoModo4, 'dependency_stops', {}),
        complete_shared_world_impacts=getattr(DiferencialPipelineModo4, 'complete_impacts', 0),
        complete_shared_world_type29_arrivals=getattr(DiferencialPipelineModo4, 'complete_projectiles', 0),
        expected_later_building_stops=getattr(DiferencialPipelineModo4, 'building_stops', 0),
        expected_shared_navigation_stops=getattr(DiferencialPipelineModo4, 'navigation_stops', 0),
        original_projectile_impact_requests=getattr(DiferencialPipelineModo4, 'projectile_requests', 0),
        original_projectile_rng_returns=getattr(DiferencialPipelineModo4, 'projectile_rng', 0),
        regression_x86=sum(t['execucoes_x86_delimitadas'] for t in r.contagens if 'test_impacto_modo4.' not in t['teste']),
        scope='Initialized mode4 unit wrapper, zero-origin evasion, shared neutral hidden ordinary world; prepared type29 arrivals/RNG/child pool/physical death and retained partial failures',
        excluded='Mode3/8/9 wrapper, building damage, general navigation/AI/audio/diplomacy/RNG provider, special physical completion, natural mission dispatch/runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-impacto-modo4-'+('emulada' if args.emular else 'local')+'.json')
    path.write_text(json.dumps(report, indent=2)+'\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
