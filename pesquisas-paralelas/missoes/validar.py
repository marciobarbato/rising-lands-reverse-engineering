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
        from test_terreno_unidades import DiferencialTerrenoUnidades,SOMA_VISAO
        from test_cadeia_auxiliar import DiferencialCadeiaAuxiliar
        from test_reinicio_missao import DiferencialReinicio
        from test_terreno_estruturas_missao import DiferencialEstruturasMissao
        native = DiferencialCarga.native
        prelude = DiferencialCabecalho.native
        tables = DiferencialCondicoes.native
        full_entry = DiferencialSelecaoCarga.native
        structures = DiferencialEstruturas.native
        names = DiferencialNome.native
        auxiliaries = DiferencialAuxiliares.native
        placement = DiferencialTerrenoUnidades.native
        chain = DiferencialCadeiaAuxiliar.native
        reset = DiferencialReinicio.native
        structure_placement = DiferencialEstruturasMissao.native
        report = dict(tests=result.testsRun, skipped=len(result.skipped), errors=len(result.errors),
                      failures=len(result.failures), unit_bounded_segments=native.execucoes,
                      unit_native_fixtures=native.loads, unit_native_returns=native.returned,
                      expected_modifier_checkpoints=native.dependency_stops,
                      original_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
                      scope='Separate filename, prelude, indexed structure/unit, complete L7 auxiliary chain, condition/objective and unit placement-prefix paths; successful file I/O and the declared KERNEL32 profile binding supplied. Native bodies unpatched; inherited physical/player/bonus tables, data images and Random state are explicit synthetic inputs. MONDE01 placement follows the published discovery domain. No extraction, AI, monster spawning, condition or mission execution.',
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
                      auxiliary_stop_before_ghost_loader=True,
                      placement_prefix_native_fixtures=placement.prefixes,
                      placement_prefix_completed_to_structure_boundary=placement.prefix_returns,
                      placement_prefix_expected_dependency_stops=placement.prefix_dependency_stops,
                      placement_prefix_bounded_segments=placement.prefix_segments,
                      placement_fixture_unit_load_entries=placement.loads,
                      placement_fixture_unit_load_segments=placement.unit_load_segments,
                      placement_preserved_minimap_resumes=placement.retomadas_minimapa,
                      placement_stop_before_structures='0x46c16d',
                      placement_supported_vision_sum_max=SOMA_VISAO,
                      chain_native_caller_entries=chain.calls,
                      chain_native_returns=chain.returned,
                      chain_bounded_segments=chain.execucoes,
                      chain_read_bindings=chain.read_stops,
                      chain_profile_bindings=chain.profile_stops,
                      chain_declared_boundary_stops=DiferencialCadeiaAuxiliar.boundary_stops,
                      chain_failure_stops=DiferencialCadeiaAuxiliar.failure_stops,
                      chain_stop_before='FileClose 0x45844c',
                      chain_compared_image='0x494000..0x523000 DGROUP+.bss',
                      reset_native_entries=reset.entries,
                      reset_declared_stops=reset.stops,
                      reset_bounded_segments=reset.execucoes,
                      reset_compared_state='0x494000..0x523000 plus unit pool, four type Bags, projectile pool and players',
                      reset_provider_dependencies={'TerrainReset': '0x46c35f / 0x46c60f', 'RechercheReset': '0x46c68c'},
                      structure_placement_entries=structure_placement.entradas,
                      structure_placement_returns=structure_placement.retornos,
                      structure_placement_expected_stops=structure_placement.dependencias,
                      structure_placement_segments=structure_placement.execucoes,
                      structure_existence_query_entries=DiferencialEstruturasMissao.structure_queries,
                      mission_number_query_entries=DiferencialEstruturasMissao.mission_queries,
                      structure_placement_complete_mission_runtime=False)
        (OWNED/'validacao').mkdir(exist_ok=True)
        (OWNED/'validacao/stage11-suite-x86.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
