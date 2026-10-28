"""Provider composition plus rerun damage/wrapper with corrected bonus inputs."""
import argparse
import json
import os
from pathlib import Path
import unittest

from validar import Resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    else:
        os.environ.pop('RISING_EMULAR', None)
    import test_bonus_combate as bonus
    import test_consumo_dano as damage
    import test_impacto_unidades as impact
    classes = (bonus.ContratosBonusCombate, bonus.DiferencialBonusCombate,
        damage.ContratosConsumoDano, damage.DiferencialConsumoDano,
        impact.ContratosImpactoUnidades, impact.DiferencialImpactoUnidades)
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in classes)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(suite)
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        provider_implementation_commit='b1eb0c06e3b016f9abc2d27f3a836f6c20abf2f9',
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        completed_real_provider_consumers=getattr(bonus.DiferencialBonusCombate, 'complete_returns', 0),
        expected_death_stops=getattr(damage.DiferencialConsumoDano, 'expected_death_stops', 0),
        expected_consumer_audio_stops=getattr(damage.DiferencialConsumoDano, 'expected_audio_stops', 0),
        consumer_pipeline_checkpoints=getattr(damage.DiferencialConsumoDano, 'pipeline_checkpoints', 0),
        wrapper_dependency_stops=getattr(impact.DiferencialImpactoUnidades, 'dependency_stops', {}),
        completed_wrapper_projectiles=getattr(impact.DiferencialImpactoUnidades, 'completed_projectiles', 0),
        correction='Reference fixture now writes selector5 u16 at+08 and selector6 u8 at+0a. Predecessor reports remain historical and unchanged.',
        scope='450 complete native damage consumers composed with real committed economy queries, plus fresh damage/wrapper regressions with corrected loaded inputs',
        excluded='Bonus loading/reset, unknown inherited-ECX selectors, death/AI/audio/navigation bodies, real mission/game runtime',
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-bonus-combate-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
