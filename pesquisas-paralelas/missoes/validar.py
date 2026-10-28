#!/usr/bin/env python3
"""Run the owned missions suite; optional native checks never run implicitly."""
import argparse
import json
import os
import unittest
from ambiente_missoes import OWNED


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    args = parser.parse_args()
    if args.emular:
        os.environ['RISING_EMULAR'] = '1'
    suite = unittest.defaultTestLoader.discover(str(OWNED/'testes'), pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.emular:
        from test_carga_unidades import DiferencialCarga
        from test_cabecalho import DiferencialCabecalho
        from test_condicoes import DiferencialCondicoes
        from test_selecao_carga import DiferencialSelecaoCarga
        from test_carga_estruturas import DiferencialEstruturas
        from test_nome_missao import DiferencialNome
        from test_auxiliares import DiferencialAuxiliares
        native = DiferencialCarga.native
        prelude = DiferencialCabecalho.native
        tables = DiferencialCondicoes.native
        full_entry = DiferencialSelecaoCarga.native
        structures = DiferencialEstruturas.native
        names = DiferencialNome.native
        auxiliaries = DiferencialAuxiliares.native
        report = dict(tests=result.testsRun, skipped=len(result.skipped), errors=len(result.errors),
                      failures=len(result.failures), unit_bounded_segments=native.execucoes,
                      unit_native_fixtures=native.loads, unit_native_returns=native.returned,
                      expected_modifier_checkpoints=native.dependency_stops,
                      original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                      scope='Separate filename, prelude, indexed structure/unit, initial auxiliary and condition/objective paths; successful file I/O supplied. Native bodies unpatched; inherited state/player/bonus tables are explicit synthetic inputs. No extraction, AI, condition or mission execution.',
                      native_faults=0 if not result.errors else 'see errors; not classified',
                      real_mission_runtime_tested=False,
                      prelude_native_calls=prelude.calls, prelude_bounded_segments=prelude.execucoes,
                      prelude_checkpoint='0x42ee1c, before Chemin_Remap executes',
                      condition_table_native_calls={hex(a):v for a,v in tables.calls.items()},
                      condition_table_bounded_segments=tables.execucoes,
                      condition_evaluation_supported=False,
                      full_entry_native_fixtures=full_entry.loads,
                      full_entry_bounded_segments=full_entry.execucoes,
                      full_entry_native_returns=full_entry.returned,
                      full_entry_expected_modifier_stops=full_entry.dependency_stops,
                      structure_native_caller_fixtures=structures.calls,
                      structure_bounded_segments=structures.execucoes,
                      structure_stop_before_unit_loader=True,
                      filename_native_calls=names.calls,
                      filename_bounded_segments=names.execucoes,
                      filename_native_returns=names.returned,
                      filename_expected_query_stops=names.dependency_stops,
                      auxiliary_native_caller_fixtures=auxiliaries.calls,
                      auxiliary_bounded_segments=auxiliaries.execucoes,
                      auxiliary_stop_before_ghost_loader=True)
        (OWNED/'validacao').mkdir(exist_ok=True)
        (OWNED/'validacao/stage7-suite-x86.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
