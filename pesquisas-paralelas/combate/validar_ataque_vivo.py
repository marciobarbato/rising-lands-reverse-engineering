"""Validate the live attack chain and the reused attack/projectile regressions."""
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
    from test_ataque_vivo import ContratosAtaqueVivo, DiferencialAtaqueVivo
    from test_animacao_disparo import ContratosAnimacao, DiferencialAnimacao
    from test_maquina_projeteis import ContratosMaquina, DiferencialMaquina
    cases = (ContratosAtaqueVivo, DiferencialAtaqueVivo, ContratosAnimacao, DiferencialAnimacao,
             ContratosMaquina, DiferencialMaquina)
    r = unittest.TextTestRunner(verbosity=2, resultclass=Resultado).run(unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases))
    report = dict(success=r.wasSuccessful(), tests=r.testsRun, failures=len(r.failures), errors=len(r.errors),
        skipped=[dict(test=t.id(), reason=m) for t, m in r.skipped],
        sha256_original='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
        sha256_normalized_analysis_only='26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0',
        original_ranges=('SetAttaqueEngin 0x445a36..0x445af1; EnginNextEtape branch 0x45673b..0x4568ad (entry 0x456886, '
                         'exit 0x454ccd); declared prelude head 0x45442c..0x454591; CalculAttaqueEngin 0x451914; '
                         'ProjectileCalcul 0x46fc0f; InfligeDegat/EnginInfligeDegat/SetDyingEngin and their callees'),
        bounded_x86_executions=sum(t['execucoes_x86_delimitadas'] for t in r.contagens), per_test=r.contagens,
        lockstep_segments=getattr(DiferencialAtaqueVivo, 'segmentos', 0),
        chain_frames=getattr(DiferencialAtaqueVivo, 'quadros', 0),
        final_stops=getattr(DiferencialAtaqueVivo, 'paradas', {}),
        native_8a_writes={f'{a} -> {v}': n for (a, v), n in getattr(DiferencialAtaqueVivo, 'escritas_8a', {}).items()},
        compared_state=('Per segment: units, structures, groups, objects, every Core grid and route, projectile pool, '
                        'search/iteration/alert globals in full bytes; every other mapped page must stay unchanged'),
        regression_x86=sum(t['execucoes_x86_delimitadas'] for t in r.contagens if 'test_ataque_vivo.' not in t['teste']),
        scope=('Declared synthetic world with real loaded type/DEGAT tables: SetAttaqueEngin, branch validity, '
               'emission, live pool, ProjectileCalcul, impact, damage, retaliation and Core physical death'),
        excluded=('Full EnginNextEtape prelude/dispatcher order, AI message bodies, audio, diplomacy statistics, '
                  'movement, RNG, level experience, building-target damage, real MONDE01 placement'),
        diagnostics=[dict(test=t.id(), detail=e) for t, e in [*r.failures, *r.errors]])
    path = Path(__file__).resolve().parent / ('validacao-ataque-vivo-' + ('emulada' if args.emular else 'local') + '.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Report: {path}\nBounded x86 executions: {report["bounded_x86_executions"]}')
    raise SystemExit(not r.wasSuccessful())


if __name__ == '__main__':
    main()
